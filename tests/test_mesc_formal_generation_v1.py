"""Synthetic qualification of the P01-04D filesystem, write-once and comparison layer.

Every workspace, repository and input in this module is synthetic and lives under
``tmp_path``.  The identifiers ``A`` and ``B`` exercise the implemented contracts
only; they are not formal P01-04D Generation A or Generation B, and no protected
registry, external source-record file or real dataset is read anywhere here.
"""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from medscale.mesc._formal_generation_v1 import (
    FormalComparisonResult,
    FormalGenerationResult,
    FormalSplitRequest,
    build_request,
    compare,
    generate,
    resolve_repository_commit,
    running_python_version,
)
from medscale.mesc._formal_split_v1 import (
    ARTIFACT_FILENAMES,
    GENERATION_MANIFEST_FILENAME,
    SPLIT_POLICY_FILENAME,
    FormalByteEqualityError,
    FormalEvidenceConfigurationError,
    FormalFingerprintError,
    FormalGenerationError,
    FormalInputIdentityError,
    FormalInputSchemaError,
    FormalInventoryError,
    FormalLabelJoinError,
    FormalMetadataError,
    FormalWorkspaceSafetyError,
)
from test_mesc_formal_split_v1 import write_synthetic_inputs

SYNTHETIC_COMMIT = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"


def make_repository(root: Path, commit: str = SYNTHETIC_COMMIT) -> Path:
    """Create a minimal synthetic Git repository checked out at ``commit``."""
    root.mkdir(parents=True, exist_ok=True)
    git_dir = root / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text(f"{commit}\n", encoding="utf-8")
    return root.resolve()


def make_environment(tmp_path: Path) -> dict[str, Path]:
    """Create a synthetic repository, evidence roots and inputs under ``tmp_path``."""
    repository = make_repository(tmp_path / "repo")
    inputs = write_synthetic_inputs(tmp_path / "inputs")
    external = tmp_path / "external-evidence"
    future = tmp_path / "future-evidence"
    external.mkdir()
    future.mkdir()
    return {
        "repository": repository,
        "external": external.resolve(),
        "future": future.resolve(),
        **{f"input:{surface}": location for surface, location in inputs.items()},
    }


def input_locations(environment: Mapping[str, Path]) -> dict[str, Path]:
    return {
        key.split(":", 1)[1]: value
        for key, value in environment.items()
        if key.startswith("input:")
    }


def make_request(
    tmp_path: Path,
    environment: Mapping[str, Path],
    *,
    generation: str = "A",
    workspace_name: str = "workspace-a",
    expected_commit: str = SYNTHETIC_COMMIT,
    python_version: str | None = None,
    workspace: Path | None = None,
    future_root: Path | None = None,
) -> FormalSplitRequest:
    return build_request(
        expected_canonical_commit=expected_commit,
        repository_root=environment["repository"],
        generation_identity=generation,
        workspace=workspace if workspace is not None else (tmp_path / workspace_name),
        external_evidence_root=environment["external"],
        future_evidence_root=future_root if future_root is not None else environment["future"],
        input_locations=input_locations(environment),
        python_version=python_version or running_python_version(),
    )


@pytest.fixture
def environment(tmp_path: Path) -> dict[str, Path]:
    return make_environment(tmp_path)


# ---------------------------------------------------------------------------
# Typed error identities
# ---------------------------------------------------------------------------


def test_all_ten_typed_error_identities_exist_and_fail_closed() -> None:
    errors = (
        FormalInputIdentityError,
        FormalInputSchemaError,
        FormalLabelJoinError,
        FormalWorkspaceSafetyError,
        FormalGenerationError,
        FormalInventoryError,
        FormalByteEqualityError,
        FormalFingerprintError,
        FormalMetadataError,
        FormalEvidenceConfigurationError,
    )
    assert len({error.__name__ for error in errors}) == 10
    for error in errors:
        assert issubclass(error, Exception)
        assert not issubclass(error, Warning)
        bases = [base for base in error.__mro__[1:] if base is not object]
        assert bases[0].__name__ == "_FormalContractError"


@pytest.mark.parametrize(
    "cls", [FormalSplitRequest, FormalGenerationResult, FormalComparisonResult]
)
def test_generation_dataclasses_are_frozen_and_slotted(cls: type) -> None:
    assert dataclasses.is_dataclass(cls)
    assert cls.__dataclass_params__.frozen  # type: ignore[attr-defined]
    assert "__slots__" in cls.__dict__


def test_request_snapshots_caller_mapping(tmp_path: Path, environment: dict[str, Path]) -> None:
    locations = input_locations(environment)
    request = build_request(
        expected_canonical_commit=SYNTHETIC_COMMIT,
        repository_root=environment["repository"],
        generation_identity="A",
        workspace=tmp_path / "ws",
        external_evidence_root=environment["external"],
        future_evidence_root=environment["future"],
        input_locations=locations,
        python_version=running_python_version(),
    )
    locations.clear()
    assert len(request.input_locations) == 5
    with pytest.raises(TypeError):
        request.input_locations["x"] = tmp_path  # type: ignore[index]


# ---------------------------------------------------------------------------
# Pre-mutation validation
# ---------------------------------------------------------------------------


def test_expected_commit_mismatch_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    with pytest.raises(FormalInputIdentityError, match="not the expected"):
        make_request(tmp_path, environment, expected_commit="f" * 40)
    assert not (tmp_path / "workspace-a").exists()


def test_malformed_expected_commit_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    with pytest.raises(FormalInputIdentityError):
        make_request(tmp_path, environment, expected_commit="abc")


def test_missing_repository_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    environment = dict(environment)
    environment["repository"] = (tmp_path / "not-a-repo").resolve()
    (tmp_path / "not-a-repo").mkdir()
    with pytest.raises(FormalInputIdentityError, match="not a Git repository"):
        make_request(tmp_path, environment)


def test_python_version_mismatch_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    with pytest.raises(FormalInputIdentityError, match="interpreter"):
        make_request(tmp_path, environment, python_version="0.0.0")


def test_unknown_generation_identity_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    with pytest.raises(FormalGenerationError, match="generation identity"):
        make_request(tmp_path, environment, generation="C")


def test_workspace_reuse_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    existing = tmp_path / "workspace-a"
    existing.mkdir()
    with pytest.raises(FormalWorkspaceSafetyError, match="already exists"):
        make_request(tmp_path, environment)


def test_repository_root_output_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    with pytest.raises(FormalWorkspaceSafetyError, match="outside the repository root"):
        make_request(tmp_path, environment, workspace=environment["repository"] / "candidate")


def test_nested_repository_output_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    nested = environment["repository"] / "deep" / "candidate"
    nested.parent.mkdir(parents=True)
    with pytest.raises(FormalWorkspaceSafetyError, match="outside the repository root"):
        make_request(tmp_path, environment, workspace=nested)


def test_p01_03g_output_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    protected = environment["repository"] / "specs" / "mesc-pilot-01" / "p01-03g"
    protected.mkdir(parents=True)
    with pytest.raises(FormalWorkspaceSafetyError):
        make_request(tmp_path, environment, workspace=protected / "candidate")


def test_future_evidence_root_output_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    with pytest.raises(FormalEvidenceConfigurationError, match="future evidence root"):
        make_request(tmp_path, environment, workspace=environment["future"] / "candidate")


def test_external_evidence_root_output_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    with pytest.raises(FormalEvidenceConfigurationError, match="external evidence root"):
        make_request(tmp_path, environment, workspace=environment["external"])


def test_relative_or_unresolved_roots_are_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    with pytest.raises(FormalWorkspaceSafetyError, match="absolute"):
        build_request(
            expected_canonical_commit=SYNTHETIC_COMMIT,
            repository_root=Path("relative-repo"),
            generation_identity="A",
            workspace=tmp_path / "ws",
            external_evidence_root=environment["external"],
            future_evidence_root=environment["future"],
            input_locations=input_locations(environment),
            python_version=running_python_version(),
        )
    with pytest.raises(FormalWorkspaceSafetyError, match="absolute"):
        make_request(tmp_path, environment, workspace=Path("relative-workspace"))


def test_protected_root_alias_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    """A `..` traversal that lands inside a protected root must be refused."""
    protected = environment["repository"] / "specs" / "mesc-pilot-01" / "p01-03g"
    protected.mkdir(parents=True)
    alias = tmp_path / "elsewhere" / ".." / "repo" / "specs" / "mesc-pilot-01" / "p01-03g" / "out"
    (tmp_path / "elsewhere").mkdir()
    with pytest.raises(FormalWorkspaceSafetyError):
        make_request(tmp_path, environment, workspace=alias)


def test_sibling_prefix_workspace_is_allowed(tmp_path: Path, environment: dict[str, Path]) -> None:
    """`repo-backup` shares a string prefix with `repo` but is not inside it."""
    sibling = tmp_path / "repo-backup"
    request = make_request(tmp_path, environment, workspace=sibling)
    assert request.workspace == sibling.resolve()


def test_missing_input_file_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    environment = dict(environment)
    environment["input:source_records"] = (tmp_path / "absent.jsonl").resolve()
    with pytest.raises(FormalInputIdentityError, match="existing regular file"):
        make_request(tmp_path, environment)


def test_no_mutation_occurs_before_validation_passes(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    workspace = tmp_path / "never-created"
    with pytest.raises(FormalInputIdentityError):
        make_request(tmp_path, environment, workspace=workspace, expected_commit="0" * 40)
    assert not workspace.exists()


def test_corrupted_input_fails_before_workspace_creation(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    request = make_request(tmp_path, environment)
    request.input_locations["source_records"].write_bytes(b"tampered\n")
    with pytest.raises(FormalInputIdentityError):
        generate(request)
    assert not request.workspace.exists()


# ---------------------------------------------------------------------------
# Write semantics
# ---------------------------------------------------------------------------


def test_generation_writes_exactly_seven_regular_files(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    result = generate(make_request(tmp_path, environment))
    assert sorted(entry.name for entry in result.workspace.iterdir()) == sorted(ARTIFACT_FILENAMES)
    assert len(list(result.workspace.iterdir())) == 7
    for filename in ARTIFACT_FILENAMES:
        target = result.workspace / filename
        assert target.is_file()
        assert not target.is_symlink()
        assert result.digests[filename]
        assert result.byte_sizes[filename] == len(target.read_bytes())
    assert len(result.split_fingerprint) == 64
    assert result.generation_identity == "A"


def test_generation_never_overwrites(tmp_path: Path, environment: dict[str, Path]) -> None:
    request = make_request(tmp_path, environment)
    generate(request)
    with pytest.raises(FormalWorkspaceSafetyError, match="already exists"):
        generate(request)


def test_read_back_verification_detects_a_short_write(
    tmp_path: Path, environment: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    request = make_request(tmp_path, environment)
    original = Path.read_bytes

    def truncated(self: Path) -> bytes:
        payload = original(self)
        if self.name == SPLIT_POLICY_FILENAME and self.parent == request.workspace:
            return payload[:-1]
        return payload

    monkeypatch.setattr(Path, "read_bytes", truncated)
    with pytest.raises(FormalGenerationError, match="read-back mismatch"):
        generate(request)


def test_inventory_rejects_extra_and_missing_files(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    result = generate(make_request(tmp_path, environment))
    other = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    (result.workspace / "unexpected.txt").write_text("x", encoding="utf-8")
    with pytest.raises(FormalInventoryError, match="unexpected"):
        compare(result.workspace, other.workspace)
    (result.workspace / "unexpected.txt").unlink()
    (result.workspace / SPLIT_POLICY_FILENAME).unlink()
    with pytest.raises(FormalInventoryError, match="missing"):
        compare(result.workspace, other.workspace)


def test_failed_workspace_cannot_be_treated_as_completed(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    partial = tmp_path / "partial"
    partial.mkdir()
    (partial / SPLIT_POLICY_FILENAME).write_bytes(b"{}\n")
    complete = generate(make_request(tmp_path, environment))
    with pytest.raises(FormalInventoryError):
        compare(partial, complete.workspace)


def test_non_directory_workspace_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    plain = tmp_path / "plain-file"
    plain.write_text("x", encoding="utf-8")
    complete = generate(make_request(tmp_path, environment))
    with pytest.raises(FormalInventoryError, match="not a completed generation workspace"):
        compare(plain, complete.workspace)


def test_symlinked_artifact_is_rejected(tmp_path: Path, environment: dict[str, Path]) -> None:
    first = generate(make_request(tmp_path, environment))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    target = second.workspace / SPLIT_POLICY_FILENAME
    payload = target.read_bytes()
    elsewhere = tmp_path / "linked-policy.json"
    elsewhere.write_bytes(payload)
    target.unlink()
    try:
        target.symlink_to(elsewhere)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not permitted on this platform")
    with pytest.raises(FormalInventoryError, match="regular file"):
        compare(first.workspace, second.workspace)


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------


def test_identical_synthetic_workspaces_compare_equal(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    assert first.split_fingerprint == second.split_fingerprint
    result = compare(first.workspace, second.workspace)
    assert result.equal is True
    assert result.filenames == ARTIFACT_FILENAMES
    assert len(result.equal_filenames) == 7
    assert result.split_fingerprint == first.split_fingerprint
    for filename in ARTIFACT_FILENAMES:
        assert (first.workspace / filename).read_bytes() == (
            second.workspace / filename
        ).read_bytes()


def test_altered_byte_invalidates_both_candidates(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    target = second.workspace / SPLIT_POLICY_FILENAME
    target.write_bytes(target.read_bytes().replace(b"none", b"NONE"))
    with pytest.raises(FormalByteEqualityError, match="invalidated"):
        compare(first.workspace, second.workspace)


def test_comparison_performs_zero_writes(tmp_path: Path, environment: dict[str, Path]) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))

    def snapshot(workspace: Path) -> dict[str, bytes]:
        return {entry.name: entry.read_bytes() for entry in sorted(workspace.iterdir())}

    before = (snapshot(first.workspace), snapshot(second.workspace))
    compare(first.workspace, second.workspace)
    assert (snapshot(first.workspace), snapshot(second.workspace)) == before
    assert len(list(first.workspace.iterdir())) == 7
    assert len(list(second.workspace.iterdir())) == 7


def test_comparison_requires_two_distinct_workspaces(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment))
    with pytest.raises(FormalInventoryError, match="distinct"):
        compare(first.workspace, first.workspace)


def test_comparison_recomputes_the_fingerprint(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    for workspace in (first.workspace, second.workspace):
        manifest = json.loads((workspace / GENERATION_MANIFEST_FILENAME).read_bytes())
        manifest["split_fingerprint"] = "0" * 64
        (workspace / GENERATION_MANIFEST_FILENAME).write_text(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8"
        )
    with pytest.raises(FormalFingerprintError, match="different fingerprints"):
        compare(first.workspace, second.workspace)


def test_manifest_verification_detects_a_missing_fingerprint(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    (first.workspace / GENERATION_MANIFEST_FILENAME).write_text("{}\n", encoding="utf-8")
    with pytest.raises(FormalFingerprintError, match="no authoritative fingerprint"):
        compare(first.workspace, second.workspace)


def test_generated_manifest_carries_no_runtime_metadata(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    result = generate(make_request(tmp_path, environment))
    manifest_text = (result.workspace / GENERATION_MANIFEST_FILENAME).read_text(encoding="utf-8")
    assert str(result.workspace) not in manifest_text
    assert result.generation_identity not in json.loads(manifest_text)
    for prohibited in ("workspace", "hostname", "username", "argv", "environ", "tmp"):
        assert prohibited not in manifest_text.lower()


def test_repository_commit_resolution_supports_ref_and_gitdir(tmp_path: Path) -> None:
    root = tmp_path / "ref-repo"
    root.mkdir()
    git_dir = root / ".git"
    (git_dir / "refs" / "heads").mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git_dir / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")
    assert resolve_repository_commit(root.resolve()) == SYNTHETIC_COMMIT

    linked = tmp_path / "linked-repo"
    linked.mkdir()
    (linked / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
    assert resolve_repository_commit(linked.resolve()) == SYNTHETIC_COMMIT


def test_repository_commit_resolution_supports_packed_refs(tmp_path: Path) -> None:
    root = tmp_path / "packed-repo"
    root.mkdir()
    git_dir = root / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git_dir / "packed-refs").write_text(
        f"# pack-refs with: peeled\n{SYNTHETIC_COMMIT} refs/heads/main\n", encoding="utf-8"
    )
    assert resolve_repository_commit(root.resolve()) == SYNTHETIC_COMMIT


def test_unresolvable_reference_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "broken-repo"
    root.mkdir()
    git_dir = root / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/absent\n", encoding="utf-8")
    with pytest.raises(FormalInputIdentityError, match="could not be resolved"):
        resolve_repository_commit(root.resolve())


def test_generate_requires_an_exact_request(tmp_path: Path) -> None:
    with pytest.raises(FormalGenerationError, match="exact FormalSplitRequest"):
        generate(object())  # type: ignore[arg-type]


def test_synthetic_inputs_never_reference_protected_locations(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    for surface, location in input_locations(environment).items():
        assert tmp_path in location.parents
        assert "p01-03g" not in str(location)
        assert surface in {
            "ordered_example_registry",
            "source_document_registry",
            "transformed_dataset_identity",
            "source_records",
            "decision_record",
        }
