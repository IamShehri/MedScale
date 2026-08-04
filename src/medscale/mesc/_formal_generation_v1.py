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

import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Final

from medscale.mesc._canonical_json_v1 import sha256_of_bytes
from medscale.mesc._formal_split_v1 import (
    ARTIFACT_FILENAMES,
    DECISION_RECORD_SURFACE,
    GENERATION_IDENTITIES,
    GENERATION_MANIFEST_FILENAME,
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    REQUIRED_INPUT_SURFACES,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    SOURCE_RECORDS_SURFACE,
    SPLIT_SUMMARY_FILENAME,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
    FormalArtifactBundle,
    FormalByteEqualityError,
    FormalEvidenceConfigurationError,
    FormalFingerprintError,
    FormalGenerationError,
    FormalInputIdentityError,
    FormalInventoryError,
    FormalSplitInputIdentity,
    FormalWorkspaceSafetyError,
    allocate_formal_groups,
    build_formal_bundle,
    build_input_identity,
    join_formal_examples,
    parse_ordered_example_registry,
    parse_source_document_registry,
    parse_source_records,
    parse_transformed_dataset_identity,
    verify_bundle,
    verify_input_digest,
)

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


def generate(request: FormalSplitRequest) -> FormalGenerationResult:
    """Execute exactly one generation. Every check completes before any mutation."""
    if not isinstance(request, FormalSplitRequest):
        raise FormalGenerationError("generate requires an exact FormalSplitRequest")
    bundle = build_bundle_for_request(request)
    _validate_workspace_safety(request)

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
    return FormalGenerationResult(
        generation_identity=request.generation_identity,
        workspace=workspace,
        filenames=ARTIFACT_FILENAMES,
        digests=digests,
        byte_sizes=byte_sizes,
        split_fingerprint=bundle.split_fingerprint,
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


def _fingerprint_of(payloads: Mapping[str, bytes], workspace: Path) -> str:
    summary = payloads[SPLIT_SUMMARY_FILENAME].decode("utf-8")
    manifest = payloads[GENERATION_MANIFEST_FILENAME].decode("utf-8")
    marker = '"split_fingerprint":"'
    start = manifest.find(marker)
    if start < 0:
        raise FormalFingerprintError(f"{workspace}: manifest carries no authoritative fingerprint")
    begin = start + len(marker)
    fingerprint = manifest[begin : begin + 64]
    if len(fingerprint) != 64 or any(character not in _HEX_DIGITS for character in fingerprint):
        raise FormalFingerprintError(f"{workspace}: manifest fingerprint is malformed")
    if f'"split_fingerprint":"{fingerprint}"' not in summary:
        raise FormalFingerprintError(
            f"{workspace}: split summary and manifest carry different fingerprints"
        )
    return fingerprint


def compare(workspace_a: Path, workspace_b: Path) -> FormalComparisonResult:
    """Compare two completed generations byte-for-byte. It never writes."""
    if not isinstance(workspace_a, Path) or not isinstance(workspace_b, Path):
        raise FormalInventoryError("compare requires two workspace paths")
    resolved_a = workspace_a.resolve()
    resolved_b = workspace_b.resolve()
    if resolved_a == resolved_b:
        raise FormalInventoryError("comparison requires two distinct generation workspaces")

    payloads_a = _verify_inventory(resolved_a)
    payloads_b = _verify_inventory(resolved_b)
    fingerprint_a = _fingerprint_of(payloads_a, resolved_a)
    fingerprint_b = _fingerprint_of(payloads_b, resolved_b)

    unequal: list[str] = []
    equal: list[str] = []
    for filename in ARTIFACT_FILENAMES:
        if payloads_a[filename] == payloads_b[filename]:
            equal.append(filename)
        else:
            unequal.append(filename)
    if unequal:
        raise FormalByteEqualityError(
            "Generation A and Generation B are not byte-identical; both candidates are "
            f"invalidated. Differing artifacts: {unequal}"
        )
    if fingerprint_a != fingerprint_b:  # pragma: no cover - byte equality already implies this
        raise FormalFingerprintError("recomputed authoritative fingerprints disagree")
    return FormalComparisonResult(
        workspace_a=resolved_a,
        workspace_b=resolved_b,
        filenames=ARTIFACT_FILENAMES,
        equal_filenames=tuple(equal),
        split_fingerprint=fingerprint_a,
        equal=True,
    )


def input_surface_order() -> Sequence[str]:
    """Return the required formal input surfaces in canonical order."""
    return sorted(REQUIRED_INPUT_SURFACES)
