"""Private P01-04E leakage-audit orchestration (FD-E-CTX-1).

Pure, deterministic, in-memory.  Reuses accepted ``_leakage_v1`` primitives
unchanged and imports no fixture-only surface.  Does not read the filesystem,
network, environment, clock, locale or process state.

Responsibilities:
- validate split and source-record identities (from caller-supplied values)
- deterministically enumerate cross-partition record pairs
- execute every ratified P01-04E detection class
- coalesce duplicate finding identities
- construct the canonical audit document

The operator owns every filesystem decision; this module sees only decoded
in-memory values.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import product
from types import MappingProxyType
from typing import Final

from medscale.mesc._canonical_json_v1 import canonical_json_bytes
from medscale.mesc._leakage_v1 import (
    CONTEXT_OVERLAP_THRESHOLD_PERCENT,
    NEAR_DUPLICATE_THRESHOLD_PERCENT,
    NORMALIZATION_RECORD,
    SCORE_REPRESENTATION_NONE,
    InvalidEvidenceReferenceError,
    LeakageAuditReport,
    LeakageFinding,
    exact_context_equality,
    exact_question_equality,
    is_empty_normalized_question_pair,
    normalize_question,
    normalized_question_equality,
    question_token_set,
    token_set_jaccard,
    tokenize,
)

AUDIT_SCHEMA_VERSION: Final = "mesc-pilot-01-leakage-audit/1"

PARTITIONS: Final[tuple[str, ...]] = ("train", "validation", "test")

PARTITION_PAIRS: Final[tuple[tuple[str, str], ...]] = (
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test"),
)

APPLIED_DETECTION_METHODS: Final[tuple[str, ...]] = (
    "exact_context_equality",
    "exact_example_identity",
    "exact_question_equality",
    "exact_source_document_identity",
    "normalized_question_equality",
    "token_set_jaccard",
)

# ---------------------------------------------------------------------------
# Audit identity contracts
# ---------------------------------------------------------------------------

_EMPTY_STRING_ERROR = "must be a non-empty string"
_EMPTY_SEQUENCE_ERROR = "must contain at least one entry"
_LOWERCASE_HEX = frozenset("0123456789abcdef")
_SHA256_LEN = 64


def _require_non_empty_str(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise LeakageAuditContractError(f"{field} {_EMPTY_STRING_ERROR}")
    return value


def _require_sha256(value: object, field: str) -> str:
    if type(value) is not str or len(value) != _SHA256_LEN:
        raise LeakageAuditContractError(f"{field} must be 64 lowercase hexadecimal characters")
    if any(ch not in _LOWERCASE_HEX for ch in value):
        raise LeakageAuditContractError(f"{field} must be lowercase hexadecimal")
    return value


def _require_positive_int(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise LeakageAuditContractError(f"{field} must be a non-negative integer")
    return value


def _require_non_empty_seq(value: object, field: str) -> tuple[object, ...]:
    if type(value) is not tuple and type(value) is not list:
        raise LeakageAuditContractError(f"{field} must be an exact tuple or list")
    seq = tuple(value)
    if not seq:
        raise LeakageAuditContractError(f"{field} {_EMPTY_SEQUENCE_ERROR}")
    return seq


# ---------------------------------------------------------------------------
# Typed errors
# ---------------------------------------------------------------------------


class LeakageAuditContractError(Exception):
    """Private fail-closed audit-orchestration contract failure."""


class AuditIdentityMismatchError(LeakageAuditContractError):
    """A supplied split or source-record identity does not match the actual content."""


class AuditInputError(LeakageAuditContractError):
    """An input outside the exact audit domain."""


class ClassificationLedgerError(LeakageAuditContractError):
    """A supplied classification ledger is invalid or inconsistent."""


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AuditSourceRecord:
    """One record with only the fields needed for leakage detection."""

    example_id: str
    original_example_id: str
    source_document_id: str
    partition: str
    question: str
    context_segments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SplitIdentityBundle:
    """Verified identity of the accepted P01-04D split the audit binds to."""

    episode_identity: str
    split_fingerprint: str
    generation_manifest_sha256: str
    generation_manifest_byte_size: int
    example_registry_sha256: str
    example_registry_byte_size: int

    def __post_init__(self) -> None:
        _require_sha256(self.episode_identity, "episode_identity")
        _require_sha256(self.split_fingerprint, "split_fingerprint")
        _require_sha256(self.generation_manifest_sha256, "generation_manifest_sha256")
        _require_positive_int(self.generation_manifest_byte_size, "generation_manifest_byte_size")
        _require_sha256(self.example_registry_sha256, "example_registry_sha256")
        _require_positive_int(self.example_registry_byte_size, "example_registry_byte_size")

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "episode_identity": self.episode_identity,
            "split_fingerprint": self.split_fingerprint,
            "generation_manifest_sha256": self.generation_manifest_sha256,
            "generation_manifest_byte_size": self.generation_manifest_byte_size,
            "example_registry_sha256": self.example_registry_sha256,
            "example_registry_byte_size": self.example_registry_byte_size,
        }


@dataclass(frozen=True, slots=True)
class SourceRecordIdentity:
    """Verified identity of the external source-records input."""

    sha256: str
    byte_size: int

    def __post_init__(self) -> None:
        _require_sha256(self.sha256, "source_records_sha256")
        _require_positive_int(self.byte_size, "source_records_byte_size")

    def to_canonical_document(self) -> dict[str, object]:
        return {"sha256": self.sha256, "byte_size": self.byte_size}


# ---------------------------------------------------------------------------
# Classification defaults
# ---------------------------------------------------------------------------

#: Finding types that auto-classify as ``confirmed_leakage`` because they
#: directly violate the split contract.  These categories are structural
#: (non-reviewable): a classification ledger may never downgrade one to
#: ``false_positive`` or ``unresolved``.
_AUTO_CONFIRMED_TYPES: Final = frozenset({"exact_example", "source_document"})


def _default_classification(finding_type: str) -> str:
    return "confirmed_leakage" if finding_type in _AUTO_CONFIRMED_TYPES else "unresolved"


# ---------------------------------------------------------------------------
# Pair enumeration
# ---------------------------------------------------------------------------


def _index_by_partition(
    records: Sequence[AuditSourceRecord],
) -> Mapping[str, tuple[AuditSourceRecord, ...]]:
    """Index records by partition, sorted by ascending original_example_id."""
    by_partition: dict[str, list[AuditSourceRecord]] = defaultdict(list)
    for record in records:
        if record.partition not in PARTITIONS:
            raise AuditInputError(f"unknown partition {record.partition!r}")
        by_partition[record.partition].append(record)
    return MappingProxyType(
        {
            partition: tuple(
                sorted(
                    partition_records,
                    key=lambda r: r.original_example_id,
                )
            )
            for partition, partition_records in by_partition.items()
        }
    )


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------


def _normalize_context_segment(value: str) -> str:
    """Apply the ratified normalization pipeline to one context segment.

    Reuses ``normalize_question`` because the pipeline (NFKC, casefold,
    whitespace collapse, trim) is identical.  The function name mentions
    "question" only because that is the primary use defined in the senior
    B2 contracts; the pipeline itself is the canonical normalization and is
    applied unchanged.
    """
    return normalize_question(value)


def _tokenize_context_segment(normalized_segment: str) -> frozenset[str]:
    """Tokenize an already-normalized context segment in the canonical way."""
    return tokenize(normalized_segment)


def _context_token_set(raw_segment: str) -> frozenset[str]:
    """Normalize then tokenize one context segment."""
    return _tokenize_context_segment(_normalize_context_segment(raw_segment))


def _unique_ids(*values: str) -> tuple[str, ...]:
    """Return unique identity values in canonical ascending order."""
    return tuple(sorted(set(values)))


# ---------------------------------------------------------------------------
# Detection dispatch
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Candidate:
    """One candidate finding before identity deduplication."""

    finding_type: str
    example_ids: tuple[str, ...]
    source_document_ids: tuple[str, ...]
    partitions: tuple[str, ...]
    score_representation: str
    shared_surface: tuple[str, ...] = ()


def _run_detection(
    indexed: Mapping[str, tuple[AuditSourceRecord, ...]],
) -> list[_Candidate]:
    """Execute every P01-04E detection class and return raw candidates."""
    candidates: list[_Candidate] = []

    for left_partition, right_partition in PARTITION_PAIRS:
        left_records = indexed.get(left_partition, ())
        right_records = indexed.get(right_partition, ())

        for left, right in product(left_records, right_records):
            left_id = left.example_id
            right_id = right.example_id
            left_oid = left.original_example_id
            right_oid = right.original_example_id
            left_sdid = left.source_document_id
            right_sdid = right.source_document_id
            example_ids = _unique_ids(left_id, right_id)
            sd_ids = _unique_ids(left_sdid, right_sdid)
            partitions = _unique_ids(left_partition, right_partition)

            # -- exact original_example_id cross-partition duplicate --
            if left_oid == right_oid:
                candidates.append(
                    _Candidate(
                        finding_type="exact_example",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=SCORE_REPRESENTATION_NONE,
                        shared_surface=("example_id",),
                    )
                )

            # -- exact source_document_id cross-partition overlap --
            if left_sdid == right_sdid:
                candidates.append(
                    _Candidate(
                        finding_type="source_document",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=SCORE_REPRESENTATION_NONE,
                        shared_surface=("source_document_id",),
                    )
                )

            # -- exact question --
            if exact_question_equality(left.question, right.question):
                candidates.append(
                    _Candidate(
                        finding_type="exact_question",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=SCORE_REPRESENTATION_NONE,
                        shared_surface=("question_bytes",),
                    )
                )

            # -- empty normalized question --
            if is_empty_normalized_question_pair(left.question, right.question):
                candidates.append(
                    _Candidate(
                        finding_type="empty_normalized_question",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation="not_evaluable",
                        shared_surface=("empty_normalized_question",),
                    )
                )

            # -- normalized question --
            if normalized_question_equality(left.question, right.question):
                candidates.append(
                    _Candidate(
                        finding_type="normalized_question",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=SCORE_REPRESENTATION_NONE,
                        shared_surface=("normalized_question",),
                    )
                )

            # -- question Jaccard >= 0.90 --
            left_qt = question_token_set(left.question)
            right_qt = question_token_set(right.question)
            qj_result = token_set_jaccard(left_qt, right_qt)
            if qj_result.near_duplicate_threshold_passed:
                candidates.append(
                    _Candidate(
                        finding_type="near_duplicate_question",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=qj_result.score_representation,
                        shared_surface=("question_token_set",),
                    )
                )

            # -- context segment comparisons --
            _detect_context_candidates(
                candidates,
                left,
                right,
                example_ids,
                partitions,
                left_sdid,
                right_sdid,
            )

    return candidates


def _detect_context_candidates(
    candidates: list[_Candidate],
    left: AuditSourceRecord,
    right: AuditSourceRecord,
    example_ids: tuple[str, ...],
    partitions: tuple[str, ...],
    left_sdid: str,
    right_sdid: str,
) -> None:
    """Run exact- and approximate-context detection on one record pair."""
    seen_exact = False
    seen_jaccard: dict[str, str] = {}
    sd_ids = _unique_ids(left_sdid, right_sdid)

    for left_seg in left.context_segments:
        for right_seg in right.context_segments:
            if exact_context_equality(left_seg, right_seg) and not seen_exact:
                candidates.append(
                    _Candidate(
                        finding_type="context_overlap",
                        example_ids=example_ids,
                        source_document_ids=sd_ids,
                        partitions=partitions,
                        score_representation=SCORE_REPRESENTATION_NONE,
                        shared_surface=("context_bytes",),
                    )
                )
                seen_exact = True

            left_cs = _context_token_set(left_seg)
            right_cs = _context_token_set(right_seg)
            cj_result = token_set_jaccard(left_cs, right_cs)
            if cj_result.context_overlap_threshold_passed:
                rep = cj_result.score_representation
                if rep not in seen_jaccard:
                    seen_jaccard[rep] = rep
                    candidates.append(
                        _Candidate(
                            finding_type="context_overlap",
                            example_ids=example_ids,
                            source_document_ids=sd_ids,
                            partitions=partitions,
                            score_representation=rep,
                            shared_surface=("context_token_set",),
                        )
                    )


# ---------------------------------------------------------------------------
# Coalescing
# ---------------------------------------------------------------------------


def _coalesce_candidates(
    candidates: Iterable[_Candidate],
) -> dict[str, _Candidate]:
    """Coalesce candidates by deterministic finding identity.

    When multiple primitive detections map to the same exact finding identity
    (same type, same example IDs, same source-document IDs, same partitions,
    same score representation), the first encountered candidate is retained and
    later duplicates are excluded.  This is safe because the identity document
    is fully semantic and carries no per-segment ordinal or detection-path
    detail.
    """
    coalesced: dict[str, _Candidate] = {}
    for candidate in candidates:
        finding_id = _derive_candidate_id(candidate)
        if finding_id not in coalesced:
            coalesced[finding_id] = candidate
    return coalesced


def _derive_candidate_id(candidate: _Candidate) -> str:
    """Derive the deterministic finding ID from a candidate's semantic fields."""
    from medscale.mesc._leakage_v1 import derive_finding_id

    return derive_finding_id(
        candidate.finding_type,
        candidate.example_ids,
        candidate.source_document_ids,
        candidate.partitions,
        candidate.score_representation,
    )


# ---------------------------------------------------------------------------
# Classification ledger
# ---------------------------------------------------------------------------


def _validate_classification_ledger(
    ledger: object,
    known_finding_ids: frozenset[str],
) -> Mapping[str, tuple[str, str | None]]:
    """Parse and validate a classification ledger.

    Returns ``{finding_id: (classification, evidence_reference)}``.
    """
    if ledger is None:
        return MappingProxyType({})

    if type(ledger) is not tuple and type(ledger) is not list:
        raise ClassificationLedgerError("classification ledger must be an exact tuple or list")

    result: dict[str, tuple[str, str | None]] = {}
    seen: set[str] = set()

    for index, entry in enumerate(tuple(ledger)):
        if not isinstance(entry, dict):
            raise ClassificationLedgerError(f"ledger entry {index} must be a dict")
        finding_id = _require_non_empty_str(entry.get("finding_id"), f"ledger[{index}].finding_id")
        classification = _require_non_empty_str(
            entry.get("classification"), f"ledger[{index}].classification"
        )

        from medscale.mesc._leakage_v1 import CLASSIFICATIONS

        if classification not in CLASSIFICATIONS:
            raise ClassificationLedgerError(
                f"ledger[{index}].classification must be one of {CLASSIFICATIONS}"
            )

        evidence_reference = entry.get("evidence_reference")
        if classification == "false_positive" and (
            evidence_reference is None
            or type(evidence_reference) is not str
            or not evidence_reference
        ):
            raise ClassificationLedgerError(
                f"ledger[{index}]: false_positive requires a non-empty evidence_reference"
            )
        if evidence_reference is not None and type(evidence_reference) is not str:
            raise ClassificationLedgerError(
                f"ledger[{index}].evidence_reference must be a string or null"
            )

        if finding_id not in known_finding_ids:
            raise ClassificationLedgerError(f"ledger[{index}]: unknown finding_id {finding_id!r}")
        if finding_id in seen:
            raise ClassificationLedgerError(f"ledger[{index}]: duplicate finding_id {finding_id!r}")
        seen.add(finding_id)
        result[finding_id] = (classification, evidence_reference)

    return MappingProxyType(result)


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def run_leakage_audit(
    records: Sequence[AuditSourceRecord],
    classification_ledger: object = None,
) -> tuple[LeakageFinding, ...]:
    """Execute every P01-04E detection class and return validated findings.

    Returns a tuple of immutable ``LeakageFinding`` instances.  Every detected
    candidate is represented; none is silently dropped.
    """
    _require_non_empty_seq(records, "records")
    for i, record in enumerate(records):
        if type(record) is not AuditSourceRecord:
            raise AuditInputError(f"records[{i}] must be an AuditSourceRecord")

    indexed = _index_by_partition(records)
    candidates = _run_detection(indexed)
    coalesced = _coalesce_candidates(candidates)

    known_ids = frozenset(coalesced)
    ledger = _validate_classification_ledger(classification_ledger, known_ids)

    findings: list[LeakageFinding] = []
    for finding_id, candidate in sorted(coalesced.items(), key=lambda item: item[0]):
        classification: str
        evidence_reference: str | None

        if finding_id in ledger:
            classification, evidence_reference = ledger[finding_id]
        else:
            classification = _default_classification(candidate.finding_type)
            evidence_reference = None

        # Structural split violations (exact_example / source_document) are
        # permanently confirmed_leakage.  An attempted ledger downgrade is an
        # invalid review ledger and fails closed; it is never silently ignored
        # or coerced back to ``confirmed_leakage``.
        if (
            candidate.finding_type in _AUTO_CONFIRMED_TYPES
            and classification != "confirmed_leakage"
        ):
            raise ClassificationLedgerError(
                f"{candidate.finding_type} is a structural split violation and cannot be "
                f"classified as {classification!r}"
            )

        score: float | None = None
        if candidate.score_representation.startswith("jaccard:"):
            fraction = candidate.score_representation[len("jaccard:") :]
            num_text, den_text = fraction.split("/")
            score = int(num_text) / int(den_text)

        try:
            finding = LeakageFinding.create(
                finding_type=candidate.finding_type,
                example_ids=candidate.example_ids,
                source_document_ids=candidate.source_document_ids,
                partitions=candidate.partitions,
                score_representation=candidate.score_representation,
                score=score,
                shared_surface=candidate.shared_surface,
                classification=classification,
                evidence_reference=evidence_reference,
            )
        except InvalidEvidenceReferenceError:
            raise
        except Exception as exc:
            raise LeakageAuditContractError(
                f"failed to construct finding {finding_id!r}: {exc}"
            ) from exc

        findings.append(finding)

    return tuple(findings)


# ---------------------------------------------------------------------------
# Audit-document construction
# ---------------------------------------------------------------------------


def build_audit_document(
    findings: Sequence[LeakageFinding],
    split_identity: SplitIdentityBundle,
    source_records_identity: SourceRecordIdentity,
) -> dict[str, object]:
    """Return the canonical P01-04E audit document.

    The document carries no path, timestamp, hostname, username, or raw
    scientific text.
    """
    if type(split_identity) is not SplitIdentityBundle:
        raise LeakageAuditContractError("split_identity must be a SplitIdentityBundle")
    if type(source_records_identity) is not SourceRecordIdentity:
        raise LeakageAuditContractError("source_records_identity must be a SourceRecordIdentity")

    report = LeakageAuditReport.create(findings, APPLIED_DETECTION_METHODS)

    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "split_identity": split_identity.to_canonical_document(),
        "source_records_identity": source_records_identity.to_canonical_document(),
        "thresholds": {
            "question_near_duplicate_jaccard_percent": NEAR_DUPLICATE_THRESHOLD_PERCENT,
            "context_overlap_jaccard_percent": CONTEXT_OVERLAP_THRESHOLD_PERCENT,
        },
        "detection_methods": list(APPLIED_DETECTION_METHODS),
        "normalization_record": dict(NORMALIZATION_RECORD),
        "finding_count": report.finding_count,
        "findings": [f.to_canonical_document() for f in report.findings],
        "leaked": report.leaked,
    }


def canonical_audit_bytes(
    findings: Sequence[LeakageFinding],
    split_identity: SplitIdentityBundle,
    source_records_identity: SourceRecordIdentity,
) -> bytes:
    """Return the canonical bytes of the audit document."""
    document = build_audit_document(findings, split_identity, source_records_identity)
    return canonical_json_bytes(document)
