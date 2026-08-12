"""Synthetic qualification of the sole controlled P01-04E operator surface.

Every invocation runs against freshly generated synthetic inputs under
``tmp_path``, including a synthetic Git repository whose checked-out commit
matches the operator's pinned canonical identity.  No test reads a protected
registry, an external real source-record file or any real dataset, and no test
executes a real leakage audit; the classification ledger is likewise synthetic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from medscale.mesc._canonical_json_v1 import sha256_of_bytes
from medscale.mesc._leakage_audit_v1 import AUDIT_SCHEMA_VERSION

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OPERATOR_PATH = REPOSITORY_ROOT / "scripts" / "mesc_p01_04e_operator.py"

AUDIT_FILENAME = "leakage-audit.json"

EPISODE_IDENTITY = "a" * 64
SPLIT_FINGERPRINT = "b" * 64
OTHER_SHA256 = "c" * 64


def load_operator() -> ModuleType:
    """Import the operator script by path, exactly as an operator would run it."""
    spec = importlib.util.spec_from_file_location(
        "_mesc_p01_04e_operator_under_test", OPERATOR_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def operator() -> ModuleType:
    return load_operator()


# ---------------------------------------------------------------------------
# Synthetic layout
# ---------------------------------------------------------------------------


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    payload = b"".join((json.dumps(dict(row), sort_keys=True) + "\n").encode() for row in rows)
    path.write_bytes(payload)


class Environment:
    """One synthetic execution environment under ``tmp_path``."""

    def __init__(self, root: Path, operator: ModuleType) -> None:
        self.root = root
        self.repository = root / "repo"
        self.dws = root / "dws"
        self.custody = root / "source-custody"
        self.registry = self.dws / "example-registry.jsonl"
        self.manifest = self.dws / "generation-manifest.json"
        self.source_records = self.custody / "source-records.jsonl"

        (self.repository / "scripts").mkdir(parents=True)  # anchor for scripts layout
        (self.repository / ".git" / "refs" / "heads").mkdir(parents=True)
        (self.repository / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        self.repo_commit = "4" * 40
        (self.repository / ".git" / "refs" / "heads" / "main").write_text(
            self.repo_commit + "\n", encoding="utf-8"
        )

        self.dws.mkdir()
        self.custody.mkdir()

    def write_manifest(self, fingerprint: str = SPLIT_FINGERPRINT, **extra: object) -> None:
        document: dict[str, object] = {"split_fingerprint": fingerprint}
        document.update(extra)
        self.manifest.write_bytes(json.dumps(document, sort_keys=True).encode())

    def write_registry(
        self,
        rows: Sequence[Mapping[str, str]] | None = None,
        *,
        raw: bytes | None = None,
    ) -> None:
        if raw is not None:
            self.registry.write_bytes(raw)
            return
        if rows is None:
            rows = [
                {
                    "example_id": "mesc-pilot-01:ex-a",
                    "source_document_id": "sd-aaa",
                    "assigned_split": "train",
                },
                {
                    "example_id": "mesc-pilot-01:ex-b",
                    "source_document_id": "sd-bbb",
                    "assigned_split": "validation",
                },
                {
                    "example_id": "mesc-pilot-01:ex-c",
                    "source_document_id": "sd-ccc",
                    "assigned_split": "test",
                },
            ]
        _write_jsonl(self.registry, rows)

    def write_source_records(
        self,
        records: Sequence[Mapping[str, object]] | None = None,
        *,
        raw: bytes | None = None,
    ) -> None:
        if raw is not None:
            self.source_records.write_bytes(raw)
            return
        if records is None:
            records = [
                {
                    "original_example_id": "ex-001",
                    "source_document_id": "sd-aaa",
                    "question": "What is the treatment for stage one disease?",
                    "context_segments": ["Unique synthetic segment alpha."],
                },
                {
                    "original_example_id": "ex-002",
                    "source_document_id": "sd-bbb",
                    "question": "What is the treatment for stage one disease?",
                    "context_segments": ["Unique synthetic segment beta."],
                },
                {
                    "original_example_id": "ex-003",
                    "source_document_id": "sd-ccc",
                    "question": "Different synthetic question.",
                    "context_segments": ["Unique synthetic segment gamma."],
                },
            ]
        lines = []
        for record in records:
            # Wrap any plain-string context segments into the canonical
            # NativeContextSegment object shape expected by the operator.
            # Pre-built dict segments are passed through unchanged so poison
            # tests can assert exact fail-closed refusal on malformed objects.
            segs_out: list[object] = []
            segs_in: object = record.get("context_segments", [])
            for si, seg in enumerate(cast(Sequence[object], segs_in)):
                if isinstance(seg, str):
                    segs_out.append({"ordinal": si, "text": seg, "section_label": "synthetic"})
                else:
                    segs_out.append(seg)
            record_out = {**dict(record), "context_segments": segs_out}
            envelope = {"record": {"schema_version": "mesc-pubmedqa-source/1", **record_out}}
            lines.append(json.dumps(envelope, sort_keys=True).encode())
        self.source_records.write_bytes(b"\n".join(lines) + b"\n")

    def audit_argv(
        self,
        *,
        workspace: Path,
        expected_commit: str | None = None,
        episode_identity: str = EPISODE_IDENTITY,
        expected_fingerprint: str = SPLIT_FINGERPRINT,
        ledger: Path | None = None,
        registry: Path | None = None,
        manifest: Path | None = None,
        source_records: Path | None = None,
        expected_gm_sha: str | None = None,
        expected_gm_size: int | None = None,
        expected_er_sha: str | None = None,
        expected_er_size: int | None = None,
        expected_sr_sha: str | None = None,
        expected_sr_size: int | None = None,
    ) -> list[str]:
        """Build an argv that is identity-consistent with the on-disk inputs.

        Expected manifest/registry/source-record identities default to the true
        digest and byte size of the actual bytes consumed, and the expected
        canonical commit defaults to the synthetic repository's pinned HEAD, so
        a test can focus a single deliberately wrong expected value while every
        other identity stays correct.
        """
        registry_path = registry or self.registry
        manifest_path = manifest or self.manifest
        source_records_path = source_records or self.source_records
        registry_bytes = registry_path.read_bytes()
        manifest_bytes = manifest_path.read_bytes()
        source_bytes = source_records_path.read_bytes()
        argv = [
            "audit",
            "--repository-root",
            str(self.repository),
            "--expected-canonical-commit",
            expected_commit or self.repo_commit,
            "--episode-identity",
            episode_identity,
            "--expected-split-fingerprint",
            expected_fingerprint,
            "--expected-generation-manifest-sha256",
            expected_gm_sha or hashlib.sha256(manifest_bytes).hexdigest(),
            "--expected-generation-manifest-byte-size",
            str(expected_gm_size if expected_gm_size is not None else len(manifest_bytes)),
            "--expected-example-registry-sha256",
            expected_er_sha or hashlib.sha256(registry_bytes).hexdigest(),
            "--expected-example-registry-byte-size",
            str(expected_er_size if expected_er_size is not None else len(registry_bytes)),
            "--expected-source-records-sha256",
            expected_sr_sha or hashlib.sha256(source_bytes).hexdigest(),
            "--expected-source-records-byte-size",
            str(expected_sr_size if expected_sr_size is not None else len(source_bytes)),
            "--example-registry",
            str(registry_path),
            "--generation-manifest",
            str(manifest_path),
            "--source-records",
            str(source_records_path),
            "--audit-workspace",
            str(workspace),
        ]
        if ledger is not None:
            argv.append("--classification-ledger")
            argv.append(str(ledger))
        return argv


def run_operator(
    operator: ModuleType, argv: Sequence[str], capsys: pytest.CaptureFixture[str]
) -> tuple[int, str, str]:
    code = operator.main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


def assert_refused(code: int, out: str, err: str, *, workspace: Path | None = None) -> None:
    assert code != 0
    assert "audit complete" not in out
    assert "audit failed" in err
    if workspace is not None:
        assert not workspace.exists()


def load_audit(workspace: Path) -> dict[str, Any]:
    payload = (workspace / AUDIT_FILENAME).read_bytes()
    assert payload.endswith(b"\n")
    assert payload.count(b"\n") == 1
    return cast(dict[str, Any], json.loads(payload))


def _structural_environment(root: Path, operator: ModuleType) -> Environment:
    """Return an environment whose records duplicate original_example_id
    across partitions (producing an ``exact_example`` finding)."""
    env = Environment(root, operator)
    env.write_registry(
        [
            {
                "example_id": "mesc-pilot-01:ex-a",
                "source_document_id": "sd-aaa",
                "assigned_split": "train",
            },
            {
                "example_id": "mesc-pilot-01:ex-b",
                "source_document_id": "sd-zz9",
                "assigned_split": "validation",
            },
        ]
    )
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "dup-01",
                "source_document_id": "sd-aaa",
                "question": "Alpha question unique.",
                "context_segments": ["Alpha segment unique."],
            },
            {
                "original_example_id": "dup-01",
                "source_document_id": "sd-zz9",
                "question": "Beta question distinct.",
                "context_segments": ["Beta segment distinct."],
            },
        ]
    )
    return env


# ---------------------------------------------------------------------------
# Surface shape
# ---------------------------------------------------------------------------


def test_exactly_one_subcommand_and_no_third(operator: ModuleType) -> None:
    assert operator.COMMANDS == ("audit",)
    parser = operator.build_parser()
    subparser_actions = list(parser._subparsers._group_actions)
    assert len(subparser_actions) == 1
    choices = sorted(subparser_actions[0].choices)
    assert choices == ["audit"]


def test_unknown_subcommand_is_rejected(operator: ModuleType) -> None:
    with pytest.raises(SystemExit) as exit_info:
        operator.main(["verify"])
    assert exit_info.value.code != 0


def test_no_arguments_is_not_a_success(operator: ModuleType) -> None:
    assert operator.main([]) == 2


# ---------------------------------------------------------------------------
# Clean synthetic audit
# ---------------------------------------------------------------------------


def test_clean_synthetic_audit_produces_canonical_schema(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)

    assert code == 0
    assert err == ""
    assert "audit complete" in out
    audit = load_audit(workspace)
    assert set(audit) == {
        "schema_version",
        "split_identity",
        "source_records_identity",
        "thresholds",
        "detection_methods",
        "normalization_record",
        "finding_count",
        "findings",
        "leaked",
    }
    assert audit["schema_version"] == AUDIT_SCHEMA_VERSION
    assert audit["thresholds"] == {
        "question_near_duplicate_jaccard_percent": 90,
        "context_overlap_jaccard_percent": 95,
    }
    assert audit["finding_count"] > 0
    assert audit["leaked"] is True  # unresolved cross-partition question findings present
    artifacts = list(workspace.iterdir())
    assert artifacts == [workspace / AUDIT_FILENAME]


def test_clean_audit_is_deterministic_across_fresh_workspaces(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()

    ws_a = tmp_path / "ws-a"
    ws_b = tmp_path / "ws-b"
    code_a, out_a, _ = run_operator(operator, env.audit_argv(workspace=ws_a), capsys)
    code_b, out_b, _ = run_operator(operator, env.audit_argv(workspace=ws_b), capsys)
    assert code_a == code_b == 0
    assert out_a == out_b
    bytes_a = (ws_a / AUDIT_FILENAME).read_bytes()
    bytes_b = (ws_b / AUDIT_FILENAME).read_bytes()
    assert sha256_of_bytes(bytes_a) == sha256_of_bytes(bytes_b)


# ---------------------------------------------------------------------------
# Q28 — repository / path safety (operator surface)
# ---------------------------------------------------------------------------


def test_workspace_inside_repository_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = env.repository / "evil"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "outside the repository" in err


def test_repository_inside_workspace_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path / "outer", operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path  # ancestor that contains the repository
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "must not be inside the workspace" in err


def test_workspace_inside_p01_04d_workspace_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = env.dws / "nested-ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "P01-04D workspace" in err


def test_workspace_inside_source_record_custody_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = env.custody / "nested-ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "source-records" in err


def test_workspace_reuse_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    workspace.mkdir()
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "already exists" in err
    assert not (workspace / AUDIT_FILENAME).exists()


def test_preexisting_leakage_audit_json_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    workspace.mkdir()
    existing = workspace / AUDIT_FILENAME
    existing.write_text("sentinel", encoding="utf-8")
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert existing.read_text(encoding="utf-8") == "sentinel"  # never overwritten


@pytest.mark.skipif(
    os.path.normcase("A") == "A", reason="case-insensitive path identity not applicable"
)
def test_case_variant_workspace_alias_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = env.repository.with_name(env.repository.name.lower()) / "injected"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "outside the repository" in err


def try_reparse_dir(link: Path, target: Path) -> bool:
    """Create a directory reparse point, reporting whether the host permitted it.

    Mirrors the portable pattern already used by the P01-04D evidence harness: a
    Windows junction needs no elevation, so the reparse containment contract is
    exercised for real on hosts that refuse unprivileged directory symlinks.
    """
    if os.name == "nt":
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            check=False,
        )
        return completed.returncode == 0 and link.exists()
    try:
        link.symlink_to(target, target_is_directory=True)
    except (OSError, NotImplementedError):
        return False
    return link.is_symlink()


@pytest.mark.parametrize(
    ("alias_target", "expected_text"),
    [
        ("repository", "outside the repository"),
        ("dws", "P01-04D workspace"),
        ("custody", "source-records"),
    ],
)
def test_reparse_alias_into_protected_location_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    alias_target: str,
    expected_text: str,
) -> None:
    """A workspace reached through a reparse point into a protected directory is
    refused because the real operator resolves aliases before containment checks."""
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    protected = {
        "repository": env.repository,
        "dws": env.dws,
        "custody": env.custody,
    }[alias_target]
    alias = tmp_path / f"{alias_target}-alias"
    if not try_reparse_dir(alias, protected):
        pytest.skip("this host cannot create a directory reparse point")
    workspace = alias / "injected-nested"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert expected_text in err


# ---------------------------------------------------------------------------
# Q23 / Q24 / Q26 — identity binding (operator surface)
#
# Q23: expected generation-manifest SHA-256 and byte_size binding (refused on
#      mismatch).  Q24: expected example-registry SHA-256 and byte_size binding.
#      Q26: expected source-records SHA-256 and byte_size binding.  Q25
#      (repository output refused) and the expected repository-commit binding
#      are proven by the repository-identity tests immediately below.
# ---------------------------------------------------------------------------


def test_wrong_expected_repository_commit_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    (env.repository / ".git" / "refs" / "heads" / "main").write_text(
        "5" * 40 + "\n", encoding="utf-8"
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "not the expected commit" in err


def test_expected_canonical_commit_arg_mismatch_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The runtime-supplied expected commit, not repository HEAD, is authoritative."""
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator,
        env.audit_argv(workspace=workspace, expected_commit="9" * 40),
        capsys,
    )
    assert_refused(code, out, err, workspace=workspace)
    assert "not the expected commit" in err


def test_missing_expected_canonical_commit_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    argv = env.audit_argv(workspace=tmp_path / "ws")
    argv = [item for item in argv if item != "--expected-canonical-commit"]
    argv.remove(env.repo_commit)
    with pytest.raises(SystemExit) as exit_info:
        operator.main(argv)
    assert exit_info.value.code != 0


def test_malformed_expected_canonical_commit_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    for bad in ("not-a-commit", "GGGG" * 10, "abc"):
        code, out, err = run_operator(
            operator,
            env.audit_argv(workspace=workspace / "ws", expected_commit=bad),
            capsys,
        )
        assert_refused(code, out, err, workspace=workspace / "ws")
        assert "hex" in err or "chars" in err
        assert "audit complete" not in out


def test_no_compile_time_canonical_main_constant(operator: ModuleType) -> None:
    assert not hasattr(operator, "_EXPECTED_CANONICAL_MAIN")
    assert operator._COMMIT_LEN == 40
    assert operator._require_commit("a" * 40) == "a" * 40
    with pytest.raises(operator.OperatorError):
        operator._require_commit("z" * 40)


def test_second_repository_verification_before_first_mutation(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A repository HEAD movement detected only by the second verification is a
    refusal, and no audit workspace or leakage-audit.json may be created."""
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    real_resolve = operator._resolve_repository_commit
    calls: list[str] = []

    def moving_head(repository_root: Path) -> str:
        value = real_resolve(repository_root) if len(calls) == 0 else "8" * 40
        calls.append(value)
        return value

    monkeypatch.setattr(operator, "_resolve_repository_commit", moving_head)
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert len(calls) == 2
    assert calls[0] == env.repo_commit
    assert_refused(code, out, err, workspace=workspace)
    assert "not the expected commit" in err
    assert not workspace.exists()


def test_second_verification_passes_and_audit_written(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, _out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    assert err == ""
    assert (workspace / AUDIT_FILENAME).is_file()


def test_wrong_split_fingerprint_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator,
        env.audit_argv(workspace=workspace, expected_fingerprint=OTHER_SHA256),
        capsys,
    )
    assert_refused(code, out, err, workspace=workspace)
    assert "split_fingerprint" in err


def test_manifest_without_fingerprint_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_source_records()
    # A manifest with no split_fingerprint key must fail the fingerprint check.
    env.manifest.write_bytes(json.dumps({"algorithm_version": "v1"}).encode())
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "split_fingerprint" in err


def test_manifest_not_valid_json_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_source_records()
    env.manifest.write_bytes(b"{not json")
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "not valid JSON" in err


@pytest.mark.parametrize(
    ("wrong", "expect_surface"),
    [
        ("gm_sha", "generation-manifest sha256"),
        ("gm_size", "generation-manifest byte_size"),
        ("er_sha", "example-registry sha256"),
        ("er_size", "example-registry byte_size"),
        ("sr_sha", "source-records sha256"),
        ("sr_size", "source-records byte_size"),
    ],
)
def test_wrong_expected_input_identity_independently_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    wrong: str,
    expect_surface: str,
) -> None:
    """Prove independent fail-closed refusal for each expected input identity.

    One deliberately wrong expected value is supplied at a time while all other
    identities stay correct, so every mismatch path is exercised independently
    (Q23 generation-manifest, Q24 example-registry, Q26 source-records; each for
    both SHA-256 and byte_size).
    """
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    kwargs: dict[str, Any] = {}
    if wrong == "gm_sha":
        kwargs["expected_gm_sha"] = "1" * 64
    elif wrong == "gm_size":
        kwargs["expected_gm_size"] = 1
    elif wrong == "er_sha":
        kwargs["expected_er_sha"] = "2" * 64
    elif wrong == "er_size":
        kwargs["expected_er_size"] = 2
    elif wrong == "sr_sha":
        kwargs["expected_sr_sha"] = "3" * 64
    else:
        kwargs["expected_sr_size"] = 3
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace, **kwargs), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "audit complete" not in out
    assert expect_surface in err
    assert "!=" in err


def test_recorded_manifest_identity_equals_true_content_identity(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_source_records()
    env.manifest.write_bytes(
        json.dumps({"split_fingerprint": SPLIT_FINGERPRINT, "algorithm_version": "v1"}).encode()
    )
    manifest_bytes = env.manifest.read_bytes()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    audit = load_audit(workspace)
    split = audit["split_identity"]
    assert isinstance(split, dict)
    assert split["generation_manifest_sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    assert split["generation_manifest_byte_size"] == len(manifest_bytes)


def test_recorded_registry_identity_equals_true_content_identity(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    registry_bytes = env.registry.read_bytes()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    split = load_audit(workspace)["split_identity"]
    assert isinstance(split, dict)
    assert split["example_registry_sha256"] == hashlib.sha256(registry_bytes).hexdigest()
    assert split["example_registry_byte_size"] == len(registry_bytes)


def test_recorded_source_records_identity_equals_true_content_identity(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    source_bytes = env.source_records.read_bytes()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    identity = load_audit(workspace)["source_records_identity"]
    assert isinstance(identity, dict)
    assert identity["sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert identity["byte_size"] == len(source_bytes)


def test_tampered_artifacts_rebind_to_the_actual_consumed_bytes(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()

    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    baseline = load_audit(workspace)
    baseline_src = baseline["source_records_identity"]
    baseline_er = baseline["split_identity"]

    # Tamper the source-records content (question text change keeps the record
    # shape valid) and re-run into a fresh workspace.  Byte-level tampering at
    # raw bytes keeps the LF-only contract intact.
    tampered_raw = env.source_records.read_bytes().replace(b"stage one", b"stage ONE")
    env.source_records.write_bytes(tampered_raw)
    tampered_bytes = env.source_records.read_bytes()
    ws2 = tmp_path / "ws2"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=ws2), capsys)
    assert code == 0
    rebound = load_audit(ws2)
    rebound_src = rebound["source_records_identity"]
    assert rebound_src["sha256"] == hashlib.sha256(tampered_bytes).hexdigest()
    assert rebound_src["byte_size"] == len(tampered_bytes)
    assert rebound_src != baseline_src

    # The registry identity is bound to the bytes actually read, not to a
    # semantic equivalent: reordering rows changes the recorded identity.
    rows = [
        {
            "example_id": "mesc-pilot-01:ex-a",
            "source_document_id": "sd-aaa",
            "assigned_split": "train",
        },
        {
            "example_id": "mesc-pilot-01:ex-c",
            "source_document_id": "sd-ccc",
            "assigned_split": "test",
        },
        {
            "example_id": "mesc-pilot-01:ex-b",
            "source_document_id": "sd-bbb",
            "assigned_split": "validation",
        },
    ]
    env.write_registry(rows=rows)
    reordered_bytes = env.registry.read_bytes()
    ws3 = tmp_path / "ws3"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=ws3), capsys)
    assert code == 0
    reordered_audit = load_audit(ws3)
    assert (
        reordered_audit["split_identity"]["example_registry_sha256"]
        == hashlib.sha256(reordered_bytes).hexdigest()
    )
    assert reordered_audit["split_identity"] != baseline_er


def test_registry_lf_requirement_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_manifest()
    env.write_source_records()
    line = json.dumps(
        {
            "example_id": "mesc-pilot-01:ex-a",
            "source_document_id": "sd-aaa",
            "assigned_split": "train",
        },
        sort_keys=True,
    )
    env.registry.write_bytes((line + "\r\n").encode())
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "LF terminators" in err


def test_source_records_wrong_schema_version_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": ["A segment."],
            }
        ],
    )
    payload = env.source_records.read_bytes()
    payload = payload.replace(b"mesc-pubmedqa-source/1", b"mesc-other-source/9")
    env.source_records.write_bytes(payload)
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "schema_version" in err


def test_source_record_missing_from_registry_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-099",
                "source_document_id": "sd-unknown",
                "question": "Q?",
                "context_segments": ["A segment."],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "not found in example registry" in err


def test_registry_duplicate_source_document_id_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_manifest()
    env.write_source_records()
    env.write_registry(
        [
            {
                "example_id": "mesc-pilot-01:ex-a",
                "source_document_id": "sd-aaa",
                "assigned_split": "train",
            },
            {
                "example_id": "mesc-pilot-01:ex-b",
                "source_document_id": "sd-aaa",
                "assigned_split": "validation",
            },
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "duplicate source_document_id" in err


# ---------------------------------------------------------------------------
# NativeContextSegment canonical shape parsing (ordinal/text/section_label)
# ---------------------------------------------------------------------------


def _canonical_records(segments: tuple[str, ...]) -> list[Mapping[str, object]]:
    """One synthetic record with the given plain-string segments wrapped as the
    canonical NativeContextSegment object shape (ordinal == segment index)."""
    return [
        {
            "original_example_id": "ex-001",
            "source_document_id": "sd-aaa",
            "question": "Synthetic detection question unique?",
            "context_segments": list(segments),
        }
    ]


def test_canonical_single_segment_object_accepted(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(_canonical_records(("Alpha unique segment.",)))
    workspace = tmp_path / "ws"
    code, _, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    assert err == ""
    assert (workspace / AUDIT_FILENAME).is_file()


def test_canonical_multiple_segments_in_ordinal_order_accepted(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        _canonical_records(("Alpha unique segment.", "Beta unique segment.", "Gamma segment."))
    )
    workspace = tmp_path / "ws"
    code, _, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    assert err == ""


def test_projection_preserves_exact_source_order_and_retains_only_text(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The operator writes exactly the segment strings, in source order; the
    canonical object scaffolding (ordinal/section_label) never reaches the audit
    artifact."""
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        _canonical_records(("First ordered unique segment.", "Second ordered unique segment."))
    )
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    report = (workspace / AUDIT_FILENAME).read_bytes()
    assert b"synthetic" not in report  # the fixed section_label scaffold never leaks
    assert b"section_label" not in report
    assert b"ordinal" not in report


@pytest.mark.parametrize("bad_kind", ["not_a_list", "empty_list", "more_than_nine"])
def test_context_segments_container_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    bad_kind: str,
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    if bad_kind == "not_a_list":
        raw = (
            b'{"record": {"schema_version": "mesc-pubmedqa-source/1", '
            b'"original_example_id": "ex-001", "source_document_id": "sd-aaa", '
            b'"question": "Q?", "context_segments": "not-a-list"}}\n'
        )
        env.source_records.write_bytes(raw)
        expect = "must be a non-empty list"
    elif bad_kind == "empty_list":
        env.write_source_records(
            [
                {
                    "original_example_id": "ex-001",
                    "source_document_id": "sd-aaa",
                    "question": "Q?",
                    "context_segments": [],
                }
            ]
        )
        expect = "must be a non-empty list"
    else:
        env.write_source_records(
            [
                {
                    "original_example_id": "ex-001",
                    "source_document_id": "sd-aaa",
                    "question": "Q?",
                    "context_segments": [f"s{i} unique." for i in range(10)],
                }
            ]
        )
        expect = "1..9"
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert expect in err


@pytest.mark.parametrize(
    "bad_segment",
    [
        "just-a-string",
        None,
        ["nested"],
        {"text": "x", "section_label": "y"},  # missing ordinal
        {"ordinal": 0, "section_label": "y"},  # missing text
        {"ordinal": 0, "text": "x"},  # missing section_label
        {"ordinal": 0, "text": "x", "section_label": "y", "extra": "Z"},  # unknown key
    ],
)
def test_segment_object_shape_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    bad_segment: object,
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    # When the poison value is a plain string, write raw bytes so the test
    # fixture helper does not auto-wrap it into a valid canonical segment.
    if isinstance(bad_segment, str):
        payload = {
            "record": {
                "schema_version": "mesc-pubmedqa-source/1",
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [bad_segment],
            }
        }
        env.source_records.write_bytes((json.dumps(payload, sort_keys=True) + "\n").encode())
    else:
        env.write_source_records(
            [
                {
                    "original_example_id": "ex-001",
                    "source_document_id": "sd-aaa",
                    "question": "Q?",
                    "context_segments": [bad_segment],
                }
            ]
        )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    # The error must never echo the offending segment content.
    assert "x" + "Z" not in err
    assert "just-a-string" not in err


@pytest.mark.parametrize(
    ("ordinal", "expect"),
    [
        (True, "ordinal must be an integer"),
        ("0", "ordinal must be an integer"),
        (1.0, "ordinal must be an integer"),
        (-1, "non-negative"),
        (1, "must equal the segment index 0"),
    ],
)
def test_ordinal_contract_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    ordinal: object,
    expect: str,
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [
                    {"ordinal": ordinal, "text": "Unique text.", "section_label": "background"}
                ],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert expect in err


def test_ordinal_gap_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [
                    {"ordinal": 0, "text": "Alpha unique.", "section_label": "background"},
                    {"ordinal": 2, "text": "Beta unique.", "section_label": "methods"},
                ],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "must equal the segment index 1" in err


def test_ordinal_duplicate_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [
                    {"ordinal": 0, "text": "Alpha unique.", "section_label": "background"},
                    {"ordinal": 0, "text": "Beta unique.", "section_label": "methods"},
                ],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert "must equal the segment index 1" in err


@pytest.mark.parametrize(
    ("text", "expect"),
    [
        (123, "text must be a string"),
        ("   ", "text must be non-blank"),
        ("\t\n", "text must be non-blank"),
    ],
)
def test_text_contract_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    text: object,
    expect: str,
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [{"ordinal": 0, "text": text, "section_label": "background"}],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert expect in err


@pytest.mark.parametrize(
    ("label", "expect"),
    [(123, "section_label must be a string"), ("", "section_label must be non-blank")],
)
def test_section_label_contract_refused(
    operator: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    label: object,
    expect: str,
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Q?",
                "context_segments": [
                    {"ordinal": 0, "text": "Unique text.", "section_label": label}
                ],
            }
        ]
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    assert expect in err


# ---------------------------------------------------------------------------
# Q27 — write-once (fresh workspace creates exactly one artifact; reuse refused)
# ---------------------------------------------------------------------------


def test_fresh_workspace_creates_exactly_one_artifact(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    assert list(workspace.iterdir()) == [workspace / AUDIT_FILENAME]


def test_second_invocation_same_workspace_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    first_bytes = (workspace / AUDIT_FILENAME).read_bytes()

    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err)
    assert "already exists" in err
    assert (workspace / AUDIT_FILENAME).read_bytes() == first_bytes


def test_no_temporary_or_alias_report_file_created(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    names = [p.name for p in workspace.iterdir()]
    assert AUDIT_FILENAME in names
    for forbidden in (
        "leakage-audit-report.json",
        "leakage-audit.json.tmp",
        "leakage-audit.json.new",
    ):
        assert forbidden not in names


# ---------------------------------------------------------------------------
# Q29 — raw-text minimisation on the operator surface
# ---------------------------------------------------------------------------

_MARKER_QUESTION = "zzQmarker5773 question unique alpha?"
_MARKER_CONTEXT = "zzCmarker4661 patient context segment unique ??"


def _marker_source_records(env: Environment) -> None:
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": _MARKER_QUESTION,
                "context_segments": [_MARKER_CONTEXT],
            },
            {
                "original_example_id": "ex-002",
                "source_document_id": "sd-bbb",
                "question": "Prognosis question unique beta.",
                "context_segments": ["Unique segment beta."],
            },
        ]
    )


def test_scientific_markers_absent_from_stdout_stderr_and_report(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    _marker_source_records(env)
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    report_bytes = (workspace / AUDIT_FILENAME).read_bytes()
    for marker in (
        _MARKER_QUESTION.encode(),
        _MARKER_CONTEXT.encode(),
        b"zzQmarker5773",
        b"zzCmarker4661",
    ):
        assert marker not in report_bytes
        assert marker not in out.encode()
        assert marker not in err.encode()


def test_paths_not_emitted_into_stdout_or_report(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    workspace = tmp_path / "ws"
    code, out, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    report_bytes = (workspace / AUDIT_FILENAME).read_bytes()
    for driver_path in (str(env.source_records), str(workspace), str(env.repository)):
        encoded = driver_path.encode()
        assert encoded not in report_bytes
        assert encoded not in out.encode()
    # The source-record custody path must never be printed, and neither must
    # the workspace path.
    assert str(env.custody) not in out
    assert str(workspace) not in out


def test_markers_absent_from_exception_text(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path, operator)
    env.write_registry()
    env.write_manifest()
    _marker_source_records(env)
    # Append a record whose source_document_id is absent from the registry so
    # the operator refuses.  The marker text from the valid records must never
    # appear in the refusal message.
    env.source_records.write_bytes(
        env.source_records.read_bytes()
        + (
            json.dumps(
                {
                    "record": {
                        "schema_version": "mesc-pubmedqa-source/1",
                        "original_example_id": "ex-009",
                        "source_document_id": "sd-absent",
                        "question": "Do not echo me.",
                        "context_segments": ["Seg."],
                    }
                },
                sort_keys=True,
            )
            + "\n"
        ).encode()
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert_refused(code, out, err, workspace=workspace)
    for marker in (_MARKER_QUESTION, _MARKER_CONTEXT, "Do not echo me."):
        assert marker not in out
        assert marker not in err


# ---------------------------------------------------------------------------
# Q31 — structural classification is non-downgradable through the real operator
# ---------------------------------------------------------------------------


def _structural_finding(
    operator: ModuleType, root: Path, capsys: pytest.CaptureFixture[str]
) -> tuple[Environment, str]:
    env = _structural_environment(root, operator)
    workspace = root / "baseline-ws"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=workspace), capsys)
    assert code == 0
    audit = load_audit(workspace)
    structural = [f for f in audit["findings"] if f["finding_type"] == "exact_example"]
    assert len(structural) == 1
    assert structural[0]["classification"] == "confirmed_leakage"
    finding_id = structural[0]["finding_id"]
    assert isinstance(finding_id, str)
    return env, finding_id


def test_operator_exact_example_false_positive_downgrade_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env, finding_id = _structural_finding(operator, tmp_path / "case", capsys)
    ledger = tmp_path / "ledger.json"
    ledger.write_bytes(
        json.dumps(
            [
                {
                    "finding_id": finding_id,
                    "classification": "false_positive",
                    "evidence_reference": "evidence:review-1",
                }
            ]
        ).encode()
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator, env.audit_argv(workspace=workspace, ledger=ledger), capsys
    )
    assert_refused(code, out, err, workspace=workspace)
    assert "structural split violation" in err


def test_operator_exact_example_unresolved_downgrade_refused(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env, finding_id = _structural_finding(operator, tmp_path / "case", capsys)
    ledger = tmp_path / "ledger.json"
    ledger.write_bytes(
        json.dumps([{"finding_id": finding_id, "classification": "unresolved"}]).encode()
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator, env.audit_argv(workspace=workspace, ledger=ledger), capsys
    )
    assert_refused(code, out, err, workspace=workspace)
    assert "structural split violation" in err


def test_operator_source_document_ledger_attempt_is_fail_closed(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # The operator's registry join makes a cross-partition source_document
    # finding structurally unreachable, so any ledger claim about one must be
    # refused before any audit disposition is produced.
    env = Environment(tmp_path / "case", operator)
    env.write_registry()
    env.write_manifest()
    env.write_source_records()
    ledger = tmp_path / "ledger.json"
    ledger.write_bytes(
        json.dumps(
            [
                {
                    "finding_id": "mesc-pilot-01-leakage-finding/1:sha256:" + "f" * 64,
                    "classification": "false_positive",
                    "evidence_reference": "evidence:review-2",
                }
            ]
        ).encode()
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator, env.audit_argv(workspace=workspace, ledger=ledger), capsys
    )
    assert_refused(code, out, err, workspace=workspace)
    assert "unknown finding_id" in err


def test_operator_scientific_text_ledger_review_end_to_end(
    operator: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env = Environment(tmp_path / "case", operator)
    env.write_registry(
        [
            {
                "example_id": "mesc-pilot-01:ex-a",
                "source_document_id": "sd-aaa",
                "assigned_split": "train",
            },
            {
                "example_id": "mesc-pilot-01:ex-b",
                "source_document_id": "sd-bbb",
                "assigned_split": "validation",
            },
        ]
    )
    env.write_manifest()
    env.write_source_records(
        [
            {
                "original_example_id": "ex-001",
                "source_document_id": "sd-aaa",
                "question": "Identical question text?",
                "context_segments": ["Alpha segment unique."],
            },
            {
                "original_example_id": "ex-002",
                "source_document_id": "sd-bbb",
                "question": "Identical question text?",
                "context_segments": ["Beta segment unique."],
            },
        ]
    )
    baseline = tmp_path / "baseline"
    code, _, _ = run_operator(operator, env.audit_argv(workspace=baseline), capsys)
    assert code == 0
    audit = load_audit(baseline)
    question_findings = [f for f in audit["findings"] if f["finding_type"] == "exact_question"]
    assert question_findings
    ledger = tmp_path / "ledger.json"
    ledger.write_bytes(
        json.dumps(
            [
                {
                    "finding_id": f["finding_id"],
                    "classification": "false_positive",
                    "evidence_reference": "evidence:synthetic-review-0001",
                }
                for f in audit["findings"]
            ]
        ).encode()
    )
    workspace = tmp_path / "ws"
    code, out, err = run_operator(
        operator, env.audit_argv(workspace=workspace, ledger=ledger), capsys
    )
    assert code == 0
    assert err == ""
    assert "leaked=false" in out
    resolved = load_audit(workspace)
    assert resolved["leaked"] is False
    assert all(f["classification"] == "false_positive" for f in resolved["findings"])
