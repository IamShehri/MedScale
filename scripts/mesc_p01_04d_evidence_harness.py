"""The P01-04D external execution-evidence harness (XD-EXEC-1, ARCHITECTURE A).

This script implements the contract adopted in
``specs/mesc-pilot-01/p01-04d-execution-evidence-harness/``.  It wraps the
canonical formal operator as a separate child process and records the runtime
facts of one execution episode into an external evidence location.  It adds no
scientific authority: it never derives a split, never mutates a generation
workspace, and never writes inside the repository or the future evidence root.

It provides exactly six commands and no seventh:

``open``
    Creates ``episode-core.json`` once, binding the canonical commit, the
    operator identity, this harness's own identity and the runtime identity.

``generate``
    Runs exactly one operator ``generate`` child and records one stage journal.

``compare``
    Runs exactly one operator ``compare`` child, derives the seven-file
    byte-equality ledger independently, and records one stage journal.

``verify``
    Reruns canonical compare as episode self-verification.  It is not P01-04F
    independent verification and it does not authorize P01-04F.

``invalidate``
    Appends one pre-seal invalidation record.  It is the only command that may
    create or append ``episode-invalidation.jsonl``.

``finalize``
    Creates the write-once terminal manifest.  Finalize is the last P-A
    mutation to an execution episode.

There is no ``record-freeze`` command.  Obligations 11 and 12 remain P01-04F
obligations and are not satisfied here.

Running this script does not authorize P01-04D execution over protected inputs.
That remains a separate founder decision.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import platform
import stat
import subprocess
import sys
import time
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import ClassVar, Final

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_SOURCE_ROOT = _REPOSITORY_ROOT / "src"
if _SOURCE_ROOT.is_dir() and str(_SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SOURCE_ROOT))

# Only pure canonical serialization and digest primitives are reused (PA1-C3, §27).
# Importing the formal generation or formal split modules is prohibited here.
from medscale.mesc._canonical_json_v1 import (  # noqa: E402 - after the path bootstrap
    canonical_json_bytes,
    sha256_of_bytes,
)

# ---------------------------------------------------------------------------
# Repository-relative identities (§15.1)
# ---------------------------------------------------------------------------

#: POSIX "/" separators regardless of host OS.
OPERATOR_RELATIVE_PATH: Final = "scripts/mesc_p01_04d_operator.py"
HARNESS_RELATIVE_PATH: Final = "scripts/mesc_p01_04d_evidence_harness.py"

# ---------------------------------------------------------------------------
# Evidence inventory — exact and closed, seven record classes (§12, §12.1)
# ---------------------------------------------------------------------------

EPISODE_CORE_FILENAME: Final = "episode-core.json"
STAGE_GENERATE_A_FILENAME: Final = "stage-generate-a.jsonl"
STAGE_GENERATE_B_FILENAME: Final = "stage-generate-b.jsonl"
STAGE_COMPARE_FILENAME: Final = "stage-compare.jsonl"
STAGE_VERIFY_FILENAME: Final = "stage-verify.jsonl"
EPISODE_INVALIDATION_FILENAME: Final = "episode-invalidation.jsonl"
EPISODE_MANIFEST_FILENAME: Final = "episode-manifest.json"

#: The complete evidence inventory. An eighth record class is prohibited.
EVIDENCE_FILENAMES: Final[tuple[str, ...]] = (
    EPISODE_CORE_FILENAME,
    STAGE_GENERATE_A_FILENAME,
    STAGE_GENERATE_B_FILENAME,
    STAGE_COMPARE_FILENAME,
    STAGE_VERIFY_FILENAME,
    EPISODE_INVALIDATION_FILENAME,
    EPISODE_MANIFEST_FILENAME,
)

#: Journals the terminal manifest binds through ``records[]``, in canonical order.
BOUND_RECORD_FILENAMES: Final[tuple[str, ...]] = (
    STAGE_GENERATE_A_FILENAME,
    STAGE_GENERATE_B_FILENAME,
    STAGE_COMPARE_FILENAME,
    STAGE_VERIFY_FILENAME,
    EPISODE_INVALIDATION_FILENAME,
)

# ---------------------------------------------------------------------------
# Schema versions (§8 deterministic implementation decisions)
# ---------------------------------------------------------------------------

EPISODE_CORE_SCHEMA_VERSION: Final = "mesc-p01-04d-execution-evidence/episode-core/v1"
STAGE_EVENT_SCHEMA_VERSION: Final = "mesc-p01-04d-execution-evidence/stage-event/v1"
INVALIDATION_SCHEMA_VERSION: Final = "mesc-p01-04d-execution-evidence/invalidation-event/v1"
EPISODE_MANIFEST_SCHEMA_VERSION: Final = "mesc-p01-04d-execution-evidence/episode-manifest/v1"

# ---------------------------------------------------------------------------
# Scientific artifact inventory — exactly seven candidate filenames (§10)
# ---------------------------------------------------------------------------

CANDIDATE_FILENAMES: Final[tuple[str, ...]] = (
    "split-policy.json",
    "group-registry.jsonl",
    "example-registry.jsonl",
    "excluded-ledger.json",
    "split-summary-identity-core.json",
    "split-summary.json",
    "generation-manifest.json",
)

GENERATION_MANIFEST_FILENAME: Final = "generation-manifest.json"
SPLIT_FINGERPRINT_KEY: Final = "split_fingerprint"

# ---------------------------------------------------------------------------
# Formal input surfaces — production string literals, never imported (§9, §27)
# ---------------------------------------------------------------------------

ORDERED_EXAMPLE_REGISTRY_SURFACE: Final = "ordered_example_registry"
SOURCE_DOCUMENT_REGISTRY_SURFACE: Final = "source_document_registry"
TRANSFORMED_DATASET_IDENTITY_SURFACE: Final = "transformed_dataset_identity"
SOURCE_RECORDS_SURFACE: Final = "source_records"
DECISION_RECORD_SURFACE: Final = "decision_record"

INPUT_SURFACES: Final[tuple[str, ...]] = (
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
    SOURCE_RECORDS_SURFACE,
    DECISION_RECORD_SURFACE,
)

#: One-to-one with the five logical input surfaces (§20.10).
SURFACE_PATH_ROLES: Final[Mapping[str, str]] = {
    ORDERED_EXAMPLE_REGISTRY_SURFACE: "FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY",
    SOURCE_DOCUMENT_REGISTRY_SURFACE: "FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY",
    TRANSFORMED_DATASET_IDENTITY_SURFACE: "FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY",
    SOURCE_RECORDS_SURFACE: "FORMAL_INPUT_SOURCE_RECORDS",
    DECISION_RECORD_SURFACE: "FORMAL_INPUT_DECISION_RECORD",
}

#: The operator's argument name for each surface, in operator argument order.
SURFACE_ARGUMENTS: Final[Mapping[str, str]] = {
    ORDERED_EXAMPLE_REGISTRY_SURFACE: "--ordered-example-registry",
    SOURCE_DOCUMENT_REGISTRY_SURFACE: "--source-document-registry",
    TRANSFORMED_DATASET_IDENTITY_SURFACE: "--transformed-dataset-identity",
    SOURCE_RECORDS_SURFACE: "--source-records",
    DECISION_RECORD_SURFACE: "--decision-record",
}

# ---------------------------------------------------------------------------
# Closed vocabularies — ten named enumerations, seventy-seven values (§20)
# ---------------------------------------------------------------------------

ROOT_CAUSE_CLASSES: Final[tuple[str, ...]] = (
    "CANONICAL_MAIN_MOVEMENT",
    "HARNESS_IDENTITY_MISMATCH",
    "OPERATOR_IDENTITY_MISMATCH",
    "RUNTIME_IDENTITY_MISMATCH",
    "INPUT_IDENTITY_FAILURE",
    "INPUT_SCHEMA_FAILURE",
    "PATH_SAFETY_FAILURE",
    "WORKSPACE_STATE_FAILURE",
    "OUTPUT_INVENTORY_FAILURE",
    "BYTE_INEQUALITY",
    "FINGERPRINT_FAILURE",
    "EVIDENCE_INTEGRITY_FAILURE",
    "EVIDENCE_CONFIGURATION_FAILURE",
    "CHILD_PROCESS_FAILURE",
    "UNDETERMINED",
)

CAUSAL_STAGES: Final[tuple[str, ...]] = (
    "PREFLIGHT",
    "OPEN",
    "GENERATE_A",
    "GENERATE_B",
    "COMPARE",
    "VERIFY",
    "INVALIDATE",
    "FINALIZE",
)

FAILURE_CLASSES: Final[tuple[str, ...]] = (
    "ARGUMENT_REFUSAL",
    "CANONICAL_MAIN_MISMATCH",
    "PATH_SEPARATION_REFUSAL",
    "REPARSE_POINT_REFUSAL",
    "HARNESS_IDENTITY_MISMATCH",
    "OPERATOR_IDENTITY_MISMATCH",
    "RUNTIME_IDENTITY_MISMATCH",
    "INPUT_HASH_FAILURE",
    "INPUT_IDENTITY_MISMATCH",
    "CHILD_LAUNCH_FAILURE",
    "CHILD_NONZERO_EXIT",
    "OUTPUT_INVENTORY_MISMATCH",
    "OUTPUT_HASH_FAILURE",
    "BYTE_INEQUALITY",
    "COMPARE_CONTRADICTION",
    "FINGERPRINT_MISMATCH",
    "EVIDENCE_WRITE_FAILURE",
    "EVIDENCE_MALFORMED_PRESERVED",
    "VERIFY_FAILURE",
    "EPISODE_PATH_IDENTITY_DRIFT",
    "UNCLASSIFIED",
)

REMEDIATION_DISPOSITIONS: Final[tuple[str, ...]] = (
    "NO_REMEDIATION_AUTHORIZED",
    "NEW_EPISODE_REQUIRED",
    "FOUNDER_DISPOSITION_REQUIRED",
    "LATER_STAGE_GOVERNANCE_REQUIRED",
)

RECORD_INTEGRITIES: Final[tuple[str, ...]] = ("WELL_FORMED", "MALFORMED_PRESERVED")

COMPARISON_DISPOSITIONS: Final[tuple[str, ...]] = (
    "EQUAL_VERIFIED",
    "INTEGRITY_FAILURE",
    "BYTE_INEQUALITY",
    "CONTRADICTION",
)

TERMINAL_DISPOSITIONS: Final[tuple[str, ...]] = (
    "EPISODE_COMPLETE_EQUAL",
    "EPISODE_FAILED",
    "EPISODE_INVALIDATED",
    "EPISODE_REFUSED",
    "EPISODE_EVIDENCE_CORRUPT",
)

OPERATOR_ERROR_CLASSES: Final[tuple[str, ...]] = (
    "NO_ERROR",
    "BYTE_EQUALITY_ERROR",
    "INPUT_IDENTITY_ERROR",
    "INPUT_SCHEMA_ERROR",
    "INVENTORY_ERROR",
    "FINGERPRINT_ERROR",
    "METADATA_ERROR",
    "WORKSPACE_SAFETY_ERROR",
    "EVIDENCE_CONFIGURATION_ERROR",
    "GENERATION_ERROR",
    "UNCLASSIFIED",
)

STAGE_DISPOSITIONS: Final[tuple[str, ...]] = (
    "STAGE_COMPLETE",
    "STAGE_REFUSED",
    "STAGE_FAILED",
)

PATH_ROLES: Final[tuple[str, ...]] = (
    "FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY",
    "FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY",
    "FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY",
    "FORMAL_INPUT_SOURCE_RECORDS",
    "FORMAL_INPUT_DECISION_RECORD",
)

#: The named closed-enumeration ledger of §20: ten enumerations, seventy-seven values.
CLOSED_VOCABULARIES: Final[Mapping[str, tuple[str, ...]]] = {
    "root_cause_class": ROOT_CAUSE_CLASSES,
    "causal_stage": CAUSAL_STAGES,
    "failure_class": FAILURE_CLASSES,
    "remediation_disposition": REMEDIATION_DISPOSITIONS,
    "record_integrity": RECORD_INTEGRITIES,
    "comparison_disposition": COMPARISON_DISPOSITIONS,
    "terminal_disposition": TERMINAL_DISPOSITIONS,
    "operator_error_class": OPERATOR_ERROR_CLASSES,
    "stage_disposition": STAGE_DISPOSITIONS,
    "path_role": PATH_ROLES,
}

# Fixed inline domains (§15.2). Closed, but outside the 10 / 77 named ledger.
STAGES: Final[tuple[str, ...]] = ("GENERATE_A", "GENERATE_B", "COMPARE", "VERIFY")
GENERATION_IDENTITIES: Final[tuple[str, ...]] = ("A", "B")
BYTE_EQUALITIES: Final[tuple[str, ...]] = ("EQUAL", "UNEQUAL")
OBSERVATION_MODES: Final[tuple[str, ...]] = ("CONTINUATION", "CONTAINMENT")

#: Stage name to journal filename.
STAGE_JOURNALS: Final[Mapping[str, str]] = {
    "GENERATE_A": STAGE_GENERATE_A_FILENAME,
    "GENERATE_B": STAGE_GENERATE_B_FILENAME,
    "COMPARE": STAGE_COMPARE_FILENAME,
    "VERIFY": STAGE_VERIFY_FILENAME,
}

# ---------------------------------------------------------------------------
# Failure mapping (§19.1, §19.2)
# ---------------------------------------------------------------------------

#: Total over the twenty ``failure_class`` values; ``CHILD_NONZERO_EXIT`` defers to §19.2.
FAILURE_TRIAD: Final[Mapping[str, tuple[str, str]]] = {
    "ARGUMENT_REFUSAL": ("EVIDENCE_CONFIGURATION_FAILURE", "NEW_EPISODE_REQUIRED"),
    "CANONICAL_MAIN_MISMATCH": ("CANONICAL_MAIN_MOVEMENT", "FOUNDER_DISPOSITION_REQUIRED"),
    "PATH_SEPARATION_REFUSAL": ("PATH_SAFETY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "REPARSE_POINT_REFUSAL": ("PATH_SAFETY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "HARNESS_IDENTITY_MISMATCH": ("HARNESS_IDENTITY_MISMATCH", "FOUNDER_DISPOSITION_REQUIRED"),
    "OPERATOR_IDENTITY_MISMATCH": ("OPERATOR_IDENTITY_MISMATCH", "FOUNDER_DISPOSITION_REQUIRED"),
    "RUNTIME_IDENTITY_MISMATCH": ("RUNTIME_IDENTITY_MISMATCH", "FOUNDER_DISPOSITION_REQUIRED"),
    "INPUT_HASH_FAILURE": ("INPUT_IDENTITY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "INPUT_IDENTITY_MISMATCH": ("INPUT_IDENTITY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "CHILD_LAUNCH_FAILURE": ("CHILD_PROCESS_FAILURE", "NEW_EPISODE_REQUIRED"),
    "OUTPUT_INVENTORY_MISMATCH": ("OUTPUT_INVENTORY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "OUTPUT_HASH_FAILURE": ("EVIDENCE_INTEGRITY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "BYTE_INEQUALITY": ("BYTE_INEQUALITY", "FOUNDER_DISPOSITION_REQUIRED"),
    "COMPARE_CONTRADICTION": ("EVIDENCE_INTEGRITY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "FINGERPRINT_MISMATCH": ("FINGERPRINT_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "EVIDENCE_WRITE_FAILURE": ("EVIDENCE_INTEGRITY_FAILURE", "NO_REMEDIATION_AUTHORIZED"),
    "EVIDENCE_MALFORMED_PRESERVED": ("EVIDENCE_INTEGRITY_FAILURE", "NO_REMEDIATION_AUTHORIZED"),
    "VERIFY_FAILURE": ("EVIDENCE_INTEGRITY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    # An in-flight episode-path swap is adversarial, not a configuration mistake.
    "EPISODE_PATH_IDENTITY_DRIFT": ("PATH_SAFETY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "UNCLASSIFIED": ("UNDETERMINED", "FOUNDER_DISPOSITION_REQUIRED"),
}

#: Total over the eleven ``operator_error_class`` values (§19.2).
CHILD_NONZERO_EXIT_TRIAD: Final[Mapping[str, tuple[str, str]]] = {
    "INPUT_IDENTITY_ERROR": ("INPUT_IDENTITY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "INPUT_SCHEMA_ERROR": ("INPUT_SCHEMA_FAILURE", "NEW_EPISODE_REQUIRED"),
    "WORKSPACE_SAFETY_ERROR": ("WORKSPACE_STATE_FAILURE", "NEW_EPISODE_REQUIRED"),
    "GENERATION_ERROR": ("CHILD_PROCESS_FAILURE", "NEW_EPISODE_REQUIRED"),
    "INVENTORY_ERROR": ("OUTPUT_INVENTORY_FAILURE", "NEW_EPISODE_REQUIRED"),
    "BYTE_EQUALITY_ERROR": ("BYTE_INEQUALITY", "FOUNDER_DISPOSITION_REQUIRED"),
    "FINGERPRINT_ERROR": ("FINGERPRINT_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "METADATA_ERROR": ("EVIDENCE_INTEGRITY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "EVIDENCE_CONFIGURATION_ERROR": ("EVIDENCE_CONFIGURATION_FAILURE", "NEW_EPISODE_REQUIRED"),
    "UNCLASSIFIED": ("UNDETERMINED", "FOUNDER_DISPOSITION_REQUIRED"),
    # Contract contradiction: NO_ERROR is reserved for exit code zero. Fail closed.
    "NO_ERROR": ("UNDETERMINED", "FOUNDER_DISPOSITION_REQUIRED"),
}

#: The exact closed set that may seal ``STAGE_REFUSED`` (§20.9, PIC-CORR-1).
REFUSAL_FAILURE_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "CANONICAL_MAIN_MISMATCH",
        "HARNESS_IDENTITY_MISMATCH",
        "OPERATOR_IDENTITY_MISMATCH",
        "RUNTIME_IDENTITY_MISMATCH",
        "INPUT_IDENTITY_MISMATCH",
    }
)


def derive_failure_triad(
    failure_class: str, operator_error_class: str | None = None
) -> tuple[str, str, str]:
    """Return the exact ``(failure_class, root_cause_class, remediation_disposition)``.

    ``failure_class`` is observed; the other two are derived, never chosen
    (PIC-CORR-2, PIC-CORR-3).  ``CHILD_NONZERO_EXIT`` derives from the
    ``operator_error_class`` already recorded on ``child_exited``, so a child
    failure has exactly one classification source.
    """
    if failure_class not in FAILURE_CLASSES:
        raise ValueError(f"failure_class outside the closed enumeration: {failure_class!r}")
    if failure_class == "CHILD_NONZERO_EXIT":
        if operator_error_class is None:
            raise ValueError("CHILD_NONZERO_EXIT requires an operator_error_class")
        if operator_error_class not in CHILD_NONZERO_EXIT_TRIAD:
            raise ValueError(f"operator_error_class outside enumeration: {operator_error_class!r}")
        root_cause, remediation = CHILD_NONZERO_EXIT_TRIAD[operator_error_class]
        return failure_class, root_cause, remediation
    root_cause, remediation = FAILURE_TRIAD[failure_class]
    return failure_class, root_cause, remediation


# ---------------------------------------------------------------------------
# Operator stderr classification (§20.8.1, §20.8.2, §20.8.2.1, §20.8.2.2)
# ---------------------------------------------------------------------------

#: A classification constant only. Carrying it grants no import of the module it names.
FORMAL_EXCEPTION_MODULE: Final = "medscale.mesc._formal_split_v1"
_EXCEPTION_PREFIX: Final[bytes] = b"medscale.mesc._formal_split_v1."

#: The exact ten allowlisted tokens (PIC-9). No other token is allowlisted.
EXCEPTION_TOKEN_CLASSES: Final[Mapping[str, str]] = {
    "FormalInputIdentityError": "INPUT_IDENTITY_ERROR",
    "FormalInputSchemaError": "INPUT_SCHEMA_ERROR",
    "FormalLabelJoinError": "INPUT_SCHEMA_ERROR",
    "FormalWorkspaceSafetyError": "WORKSPACE_SAFETY_ERROR",
    "FormalGenerationError": "GENERATION_ERROR",
    "FormalInventoryError": "INVENTORY_ERROR",
    "FormalByteEqualityError": "BYTE_EQUALITY_ERROR",
    "FormalFingerprintError": "FINGERPRINT_ERROR",
    "FormalMetadataError": "METADATA_ERROR",
    "FormalEvidenceConfigurationError": "EVIDENCE_CONFIGURATION_ERROR",
}


def classify_operator_stderr(stderr: bytes) -> str:
    """Return exactly one ``operator_error_class`` from raw stderr bytes.

    The scan is byte-level and fixed (PIC-CORR-8): stderr is never decoded as a
    whole, only the final non-empty logical line is inspected, and message bytes
    after the optional colon are untrusted and ignored.  Nothing derived here
    carries raw class text or raw message text into durable evidence.
    """
    segments = stderr.split(b"\n")
    normalized = [segment[:-1] if segment.endswith(b"\r") else segment for segment in segments]
    non_empty = [segment for segment in normalized if segment]
    if not non_empty:
        return "UNCLASSIFIED"
    line = non_empty[-1]
    if not line.startswith(_EXCEPTION_PREFIX):
        return "UNCLASSIFIED"
    remainder = line[len(_EXCEPTION_PREFIX) :]
    colon = remainder.find(b":")
    token_bytes = remainder if colon == -1 else remainder[:colon]
    try:
        token = token_bytes.decode("ascii")
    except UnicodeDecodeError:
        return "UNCLASSIFIED"
    return EXCEPTION_TOKEN_CLASSES.get(token, "UNCLASSIFIED")


def operator_error_class_for(exit_code: int, stderr: bytes) -> str:
    """Return the durable ``child_exited.error_class`` value (§20.8)."""
    if exit_code == 0:
        return "NO_ERROR"
    return classify_operator_stderr(stderr)


# ---------------------------------------------------------------------------
# Fail-closed harness errors
# ---------------------------------------------------------------------------


class HarnessError(Exception):
    """Base class for every fail-closed harness refusal or failure."""

    failure_class: ClassVar[str] = "UNCLASSIFIED"


class ArgumentRefusalError(HarnessError):
    failure_class: ClassVar[str] = "ARGUMENT_REFUSAL"


class PathSeparationRefusalError(HarnessError):
    failure_class: ClassVar[str] = "PATH_SEPARATION_REFUSAL"


class ReparsePointRefusalError(HarnessError):
    failure_class: ClassVar[str] = "REPARSE_POINT_REFUSAL"


class CanonicalMainMismatchError(HarnessError):
    failure_class: ClassVar[str] = "CANONICAL_MAIN_MISMATCH"


class RepositoryShapeError(HarnessError):
    """An unsupported or ambiguous repository shape. Fail closed as UNCLASSIFIED."""

    failure_class: ClassVar[str] = "UNCLASSIFIED"


class HarnessIdentityMismatchError(HarnessError):
    failure_class: ClassVar[str] = "HARNESS_IDENTITY_MISMATCH"


class OperatorIdentityMismatchError(HarnessError):
    failure_class: ClassVar[str] = "OPERATOR_IDENTITY_MISMATCH"


class RuntimeIdentityMismatchError(HarnessError):
    failure_class: ClassVar[str] = "RUNTIME_IDENTITY_MISMATCH"


class InputHashFailureError(HarnessError):
    failure_class: ClassVar[str] = "INPUT_HASH_FAILURE"


class InputIdentityMismatchError(HarnessError):
    failure_class: ClassVar[str] = "INPUT_IDENTITY_MISMATCH"


class ChildLaunchFailureError(HarnessError):
    failure_class: ClassVar[str] = "CHILD_LAUNCH_FAILURE"


class OutputInventoryMismatchError(HarnessError):
    failure_class: ClassVar[str] = "OUTPUT_INVENTORY_MISMATCH"


class OutputHashFailureError(HarnessError):
    failure_class: ClassVar[str] = "OUTPUT_HASH_FAILURE"


class FingerprintMismatchError(HarnessError):
    failure_class: ClassVar[str] = "FINGERPRINT_MISMATCH"


class EvidenceWriteFailureError(HarnessError):
    """A required append failed leaving zero bytes added or changed (§18.2, case A)."""

    failure_class: ClassVar[str] = "EVIDENCE_WRITE_FAILURE"


class EvidenceMalformedPreservedError(HarnessError):
    """A required append left partial or malformed bytes (§18.3, case B)."""

    failure_class: ClassVar[str] = "EVIDENCE_MALFORMED_PRESERVED"


class StructurallyUnsealedError(HarnessError):
    """Case C: bytes stay well formed but a required append is not safely recordable.

    Structural unseal is a condition, never a durable value.  Nothing is written
    to record it (§18.4).
    """

    failure_class: ClassVar[str] = "EVIDENCE_WRITE_FAILURE"


class EpisodePathIdentityDriftError(HarnessError):
    """The episode directory was replaced while the episode was in flight.

    Reparse and containment both pass when a real directory is swapped for
    another real directory inside the evidence root, so the measured path
    identity is what detects it (PA2G-R1, D4).
    """

    failure_class: ClassVar[str] = "EPISODE_PATH_IDENTITY_DRIFT"


class EpisodeStateError(HarnessError):
    """The episode is not in a state that permits the requested command."""

    failure_class: ClassVar[str] = "ARGUMENT_REFUSAL"


#: Path-safety refusals are fatal: nothing further may be written, because the
#: destination is no longer provably the authorized episode directory.
_PATH_SAFETY_ERRORS: Final[tuple[type[HarnessError], ...]] = (
    ReparsePointRefusalError,
    PathSeparationRefusalError,
    EpisodePathIdentityDriftError,
)


# ---------------------------------------------------------------------------
# Deterministic primitives
# ---------------------------------------------------------------------------

#: Windows needs the explicit binary flag; POSIX has no such flag and uses zero.
_O_BINARY: Final[int] = getattr(os, "O_BINARY", 0)
_EXCLUSIVE_FLAGS: Final[int] = os.O_CREAT | os.O_EXCL | os.O_WRONLY | _O_BINARY
_REPARSE_ATTRIBUTE: Final[int] = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)

_HEX_DIGITS: Final = frozenset("0123456789abcdef")
_COMMIT_LENGTH: Final = 40
_EPISODE_ID_MINIMUM: Final = 3
_EPISODE_ID_MAXIMUM: Final = 64
_EPISODE_ID_ALPHABET: Final = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")
_READ_CHUNK: Final = 1 << 20


def utc_timestamp() -> str:
    """Return the exact canonical UTC form ``YYYY-MM-DDTHH:MM:SS.ffffffZ`` (§16)."""
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def require_commit(value: str) -> str:
    """Return a validated forty-character lowercase hexadecimal commit."""
    if len(value) != _COMMIT_LENGTH or any(character not in _HEX_DIGITS for character in value):
        raise ArgumentRefusalError(
            f"canonical commit must be {_COMMIT_LENGTH} lowercase hex characters"
        )
    return value


def require_episode_id(value: str) -> str:
    """Return a validated episode identifier (§14).

    The constraint prevents path traversal into the evidence root and prevents
    protected content from being carried in a directory name.
    """
    if not _EPISODE_ID_MINIMUM <= len(value) <= _EPISODE_ID_MAXIMUM:
        raise ArgumentRefusalError(
            f"episode_id must be {_EPISODE_ID_MINIMUM}..{_EPISODE_ID_MAXIMUM} characters"
        )
    if any(character not in _EPISODE_ID_ALPHABET for character in value):
        raise ArgumentRefusalError("episode_id must be lowercase alphanumeric or hyphen")
    if not value[0].isalnum():
        raise ArgumentRefusalError("episode_id must begin with an alphanumeric character")
    return value


def sha256_of_file(path: Path) -> tuple[str, int]:
    """Return the SHA-256 and byte size of a file, read in bounded chunks."""
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(_READ_CHUNK)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


# ---------------------------------------------------------------------------
# Path safety (§23, PA1-FD-17)
# ---------------------------------------------------------------------------


def is_reparse_point(path: Path) -> bool:
    """Return whether one path component is a symlink, junction or other reparse point."""
    try:
        info = path.lstat()
    except OSError:
        return False
    if stat.S_ISLNK(info.st_mode):
        return True
    attributes: int = getattr(info, "st_file_attributes", 0)
    return bool(attributes & _REPARSE_ATTRIBUTE)


def _components(path: Path) -> Iterator[Path]:
    """Yield the path and every ancestor, anchor first."""
    yield from reversed([path, *path.parents])


def require_no_reparse(path: Path) -> Path:
    """Return the path after refusing any reparse-point redirect along it.

    This is the single authorized divergence from ``resolve_repository_commit``
    (§5.3.1): the harness refuses reparse shapes even where the oracle resolves
    them.
    """
    for component in _components(path):
        if is_reparse_point(component):
            raise ReparsePointRefusalError(f"reparse-point redirect is refused: {component}")
    return path


def resolve_safe_path(value: str | Path) -> Path:
    """Return an absolute resolved path after refusing reparse redirects."""
    candidate = Path(value)
    if not candidate.is_absolute():
        raise PathSeparationRefusalError(f"path must be absolute: {candidate}")
    require_no_reparse(candidate)
    return candidate.resolve()


def is_within(child: Path, parent: Path) -> bool:
    """Return containment decided on resolved components, never on string prefixes."""
    return child == parent or parent in child.parents


def require_disjoint(first: Path, first_name: str, second: Path, second_name: str) -> None:
    """Refuse when either resolved path contains the other."""
    if is_within(first, second) or is_within(second, first):
        raise PathSeparationRefusalError(
            f"{first_name} and {second_name} must be disjoint: {first} / {second}"
        )


def validate_evidence_root(evidence_root: Path, repository_root: Path) -> None:
    """Apply the evidence-root conditions that hold for every command (§23)."""
    if not evidence_root.is_dir():
        raise ArgumentRefusalError(f"external evidence root must exist: {evidence_root}")
    if not os.access(evidence_root, os.W_OK):
        raise ArgumentRefusalError(f"external evidence root must be writable: {evidence_root}")
    require_disjoint(evidence_root, "external evidence root", repository_root, "repository root")


def require_safe_metadata_reference(reference: str) -> Path:
    """Return a validated Git-metadata-relative reference (GREPTILE-G1).

    A symbolic ``HEAD`` reference names a ref *inside* the Git metadata base. It
    is never an absolute filesystem path and never escapes that base, so an
    absolute, drive-rooted, UNC-rooted or parent-traversing reference is refused
    before any candidate path is built or read — including when the file it
    would name happens to contain a syntactically valid commit.

    ``PureWindowsPath`` is used for validation on every host because it is the
    stricter parser: it treats both separators as separators and recognizes
    drive and UNC roots that a POSIX parser would silently accept as an ordinary
    relative name.
    """
    if not reference:
        raise RepositoryShapeError("repository reference is empty")
    pure = PureWindowsPath(reference)
    if pure.is_absolute() or pure.drive or pure.root:
        raise PathSeparationRefusalError(
            f"repository reference must be metadata-relative, not absolute: {reference!r}"
        )
    if any(part == ".." for part in pure.parts):
        raise PathSeparationRefusalError(
            f"repository reference must not traverse outside the metadata base: {reference!r}"
        )
    if not pure.parts:
        raise RepositoryShapeError("repository reference is empty")
    return Path(*pure.parts)


def resolve_metadata_path(base: Path, target: Path) -> Path:
    """Join a Git metadata path without ever following a reparse redirect (GREPTILE-G2).

    ``Path.resolve`` follows symlinks, so calling it first would erase exactly
    the components that must be inspected. This walks the path one real
    component at a time and refuses a symlink, junction or other reparse point
    the moment it appears, before descending through it.

    Lexical ``.`` and ``..`` are honoured rather than rejected, because valid Git
    worktree metadata uses them — a ``commondir`` of ``../..`` is ordinary — but
    they are applied lexically and never by following a redirect.
    """
    if target.is_absolute():
        start = Path(target.parts[0])
        parts = target.parts[1:]
    else:
        start = base
        parts = target.parts
    require_no_reparse(start)
    current = start
    for part in parts:
        if part == ".":
            continue
        if part == "..":
            current = current.parent
            continue
        current = current / part
        if is_reparse_point(current):
            raise ReparsePointRefusalError(f"reparse-point redirect is refused: {current}")
    return current


def measure_episode_path_identity(directory: Path) -> str:
    """Return the measured filesystem identity of the episode directory (PA2G-R1, D1).

    ``(st_dev, st_ino)`` — the volume serial and file index on Windows — names the
    directory *object* rather than the path that currently leads to it, so a
    directory swapped for another real directory at the same path is detectable
    even when reparse and containment both still pass.

    The pair is normalized through the frozen canonical serializer and reduced to
    a digest, so no host device or inode number is ever persisted or reported.
    """
    try:
        info = directory.stat(follow_symlinks=False)
    except OSError as error:
        raise EpisodePathIdentityDriftError(
            f"episode directory identity could not be measured: {directory}"
        ) from error
    return sha256_of_bytes(
        canonical_json_bytes({"st_dev": int(info.st_dev), "st_ino": int(info.st_ino)})
    )


def require_safe_episode_directory(
    directory: Path, evidence_root: Path, expected_identity: str | None = None
) -> str:
    """Run the ordered episode-path gate and return the measured identity.

    The order is fixed and is the single gate every episode operation uses
    (GREPTILE-G3, PA2G-R1 D2):

    1. no reparse redirect on any component of the episode path;
    2. containment inside the validated external evidence root;
    3. equality with the identity pinned when the episode context was opened.

    No durable write may occur before all three pass, and no check may follow a
    sensitive read or write.

    This narrows the exposure window; it does not eliminate it. A swap performed
    between this gate and the immediately following write syscall is not
    prevented by the gate alone, and no stronger race guarantee is claimed here.
    """
    require_no_reparse(directory)
    if not is_within(directory, evidence_root):
        raise PathSeparationRefusalError(
            f"episode directory is not contained by the evidence root: {directory}"
        )
    observed = measure_episode_path_identity(directory)
    if expected_identity is not None and observed != expected_identity:
        raise EpisodePathIdentityDriftError(
            f"episode directory identity changed while the episode was in flight: {directory}"
        )
    return observed


def require_safe_evidence_path(path: Path) -> Path:
    """Refuse a redirected durable evidence path before it is read or written."""
    if is_reparse_point(path):
        raise ReparsePointRefusalError(f"reparse-point redirect is refused: {path}")
    return path


# ---------------------------------------------------------------------------
# Independent repository-identity resolver (§5.3, PA1-FD-4)
# ---------------------------------------------------------------------------


def resolve_canonical_commit(repository_root: Path) -> str:
    """Return the checked-out commit by reading Git ref files, never by invoking Git.

    This is the harness's own resolver.  Importing the formal resolver for
    repository-identity enforcement is prohibited (§27).  Supported shapes are a
    normal ``.git`` directory, a ``.git`` file gitdir pointer, ``commondir``,
    ``packed-refs`` and detached HEAD; anything else fails closed.
    """
    require_no_reparse(repository_root)
    git_entry = repository_root / ".git"
    # The .git metadata surface is inspected before it is read or followed.
    require_no_reparse(git_entry)
    if git_entry.is_file():
        pointer = git_entry.read_text(encoding="utf-8").strip()
        if not pointer.startswith("gitdir:"):
            raise RepositoryShapeError("repository .git file is not a gitdir pointer")
        git_dir = resolve_metadata_path(repository_root, Path(pointer.split(":", 1)[1].strip()))
    elif git_entry.is_dir():
        git_dir = git_entry
    else:
        raise RepositoryShapeError(f"{repository_root} is not a Git repository")
    require_no_reparse(git_dir)

    head_file = git_dir / "HEAD"
    require_no_reparse(head_file)
    if not head_file.is_file():
        raise RepositoryShapeError("repository HEAD is missing")
    head = head_file.read_text(encoding="utf-8").strip()
    if not head.startswith("ref:"):
        return require_commit(head)

    reference = head.split(":", 1)[1].strip()
    relative = require_safe_metadata_reference(reference)
    common_dir = git_dir
    common_file = git_dir / "commondir"
    # The commondir metadata file is inspected before it is read or followed.
    require_safe_evidence_path(common_file)
    if common_file.is_file():
        common = Path(common_file.read_text(encoding="utf-8").strip())
        common_dir = resolve_metadata_path(git_dir, common)
        require_no_reparse(common_dir)
    for base in (git_dir, common_dir):
        candidate = resolve_metadata_path(base, relative)
        if not is_within(candidate, base):
            raise PathSeparationRefusalError(
                f"repository reference escapes the metadata base: {reference!r}"
            )
        if candidate.is_file():
            require_no_reparse(candidate)
            return require_commit(candidate.read_text(encoding="utf-8").strip())
    packed = common_dir / "packed-refs"
    require_safe_evidence_path(packed)
    if packed.is_file():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line.startswith(("#", "^")) or " " not in line:
                continue
            value, name = line.split(" ", 1)
            if name.strip() == reference:
                return require_commit(value.strip())
    raise RepositoryShapeError(f"repository reference {reference!r} could not be resolved")


# ---------------------------------------------------------------------------
# Identity binding (§7, §15.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactIdentity:
    """The SHA-256 and byte size of one exact file."""

    sha256: str
    byte_size: int


def resolve_operator_identity(repository_root: Path) -> ArtifactIdentity:
    """Return the frozen operator identity, read-only. The operator is never imported."""
    operator = repository_root / Path(OPERATOR_RELATIVE_PATH)
    if not operator.is_file():
        raise OperatorIdentityMismatchError(f"operator script is missing: {operator}")
    require_no_reparse(operator)
    digest, size = sha256_of_file(operator)
    return ArtifactIdentity(digest, size)


def resolve_harness_identity(repository_root: Path) -> ArtifactIdentity:
    """Return this harness's own identity, bound to the bytes actually executing.

    The resolved target must equal the running script's resolved ``__file__``,
    so a harness can never attest to bytes other than the ones running (§15.1).
    """
    harness = repository_root / Path(HARNESS_RELATIVE_PATH)
    if not harness.is_file():
        raise HarnessIdentityMismatchError(f"harness script is missing: {harness}")
    require_no_reparse(harness)
    running = Path(__file__).resolve()
    if harness.resolve() != running:
        raise HarnessIdentityMismatchError(
            f"harness path {harness.resolve()} is not the running script {running}"
        )
    digest, size = sha256_of_file(harness)
    return ArtifactIdentity(digest, size)


@dataclass(frozen=True)
class RuntimeIdentity:
    """Exactly the five runtime fields of §7. There is no sixth field."""

    resolved_python_executable_path: str
    python_executable_sha256: str
    python_executable_byte_size: int
    python_version: str
    python_implementation: str

    def as_fields(self) -> dict[str, object]:
        return {
            "resolved_python_executable_path": self.resolved_python_executable_path,
            "python_executable_sha256": self.python_executable_sha256,
            "python_executable_byte_size": self.python_executable_byte_size,
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
        }


def resolve_runtime_identity() -> RuntimeIdentity:
    """Bind the exact configured interpreter artifact (PA1-FD-10, R3)."""
    executable = Path(sys.executable).resolve()
    if not executable.is_file():
        raise RuntimeIdentityMismatchError(f"python executable is missing: {executable}")
    digest, size = sha256_of_file(executable)
    return RuntimeIdentity(
        resolved_python_executable_path=str(executable),
        python_executable_sha256=digest,
        python_executable_byte_size=size,
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
    )


# ---------------------------------------------------------------------------
# Evidence storage boundary
# ---------------------------------------------------------------------------


class EvidenceStore:
    """The filesystem boundary for every canonical evidence byte.

    Every durable write in the harness passes through this class.  Qualification
    subclasses it to inject controlled write failures; production constructs it
    unchanged.  No command-line flag selects a different store, so the
    production boundary cannot be weakened from outside.
    """

    def create_exclusive(self, path: Path, payload: bytes) -> None:
        """Create a write-once record. A second attempt fails rather than replaces."""
        descriptor = os.open(path, _EXCLUSIVE_FLAGS)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

    def append(self, path: Path, payload: bytes) -> None:
        """Append exact bytes to an append-only record."""
        with path.open("ab") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())


def _byte_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def append_canonical_event(store: EvidenceStore, path: Path, record: Mapping[str, object]) -> None:
    """Append one canonical event, classifying a failure as case A or case B (§18.1).

    A failure that added or changed no byte leaves the journal well formed and
    raises ``EvidenceWriteFailureError``.  A failure that left partial bytes
    preserves them exactly and raises ``EvidenceMalformedPreservedError``: the
    bytes are never truncated, repaired or patched.
    """
    payload = canonical_json_bytes(record)
    # A durable evidence path that has become a redirect is never appended to.
    require_safe_evidence_path(path)
    before = _byte_size(path)
    try:
        store.append(path, payload)
    except OSError as error:
        if _byte_size(path) == before:
            raise EvidenceWriteFailureError(
                f"append failed with no byte changed: {path}"
            ) from error
        raise EvidenceMalformedPreservedError(f"append left partial bytes: {path}") from error
    if _byte_size(path) != before + len(payload):
        raise EvidenceMalformedPreservedError(f"append left partial bytes: {path}")


# ---------------------------------------------------------------------------
# Episode core (§15.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EpisodeCore:
    """The write-once identity anchor of one execution episode."""

    fields: Mapping[str, object]
    identity: str

    @property
    def expected_canonical_commit(self) -> str:
        return str(self.fields["expected_canonical_commit"])

    @property
    def repository_root(self) -> Path:
        return Path(str(self.fields["repository_root"]))

    @property
    def external_evidence_root(self) -> Path:
        return Path(str(self.fields["external_evidence_root"]))


#: The exact and closed ``episode-core.json`` field set (§15.1).
EPISODE_CORE_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "episode_id",
    "expected_canonical_commit",
    "repository_root",
    "external_evidence_root",
    "operator_relative_path",
    "operator_sha256",
    "operator_byte_size",
    "harness_sha256",
    "harness_byte_size",
    "resolved_python_executable_path",
    "python_executable_sha256",
    "python_executable_byte_size",
    "python_version",
    "python_implementation",
)


def build_episode_core(
    *,
    episode_id: str,
    expected_canonical_commit: str,
    repository_root: Path,
    external_evidence_root: Path,
    operator: ArtifactIdentity,
    harness: ArtifactIdentity,
    runtime: RuntimeIdentity,
) -> dict[str, object]:
    """Return the exact episode-core field set. No repository-observation field exists."""
    core: dict[str, object] = {
        "schema_version": EPISODE_CORE_SCHEMA_VERSION,
        "episode_id": episode_id,
        "expected_canonical_commit": expected_canonical_commit,
        "repository_root": str(repository_root),
        "external_evidence_root": str(external_evidence_root),
        "operator_relative_path": OPERATOR_RELATIVE_PATH,
        "operator_sha256": operator.sha256,
        "operator_byte_size": operator.byte_size,
        "harness_sha256": harness.sha256,
        "harness_byte_size": harness.byte_size,
    }
    core.update(runtime.as_fields())
    return core


def load_episode_core(episode_directory: Path) -> EpisodeCore:
    """Read and validate ``episode-core.json``, returning it with its identity."""
    path = require_safe_evidence_path(episode_directory / EPISODE_CORE_FILENAME)
    if not path.is_file():
        raise EpisodeStateError(f"episode core is missing: {path}")
    payload = path.read_bytes()
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EpisodeStateError(f"episode core is not valid JSON: {path}") from error
    if not isinstance(decoded, dict):
        raise EpisodeStateError(f"episode core must be a JSON object: {path}")
    if canonical_json_bytes(decoded) != payload:
        raise EpisodeStateError(f"episode core bytes are not canonical: {path}")
    if tuple(sorted(decoded)) != tuple(sorted(EPISODE_CORE_FIELDS)):
        raise EpisodeStateError(f"episode core field set is not exact: {path}")
    if decoded["schema_version"] != EPISODE_CORE_SCHEMA_VERSION:
        raise EpisodeStateError(f"episode core schema_version is wrong: {path}")
    return EpisodeCore(fields=decoded, identity=sha256_of_bytes(payload))


# ---------------------------------------------------------------------------
# Journals (§15.2, §21.2)
# ---------------------------------------------------------------------------


@dataclass
class StageJournal:
    """One append-only stage record with a one-based per-file event ordinal."""

    store: EvidenceStore
    path: Path
    stage: str
    episode_identity: str
    #: Ordered episode-path gate, run before every durable append (PA2G-R1 D2/D5).
    guard: Callable[[], object] | None = None
    ordinal: int = 0
    child_started: bool = False
    sealed: bool = False

    def append(self, event: str, fields: Mapping[str, object] | None = None) -> None:
        """Append one complete canonical event, advancing the ordinal only on success.

        The ordered episode-path gate runs first, so no stage event is written
        to a directory that is no longer provably the authorized one.
        """
        if self.guard is not None:
            self.guard()
        record: dict[str, object] = {
            "schema_version": STAGE_EVENT_SCHEMA_VERSION,
            "episode_identity": self.episode_identity,
            "stage": self.stage,
            "event": event,
            "event_ordinal": self.ordinal + 1,
        }
        if fields:
            record.update(fields)
        append_canonical_event(self.store, self.path, record)
        self.ordinal += 1

    def observe_repository(self, expected: str, observed: str, mode: str) -> None:
        self.append(
            "repository_identity_observed",
            {
                "expected_canonical_commit": expected,
                "observed_canonical_commit": observed,
                "identity_match": expected == observed,
                "mode": mode,
            },
        )

    def seal(self, disposition: str) -> None:
        """Emit ``stage_sealed`` between two runs of the ordered gate (PA2G-R1 D3).

        The gate runs before the seal is written and again immediately after,
        so a swap in the residual window is still refused rather than yielding
        a clean sealed stage.
        """
        self.append("stage_sealed", {"stage_disposition": disposition})
        if self.guard is not None:
            self.guard()
        self.sealed = True


@dataclass
class JournalScan:
    """The observable condition of one journal's exact existing bytes."""

    filename: str
    sha256: str
    byte_size: int
    record_integrity: str
    event_count: int | None
    events: tuple[Mapping[str, object], ...]

    @property
    def opened(self) -> bool:
        return any(event.get("event") == "stage_opened" for event in self.events)

    @property
    def sealed_disposition(self) -> str | None:
        """Return the disposition only where the journal ends in one valid seal."""
        seals = [event for event in self.events if event.get("event") == "stage_sealed"]
        if len(seals) != 1 or not self.events or self.events[-1].get("event") != "stage_sealed":
            return None
        disposition = seals[0].get("stage_disposition")
        if isinstance(disposition, str) and disposition in STAGE_DISPOSITIONS:
            return disposition
        return None

    @property
    def structurally_unsealed(self) -> bool:
        """``stage_opened`` exists and the journal does not end in one valid seal (§18.4)."""
        return self.opened and self.sealed_disposition is None

    def latest(self, event: str) -> Mapping[str, object] | None:
        for candidate in reversed(self.events):
            if candidate.get("event") == event:
                return candidate
        return None


def scan_journal(path: Path) -> JournalScan:
    """Classify one journal's exact bytes. Syntax only — never lifecycle completeness."""
    require_safe_evidence_path(path)
    payload = path.read_bytes()
    digest = sha256_of_bytes(payload)
    events: list[Mapping[str, object]] = []
    integrity = "WELL_FORMED"
    if payload and not payload.endswith(b"\n"):
        integrity = "MALFORMED_PRESERVED"
    for line in payload.split(b"\n"):
        if not line:
            continue
        try:
            decoded = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            integrity = "MALFORMED_PRESERVED"
            break
        if not isinstance(decoded, dict) or canonical_json_bytes(decoded) != line + b"\n":
            integrity = "MALFORMED_PRESERVED"
            break
        events.append(decoded)
    if integrity == "MALFORMED_PRESERVED":
        return JournalScan(path.name, digest, len(payload), integrity, None, ())
    return JournalScan(path.name, digest, len(payload), integrity, len(events), tuple(events))


# ---------------------------------------------------------------------------
# Child process boundary (§6, PA1-FD-5)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChildOutcome:
    """The exact runtime facts of one child process. Raw streams never persist."""

    pid: int
    started_at: str
    exited_at: str
    exit_code: int
    elapsed_ms: int
    stdout: bytes
    stderr: bytes


class ChildRunner:
    """Launches the canonical operator as exactly one separate child process.

    Qualification substitutes a synthetic runner through this boundary so the
    real frozen operator is never executed during P-A2 qualification; the
    production command path is unchanged and reaches the real operator.
    """

    def run(self, command: Sequence[str]) -> ChildOutcome:
        try:
            process = subprocess.Popen(
                list(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
        except OSError as error:
            raise ChildLaunchFailureError(f"child process creation failed: {error}") from error
        started_at = utc_timestamp()
        started_monotonic = time.monotonic()
        stdout, stderr = process.communicate()
        elapsed_ms = int((time.monotonic() - started_monotonic) * 1000)
        return ChildOutcome(
            pid=process.pid,
            started_at=started_at,
            exited_at=utc_timestamp(),
            exit_code=process.returncode,
            elapsed_ms=elapsed_ms,
            stdout=stdout,
            stderr=stderr,
        )


def build_generate_command(
    *,
    python_executable: str,
    operator_path: Path,
    expected_canonical_commit: str,
    repository_root: Path,
    generation: str,
    workspace: Path,
    external_evidence_root: Path,
    future_evidence_root: Path,
    inputs: Mapping[str, Path],
    python_version: str,
) -> tuple[str, ...]:
    """Return the exact canonical operator ``generate`` command line."""
    command = [
        python_executable,
        str(operator_path),
        "generate",
        "--expected-canonical-commit",
        expected_canonical_commit,
        "--repository-root",
        str(repository_root),
        "--generation",
        generation,
        "--workspace",
        str(workspace),
        "--external-evidence-root",
        str(external_evidence_root),
        "--future-evidence-root",
        str(future_evidence_root),
    ]
    for surface in INPUT_SURFACES:
        command.extend([SURFACE_ARGUMENTS[surface], str(inputs[surface])])
    command.extend(["--python-version", python_version])
    return tuple(command)


def build_compare_command(
    *,
    python_executable: str,
    operator_path: Path,
    generation_a_workspace: Path,
    generation_b_workspace: Path,
) -> tuple[str, ...]:
    """Return the exact canonical operator ``compare`` command line."""
    return (
        python_executable,
        str(operator_path),
        "compare",
        "--generation-a-workspace",
        str(generation_a_workspace),
        "--generation-b-workspace",
        str(generation_b_workspace),
    )


# ---------------------------------------------------------------------------
# Workspace observation (§10, §10.1, §11, §25)
# ---------------------------------------------------------------------------


def hash_candidate_bundle(workspace: Path) -> tuple[dict[str, object], ...]:
    """Return the seven-file output ledger, read-only, after the child has exited.

    The inventory must be exactly the seven canonical candidate artifacts.  A
    workspace that is absent, differently populated or unreadable yields no
    partial ledger: it raises, and the caller omits the event entirely.
    """
    if not workspace.is_dir():
        raise OutputInventoryMismatchError(f"generation workspace is absent: {workspace}")
    present = sorted(entry.name for entry in workspace.iterdir())
    if present != sorted(CANDIDATE_FILENAMES):
        raise OutputInventoryMismatchError(
            f"workspace inventory is not the seven candidate artifacts: {workspace}"
        )
    outputs: list[dict[str, object]] = []
    for filename in CANDIDATE_FILENAMES:
        try:
            digest, size = sha256_of_file(workspace / filename)
        except OSError as error:
            raise OutputHashFailureError(f"candidate artifact is unreadable: {filename}") from error
        outputs.append({"filename": filename, "sha256": digest, "byte_size": size})
    return tuple(outputs)


def read_split_fingerprint(workspace: Path) -> str:
    """Read the authoritative fingerprint from the generation manifest, read-only.

    Deriving it from persisted stdout is prohibited: child output is never
    persisted, so it is never an evidence source (§10.1).
    """
    manifest = workspace / GENERATION_MANIFEST_FILENAME
    try:
        decoded = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FingerprintMismatchError(f"generation manifest is unreadable: {manifest}") from error
    if not isinstance(decoded, dict) or SPLIT_FINGERPRINT_KEY not in decoded:
        raise FingerprintMismatchError(f"generation manifest carries no fingerprint: {manifest}")
    fingerprint = decoded[SPLIT_FINGERPRINT_KEY]
    if not isinstance(fingerprint, str) or not fingerprint:
        raise FingerprintMismatchError(f"generation manifest fingerprint is invalid: {manifest}")
    return fingerprint


def agreed_split_fingerprint(first: Path, second: Path) -> str:
    """Return the one observed fingerprint only where both manifests agree (§10.1)."""
    left = read_split_fingerprint(first)
    right = read_split_fingerprint(second)
    if left != right:
        raise FingerprintMismatchError("generation manifests disagree on split_fingerprint")
    return left


def derive_byte_equality(
    left: Sequence[Mapping[str, object]], right: Sequence[Mapping[str, object]]
) -> tuple[str, tuple[str, ...]]:
    """Return the harness-derived equality ledger over the seven candidate files (§11)."""
    left_by_name = {str(entry["filename"]): entry for entry in left}
    right_by_name = {str(entry["filename"]): entry for entry in right}
    unequal = tuple(
        filename
        for filename in CANDIDATE_FILENAMES
        if left_by_name[filename]["sha256"] != right_by_name[filename]["sha256"]
    )
    return ("UNEQUAL" if unequal else "EQUAL"), unequal


def comparison_disposition_for(byte_equality: str, operator_exit_code: int) -> str:
    """Return the §11 disposition. The table is total over EQUAL/UNEQUAL x zero/nonzero."""
    if byte_equality == "EQUAL":
        return "EQUAL_VERIFIED" if operator_exit_code == 0 else "INTEGRITY_FAILURE"
    return "CONTRADICTION" if operator_exit_code == 0 else "BYTE_INEQUALITY"


#: The failure_class implied by a non-successful comparison disposition.
COMPARISON_FAILURE_CLASSES: Final[Mapping[str, str]] = {
    # A child that failed while the harness derived equality keeps child provenance.
    "INTEGRITY_FAILURE": "CHILD_NONZERO_EXIT",
    "BYTE_INEQUALITY": "BYTE_INEQUALITY",
    "CONTRADICTION": "COMPARE_CONTRADICTION",
}


# ---------------------------------------------------------------------------
# Episode context and the PRE-STAGE gates (§21.1)
# ---------------------------------------------------------------------------


@dataclass
class EpisodeContext:
    """One opened episode's validated location, core and identities."""

    episode_id: str
    repository_root: Path
    evidence_root: Path
    directory: Path
    core: EpisodeCore
    store: EvidenceStore
    #: Measured at context open and re-confirmed before every durable write.
    episode_path_identity: str

    def journal_path(self, stage: str) -> Path:
        return self.directory / STAGE_JOURNALS[stage]

    @property
    def manifest_path(self) -> Path:
        return self.directory / EPISODE_MANIFEST_FILENAME

    @property
    def invalidation_path(self) -> Path:
        return self.directory / EPISODE_INVALIDATION_FILENAME

    def require_safe_directory(self) -> str:
        """Re-run the ordered episode-path gate before an evidence read or write."""
        return require_safe_episode_directory(
            self.directory, self.evidence_root, self.episode_path_identity
        )

    @contextlib.contextmanager
    def pinned(self) -> Iterator[None]:
        """Hold the episode directory open for the duration of a write-bearing span.

        An open handle on a file inside the directory makes the directory
        undeletable and unrenamable on Windows, so the swap the gate would
        otherwise only detect cannot be performed at all while the span runs.
        Where the platform does not offer that guarantee the span is unaffected
        and the ordered gate remains the protection.
        """
        try:
            handle = (self.directory / EPISODE_CORE_FILENAME).open("rb")
        except OSError:
            yield
            return
        try:
            yield
        finally:
            handle.close()

    def scans(self) -> dict[str, JournalScan]:
        self.require_safe_directory()
        found: dict[str, JournalScan] = {}
        for filename in BOUND_RECORD_FILENAMES:
            path = self.directory / filename
            if path.is_file():
                found[filename] = scan_journal(path)
        return found


def open_episode_context(
    *,
    episode_id: str,
    repository_root: Path,
    evidence_root: Path,
    store: EvidenceStore,
) -> EpisodeContext:
    """Run the PRE-STAGE gates in their exact fixed order (§21.1).

    A failure here is a harness or process refusal: it creates no stage journal,
    fabricates no stage and implies no automatic invalidation.
    """
    # 1. arguments; 2. evidence location; 3. path separation and reparse safety
    require_episode_id(episode_id)
    validate_evidence_root(evidence_root, repository_root)
    # 4. the episode exists and episode-core agrees with the supplied location.
    # The episode directory itself is validated before episode-core is read: a
    # validated evidence root does not imply a non-redirected episode directory.
    directory = evidence_root / episode_id
    episode_path_identity = require_safe_episode_directory(directory, evidence_root)
    if not directory.is_dir():
        raise EpisodeStateError(f"episode does not exist: {directory}")
    core = load_episode_core(directory)
    if core.fields["episode_id"] != episode_id:
        raise EpisodeStateError("episode-core episode_id disagrees with the supplied identifier")
    if core.repository_root != repository_root:
        raise EpisodeStateError("episode-core repository_root disagrees with the supplied root")
    if core.external_evidence_root != evidence_root:
        raise EpisodeStateError("episode-core external_evidence_root disagrees with the location")
    return EpisodeContext(
        episode_id=episode_id,
        repository_root=repository_root,
        evidence_root=evidence_root,
        directory=directory,
        core=core,
        store=store,
        episode_path_identity=episode_path_identity,
    )


def require_scientific_continuation(context: EpisodeContext) -> None:
    """Refuse every scientific continuation the contract prohibits (§17.2, §18.5, §18.8).

    Every barrier here is **derived** from the exact existing evidence bytes.
    Nothing is written to record one, no record is repaired or backfilled, and no
    field, enumeration value or evidence class represents a barrier.

    The gate runs during PRE-STAGE, before any protected input is hashed, before
    any workspace is inspected, before any child is launched and before the
    stage journal for the attempted continuation is created.
    """
    if context.manifest_path.exists():
        raise EpisodeStateError("the episode is sealed or terminalization failed; no continuation")
    scans = context.scans()
    invalidation = scans.pop(EPISODE_INVALIDATION_FILENAME, None)
    if invalidation is not None:
        # A durable invalidation ends the episode's scientific life. Invalidation
        # bytes that cannot be safely interpreted refuse identically, and are
        # never repaired (§17.1, §17.2, §22).
        if invalidation.record_integrity != "WELL_FORMED" or not invalidation.event_count:
            raise EpisodeStateError(
                "invalidation evidence cannot be safely interpreted; no continuation"
            )
        raise EpisodeStateError("the episode carries a durable invalidation; no continuation")
    # Only stage journals remain: the invalidation record refused above or is absent.
    for filename, scan in scans.items():
        if scan.record_integrity == "MALFORMED_PRESERVED" or scan.structurally_unsealed:
            raise EpisodeStateError(f"evidence is structurally incomplete: {filename}")
        # A journal whose required first stage_opened event never durably landed
        # cannot represent a valid completed scientific predecessor. Its exact
        # bytes are preserved and it bars every later continuation (§13, §18.5).
        if not scan.opened:
            raise EpisodeStateError(f"stage evidence never durably opened: {filename}")
        if scan.sealed_disposition in ("STAGE_REFUSED", "STAGE_FAILED"):
            raise EpisodeStateError(f"a stage already sealed {scan.sealed_disposition}: {filename}")


# ---------------------------------------------------------------------------
# Stage execution (§21.2)
# ---------------------------------------------------------------------------


@dataclass
class StageOutcome:
    """What a stage actually produced. Absent values are absent, never null."""

    stage: str
    disposition: str | None
    failure_class: str | None = None
    structurally_unsealed: bool = False


def seal_after_failure(journal: StageJournal, failure_class: str, error_class: str | None) -> str:
    """Record ``stage_failed`` then ``stage_sealed`` where it is safely recordable."""
    observed, root_cause, remediation = derive_failure_triad(failure_class, error_class)
    journal.append(
        "stage_failed",
        {
            "failure_class": observed,
            "root_cause_class": root_cause,
            "remediation_disposition": remediation,
        },
    )
    refused = not journal.child_started and failure_class in REFUSAL_FAILURE_CLASSES
    disposition = "STAGE_REFUSED" if refused else "STAGE_FAILED"
    journal.seal(disposition)
    return disposition


def run_stage(
    context: EpisodeContext,
    *,
    stage: str,
    argv: Sequence[str],
    generation_identity: str | None,
    body: StageBody,
    runner: ChildRunner,
) -> StageOutcome:
    """Open a stage journal and drive the fixed OPENED STAGE lifecycle.

    Every failure after ``stage_opened`` that remains safely recordable becomes
    ``stage_failed`` then ``stage_sealed``.  Where a required append is no
    longer safely recordable, nothing is fabricated and the stage is left
    structurally unsealed (§18.4, PIC-CORR-7).
    """
    path = context.journal_path(stage)
    journal = StageJournal(
        store=context.store,
        path=path,
        stage=stage,
        episode_identity=context.core.identity,
        guard=context.require_safe_directory,
    )
    # 5. exclusively create the stage journal, in a re-validated episode directory
    context.require_safe_directory()
    try:
        context.store.create_exclusive(path, b"")
    except FileExistsError as error:
        raise EpisodeStateError(f"stage journal already exists: {path}") from error
    except OSError as error:
        raise EvidenceWriteFailureError(f"stage journal could not be created: {path}") from error

    opened: dict[str, object] = {"argv": list(argv)}
    if generation_identity is not None:
        opened["generation_identity"] = generation_identity
    try:
        # 6. stage_opened is the first stage event
        journal.append("stage_opened", opened)
    except (EvidenceWriteFailureError, EvidenceMalformedPreservedError):
        # No stage_opened means no opened stage; nothing is fabricated.
        raise

    try:
        body(context, journal, runner)
    except _PATH_SAFETY_ERRORS:
        # The episode path is no longer provably the authorized directory, so no
        # further byte may be written anywhere — not stage_failed, not
        # stage_sealed. The refusal is fatal and terminal (PA2G-R1 D3).
        raise
    except EvidenceMalformedPreservedError:
        # Case B (§18.3): the exact malformed bytes are preserved and no later event —
        # not stage_failed, not stage_sealed — may be fabricated after them.
        return StageOutcome(stage, None, "EVIDENCE_MALFORMED_PRESERVED")
    except HarnessError as error:
        observed = getattr(error, "operator_error_class", None)
        error_class = observed if isinstance(observed, str) else None
        try:
            disposition = seal_after_failure(journal, type(error).failure_class, error_class)
        except _PATH_SAFETY_ERRORS:
            raise
        except EvidenceWriteFailureError:
            return StageOutcome(stage, None, type(error).failure_class, structurally_unsealed=True)
        except EvidenceMalformedPreservedError:
            return StageOutcome(stage, None, type(error).failure_class)
        return StageOutcome(stage, disposition, type(error).failure_class)

    try:
        journal.seal("STAGE_COMPLETE")
    except _PATH_SAFETY_ERRORS:
        raise
    except EvidenceWriteFailureError:
        return StageOutcome(stage, None, "EVIDENCE_WRITE_FAILURE", structurally_unsealed=True)
    except EvidenceMalformedPreservedError:
        return StageOutcome(stage, None, "EVIDENCE_MALFORMED_PRESERVED")
    return StageOutcome(stage, "STAGE_COMPLETE")


class ChildNonzeroExitError(HarnessError):
    """The operator child exited nonzero. The recorded error class carries the cause."""

    failure_class: ClassVar[str] = "CHILD_NONZERO_EXIT"

    def __init__(self, message: str, operator_error_class: str) -> None:
        super().__init__(message)
        self.operator_error_class = operator_error_class


class VerifyFailureError(HarnessError):
    """The verification rerun disagreed with the recorded comparison disposition."""

    failure_class: ClassVar[str] = "VERIFY_FAILURE"


def _verify_bound_identities(context: EpisodeContext) -> None:
    """Step 8: harness, operator and runtime identities must still match the core."""
    harness = resolve_harness_identity(context.repository_root)
    if harness.sha256 != context.core.fields["harness_sha256"]:
        raise HarnessIdentityMismatchError("harness identity differs from the episode core")
    operator = resolve_operator_identity(context.repository_root)
    if operator.sha256 != context.core.fields["operator_sha256"]:
        raise OperatorIdentityMismatchError("operator identity differs from the episode core")
    runtime = resolve_runtime_identity()
    for name, value in runtime.as_fields().items():
        if context.core.fields[name] != value:
            raise RuntimeIdentityMismatchError(f"runtime identity differs from the core: {name}")


def _observe_continuation(context: EpisodeContext, journal: StageJournal) -> None:
    """Observe canonical identity and refuse scientific continuation on a mismatch."""
    expected = context.core.expected_canonical_commit
    observed = resolve_canonical_commit(context.repository_root)
    journal.observe_repository(expected, observed, "CONTINUATION")
    if observed != expected:
        raise CanonicalMainMismatchError("canonical main moved; scientific continuation refused")


def _record_child(journal: StageJournal, outcome: ChildOutcome) -> str:
    """Record the child's outcome first and unconditionally (§21.2.1)."""
    journal.append("child_started", {"pid": outcome.pid, "started_at": outcome.started_at})
    journal.child_started = True
    stdout_digest = sha256_of_bytes(outcome.stdout)
    stderr_digest = sha256_of_bytes(outcome.stderr)
    error_class = operator_error_class_for(outcome.exit_code, outcome.stderr)
    journal.append(
        "child_exited",
        {
            "exited_at": outcome.exited_at,
            "exit_code": outcome.exit_code,
            "elapsed_ms": outcome.elapsed_ms,
            "stdout_sha256": stdout_digest,
            "stdout_byte_size": len(outcome.stdout),
            "stderr_sha256": stderr_digest,
            "stderr_byte_size": len(outcome.stderr),
            "error_class": error_class,
        },
    )
    return error_class


# ---------------------------------------------------------------------------
# Stage bodies
# ---------------------------------------------------------------------------


class StageBody:
    """The stage-specific work between ``stage_opened`` and ``stage_sealed``."""

    def __call__(
        self, context: EpisodeContext, journal: StageJournal, runner: ChildRunner
    ) -> None:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass
class GenerateBody(StageBody):
    """Generation A or B: identity gates, input digests, one child, output digests."""

    generation: str
    workspace: Path
    future_evidence_root: Path
    inputs: Mapping[str, Path]
    command: Sequence[str]

    def __call__(self, context: EpisodeContext, journal: StageJournal, runner: ChildRunner) -> None:
        # 7. observe canonical repository identity
        _observe_continuation(context, journal)
        # 8. verify harness, operator and runtime identities
        _verify_bound_identities(context)
        # 9. hash permitted inputs — digests and sizes only, never bytes
        entries = hash_input_surfaces(self.inputs)
        require_input_agreement(context, entries)
        journal.append("inputs_hashed", {"inputs": [dict(entry) for entry in entries]})
        # the immediate pre-child observation is durable because the journal exists
        _observe_continuation(context, journal)
        # 10. launch exactly one child process
        outcome = runner.run(self.command)
        # 11. append child completion
        error_class = _record_child(journal, outcome)
        if outcome.exit_code != 0:
            raise ChildNonzeroExitError("operator generate exited nonzero", error_class)
        # 12. derive output evidence read-only, after the child has exited
        outputs = hash_candidate_bundle(self.workspace)
        journal.append("outputs_hashed", {"outputs": [dict(entry) for entry in outputs]})
        journal.append(
            "split_fingerprint_observed",
            {"split_fingerprint": read_split_fingerprint(self.workspace)},
        )


@dataclass
class CompareBody(StageBody):
    """Comparison or verification: one child, then the independent equality ledger."""

    generation_a_workspace: Path
    generation_b_workspace: Path
    command: Sequence[str]
    observe_before_child: bool
    expected_disposition: str | None = None

    def __call__(self, context: EpisodeContext, journal: StageJournal, runner: ChildRunner) -> None:
        _observe_continuation(context, journal)
        _verify_bound_identities(context)
        if self.observe_before_child:
            _observe_continuation(context, journal)
        outcome = runner.run(self.command)
        error_class = _record_child(journal, outcome)
        # A fully derivable ledger is recorded even where the child failed (§21.2.1).
        left = hash_candidate_bundle(self.generation_a_workspace)
        right = hash_candidate_bundle(self.generation_b_workspace)
        fingerprint = agreed_split_fingerprint(
            self.generation_a_workspace, self.generation_b_workspace
        )
        journal.append("split_fingerprint_observed", {"split_fingerprint": fingerprint})
        byte_equality, unequal = derive_byte_equality(left, right)
        disposition = comparison_disposition_for(byte_equality, outcome.exit_code)
        journal.append(
            "comparison_derived",
            {
                "byte_equality": byte_equality,
                "unequal_filenames": list(unequal),
                "operator_exit_code": outcome.exit_code,
                "comparison_disposition": disposition,
            },
        )
        # A rerun that contradicts the sealed comparison is a verification failure first:
        # verify only runs after compare sealed EQUAL_VERIFIED (§4, §17.2).
        if self.expected_disposition is not None and disposition != self.expected_disposition:
            raise VerifyFailureError("verification disagrees with the recorded comparison")
        if disposition != "EQUAL_VERIFIED":
            failure_class = COMPARISON_FAILURE_CLASSES[disposition]
            if failure_class == "CHILD_NONZERO_EXIT":
                raise ChildNonzeroExitError("operator compare exited nonzero", error_class)
            raise _COMPARISON_ERRORS[failure_class]("comparison did not verify equality")


class ByteInequalityError(HarnessError):
    failure_class: ClassVar[str] = "BYTE_INEQUALITY"


class CompareContradictionError(HarnessError):
    failure_class: ClassVar[str] = "COMPARE_CONTRADICTION"


_COMPARISON_ERRORS: Final[Mapping[str, type[HarnessError]]] = {
    "BYTE_INEQUALITY": ByteInequalityError,
    "COMPARE_CONTRADICTION": CompareContradictionError,
}


def hash_input_surfaces(inputs: Mapping[str, Path]) -> tuple[Mapping[str, object], ...]:
    """Return one identity entry per logical input surface. Input bytes never persist."""
    entries: list[Mapping[str, object]] = []
    for surface in INPUT_SURFACES:
        try:
            digest, size = sha256_of_file(inputs[surface])
        except OSError as error:
            raise InputHashFailureError(f"formal input is unreadable: {surface}") from error
        entries.append(
            {
                "surface": surface,
                "sha256": digest,
                "byte_size": size,
                "path_role": SURFACE_PATH_ROLES[surface],
            }
        )
    return tuple(entries)


def require_input_agreement(
    context: EpisodeContext, entries: Sequence[Mapping[str, object]]
) -> None:
    """Refuse when a later stage presents different bytes for the same input surface."""
    for filename in (STAGE_GENERATE_A_FILENAME, STAGE_GENERATE_B_FILENAME):
        path = context.directory / filename
        if not path.is_file():
            continue
        recorded = scan_journal(path).latest("inputs_hashed")
        if recorded is None:
            continue
        previous = recorded.get("inputs")
        if not isinstance(previous, list):
            continue
        by_surface = {
            str(entry.get("surface")): entry for entry in previous if isinstance(entry, dict)
        }
        for entry in entries:
            earlier = by_surface.get(str(entry["surface"]))
            if earlier is not None and earlier.get("sha256") != entry["sha256"]:
                raise InputIdentityMismatchError(
                    f"input identity differs from the recorded episode identity: {entry['surface']}"
                )


# ---------------------------------------------------------------------------
# Terminal manifest (§15.4, §18.8, §20.7, §22)
# ---------------------------------------------------------------------------

#: The exact and closed ``episode-manifest.json`` field set (§15.4).
EPISODE_MANIFEST_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "episode_identity",
    "episode_core",
    "records",
    "terminal_disposition",
    "manifest_sealed_at",
)

TM_ABSENT: Final = "TM-0"
TM_INVALID: Final = "TM-1"
TM_VALID: Final = "TM-2"


def classify_terminal_manifest(episode_directory: Path) -> str:
    """Return the physical creation state TM-0, TM-1 or TM-2 (§18.8).

    The states are structural, mutually exclusive, exhaustive and observable.
    Nothing is written to record which one holds, and there is no fourth state.
    """
    path = episode_directory / EPISODE_MANIFEST_FILENAME
    if not path.exists():
        return TM_ABSENT
    return TM_VALID if _is_valid_terminal_manifest(episode_directory, path) else TM_INVALID


def _is_valid_terminal_manifest(episode_directory: Path, path: Path) -> bool:
    """Validate exact bytes against the complete canonical manifest contract."""
    try:
        payload = path.read_bytes()
    except OSError:
        return False
    if not payload:
        return False
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    if not isinstance(decoded, dict):
        return False
    if canonical_json_bytes(decoded) != payload:
        return False
    if tuple(sorted(decoded)) != tuple(sorted(EPISODE_MANIFEST_FIELDS)):
        return False
    if decoded["schema_version"] != EPISODE_MANIFEST_SCHEMA_VERSION:
        return False
    if decoded["terminal_disposition"] not in TERMINAL_DISPOSITIONS:
        return False
    core = decoded["episode_core"]
    if not _is_valid_binding(core, countable=False):
        return False
    records = decoded["records"]
    if not isinstance(records, list):
        return False
    bound: list[str] = []
    for entry in records:
        if not _is_valid_binding(entry, countable=True):
            return False
        bound.append(str(entry["filename"]))
    if sorted(bound) != sorted(set(bound)):
        return False
    present = sorted(
        name for name in BOUND_RECORD_FILENAMES if (episode_directory / name).is_file()
    )
    if sorted(bound) != present:
        return False
    return _bindings_match_bytes(episode_directory, [core, *records])


def _is_valid_binding(entry: object, *, countable: bool) -> bool:
    if not isinstance(entry, dict):
        return False
    required = {"filename", "sha256", "byte_size", "record_integrity"}
    permitted = required | ({"event_count"} if countable else set())
    if not required <= set(entry) or not set(entry) <= permitted:
        return False
    if not isinstance(entry["filename"], str) or entry["filename"] not in EVIDENCE_FILENAMES:
        return False
    if not isinstance(entry["sha256"], str) or len(entry["sha256"]) != 64:
        return False
    if type(entry["byte_size"]) is not int:
        return False
    if entry["record_integrity"] not in RECORD_INTEGRITIES:
        return False
    if "event_count" in entry and type(entry["event_count"]) is not int:
        return False
    # event_count is omitted rather than invented for malformed bytes (§18.3).
    return not (entry["record_integrity"] == "MALFORMED_PRESERVED" and "event_count" in entry)


def _bindings_match_bytes(episode_directory: Path, entries: Sequence[object]) -> bool:
    for entry in entries:
        if not isinstance(entry, dict):
            return False
        path = episode_directory / str(entry["filename"])
        if not path.is_file():
            return False
        try:
            digest, size = sha256_of_file(path)
        except OSError:
            return False
        if digest != entry["sha256"] or size != entry["byte_size"]:
            return False
    return True


def terminal_identity(episode_directory: Path) -> tuple[str, int]:
    """Return the terminal identity. It exists if and only if the manifest is TM-2."""
    if classify_terminal_manifest(episode_directory) != TM_VALID:
        raise EpisodeStateError("terminal identity exists only for a TM-2 manifest")
    return sha256_of_file(episode_directory / EPISODE_MANIFEST_FILENAME)


@dataclass
class EpisodeSurvey:
    """Everything ``finalize`` needs to bind and to select a terminal disposition."""

    core_binding: dict[str, object]
    record_bindings: list[dict[str, object]]
    corrupt: bool
    invalidated: bool
    refused: bool
    failed: bool
    complete_equal: bool


def survey_episode(context: EpisodeContext) -> EpisodeSurvey:
    """Bind every evidence record present at seal and classify the episode."""
    core_path = context.directory / EPISODE_CORE_FILENAME
    core_digest, core_size = sha256_of_file(core_path)
    core_bytes = core_path.read_bytes()
    core_integrity = "WELL_FORMED"
    try:
        decoded = json.loads(core_bytes.decode("utf-8"))
        if not isinstance(decoded, dict) or canonical_json_bytes(decoded) != core_bytes:
            core_integrity = "MALFORMED_PRESERVED"
    except (UnicodeDecodeError, json.JSONDecodeError):
        core_integrity = "MALFORMED_PRESERVED"

    scans = context.scans()
    bindings: list[dict[str, object]] = []
    corrupt = core_integrity == "MALFORMED_PRESERVED"
    refused = False
    failed = False
    for filename in BOUND_RECORD_FILENAMES:
        scan = scans.get(filename)
        if scan is None:
            continue
        binding: dict[str, object] = {
            "filename": scan.filename,
            "sha256": scan.sha256,
            "byte_size": scan.byte_size,
            "record_integrity": scan.record_integrity,
        }
        if scan.event_count is not None:
            binding["event_count"] = scan.event_count
        bindings.append(binding)
        if scan.record_integrity == "MALFORMED_PRESERVED":
            corrupt = True
            continue
        if filename == EPISODE_INVALIDATION_FILENAME:
            continue
        # A structurally unsealed opened stage is an unresolved corruption condition.
        if scan.structurally_unsealed:
            corrupt = True
        elif scan.sealed_disposition == "STAGE_REFUSED":
            refused = True
        elif scan.sealed_disposition == "STAGE_FAILED":
            failed = True

    invalidated = EPISODE_INVALIDATION_FILENAME in scans
    complete_equal = _is_complete_equal(scans)
    return EpisodeSurvey(
        core_binding={
            "filename": EPISODE_CORE_FILENAME,
            "sha256": core_digest,
            "byte_size": core_size,
            "record_integrity": core_integrity,
        },
        record_bindings=bindings,
        corrupt=corrupt,
        invalidated=invalidated,
        refused=refused,
        failed=failed,
        complete_equal=complete_equal,
    )


def _is_complete_equal(scans: Mapping[str, JournalScan]) -> bool:
    """Return whether every §13.1 success prerequisite holds."""
    required = (
        STAGE_GENERATE_A_FILENAME,
        STAGE_GENERATE_B_FILENAME,
        STAGE_COMPARE_FILENAME,
        STAGE_VERIFY_FILENAME,
    )
    if any(name not in scans for name in required):
        return False
    for name in required:
        scan = scans[name]
        if scan.record_integrity != "WELL_FORMED" or scan.sealed_disposition != "STAGE_COMPLETE":
            return False
    for name in (STAGE_COMPARE_FILENAME, STAGE_VERIFY_FILENAME):
        derived = scans[name].latest("comparison_derived")
        if derived is None or derived.get("comparison_disposition") != "EQUAL_VERIFIED":
            return False
    return True


def select_terminal_disposition(survey: EpisodeSurvey) -> str:
    """Apply the fixed §20.7 precedence. Evidence integrity outranks causal outcome."""
    if survey.corrupt:
        return "EPISODE_EVIDENCE_CORRUPT"
    if survey.invalidated:
        return "EPISODE_INVALIDATED"
    if survey.refused:
        return "EPISODE_REFUSED"
    if survey.failed or not survey.complete_equal:
        return "EPISODE_FAILED"
    return "EPISODE_COMPLETE_EQUAL"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def command_open(arguments: argparse.Namespace, store: EvidenceStore) -> int:
    """Create ``episode-core.json`` exactly once."""
    episode_id = require_episode_id(arguments.episode_id)
    expected = require_commit(arguments.expected_canonical_commit)
    repository_root = resolve_safe_path(arguments.repository_root)
    evidence_root = resolve_safe_path(arguments.external_evidence_root)
    validate_evidence_root(evidence_root, repository_root)

    # The pre-open observation is mandatory and non-durable (PIC-2).
    observed = resolve_canonical_commit(repository_root)
    if observed != expected:
        # Nothing at all is created: no directory, no core, no terminal identity.
        raise CanonicalMainMismatchError(
            "canonical main does not match expected_canonical_commit; open refuses"
        )

    operator = resolve_operator_identity(repository_root)
    harness = resolve_harness_identity(repository_root)
    runtime = resolve_runtime_identity()
    core = build_episode_core(
        episode_id=episode_id,
        expected_canonical_commit=expected,
        repository_root=repository_root,
        external_evidence_root=evidence_root,
        operator=operator,
        harness=harness,
        runtime=runtime,
    )
    directory = evidence_root / episode_id
    try:
        directory.mkdir(parents=False, exist_ok=False)
    except FileExistsError as error:
        raise EpisodeStateError(f"episode directory already exists: {directory}") from error
    # The newly created episode directory is validated before episode-core is written.
    require_safe_episode_directory(directory, evidence_root)
    payload = canonical_json_bytes(core)
    core_path = require_safe_evidence_path(directory / EPISODE_CORE_FILENAME)
    try:
        store.create_exclusive(core_path, payload)
    except FileExistsError as error:
        raise EpisodeStateError("episode-core.json already exists; write-once") from error
    identity = sha256_of_bytes(payload)
    _report(
        f"episode {episode_id} opened",
        f"episode_identity {identity}",
    )
    return 0


def _generate_stage_for(generation: str) -> str:
    return "GENERATE_A" if generation == "A" else "GENERATE_B"


def command_generate(
    arguments: argparse.Namespace, store: EvidenceStore, runner: ChildRunner
) -> int:
    repository_root = resolve_safe_path(arguments.repository_root)
    evidence_root = resolve_safe_path(arguments.external_evidence_root)
    workspace = resolve_safe_path(arguments.workspace)
    future_evidence_root = resolve_safe_path(arguments.future_evidence_root)
    require_disjoint(evidence_root, "external evidence root", workspace, "generation workspace")
    require_disjoint(
        evidence_root, "external evidence root", future_evidence_root, "future evidence root"
    )
    context = open_episode_context(
        episode_id=arguments.episode_id,
        repository_root=repository_root,
        evidence_root=evidence_root,
        store=store,
    )
    require_scientific_continuation(context)
    inputs = {surface: resolve_safe_path(getattr(arguments, surface)) for surface in INPUT_SURFACES}
    runtime = resolve_runtime_identity()
    command = build_generate_command(
        python_executable=runtime.resolved_python_executable_path,
        operator_path=repository_root / Path(OPERATOR_RELATIVE_PATH),
        expected_canonical_commit=context.core.expected_canonical_commit,
        repository_root=repository_root,
        generation=arguments.generation,
        workspace=workspace,
        external_evidence_root=evidence_root,
        future_evidence_root=future_evidence_root,
        inputs=inputs,
        python_version=runtime.python_version,
    )
    body = GenerateBody(
        generation=arguments.generation,
        workspace=workspace,
        future_evidence_root=future_evidence_root,
        inputs=inputs,
        command=command,
    )
    with context.pinned():
        outcome = run_stage(
            context,
            stage=_generate_stage_for(arguments.generation),
            argv=command,
            generation_identity=arguments.generation,
            body=body,
            runner=runner,
        )
    return _report_stage(outcome)


def _compare_context(
    arguments: argparse.Namespace, store: EvidenceStore
) -> tuple[EpisodeContext, Path, Path, tuple[str, ...]]:
    repository_root = resolve_safe_path(arguments.repository_root)
    evidence_root = resolve_safe_path(arguments.external_evidence_root)
    workspace_a = resolve_safe_path(arguments.generation_a_workspace)
    workspace_b = resolve_safe_path(arguments.generation_b_workspace)
    require_disjoint(evidence_root, "external evidence root", workspace_a, "Generation A workspace")
    require_disjoint(evidence_root, "external evidence root", workspace_b, "Generation B workspace")
    context = open_episode_context(
        episode_id=arguments.episode_id,
        repository_root=repository_root,
        evidence_root=evidence_root,
        store=store,
    )
    require_scientific_continuation(context)
    runtime = resolve_runtime_identity()
    command = build_compare_command(
        python_executable=runtime.resolved_python_executable_path,
        operator_path=repository_root / Path(OPERATOR_RELATIVE_PATH),
        generation_a_workspace=workspace_a,
        generation_b_workspace=workspace_b,
    )
    return context, workspace_a, workspace_b, command


def command_compare(
    arguments: argparse.Namespace, store: EvidenceStore, runner: ChildRunner
) -> int:
    context, workspace_a, workspace_b, command = _compare_context(arguments, store)
    for filename in (STAGE_GENERATE_A_FILENAME, STAGE_GENERATE_B_FILENAME):
        path = context.directory / filename
        if not path.is_file() or scan_journal(path).sealed_disposition != "STAGE_COMPLETE":
            raise EpisodeStateError(f"compare requires a completed {filename}")
    body = CompareBody(
        generation_a_workspace=workspace_a,
        generation_b_workspace=workspace_b,
        command=command,
        observe_before_child=True,
    )
    with context.pinned():
        outcome = run_stage(
            context,
            stage="COMPARE",
            argv=command,
            generation_identity=None,
            body=body,
            runner=runner,
        )
    return _report_stage(outcome)


def command_verify(arguments: argparse.Namespace, store: EvidenceStore, runner: ChildRunner) -> int:
    context, workspace_a, workspace_b, command = _compare_context(arguments, store)
    compare_path = context.directory / STAGE_COMPARE_FILENAME
    if not compare_path.is_file():
        raise EpisodeStateError("verify requires a completed stage-compare.jsonl")
    compare_scan = scan_journal(compare_path)
    if compare_scan.sealed_disposition != "STAGE_COMPLETE":
        raise EpisodeStateError("verify requires a completed stage-compare.jsonl")
    derived = compare_scan.latest("comparison_derived")
    expected = str(derived["comparison_disposition"]) if derived else None
    body = CompareBody(
        generation_a_workspace=workspace_a,
        generation_b_workspace=workspace_b,
        command=command,
        # The §5 matrix gives verify one observation only, with no pre-child repeat.
        observe_before_child=False,
        expected_disposition=expected,
    )
    with context.pinned():
        outcome = run_stage(
            context,
            stage="VERIFY",
            argv=command,
            generation_identity=None,
            body=body,
            runner=runner,
        )
    return _report_stage(outcome)


def command_invalidate(arguments: argparse.Namespace, store: EvidenceStore) -> int:
    """Append one pre-seal invalidation record. This is the only writer of that record."""
    repository_root = resolve_safe_path(arguments.repository_root)
    evidence_root = resolve_safe_path(arguments.external_evidence_root)
    context = open_episode_context(
        episode_id=arguments.episode_id,
        repository_root=repository_root,
        evidence_root=evidence_root,
        store=store,
    )
    if context.manifest_path.exists():
        raise EpisodeStateError("the episode is sealed or terminalized; invalidation is pre-seal")
    failure_class = arguments.failure_class
    if failure_class not in FAILURE_CLASSES:
        raise ArgumentRefusalError(f"failure_class outside the closed enumeration: {failure_class}")
    if arguments.causal_stage not in CAUSAL_STAGES:
        raise ArgumentRefusalError(f"causal_stage outside enumeration: {arguments.causal_stage}")
    # CHILD_NONZERO_EXIT derives its triad from operator_error_class (§19.2), so a
    # missing or non-enumerated value is a controlled pre-mutation argument
    # refusal here rather than an uncaught error inside the closed table.
    operator_error_class = arguments.operator_error_class
    if failure_class == "CHILD_NONZERO_EXIT" and operator_error_class not in OPERATOR_ERROR_CLASSES:
        raise ArgumentRefusalError(
            "failure_class CHILD_NONZERO_EXIT requires an operator_error_class from the "
            "closed enumeration"
        )
    observed_class, root_cause, remediation = derive_failure_triad(
        failure_class, operator_error_class
    )

    record: dict[str, object] = {
        "schema_version": INVALIDATION_SCHEMA_VERSION,
        "episode_identity": context.core.identity,
        "event_ordinal": _next_invalidation_ordinal(context),
        "root_cause_class": root_cause,
        "causal_stage": arguments.causal_stage,
        "failure_class": observed_class,
        "remediation_disposition": remediation,
        "affected_candidates": _affected_candidates(arguments.affected_candidate_workspace),
        "originating_episode_identity": context.core.identity,
        # An invalidated episode can never be continued, so a fresh attempt always
        # requires a new episode (§17.2, §22).
        "new_episode_required": True,
        "recorded_at": utc_timestamp(),
    }
    # Repository identity is material exactly for canonical-main movement (PIC-4).
    if root_cause == "CANONICAL_MAIN_MOVEMENT" or failure_class == "CANONICAL_MAIN_MISMATCH":
        expected = context.core.expected_canonical_commit
        observed = resolve_canonical_commit(repository_root)
        if expected == observed:
            raise ArgumentRefusalError(
                "canonical-main movement was claimed but expected equals observed"
            )
        record["canonical_main_movement"] = {
            "expected_canonical_commit": expected,
            "observed_canonical_commit": observed,
        }
    # The episode directory and the invalidation path are re-validated before the append.
    with context.pinned():
        context.require_safe_directory()
        require_safe_evidence_path(context.invalidation_path)
        if not context.invalidation_path.exists():
            store.create_exclusive(context.invalidation_path, b"")
        append_canonical_event(store, context.invalidation_path, record)
    _report(f"invalidation recorded: {observed_class} / {root_cause} / {remediation}")
    return 0


def _next_invalidation_ordinal(context: EpisodeContext) -> int:
    if not context.invalidation_path.is_file():
        return 1
    scan = scan_journal(context.invalidation_path)
    if scan.event_count is None:
        raise EpisodeStateError("invalidation record bytes are malformed; nothing is appended")
    return scan.event_count + 1


def _affected_candidates(workspace: str | None) -> list[dict[str, object]]:
    if workspace is None:
        return []
    resolved = resolve_safe_path(workspace)
    return [dict(entry) for entry in hash_candidate_bundle(resolved)]


def command_finalize(arguments: argparse.Namespace, store: EvidenceStore) -> int:
    """Create the write-once terminal manifest. Finalize is the last P-A mutation."""
    repository_root = resolve_safe_path(arguments.repository_root)
    evidence_root = resolve_safe_path(arguments.external_evidence_root)
    context = open_episode_context(
        episode_id=arguments.episode_id,
        repository_root=repository_root,
        evidence_root=evidence_root,
        store=store,
    )
    # The episode directory and the manifest path are validated before the
    # terminal-manifest state is even classified.
    context.require_safe_directory()
    require_safe_evidence_path(context.manifest_path)
    state = classify_terminal_manifest(context.directory)
    if state == TM_VALID:
        # Already sealed. The identity is recomputed read-only; nothing is mutated.
        digest, size = terminal_identity(context.directory)
        raise EpisodeStateError(
            f"episode is already sealed (TM-2); terminal identity {digest} / {size} bytes"
        )
    if state == TM_INVALID:
        raise EpisodeStateError(
            "terminalization irrecoverably failed (TM-1); exact bytes are preserved and no "
            "terminal disposition or terminal identity exists"
        )

    # The pre-finalize observation is mandatory and non-durable (PIC-3).
    expected = context.core.expected_canonical_commit
    observed = resolve_canonical_commit(repository_root)
    if observed != expected:
        _require_recorded_movement(context, expected, observed)

    survey = survey_episode(context)
    disposition = select_terminal_disposition(survey)
    manifest: dict[str, object] = {
        "schema_version": EPISODE_MANIFEST_SCHEMA_VERSION,
        "episode_identity": context.core.identity,
        "episode_core": survey.core_binding,
        "records": survey.record_bindings,
        "terminal_disposition": disposition,
        "manifest_sealed_at": utc_timestamp(),
    }
    payload = canonical_json_bytes(manifest)
    with context.pinned():
        context.require_safe_directory()
        try:
            store.create_exclusive(require_safe_evidence_path(context.manifest_path), payload)
        except FileExistsError as error:
            raise EpisodeStateError("episode-manifest.json already exists; write-once") from error
        # The seal is only reported once the path is re-confirmed after the write.
        context.require_safe_directory()
        digest, size = terminal_identity(context.directory)
    _report(
        f"episode sealed: {disposition}",
        f"terminal_identity {digest}",
        f"terminal_byte_size {size}",
    )
    return 0


def _require_recorded_movement(context: EpisodeContext, expected: str, observed: str) -> None:
    """Containment requires an explicit prior invalidate carrying the exact pair (§5.2.1)."""
    path = context.invalidation_path
    if not path.is_file():
        raise CanonicalMainMismatchError(
            "canonical main moved; an explicit invalidate must record the movement first"
        )
    scan = scan_journal(path)
    for event in scan.events:
        movement = event.get("canonical_main_movement")
        if not isinstance(movement, dict):
            continue
        if (
            movement.get("expected_canonical_commit") == expected
            and movement.get("observed_canonical_commit") == observed
        ):
            return
    raise CanonicalMainMismatchError(
        "canonical main moved again after invalidate; a new explicit invalidate is required"
    )


# ---------------------------------------------------------------------------
# Reporting and CLI
# ---------------------------------------------------------------------------


def _report(*lines: str) -> None:
    """Emit closed-vocabulary progress only. No protected content is ever emitted."""
    for line in lines:
        sys.stdout.write(f"{line}\n")


def _report_stage(outcome: StageOutcome) -> int:
    if outcome.structurally_unsealed:
        _report(
            f"stage {outcome.stage} is structurally unsealed; nothing was fabricated",
            "scientific continuation is prohibited",
        )
        return 1
    if outcome.disposition is None:
        _report(
            f"stage {outcome.stage} evidence bytes are malformed and preserved exactly",
            "no stage_disposition exists",
        )
        return 1
    _report(f"stage {outcome.stage} sealed: {outcome.disposition}")
    return 0 if outcome.disposition == "STAGE_COMPLETE" else 1


#: Exactly six commands. There is no seventh, and no alias creates new semantics.
COMMANDS: Final[tuple[str, ...]] = (
    "open",
    "generate",
    "compare",
    "verify",
    "invalidate",
    "finalize",
)


def _add_episode_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--episode-id", required=True)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--external-evidence-root", required=True)


def build_parser() -> argparse.ArgumentParser:
    """Return the six-command harness parser. Every path argument is explicit."""
    parser = argparse.ArgumentParser(
        prog="mesc_p01_04d_evidence_harness",
        description=(
            "MESC P01-04D external execution-evidence harness. Running it does not "
            "authorize P01-04D execution over protected inputs."
        ),
    )
    subparsers = parser.add_subparsers(
        dest="command", metavar="{open,generate,compare,verify,invalidate,finalize}"
    )

    open_parser = subparsers.add_parser("open", help="create the write-once episode core")
    _add_episode_arguments(open_parser)
    open_parser.add_argument("--expected-canonical-commit", required=True)

    generate_parser = subparsers.add_parser("generate", help="run exactly one operator generate")
    _add_episode_arguments(generate_parser)
    generate_parser.add_argument("--generation", required=True, choices=list(GENERATION_IDENTITIES))
    generate_parser.add_argument("--workspace", required=True)
    generate_parser.add_argument("--future-evidence-root", required=True)
    for surface in INPUT_SURFACES:
        generate_parser.add_argument(SURFACE_ARGUMENTS[surface], required=True, dest=surface)

    compare_parser = subparsers.add_parser("compare", help="run exactly one operator compare")
    _add_episode_arguments(compare_parser)
    compare_parser.add_argument("--generation-a-workspace", required=True)
    compare_parser.add_argument("--generation-b-workspace", required=True)

    verify_parser = subparsers.add_parser("verify", help="rerun canonical compare for this episode")
    _add_episode_arguments(verify_parser)
    verify_parser.add_argument("--generation-a-workspace", required=True)
    verify_parser.add_argument("--generation-b-workspace", required=True)

    invalidate_parser = subparsers.add_parser(
        "invalidate", help="append one pre-seal invalidation record"
    )
    _add_episode_arguments(invalidate_parser)
    invalidate_parser.add_argument("--failure-class", required=True, choices=list(FAILURE_CLASSES))
    invalidate_parser.add_argument("--causal-stage", required=True, choices=list(CAUSAL_STAGES))
    invalidate_parser.add_argument(
        "--operator-error-class", default=None, choices=list(OPERATOR_ERROR_CLASSES)
    )
    invalidate_parser.add_argument("--affected-candidate-workspace", default=None)

    finalize_parser = subparsers.add_parser("finalize", help="create the terminal manifest once")
    _add_episode_arguments(finalize_parser)
    return parser


def dispatch(
    arguments: argparse.Namespace,
    *,
    store: EvidenceStore,
    runner: ChildRunner,
) -> int:
    """Route one parsed command. Qualification injects the store and runner here."""
    if arguments.command == "open":
        return command_open(arguments, store)
    if arguments.command == "generate":
        return command_generate(arguments, store, runner)
    if arguments.command == "compare":
        return command_compare(arguments, store, runner)
    if arguments.command == "verify":
        return command_verify(arguments, store, runner)
    if arguments.command == "invalidate":
        return command_invalidate(arguments, store)
    if arguments.command == "finalize":
        return command_finalize(arguments, store)
    raise ArgumentRefusalError(f"unknown command: {arguments.command!r}")


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and dispatch, failing closed on every harness refusal."""
    parser = build_parser()
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    if arguments.command is None:
        parser.print_usage(sys.stderr)
        return 2
    try:
        return dispatch(arguments, store=EvidenceStore(), runner=ChildRunner())
    except HarnessError as error:
        # Closed-vocabulary classification only; no traceback and no environment is emitted.
        sys.stderr.write(f"{type(error).failure_class}: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
