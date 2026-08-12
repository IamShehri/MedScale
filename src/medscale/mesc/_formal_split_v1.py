"""Pure formal P01-04D input, policy and artifact layer (FD-DREADY-1 .. FD-DREADY-12).

This private module is the scientific half of the controlled formal executor.  It
performs no filesystem write, opens no socket, reads no clock and reads no
environment value.  Callers hand it decoded text and it returns exact immutable
artifact bytes.

It deliberately reuses the accepted pure primitives rather than restating them:
identity-safe source-label reduction, the exact fail-closed label join, canonical
example-ID derivation, constrained integer apportionment, deterministic SHA-256
ranking and indivisible source-document allocation all come from
``medscale.mesc._split_v1``; strict canonical JSON/JSONL bytes come from
``medscale.mesc._canonical_json_v1``; and descriptor construction, the
non-circular fingerprint and forbidden-metadata rejection come from
``medscale.mesc._split_artifacts_v1``.

Nothing here imports the fixture-only tooling.  ``FixtureSplitFacade``,
``_fixture_split_v1`` and ``_fixture_publication_v1`` have no role in formal
execution (FD-DREADY-2), so the group-identifier and registry record shapes that
those surfaces also implement are reconstructed here against the same accepted
artifact contract rather than imported across the boundary.

No artifact byte produced here contains question, context, answer or rationale
text, and no artifact byte contains a path, a date, a clock reading, a host name,
a user name, a process identifier or any environment value.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from medscale.mesc._canonical_json_v1 import (
    canonical_json_bytes,
    canonical_jsonl_bytes,
    sha256_of_bytes,
)
from medscale.mesc._split_artifacts_v1 import (
    ARTIFACT_SCHEMA_VERSIONS,
    SplitSummaryIdentityCore,
    build_split_fingerprint_identity,
    build_split_fingerprint_record,
    reject_forbidden_metadata,
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
    _allocate_indivisible_groups_with_minimum_deviation,
    constrained_apportionment,
    join_labels,
    source_label_from_envelope,
)
from medscale.mesc.split import PilotSplitAssignment, PilotSplitManifest

# ---------------------------------------------------------------------------
# Ratified scientific constants (D1, D2, D3, D4, D7, D8, D10)
# ---------------------------------------------------------------------------

#: D2 exact partition totals. Version 1 defines no tolerance.
TARGET_PARTITION_TOTALS: Final[Mapping[str, int]] = MappingProxyType(
    {"train": 700, "validation": 150, "test": 150}
)

#: D7 minimum sizes. Only validation and test carry a ratified minimum.
MINIMUM_PARTITION_SIZES: Final[Mapping[str, int]] = MappingProxyType(
    {"train": 0, "validation": 100, "test": 100}
)

GROUPING_KEY: Final = "source_document_id"
STRATIFICATION_FIELD: Final = "decision"
HOLDOUT_POLICY: Final = "none"
APPORTIONMENT_METHOD: Final = "constrained-integer-minimum-squared-deviation"

# ---------------------------------------------------------------------------
# Formal input surfaces
# ---------------------------------------------------------------------------

ORDERED_EXAMPLE_REGISTRY_SURFACE: Final = "ordered_example_registry"
SOURCE_DOCUMENT_REGISTRY_SURFACE: Final = "source_document_registry"
TRANSFORMED_DATASET_IDENTITY_SURFACE: Final = "transformed_dataset_identity"
SOURCE_RECORDS_SURFACE: Final = "source_records"
DECISION_RECORD_SURFACE: Final = "decision_record"

REQUIRED_INPUT_SURFACES: Final[tuple[str, ...]] = (
    DECISION_RECORD_SURFACE,
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    SOURCE_RECORDS_SURFACE,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
)

#: Canonical upstream schemas from accepted P01-03G / P01-03E artifacts.
CANONICAL_TRANSFORMED_DATASET_IDENTITY_SCHEMA: Final = "mesc-pubmedqa-transform/1"
CANONICAL_SOURCE_RECORD_SCHEMA: Final = "mesc-pubmedqa-source/1"

#: The exact closed member set of the accepted canonical P01-03E nested
#: scientific record, from the canonical producer implementation.  Every
#: member is required; nothing else is accepted (subset and superset are
#: both refused).
CANONICAL_SOURCE_RECORD_MEMBERS: Final[tuple[str, ...]] = (
    "schema_version",
    "dataset_id",
    "dataset_revision",
    "configuration",
    "original_example_id",
    "source_document_id",
    "pubid",
    "question",
    "context_segments",
    "mesh_terms",
    "long_answer",
    "final_decision",
    "reasoning_required_pred",
    "reasoning_free_pred",
    "license_id",
)

#: The execution-input manifest schema (P-C1a §5.1). It is deliberately distinct
#: from every artifact schema, and in particular from ``generation-manifest.json``
#: of the seven-file candidate bundle, which is a different concept (`F3`).
EXECUTION_INPUT_MANIFEST_SCHEMA: Final = "mesc-p01-04d-execution-input/manifest/v1"

#: Surfaces that carry a canonical schema version.  ``ordered_example_registry``
#: and ``source_document_registry`` have no per-row schema in the accepted
#: P01-03G artifacts, and ``decision_record`` is governance prose bound by
#: digest alone.
CANONICAL_SCHEMA_VERSIONS: Final[Mapping[str, str]] = MappingProxyType(
    {
        SOURCE_RECORDS_SURFACE: CANONICAL_SOURCE_RECORD_SCHEMA,
        TRANSFORMED_DATASET_IDENTITY_SURFACE: CANONICAL_TRANSFORMED_DATASET_IDENTITY_SCHEMA,
    }
)

# ---------------------------------------------------------------------------
# Formal artifact surfaces (FD-DREADY-6, FD-DREADY-7)
# ---------------------------------------------------------------------------

SPLIT_POLICY_SCHEMA: Final = "mesc-pilot-01-split-policy/1"
GROUP_REGISTRY_SCHEMA: Final = ARTIFACT_SCHEMA_VERSIONS["group_registry"]
EXAMPLE_REGISTRY_SCHEMA: Final = ARTIFACT_SCHEMA_VERSIONS["example_registry"]
EXCLUDED_LEDGER_SCHEMA: Final = ARTIFACT_SCHEMA_VERSIONS["excluded_ledger"]
SPLIT_SUMMARY_IDENTITY_CORE_SCHEMA: Final = ARTIFACT_SCHEMA_VERSIONS["split_summary"]
SPLIT_SUMMARY_DOCUMENT_SCHEMA: Final = "mesc-pilot-01-split-summary/1"
GENERATION_MANIFEST_SCHEMA: Final = "mesc-pilot-01-formal-generation-manifest/1"

GROUP_ID_SCHEMA: Final = "mesc-pilot-01-group/1"
GROUP_ID_PREFIX: Final = f"{GROUP_ID_SCHEMA}:sha256:"

SPLIT_POLICY_FILENAME: Final = "split-policy.json"
GROUP_REGISTRY_FILENAME: Final = "group-registry.jsonl"
EXAMPLE_REGISTRY_FILENAME: Final = "example-registry.jsonl"
EXCLUDED_LEDGER_FILENAME: Final = "excluded-ledger.json"
SPLIT_SUMMARY_IDENTITY_CORE_FILENAME: Final = "split-summary-identity-core.json"
SPLIT_SUMMARY_FILENAME: Final = "split-summary.json"
GENERATION_MANIFEST_FILENAME: Final = "generation-manifest.json"

#: The exact seven-file P01-04D candidate inventory. There is no eighth artifact
#: and no standalone ``split-fingerprint.json`` (FD-DREADY-6, FD-DREADY-7).
ARTIFACT_FILENAMES: Final[tuple[str, ...]] = (
    SPLIT_POLICY_FILENAME,
    GROUP_REGISTRY_FILENAME,
    EXAMPLE_REGISTRY_FILENAME,
    EXCLUDED_LEDGER_FILENAME,
    SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
    SPLIT_SUMMARY_FILENAME,
    GENERATION_MANIFEST_FILENAME,
)

ARTIFACT_SURFACES: Final[Mapping[str, str]] = MappingProxyType(
    {
        SPLIT_POLICY_FILENAME: "split_policy",
        GROUP_REGISTRY_FILENAME: "group_registry",
        EXAMPLE_REGISTRY_FILENAME: "example_registry",
        EXCLUDED_LEDGER_FILENAME: "excluded_ledger",
        SPLIT_SUMMARY_IDENTITY_CORE_FILENAME: "split_summary_identity_core",
        SPLIT_SUMMARY_FILENAME: "split_summary_document",
        GENERATION_MANIFEST_FILENAME: "generation_manifest",
    }
)

ARTIFACT_FILE_SCHEMAS: Final[Mapping[str, str]] = MappingProxyType(
    {
        SPLIT_POLICY_FILENAME: SPLIT_POLICY_SCHEMA,
        GROUP_REGISTRY_FILENAME: GROUP_REGISTRY_SCHEMA,
        EXAMPLE_REGISTRY_FILENAME: EXAMPLE_REGISTRY_SCHEMA,
        EXCLUDED_LEDGER_FILENAME: EXCLUDED_LEDGER_SCHEMA,
        SPLIT_SUMMARY_IDENTITY_CORE_FILENAME: SPLIT_SUMMARY_IDENTITY_CORE_SCHEMA,
        SPLIT_SUMMARY_FILENAME: SPLIT_SUMMARY_DOCUMENT_SCHEMA,
        GENERATION_MANIFEST_FILENAME: GENERATION_MANIFEST_SCHEMA,
    }
)

#: The six surfaces the manifest digests. It never digests itself.
MANIFEST_DIGESTED_FILENAMES: Final[tuple[str, ...]] = tuple(
    name for name in ARTIFACT_FILENAMES if name != GENERATION_MANIFEST_FILENAME
)

GENERATION_IDENTITIES: Final[tuple[str, ...]] = ("A", "B")

_SHA256_LENGTH: Final = 64
_HEX_DIGITS: Final = frozenset("0123456789abcdef")

#: Fields the accepted canonical P01-03E source record carries that must never
#: reach a split artifact.  The formal executor accepts the full canonical
#: record, validates it, then immediately reduces it to identity + final_decision
#: via ``source_label_from_envelope``; no entry below survives into memory beyond
#: the single line being reduced.
_CANONICAL_RECORD_SCIENTIFIC_FIELDS: Final[tuple[str, ...]] = (
    "context_segments",
    "license_id",
    "long_answer",
    "mesh_terms",
    "pubid",
    "question",
    "reasoning_free_pred",
    "reasoning_required_pred",
)


# ---------------------------------------------------------------------------
# Typed formal errors (FD-DREADY implementation contract §9)
# ---------------------------------------------------------------------------


class _FormalContractError(Exception):
    """Private common base for every formal fail-closed refusal.

    Only the ten named subclasses below are externally meaningful formal error
    identities; this base exists so a caller can catch the family without a
    tuple, and is never raised directly.
    """


class FormalInputIdentityError(_FormalContractError):
    """An input digest, byte size, dataset identity or canonical commit disagreed."""


class FormalInputSchemaError(_FormalContractError):
    """An input did not satisfy its declared schema, encoding or type contract."""


class FormalLabelJoinError(_FormalContractError):
    """The label join was not exact and total under the fail-closed join rules."""


class FormalWorkspaceSafetyError(_FormalContractError):
    """A workspace or protected-root configuration would allow an unsafe write."""


class FormalGenerationError(_FormalContractError):
    """A failure inside one generation, including an unknown generation identity."""


class FormalInventoryError(_FormalContractError):
    """A workspace whose contents are not exactly the seven candidate artifacts."""


class FormalByteEqualityError(_FormalContractError):
    """A byte inequality between Generation A and Generation B."""


class FormalFingerprintError(_FormalContractError):
    """An authoritative split fingerprint that could not be recomputed identically."""


class FormalMetadataError(_FormalContractError):
    """Prohibited runtime metadata reached a deterministic artifact."""


class FormalEvidenceConfigurationError(_FormalContractError):
    """An evidence-root configuration that a generator or validator must refuse."""


# ---------------------------------------------------------------------------
# Identity records
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FormalInputDescriptor:
    """Identity of exactly one formal input surface. Never its content."""

    surface: str
    schema_version: str | None
    sha256: str
    byte_size: int

    def __post_init__(self) -> None:
        if self.surface not in REQUIRED_INPUT_SURFACES:
            raise FormalInputIdentityError(f"unknown formal input surface: {self.surface!r}")
        _require_sha256(self.sha256, f"{self.surface} sha256")
        _require_count(self.byte_size, f"{self.surface} byte_size")

    def to_canonical_document(self) -> dict[str, object]:
        document: dict[str, object] = {
            "byte_size": self.byte_size,
            "sha256": self.sha256,
            "surface": self.surface,
        }
        if self.schema_version is not None:
            document["schema_version"] = self.schema_version
        return document


@dataclass(frozen=True, slots=True)
class FormalSplitInputIdentity:
    """Bound identity of the five formal inputs, and nothing else.

    It carries no file content, no label, no membership, no local path, no
    workspace path, no host name, no user name, no timestamp and no command line.
    """

    descriptors: tuple[FormalInputDescriptor, ...]

    def __post_init__(self) -> None:
        # Snapshot before validating, so the tuple that was validated is exactly
        # the tuple that is stored even if the caller passed a live sequence.
        snapshot = tuple(self.descriptors)
        object.__setattr__(self, "descriptors", snapshot)
        seen: list[str] = []
        for descriptor in snapshot:
            if not isinstance(descriptor, FormalInputDescriptor):
                raise FormalInputIdentityError(
                    "every input identity entry must be a FormalInputDescriptor"
                )
            if descriptor.surface in seen:
                raise FormalInputIdentityError(f"duplicate input surface: {descriptor.surface!r}")
            seen.append(descriptor.surface)
        missing = sorted(set(REQUIRED_INPUT_SURFACES) - set(seen))
        if missing:
            raise FormalInputIdentityError(f"missing formal input surfaces: {missing}")
        object.__setattr__(
            self, "descriptors", tuple(sorted(snapshot, key=lambda item: item.surface))
        )

    def descriptor(self, surface: str) -> FormalInputDescriptor:
        for descriptor in self.descriptors:
            if descriptor.surface == surface:
                return descriptor
        raise FormalInputIdentityError(f"unknown formal input surface: {surface!r}")

    def to_canonical_document(self) -> list[dict[str, object]]:
        return [descriptor.to_canonical_document() for descriptor in self.descriptors]


@dataclass(frozen=True, slots=True)
class ExecutionInputManifestIdentity:
    """The identity MODEL A-prime activation binds (P-C1a section 5.6).

    It is the SHA-256 and byte size of the exact canonical manifest bytes, and
    nothing else. Because the manifest carries no path, timestamp or repository
    commit, this identity is a pure function of the five formal input surfaces
    and is independently recomputable read-only.
    """

    sha256: str
    byte_size: int

    def __post_init__(self) -> None:
        _require_sha256(self.sha256, "execution input manifest sha256")
        _require_count(self.byte_size, "execution input manifest byte_size")


def build_execution_input_manifest(identity: FormalSplitInputIdentity) -> dict[str, object]:
    """Return the exact and closed two-field execution-input manifest (P-C1a §5.2).

    The per-surface entries come from the executor's own
    ``build_input_identity`` measurement, already ordered by surface and already
    omitting an absent ``schema_version`` rather than serializing ``null``.
    """
    if not isinstance(identity, FormalSplitInputIdentity):
        raise FormalInputIdentityError(
            "execution input manifest requires an exact FormalSplitInputIdentity"
        )
    return {
        "schema_version": EXECUTION_INPUT_MANIFEST_SCHEMA,
        "input_surfaces": identity.to_canonical_document(),
    }


def execution_input_manifest_bytes(identity: FormalSplitInputIdentity) -> bytes:
    """Serialize the manifest through the frozen canonical serializer (P-C1a §5.4)."""
    return canonical_json_bytes(build_execution_input_manifest(identity))


def execution_input_manifest_identity(
    identity: FormalSplitInputIdentity,
) -> ExecutionInputManifestIdentity:
    """Derive the execution-input-manifest identity from the five formal inputs."""
    payload = execution_input_manifest_bytes(identity)
    return ExecutionInputManifestIdentity(sha256=sha256_of_bytes(payload), byte_size=len(payload))


@dataclass(frozen=True, slots=True)
class FormalDatasetIdentity:
    """The canonical P01-03G transformed-dataset identity fields needed downstream.

    ``dataset_id``, ``dataset_revision`` and ``configuration`` are not carried
    by the canonical ``transformed-dataset-identity.json``; they are attested
    inside the accepted source records and enforced during the join.
    """

    transformation_version: str
    source_records_sha256: str
    source_records_byte_size: int
    record_count: int


@dataclass(frozen=True, slots=True)
class FormalArtifactEntry:
    """One digested artifact surface inside the generation manifest."""

    filename: str
    surface: str
    schema_version: str
    sha256: str
    byte_size: int

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "byte_size": self.byte_size,
            "filename": self.filename,
            "schema_version": self.schema_version,
            "sha256": self.sha256,
            "surface": self.surface,
        }


@dataclass(frozen=True, slots=True)
class FormalGenerationManifest:
    """The deterministic, non-circular P01-04D candidate-bundle manifest.

    It carries no generation identity, no workspace path, no repository path, no
    evidence path, no process identifier, no timestamp, no date, no host name, no
    user name, no command line, no interpreter path and no environment value, and
    neither its own digest nor its own byte size.  Generation A and Generation B
    therefore produce byte-identical manifest bytes from identical inputs and
    code (FD-DREADY-10).
    """

    schema_version: str
    algorithm_version: str
    bundle_filenames: tuple[str, ...]
    artifacts: tuple[FormalArtifactEntry, ...]
    input_identity: FormalSplitInputIdentity
    split_fingerprint: str

    def __post_init__(self) -> None:
        if self.schema_version != GENERATION_MANIFEST_SCHEMA:
            raise FormalInputSchemaError(
                f"manifest schema must be {GENERATION_MANIFEST_SCHEMA!r}, "
                f"got {self.schema_version!r}"
            )
        if self.algorithm_version != ALGORITHM_VERSION:
            raise FormalInputSchemaError(
                f"manifest algorithm must be {ALGORITHM_VERSION!r}, got {self.algorithm_version!r}"
            )
        if tuple(self.bundle_filenames) != ARTIFACT_FILENAMES:
            raise FormalInventoryError(
                f"manifest must list exactly {list(ARTIFACT_FILENAMES)}, "
                f"got {list(self.bundle_filenames)}"
            )
        digested = tuple(entry.filename for entry in self.artifacts)
        if digested != MANIFEST_DIGESTED_FILENAMES:
            raise FormalInventoryError(
                f"manifest must digest exactly {list(MANIFEST_DIGESTED_FILENAMES)}, "
                f"got {list(digested)}"
            )
        _require_sha256(self.split_fingerprint, "split_fingerprint")

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "algorithm_version": self.algorithm_version,
            "artifacts": [entry.to_canonical_document() for entry in self.artifacts],
            "bundle_filenames": list(self.bundle_filenames),
            "input_identity": self.input_identity.to_canonical_document(),
            "schema_version": self.schema_version,
            "split_fingerprint": self.split_fingerprint,
        }

    def canonical_bytes(self) -> bytes:
        document = self.to_canonical_document()
        _reject_metadata(document)
        return canonical_json_bytes(document)


@dataclass(frozen=True, slots=True)
class FormalArtifactBundle:
    """The exact seven in-memory candidate payloads and their bound fingerprint."""

    payloads: Mapping[str, bytes]
    split_fingerprint: str
    split_hash: str
    manifest: FormalGenerationManifest

    def __post_init__(self) -> None:
        frozen = MappingProxyType(dict(self.payloads))
        object.__setattr__(self, "payloads", frozen)
        if tuple(sorted(frozen)) != tuple(sorted(ARTIFACT_FILENAMES)):
            raise FormalInventoryError(
                f"bundle must contain exactly {sorted(ARTIFACT_FILENAMES)}, got {sorted(frozen)}"
            )
        _require_sha256(self.split_fingerprint, "split_fingerprint")

    def ordered_payloads(self) -> tuple[tuple[str, bytes], ...]:
        """Return the payloads in the canonical write order, manifest last."""
        return tuple((name, self.payloads[name]) for name in ARTIFACT_FILENAMES)


# ---------------------------------------------------------------------------
# Strict decoding helpers
# ---------------------------------------------------------------------------


def decode_utf8(payload: bytes, *, surface: str) -> str:
    """Decode exact UTF-8, refusing a BOM and any invalid sequence."""
    if not isinstance(payload, bytes):
        raise FormalInputSchemaError(f"{surface} payload must be bytes")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise FormalInputSchemaError(f"{surface} must not begin with a byte-order mark")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise FormalInputSchemaError(f"{surface} is not valid UTF-8") from error


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise FormalInputSchemaError(f"duplicate JSON object key: {key!r}")
        seen.add(key)
    return dict(pairs)


def _strict_json(text: str, *, surface: str) -> object:
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except FormalInputSchemaError:
        raise
    except ValueError as error:
        raise FormalInputSchemaError(f"{surface} is not valid JSON") from error


def _strict_json_object(text: str, *, surface: str) -> Mapping[str, object]:
    value = _strict_json(text, surface=surface)
    if not isinstance(value, dict):
        raise FormalInputSchemaError(f"{surface} must be a JSON object")
    return value


def _strict_jsonl_objects(text: str, *, surface: str) -> tuple[Mapping[str, object], ...]:
    if text == "":
        raise FormalInputSchemaError(f"{surface} must contain at least one record")
    if not text.endswith("\n"):
        raise FormalInputSchemaError(f"{surface} must end with exactly one line feed")
    if "\r" in text:
        raise FormalInputSchemaError(f"{surface} must use line-feed terminators only")
    records: list[Mapping[str, object]] = []
    for index, line in enumerate(text[:-1].split("\n")):
        if line.strip() == "":
            raise FormalInputSchemaError(f"{surface} record {index} is blank")
        value = _strict_json(line, surface=f"{surface} record {index}")
        if not isinstance(value, dict):
            raise FormalInputSchemaError(f"{surface} record {index} must be a JSON object")
        records.append(value)
    return tuple(records)


def _exact_keys(record: Mapping[str, object], expected: Sequence[str], *, surface: str) -> None:
    actual = sorted(record)
    if actual != sorted(expected):
        raise FormalInputSchemaError(
            f"{surface} must have exactly the members {sorted(expected)}, got {actual}"
        )


def _exact_str(record: Mapping[str, object], key: str, *, surface: str) -> str:
    value = record.get(key)
    if type(value) is not str or value == "" or value.strip() != value:
        raise FormalInputSchemaError(f"{surface}.{key} must be a non-blank untrimmed string")
    return value


def _exact_int(record: Mapping[str, object], key: str, *, surface: str) -> int:
    value = record.get(key)
    if type(value) is not int:
        raise FormalInputSchemaError(f"{surface}.{key} must be an exact integer")
    if value < 0:
        raise FormalInputSchemaError(f"{surface}.{key} must be non-negative")
    return value


def _require_schema(record: Mapping[str, object], expected: str, *, surface: str) -> None:
    value = _exact_str(record, "schema_version", surface=surface)
    if value != expected:
        raise FormalInputSchemaError(f"{surface} requires schema {expected!r}, got {value!r}")


def _require_sha256(value: object, field: str) -> str:
    if type(value) is not str or len(value) != _SHA256_LENGTH:
        raise FormalInputIdentityError(f"{field} must be 64 hexadecimal characters, got {value!r}")
    if any(character not in _HEX_DIGITS for character in value):
        raise FormalInputIdentityError(f"{field} must be lowercase hexadecimal, got {value!r}")
    return value


def _require_sha256_or_empty(value: object, field: str) -> str:
    """Require either a 64-hex sha256 or an empty string."""
    if value == "":
        return ""
    return _require_sha256(value, field)


def _require_count(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise FormalInputIdentityError(f"{field} must be a non-negative integer, got {value!r}")
    return value


def _reject_metadata(document: object) -> None:
    """Re-raise the accepted metadata refusal as the formal typed identity."""
    try:
        reject_forbidden_metadata(document)
    except Exception as error:
        raise FormalMetadataError(str(error)) from error


# ---------------------------------------------------------------------------
# Strict formal input parsers
# ---------------------------------------------------------------------------


def parse_ordered_example_registry(payload: bytes) -> tuple[OrderedExampleRow, ...]:
    """Parse the canonical P01-03G ordered example registry into identity-only rows.

    Canonical rows carry ``original_example_id``, ``row_ordinal``,
    ``source_document_id`` and ``source_record_hash``.  There is no per-row
    ``schema_version`` in the accepted artifact.
    """
    surface = ORDERED_EXAMPLE_REGISTRY_SURFACE
    text = decode_utf8(payload, surface=surface)
    rows: list[OrderedExampleRow] = []
    seen_ids: set[str] = set()
    seen_ordinals: set[int] = set()
    for index, record in enumerate(_strict_jsonl_objects(text, surface=surface)):
        location = f"{surface}[{index}]"
        _exact_keys(
            record,
            ("original_example_id", "row_ordinal", "source_document_id", "source_record_hash"),
            surface=location,
        )
        original_example_id = _exact_str(record, "original_example_id", surface=location)
        source_document_id = _exact_str(record, "source_document_id", surface=location)
        row_ordinal = _exact_int(record, "row_ordinal", surface=location)
        _require_sha256_or_empty(record.get("source_record_hash"), f"{location}.source_record_hash")
        if original_example_id in seen_ids:
            raise FormalInputSchemaError(f"duplicate original_example_id: {original_example_id!r}")
        if row_ordinal in seen_ordinals:
            raise FormalInputSchemaError(f"duplicate row_ordinal: {row_ordinal}")
        seen_ids.add(original_example_id)
        seen_ordinals.add(row_ordinal)
        rows.append(
            OrderedExampleRow(
                original_example_id=original_example_id,
                row_ordinal=row_ordinal,
                source_document_id=source_document_id,
            )
        )
    if sorted(seen_ordinals) != list(range(len(rows))):
        raise FormalInputSchemaError("row ordinals must be the exact contiguous range from zero")
    return tuple(rows)


def parse_source_document_registry(payload: bytes) -> Mapping[str, int]:
    """Parse the canonical P01-03G source-document registry.

    Canonical rows carry ``source_document_id``, ``example_count`` and
    ``row_ordinals``.  There is no per-row ``schema_version``.
    """
    surface = SOURCE_DOCUMENT_REGISTRY_SURFACE
    text = decode_utf8(payload, surface=surface)
    counts: dict[str, int] = {}
    for index, record in enumerate(_strict_jsonl_objects(text, surface=surface)):
        location = f"{surface}[{index}]"
        _exact_keys(
            record, ("example_count", "row_ordinals", "source_document_id"), surface=location
        )
        source_document_id = _exact_str(record, "source_document_id", surface=location)
        example_count = _exact_int(record, "example_count", surface=location)
        if example_count == 0:
            raise FormalInputSchemaError(f"{location}.example_count must be positive")
        row_ordinals = record.get("row_ordinals")
        if not isinstance(row_ordinals, list) or len(row_ordinals) != example_count:
            raise FormalInputSchemaError(
                f"{location}.row_ordinals must be a list of exactly {example_count} integers"
            )
        seen_ordinals: set[int] = set()
        for ordinal in row_ordinals:
            if type(ordinal) is not int or ordinal < 0:
                raise FormalInputSchemaError(
                    f"{location}.row_ordinals must contain only non-negative integers"
                )
            if ordinal in seen_ordinals:
                raise FormalInputSchemaError(
                    f"{location}.row_ordinals contains duplicate ordinal {ordinal}"
                )
            seen_ordinals.add(ordinal)
        if source_document_id in counts:
            raise FormalInputSchemaError(f"duplicate source_document_id: {source_document_id!r}")
        counts[source_document_id] = example_count
    return MappingProxyType(counts)


def parse_transformed_dataset_identity(payload: bytes) -> FormalDatasetIdentity:
    """Parse the canonical P01-03G transformed-dataset identity."""
    surface = TRANSFORMED_DATASET_IDENTITY_SURFACE
    text = decode_utf8(payload, surface=surface)
    record = _strict_json_object(text, surface=surface)
    _exact_keys(
        record,
        (
            "canonical_main",
            "decision_counts",
            "fingerprint",
            "p01_03e_output",
            "p01_03f_formal_validation",
            "p01_03g_authorization",
            "record_count",
            "schema_version",
            "source_artifact",
        ),
        surface=surface,
    )
    _require_schema(record, CANONICAL_TRANSFORMED_DATASET_IDENTITY_SCHEMA, surface=surface)
    p01_03e_output = record.get("p01_03e_output")
    if not isinstance(p01_03e_output, dict):
        raise FormalInputSchemaError(f"{surface}.p01_03e_output must be an object")
    output_files = p01_03e_output.get("output_files")
    if not isinstance(output_files, dict):
        raise FormalInputSchemaError(f"{surface}.p01_03e_output.output_files must be an object")
    sr_entry = output_files.get("source-records.jsonl")
    if not isinstance(sr_entry, dict):
        raise FormalInputSchemaError(
            f"{surface}.p01_03e_output.output_files['source-records.jsonl'] must be an object"
        )
    source_records_sha256 = _require_sha256(
        sr_entry.get("sha256"), f"{surface}.source_records_sha256"
    )
    source_records_byte_size = _exact_int(sr_entry, "byte_size", surface=surface)
    e_record_count = _exact_int(p01_03e_output, "record_count", surface=surface)
    t_record_count = _exact_int(record, "record_count", surface=surface)
    if e_record_count != t_record_count:
        raise FormalInputSchemaError(
            f"{surface}: p01_03e_output.record_count ({e_record_count}) "
            f"disagrees with top-level record_count ({t_record_count})"
        )
    transformation_version = _exact_str(record, "schema_version", surface=surface)
    return FormalDatasetIdentity(
        transformation_version=transformation_version,
        source_records_sha256=source_records_sha256,
        source_records_byte_size=source_records_byte_size,
        record_count=t_record_count,
    )


def parse_source_records(payload: bytes) -> tuple[SourceLabelRow, ...]:
    """Accept the canonical P01-03E source-record envelope and reduce immediately.

    The canonical envelope has no top-level ``schema_version``.  It carries
    ``record`` (a full scientific record including question, context, and
    annotation fields) and ``source_record_hash``.  The P01-04 rule is: accept
    the canonical input, validate it, immediately reduce to identity +
    ``final_decision`` via the accepted ``source_label_from_envelope``
    projection, and ensure no scientific text reaches any split artifact.

    The nested scientific record must carry the exact closed 15-member
    canonical field set and ``schema_version == mesc-pubmedqa-source/1``
    uniformly across all rows.
    """
    surface = SOURCE_RECORDS_SURFACE
    text = decode_utf8(payload, surface=surface)
    labels: list[SourceLabelRow] = []
    expected_schema = CANONICAL_SOURCE_RECORD_SCHEMA
    for index, envelope in enumerate(_strict_jsonl_objects(text, surface=surface)):
        location = f"{surface}[{index}]"
        _exact_keys(envelope, ("record", "source_record_hash"), surface=location)
        record = envelope.get("record")
        if not isinstance(record, dict):
            raise FormalInputSchemaError(f"{location}.record must be a JSON object")
        _exact_keys(record, CANONICAL_SOURCE_RECORD_MEMBERS, surface=f"{location}.record")
        actual_schema = _exact_str(record, "schema_version", surface=f"{location}.record")
        if actual_schema != expected_schema:
            raise FormalInputSchemaError(
                f"{location}.record requires schema {expected_schema!r}, got {actual_schema!r}"
            )
        try:
            labels.append(source_label_from_envelope(envelope))
        except Exception as error:
            raise FormalInputSchemaError(f"{location}: {error}") from error
    return tuple(labels)


def verify_input_digest(payload: bytes, descriptor: FormalInputDescriptor) -> None:
    """Recompute the digest and size of one formal input and reject disagreement."""
    actual_digest = sha256_of_bytes(payload)
    if actual_digest != descriptor.sha256:
        raise FormalInputIdentityError(
            f"surface {descriptor.surface!r} digest {descriptor.sha256!r} "
            f"does not match actual {actual_digest!r}"
        )
    if len(payload) != descriptor.byte_size:
        raise FormalInputIdentityError(
            f"surface {descriptor.surface!r} byte size {descriptor.byte_size} "
            f"does not match actual {len(payload)}"
        )


def _read_schema_from_json_object(payload: bytes, *, surface: str) -> str:
    """Lightweight extraction of ``schema_version`` from a canonical JSON object.

    This performs a shallow parse of the first JSON object in *payload* to read
    the ``schema_version`` field without a full structural parse.  It is used
    only inside ``build_input_identity`` to validate that a surface truly
    carries the canonical schema it claims.
    """
    text = decode_utf8(payload, surface=surface)
    record = _strict_json_object(text, surface=surface)
    return _exact_str(record, "schema_version", surface=surface)


def _read_source_record_schema(payload: bytes) -> str:
    """Read the schema from the first source-record envelope's nested record.

    The canonical P01-03E envelope is ``{"record": {...}, "source_record_hash":
    "..."}`` with no top-level ``schema_version``.
    ``record.schema_version`` must be ``mesc-pubmedqa-source/1`` uniformly
    across all rows.
    """
    surface = SOURCE_RECORDS_SURFACE
    text = decode_utf8(payload, surface=surface)
    envelopes = _strict_jsonl_objects(text, surface=surface)
    if not envelopes:
        raise FormalInputSchemaError(f"{surface} must contain at least one record")
    record = envelopes[0].get("record")
    if not isinstance(record, dict):
        raise FormalInputSchemaError(f"{surface}[0].record must be a JSON object")
    return _exact_str(record, "schema_version", surface=f"{surface}[0].record")


def build_input_identity(payloads: Mapping[str, bytes]) -> FormalSplitInputIdentity:
    """Bind identity for exactly the five formal input surfaces.

    Schema version is derived from the actual canonical content — not from
    internal constants — and is only recorded for surfaces where a canonical
    schema genuinely exists.
    """
    supplied = sorted(payloads)
    if supplied != sorted(REQUIRED_INPUT_SURFACES):
        raise FormalInputIdentityError(
            f"formal inputs must be exactly {sorted(REQUIRED_INPUT_SURFACES)}, got {supplied}"
        )
    descriptors: list[FormalInputDescriptor] = []
    for surface in sorted(REQUIRED_INPUT_SURFACES):
        payload = payloads[surface]
        sha = sha256_of_bytes(payload)
        size = len(payload)

        if surface in CANONICAL_SCHEMA_VERSIONS:
            expected = CANONICAL_SCHEMA_VERSIONS[surface]
            if surface == TRANSFORMED_DATASET_IDENTITY_SURFACE:
                actual = _read_schema_from_json_object(payload, surface=surface)
            elif surface == SOURCE_RECORDS_SURFACE:
                actual = _read_source_record_schema(payload)
            else:
                actual = ""
            if actual != expected:
                raise FormalInputSchemaError(
                    f"surface {surface!r} requires canonical schema {expected!r}, got {actual!r}"
                )
            schema: str | None = expected
        else:
            schema = None

        descriptors.append(
            FormalInputDescriptor(
                surface=surface,
                schema_version=schema,
                sha256=sha,
                byte_size=size,
            )
        )
    return FormalSplitInputIdentity(descriptors=tuple(descriptors))


# ---------------------------------------------------------------------------
# Scientific validation and artifact construction
# ---------------------------------------------------------------------------


def join_formal_examples(
    ordered_rows: Sequence[OrderedExampleRow],
    source_labels: Sequence[SourceLabelRow],
    dataset_identity: FormalDatasetIdentity,
    source_document_counts: Mapping[str, int],
) -> tuple[LabeledExample, ...]:
    """Perform the exact fail-closed join and every cross-input agreement check.

    Dataset identity (``dataset_id``, ``dataset_revision``, ``configuration``)
    is enforced inside ``join_labels`` which requires a single consistent
    identity across all source-label rows; it is not duplicated from the
    transformed-dataset identity, which does not carry those fields.
    """
    try:
        joined = join_labels(
            ordered_rows,
            source_labels,
            transformation_version=dataset_identity.transformation_version,
        )
    except Exception as error:
        raise FormalLabelJoinError(str(error)) from error

    if len(joined) != dataset_identity.record_count:
        raise FormalInputIdentityError(
            f"joined record count ({len(joined)}) disagrees with "
            f"transformed-dataset identity record_count ({dataset_identity.record_count})"
        )

    observed: dict[str, int] = {}
    for example in joined:
        observed[example.source_document_id] = observed.get(example.source_document_id, 0) + 1
    if observed != dict(source_document_counts):
        missing = sorted(set(source_document_counts) - set(observed))
        unexpected = sorted(set(observed) - set(source_document_counts))
        raise FormalInputIdentityError(
            "source-document registry disagrees with the ordered registry grouping: "
            f"missing={missing}, unexpected={unexpected}"
        )
    return joined


def allocate_formal_groups(joined: Sequence[LabeledExample]) -> tuple[GroupAssignment, ...]:
    """Apportion and allocate under the ratified D2/D4/D5/D6 contract."""
    expected_total = sum(TARGET_PARTITION_TOTALS.values())
    if len(joined) != expected_total:
        raise FormalGenerationError(
            f"formal generation requires exactly {expected_total} examples, got {len(joined)}"
        )
    label_totals: dict[str, int] = dict.fromkeys(DECISIONS, 0)
    for example in joined:
        label_totals[example.decision] += 1
    try:
        targets = constrained_apportionment(label_totals, dict(TARGET_PARTITION_TOTALS))
        assignments = _allocate_indivisible_groups_with_minimum_deviation(joined, targets)
    except Exception as error:
        raise FormalGenerationError(str(error)) from error

    totals: dict[str, int] = dict.fromkeys(PARTITIONS, 0)
    for assignment in assignments:
        totals[assignment.partition] += len(assignment.example_ids)
    if totals != dict(TARGET_PARTITION_TOTALS):
        raise FormalGenerationError(
            f"allocation produced {totals}, not the ratified {dict(TARGET_PARTITION_TOTALS)}"
        )
    for partition, minimum in MINIMUM_PARTITION_SIZES.items():
        if totals[partition] < minimum:
            raise FormalGenerationError(
                f"partition {partition!r} has {totals[partition]} examples, below the "
                f"ratified minimum {minimum}"
            )
    return assignments


def build_split_policy_document() -> dict[str, object]:
    """Return the deterministic, date-free versioned scientific policy (FD-DREADY-9)."""
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "apportionment_method": APPORTIONMENT_METHOD,
        "grouping_key": GROUPING_KEY,
        "holdout_policy": HOLDOUT_POLICY,
        "label_order": list(DECISIONS),
        "minimum_partition_sizes": dict(MINIMUM_PARTITION_SIZES),
        "partition_order": list(PARTITIONS),
        "ranking_key_schema": {
            "digest": "sha256",
            "members": ["algorithm_version", "seed", "source_document_id", "stratum"],
            "order": ["digest_ascending", "source_document_id_ascending", "row_ordinal_ascending"],
        },
        "schema_version": SPLIT_POLICY_SCHEMA,
        "serialization_rules": {
            "allow_nan": False,
            "encoding": "utf-8",
            "ensure_ascii": False,
            "separators": [",", ":"],
            "sort_keys": True,
            "terminal_line_feed": True,
        },
        "split_seed": SPLIT_SEED,
        "stratification_field": STRATIFICATION_FIELD,
        "target_counts": dict(TARGET_PARTITION_TOTALS),
    }


def build_split_policy_bytes() -> bytes:
    document = build_split_policy_document()
    _reject_metadata(document)
    return canonical_json_bytes(document)


def _group_id(assignment: GroupAssignment) -> str:
    payload = {
        "schema": GROUP_ID_SCHEMA,
        "source_document_id": assignment.source_document_id,
        "assigned_split": assignment.partition,
        "example_ids": sorted(assignment.example_ids),
        "row_ordinals": sorted(assignment.row_ordinals),
        "partition_key": assignment.partition_key,
    }
    return GROUP_ID_PREFIX + sha256_of_bytes(canonical_json_bytes(payload))


def build_group_registry_bytes(assignments: Sequence[GroupAssignment]) -> bytes:
    """Return canonical group-registry JSONL, ordered by assigned split then group id."""
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


def build_example_registry_bytes(
    assignments: Sequence[GroupAssignment], row_ordinals: Mapping[str, int]
) -> bytes:
    """Return canonical example-registry JSONL, ordered by split, ordinal then id."""
    ranked: list[tuple[str, int, str, dict[str, object]]] = []
    for assignment in assignments:
        for example_id in assignment.example_ids:
            if example_id not in row_ordinals:
                raise FormalGenerationError(
                    "assigned example_id is absent from the joined examples"
                )
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


def build_excluded_ledger_bytes(
    joined: Sequence[LabeledExample], assignments: Sequence[GroupAssignment]
) -> bytes:
    """Return the deterministic empty ledger, or fail closed.

    P01-04D version 1 expects the exact assigned population and no holdout, so a
    shortfall is a refusal rather than a ledger entry.
    """
    assigned: set[str] = set()
    for assignment in assignments:
        for example_id in assignment.example_ids:
            if example_id in assigned:
                raise FormalGenerationError(f"example {example_id!r} was assigned more than once")
            assigned.add(example_id)
    expected = {example.example_id for example in joined}
    if assigned != expected:
        missing = sorted(expected - assigned)
        unexpected = sorted(assigned - expected)
        raise FormalGenerationError(
            f"every example must be assigned exactly once: missing={len(missing)}, "
            f"unexpected={len(unexpected)}"
        )
    document = {
        "count": 0,
        "excluded_ids": [],
        "reason": "none",
        "schema_version": EXCLUDED_LEDGER_SCHEMA,
    }
    _reject_metadata(document)
    return canonical_json_bytes(document)


def build_summary_identity_core(
    joined: Sequence[LabeledExample], assignments: Sequence[GroupAssignment]
) -> SplitSummaryIdentityCore:
    """Return the fingerprint-free identity core with every combination explicit."""
    partition_totals: dict[str, int] = dict.fromkeys(PARTITIONS, 0)
    group_counts: dict[str, int] = dict.fromkeys(PARTITIONS, 0)
    label_totals: dict[str, int] = dict.fromkeys(DECISIONS, 0)
    matrix: dict[str, dict[str, int]] = {
        partition: dict.fromkeys(DECISIONS, 0) for partition in PARTITIONS
    }
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


def _compatibility_split_hash(
    assignments: Sequence[GroupAssignment], row_ordinals: Mapping[str, int]
) -> str:
    """Return the accepted 16-hex compatibility value. It is never authoritative."""
    partition_order = {partition: index for index, partition in enumerate(PARTITIONS)}
    ranked: list[tuple[int, int, str, PilotSplitAssignment]] = []
    for assignment in assignments:
        for example_id in assignment.example_ids:
            ranked.append(
                (
                    partition_order[assignment.partition],
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
    manifest = PilotSplitManifest(
        split_assignments=tuple(item[3] for item in ranked),
        split_hash="",
        split_seed=SPLIT_SEED,
    )
    return manifest.computed_split_hash


def build_formal_bundle(
    *,
    input_identity: FormalSplitInputIdentity,
    joined: Sequence[LabeledExample],
    assignments: Sequence[GroupAssignment],
) -> FormalArtifactBundle:
    """Build the exact seven candidate payloads and the authoritative fingerprint."""
    row_ordinals: dict[str, int] = {}
    for example in joined:
        if example.example_id in row_ordinals:
            raise FormalGenerationError("joined examples contain a duplicate example_id")
        row_ordinals[example.example_id] = example.row_ordinal

    policy_bytes = build_split_policy_bytes()
    group_registry_bytes = build_group_registry_bytes(assignments)
    example_registry_bytes = build_example_registry_bytes(assignments, row_ordinals)
    excluded_ledger_bytes = build_excluded_ledger_bytes(joined, assignments)
    core = build_summary_identity_core(joined, assignments)
    core_bytes = core.canonical_bytes()

    try:
        identity = build_split_fingerprint_identity(
            policy_id=SPLIT_POLICY_SCHEMA,
            algorithm_version=ALGORITHM_VERSION,
            split_seed=SPLIT_SEED,
            group_registry_payload=group_registry_bytes,
            example_registry_payload=example_registry_bytes,
            excluded_ledger_payload=excluded_ledger_bytes,
            split_summary_identity_core=core,
        )
        record = build_split_fingerprint_record(identity)
        verify_split_fingerprint_record(record)
    except Exception as error:
        raise FormalFingerprintError(str(error)) from error

    split_hash = _compatibility_split_hash(assignments, row_ordinals)
    summary_document = dict(core.to_canonical_document())
    summary_document["schema_version"] = SPLIT_SUMMARY_DOCUMENT_SCHEMA
    summary_document["split_hash"] = split_hash
    summary_document["split_fingerprint"] = record.split_fingerprint
    summary_bytes = canonical_json_bytes(summary_document)

    payloads: dict[str, bytes] = {
        SPLIT_POLICY_FILENAME: policy_bytes,
        GROUP_REGISTRY_FILENAME: group_registry_bytes,
        EXAMPLE_REGISTRY_FILENAME: example_registry_bytes,
        EXCLUDED_LEDGER_FILENAME: excluded_ledger_bytes,
        SPLIT_SUMMARY_IDENTITY_CORE_FILENAME: core_bytes,
        SPLIT_SUMMARY_FILENAME: summary_bytes,
    }
    manifest = FormalGenerationManifest(
        schema_version=GENERATION_MANIFEST_SCHEMA,
        algorithm_version=ALGORITHM_VERSION,
        bundle_filenames=ARTIFACT_FILENAMES,
        artifacts=tuple(
            FormalArtifactEntry(
                filename=filename,
                surface=ARTIFACT_SURFACES[filename],
                schema_version=ARTIFACT_FILE_SCHEMAS[filename],
                sha256=sha256_of_bytes(payloads[filename]),
                byte_size=len(payloads[filename]),
            )
            for filename in MANIFEST_DIGESTED_FILENAMES
        ),
        input_identity=input_identity,
        split_fingerprint=record.split_fingerprint,
    )
    payloads[GENERATION_MANIFEST_FILENAME] = manifest.canonical_bytes()
    return FormalArtifactBundle(
        payloads=payloads,
        split_fingerprint=record.split_fingerprint,
        split_hash=split_hash,
        manifest=manifest,
    )


def verify_bundle(bundle: FormalArtifactBundle) -> None:
    """Recompute every descriptor, the manifest bytes and the authoritative fingerprint."""
    payloads = bundle.payloads
    if tuple(sorted(payloads)) != tuple(sorted(ARTIFACT_FILENAMES)):
        raise FormalInventoryError(
            f"bundle inventory must be exactly {sorted(ARTIFACT_FILENAMES)}, got {sorted(payloads)}"
        )
    for entry in bundle.manifest.artifacts:
        payload = payloads[entry.filename]
        if entry.sha256 != sha256_of_bytes(payload):
            raise FormalFingerprintError(f"descriptor digest mismatch for {entry.filename!r}")
        if entry.byte_size != len(payload):
            raise FormalFingerprintError(f"descriptor byte size mismatch for {entry.filename!r}")
    if bundle.manifest.split_fingerprint != bundle.split_fingerprint:
        raise FormalFingerprintError("manifest fingerprint disagrees with the bundle fingerprint")
    if bundle.manifest.canonical_bytes() != payloads[GENERATION_MANIFEST_FILENAME]:
        raise FormalFingerprintError("manifest bytes are not reproducible from the manifest record")
    fingerprint = bundle.split_fingerprint.encode("utf-8")
    if fingerprint not in payloads[SPLIT_SUMMARY_FILENAME]:
        raise FormalFingerprintError("split summary does not carry the authoritative fingerprint")
    if fingerprint in payloads[SPLIT_SUMMARY_IDENTITY_CORE_FILENAME]:
        raise FormalFingerprintError("the fingerprint-free identity core must not carry it")
    policy_document = _strict_json(
        payloads[SPLIT_POLICY_FILENAME].decode("utf-8"), surface="policy"
    )
    _reject_metadata(policy_document)
    manifest_document = _strict_json(
        payloads[GENERATION_MANIFEST_FILENAME].decode("utf-8"), surface="manifest"
    )
    _reject_metadata(manifest_document)
    if not isinstance(manifest_document, dict):  # pragma: no cover - canonical bytes are an object
        raise FormalInputSchemaError("generation manifest must be a JSON object")
    for prohibited in ("generation", "generation_identity", "workspace"):
        if prohibited in manifest_document:
            raise FormalMetadataError(f"manifest must not carry {prohibited!r}")
