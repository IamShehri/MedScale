"""Private immutable split-artifact contracts and the non-circular fingerprint (FD-B2A-4..7).

The fingerprint is built in two layers so it can never contain itself
(FD-B2A-5).  ``SplitFingerprintIdentity`` holds only bound identity inputs and
is the sole hashed payload; ``SplitFingerprintRecord`` is constructed *after*
the digest exists and is never fed back into its own hash.  Because the identity
is a fixed-field frozen dataclass, ``split_fingerprint`` cannot appear inside it
by construction rather than by convention.

Nothing here reads the filesystem, the clock, the environment, or the network,
and nothing here mutates B1.  B1's 16-hex ``split_hash`` remains a
compatibility and display value only and is never authoritative (FD-B2-2).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import ClassVar, Final

from medscale.mesc._canonical_json_v1 import (
    CanonicalContractError,
    UnsupportedValueTypeError,
    canonical_json_bytes,
    sha256_of_bytes,
)

BUNDLE_SCHEMA_VERSION: Final = "mesc-pilot-01-split-fingerprint-bundle/1"

#: The exact role allowlist. Version 1 requires all four, and admits no others.
ARTIFACT_SCHEMA_VERSIONS: Final[Mapping[str, str]] = {
    "example_registry": "mesc-pilot-01-example-registry/1",
    "excluded_ledger": "mesc-pilot-01-excluded-ledger/1",
    "group_registry": "mesc-pilot-01-group-registry/1",
    "split_summary": "mesc-pilot-01-split-summary-identity-core/1",
}

#: Required roles in ascending canonical order.
REQUIRED_ARTIFACT_ROLES: Final[tuple[str, ...]] = tuple(sorted(ARTIFACT_SCHEMA_VERSIONS))

_HEX_DIGITS: Final = frozenset("0123456789abcdef")
_SHA256_LENGTH: Final = 64

# Key fragments that betray a date, a clock reading, or environment provenance.
# Both categories are prohibited from the fingerprinted payload (FD-B2A-5/6).
_DATE_KEY_FRAGMENTS: Final = ("date", "timestamp", "_at", "time", "clock", "epoch")
_RUNTIME_KEY_FRAGMENTS: Final = (
    "path",
    "username",
    "user",
    "hostname",
    "host",
    "machine",
    "platform",
    "python",
    "runtime",
    "environ",
    "env",
    "command",
    "cwd",
    "locale",
    "timezone",
)


class DuplicateArtifactRoleError(CanonicalContractError):
    """The same artifact role was supplied more than once."""

    code: ClassVar[str] = "duplicate_artifact_role"


class MissingArtifactRoleError(CanonicalContractError):
    """A required artifact role was absent."""

    code: ClassVar[str] = "missing_artifact_role"


class UnknownArtifactRoleError(CanonicalContractError):
    """A role outside the ratified version-1 allowlist."""

    code: ClassVar[str] = "unknown_artifact_role"


class InvalidSha256Error(CanonicalContractError):
    """A digest that is not 64 lowercase hex characters, or does not match its bytes."""

    code: ClassVar[str] = "invalid_sha256"


class InvalidByteSizeError(CanonicalContractError):
    """A byte size that is not a non-negative integer, or does not match its bytes."""

    code: ClassVar[str] = "invalid_byte_size"


class InvalidSchemaVersionError(CanonicalContractError):
    """A schema identifier that is empty, malformed, unknown, or wrong for its role."""

    code: ClassVar[str] = "invalid_schema_version"


class ForbiddenRuntimeMetadataError(CanonicalContractError):
    """Runtime, host, path, or environment provenance inside a fingerprinted payload."""

    code: ClassVar[str] = "forbidden_runtime_metadata"


class ForbiddenDateOrTimestampError(CanonicalContractError):
    """A date or timestamp inside a fingerprinted payload."""

    code: ClassVar[str] = "forbidden_date_or_timestamp"


class FingerprintMismatchError(CanonicalContractError):
    """A recomputed fingerprint disagreed with the bound one."""

    code: ClassVar[str] = "fingerprint_mismatch"


@dataclass(frozen=True, slots=True)
class SplitArtifactDescriptor:
    """One immutable artifact descriptor, validated on construction.

    Validation order is fixed: role, then schema version, then digest, then byte
    size.  An instance therefore never exists in an invalid state.
    """

    role: str
    schema_version: str
    sha256: str
    byte_size: int

    def __post_init__(self) -> None:
        if not isinstance(self.role, str) or self.role not in ARTIFACT_SCHEMA_VERSIONS:
            raise UnknownArtifactRoleError(f"unknown artifact role: {self.role!r}")
        expected_version = ARTIFACT_SCHEMA_VERSIONS[self.role]
        if not isinstance(self.schema_version, str) or self.schema_version != expected_version:
            raise InvalidSchemaVersionError(
                f"role {self.role!r} requires schema {expected_version!r}, "
                f"got {self.schema_version!r}"
            )
        _validate_sha256(self.sha256)
        _validate_byte_size(self.byte_size)

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "byte_size": self.byte_size,
            "role": self.role,
            "schema_version": self.schema_version,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class SplitSummaryIdentityCore:
    """Deterministic aggregate facts that bind the split, and nothing else.

    Per-example labels, raw question or context text, dates, runtime provenance,
    and the authoritative fingerprint itself are all structurally absent.
    """

    total_example_count: int
    total_group_count: int
    excluded_record_count: int
    partition_totals: Mapping[str, int]
    label_totals: Mapping[str, int]
    partition_label_matrix: Mapping[str, Mapping[str, int]]
    group_counts_by_partition: Mapping[str, int]
    algorithm_version: str
    schema_version: str = ARTIFACT_SCHEMA_VERSIONS["split_summary"]

    def __post_init__(self) -> None:
        for name in ("total_example_count", "total_group_count", "excluded_record_count"):
            _validate_count(getattr(self, name), name)
        for name in ("partition_totals", "label_totals", "group_counts_by_partition"):
            _validate_count_mapping(getattr(self, name), name)
        _validate_matrix(self.partition_label_matrix, "partition_label_matrix")
        if not isinstance(self.algorithm_version, str) or not self.algorithm_version:
            raise UnsupportedValueTypeError("algorithm_version must be a non-empty string")
        expected = ARTIFACT_SCHEMA_VERSIONS["split_summary"]
        if self.schema_version != expected:
            raise InvalidSchemaVersionError(
                f"split_summary requires schema {expected!r}, got {self.schema_version!r}"
            )

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "algorithm_version": self.algorithm_version,
            "excluded_record_count": self.excluded_record_count,
            "group_counts_by_partition": dict(self.group_counts_by_partition),
            "label_totals": dict(self.label_totals),
            "partition_label_matrix": {
                partition: dict(row) for partition, row in self.partition_label_matrix.items()
            },
            "partition_totals": dict(self.partition_totals),
            "schema_version": self.schema_version,
            "total_example_count": self.total_example_count,
            "total_group_count": self.total_group_count,
        }

    def canonical_bytes(self) -> bytes:
        """Return the exact bytes the ``split_summary`` descriptor digests."""
        document = self.to_canonical_document()
        reject_forbidden_metadata(document)
        return canonical_json_bytes(document)


@dataclass(frozen=True, slots=True)
class SplitFingerprintIdentity:
    """The sole hashed payload. It cannot contain ``split_fingerprint``."""

    bundle_schema_version: str
    policy_id: str
    algorithm_version: str
    split_seed: str
    artifact_descriptors: tuple[SplitArtifactDescriptor, ...]
    split_summary_identity_core: SplitSummaryIdentityCore

    def __post_init__(self) -> None:
        if self.bundle_schema_version != BUNDLE_SCHEMA_VERSION:
            raise InvalidSchemaVersionError(
                f"bundle schema must be {BUNDLE_SCHEMA_VERSION!r}, "
                f"got {self.bundle_schema_version!r}"
            )
        for name in ("policy_id", "algorithm_version", "split_seed"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise UnsupportedValueTypeError(f"{name} must be a non-empty string")
        # Normalize to role-ascending order so descriptor ordering can never
        # depend on the order the caller happened to supply.
        object.__setattr__(
            self, "artifact_descriptors", validate_descriptor_set(self.artifact_descriptors)
        )

    def to_canonical_document(self) -> dict[str, object]:
        return {
            "algorithm_version": self.algorithm_version,
            "artifact_descriptors": [
                descriptor.to_canonical_document() for descriptor in self.artifact_descriptors
            ],
            "bundle_schema_version": self.bundle_schema_version,
            "policy_id": self.policy_id,
            "split_seed": self.split_seed,
            "split_summary_identity_core": self.split_summary_identity_core.to_canonical_document(),
        }

    def canonical_bytes(self) -> bytes:
        document = self.to_canonical_document()
        reject_forbidden_metadata(document)
        return canonical_json_bytes(document)


@dataclass(frozen=True, slots=True)
class SplitFingerprintRecord:
    """The identity plus its computed digest. Never an input to its own hash."""

    identity: SplitFingerprintIdentity
    split_fingerprint: str

    def __post_init__(self) -> None:
        _validate_sha256(self.split_fingerprint)


def descriptor_for_bytes(*, role: str, payload: bytes) -> SplitArtifactDescriptor:
    """Bind a descriptor to the actual canonical bytes it describes."""
    if not isinstance(payload, bytes):
        raise UnsupportedValueTypeError(f"payload must be bytes, got {type(payload).__name__}")
    if role not in ARTIFACT_SCHEMA_VERSIONS:
        raise UnknownArtifactRoleError(f"unknown artifact role: {role!r}")
    return SplitArtifactDescriptor(
        role=role,
        schema_version=ARTIFACT_SCHEMA_VERSIONS[role],
        sha256=sha256_of_bytes(payload),
        byte_size=len(payload),
    )


def verify_descriptor_against_bytes(descriptor: SplitArtifactDescriptor, payload: bytes) -> None:
    """Recompute the digest and size and reject any disagreement."""
    actual_sha256 = sha256_of_bytes(payload)
    if descriptor.sha256 != actual_sha256:
        raise InvalidSha256Error(
            f"role {descriptor.role!r} digest {descriptor.sha256!r} "
            f"does not match actual bytes {actual_sha256!r}"
        )
    if descriptor.byte_size != len(payload):
        raise InvalidByteSizeError(
            f"role {descriptor.role!r} byte size {descriptor.byte_size} "
            f"does not match actual {len(payload)}"
        )


def validate_descriptor_set(
    descriptors: Sequence[SplitArtifactDescriptor],
) -> tuple[SplitArtifactDescriptor, ...]:
    """Reject duplicate, then missing, then unknown roles; return role-ascending order."""
    seen: set[str] = set()
    for descriptor in descriptors:
        if not isinstance(descriptor, SplitArtifactDescriptor):
            raise UnsupportedValueTypeError(
                f"descriptor must be a SplitArtifactDescriptor, got {type(descriptor).__name__}"
            )
        if descriptor.role in seen:
            raise DuplicateArtifactRoleError(f"duplicate artifact role: {descriptor.role!r}")
        seen.add(descriptor.role)
    missing = sorted(set(REQUIRED_ARTIFACT_ROLES) - seen)
    if missing:
        raise MissingArtifactRoleError(f"missing required artifact roles: {missing}")
    unknown = sorted(seen - set(REQUIRED_ARTIFACT_ROLES))
    if unknown:  # pragma: no cover - descriptor construction already rejects unknown roles
        raise UnknownArtifactRoleError(f"unknown artifact roles: {unknown}")
    return tuple(sorted(descriptors, key=lambda item: item.role))


def build_split_fingerprint_identity(
    *,
    policy_id: str,
    algorithm_version: str,
    split_seed: str,
    group_registry_payload: bytes,
    example_registry_payload: bytes,
    excluded_ledger_payload: bytes,
    split_summary_identity_core: SplitSummaryIdentityCore,
) -> SplitFingerprintIdentity:
    """Assemble the identity, deriving the ``split_summary`` digest from the core itself.

    The ``split_summary`` payload is computed here rather than accepted from the
    caller, so that descriptor can only ever digest the fingerprint-free
    identity core — step 1 and 2 of the ratified validation sequence.
    """
    descriptors = (
        descriptor_for_bytes(role="group_registry", payload=group_registry_payload),
        descriptor_for_bytes(role="example_registry", payload=example_registry_payload),
        descriptor_for_bytes(role="excluded_ledger", payload=excluded_ledger_payload),
        descriptor_for_bytes(
            role="split_summary", payload=split_summary_identity_core.canonical_bytes()
        ),
    )
    return SplitFingerprintIdentity(
        bundle_schema_version=BUNDLE_SCHEMA_VERSION,
        policy_id=policy_id,
        algorithm_version=algorithm_version,
        split_seed=split_seed,
        artifact_descriptors=validate_descriptor_set(descriptors),
        split_summary_identity_core=split_summary_identity_core,
    )


def compute_split_fingerprint(identity: SplitFingerprintIdentity) -> str:
    """Return the authoritative lowercase 64-hex SHA-256 over the identity bytes."""
    return sha256_of_bytes(identity.canonical_bytes())


def build_split_fingerprint_record(
    identity: SplitFingerprintIdentity,
) -> SplitFingerprintRecord:
    """Compute the fingerprint first, then construct the record around it."""
    return SplitFingerprintRecord(
        identity=identity, split_fingerprint=compute_split_fingerprint(identity)
    )


def verify_split_fingerprint_record(record: SplitFingerprintRecord) -> None:
    """Recompute the fingerprint from the bound identity and reject any mismatch."""
    recomputed = compute_split_fingerprint(record.identity)
    if recomputed != record.split_fingerprint:
        raise FingerprintMismatchError(
            f"bound fingerprint {record.split_fingerprint!r} does not match "
            f"recomputed {recomputed!r}"
        )


def reject_forbidden_metadata(document: object, *, _path: str = "") -> None:
    """Reject date, timestamp, and runtime-provenance keys anywhere in a payload.

    Dates are checked before runtime provenance so a key matching both
    categories always fails the same way.
    """
    if isinstance(document, Mapping):
        for key in sorted(str(key) for key in document):
            lowered = key.lower()
            location = f"{_path}.{key}" if _path else key
            if any(fragment in lowered for fragment in _DATE_KEY_FRAGMENTS):
                raise ForbiddenDateOrTimestampError(f"date or timestamp key at {location!r}")
            if any(fragment in lowered for fragment in _RUNTIME_KEY_FRAGMENTS):
                raise ForbiddenRuntimeMetadataError(f"runtime metadata key at {location!r}")
            reject_forbidden_metadata(document[key], _path=location)
    elif isinstance(document, list | tuple):
        for index, item in enumerate(document):
            reject_forbidden_metadata(item, _path=f"{_path}[{index}]")


def _validate_sha256(value: object) -> None:
    if not isinstance(value, str) or len(value) != _SHA256_LENGTH:
        raise InvalidSha256Error(f"sha256 must be {_SHA256_LENGTH} hex characters, got {value!r}")
    if not all(character in _HEX_DIGITS for character in value):
        raise InvalidSha256Error(f"sha256 must be lowercase hexadecimal, got {value!r}")


def _validate_byte_size(value: object) -> None:
    # ``bool`` must not satisfy an integer requirement, including byte size.
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidByteSizeError(f"byte_size must be a non-negative integer, got {value!r}")
    if value < 0:
        raise InvalidByteSizeError(f"byte_size must be a non-negative integer, got {value!r}")


def _validate_count(value: object, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise UnsupportedValueTypeError(f"{name} must be a non-negative integer, got {value!r}")
    if value < 0:
        raise UnsupportedValueTypeError(f"{name} must be a non-negative integer, got {value!r}")


def _validate_count_mapping(value: object, name: str) -> None:
    if not isinstance(value, Mapping):
        raise UnsupportedValueTypeError(f"{name} must be a string-keyed mapping")
    if any(not isinstance(key, str) for key in value):
        raise UnsupportedValueTypeError(f"{name} keys must be strings")
    for key in sorted(value):
        _validate_count(value[key], f"{name}[{key!r}]")


def _validate_matrix(value: object, name: str) -> None:
    if not isinstance(value, Mapping):
        raise UnsupportedValueTypeError(f"{name} must be a string-keyed mapping")
    for key in sorted(str(key) for key in value):
        _validate_count_mapping(value[key], f"{name}[{key!r}]")
