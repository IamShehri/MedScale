"""Private fixture-only in-memory split facade for P01-04B2C (FD-B2C-1..FD-B2C-12).

This private module composes the accepted P01-04B1 split core, the P01-04B2A
canonical artifact and fingerprint layer, and the P01-04B2B leakage primitives
into exactly one deterministic, library-only result object.  It is not exported,
has no CLI, accepts no path or external-resource input, and performs no I/O of
any kind: every byte surface it builds stays in memory and is never written,
published or persisted.

The declared ``fixture_only``, ``non_evidence`` and ``synthetic_identity_proof``
markers establish that a request is *internally consistent* with the identity it
claims.  They are deliberately not a cryptographic or real-world provenance
oracle, and no combination of them can detect a caller who repackages real data
into the accepted row types.  Safety here comes from structure instead: the
module is private and unexported, there is no CLI, no path input, no registry
adapter, no filesystem access and no real-data entry point, and the public
``SourceDocumentGroupedSplitter.assign`` remains unconditionally fail-closed
because nothing here calls it.

A ``FixtureSplitResult`` is a synthetic in-memory value.  It is not promotable,
not written, not published, not clinical evidence, not research evidence, and
not a real split artifact.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Final

from medscale.mesc._canonical_json_v1 import (
    canonical_json_bytes,
    canonical_jsonl_bytes,
    sha256_of_bytes,
)
from medscale.mesc._leakage_v1 import LeakageAuditReport, LeakageFinding
from medscale.mesc._split_artifacts_v1 import (
    SplitFingerprintRecord,
    SplitSummaryIdentityCore,
    build_split_fingerprint_identity,
    build_split_fingerprint_record,
    verify_descriptor_against_bytes,
    verify_split_fingerprint_record,
)
from medscale.mesc._split_v1 import (
    ALGORITHM_VERSION,
    DECISIONS,
    PARTITIONS,
    SPLIT_SEED,
    GroupAssignment,
    LabeledExample,
    OrderedExampleRow,
    SourceLabelRow,
    allocate_indivisible_groups,
    constrained_apportionment,
    join_labels,
)
from medscale.mesc.split import PilotSplitAssignment, PilotSplitManifest

#: The only accepted fixture schema version (FD-B2C-3).
FIXTURE_SCHEMA_VERSION: Final = "1"

#: Namespaces are derived, never free-form: exactly this prefix plus the fixture ID.
FIXTURE_NAMESPACE_PREFIX: Final = "mesc-fixture/p01-04b2/1/"

#: Schema of the sixteen-member fixture identity document (FD-B2C-4).
FIXTURE_IDENTITY_SCHEMA: Final = "mesc-pilot-01-fixture-identity/1"

#: Schema of the four-member request identity document (FD-B2C-4).
REQUEST_IDENTITY_SCHEMA: Final = "mesc-pilot-01-fixture-request-identity/1"

#: The fixed, identity-bearing request-ID domain.
REQUEST_ID_DOMAIN: Final = "p01-04b2c"

#: Derived request identifiers carry this prefix and a 64-lowercase-hex digest.
REQUEST_ID_PREFIX: Final = "mesc-pilot-01-fixture-request/1:sha256:"

#: Declared synthetic-batch markers carry this prefix and a 64-lowercase-hex digest.
SYNTHETIC_PROOF_PREFIX: Final = "mesc-synthetic-batch/1:sha256:"

#: Schema bound into the six-member group identity payload.
GROUP_ID_SCHEMA: Final = "mesc-pilot-01-group/1"

#: Derived group identifiers carry this prefix and a 64-lowercase-hex digest.
GROUP_ID_PREFIX: Final = f"{GROUP_ID_SCHEMA}:sha256:"

#: Canonical schema versions of the B2C byte surfaces, pinned by the contract.
GROUP_REGISTRY_SCHEMA: Final = "mesc-pilot-01-group-registry/1"
EXAMPLE_REGISTRY_SCHEMA: Final = "mesc-pilot-01-example-registry/1"
EXCLUDED_LEDGER_SCHEMA: Final = "mesc-pilot-01-excluded-ledger/1"
SPLIT_SUMMARY_SCHEMA: Final = "mesc-pilot-01-split-summary/1"

#: B2C authorizes no exclusion, so the ledger is a constant rather than a derivation.
EXCLUDED_LEDGER_DOCUMENT: Final[Mapping[str, object]] = MappingProxyType(
    {
        "count": 0,
        "excluded_ids": (),
        "reason": "none",
        "schema_version": EXCLUDED_LEDGER_SCHEMA,
    }
)

#: Canonical partition order for the compatibility manifest, which is deliberately
#: *not* the lexicographic order used by the two registries.
_PARTITION_ORDER: Final[Mapping[str, int]] = MappingProxyType(
    {partition: index for index, partition in enumerate(PARTITIONS)}
)

_SHA256_LENGTH: Final = 64
_HEX_DIGITS: Final = frozenset("0123456789abcdef")
_FIXTURE_ID_CHARACTERS: Final = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")
_FIXTURE_ID_EDGE_CHARACTERS: Final = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")
_PATH_PREFIXES: Final = ("/", "./", "../", "~")


class FixtureFacadeContractError(Exception):
    """Base class for every private B2C facade contract failure.

    This hierarchy is facade-specific.  B1, B2A and B2B typed exceptions are
    never caught and re-raised as one of these, so a failing contract always
    stays attributable to the layer that owns it.
    """

    #: Stable machine-readable taxonomy code.
    code: ClassVar[str] = "fixture_facade_contract_error"


class FixtureOnlyModeError(FixtureFacadeContractError):
    """A request that does not declare itself fixture-only and non-evidence."""

    code: ClassVar[str] = "fixture_only_mode_error"


class InvalidFixtureRequestError(FixtureFacadeContractError):
    """A request field outside its exact contract."""

    code: ClassVar[str] = "invalid_fixture_request"


class FixtureIdentityMismatchError(FixtureFacadeContractError):
    """A caller-supplied digest or identifier that does not match its regeneration."""

    code: ClassVar[str] = "fixture_identity_mismatch"


class FixtureIntegrationInvariantError(FixtureFacadeContractError):
    """A cross-object invariant that the composed layers did not satisfy."""

    code: ClassVar[str] = "fixture_integration_invariant"


class InvalidExecutionEvidenceReferenceError(FixtureFacadeContractError):
    """An execution-evidence reference that is absent, unstable or path-shaped."""

    code: ClassVar[str] = "invalid_execution_evidence_reference"


def _is_blank_or_padded(value: str) -> bool:
    """Return true when a value is empty or differs from its stripped form."""
    return not value or value.strip() != value


def _is_path_like(value: str) -> bool:
    """Return true when a value is shaped like a local path or external resource.

    The rule is exactly the one ratified in the implementation contract: a
    backslash anywhere, a leading ``/``, ``./``, ``../`` or ``~``, or a
    ``<letter>:`` drive shape in the first two characters.  Emptiness and
    surrounding whitespace are handled separately by ``_is_blank_or_padded`` so
    the primitive-type step and the path step stay distinct.
    """
    if "\\" in value or value.startswith(_PATH_PREFIXES):
        return True
    return len(value) >= 2 and value[0].isalpha() and value[1] == ":"


def _is_lowercase_hex(value: str, length: int) -> bool:
    """Return true when a value is exactly ``length`` lowercase hexadecimal characters."""
    return len(value) == length and all(character in _HEX_DIGITS for character in value)


def _is_suffixed_digest(value: str, prefix: str) -> bool:
    """Return true when a value is ``prefix`` followed by a 64-lowercase-hex digest."""
    return value.startswith(prefix) and _is_lowercase_hex(value[len(prefix) :], _SHA256_LENGTH)


def _is_valid_fixture_id(value: str) -> bool:
    """Return true for a non-empty lowercase ASCII identifier bounded by alphanumerics."""
    if not value:
        return False
    if any(character not in _FIXTURE_ID_CHARACTERS for character in value):
        return False
    return value[0] in _FIXTURE_ID_EDGE_CHARACTERS and value[-1] in _FIXTURE_ID_EDGE_CHARACTERS


@dataclass(frozen=True, slots=True)
class FixtureSplitRequest:
    """The exact seventeen-field immutable fixture request (FD-B2C-3).

    Payload ownership is identity-only.  The request carries the accepted B1
    identity-and-label row types and never carries raw question, context or
    answer text, so the facade cannot read such text: no field can hold it.

    Every caller-owned collection is either already immutable on entry (the four
    tuple fields, whose element types are frozen dataclasses) or snapshotted into
    an immutable mapping during construction.  After ``__post_init__`` no
    caller-owned mutable object remains reachable, so a later mutation by the
    caller cannot change any canonical byte surface, digest or fingerprint
    derived from this request.
    """

    fixture_schema_version: str
    fixture_namespace: str
    fixture_id: str
    fixture_sha256: str
    fixture_only: bool
    non_evidence: bool
    synthetic_identity_proof: str
    request_id: str
    seed: str
    policy_id: str
    transformation_version: str
    ordered_rows: tuple[OrderedExampleRow, ...]
    source_labels: tuple[SourceLabelRow, ...]
    partition_totals: Mapping[str, int]
    leakage_findings: tuple[LeakageFinding, ...]
    detection_methods: tuple[str, ...]
    execution_evidence_ref: str

    def __post_init__(self) -> None:
        """Validate in the controlling order, so the earliest failure always controls.

        Steps 2 through 6 of the ratified twelve-step order belong to the request
        itself; step 1 (exact request type) and steps 7 through 12 belong to
        ``FixtureSplitFacade.run``.  ``partition_totals`` is snapshotted at the
        start of step 6 and validated afterwards, because the contract requires
        the values validated to be exactly the values stored.
        """
        self._validate_markers()
        self._validate_schema_and_namespace()
        self._validate_primitive_types()
        self._validate_path_rejection()
        self._snapshot_and_validate_collections()

    # -- step 2 -------------------------------------------------------------
    def _validate_markers(self) -> None:
        if type(self.fixture_only) is not bool or not self.fixture_only:
            raise FixtureOnlyModeError("fixture_only must be exactly True")
        if type(self.non_evidence) is not bool or not self.non_evidence:
            raise FixtureOnlyModeError("non_evidence must be exactly True")

    # -- step 3 -------------------------------------------------------------
    def _validate_schema_and_namespace(self) -> None:
        if (
            type(self.fixture_schema_version) is not str
            or self.fixture_schema_version != FIXTURE_SCHEMA_VERSION
        ):
            raise InvalidFixtureRequestError("fixture_schema_version must be exactly '1'")
        if type(self.fixture_id) is not str or not _is_valid_fixture_id(self.fixture_id):
            raise InvalidFixtureRequestError(
                "fixture_id must be a non-empty lowercase ASCII identifier of letters, "
                "digits and hyphens beginning and ending with a letter or digit"
            )
        if (
            type(self.fixture_namespace) is not str
            or self.fixture_namespace != FIXTURE_NAMESPACE_PREFIX + self.fixture_id
        ):
            raise InvalidFixtureRequestError(
                "fixture_namespace must be exactly the authorized prefix plus fixture_id"
            )

    # -- step 4 -------------------------------------------------------------
    def _validate_primitive_types(self) -> None:
        if type(self.fixture_sha256) is not str or not _is_lowercase_hex(
            self.fixture_sha256, _SHA256_LENGTH
        ):
            raise InvalidFixtureRequestError(
                "fixture_sha256 must be 64 lowercase hexadecimal characters"
            )
        if type(self.synthetic_identity_proof) is not str or not _is_suffixed_digest(
            self.synthetic_identity_proof, SYNTHETIC_PROOF_PREFIX
        ):
            raise InvalidFixtureRequestError(
                "synthetic_identity_proof must carry the authorized prefix and digest"
            )
        if type(self.request_id) is not str or not _is_suffixed_digest(
            self.request_id, REQUEST_ID_PREFIX
        ):
            raise InvalidFixtureRequestError(
                "request_id must carry the authorized prefix and digest"
            )
        if type(self.seed) is not str or self.seed != SPLIT_SEED:
            raise InvalidFixtureRequestError("seed must be exactly the accepted B1 split seed")
        for name in ("policy_id", "transformation_version"):
            value = getattr(self, name)
            if type(value) is not str or _is_blank_or_padded(value):
                raise InvalidFixtureRequestError(f"{name} must be a non-empty stripped str")
        if type(self.execution_evidence_ref) is not str or _is_blank_or_padded(
            self.execution_evidence_ref
        ):
            raise InvalidExecutionEvidenceReferenceError(
                "execution_evidence_ref must be a non-empty stripped str"
            )
        self._validate_collection_types()

    def _validate_collection_types(self) -> None:
        """Reject any container or element that is not the exact authorized type.

        ``type(...) is`` rather than ``isinstance``: a subclass of an accepted row
        type could override behaviour the identity payload depends on, and a list
        or a generator would leave a caller-owned mutable object reachable.
        """
        if type(self.ordered_rows) is not tuple or not self.ordered_rows:
            raise InvalidFixtureRequestError("ordered_rows must be a non-empty exact tuple")
        for row in self.ordered_rows:
            if type(row) is not OrderedExampleRow:
                raise InvalidFixtureRequestError(
                    "every ordered_rows element must be an exact OrderedExampleRow"
                )
        if type(self.source_labels) is not tuple or not self.source_labels:
            raise InvalidFixtureRequestError("source_labels must be a non-empty exact tuple")
        for label in self.source_labels:
            if type(label) is not SourceLabelRow:
                raise InvalidFixtureRequestError(
                    "every source_labels element must be an exact SourceLabelRow"
                )
        if type(self.leakage_findings) is not tuple:
            raise InvalidFixtureRequestError("leakage_findings must be an exact tuple")
        for finding in self.leakage_findings:
            if type(finding) is not LeakageFinding:
                raise InvalidFixtureRequestError(
                    "every leakage_findings element must be an exact LeakageFinding"
                )
        if type(self.detection_methods) is not tuple:
            raise InvalidFixtureRequestError("detection_methods must be an exact tuple")
        for method in self.detection_methods:
            if type(method) is not str:
                raise InvalidFixtureRequestError(
                    "every detection_methods element must be an exact str"
                )

    # -- step 5 -------------------------------------------------------------
    def _validate_path_rejection(self) -> None:
        for name in ("synthetic_identity_proof", "policy_id"):
            if _is_path_like(getattr(self, name)):
                raise InvalidFixtureRequestError(
                    f"{name} must not be a local path or external resource"
                )
        if _is_path_like(self.execution_evidence_ref):
            raise InvalidExecutionEvidenceReferenceError(
                "execution_evidence_ref must not be a local path or external resource"
            )

    # -- step 6 -------------------------------------------------------------
    def _snapshot_and_validate_collections(self) -> None:
        object.__setattr__(
            self, "partition_totals", _snapshot_partition_totals(self.partition_totals)
        )
        self._validate_partition_totals()
        self._reject_duplicates()

    def _validate_partition_totals(self) -> None:
        if set(self.partition_totals) != set(PARTITIONS):
            raise InvalidFixtureRequestError(
                "partition_totals must contain exactly train, validation and test"
            )
        for partition, total in self.partition_totals.items():
            # ``type(...) is int`` rather than ``isinstance``: Python makes ``bool``
            # an ``int`` subclass and a boolean count must never satisfy a count.
            if type(total) is not int or total < 0:
                raise InvalidFixtureRequestError(
                    f"partition_totals[{partition!r}] must be a non-negative exact int"
                )
        if sum(self.partition_totals.values()) != len(self.ordered_rows):
            raise InvalidFixtureRequestError("partition_totals must sum to the ordered-row count")

    def _reject_duplicates(self) -> None:
        """Reject every duplicate identity; duplicates are never silently collapsed."""
        _reject_duplicate_values(
            [row.original_example_id for row in self.ordered_rows],
            "ordered_rows original_example_id",
        )
        _reject_duplicate_values(
            [row.row_ordinal for row in self.ordered_rows], "ordered_rows row_ordinal"
        )
        _reject_duplicate_values(
            [label.original_example_id for label in self.source_labels],
            "source_labels original_example_id",
        )
        _reject_duplicate_values(
            [finding.finding_id for finding in self.leakage_findings],
            "leakage_findings finding_id",
        )
        _reject_duplicate_values(list(self.detection_methods), "detection_methods")


def _snapshot_partition_totals(value: Mapping[str, int]) -> Mapping[str, int]:
    """Return a single immutable snapshot of a caller-owned partition mapping.

    The caller mapping is read exactly once, and every key is required to be an
    exact ``str`` before any value is trusted, so a mapping that mutates between
    reads can never inject an unvalidated key.
    """
    if not isinstance(value, Mapping):
        raise InvalidFixtureRequestError("partition_totals must be a mapping")
    snapshot = dict(value.items())
    for key in snapshot:
        if type(key) is not str:
            raise InvalidFixtureRequestError("partition_totals keys must be exact strings")
    return MappingProxyType(snapshot)


def _zeroed(keys: Sequence[str]) -> dict[str, int]:
    """Return a complete mapping from every key to an explicit zero.

    Absent combinations must be explicit zeros rather than missing members, so
    the canonical bytes never depend on which combinations a particular fixture
    happened to populate.
    """
    totals: dict[str, int] = {}
    for key in keys:
        totals[key] = 0
    return totals


def _reject_duplicate_values(values: Sequence[object], field: str) -> None:
    seen: list[object] = []
    for value in values:
        if value in seen:
            raise InvalidFixtureRequestError(f"{field} must not contain a duplicate value")
        seen.append(value)


@dataclass(frozen=True, slots=True)
class FixtureSplitResult:
    """The exact twelve-field immutable fixture result (FD-B2C-9).

    This value is non-promotable: it is not written, not published, not clinical
    evidence, not research evidence and not a real split artifact.  It carries
    only the canonical bytes and accepted objects the facade constructed, so a
    caller can re-verify every binding without re-running the pipeline.
    """

    request_id: str
    split_manifest: PilotSplitManifest
    group_registry_bytes: bytes
    example_registry_bytes: bytes
    excluded_ledger_bytes: bytes
    split_summary_identity_core: SplitSummaryIdentityCore
    split_summary_identity_core_bytes: bytes
    split_summary_document_bytes: bytes
    split_fingerprint_record: SplitFingerprintRecord
    audit_report: LeakageAuditReport
    audit_report_bytes: bytes
    execution_evidence_ref: str

    def __post_init__(self) -> None:
        for name in (
            "group_registry_bytes",
            "example_registry_bytes",
            "excluded_ledger_bytes",
            "split_summary_identity_core_bytes",
            "split_summary_document_bytes",
            "audit_report_bytes",
        ):
            if type(getattr(self, name)) is not bytes:
                raise FixtureIntegrationInvariantError(f"{name} must be exact bytes")
        for name in ("request_id", "execution_evidence_ref"):
            if type(getattr(self, name)) is not str:
                raise FixtureIntegrationInvariantError(f"{name} must be an exact str")
        for name, expected in (
            ("split_manifest", PilotSplitManifest),
            ("split_summary_identity_core", SplitSummaryIdentityCore),
            ("split_fingerprint_record", SplitFingerprintRecord),
            ("audit_report", LeakageAuditReport),
        ):
            if type(getattr(self, name)) is not expected:
                raise FixtureIntegrationInvariantError(
                    f"{name} must be an exact {expected.__name__}"
                )


def _fixture_identity_document(request: FixtureSplitRequest) -> dict[str, object]:
    """Return the exact sixteen-member fixture identity document.

    The document deliberately excludes ``fixture_sha256`` and ``request_id``, so
    neither digest can ever contain itself.  Every array is placed in canonical
    order here, because the accepted serializer sorts object members but never
    reorders arrays.
    """
    ordered_rows = sorted(
        request.ordered_rows, key=lambda row: (row.row_ordinal, row.original_example_id)
    )
    source_labels = sorted(request.source_labels, key=lambda label: label.original_example_id)
    findings = sorted(request.leakage_findings, key=lambda finding: finding.finding_id)
    return {
        "schema": FIXTURE_IDENTITY_SCHEMA,
        "fixture_schema_version": request.fixture_schema_version,
        "fixture_namespace": request.fixture_namespace,
        "fixture_id": request.fixture_id,
        "fixture_only": request.fixture_only,
        "non_evidence": request.non_evidence,
        "synthetic_identity_proof": request.synthetic_identity_proof,
        "seed": request.seed,
        "policy_id": request.policy_id,
        "transformation_version": request.transformation_version,
        "ordered_rows": [
            {
                "original_example_id": row.original_example_id,
                "row_ordinal": row.row_ordinal,
                "source_document_id": row.source_document_id,
            }
            for row in ordered_rows
        ],
        "source_labels": [
            {
                "configuration": label.configuration,
                "dataset_id": label.dataset_id,
                "dataset_revision": label.dataset_revision,
                "decision": label.decision,
                "original_example_id": label.original_example_id,
                "source_document_id": label.source_document_id,
                "source_record_hash": label.source_record_hash,
            }
            for label in source_labels
        ],
        "partition_totals": dict(request.partition_totals),
        # The accepted B2B document is reused verbatim; B2C constructs no finding
        # document of its own.
        "leakage_finding_documents": [finding.to_canonical_document() for finding in findings],
        # Caller order is preserved because detection-method order is semantic.
        "detection_methods": list(request.detection_methods),
        "execution_evidence_ref": request.execution_evidence_ref,
    }


def _request_identity_document(
    request: FixtureSplitRequest, fixture_sha256: str
) -> dict[str, object]:
    """Return the exact four-member request identity document.

    ``fixture_sha256`` is the *recomputed* digest, never the caller-supplied one,
    and ``request_id`` is structurally absent so the identifier can never be part
    of the payload it is derived from.
    """
    return {
        "schema": REQUEST_IDENTITY_SCHEMA,
        "fixture_sha256": fixture_sha256,
        "fixture_namespace": request.fixture_namespace,
        "request_id_domain": REQUEST_ID_DOMAIN,
    }


def _group_id(assignment: GroupAssignment) -> str:
    """Return the derived group identifier for one accepted group assignment.

    The payload has exactly the six ratified members.  ``decision`` is not a
    seventh member and must not become one: ``partition_key`` already binds the
    algorithm version, the split seed, the source document and the decision
    stratum, and B1 refuses to build a source-document group that crosses
    decision strata.
    """
    payload = {
        "schema": GROUP_ID_SCHEMA,
        "source_document_id": assignment.source_document_id,
        "assigned_split": assignment.partition,
        "example_ids": sorted(assignment.example_ids),
        "row_ordinals": sorted(assignment.row_ordinals),
        "partition_key": assignment.partition_key,
    }
    return GROUP_ID_PREFIX + sha256_of_bytes(canonical_json_bytes(payload))


def _row_ordinals_by_example_id(joined: Sequence[LabeledExample]) -> dict[str, int]:
    """Return the explicit example-to-ordinal mapping, failing closed on a duplicate.

    The mapping is built from the accepted joined examples rather than by pairing
    the parallel tuples of a group assignment positionally, so nothing here
    depends on an undocumented coincidence between two orderings.
    """
    ordinals: dict[str, int] = {}
    for example in joined:
        if example.example_id in ordinals:
            raise FixtureIntegrationInvariantError("joined examples contain a duplicate example_id")
        ordinals[example.example_id] = example.row_ordinal
    return ordinals


def _compatibility_manifest(
    assignments: Sequence[GroupAssignment], row_ordinals: Mapping[str, int]
) -> PilotSplitManifest:
    """Return the B1-compatibility manifest in exact train/validation/test order.

    ``split_hash`` must be empty: ``computed_split_hash`` returns a supplied value
    verbatim and only derives the 16-hex value from the actual assignments when
    none was supplied.  ``split_seed`` must be passed explicitly because the
    class default is a different seed.
    """
    ranked: list[tuple[int, int, str, PilotSplitAssignment]] = []
    for assignment in assignments:
        for example_id in assignment.example_ids:
            if example_id not in row_ordinals:
                raise FixtureIntegrationInvariantError(
                    "assigned example_id is absent from the joined examples"
                )
            ranked.append(
                (
                    _PARTITION_ORDER[assignment.partition],
                    row_ordinals[example_id],
                    example_id,
                    PilotSplitAssignment(
                        example_id=example_id,
                        split=assignment.partition,
                        source_document_id=assignment.source_document_id,
                        partition_key=assignment.partition_key,
                    ),
                )
            )
    ranked.sort(key=lambda item: (item[0], item[1], item[2]))
    return PilotSplitManifest(
        split_assignments=tuple(item[3] for item in ranked),
        split_hash="",
        split_seed=SPLIT_SEED,
    )


def _group_registry_bytes(assignments: Sequence[GroupAssignment]) -> bytes:
    """Return the canonical group-registry JSONL bytes.

    Ordering is ``assigned_split`` lexicographically and then ``group_id``.  That
    is intentionally *not* the canonical partition order: lexicographically
    ``"test" < "train" < "validation"``.
    """
    ranked: list[tuple[str, str, dict[str, object]]] = []
    for assignment in assignments:
        group_id = _group_id(assignment)
        ranked.append(
            (
                assignment.partition,
                group_id,
                {
                    "schema_version": GROUP_REGISTRY_SCHEMA,
                    "group_id": group_id,
                    "source_document_id": assignment.source_document_id,
                    "example_count": len(assignment.example_ids),
                    "row_ordinals": sorted(assignment.row_ordinals),
                    "assigned_split": assignment.partition,
                    "partition_key": assignment.partition_key,
                },
            )
        )
    ranked.sort(key=lambda item: (item[0], item[1]))
    return canonical_jsonl_bytes([item[2] for item in ranked])


def _example_registry_bytes(
    assignments: Sequence[GroupAssignment], row_ordinals: Mapping[str, int]
) -> bytes:
    """Return the canonical example-registry JSONL bytes.

    Ordering is ``assigned_split`` lexicographically, then ``row_ordinal``, then
    ``example_id`` — again lexicographic on the split, not canonical partition
    order.
    """
    ranked: list[tuple[str, int, str, dict[str, object]]] = []
    for assignment in assignments:
        for example_id in assignment.example_ids:
            row_ordinal = row_ordinals[example_id]
            ranked.append(
                (
                    assignment.partition,
                    row_ordinal,
                    example_id,
                    {
                        "schema_version": EXAMPLE_REGISTRY_SCHEMA,
                        "example_id": example_id,
                        "source_document_id": assignment.source_document_id,
                        "row_ordinal": row_ordinal,
                        "assigned_split": assignment.partition,
                        "partition_key": assignment.partition_key,
                    },
                )
            )
    ranked.sort(key=lambda item: (item[0], item[1], item[2]))
    return canonical_jsonl_bytes([item[3] for item in ranked])


def _summary_identity_core(
    joined: Sequence[LabeledExample], assignments: Sequence[GroupAssignment]
) -> SplitSummaryIdentityCore:
    """Return the fingerprint-free identity core with every combination explicit.

    Every mapping is complete over its domain and absent combinations are
    explicit zeros, so the canonical bytes never depend on which combinations a
    particular fixture happened to populate.
    """
    partition_totals = _zeroed(PARTITIONS)
    group_counts = _zeroed(PARTITIONS)
    label_totals = _zeroed(DECISIONS)
    matrix: dict[str, dict[str, int]] = {partition: _zeroed(DECISIONS) for partition in PARTITIONS}
    for example in joined:
        label_totals[example.decision] += 1
    for assignment in assignments:
        example_count = len(assignment.example_ids)
        partition_totals[assignment.partition] += example_count
        group_counts[assignment.partition] += 1
        matrix[assignment.partition][assignment.decision] += example_count
    return SplitSummaryIdentityCore(
        total_example_count=len(joined),
        total_group_count=len(assignments),
        excluded_record_count=0,
        partition_totals=partition_totals,
        label_totals=label_totals,
        partition_label_matrix=matrix,
        group_counts_by_partition=group_counts,
        algorithm_version=ALGORITHM_VERSION,
    )


def _split_summary_document_bytes(
    core: SplitSummaryIdentityCore, split_hash: str, split_fingerprint: str
) -> bytes:
    """Return the final summary bytes, constructed only after the fingerprint exists.

    This document is never an input to the fingerprint.  The authoritative
    fingerprint binds the fingerprint-free identity core, so no value derived
    from the fingerprint can re-enter the payload it was computed over.
    """
    document = dict(core.to_canonical_document())
    document["schema_version"] = SPLIT_SUMMARY_SCHEMA
    document["split_hash"] = split_hash
    document["split_fingerprint"] = split_fingerprint
    return canonical_json_bytes(document)


class FixtureSplitFacade:
    """The stateless private fixture-only split facade (FD-B2C-2).

    The facade holds no instance state that can influence a result, reads no
    environment or configuration, and performs no side effect.  Two invocations
    with the same semantic request produce identical bytes in every byte surface.
    """

    __slots__ = ()

    @staticmethod
    def run(request: FixtureSplitRequest) -> FixtureSplitResult:
        """Compose the accepted layers into exactly one immutable result.

        The twelve-step validation order is controlling.  Steps 2 through 6 are
        enforced by ``FixtureSplitRequest`` construction, so a request that
        reaches this method has already satisfied them; this method performs step
        1 and then steps 7 through 12 in order.

        B1, B2A and B2B typed exceptions raised by the accepted modules propagate
        as themselves and are never translated into a facade error.
        """
        # 1. exact request type — no coercion of mappings, duck-typed objects,
        #    path-like objects, adapters, handles, URLs or external iterators.
        if type(request) is not FixtureSplitRequest:
            raise InvalidFixtureRequestError(
                "run requires an exact FixtureSplitRequest; no coercion is performed"
            )

        # 7. fixture identity
        fixture_sha256 = sha256_of_bytes(canonical_json_bytes(_fixture_identity_document(request)))
        if fixture_sha256 != request.fixture_sha256:
            raise FixtureIdentityMismatchError(
                "fixture_sha256 does not match the regenerated fixture identity digest"
            )

        # 8. request identity — bound to the recomputed digest, never the supplied one.
        derived_request_id = REQUEST_ID_PREFIX + sha256_of_bytes(
            canonical_json_bytes(_request_identity_document(request, fixture_sha256))
        )
        if derived_request_id != request.request_id:
            raise FixtureIdentityMismatchError(
                "request_id does not match the regenerated request identity"
            )

        # 9. B1 integration — the accepted functions are used, never reimplemented.
        joined = join_labels(
            request.ordered_rows,
            request.source_labels,
            transformation_version=request.transformation_version,
        )
        label_totals = _zeroed(DECISIONS)
        for example in joined:
            label_totals[example.decision] += 1
        targets = constrained_apportionment(label_totals, request.partition_totals)
        assignments = allocate_indivisible_groups(joined, targets)

        row_ordinals = _row_ordinals_by_example_id(joined)
        manifest = _compatibility_manifest(assignments, row_ordinals)

        # 10. artifact construction and fingerprint verification
        group_registry_bytes = _group_registry_bytes(assignments)
        example_registry_bytes = _example_registry_bytes(assignments, row_ordinals)
        excluded_ledger_bytes = canonical_json_bytes(dict(EXCLUDED_LEDGER_DOCUMENT))
        core = _summary_identity_core(joined, assignments)
        core_bytes = core.canonical_bytes()

        identity = build_split_fingerprint_identity(
            policy_id=request.policy_id,
            algorithm_version=ALGORITHM_VERSION,
            split_seed=SPLIT_SEED,
            group_registry_payload=group_registry_bytes,
            example_registry_payload=example_registry_bytes,
            excluded_ledger_payload=excluded_ledger_bytes,
            split_summary_identity_core=core,
        )
        record = build_split_fingerprint_record(identity)
        verify_split_fingerprint_record(record)

        summary_document_bytes = _split_summary_document_bytes(
            core, manifest.computed_split_hash, record.split_fingerprint
        )

        # 11. B2B report construction — explicit accepted findings only.  Sorting
        #     and aggregation are performed by the accepted B2B code, not here.
        audit_report = LeakageAuditReport.create(
            findings=request.leakage_findings,
            detection_methods=request.detection_methods,
        )

        result = FixtureSplitResult(
            request_id=request.request_id,
            split_manifest=manifest,
            group_registry_bytes=group_registry_bytes,
            example_registry_bytes=example_registry_bytes,
            excluded_ledger_bytes=excluded_ledger_bytes,
            split_summary_identity_core=core,
            split_summary_identity_core_bytes=core_bytes,
            split_summary_document_bytes=summary_document_bytes,
            split_fingerprint_record=record,
            audit_report=audit_report,
            audit_report_bytes=audit_report.to_canonical_bytes(),
            execution_evidence_ref=request.execution_evidence_ref,
        )

        # 12. final cross-object invariants
        _verify_invariants(request, joined, assignments, label_totals, result)
        return result


def _verify_invariants(
    request: FixtureSplitRequest,
    joined: Sequence[LabeledExample],
    assignments: Sequence[GroupAssignment],
    label_totals: Mapping[str, int],
    result: FixtureSplitResult,
) -> None:
    """Verify every cross-object invariant before a result is ever returned.

    Some invariants are statements about the request and the result together
    rather than about the result alone, so they are checked here, inside the run,
    using the validated request, the joined examples, the assignments and the
    constructed result.  Descriptor verification is delegated to the accepted
    B2A functions, whose typed errors propagate as themselves.
    """
    if result.request_id != request.request_id:
        raise FixtureIntegrationInvariantError("result request_id does not match the request")
    if result.execution_evidence_ref != request.execution_evidence_ref:
        raise FixtureIntegrationInvariantError(
            "result execution_evidence_ref does not match the request"
        )

    assigned_ids = [assignment.example_id for assignment in result.split_manifest.split_assignments]
    if len(set(assigned_ids)) != len(assigned_ids):
        raise FixtureIntegrationInvariantError("an example_id is assigned more than once")
    if set(assigned_ids) != {example.example_id for example in joined}:
        raise FixtureIntegrationInvariantError(
            "the manifest does not contain exactly the joined examples"
        )

    ordinals = [example.row_ordinal for example in joined]
    if len(set(ordinals)) != len(ordinals):
        raise FixtureIntegrationInvariantError("a row_ordinal occurs more than once")

    partition_by_document: dict[str, str] = {}
    for assignment in assignments:
        existing = partition_by_document.setdefault(
            assignment.source_document_id, assignment.partition
        )
        if existing != assignment.partition:
            raise FixtureIntegrationInvariantError("a source-document group crosses partitions")

    core = result.split_summary_identity_core
    observed_partitions = _zeroed(PARTITIONS)
    for assignment_row in result.split_manifest.split_assignments:
        observed_partitions[assignment_row.split] += 1
    if observed_partitions != dict(request.partition_totals):
        raise FixtureIntegrationInvariantError(
            "per-partition example counts do not reconcile with the request"
        )
    if dict(core.partition_totals) != observed_partitions:
        raise FixtureIntegrationInvariantError(
            "summary partition totals do not reconcile with the manifest"
        )
    if dict(core.label_totals) != dict(label_totals):
        raise FixtureIntegrationInvariantError(
            "summary label totals do not reconcile with the joined examples"
        )
    if sum(core.group_counts_by_partition.values()) != len(assignments):
        raise FixtureIntegrationInvariantError(
            "summary group counts do not reconcile with the assignments"
        )
    if core.total_example_count != len(joined) or core.total_group_count != len(assignments):
        raise FixtureIntegrationInvariantError("summary totals do not reconcile")
    if core.excluded_record_count != 0:
        raise FixtureIntegrationInvariantError("B2C authorizes no exclusion")

    payload_by_role = {
        "group_registry": result.group_registry_bytes,
        "example_registry": result.example_registry_bytes,
        "excluded_ledger": result.excluded_ledger_bytes,
        "split_summary": result.split_summary_identity_core_bytes,
    }
    verified: set[str] = set()
    for descriptor in result.split_fingerprint_record.identity.artifact_descriptors:
        payload = payload_by_role.get(descriptor.role)
        if payload is None:
            raise FixtureIntegrationInvariantError(
                f"unexpected artifact descriptor role {descriptor.role!r}"
            )
        # ``verify_split_fingerprint_record`` proves only the ``split_summary``
        # binding, because the record does not carry the other three payloads.
        # Each of those is therefore verified here against the exact bytes this
        # facade constructed.
        verify_descriptor_against_bytes(descriptor, payload)
        verified.add(descriptor.role)
    if verified != set(payload_by_role):
        raise FixtureIntegrationInvariantError("not every artifact descriptor was verified")

    verify_split_fingerprint_record(result.split_fingerprint_record)
    if result.split_summary_identity_core_bytes != core.canonical_bytes():
        raise FixtureIntegrationInvariantError(
            "summary identity core bytes do not match the carried core"
        )
    if result.audit_report_bytes != result.audit_report.to_canonical_bytes():
        raise FixtureIntegrationInvariantError("audit report bytes do not match the carried report")
    fingerprint = result.split_fingerprint_record.split_fingerprint
    if fingerprint.encode("utf-8") not in result.split_summary_document_bytes:
        raise FixtureIntegrationInvariantError(
            "the final summary does not carry the authoritative fingerprint"
        )
