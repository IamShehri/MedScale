"""Deterministic P01-05 B1 evidence-cue domain (private).

Implements the ratified B1 supplied-evidence channel (FD-P01-05-B1-EVIDENCE-1):
manual, label-blind, deterministic evidence-cue annotations over the native
PubMedQA context.

This module is pure and fail-closed. It contains no filesystem roots, no
network access, no retrieval, and no model access. The tooling contracts here
cannot even represent gold decisions, long answers, or other label material:
``B1SourceRecord`` and ``B1AnnotationInput`` accept only identity, question and
ordered native context segments, and the annotation view serialization
explicitly rejects any prohibited field name.
"""

from __future__ import annotations

import contextlib
import hashlib
import itertools
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from medscale.mesc._split_v1 import (
    PARTITIONS,
    Partition,
    canonical_json_bytes,
    sha256_hexdigest,
)

__all__ = [
    "ANNOTATION_PROTOCOL_VERSION",
    "ANNOTATION_VIEW_SCHEMA_VERSION",
    "DEVELOPMENT_SUBSET_SCHEMA_VERSION",
    "DEVELOPMENT_SUBSET_SIZE",
    "EVIDENCE_CUE_SCHEMA_VERSION",
    "EVIDENCE_ID_PREFIX",
    "EVIDENCE_PACK_SCHEMA_VERSION",
    "EXAMPLE_REGISTRY_SCHEMA_VERSION",
    "SUBSET_DOMAIN_SEPARATOR",
    "VALIDATION_POPULATION",
    "AnnotationStatus",
    "B1AdjudicationSubmission",
    "B1AnnotationComparison",
    "B1AnnotationInput",
    "B1AnnotationSubmission",
    "B1EvidenceCue",
    "B1EvidenceError",
    "B1EvidencePack",
    "B1EvidenceReferenceError",
    "B1EvidenceValidationError",
    "B1SourceRecord",
    "DevelopmentSubsetSelection",
    "ExampleRegistryRow",
    "SegmentReference",
    "build_evidence_pack",
    "build_final_cue_from_adjudication",
    "build_final_cue_from_agreement",
    "compare_annotations",
    "cue_from_document",
    "cue_to_document",
    "derive_evidence_id",
    "load_b1_source_records_from_bytes",
    "load_b1_source_records_from_path",
    "load_b1_source_records_from_records",
    "load_example_registry_from_bytes",
    "load_example_registry_from_path",
    "make_adjudication_submission",
    "make_annotation_submission",
    "pack_from_document",
    "pack_to_document",
    "render_annotation_view",
    "segment_sha256",
    "select_development_subset",
    "subset_manifest_document",
    "subset_ordering_key",
    "validate_evidence_cue",
    "validate_evidence_pack",
    "validate_view_has_no_prohibited_fields",
    "write_evidence_pack",
    "write_subset_manifest",
]

EVIDENCE_CUE_SCHEMA_VERSION = "mesc-pilot-01-b1-evidence-cue/1"
ANNOTATION_PROTOCOL_VERSION = "mesc-pilot-01-b1-annotation/1"
ANNOTATION_VIEW_SCHEMA_VERSION = "mesc-pilot-01-b1-annotation-view/1"
DEVELOPMENT_SUBSET_SCHEMA_VERSION = "mesc-pilot-01-b1-development-subset/1"
EVIDENCE_PACK_SCHEMA_VERSION = "mesc-pilot-01-b1-evidence-pack/1"
EXAMPLE_REGISTRY_SCHEMA_VERSION = "mesc-pilot-01-example-registry/1"
SUBSET_DOMAIN_SEPARATOR = "mesc-pilot-01-b1-evidence-subset/1"
EVIDENCE_ID_PREFIX = "mesc-b1-evidence:"

VALIDATION_POPULATION = 150
DEVELOPMENT_SUBSET_SIZE = 100

AnnotationStatus = Literal["AVAILABLE", "INSUFFICIENT", "AMBIGUOUS"]
ReviewStatus = Literal["UNREVIEWED", "UNRESOLVED", "AGREED", "ADJUDICATED", "FINAL"]
ComparisonOutcome = Literal["AGREED", "ADJUDICATION_REQUIRED"]

_ANNOTATION_STATUSES: tuple[AnnotationStatus, ...] = ("AVAILABLE", "INSUFFICIENT", "AMBIGUOUS")
_REVIEW_STATUSES: tuple[ReviewStatus, ...] = (
    "UNREVIEWED",
    "UNRESOLVED",
    "AGREED",
    "ADJUDICATED",
    "FINAL",
)

#: Field names that must never appear in any serialized annotation view.
PROHIBITED_VIEW_FIELD_NAMES: tuple[str, ...] = (
    "gold_decision",
    "decision",
    "final_decision",
    "long_answer",
    "answer",
    "gold_claims",
    "b0_prediction",
    "b1_prediction",
    "model_confidence",
    "split_performance",
    "test_result",
    "test_results",
)

_SOURCE_RECORD_KEYS: frozenset[str] = frozenset(
    {"example_id", "source_document_id", "question", "context"}
)
_REGISTRY_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "example_id",
        "source_document_id",
        "assigned_split",
        "partition_key",
        "row_ordinal",
    }
)


class B1EvidenceError(ValueError):
    """Base error for the B1 evidence-cue domain."""


class B1EvidenceValidationError(B1EvidenceError):
    """A cue, submission, pack, or manifest record is invalid."""


class B1EvidenceReferenceError(B1EvidenceError):
    """A segment reference cannot be resolved or its hash does not match."""


@dataclass(frozen=True, slots=True)
class SegmentReference:
    """Deterministic binding: source_document_id + zero-based context segment index."""

    source_document_id: str
    context_segment_index: int


@dataclass(frozen=True, slots=True)
class B1SourceRecord:
    """Label-free source record: identity + question + ordered native context.

    Gold decisions, long answers, and any other label material cannot be
    represented by this type and are rejected by the loader.
    """

    example_id: str
    source_document_id: str
    question: str
    context: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class B1AnnotationInput:
    """The only input an annotator may see: identity, question, context."""

    example_id: str
    source_document_id: str
    question: str
    context: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class B1AnnotationSubmission:
    """One pseudonymous annotator's evidence SELECTION.

    Contains no rationale, no proposed answer, no yes/no/maybe, no claims, and
    no summary. ``reviewer_id`` is a stable pseudonymous reviewer role and is
    excluded from every scientific evidence identity.
    """

    reviewer_id: str
    example_id: str
    source_document_id: str
    selected_segment_indices: tuple[int, ...]
    annotation_status: AnnotationStatus
    annotation_protocol_version: str = ANNOTATION_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True)
class B1AdjudicationSubmission:
    """One label-blind human adjudicator's evidence SELECTION."""

    reviewer_id: str
    example_id: str
    source_document_id: str
    selected_segment_indices: tuple[int, ...]
    annotation_status: AnnotationStatus
    annotation_protocol_version: str = ANNOTATION_PROTOCOL_VERSION


@dataclass(frozen=True, slots=True)
class B1AnnotationComparison:
    """Deterministic A/B comparison; never invents a consensus."""

    example_id: str
    source_document_id: str
    outcome: ComparisonOutcome
    submission_a: B1AnnotationSubmission
    submission_b: B1AnnotationSubmission


@dataclass(frozen=True, slots=True)
class B1EvidenceCue:
    """The final scientific evidence cue (review-complete, identity-bound)."""

    schema_version: str
    evidence_id: str
    example_id: str
    source_document_id: str
    ordered_segment_references: tuple[SegmentReference, ...]
    ordered_segment_sha256s: tuple[str, ...]
    annotation_status: AnnotationStatus
    annotation_protocol_version: str
    review_status: ReviewStatus


@dataclass(frozen=True, slots=True)
class B1EvidencePack:
    """Identity-bound collection: manifest metadata + exactly one cue per example."""

    schema_version: str
    annotation_protocol_version: str
    source_split_fingerprint: str
    subset_digest: str
    cues: tuple[B1EvidenceCue, ...]
    pack_sha256: str
    record_count: int


@dataclass(frozen=True, slots=True)
class ExampleRegistryRow:
    """Identity-only row of the canonical P01-04 example registry.

    Deliberately label-free: the subset-selection algorithm can never read a
    decision from this type.
    """

    example_id: str
    source_document_id: str
    assigned_split: Partition
    partition_key: str
    row_ordinal: int


@dataclass(frozen=True, slots=True)
class DevelopmentSubsetSelection:
    """Deterministic prospective manifest of the future development subset."""

    schema_version: str
    source_split_fingerprint: str
    example_registry_sha256: str
    selection_domain_separator: str
    validation_population: int
    selected_count: int
    ordered_selected_example_ids: tuple[str, ...]
    ordered_selected_source_document_ids: tuple[str, ...]
    ordered_selection_keys: tuple[str, ...]
    subset_digest: str


def segment_sha256(segment: str) -> str:
    """SHA-256 of the exact UTF-8 bytes of one native context segment.

    No Unicode normalization, whitespace trimming, case folding, newline
    rewriting, or semantic normalization is applied before hashing.
    """
    return hashlib.sha256(segment.encode("utf-8")).hexdigest()


def subset_ordering_key(example_id: str) -> str:
    """Canonical domain-separated ordering key for the development subset.

    ``SHA-256(UTF8("mesc-pilot-01-b1-evidence-subset/1" + ":" + example_id))``
    """
    if not isinstance(example_id, str) or not example_id.strip():
        raise B1EvidenceValidationError("example_id must be a non-blank string")
    payload = (SUBSET_DOMAIN_SEPARATOR + ":" + example_id).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_nonblank_str(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise B1EvidenceValidationError(f"{field} must be a non-blank string")
    return value


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise B1EvidenceValidationError(f"duplicate JSON key: {key!r}")
        seen.add(key)
    return dict(pairs)


def _require_indices(value: object, field: str) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise B1EvidenceValidationError(f"{field} must be a list of non-negative integers")
    indices: list[int] = []
    for index, item in enumerate(value):
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise B1EvidenceValidationError(f"{field}[{index}] must be a non-negative integer")
        indices.append(item)
    for previous, current in itertools.pairwise(indices):
        if previous >= current:
            raise B1EvidenceValidationError(
                f"{field} must be strictly increasing (canonical segment order); got {indices}"
            )
    return tuple(indices)


def _require_status(value: object) -> AnnotationStatus:
    if value not in _ANNOTATION_STATUSES:
        raise B1EvidenceValidationError(
            f"annotation_status must be one of {_ANNOTATION_STATUSES}, got {value!r}"
        )
    for candidate in _ANNOTATION_STATUSES:
        if value == candidate:
            return candidate
    raise B1EvidenceValidationError(
        f"annotation_status must be one of {_ANNOTATION_STATUSES}, got {value!r}"
    )


def _require_review_status(value: object) -> ReviewStatus:
    if value not in _REVIEW_STATUSES:
        raise B1EvidenceValidationError(
            f"review_status must be one of {_REVIEW_STATUSES}, got {value!r}"
        )
    for candidate in _REVIEW_STATUSES:
        if value == candidate:
            return candidate
    raise B1EvidenceValidationError(
        f"review_status must be one of {_REVIEW_STATUSES}, got {value!r}"
    )


# ---------------------------------------------------------------------------
# Source records (label-free)
# ---------------------------------------------------------------------------


def _source_record_from_object(obj: Mapping[str, object]) -> B1SourceRecord:
    keys = set(obj)
    missing = sorted(_SOURCE_RECORD_KEYS - keys)
    unexpected = sorted(keys - _SOURCE_RECORD_KEYS)
    if missing or unexpected:
        raise B1EvidenceValidationError(
            f"source record fields must be exactly {sorted(_SOURCE_RECORD_KEYS)}; "
            f"missing={missing}, unexpected={unexpected}"
        )
    context = obj["context"]
    if not isinstance(context, list):
        raise B1EvidenceValidationError("context must be a list of strings")
    segments: list[str] = []
    for index, segment in enumerate(context):
        if not isinstance(segment, str):
            raise B1EvidenceValidationError(f"context[{index}] must be a string")
        segments.append(segment)
    return B1SourceRecord(
        example_id=_require_nonblank_str(obj["example_id"], "example_id"),
        source_document_id=_require_nonblank_str(obj["source_document_id"], "source_document_id"),
        question=_require_nonblank_str(obj["question"], "question"),
        context=tuple(segments),
    )


def load_b1_source_records_from_records(
    records: Sequence[Mapping[str, object]],
) -> tuple[B1SourceRecord, ...]:
    """Load label-free B1 source records from an in-memory sequence."""
    parsed = [_source_record_from_object(obj) for obj in records]
    return _assemble_source_records(parsed)


def _assemble_source_records(records: Sequence[B1SourceRecord]) -> tuple[B1SourceRecord, ...]:
    if not records:
        raise B1EvidenceValidationError("source records must contain at least one record")
    seen: set[str] = set()
    for record in records:
        if record.example_id in seen:
            raise B1EvidenceValidationError(f"duplicate example_id: {record.example_id}")
        seen.add(record.example_id)
    return tuple(records)


def load_b1_source_records_from_bytes(data: bytes) -> tuple[B1SourceRecord, ...]:
    """Load label-free B1 source records from raw JSONL bytes."""
    if not isinstance(data, bytes | bytearray):
        raise B1EvidenceValidationError("source records must be bytes")
    raw = bytes(data)
    if raw.startswith(b"\xef\xbb\xbf"):
        raise B1EvidenceValidationError(
            "input begins with a UTF-8 byte-order mark (BOM); remove the BOM"
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise B1EvidenceValidationError(f"input is not valid UTF-8: {exc}") from exc
    parsed: list[B1SourceRecord] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except json.JSONDecodeError as exc:
            raise B1EvidenceValidationError(f"line {line_number}: malformed JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise B1EvidenceValidationError(
                f"line {line_number}: each record must be a JSON object"
            )
        parsed.append(_source_record_from_object(obj))
    return _assemble_source_records(parsed)


def load_b1_source_records_from_path(path: Path) -> tuple[B1SourceRecord, ...]:
    """Load label-free B1 source records from an explicit caller-supplied path."""
    return load_b1_source_records_from_bytes(path.read_bytes())


# ---------------------------------------------------------------------------
# Annotation view (label-blind)
# ---------------------------------------------------------------------------


def annotation_input_from_source_record(record: B1SourceRecord) -> B1AnnotationInput:
    """The annotator view input is derived only from label-free fields."""
    return B1AnnotationInput(
        example_id=record.example_id,
        source_document_id=record.source_document_id,
        question=record.question,
        context=record.context,
    )


def validate_view_has_no_prohibited_fields(value: object) -> None:
    """Recursively refuse any serialized annotation view containing a prohibited field."""
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in PROHIBITED_VIEW_FIELD_NAMES:
                raise B1EvidenceValidationError(
                    f"annotation view contains prohibited field: {key!r}"
                )
            validate_view_has_no_prohibited_fields(item)
    elif isinstance(value, list):
        for item in value:
            validate_view_has_no_prohibited_fields(item)


def render_annotation_view(view_input: B1AnnotationInput) -> dict[str, object]:
    """Serialize the deterministic label-blind annotation view.

    Contains only example identity, source-document identity, question, and
    ordered native context segments.
    """
    document: dict[str, object] = {
        "schema_version": ANNOTATION_VIEW_SCHEMA_VERSION,
        "example_id": view_input.example_id,
        "source_document_id": view_input.source_document_id,
        "question": view_input.question,
        "context": list(view_input.context),
    }
    validate_view_has_no_prohibited_fields(document)
    return document


# ---------------------------------------------------------------------------
# Submissions, comparison, adjudication
# ---------------------------------------------------------------------------


def make_annotation_submission(
    *,
    reviewer_id: str,
    example_id: str,
    source_document_id: str,
    selected_segment_indices: Sequence[int],
    annotation_status: str,
) -> B1AnnotationSubmission:
    """Validate and construct one pseudonymous annotator submission."""
    status = _require_status(annotation_status)
    indices = _require_indices(list(selected_segment_indices), "selected_segment_indices")
    _require_status_index_consistency(status, indices)
    return B1AnnotationSubmission(
        reviewer_id=_require_nonblank_str(reviewer_id, "reviewer_id"),
        example_id=_require_nonblank_str(example_id, "example_id"),
        source_document_id=_require_nonblank_str(source_document_id, "source_document_id"),
        selected_segment_indices=indices,
        annotation_status=status,
        annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
    )


def make_adjudication_submission(
    *,
    reviewer_id: str,
    example_id: str,
    source_document_id: str,
    selected_segment_indices: Sequence[int],
    annotation_status: str,
) -> B1AdjudicationSubmission:
    """Validate and construct one label-blind human adjudication submission."""
    status = _require_status(annotation_status)
    indices = _require_indices(list(selected_segment_indices), "selected_segment_indices")
    _require_status_index_consistency(status, indices)
    return B1AdjudicationSubmission(
        reviewer_id=_require_nonblank_str(reviewer_id, "reviewer_id"),
        example_id=_require_nonblank_str(example_id, "example_id"),
        source_document_id=_require_nonblank_str(source_document_id, "source_document_id"),
        selected_segment_indices=indices,
        annotation_status=status,
        annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
    )


def _require_status_index_consistency(status: AnnotationStatus, indices: tuple[int, ...]) -> None:
    if status == "AVAILABLE" and not indices:
        raise B1EvidenceValidationError(
            "AVAILABLE annotation requires at least one selected segment index"
        )
    if status in ("INSUFFICIENT", "AMBIGUOUS") and indices:
        raise B1EvidenceValidationError(
            f"{status} annotation must have no selected segment indices; got {indices}"
        )


def compare_annotations(
    submission_a: B1AnnotationSubmission,
    submission_b: B1AnnotationSubmission,
) -> B1AnnotationComparison:
    """Deterministic A/B comparison: exact agreement or adjudication required.

    Never invents a consensus, never prefers an annotator, never majority-votes.
    """
    if submission_a.example_id != submission_b.example_id:
        raise B1EvidenceValidationError(
            "cannot compare submissions for different example_ids: "
            f"{submission_a.example_id!r} vs {submission_b.example_id!r}"
        )
    if submission_a.source_document_id != submission_b.source_document_id:
        raise B1EvidenceValidationError(
            "cannot compare submissions for different source_document_ids: "
            f"{submission_a.source_document_id!r} vs {submission_b.source_document_id!r}"
        )
    if submission_a.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1EvidenceValidationError(
            f"submission A protocol must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {submission_a.annotation_protocol_version!r}"
        )
    if submission_b.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1EvidenceValidationError(
            f"submission B protocol must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {submission_b.annotation_protocol_version!r}"
        )
    agreed = (
        submission_a.annotation_status == submission_b.annotation_status
        and submission_a.selected_segment_indices == submission_b.selected_segment_indices
    )
    outcome: ComparisonOutcome = "AGREED" if agreed else "ADJUDICATION_REQUIRED"
    return B1AnnotationComparison(
        example_id=submission_a.example_id,
        source_document_id=submission_a.source_document_id,
        outcome=outcome,
        submission_a=submission_a,
        submission_b=submission_b,
    )


# ---------------------------------------------------------------------------
# Evidence identity and final cues
# ---------------------------------------------------------------------------


def derive_evidence_id(
    *,
    schema_version: str,
    example_id: str,
    source_document_id: str,
    annotation_status: str,
    ordered_segment_references: Sequence[SegmentReference],
    ordered_segment_sha256s: Sequence[str],
    annotation_protocol_version: str,
) -> str:
    """Deterministic domain-separated evidence identity.

    ``"mesc-b1-evidence:" + SHA-256(canonical identity payload)``. Reviewer
    identity, timestamps, hostnames, workspace paths, random UUIDs, and process
    IDs are never part of the payload.
    """
    payload = {
        "schema_version": schema_version,
        "example_id": example_id,
        "source_document_id": source_document_id,
        "annotation_status": annotation_status,
        "ordered_segment_references": [
            {
                "source_document_id": reference.source_document_id,
                "context_segment_index": reference.context_segment_index,
            }
            for reference in ordered_segment_references
        ],
        "ordered_segment_sha256s": list(ordered_segment_sha256s),
        "annotation_protocol_version": annotation_protocol_version,
    }
    return EVIDENCE_ID_PREFIX + sha256_hexdigest(payload)


def _final_cue_from_selection(
    *,
    status: AnnotationStatus,
    indices: tuple[int, ...],
    example_id: str,
    source_document_id: str,
    context: Sequence[str],
) -> B1EvidenceCue:
    _require_status_index_consistency(status, indices)
    if example_id != _require_nonblank_str(example_id, "example_id"):
        raise B1EvidenceValidationError("example_id must be a non-blank string")
    references: list[SegmentReference] = []
    hashes: list[str] = []
    for index in indices:
        if index < 0 or index >= len(context):
            raise B1EvidenceReferenceError(
                f"segment index {index} out of range for context of size {len(context)}"
            )
        segment = context[index]
        if not isinstance(segment, str):
            raise B1EvidenceReferenceError(f"context[{index}] must be a string")
        references.append(
            SegmentReference(source_document_id=source_document_id, context_segment_index=index)
        )
        hashes.append(segment_sha256(segment))
    evidence_id = derive_evidence_id(
        schema_version=EVIDENCE_CUE_SCHEMA_VERSION,
        example_id=example_id,
        source_document_id=source_document_id,
        annotation_status=status,
        ordered_segment_references=references,
        ordered_segment_sha256s=hashes,
        annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
    )
    return B1EvidenceCue(
        schema_version=EVIDENCE_CUE_SCHEMA_VERSION,
        evidence_id=evidence_id,
        example_id=example_id,
        source_document_id=source_document_id,
        ordered_segment_references=tuple(references),
        ordered_segment_sha256s=tuple(hashes),
        annotation_status=status,
        annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
        review_status="FINAL",
    )


def build_final_cue_from_agreement(
    comparison: B1AnnotationComparison,
    *,
    source_record: B1SourceRecord,
) -> B1EvidenceCue:
    """A final cue may be built from exact A/B agreement only.

    A comparison marked ADJUDICATION_REQUIRED is refused; the software never
    invents a consensus.
    """
    if comparison.outcome != "AGREED":
        raise B1EvidenceValidationError(
            "cannot build a final cue from a non-AGREED comparison; human adjudication is required"
        )
    submission = comparison.submission_a
    if (
        submission.example_id != source_record.example_id
        or submission.source_document_id != source_record.source_document_id
    ):
        raise B1EvidenceValidationError(
            "agreed submission does not match the source record identity"
        )
    return _final_cue_from_selection(
        status=submission.annotation_status,
        indices=submission.selected_segment_indices,
        example_id=submission.example_id,
        source_document_id=submission.source_document_id,
        context=source_record.context,
    )


def build_final_cue_from_adjudication(
    adjudication: B1AdjudicationSubmission,
    *,
    source_record: B1SourceRecord,
) -> B1EvidenceCue:
    """A final cue may be built from a valid human adjudication submission."""
    if adjudication.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1EvidenceValidationError(
            f"adjudication protocol must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {adjudication.annotation_protocol_version!r}"
        )
    if (
        adjudication.example_id != source_record.example_id
        or adjudication.source_document_id != source_record.source_document_id
    ):
        raise B1EvidenceValidationError("adjudication does not match the source record identity")
    return _final_cue_from_selection(
        status=adjudication.annotation_status,
        indices=adjudication.selected_segment_indices,
        example_id=adjudication.example_id,
        source_document_id=adjudication.source_document_id,
        context=source_record.context,
    )


# ---------------------------------------------------------------------------
# Cue serialization and validation
# ---------------------------------------------------------------------------


def _segment_reference_from_object(obj: Mapping[str, object]) -> SegmentReference:
    if set(obj) != {"source_document_id", "context_segment_index"}:
        raise B1EvidenceValidationError(
            f"segment reference fields must be exactly "
            f"{['context_segment_index', 'source_document_id']}; got {sorted(obj)}"
        )
    index = obj["context_segment_index"]
    if not isinstance(index, int) or isinstance(index, bool) or index < 0:
        raise B1EvidenceValidationError("context_segment_index must be a non-negative integer")
    return SegmentReference(
        source_document_id=_require_nonblank_str(obj["source_document_id"], "source_document_id"),
        context_segment_index=index,
    )


def cue_to_document(cue: B1EvidenceCue) -> dict[str, object]:
    """Deterministic serializable form of one final evidence cue (no raw text)."""
    return {
        "schema_version": cue.schema_version,
        "evidence_id": cue.evidence_id,
        "example_id": cue.example_id,
        "source_document_id": cue.source_document_id,
        "ordered_segment_references": [
            {
                "source_document_id": reference.source_document_id,
                "context_segment_index": reference.context_segment_index,
            }
            for reference in cue.ordered_segment_references
        ],
        "ordered_segment_sha256s": list(cue.ordered_segment_sha256s),
        "annotation_status": cue.annotation_status,
        "annotation_protocol_version": cue.annotation_protocol_version,
        "review_status": cue.review_status,
    }


def cue_from_document(document: Mapping[str, object]) -> B1EvidenceCue:
    """Parse one final evidence cue from its deterministic document form."""
    expected = set(
        cue_to_document(
            B1EvidenceCue(
                schema_version=EVIDENCE_CUE_SCHEMA_VERSION,
                evidence_id="",
                example_id="",
                source_document_id="",
                ordered_segment_references=(),
                ordered_segment_sha256s=(),
                annotation_status="AVAILABLE",
                annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
                review_status="FINAL",
            )
        )
    )
    if set(document) != expected:
        raise B1EvidenceValidationError(
            f"cue fields must be exactly {sorted(expected)}; got {sorted(document)}"
        )
    refs_value = document["ordered_segment_references"]
    if not isinstance(refs_value, list):
        raise B1EvidenceValidationError("ordered_segment_references must be a list")
    references = tuple(_segment_reference_from_object(item) for item in refs_value)
    hashes_value = document["ordered_segment_sha256s"]
    if not isinstance(hashes_value, list) or not all(
        isinstance(item, str) and len(item) == 64 for item in hashes_value
    ):
        raise B1EvidenceValidationError(
            "ordered_segment_sha256s must be a list of 64-hex SHA-256 strings"
        )
    return B1EvidenceCue(
        schema_version=_require_nonblank_str(document["schema_version"], "schema_version"),
        evidence_id=_require_nonblank_str(document["evidence_id"], "evidence_id"),
        example_id=_require_nonblank_str(document["example_id"], "example_id"),
        source_document_id=_require_nonblank_str(
            document["source_document_id"], "source_document_id"
        ),
        ordered_segment_references=references,
        ordered_segment_sha256s=tuple(hashes_value),
        annotation_status=_require_status(document["annotation_status"]),
        annotation_protocol_version=_require_nonblank_str(
            document["annotation_protocol_version"], "annotation_protocol_version"
        ),
        review_status=_require_review_status(document["review_status"]),
    )


def validate_evidence_cue(cue: B1EvidenceCue, context: Sequence[str]) -> None:
    """Fail-closed full validation of one evidence cue against its native context.

    Draft or unresolved review records fail closed. Every referenced segment is
    resolved and every SHA-256 is verified against the exact local context.
    """
    if cue.schema_version != EVIDENCE_CUE_SCHEMA_VERSION:
        raise B1EvidenceValidationError(
            f"cue schema_version must be {EVIDENCE_CUE_SCHEMA_VERSION!r}, "
            f"got {cue.schema_version!r}"
        )
    if cue.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1EvidenceValidationError(
            f"cue annotation_protocol_version must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {cue.annotation_protocol_version!r}"
        )
    if cue.review_status != "FINAL":
        raise B1EvidenceValidationError(
            f"cue review_status must be FINAL before B1 execution; got {cue.review_status!r}"
        )
    if not cue.example_id.strip() or not cue.source_document_id.strip():
        raise B1EvidenceValidationError("cue example_id and source_document_id must be non-blank")
    if cue.annotation_status == "AVAILABLE" and not cue.ordered_segment_references:
        raise B1EvidenceValidationError(
            "AVAILABLE cue must reference at least one native context segment"
        )
    if cue.annotation_status in ("INSUFFICIENT", "AMBIGUOUS") and (
        cue.ordered_segment_references or cue.ordered_segment_sha256s
    ):
        raise B1EvidenceValidationError(
            f"{cue.annotation_status} cue must have no segment references or hashes"
        )
    if len(cue.ordered_segment_references) != len(cue.ordered_segment_sha256s):
        raise B1EvidenceValidationError("cue segment references and hashes must be aligned")
    previous: int | None = None
    for reference, expected_hash in zip(
        cue.ordered_segment_references, cue.ordered_segment_sha256s, strict=True
    ):
        if reference.source_document_id != cue.source_document_id:
            raise B1EvidenceReferenceError(
                f"segment reference binds wrong source_document_id "
                f"{reference.source_document_id!r} (cue binds {cue.source_document_id!r})"
            )
        index = reference.context_segment_index
        if index < 0 or index >= len(context):
            raise B1EvidenceReferenceError(
                f"segment index {index} out of range for context of size {len(context)}"
            )
        if previous is not None and index <= previous:
            raise B1EvidenceReferenceError(
                f"segment indices must be strictly increasing; got {index} after {previous}"
            )
        previous = index
        actual_hash = segment_sha256(context[index])
        if actual_hash != expected_hash:
            raise B1EvidenceReferenceError(
                f"segment hash mismatch at index {index}: "
                f"expected {expected_hash}, got {actual_hash}"
            )
    derived = derive_evidence_id(
        schema_version=cue.schema_version,
        example_id=cue.example_id,
        source_document_id=cue.source_document_id,
        annotation_status=cue.annotation_status,
        ordered_segment_references=cue.ordered_segment_references,
        ordered_segment_sha256s=cue.ordered_segment_sha256s,
        annotation_protocol_version=cue.annotation_protocol_version,
    )
    if derived != cue.evidence_id:
        raise B1EvidenceValidationError(
            f"cue evidence_id does not match its canonical derivation: {cue.evidence_id!r}"
        )


# ---------------------------------------------------------------------------
# Development subset selection
# ---------------------------------------------------------------------------


def _registry_row_from_object(obj: Mapping[str, object]) -> ExampleRegistryRow:
    keys = set(obj)
    missing = sorted(_REGISTRY_KEYS - keys)
    unexpected = sorted(keys - _REGISTRY_KEYS)
    if missing or unexpected:
        raise B1EvidenceValidationError(
            f"registry row fields must be exactly {sorted(_REGISTRY_KEYS)}; "
            f"missing={missing}, unexpected={unexpected}"
        )
    schema = _require_nonblank_str(obj["schema_version"], "schema_version")
    if schema != EXAMPLE_REGISTRY_SCHEMA_VERSION:
        raise B1EvidenceValidationError(
            f"registry schema_version must be {EXAMPLE_REGISTRY_SCHEMA_VERSION!r}, got {schema!r}"
        )
    split = obj["assigned_split"]
    if split not in PARTITIONS:
        raise B1EvidenceValidationError(
            f"assigned_split must be one of {PARTITIONS}, got {split!r}"
        )
    partition: Partition = split
    ordinal = obj["row_ordinal"]
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 0:
        raise B1EvidenceValidationError("row_ordinal must be a non-negative integer")
    return ExampleRegistryRow(
        example_id=_require_nonblank_str(obj["example_id"], "example_id"),
        source_document_id=_require_nonblank_str(obj["source_document_id"], "source_document_id"),
        assigned_split=partition,
        partition_key=_require_nonblank_str(obj["partition_key"], "partition_key"),
        row_ordinal=ordinal,
    )


def load_example_registry_from_bytes(data: bytes) -> tuple[tuple[ExampleRegistryRow, ...], str]:
    """Parse the canonical example registry and return rows plus its exact SHA-256."""
    if not isinstance(data, bytes | bytearray):
        raise B1EvidenceValidationError("registry must be bytes")
    raw = bytes(data)
    registry_sha256 = hashlib.sha256(raw).hexdigest()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise B1EvidenceValidationError(
            "registry begins with a UTF-8 byte-order mark (BOM); remove the BOM"
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise B1EvidenceValidationError(f"registry is not valid UTF-8: {exc}") from exc
    parsed: list[ExampleRegistryRow] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except json.JSONDecodeError as exc:
            raise B1EvidenceValidationError(f"line {line_number}: malformed JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise B1EvidenceValidationError(f"line {line_number}: each row must be a JSON object")
        parsed.append(_registry_row_from_object(obj))
    if not parsed:
        raise B1EvidenceValidationError("registry must contain at least one row")
    seen: set[str] = set()
    for row in parsed:
        if row.example_id in seen:
            raise B1EvidenceValidationError(f"duplicate example_id: {row.example_id}")
        seen.add(row.example_id)
    return tuple(parsed), registry_sha256


def load_example_registry_from_path(path: Path) -> tuple[tuple[ExampleRegistryRow, ...], str]:
    """Parse the canonical example registry from an explicit caller-supplied path."""
    return load_example_registry_from_bytes(path.read_bytes())


def select_development_subset(
    records: Sequence[ExampleRegistryRow],
    *,
    registry_sha256: str,
    source_split_fingerprint: str,
    require_production_counts: bool = False,
) -> DevelopmentSubsetSelection:
    """Deterministic label-blind selection of the first 100 validation examples.

    Rows are sorted ascending by the domain-separated ordering hash, with a
    deterministic ``example_id`` ascending tie-breaker. No label field exists
    on the row type, so labels cannot be read or used.
    """
    if not isinstance(registry_sha256, str) or len(registry_sha256) != 64:
        raise B1EvidenceValidationError("registry_sha256 must be a full 64-hex SHA-256")
    _require_nonblank_str(source_split_fingerprint, "source_split_fingerprint")
    validation = [row for row in records if row.assigned_split == "validation"]
    if require_production_counts and len(validation) != VALIDATION_POPULATION:
        raise B1EvidenceValidationError(
            f"production validation population must be {VALIDATION_POPULATION}, "
            f"got {len(validation)}"
        )
    keyed = [(subset_ordering_key(row.example_id), row) for row in validation]
    keyed.sort(key=lambda item: (item[0], item[1].example_id))
    selected = keyed[:DEVELOPMENT_SUBSET_SIZE]
    if require_production_counts and len(selected) != DEVELOPMENT_SUBSET_SIZE:
        raise B1EvidenceValidationError(
            f"production subset size must be {DEVELOPMENT_SUBSET_SIZE}, got {len(selected)}"
        )
    ordered_ids = tuple(row.example_id for _, row in selected)
    ordered_documents = tuple(row.source_document_id for _, row in selected)
    ordered_keys = tuple(key for key, _ in selected)
    selection = DevelopmentSubsetSelection(
        schema_version=DEVELOPMENT_SUBSET_SCHEMA_VERSION,
        source_split_fingerprint=source_split_fingerprint,
        example_registry_sha256=registry_sha256,
        selection_domain_separator=SUBSET_DOMAIN_SEPARATOR,
        validation_population=len(validation),
        selected_count=len(selected),
        ordered_selected_example_ids=ordered_ids,
        ordered_selected_source_document_ids=ordered_documents,
        ordered_selection_keys=ordered_keys,
        subset_digest="",
    )
    document = subset_manifest_document(selection)
    digest = sha256_hexdigest(document)
    return DevelopmentSubsetSelection(
        schema_version=selection.schema_version,
        source_split_fingerprint=selection.source_split_fingerprint,
        example_registry_sha256=selection.example_registry_sha256,
        selection_domain_separator=selection.selection_domain_separator,
        validation_population=selection.validation_population,
        selected_count=selection.selected_count,
        ordered_selected_example_ids=selection.ordered_selected_example_ids,
        ordered_selected_source_document_ids=selection.ordered_selected_source_document_ids,
        ordered_selection_keys=selection.ordered_selection_keys,
        subset_digest=digest,
    )


def subset_manifest_document(selection: DevelopmentSubsetSelection) -> dict[str, object]:
    """Deterministic prospective manifest containing only identity metadata."""
    return {
        "schema_version": selection.schema_version,
        "source_split_fingerprint": selection.source_split_fingerprint,
        "example_registry_sha256": selection.example_registry_sha256,
        "selection_domain_separator": selection.selection_domain_separator,
        "validation_population": selection.validation_population,
        "selected_count": selection.selected_count,
        "ordered_selected_example_ids": list(selection.ordered_selected_example_ids),
        "ordered_selected_source_document_ids": list(
            selection.ordered_selected_source_document_ids
        ),
        "ordered_selection_keys": list(selection.ordered_selection_keys),
        "subset_digest": selection.subset_digest,
    }


def write_subset_manifest(selection: DevelopmentSubsetSelection, path: Path) -> None:
    """Write the subset manifest deterministically; refuse to overwrite."""
    _write_atomic_json(path, subset_manifest_document(selection))


# ---------------------------------------------------------------------------
# Evidence pack
# ---------------------------------------------------------------------------


def _cue_documents(cues: Sequence[B1EvidenceCue]) -> list[dict[str, object]]:
    return [cue_to_document(cue) for cue in cues]


def pack_to_document(pack: B1EvidencePack) -> dict[str, object]:
    """Deterministic serializable form of the evidence pack (no raw text)."""
    return {
        "schema_version": pack.schema_version,
        "annotation_protocol_version": pack.annotation_protocol_version,
        "source_split_fingerprint": pack.source_split_fingerprint,
        "subset_digest": pack.subset_digest,
        "cues": _cue_documents(pack.cues),
        "pack_sha256": pack.pack_sha256,
        "record_count": pack.record_count,
    }


def pack_from_document(document: Mapping[str, object]) -> B1EvidencePack:
    """Parse an evidence pack from its deterministic document form."""
    expected = {
        "schema_version",
        "annotation_protocol_version",
        "source_split_fingerprint",
        "subset_digest",
        "cues",
        "pack_sha256",
        "record_count",
    }
    if set(document) != expected:
        raise B1EvidenceValidationError(
            f"pack fields must be exactly {sorted(expected)}; got {sorted(document)}"
        )
    cues_value = document["cues"]
    if not isinstance(cues_value, list):
        raise B1EvidenceValidationError("cues must be a list")
    cues = tuple(cue_from_document(item) for item in cues_value)
    count = document["record_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count != len(cues):
        raise B1EvidenceValidationError(
            f"record_count must equal the number of cues ({len(cues)}), got {count!r}"
        )
    pack_sha = document["pack_sha256"]
    if not isinstance(pack_sha, str) or len(pack_sha) != 64:
        raise B1EvidenceValidationError("pack_sha256 must be a full 64-hex SHA-256")
    return B1EvidencePack(
        schema_version=_require_nonblank_str(document["schema_version"], "schema_version"),
        annotation_protocol_version=_require_nonblank_str(
            document["annotation_protocol_version"], "annotation_protocol_version"
        ),
        source_split_fingerprint=_require_nonblank_str(
            document["source_split_fingerprint"], "source_split_fingerprint"
        ),
        subset_digest=_require_nonblank_str(document["subset_digest"], "subset_digest"),
        cues=cues,
        pack_sha256=pack_sha,
        record_count=count,
    )


def build_evidence_pack(
    cues: Sequence[B1EvidenceCue],
    *,
    source_split_fingerprint: str,
    subset_digest: str,
    require_record_count: int | None = None,
) -> B1EvidencePack:
    """Build a deterministic identity-bound evidence pack.

    ``require_record_count`` enforces an exact record count where the ratified
    contract fixes it (the future development pack requires exactly 100).
    """
    if not cues:
        raise B1EvidenceValidationError("evidence pack must contain at least one cue")
    _require_nonblank_str(source_split_fingerprint, "source_split_fingerprint")
    _require_nonblank_str(subset_digest, "subset_digest")
    if require_record_count is not None and (
        not isinstance(require_record_count, int)
        or isinstance(require_record_count, bool)
        or require_record_count <= 0
    ):
        raise B1EvidenceValidationError("require_record_count must be a positive integer")
    seen: set[str] = set()
    for cue in cues:
        if cue.schema_version != EVIDENCE_CUE_SCHEMA_VERSION:
            raise B1EvidenceValidationError(
                f"cue schema_version must be {EVIDENCE_CUE_SCHEMA_VERSION!r}"
            )
        if cue.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
            raise B1EvidenceValidationError(
                f"cue annotation_protocol_version must be {ANNOTATION_PROTOCOL_VERSION!r}"
            )
        if cue.review_status != "FINAL":
            raise B1EvidenceValidationError(
                "pack may only contain FINAL (review-complete) cues; "
                f"got review_status {cue.review_status!r}"
            )
        if cue.example_id in seen:
            raise B1EvidenceValidationError(f"duplicate cue example_id: {cue.example_id}")
        seen.add(cue.example_id)
    if require_record_count is not None and len(cues) != require_record_count:
        raise B1EvidenceValidationError(
            f"pack record count must be exactly {require_record_count}, got {len(cues)}"
        )
    provisional = B1EvidencePack(
        schema_version=EVIDENCE_PACK_SCHEMA_VERSION,
        annotation_protocol_version=ANNOTATION_PROTOCOL_VERSION,
        source_split_fingerprint=source_split_fingerprint,
        subset_digest=subset_digest,
        cues=tuple(cues),
        pack_sha256="",
        record_count=len(cues),
    )
    document = pack_to_document(provisional)
    document["pack_sha256"] = ""
    pack_sha256 = sha256_hexdigest(document)
    return B1EvidencePack(
        schema_version=provisional.schema_version,
        annotation_protocol_version=provisional.annotation_protocol_version,
        source_split_fingerprint=provisional.source_split_fingerprint,
        subset_digest=provisional.subset_digest,
        cues=provisional.cues,
        pack_sha256=pack_sha256,
        record_count=provisional.record_count,
    )


def validate_evidence_pack(
    pack: B1EvidencePack,
    contexts: Mapping[tuple[str, str], Sequence[str]],
) -> None:
    """Fail-closed pack validation: identity, count, and every cue against context.

    ``contexts`` maps ``(example_id, source_document_id)`` to the exact native
    ordered context tuple.
    """
    if pack.schema_version != EVIDENCE_PACK_SCHEMA_VERSION:
        raise B1EvidenceValidationError(
            f"pack schema_version must be {EVIDENCE_PACK_SCHEMA_VERSION!r}, "
            f"got {pack.schema_version!r}"
        )
    if pack.annotation_protocol_version != ANNOTATION_PROTOCOL_VERSION:
        raise B1EvidenceValidationError(
            f"pack annotation_protocol_version must be {ANNOTATION_PROTOCOL_VERSION!r}, "
            f"got {pack.annotation_protocol_version!r}"
        )
    if pack.record_count != len(pack.cues):
        raise B1EvidenceValidationError(
            f"pack record_count {pack.record_count} does not match cue count {len(pack.cues)}"
        )
    if not pack.pack_sha256 or len(pack.pack_sha256) != 64:
        raise B1EvidenceValidationError("pack_sha256 must be a full 64-hex SHA-256")
    document = pack_to_document(pack)
    document["pack_sha256"] = ""
    if sha256_hexdigest(document) != pack.pack_sha256:
        raise B1EvidenceValidationError("pack SHA-256 does not match its canonical content")
    seen: set[str] = set()
    for cue in pack.cues:
        if cue.example_id in seen:
            raise B1EvidenceValidationError(f"duplicate cue example_id: {cue.example_id}")
        seen.add(cue.example_id)
        context = contexts.get((cue.example_id, cue.source_document_id))
        if context is None:
            raise B1EvidenceReferenceError(
                f"no context available for cue ({cue.example_id}, {cue.source_document_id})"
            )
        validate_evidence_cue(cue, context)


def write_evidence_pack(pack: B1EvidencePack, path: Path) -> None:
    """Write the evidence pack deterministically; refuse to overwrite."""
    _write_atomic_json(path, pack_to_document(pack))


def _write_atomic_json(path: Path, document: Mapping[str, object]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {path}")
    data = canonical_json_bytes(document) + b"\n"
    tmp = path.with_name(path.name + ".partial")
    published = False
    try:
        with tmp.open("wb") as handle:
            handle.write(data)
            handle.flush()
        tmp.replace(path)
        published = True
    finally:
        if not published:
            with contextlib.suppress(FileNotFoundError):
                tmp.unlink()
