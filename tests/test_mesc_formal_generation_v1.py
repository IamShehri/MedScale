"""Synthetic qualification of the P01-04D filesystem, write-once and comparison layer.

Every workspace, repository and input in this module is synthetic and lives under
``tmp_path``.  The identifiers ``A`` and ``B`` exercise the implemented contracts
only; they are not formal P01-04D Generation A or Generation B, and no protected
registry, external source-record file or real dataset is read anywhere here.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Callable, Mapping
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
    EXAMPLE_REGISTRY_FILENAME,
    EXCLUDED_LEDGER_FILENAME,
    GENERATION_MANIFEST_FILENAME,
    GROUP_REGISTRY_FILENAME,
    SOURCE_RECORDS_SURFACE,
    SPLIT_POLICY_FILENAME,
    SPLIT_SUMMARY_FILENAME,
    SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
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
    FormalLabelJoinError,
    FormalMetadataError,
    FormalSplitInputIdentity,
    FormalWorkspaceSafetyError,
)
from medscale.mesc._split_artifacts_v1 import (
    SplitSummaryIdentityCore,
    build_split_fingerprint_identity,
    compute_split_fingerprint,
)
from medscale.mesc._split_v1 import ALGORITHM_VERSION, SPLIT_SEED
from test_mesc_formal_split_v1 import synthetic_payloads, write_synthetic_inputs

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
    """A one-sided tamper is an integrity failure, not a byte-equality disposition.

    Each workspace is now verified independently before equality is considered, so
    the tampered side fails its own descriptor check first.  Reporting this as mere
    byte inequality would understate it: the bundle is internally invalid, not
    merely different from its counterpart.
    """
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    target = second.workspace / SPLIT_POLICY_FILENAME
    target.write_bytes(target.read_bytes().replace(b"none", b"NONE"))
    with pytest.raises(FormalFingerprintError, match="descriptor digest"):
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
        # Written as bytes on purpose: text mode would translate the terminal LF
        # to CRLF on Windows, and the manifest-contract check would then reject
        # the non-canonical serialization before the carrier check is reached.
        (workspace / GENERATION_MANIFEST_FILENAME).write_bytes(
            (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        )
    with pytest.raises(FormalFingerprintError, match="different fingerprints"):
        compare(first.workspace, second.workspace)


def test_manifest_verification_detects_a_missing_fingerprint(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="ws-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="ws-b"))
    # An empty manifest object no longer reaches the fingerprint carrier check:
    # it fails the declared-schema check first, which is the mapped schema error.
    (first.workspace / GENERATION_MANIFEST_FILENAME).write_text("{}\n", encoding="utf-8")
    with pytest.raises(FormalInputSchemaError, match="requires schema"):
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


# ---------------------------------------------------------------------------
# F1 — independent completed-workspace integrity verification
#
# The independent clean-room review demonstrated that byte equality alone let a
# pair of identically corrupted workspaces compare successfully.  Comparison now
# verifies each workspace against its own bytes first, so every case below must
# fail closed before any equality disposition can be produced.
# ---------------------------------------------------------------------------


def snapshot_tree(workspace: Path) -> dict[str, bytes]:
    """Return the exact byte content of a workspace, for zero-write proofs."""
    return {entry.name: entry.read_bytes() for entry in sorted(workspace.iterdir())}


def make_pair(tmp_path: Path, environment: Mapping[str, Path]) -> tuple[Path, Path]:
    """Generate two valid synthetic workspaces from the same synthetic inputs."""
    first = generate(make_request(tmp_path, environment, generation="A", workspace_name="pair-a"))
    second = generate(make_request(tmp_path, environment, generation="B", workspace_name="pair-b"))
    return first.workspace, second.workspace


def _canonical_line(document: object) -> bytes:
    return (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _corrupt_zero_length(payload: bytes) -> bytes:
    return b""


def _corrupt_policy_field(payload: bytes) -> bytes:
    document = json.loads(payload)
    document["holdout_policy"] = "tampered"
    return _canonical_line(document)


def _corrupt_jsonl_byte(payload: bytes) -> bytes:
    lines = payload.decode("utf-8").splitlines()
    record = json.loads(lines[0])
    record["assigned_split"] = "train" if record["assigned_split"] != "train" else "test"
    lines[0] = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return ("\n".join(lines) + "\n").encode("utf-8")


def _corrupt_ledger_count(payload: bytes) -> bytes:
    document = json.loads(payload)
    document["count"] = 1
    return _canonical_line(document)


def _corrupt_core_total(payload: bytes) -> bytes:
    document = json.loads(payload)
    document["total_example_count"] = document["total_example_count"] + 1
    return _canonical_line(document)


def _corrupt_summary_hash(payload: bytes) -> bytes:
    document = json.loads(payload)
    document["split_hash"] = "0" * 16
    return _canonical_line(document)


def _corrupt_manifest_descriptor(payload: bytes) -> bytes:
    document = json.loads(payload)
    document["artifacts"][0]["sha256"] = "0" * 64
    return _canonical_line(document)


IDENTICAL_CORRUPTIONS: tuple[tuple[str, str, Callable[[bytes], bytes], type[Exception]], ...] = (
    ("policy-zero-length", SPLIT_POLICY_FILENAME, _corrupt_zero_length, FormalInputSchemaError),
    ("policy-field", SPLIT_POLICY_FILENAME, _corrupt_policy_field, FormalFingerprintError),
    ("group-registry-byte", GROUP_REGISTRY_FILENAME, _corrupt_jsonl_byte, FormalFingerprintError),
    (
        "example-registry-byte",
        EXAMPLE_REGISTRY_FILENAME,
        _corrupt_jsonl_byte,
        FormalFingerprintError,
    ),
    ("ledger-count", EXCLUDED_LEDGER_FILENAME, _corrupt_ledger_count, FormalFingerprintError),
    (
        "identity-core-total",
        SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
        _corrupt_core_total,
        FormalFingerprintError,
    ),
    ("summary-hash", SPLIT_SUMMARY_FILENAME, _corrupt_summary_hash, FormalFingerprintError),
    (
        "manifest-descriptor",
        GENERATION_MANIFEST_FILENAME,
        _corrupt_manifest_descriptor,
        FormalFingerprintError,
    ),
    (
        "manifest-zero-length",
        GENERATION_MANIFEST_FILENAME,
        _corrupt_zero_length,
        FormalInputSchemaError,
    ),
    ("registry-zero-length", GROUP_REGISTRY_FILENAME, _corrupt_zero_length, FormalInputSchemaError),
    (
        "core-zero-length",
        SPLIT_SUMMARY_IDENTITY_CORE_FILENAME,
        _corrupt_zero_length,
        FormalInputSchemaError,
    ),
    (
        "example-registry-zero-length",
        EXAMPLE_REGISTRY_FILENAME,
        _corrupt_zero_length,
        FormalInputSchemaError,
    ),
    (
        "ledger-zero-length",
        EXCLUDED_LEDGER_FILENAME,
        _corrupt_zero_length,
        FormalInputSchemaError,
    ),
    (
        "summary-zero-length",
        SPLIT_SUMMARY_FILENAME,
        _corrupt_zero_length,
        FormalInputSchemaError,
    ),
)


@pytest.mark.parametrize(
    ("label", "filename", "corrupt", "expected"),
    IDENTICAL_CORRUPTIONS,
    ids=[case[0] for case in IDENTICAL_CORRUPTIONS],
)
def test_identical_corruption_in_both_workspaces_is_rejected(
    tmp_path: Path,
    environment: dict[str, Path],
    label: str,
    filename: str,
    corrupt: Callable[[bytes], bytes],
    expected: type[Exception],
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    corrupted = corrupt((workspace_a / filename).read_bytes())
    (workspace_a / filename).write_bytes(corrupted)
    (workspace_b / filename).write_bytes(corrupted)
    # The pair stays byte-identical, which is exactly what the pre-correction
    # comparison accepted as proof of a valid bundle.
    assert (workspace_a / filename).read_bytes() == (workspace_b / filename).read_bytes()

    before = (snapshot_tree(workspace_a), snapshot_tree(workspace_b))
    with pytest.raises(expected):
        compare(workspace_a, workspace_b)
    assert (snapshot_tree(workspace_a), snapshot_tree(workspace_b)) == before
    assert len(list(workspace_a.iterdir())) == 7
    assert len(list(workspace_b.iterdir())) == 7


def test_every_artifact_has_identical_corruption_coverage() -> None:
    covered = {case[1] for case in IDENTICAL_CORRUPTIONS}
    assert covered == set(ARTIFACT_FILENAMES)
    assert len(covered) == 7


def test_altered_payload_with_stale_fingerprint_text_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """Both carriers keep the old fingerprint text while the payload changed."""
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    original = json.loads((workspace_a / SPLIT_SUMMARY_FILENAME).read_bytes())["split_fingerprint"]
    corrupted = _corrupt_jsonl_byte((workspace_a / EXAMPLE_REGISTRY_FILENAME).read_bytes())
    for workspace in (workspace_a, workspace_b):
        (workspace / EXAMPLE_REGISTRY_FILENAME).write_bytes(corrupted)
        summary = json.loads((workspace / SPLIT_SUMMARY_FILENAME).read_bytes())
        manifest = json.loads((workspace / GENERATION_MANIFEST_FILENAME).read_bytes())
        assert summary["split_fingerprint"] == original
        assert manifest["split_fingerprint"] == original
    with pytest.raises(FormalFingerprintError):
        compare(workspace_a, workspace_b)


def test_identical_policy_tamper_with_stale_descriptor_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """The tampered policy stays syntactically valid; only its digest disagrees."""
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    tampered = _corrupt_policy_field((workspace_a / SPLIT_POLICY_FILENAME).read_bytes())
    assert json.loads(tampered)["holdout_policy"] == "tampered"
    for workspace in (workspace_a, workspace_b):
        (workspace / SPLIT_POLICY_FILENAME).write_bytes(tampered)
    with pytest.raises(FormalFingerprintError, match="descriptor digest"):
        compare(workspace_a, workspace_b)


def test_identical_descriptor_digest_corruption_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    tampered = _corrupt_manifest_descriptor(
        (workspace_a / GENERATION_MANIFEST_FILENAME).read_bytes()
    )
    for workspace in (workspace_a, workspace_b):
        (workspace / GENERATION_MANIFEST_FILENAME).write_bytes(tampered)
    with pytest.raises(FormalFingerprintError, match="descriptor digest"):
        compare(workspace_a, workspace_b)


def test_manifest_must_not_describe_itself(tmp_path: Path, environment: dict[str, Path]) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    document = json.loads((workspace_a / GENERATION_MANIFEST_FILENAME).read_bytes())
    document["artifacts"].append(
        {
            "byte_size": 1,
            "filename": GENERATION_MANIFEST_FILENAME,
            "schema_version": "mesc-pilot-01-formal-generation-manifest/1",
            "sha256": "0" * 64,
            "surface": "generation_manifest",
        }
    )
    payload = _canonical_line(document)
    for workspace in (workspace_a, workspace_b):
        (workspace / GENERATION_MANIFEST_FILENAME).write_bytes(payload)
    with pytest.raises(FormalInventoryError):
        compare(workspace_a, workspace_b)


def test_independent_descriptor_oracle(tmp_path: Path, environment: dict[str, Path]) -> None:
    """Recompute every non-self descriptor without using the comparison verifier."""
    result = generate(make_request(tmp_path, environment))
    manifest = json.loads((result.workspace / GENERATION_MANIFEST_FILENAME).read_bytes())
    described = {entry["filename"]: entry for entry in manifest["artifacts"]}
    non_self = [name for name in ARTIFACT_FILENAMES if name != GENERATION_MANIFEST_FILENAME]
    assert sorted(described) == sorted(non_self)
    assert len(non_self) == 6
    for filename in non_self:
        payload = (result.workspace / filename).read_bytes()
        expected_digest = hashlib.sha256(payload).hexdigest()
        assert described[filename]["sha256"] == expected_digest
        assert described[filename]["byte_size"] == len(payload)
        assert len(expected_digest) == 64


def test_independent_fingerprint_oracle(tmp_path: Path, environment: dict[str, Path]) -> None:
    """Rebuild the fingerprint from workspace bytes via the accepted primitives only."""
    result = generate(make_request(tmp_path, environment))
    workspace = result.workspace
    core_document = json.loads((workspace / SPLIT_SUMMARY_IDENTITY_CORE_FILENAME).read_bytes())
    core = SplitSummaryIdentityCore(
        total_example_count=core_document["total_example_count"],
        total_group_count=core_document["total_group_count"],
        excluded_record_count=core_document["excluded_record_count"],
        partition_totals=core_document["partition_totals"],
        label_totals=core_document["label_totals"],
        partition_label_matrix=core_document["partition_label_matrix"],
        group_counts_by_partition=core_document["group_counts_by_partition"],
        algorithm_version=core_document["algorithm_version"],
        schema_version=core_document["schema_version"],
    )
    identity = build_split_fingerprint_identity(
        policy_id="mesc-pilot-01-split-policy/1",
        algorithm_version=ALGORITHM_VERSION,
        split_seed=SPLIT_SEED,
        group_registry_payload=(workspace / GROUP_REGISTRY_FILENAME).read_bytes(),
        example_registry_payload=(workspace / EXAMPLE_REGISTRY_FILENAME).read_bytes(),
        excluded_ledger_payload=(workspace / EXCLUDED_LEDGER_FILENAME).read_bytes(),
        split_summary_identity_core=core,
    )
    recomputed = compute_split_fingerprint(identity)
    summary = json.loads((workspace / SPLIT_SUMMARY_FILENAME).read_bytes())
    manifest = json.loads((workspace / GENERATION_MANIFEST_FILENAME).read_bytes())
    assert len(recomputed) == 64
    assert recomputed == summary["split_fingerprint"]
    assert recomputed == manifest["split_fingerprint"]
    assert recomputed == result.split_fingerprint


def make_variant_environment(tmp_path: Path, revision: str) -> dict[str, Path]:
    """Build a second, legitimately different synthetic corpus.

    Only the synthetic dataset revision changes, so every derived example
    identifier changes and the bundle is internally valid but not byte-identical.
    """
    payloads = dict(synthetic_payloads())
    records = payloads[SOURCE_RECORDS_SURFACE].decode("utf-8").splitlines()
    rebuilt: list[str] = []
    for line in records:
        envelope = json.loads(line)
        envelope["record"]["dataset_revision"] = revision
        rebuilt.append(json.dumps(envelope, sort_keys=True))
    payloads[SOURCE_RECORDS_SURFACE] = ("\n".join(rebuilt) + "\n").encode("utf-8")
    identity = json.loads(payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE])
    identity["dataset_revision"] = revision
    identity["source_records_sha256"] = hashlib.sha256(payloads[SOURCE_RECORDS_SURFACE]).hexdigest()
    identity["source_records_byte_size"] = len(payloads[SOURCE_RECORDS_SURFACE])
    payloads[TRANSFORMED_DATASET_IDENTITY_SURFACE] = (
        json.dumps(identity, sort_keys=True) + "\n"
    ).encode("utf-8")

    root = tmp_path / f"variant-{revision}"
    repository = make_repository(root / "repo")
    inputs = write_synthetic_inputs(root / "inputs", payloads)
    external = root / "external-evidence"
    future = root / "future-evidence"
    external.mkdir()
    future.mkdir()
    return {
        "repository": repository,
        "external": external.resolve(),
        "future": future.resolve(),
        **{f"input:{surface}": location for surface, location in inputs.items()},
    }


def test_valid_but_different_pair_raises_byte_equality(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """Two independently valid bundles that differ raise the byte-equality error."""
    valid_a = generate(make_request(tmp_path, environment, workspace_name="classify-a")).workspace
    variant = make_variant_environment(tmp_path, "synthetic-revision-0002")
    valid_b = generate(
        make_request(tmp_path, variant, generation="B", workspace_name="classify-b")
    ).workspace

    first = json.loads((valid_a / SPLIT_SUMMARY_FILENAME).read_bytes())["split_fingerprint"]
    second = json.loads((valid_b / SPLIT_SUMMARY_FILENAME).read_bytes())["split_fingerprint"]
    assert first != second

    with pytest.raises(FormalByteEqualityError, match="invalidated"):
        compare(valid_a, valid_b)


def test_equality_classification_matrix(tmp_path: Path, environment: dict[str, Path]) -> None:
    """valid+identical succeeds; invalid+valid and invalid+invalid never do."""
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    assert compare(workspace_a, workspace_b).equal is True

    tampered = _corrupt_policy_field((workspace_a / SPLIT_POLICY_FILENAME).read_bytes())
    (workspace_a / SPLIT_POLICY_FILENAME).write_bytes(tampered)
    with pytest.raises(FormalFingerprintError):
        compare(workspace_a, workspace_b)

    (workspace_b / SPLIT_POLICY_FILENAME).write_bytes(tampered)
    with pytest.raises(FormalFingerprintError):
        compare(workspace_a, workspace_b)


# ---------------------------------------------------------------------------
# F2 — second repository-identity check immediately before first mutation
# ---------------------------------------------------------------------------


def test_commit_movement_between_validation_and_generation_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    request = make_request(tmp_path, environment, workspace_name="moved-ws")
    external_before = snapshot_tree(environment["external"])
    future_before = snapshot_tree(environment["future"])
    head = environment["repository"] / ".git" / "HEAD"
    original_head = head.read_bytes()

    moved = "b" * 40
    head.write_text(f"{moved}\n", encoding="utf-8")
    with pytest.raises(FormalInputIdentityError, match="moved"):
        generate(request)

    assert not request.workspace.exists()
    assert snapshot_tree(environment["external"]) == external_before
    assert snapshot_tree(environment["future"]) == future_before
    assert head.read_text(encoding="utf-8").strip() == moved
    git_entries = sorted(entry.name for entry in (environment["repository"] / ".git").iterdir())
    assert git_entries == ["HEAD"]
    head.write_bytes(original_head)


def test_repository_identity_is_read_twice_and_second_read_blocks_mutation(
    tmp_path: Path, environment: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The reader runs once at request build and again just before first mutation."""
    import medscale.mesc._formal_generation_v1 as module

    real_reader = module.resolve_repository_commit
    observed: list[str] = []

    def reader(repository_root: Path) -> str:
        actual = real_reader(repository_root)
        observed.append(actual if not observed else "b" * 40)
        return observed[-1]

    monkeypatch.setattr(module, "resolve_repository_commit", reader)

    mkdir_calls: list[Path] = []
    real_mkdir = Path.mkdir

    def spy_mkdir(self: Path, *args: object, **kwargs: object) -> None:
        mkdir_calls.append(self)
        real_mkdir(self, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "mkdir", spy_mkdir)

    request = make_request(tmp_path, environment, workspace_name="spied-ws")
    assert len(observed) == 1
    assert observed[0] == SYNTHETIC_COMMIT

    with pytest.raises(FormalInputIdentityError, match="moved"):
        generate(request)
    assert len(observed) == 2
    assert observed[1] != SYNTHETIC_COMMIT
    assert not request.workspace.exists()
    assert [path for path in mkdir_calls if path == request.workspace] == []


def test_second_check_supports_every_accepted_repository_shape(tmp_path: Path) -> None:
    """The re-verification reuses the accepted helper, so no layout support is lost."""
    detached = make_repository(tmp_path / "detached")
    assert resolve_repository_commit(detached) == SYNTHETIC_COMMIT

    symbolic = tmp_path / "symbolic"
    symbolic.mkdir()
    git_dir = symbolic / ".git"
    (git_dir / "refs" / "heads").mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/main\r\n", encoding="utf-8")
    (git_dir / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\r\n", encoding="utf-8")
    assert resolve_repository_commit(symbolic.resolve()) == SYNTHETIC_COMMIT

    linked = tmp_path / "linked"
    linked.mkdir()
    (linked / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
    assert resolve_repository_commit(linked.resolve()) == SYNTHETIC_COMMIT

    packed = tmp_path / "packed"
    packed.mkdir()
    packed_git = packed / ".git"
    packed_git.mkdir()
    (packed_git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (packed_git / "packed-refs").write_text(
        f"# pack-refs with: peeled\n{SYNTHETIC_COMMIT} refs/heads/main\n", encoding="utf-8"
    )
    assert resolve_repository_commit(packed.resolve()) == SYNTHETIC_COMMIT


# ---------------------------------------------------------------------------
# F3 — complete manifest-contract validation
#
# The targeted re-review showed that two otherwise valid, byte-identical
# workspaces were accepted when both manifests carried a modified
# algorithm_version or an extra top-level key: the manifest was validated only
# against its non-prohibited fields.  Verification now reconstructs the manifest
# through the pure model and regenerates its canonical bytes, so the whole
# contract is enforced.
# ---------------------------------------------------------------------------


def read_manifest(workspace: Path) -> dict[str, object]:
    document = json.loads((workspace / GENERATION_MANIFEST_FILENAME).read_bytes())
    assert isinstance(document, dict)
    return document


def write_manifest(workspace: Path, document: object) -> None:
    (workspace / GENERATION_MANIFEST_FILENAME).write_bytes(_canonical_line(document))


def corrupt_both_manifests(
    workspace_a: Path, workspace_b: Path, mutate: Callable[[dict[str, object]], None]
) -> None:
    """Apply the same deterministic manifest mutation to both workspaces."""
    for workspace in (workspace_a, workspace_b):
        document = read_manifest(workspace)
        mutate(document)
        write_manifest(workspace, document)
    assert (workspace_a / GENERATION_MANIFEST_FILENAME).read_bytes() == (
        workspace_b / GENERATION_MANIFEST_FILENAME
    ).read_bytes()


def assert_rejected_without_writes(
    workspace_a: Path, workspace_b: Path, expected: type[Exception]
) -> None:
    before = (snapshot_tree(workspace_a), snapshot_tree(workspace_b))
    with pytest.raises(expected):
        compare(workspace_a, workspace_b)
    assert (snapshot_tree(workspace_a), snapshot_tree(workspace_b)) == before
    assert len(list(workspace_a.iterdir())) == 7
    assert len(list(workspace_b.iterdir())) == 7


def test_f3_1_modified_algorithm_version_in_both_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    assert compare(workspace_a, workspace_b).equal is True
    corrupt_both_manifests(
        workspace_a,
        workspace_b,
        lambda document: document.__setitem__(
            "algorithm_version", "mesc-pilot-01-split-algorithm/9"
        ),
    )
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


@pytest.mark.parametrize(
    "value",
    ["", "   ", " mesc-pilot-01-split-algorithm/1", "mesc-pilot-01-split-algorithm/1 ", 1, None],
    ids=["blank", "whitespace", "left-padded", "right-padded", "integer", "null"],
)
def test_f3_1_algorithm_version_must_be_the_accepted_value(
    tmp_path: Path, environment: dict[str, Path], value: object
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    corrupt_both_manifests(
        workspace_a, workspace_b, lambda document: document.__setitem__("algorithm_version", value)
    )
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


def test_f3_2_extra_top_level_key_in_both_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """The exact probe the targeted re-review demonstrated as accepted."""
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    corrupt_both_manifests(
        workspace_a, workspace_b, lambda document: document.__setitem__("note", "innocuous")
    )
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


@pytest.mark.parametrize(
    "key",
    ["algorithm_version", "input_identity", "artifacts", "bundle_filenames", "split_fingerprint"],
)
def test_f3_3_missing_required_top_level_key_is_rejected(
    tmp_path: Path, environment: dict[str, Path], key: str
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)

    def drop_key(document: dict[str, object]) -> None:
        document.pop(key)

    corrupt_both_manifests(workspace_a, workspace_b, drop_key)
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


def _identity_drop_surface(document: dict[str, object]) -> None:
    entries = document["input_identity"]
    assert isinstance(entries, list)
    document["input_identity"] = entries[1:]


def _identity_add_surface(document: dict[str, object]) -> None:
    entries = document["input_identity"]
    assert isinstance(entries, list)
    extra = dict(entries[0])
    extra["surface"] = "decision_record"
    extra.pop("schema_version", None)
    entries.append(extra)


def _identity_duplicate_surface(document: dict[str, object]) -> None:
    entries = document["input_identity"]
    assert isinstance(entries, list)
    entries.append(dict(entries[0]))


def _identity_unknown_surface(document: dict[str, object]) -> None:
    entries = document["input_identity"]
    assert isinstance(entries, list)
    entries[0] = {**entries[0], "surface": "not_a_formal_surface"}


IDENTITY_SURFACE_CASES: tuple[tuple[str, Callable[[dict[str, object]], None]], ...] = (
    ("missing-surface", _identity_drop_surface),
    ("extra-surface", _identity_add_surface),
    ("duplicate-surface", _identity_duplicate_surface),
    ("unknown-surface", _identity_unknown_surface),
)


@pytest.mark.parametrize(
    ("label", "mutate"), IDENTITY_SURFACE_CASES, ids=[case[0] for case in IDENTITY_SURFACE_CASES]
)
def test_f3_4_input_identity_exact_surfaces(
    tmp_path: Path,
    environment: dict[str, Path],
    label: str,
    mutate: Callable[[dict[str, object]], None],
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    corrupt_both_manifests(workspace_a, workspace_b, mutate)
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


def _schema_bearing_index(entries: list[dict[str, object]]) -> int:
    """Return an entry that declares a schema version.

    The ratified decision record is governance prose bound by digest alone, so it
    carries no ``schema_version``; targeting it would make a schema-field probe a
    silent no-op.
    """
    for index, entry in enumerate(entries):
        if "schema_version" in entry:
            return index
    raise AssertionError("no input-identity entry declares a schema version")


def _field_mutator(field: str, value: object) -> Callable[[dict[str, object]], None]:
    def mutate(document: dict[str, object]) -> None:
        entries = document["input_identity"]
        assert isinstance(entries, list)
        index = _schema_bearing_index(entries)
        entries[index] = {**entries[index], field: value}

    return mutate


def _field_remover(field: str) -> Callable[[dict[str, object]], None]:
    def mutate(document: dict[str, object]) -> None:
        entries = document["input_identity"]
        assert isinstance(entries, list)
        index = _schema_bearing_index(entries)
        trimmed = dict(entries[index])
        assert field in trimmed, f"probe would be a no-op: {field!r} is absent"
        trimmed.pop(field)
        entries[index] = trimmed

    return mutate


IDENTITY_FIELD_CASES: tuple[tuple[str, Callable[[dict[str, object]], None]], ...] = (
    ("uppercase-digest", _field_mutator("sha256", "A" * 64)),
    ("digest-63", _field_mutator("sha256", "a" * 63)),
    ("digest-65", _field_mutator("sha256", "a" * 65)),
    ("non-hex-digest", _field_mutator("sha256", "z" * 64)),
    ("negative-byte-size", _field_mutator("byte_size", -1)),
    ("boolean-byte-size", _field_mutator("byte_size", True)),
    ("float-byte-size", _field_mutator("byte_size", 1.5)),
    ("missing-schema-field", _field_remover("schema_version")),
    ("extra-nested-field", _field_mutator("note", "extra")),
    ("wrong-primitive-type", _field_mutator("sha256", 12345)),
    ("padded-schema", _field_mutator("schema_version", " mesc-pilot-01-source-records/1")),
)


@pytest.mark.parametrize(
    ("label", "mutate"), IDENTITY_FIELD_CASES, ids=[case[0] for case in IDENTITY_FIELD_CASES]
)
def test_f3_5_input_identity_field_validation(
    tmp_path: Path,
    environment: dict[str, Path],
    label: str,
    mutate: Callable[[dict[str, object]], None],
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    corrupt_both_manifests(workspace_a, workspace_b, mutate)
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


@pytest.mark.parametrize(
    ("label", "mutate"),
    (
        ("extra-artifact-field", _field_mutator("note", "extra")),
        ("missing-artifact-field", _field_remover("schema_version")),
    ),
    ids=["artifact-extra-field", "artifact-missing-field"],
)
def test_f3_5_artifact_descriptor_field_validation(
    tmp_path: Path,
    environment: dict[str, Path],
    label: str,
    mutate: Callable[[dict[str, object]], None],
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)

    def mutate_artifacts(document: dict[str, object]) -> None:
        holder: dict[str, object] = {"input_identity": document["artifacts"]}
        mutate(holder)
        document["artifacts"] = holder["input_identity"]

    corrupt_both_manifests(workspace_a, workspace_b, mutate_artifacts)
    assert_rejected_without_writes(workspace_a, workspace_b, FormalInputSchemaError)


def test_f3_6_canonical_byte_regeneration_is_exact(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """Rebuild the manifest through an independent path and match the bytes exactly."""
    result = generate(make_request(tmp_path, environment))
    workspace = result.workspace
    actual = (workspace / GENERATION_MANIFEST_FILENAME).read_bytes()
    document = json.loads(actual)

    rebuilt = FormalGenerationManifest(
        schema_version=document["schema_version"],
        algorithm_version=document["algorithm_version"],
        bundle_filenames=tuple(document["bundle_filenames"]),
        artifacts=tuple(
            FormalArtifactEntry(
                filename=entry["filename"],
                surface=entry["surface"],
                schema_version=entry["schema_version"],
                sha256=entry["sha256"],
                byte_size=entry["byte_size"],
            )
            for entry in document["artifacts"]
        ),
        input_identity=FormalSplitInputIdentity(
            descriptors=tuple(
                FormalInputDescriptor(
                    surface=entry["surface"],
                    schema_version=entry.get("schema_version"),
                    sha256=entry["sha256"],
                    byte_size=entry["byte_size"],
                )
                for entry in document["input_identity"]
            )
        ),
        split_fingerprint=document["split_fingerprint"],
    )
    assert rebuilt.canonical_bytes() == actual


def test_f3_6_non_canonical_formatting_is_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """The same decoded values, serialized non-canonically, must be refused."""
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    document = read_manifest(workspace_a)
    variants = (
        json.dumps(document, sort_keys=True, indent=2) + "\n",
        json.dumps(document, sort_keys=True, separators=(", ", ": ")) + "\n",
        json.dumps(document, sort_keys=True, separators=(",", ":")),
        json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n\n",
    )
    for variant in variants:
        payload = variant.encode("utf-8")
        for workspace in (workspace_a, workspace_b):
            (workspace / GENERATION_MANIFEST_FILENAME).write_bytes(payload)
        assert json.loads(payload) == document
        with pytest.raises(FormalInputSchemaError):
            compare(workspace_a, workspace_b)


def test_f3_6_duplicate_manifest_keys_are_rejected(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    text = (workspace_a / GENERATION_MANIFEST_FILENAME).read_text(encoding="utf-8")
    duplicated = text.replace('"schema_version":', '"schema_version":"x","schema_version":', 1)
    for workspace in (workspace_a, workspace_b):
        (workspace / GENERATION_MANIFEST_FILENAME).write_text(duplicated, encoding="utf-8")
    with pytest.raises(FormalInputSchemaError, match="duplicate JSON object key"):
        compare(workspace_a, workspace_b)


def test_f3_7_exact_valid_manifest_is_accepted(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    workspace_a, workspace_b = make_pair(tmp_path, environment)
    document = read_manifest(workspace_a)

    assert sorted(document) == [
        "algorithm_version",
        "artifacts",
        "bundle_filenames",
        "input_identity",
        "schema_version",
        "split_fingerprint",
    ]
    bundle_filenames = document["bundle_filenames"]
    artifacts = document["artifacts"]
    identity = document["input_identity"]
    fingerprint = document["split_fingerprint"]
    assert isinstance(bundle_filenames, list)
    assert isinstance(artifacts, list)
    assert isinstance(identity, list)
    assert isinstance(fingerprint, str)

    assert document["schema_version"] == "mesc-pilot-01-formal-generation-manifest/1"
    assert document["algorithm_version"] == ALGORITHM_VERSION
    assert bundle_filenames == list(ARTIFACT_FILENAMES)
    assert len(bundle_filenames) == 7
    assert len(artifacts) == 6
    assert GENERATION_MANIFEST_FILENAME not in {entry["filename"] for entry in artifacts}
    assert len(identity) == 5
    assert {entry["surface"] for entry in identity} == {
        "ordered_example_registry",
        "source_document_registry",
        "transformed_dataset_identity",
        "source_records",
        "decision_record",
    }
    assert len(fingerprint) == 64
    assert fingerprint == fingerprint.lower()
    summary = json.loads((workspace_a / SPLIT_SUMMARY_FILENAME).read_bytes())
    assert summary["split_fingerprint"] == fingerprint

    result = compare(workspace_a, workspace_b)
    assert result.equal is True
    assert result.split_fingerprint == fingerprint


def test_f3_manifest_still_carries_no_self_descriptor(
    tmp_path: Path, environment: dict[str, Path]
) -> None:
    """Closing F3 must not introduce a self-hash, self-size or eighth artifact."""
    result = generate(make_request(tmp_path, environment))
    workspace = result.workspace
    payload = (workspace / GENERATION_MANIFEST_FILENAME).read_bytes()
    document = json.loads(payload)
    assert GENERATION_MANIFEST_FILENAME not in {
        entry["filename"] for entry in document["artifacts"]
    }
    assert hashlib.sha256(payload).hexdigest() not in payload.decode("utf-8")
    assert str(len(payload)) not in {str(entry["byte_size"]) for entry in document["artifacts"]}
    assert sorted(entry.name for entry in workspace.iterdir()) == sorted(ARTIFACT_FILENAMES)
    assert "split-fingerprint.json" not in {entry.name for entry in workspace.iterdir()}
