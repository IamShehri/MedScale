"""Filesystem safety, write-once generation and A/B comparison for P01-04D.

This private module is the operational half of the controlled formal executor.
It owns every filesystem decision and nothing scientific: the policy, the
allocation and the seven candidate payloads all come from
``medscale.mesc._formal_split_v1``.

It performs no network access, spawns no subprocess, reads no clock and reads no
environment value.  It reads the running interpreter version and the caller's
explicit paths *for validation only*; neither ever reaches a deterministic
artifact byte.  Repository identity is resolved by reading the Git ref files
directly rather than by invoking Git.

Nothing here imports the fixture-only tooling (FD-DREADY-2).

Every failure is typed and fail-closed.  A failed or partial workspace is never
repaired, reused, promoted or treated as a valid candidate, and comparison never
writes.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Final

from medscale.mesc._canonical_json_v1 import sha256_of_bytes
from medscale.mesc._formal_split_v1 import (
    ARTIFACT_FILE_SCHEMAS,
    ARTIFACT_FILENAMES,
    ARTIFACT_SURFACES,
    DECISION_RECORD_SURFACE,
    EXAMPLE_REGISTRY_FILENAME,
    EXCLUDED_LEDGER_FILENAME,
    GENERATION_IDENTITIES,
    GENERATION_MANIFEST_FILENAME,
    GENERATION_MANIFEST_SCHEMA,
    GROUP_REGISTRY_FILENAME,
    INPUT_SCHEMA_VERSIONS,
    MANIFEST_DIGESTED_FILENAMES,
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    REQUIRED_INPUT_SURFACES,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    SOURCE_RECORDS_SURFACE,
    SPLIT_POLICY_FILENAME,
    SPLIT_POLICY_SCHEMA,
    SPLIT_SUMMARY_FILENAME,
    SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
    FormalArtifactBundle,
    FormalArtifactEntry,
    FormalByteEqualityError,
    FormalEvidenceConfigurationError,
    FormalFingerprintError,
    FormalGenerationError,
    FormalGenerationManifest,
    FormalInputDescriptor,
    FormalInputIdentityError,
    FormalInputSchemaError,
    FormalInventoryError,
    FormalMetadataError,
    FormalSplitInputIdentity,
    FormalWorkspaceSafetyError,
    allocate_formal_groups,
    build_formal_bundle,
    build_input_identity,
    execution_input_manifest_identity,
    join_formal_examples,
    parse_ordered_example_registry,
    parse_source_document_registry,
    parse_source_records,
    parse_transformed_dataset_identity,
    verify_bundle,
    verify_input_digest,
)
from medscale.mesc._split_artifacts_v1 import (
    SplitSummaryIdentityCore,
    build_split_fingerprint_identity,
    build_split_fingerprint_record,
    reject_forbidden_metadata,
    verify_split_fingerprint_record,
)
from medscale.mesc._split_v1 import ALGORITHM_VERSION, SPLIT_SEED

_HEX_DIGITS: Final = frozenset("0123456789abcdef")
_COMMIT_LENGTH: Final = 40


@dataclass(frozen=True, slots=True)
class FormalSplitRequest:
    """One immutable, fully validated request for exactly one generation.

    Construction resolves nothing and reads nothing; :func:`build_request` does
    the resolution and hands over values that are already absolute.  Caller-owned
    mappings and sequences are snapshotted so later caller mutation cannot alter
    a request that has already been validated.
    """

    expected_canonical_commit: str
    generation_identity: str
    input_identity: FormalSplitInputIdentity
    workspace: Path
    repository_root: Path
    protected_roots: tuple[Path, ...]
    external_evidence_root: Path
    future_evidence_root: Path
    python_version: str
    input_locations: Mapping[str, Path]

    def __post_init__(self) -> None:
        object.__setattr__(self, "protected_roots", tuple(self.protected_roots))
        object.__setattr__(self, "input_locations", MappingProxyType(dict(self.input_locations)))
        if self.generation_identity not in GENERATION_IDENTITIES:
            raise FormalGenerationError(
                f"generation identity must be one of {list(GENERATION_IDENTITIES)}, "
                f"got {self.generation_identity!r}"
            )
        _require_commit(self.expected_canonical_commit)
        if not isinstance(self.input_identity, FormalSplitInputIdentity):
            raise FormalInputIdentityError("input_identity must be a FormalSplitInputIdentity")
        if sorted(self.input_locations) != sorted(REQUIRED_INPUT_SURFACES):
            raise FormalInputIdentityError(
                f"input locations must be exactly {sorted(REQUIRED_INPUT_SURFACES)}"
            )
        for name in (
            "workspace",
            "repository_root",
            "external_evidence_root",
            "future_evidence_root",
        ):
            value = getattr(self, name)
            if not isinstance(value, Path) or not value.is_absolute():
                raise FormalWorkspaceSafetyError(f"{name} must be an absolute resolved path")


@dataclass(frozen=True, slots=True)
class FormalGenerationResult:
    """The immutable outcome of exactly one completed generation."""

    generation_identity: str
    workspace: Path
    filenames: tuple[str, ...]
    digests: Mapping[str, str]
    byte_sizes: Mapping[str, int]
    split_fingerprint: str
    #: The execution-input-manifest identity (P-C1a §5.6, XD-EXEC-3). It is
    #: derived from this executor's own input measurement, never from P-A2
    #: evidence, and it names no path, time or commit.
    execution_input_manifest_sha256: str
    execution_input_manifest_byte_size: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "digests", MappingProxyType(dict(self.digests)))
        object.__setattr__(self, "byte_sizes", MappingProxyType(dict(self.byte_sizes)))
        if tuple(self.filenames) != ARTIFACT_FILENAMES:
            raise FormalInventoryError(
                f"result must carry exactly {list(ARTIFACT_FILENAMES)}, got {list(self.filenames)}"
            )


@dataclass(frozen=True, slots=True)
class FormalComparisonResult:
    """The immutable disposition of one A/B comparison. It records; it never repairs."""

    workspace_a: Path
    workspace_b: Path
    filenames: tuple[str, ...]
    equal_filenames: tuple[str, ...]
    split_fingerprint: str
    equal: bool

    def __post_init__(self) -> None:
        if tuple(self.filenames) != ARTIFACT_FILENAMES:
            raise FormalInventoryError("comparison must cover exactly the seven candidate files")


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _require_commit(value: object) -> str:
    if type(value) is not str or len(value) != _COMMIT_LENGTH:
        raise FormalInputIdentityError(
            f"expected canonical commit must be {_COMMIT_LENGTH} hex characters, got {value!r}"
        )
    if any(character not in _HEX_DIGITS for character in value):
        raise FormalInputIdentityError("expected canonical commit must be lowercase hexadecimal")
    return value


def running_python_version() -> str:
    """Return the running interpreter version. Validation only; never an artifact value."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def _is_within(candidate: Path, ancestor: Path) -> bool:
    """Return whether ``candidate`` is ``ancestor`` or lies beneath it.

    Path components are compared after resolution.  A string-prefix test would
    treat ``/srv/repo-backup`` as being inside ``/srv/repo``.
    """
    return candidate == ancestor or ancestor.parts == candidate.parts[: len(ancestor.parts)]


def resolve_repository_commit(repository_root: Path) -> str:
    """Return the checked-out commit by reading Git ref files, never by invoking Git."""
    git_entry = repository_root / ".git"
    if git_entry.is_file():
        pointer = git_entry.read_text(encoding="utf-8").strip()
        if not pointer.startswith("gitdir:"):
            raise FormalInputIdentityError("repository .git file is not a gitdir pointer")
        git_dir = Path(pointer.split(":", 1)[1].strip())
        if not git_dir.is_absolute():
            git_dir = (repository_root / git_dir).resolve()
    elif git_entry.is_dir():
        git_dir = git_entry
    else:
        raise FormalInputIdentityError(f"{repository_root} is not a Git repository")

    head_file = git_dir / "HEAD"
    if not head_file.is_file():
        raise FormalInputIdentityError("repository HEAD is missing")
    head = head_file.read_text(encoding="utf-8").strip()
    if not head.startswith("ref:"):
        return _require_commit(head)

    ref_name = head.split(":", 1)[1].strip()
    common_dir = git_dir
    common_file = git_dir / "commondir"
    if common_file.is_file():
        common = Path(common_file.read_text(encoding="utf-8").strip())
        common_dir = common if common.is_absolute() else (git_dir / common).resolve()
    for base in (git_dir, common_dir):
        candidate = base / Path(ref_name)
        if candidate.is_file():
            return _require_commit(candidate.read_text(encoding="utf-8").strip())
    packed = common_dir / "packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or line.startswith("^") or " " not in line:
                continue
            value, name = line.split(" ", 1)
            if name.strip() == ref_name:
                return _require_commit(value.strip())
    raise FormalInputIdentityError(f"repository reference {ref_name!r} could not be resolved")


def _validate_workspace_safety(request: FormalSplitRequest) -> None:
    """Refuse an unsafe destination.

    Order is fixed so a destination that is wrong in several ways always fails
    the same way: evidence-root **configuration** first, then protected-root
    ancestry, then workspace **state**.  Checking freshness first would report an
    evidence root that happens to exist as mere reuse and hide the configuration
    defect that actually has to be corrected.
    """
    workspace = request.workspace
    if _is_within(workspace, request.future_evidence_root):
        raise FormalEvidenceConfigurationError(
            "a generator must never write into the future evidence root"
        )
    if workspace == request.external_evidence_root or _is_within(
        workspace, request.external_evidence_root
    ):
        raise FormalEvidenceConfigurationError(
            "the generation workspace must not be the external evidence root"
        )
    if _is_within(workspace, request.repository_root):
        raise FormalWorkspaceSafetyError("generation workspace must be outside the repository root")
    for protected in request.protected_roots:
        if _is_within(workspace, protected):
            raise FormalWorkspaceSafetyError(
                f"generation workspace must be outside the protected root {protected}"
            )
    if _is_within(request.repository_root, workspace):
        raise FormalWorkspaceSafetyError("the repository root must not be inside the workspace")
    if workspace.exists() or workspace.is_symlink():
        raise FormalWorkspaceSafetyError(f"generation workspace already exists: {workspace}")
    parent = workspace.parent
    if not parent.is_dir():
        raise FormalWorkspaceSafetyError(f"workspace parent does not exist: {parent}")


def _resolve_protected_root(value: Path, *, label: str) -> Path:
    if not value.is_absolute():
        raise FormalWorkspaceSafetyError(f"{label} must be an absolute path, got {value}")
    resolved = value.resolve()
    if not resolved.is_absolute():  # pragma: no cover - resolve always yields absolute
        raise FormalWorkspaceSafetyError(f"{label} could not be resolved")
    return resolved


def build_request(
    *,
    expected_canonical_commit: str,
    repository_root: Path,
    generation_identity: str,
    workspace: Path,
    external_evidence_root: Path,
    future_evidence_root: Path,
    input_locations: Mapping[str, Path],
    python_version: str,
) -> FormalSplitRequest:
    """Resolve, verify and freeze one request. No workspace mutation occurs here."""
    if generation_identity not in GENERATION_IDENTITIES:
        raise FormalGenerationError(
            f"generation identity must be one of {list(GENERATION_IDENTITIES)}, "
            f"got {generation_identity!r}"
        )
    if sorted(input_locations) != sorted(REQUIRED_INPUT_SURFACES):
        raise FormalInputIdentityError(
            f"input locations must be exactly {sorted(REQUIRED_INPUT_SURFACES)}"
        )
    _require_commit(expected_canonical_commit)

    actual_version = running_python_version()
    if python_version != actual_version:
        raise FormalInputIdentityError(
            f"declared interpreter version {python_version!r} does not match the running "
            f"interpreter {actual_version!r}"
        )

    resolved_repository = _resolve_protected_root(repository_root, label="repository root")
    resolved_external = _resolve_protected_root(
        external_evidence_root, label="external evidence root"
    )
    resolved_future = _resolve_protected_root(future_evidence_root, label="future evidence root")
    if not workspace.is_absolute():
        raise FormalWorkspaceSafetyError(f"workspace must be an absolute path, got {workspace}")
    # ``strict=False`` is required: the workspace must not exist yet.
    resolved_workspace = Path(workspace).resolve()

    actual_commit = resolve_repository_commit(resolved_repository)
    if actual_commit != expected_canonical_commit:
        raise FormalInputIdentityError(
            f"repository is at {actual_commit!r}, not the expected {expected_canonical_commit!r}"
        )

    resolved_inputs: dict[str, Path] = {}
    payloads: dict[str, bytes] = {}
    for surface in sorted(REQUIRED_INPUT_SURFACES):
        location = Path(input_locations[surface])
        if not location.is_absolute():
            raise FormalInputIdentityError(f"input {surface!r} must be an absolute path")
        resolved = location.resolve()
        if resolved.is_symlink() or not resolved.is_file():
            raise FormalInputIdentityError(f"input {surface!r} must be an existing regular file")
        resolved_inputs[surface] = resolved
        payloads[surface] = resolved.read_bytes()

    protected_roots = (resolved_repository / "specs" / "mesc-pilot-01" / "p01-03g", resolved_future)
    identity = build_input_identity(payloads)
    request = FormalSplitRequest(
        expected_canonical_commit=expected_canonical_commit,
        generation_identity=generation_identity,
        input_identity=identity,
        workspace=resolved_workspace,
        repository_root=resolved_repository,
        protected_roots=protected_roots,
        external_evidence_root=resolved_external,
        future_evidence_root=resolved_future,
        python_version=python_version,
        input_locations=resolved_inputs,
    )
    _validate_workspace_safety(request)
    return request


def build_bundle_for_request(request: FormalSplitRequest) -> FormalArtifactBundle:
    """Perform every scientific check and build the seven payloads entirely in memory."""
    payloads: dict[str, bytes] = {}
    for surface, location in request.input_locations.items():
        payload = location.read_bytes()
        verify_input_digest(payload, request.input_identity.descriptor(surface))
        payloads[surface] = payload

    dataset_identity = parse_transformed_dataset_identity(
        payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE]
    )
    source_records = payloads[SOURCE_RECORDS_SURFACE]
    if sha256_of_bytes(source_records) != dataset_identity.source_records_sha256:
        raise FormalInputIdentityError(
            "label source digest does not match the attested transformed-dataset identity"
        )
    if len(source_records) != dataset_identity.source_records_byte_size:
        raise FormalInputIdentityError(
            "label source byte size does not match the attested transformed-dataset identity"
        )
    if not payloads[DECISION_RECORD_SURFACE]:
        raise FormalInputIdentityError("the ratified decision record must not be empty")

    ordered_rows = parse_ordered_example_registry(payloads[ORDERED_EXAMPLE_REGISTRY_SURFACE])
    document_counts = parse_source_document_registry(payloads[SOURCE_DOCUMENT_REGISTRY_SURFACE])
    source_labels = parse_source_records(source_records)

    joined = join_formal_examples(ordered_rows, source_labels, dataset_identity, document_counts)
    assignments = allocate_formal_groups(joined)
    bundle = build_formal_bundle(
        input_identity=request.input_identity, joined=joined, assignments=assignments
    )
    verify_bundle(bundle)
    return bundle


def _reverify_repository_identity(request: FormalSplitRequest) -> None:
    """Re-read the repository commit immediately before the first mutation.

    ``build_request`` verified the commit when the request was assembled, but an
    arbitrary amount of time and work passes between then and workspace creation.
    This re-reads the actual repository identity from disk through the same
    accepted helper — never a value cached on the request — so a commit that moved
    in between is refused before any filesystem mutation (review finding F2).
    """
    actual = resolve_repository_commit(request.repository_root)
    if actual != request.expected_canonical_commit:
        raise FormalInputIdentityError(
            f"canonical commit moved before generation: repository is at {actual!r}, "
            f"not the expected {request.expected_canonical_commit!r}"
        )


def generate(request: FormalSplitRequest) -> FormalGenerationResult:
    """Execute exactly one generation. Every check completes before any mutation."""
    if not isinstance(request, FormalSplitRequest):
        raise FormalGenerationError("generate requires an exact FormalSplitRequest")
    bundle = build_bundle_for_request(request)
    _validate_workspace_safety(request)
    _reverify_repository_identity(request)

    workspace = request.workspace
    workspace.mkdir(parents=False, exist_ok=False)
    for filename, payload in bundle.ordered_payloads():
        target = workspace / filename
        with target.open("xb") as handle:
            handle.write(payload)

    _verify_inventory(workspace)
    digests: dict[str, str] = {}
    byte_sizes: dict[str, int] = {}
    for filename, payload in bundle.ordered_payloads():
        written = (workspace / filename).read_bytes()
        if written != payload:
            raise FormalGenerationError(f"read-back mismatch for {filename!r}")
        digests[filename] = sha256_of_bytes(written)
        byte_sizes[filename] = len(written)

    verify_bundle(bundle)
    # Derived here, after the protected mutation boundary, and deliberately not
    # between _reverify_repository_identity and the first mkdir: no manifest
    # construction, serialization, digest or output work may widen that window
    # (review finding F2, P-C1a §8).
    manifest_identity = execution_input_manifest_identity(request.input_identity)
    return FormalGenerationResult(
        generation_identity=request.generation_identity,
        workspace=workspace,
        filenames=ARTIFACT_FILENAMES,
        digests=digests,
        byte_sizes=byte_sizes,
        split_fingerprint=bundle.split_fingerprint,
        execution_input_manifest_sha256=manifest_identity.sha256,
        execution_input_manifest_byte_size=manifest_identity.byte_size,
    )


def _verify_inventory(workspace: Path) -> dict[str, bytes]:
    """Return the seven artifact payloads, refusing any other workspace shape."""
    if workspace.is_symlink() or not workspace.is_dir():
        raise FormalInventoryError(f"{workspace} is not a completed generation workspace")
    present = sorted(entry.name for entry in workspace.iterdir())
    if present != sorted(ARTIFACT_FILENAMES):
        missing = sorted(set(ARTIFACT_FILENAMES) - set(present))
        unexpected = sorted(set(present) - set(ARTIFACT_FILENAMES))
        raise FormalInventoryError(
            f"workspace inventory must be exactly the seven candidate artifacts: "
            f"missing={missing}, unexpected={unexpected}"
        )
    payloads: dict[str, bytes] = {}
    for filename in ARTIFACT_FILENAMES:
        target = workspace / filename
        if target.is_symlink() or not target.is_file():
            raise FormalInventoryError(f"{filename!r} must be a regular file")
        payloads[filename] = target.read_bytes()
    return payloads


@dataclass(frozen=True, slots=True)
class _VerifiedWorkspace:
    """One completed workspace proved self-consistent from its own bytes alone.

    An instance exists only after every non-self descriptor and the authoritative
    fingerprint have been recomputed from the actual files, so possessing one is
    proof of integrity rather than a claim of it.
    """

    workspace: Path
    payloads: Mapping[str, bytes]
    split_fingerprint: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "payloads", MappingProxyType(dict(self.payloads)))


def _decode(payload: bytes, *, workspace: Path, filename: str) -> str:
    if payload.startswith(b"\xef\xbb\xbf"):
        raise FormalInputSchemaError(
            f"{workspace}: {filename} must not begin with a byte-order mark"
        )
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise FormalInputSchemaError(f"{workspace}: {filename} is not valid UTF-8") from error


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise FormalInputSchemaError(f"duplicate JSON object key: {key!r}")
        seen.add(key)
    return dict(pairs)


def _read_json_object(
    payloads: Mapping[str, bytes], filename: str, *, workspace: Path
) -> Mapping[str, object]:
    text = _decode(payloads[filename], workspace=workspace, filename=filename)
    try:
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except FormalInputSchemaError:
        raise
    except ValueError as error:
        raise FormalInputSchemaError(f"{workspace}: {filename} is not valid JSON") from error
    if not isinstance(value, dict):
        raise FormalInputSchemaError(f"{workspace}: {filename} must be a JSON object")
    return value


def _read_jsonl_records(
    payloads: Mapping[str, bytes], filename: str, *, workspace: Path
) -> tuple[Mapping[str, object], ...]:
    text = _decode(payloads[filename], workspace=workspace, filename=filename)
    if text == "" or not text.endswith("\n") or "\r" in text:
        raise FormalInputSchemaError(
            f"{workspace}: {filename} must be non-empty and line-feed terminated"
        )
    records: list[Mapping[str, object]] = []
    for index, line in enumerate(text[:-1].split("\n")):
        if line.strip() == "":
            raise FormalInputSchemaError(f"{workspace}: {filename} record {index} is blank")
        try:
            value = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except FormalInputSchemaError:
            raise
        except ValueError as error:
            raise FormalInputSchemaError(
                f"{workspace}: {filename} record {index} is not valid JSON"
            ) from error
        if not isinstance(value, dict):
            raise FormalInputSchemaError(
                f"{workspace}: {filename} record {index} must be a JSON object"
            )
        records.append(value)
    return tuple(records)


def _require_declared_schema(
    document: Mapping[str, object], filename: str, *, workspace: Path
) -> None:
    expected = ARTIFACT_FILE_SCHEMAS[filename]
    if document.get("schema_version") != expected:
        raise FormalInputSchemaError(
            f"{workspace}: {filename} requires schema {expected!r}, "
            f"got {document.get('schema_version')!r}"
        )


def _reject_metadata(document: object, *, workspace: Path, filename: str) -> None:
    try:
        reject_forbidden_metadata(document)
    except Exception as error:  # re-typed, never suppressed
        raise FormalMetadataError(f"{workspace}: {filename}: {error}") from error


def _carrier_fingerprint(document: Mapping[str, object], filename: str, *, workspace: Path) -> str:
    value = document.get("split_fingerprint")
    if not isinstance(value, str) or len(value) != 64:
        raise FormalFingerprintError(
            f"{workspace}: {filename} carries no well-formed authoritative fingerprint"
        )
    if any(character not in _HEX_DIGITS for character in value):
        raise FormalFingerprintError(f"{workspace}: {filename} fingerprint is not lowercase hex")
    return value


def _rebuild_identity_core(
    document: Mapping[str, object], *, workspace: Path
) -> SplitSummaryIdentityCore:
    """Reconstruct the accepted identity core from the on-disk core document."""
    required = (
        "algorithm_version",
        "excluded_record_count",
        "group_counts_by_partition",
        "label_totals",
        "partition_label_matrix",
        "partition_totals",
        "schema_version",
        "total_example_count",
        "total_group_count",
    )
    if sorted(document) != sorted(required):
        raise FormalInputSchemaError(
            f"{workspace}: {SPLIT_SUMMARY_IDENTITY_CORE_FILENAME} must have exactly "
            f"{sorted(required)}, got {sorted(document)}"
        )
    try:
        return SplitSummaryIdentityCore(
            total_example_count=document["total_example_count"],  # type: ignore[arg-type]
            total_group_count=document["total_group_count"],  # type: ignore[arg-type]
            excluded_record_count=document["excluded_record_count"],  # type: ignore[arg-type]
            partition_totals=document["partition_totals"],  # type: ignore[arg-type]
            label_totals=document["label_totals"],  # type: ignore[arg-type]
            partition_label_matrix=document["partition_label_matrix"],  # type: ignore[arg-type]
            group_counts_by_partition=document["group_counts_by_partition"],  # type: ignore[arg-type]
            algorithm_version=document["algorithm_version"],  # type: ignore[arg-type]
            schema_version=document["schema_version"],  # type: ignore[arg-type]
        )
    except Exception as error:  # re-typed, never suppressed
        raise FormalInputSchemaError(
            f"{workspace}: {SPLIT_SUMMARY_IDENTITY_CORE_FILENAME} is not a valid identity core: "
            f"{error}"
        ) from error


#: The exact top-level key set produced by ``FormalGenerationManifest``. It is
#: derived from the model rather than restated, so it cannot drift from it.
_MANIFEST_TOP_LEVEL_KEYS: Final = frozenset(
    (
        "algorithm_version",
        "artifacts",
        "bundle_filenames",
        "input_identity",
        "schema_version",
        "split_fingerprint",
    )
)
_ARTIFACT_ENTRY_KEYS: Final = frozenset(
    ("byte_size", "filename", "schema_version", "sha256", "surface")
)


def _exact_object(value: object, *, label: str, keys: frozenset[str]) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise FormalInputSchemaError(f"{label} must be a JSON object")
    actual = frozenset(value)
    if actual != keys:
        missing = sorted(keys - actual)
        unknown = sorted(actual - keys)
        raise FormalInputSchemaError(
            f"{label} must have exactly {sorted(keys)}: missing={missing}, unknown={unknown}"
        )
    return value


def _exact_text(value: object, *, label: str) -> str:
    if type(value) is not str or value == "" or value.strip() != value:
        raise FormalInputSchemaError(f"{label} must be a non-blank untrimmed string")
    return value


def _exact_size(value: object, *, label: str) -> int:
    # ``type(...) is int`` rejects ``bool`` and every ``int`` subclass; a JSON
    # float decodes to ``float`` and is rejected by the same test.
    if type(value) is not int or value < 0:
        raise FormalInputSchemaError(f"{label} must be a non-negative integer, got {value!r}")
    return value


def _rebuild_input_identity(value: object, *, workspace: Path) -> FormalSplitInputIdentity:
    """Rebuild the manifest's input identity through the immutable formal type."""
    label = f"{workspace}: manifest input_identity"
    if not isinstance(value, list):
        raise FormalInputSchemaError(f"{label} must be an array")
    descriptors: list[FormalInputDescriptor] = []
    for index, entry in enumerate(value):
        entry_label = f"{label}[{index}]"
        if not isinstance(entry, dict):
            raise FormalInputSchemaError(f"{entry_label} must be a JSON object")
        surface = entry.get("surface")
        if surface not in REQUIRED_INPUT_SURFACES:
            raise FormalInputSchemaError(f"{entry_label}.surface is unknown: {surface!r}")
        expected_keys = {"byte_size", "sha256", "surface"}
        if surface in INPUT_SCHEMA_VERSIONS:
            expected_keys.add("schema_version")
        _exact_object(entry, label=entry_label, keys=frozenset(expected_keys))
        # The accepted descriptor type reports a bad digest or byte size as an
        # input-identity failure. Inside manifest validation the defect is a
        # malformed manifest document, so it is re-typed to the schema identity
        # the F3 contract assigns to manifest-structure failures.
        try:
            descriptors.append(
                FormalInputDescriptor(
                    surface=_exact_text(surface, label=f"{entry_label}.surface"),
                    schema_version=(
                        _exact_text(
                            entry.get("schema_version"), label=f"{entry_label}.schema_version"
                        )
                        if surface in INPUT_SCHEMA_VERSIONS
                        else None
                    ),
                    sha256=_exact_text(entry.get("sha256"), label=f"{entry_label}.sha256"),
                    byte_size=_exact_size(entry.get("byte_size"), label=f"{entry_label}.byte_size"),
                )
            )
        except FormalInputSchemaError:
            raise
        except Exception as error:  # re-typed, never suppressed
            raise FormalInputSchemaError(f"{entry_label} is invalid: {error}") from error
    try:
        return FormalSplitInputIdentity(descriptors=tuple(descriptors))
    except FormalInputSchemaError:
        raise
    except Exception as error:  # re-typed, never suppressed
        raise FormalInputSchemaError(
            f"{label} is not the exact formal input-identity structure: {error}"
        ) from error


def _verify_manifest_contract(
    manifest: Mapping[str, object], payloads: Mapping[str, bytes], *, workspace: Path
) -> None:
    """Reconstruct the manifest and require its canonical bytes to match exactly.

    The pure ``FormalGenerationManifest`` model and the accepted canonical
    serializer are the single source of truth, so no second hand-maintained
    schema can drift from the builder.  Because the regenerated bytes must equal
    the on-disk bytes exactly, an additional innocuous key, a missing key, a
    different spelling, a changed ``algorithm_version`` or any non-canonical
    serialization is refused — including when both workspaces carry the same
    altered bytes.
    """
    _exact_object(
        manifest, label=f"{workspace}: manifest", keys=frozenset(_MANIFEST_TOP_LEVEL_KEYS)
    )
    bundle_filenames = manifest.get("bundle_filenames")
    if not isinstance(bundle_filenames, list) or any(
        type(name) is not str for name in bundle_filenames
    ):
        raise FormalInputSchemaError(f"{workspace}: manifest bundle_filenames must be strings")
    raw_artifacts = manifest.get("artifacts")
    if not isinstance(raw_artifacts, list):
        raise FormalInputSchemaError(f"{workspace}: manifest artifacts must be an array")

    entries: list[FormalArtifactEntry] = []
    for index, entry in enumerate(raw_artifacts):
        label = f"{workspace}: manifest artifacts[{index}]"
        _exact_object(entry, label=label, keys=_ARTIFACT_ENTRY_KEYS)
        assert isinstance(entry, dict)  # narrowed by _exact_object
        entries.append(
            FormalArtifactEntry(
                filename=_exact_text(entry.get("filename"), label=f"{label}.filename"),
                surface=_exact_text(entry.get("surface"), label=f"{label}.surface"),
                schema_version=_exact_text(
                    entry.get("schema_version"), label=f"{label}.schema_version"
                ),
                sha256=_exact_text(entry.get("sha256"), label=f"{label}.sha256"),
                byte_size=_exact_size(entry.get("byte_size"), label=f"{label}.byte_size"),
            )
        )

    identity = _rebuild_input_identity(manifest.get("input_identity"), workspace=workspace)
    try:
        rebuilt = FormalGenerationManifest(
            schema_version=_exact_text(
                manifest.get("schema_version"), label=f"{workspace}: manifest schema_version"
            ),
            algorithm_version=_exact_text(
                manifest.get("algorithm_version"), label=f"{workspace}: manifest algorithm_version"
            ),
            bundle_filenames=tuple(bundle_filenames),
            artifacts=tuple(entries),
            input_identity=identity,
            split_fingerprint=_exact_text(
                manifest.get("split_fingerprint"), label=f"{workspace}: manifest split_fingerprint"
            ),
        )
    except FormalInventoryError:
        # An inventory-shaped refusal keeps its own identity: a manifest that
        # lists the wrong bundle or describes itself is an inventory failure,
        # not a schema failure.
        raise
    except FormalInputSchemaError:
        raise
    except Exception as error:  # re-typed, never suppressed
        raise FormalInputSchemaError(
            f"{workspace}: manifest does not satisfy the formal manifest contract: {error}"
        ) from error

    if rebuilt.algorithm_version != ALGORITHM_VERSION:  # pragma: no cover - model enforces this
        raise FormalInputSchemaError(
            f"{workspace}: manifest algorithm_version must be {ALGORITHM_VERSION!r}"
        )
    if rebuilt.canonical_bytes() != payloads[GENERATION_MANIFEST_FILENAME]:
        raise FormalInputSchemaError(
            f"{workspace}: {GENERATION_MANIFEST_FILENAME} is not the canonical serialization of "
            "the formal manifest it decodes to"
        )


def _verify_manifest_descriptors(
    manifest: Mapping[str, object], payloads: Mapping[str, bytes], *, workspace: Path
) -> None:
    """Recompute every non-self digest and byte size from the actual file bytes."""
    bundle_filenames = manifest.get("bundle_filenames")
    if not isinstance(bundle_filenames, list) or tuple(bundle_filenames) != ARTIFACT_FILENAMES:
        raise FormalInventoryError(
            f"{workspace}: manifest must list exactly {list(ARTIFACT_FILENAMES)}, "
            f"got {bundle_filenames!r}"
        )
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise FormalInputSchemaError(f"{workspace}: manifest artifacts must be an array")
    described = tuple(
        entry.get("filename") if isinstance(entry, dict) else None for entry in artifacts
    )
    if described != MANIFEST_DIGESTED_FILENAMES:
        raise FormalInventoryError(
            f"{workspace}: manifest must describe exactly {list(MANIFEST_DIGESTED_FILENAMES)}, "
            f"got {list(described)}"
        )
    if any(entry.get("filename") == GENERATION_MANIFEST_FILENAME for entry in artifacts):
        raise FormalInventoryError(f"{workspace}: the manifest must not describe itself")

    for entry in artifacts:
        filename = entry["filename"]
        payload = payloads[filename]
        actual_digest = sha256_of_bytes(payload)
        actual_size = len(payload)
        if entry.get("sha256") != actual_digest:
            raise FormalFingerprintError(
                f"{workspace}: descriptor digest for {filename!r} is "
                f"{entry.get('sha256')!r}, recomputed {actual_digest!r}"
            )
        if entry.get("byte_size") != actual_size:
            raise FormalFingerprintError(
                f"{workspace}: descriptor byte size for {filename!r} is "
                f"{entry.get('byte_size')!r}, recomputed {actual_size}"
            )
        if entry.get("surface") != ARTIFACT_SURFACES[filename]:
            raise FormalInputSchemaError(
                f"{workspace}: descriptor surface for {filename!r} is {entry.get('surface')!r}"
            )
        if entry.get("schema_version") != ARTIFACT_FILE_SCHEMAS[filename]:
            raise FormalInputSchemaError(
                f"{workspace}: descriptor schema for {filename!r} is "
                f"{entry.get('schema_version')!r}"
            )


def _verify_completed_workspace(workspace: Path) -> _VerifiedWorkspace:
    """Prove one completed workspace self-consistent from its own bytes. Never writes.

    Byte equality between two workspaces proves only that they agree, not that
    either is a valid bundle, so this runs independently against each workspace
    before any comparison is attempted (review finding F1).
    """
    if not isinstance(workspace, Path):
        raise FormalInventoryError("a workspace must be a path")
    resolved = workspace.resolve()
    payloads = _verify_inventory(resolved)

    policy = _read_json_object(payloads, SPLIT_POLICY_FILENAME, workspace=resolved)
    _require_declared_schema(policy, SPLIT_POLICY_FILENAME, workspace=resolved)
    _reject_metadata(policy, workspace=resolved, filename=SPLIT_POLICY_FILENAME)

    ledger = _read_json_object(payloads, EXCLUDED_LEDGER_FILENAME, workspace=resolved)
    _require_declared_schema(ledger, EXCLUDED_LEDGER_FILENAME, workspace=resolved)
    _reject_metadata(ledger, workspace=resolved, filename=EXCLUDED_LEDGER_FILENAME)

    for filename in (GROUP_REGISTRY_FILENAME, EXAMPLE_REGISTRY_FILENAME):
        records = _read_jsonl_records(payloads, filename, workspace=resolved)
        expected_schema = ARTIFACT_FILE_SCHEMAS[filename]
        for index, record in enumerate(records):
            if record.get("schema_version") != expected_schema:
                raise FormalInputSchemaError(
                    f"{resolved}: {filename} record {index} requires schema {expected_schema!r}"
                )

    core_document = _read_json_object(
        payloads, SPLIT_SUMMARY_IDENTITY_CORE_FILENAME, workspace=resolved
    )
    _require_declared_schema(
        core_document, SPLIT_SUMMARY_IDENTITY_CORE_FILENAME, workspace=resolved
    )
    _reject_metadata(
        core_document, workspace=resolved, filename=SPLIT_SUMMARY_IDENTITY_CORE_FILENAME
    )
    core = _rebuild_identity_core(core_document, workspace=resolved)

    summary = _read_json_object(payloads, SPLIT_SUMMARY_FILENAME, workspace=resolved)
    _require_declared_schema(summary, SPLIT_SUMMARY_FILENAME, workspace=resolved)

    manifest = _read_json_object(payloads, GENERATION_MANIFEST_FILENAME, workspace=resolved)
    _require_declared_schema(manifest, GENERATION_MANIFEST_FILENAME, workspace=resolved)
    if manifest.get("schema_version") != GENERATION_MANIFEST_SCHEMA:  # pragma: no cover - as above
        raise FormalInputSchemaError(f"{resolved}: manifest schema is wrong")
    _reject_metadata(manifest, workspace=resolved, filename=GENERATION_MANIFEST_FILENAME)

    # The complete manifest contract, not merely its non-prohibited fields: the
    # document is reconstructed through the pure manifest model and its canonical
    # bytes regenerated, so an altered algorithm version, an unknown key, a
    # missing key or any non-canonical shape is refused even when A and B carry
    # identical bytes (review finding F3).
    _verify_manifest_contract(manifest, payloads, workspace=resolved)
    _verify_manifest_descriptors(manifest, payloads, workspace=resolved)

    # The accepted fingerprint layer digests the core it is handed, so the core
    # must first be proved to re-serialize to exactly the bytes on disk.
    if core.canonical_bytes() != payloads[SPLIT_SUMMARY_IDENTITY_CORE_FILENAME]:
        raise FormalFingerprintError(
            f"{resolved}: {SPLIT_SUMMARY_IDENTITY_CORE_FILENAME} does not re-serialize to its "
            "own canonical bytes"
        )
    try:
        identity = build_split_fingerprint_identity(
            policy_id=SPLIT_POLICY_SCHEMA,
            algorithm_version=ALGORITHM_VERSION,
            split_seed=SPLIT_SEED,
            group_registry_payload=payloads[GROUP_REGISTRY_FILENAME],
            example_registry_payload=payloads[EXAMPLE_REGISTRY_FILENAME],
            excluded_ledger_payload=payloads[EXCLUDED_LEDGER_FILENAME],
            split_summary_identity_core=core,
        )
        fingerprint_record = build_split_fingerprint_record(identity)
        verify_split_fingerprint_record(fingerprint_record)
    except Exception as error:  # re-typed, never suppressed
        raise FormalFingerprintError(
            f"{resolved}: authoritative fingerprint could not be reconstructed: {error}"
        ) from error
    recomputed = fingerprint_record.split_fingerprint

    summary_carrier = _carrier_fingerprint(summary, SPLIT_SUMMARY_FILENAME, workspace=resolved)
    manifest_carrier = _carrier_fingerprint(
        manifest, GENERATION_MANIFEST_FILENAME, workspace=resolved
    )
    if summary_carrier != manifest_carrier:
        raise FormalFingerprintError(
            f"{resolved}: split summary and manifest carry different fingerprints"
        )
    if recomputed != summary_carrier:
        raise FormalFingerprintError(
            f"{resolved}: {SPLIT_SUMMARY_FILENAME} carries {summary_carrier!r}, "
            f"recomputed {recomputed!r}"
        )
    if recomputed != manifest_carrier:  # pragma: no cover - equality with the summary implies this
        raise FormalFingerprintError(
            f"{resolved}: {GENERATION_MANIFEST_FILENAME} carries {manifest_carrier!r}, "
            f"recomputed {recomputed!r}"
        )
    return _VerifiedWorkspace(workspace=resolved, payloads=payloads, split_fingerprint=recomputed)


def compare(workspace_a: Path, workspace_b: Path) -> FormalComparisonResult:
    """Verify each workspace independently, then compare byte-for-byte. Never writes."""
    if not isinstance(workspace_a, Path) or not isinstance(workspace_b, Path):
        raise FormalInventoryError("compare requires two workspace paths")
    resolved_a = workspace_a.resolve()
    resolved_b = workspace_b.resolve()
    if resolved_a == resolved_b:
        raise FormalInventoryError("comparison requires two distinct generation workspaces")

    # Complete independent integrity verification precedes any equality question,
    # so two identically corrupted workspaces fail before an equality disposition
    # can be produced (review finding F1).
    verified_a = _verify_completed_workspace(resolved_a)
    verified_b = _verify_completed_workspace(resolved_b)

    unequal: list[str] = []
    equal: list[str] = []
    for filename in ARTIFACT_FILENAMES:
        if verified_a.payloads[filename] == verified_b.payloads[filename]:
            equal.append(filename)
        else:
            unequal.append(filename)
    if unequal:
        raise FormalByteEqualityError(
            "Generation A and Generation B are not byte-identical; both candidates are "
            f"invalidated. Differing artifacts: {unequal}"
        )
    if verified_a.split_fingerprint != verified_b.split_fingerprint:
        raise FormalFingerprintError(  # pragma: no cover - byte equality already implies this
            "recomputed authoritative fingerprints disagree"
        )
    return FormalComparisonResult(
        workspace_a=resolved_a,
        workspace_b=resolved_b,
        filenames=ARTIFACT_FILENAMES,
        equal_filenames=tuple(equal),
        split_fingerprint=verified_a.split_fingerprint,
        equal=True,
    )


def input_surface_order() -> Sequence[str]:
    """Return the required formal input surfaces in canonical order."""
    return sorted(REQUIRED_INPUT_SURFACES)
