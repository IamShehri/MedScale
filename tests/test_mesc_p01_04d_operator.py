"""Synthetic qualification of the sole controlled P01-04D operator surface.

Every invocation here runs against freshly generated synthetic inputs under
``tmp_path``.  The identifiers ``A`` and ``B`` exercise the implemented operator
contracts only; they are not formal P01-04D Generation A or Generation B.  No
test reads a protected registry, an external real source-record file or any real
dataset, and no test authorizes P01-04D entry or execution.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

import pytest

import medscale.mesc as mesc_package
from medscale.mesc._formal_split_v1 import (
    ARTIFACT_FILENAMES,
    FormalInputIdentityError,
    FormalInventoryError,
    FormalWorkspaceSafetyError,
)
from test_mesc_formal_generation_v1 import SYNTHETIC_COMMIT, make_environment
from test_mesc_formal_split_v1 import write_synthetic_inputs  # noqa: F401 - shared fixture helper

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OPERATOR_PATH = REPOSITORY_ROOT / "scripts" / "mesc_p01_04d_operator.py"


def load_operator() -> ModuleType:
    """Import the operator script by path, exactly as an operator would run it."""
    spec = importlib.util.spec_from_file_location(
        "_mesc_p01_04d_operator_under_test", OPERATOR_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def operator() -> ModuleType:
    return load_operator()


def generate_argv(
    environment: dict[str, Path],
    *,
    generation: str,
    workspace: Path,
    commit: str = SYNTHETIC_COMMIT,
) -> list[str]:
    return [
        "generate",
        "--expected-canonical-commit",
        commit,
        "--repository-root",
        str(environment["repository"]),
        "--generation",
        generation,
        "--workspace",
        str(workspace),
        "--external-evidence-root",
        str(environment["external"]),
        "--future-evidence-root",
        str(environment["future"]),
        "--ordered-example-registry",
        str(environment["input:ordered_example_registry"]),
        "--source-document-registry",
        str(environment["input:source_document_registry"]),
        "--transformed-dataset-identity",
        str(environment["input:transformed_dataset_identity"]),
        "--source-records",
        str(environment["input:source_records"]),
        "--decision-record",
        str(environment["input:decision_record"]),
        "--python-version",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    ]


# ---------------------------------------------------------------------------
# Surface shape
# ---------------------------------------------------------------------------


def test_exactly_two_subcommands_and_no_third(operator: ModuleType) -> None:
    assert operator.COMMANDS == ("generate", "compare")
    parser = operator.build_parser()
    # argparse exposes no public accessor for its registered subcommands.
    subparser_actions = list(parser._subparsers._group_actions)
    assert len(subparser_actions) == 1
    choices = sorted(subparser_actions[0].choices)
    assert choices == ["compare", "generate"]
    assert len(choices) == 2


def test_unknown_subcommand_is_rejected(operator: ModuleType) -> None:
    with pytest.raises(SystemExit) as exit_info:
        operator.main(["verify"])
    assert exit_info.value.code != 0


def test_no_arguments_is_not_a_success(operator: ModuleType) -> None:
    assert operator.main([]) == 2


def test_generate_requires_explicit_generation_identity(operator: ModuleType) -> None:
    with pytest.raises(SystemExit):
        operator.main(["generate"])


def test_generate_rejects_an_unknown_generation_identity(
    tmp_path: Path, operator: ModuleType
) -> None:
    environment = make_environment(tmp_path)
    argv = generate_argv(environment, generation="A", workspace=tmp_path / "ws")
    argv[argv.index("--generation") + 1] = "C"
    with pytest.raises(SystemExit):
        operator.main(argv)


def test_generate_declares_no_input_path_defaults(operator: ModuleType) -> None:
    parser = operator.build_parser()
    generate_parser = parser._subparsers._group_actions[0].choices["generate"]
    required = {
        "--expected-canonical-commit",
        "--repository-root",
        "--generation",
        "--workspace",
        "--external-evidence-root",
        "--future-evidence-root",
        "--ordered-example-registry",
        "--source-document-registry",
        "--transformed-dataset-identity",
        "--source-records",
        "--decision-record",
        "--python-version",
    }
    declared = {option for action in generate_parser._actions for option in action.option_strings}
    assert required <= declared
    for action in generate_parser._actions:
        if action.dest == "help":
            continue
        assert action.required is True
        assert action.default is None


def test_compare_requires_both_workspaces(operator: ModuleType, tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        operator.main(["compare"])
    with pytest.raises(SystemExit):
        operator.main(["compare", "--generation-a-workspace", str(tmp_path)])


def test_operator_source_declares_no_environment_activation() -> None:
    source = OPERATOR_PATH.read_text(encoding="utf-8")
    for prohibited in ("os.environ", "getenv", "environ.get", "putenv"):
        assert prohibited not in source
    assert "argparse" in source


# ---------------------------------------------------------------------------
# Synthetic generation and comparison
# ---------------------------------------------------------------------------


def test_synthetic_generate_a_then_b_then_compare(
    tmp_path: Path, operator: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    environment = make_environment(tmp_path)
    workspace_a = tmp_path / "synthetic-a"
    workspace_b = tmp_path / "synthetic-b"

    assert operator.main(generate_argv(environment, generation="A", workspace=workspace_a)) == 0
    first = capsys.readouterr().out
    assert "generation A complete" in first

    assert operator.main(generate_argv(environment, generation="B", workspace=workspace_b)) == 0
    second = capsys.readouterr().out
    assert "generation B complete" in second

    for workspace in (workspace_a, workspace_b):
        assert sorted(entry.name for entry in workspace.iterdir()) == sorted(ARTIFACT_FILENAMES)

    exit_code = operator.main(
        [
            "compare",
            "--generation-a-workspace",
            str(workspace_a),
            "--generation-b-workspace",
            str(workspace_b),
        ]
    )
    assert exit_code == 0
    assert "comparison equal: 7 artifacts byte-identical" in capsys.readouterr().out
    for filename in ARTIFACT_FILENAMES:
        assert (workspace_a / filename).read_bytes() == (workspace_b / filename).read_bytes()


def test_one_invocation_performs_exactly_one_generation(
    tmp_path: Path, operator: ModuleType
) -> None:
    environment = make_environment(tmp_path)
    workspace_a = tmp_path / "only-a"
    operator.main(generate_argv(environment, generation="A", workspace=workspace_a))
    siblings = sorted(entry.name for entry in tmp_path.iterdir() if entry.is_dir())
    assert "only-a" in siblings
    assert not any(name.endswith("-b") or name == "only-b" for name in siblings)


def test_typed_failures_remain_non_success(tmp_path: Path, operator: ModuleType) -> None:
    environment = make_environment(tmp_path)
    argv = generate_argv(environment, generation="A", workspace=tmp_path / "ws", commit="f" * 40)
    with pytest.raises(FormalInputIdentityError):
        operator.main(argv)
    assert not (tmp_path / "ws").exists()

    reuse = tmp_path / "reused"
    reuse.mkdir()
    with pytest.raises(FormalWorkspaceSafetyError):
        operator.main(generate_argv(environment, generation="A", workspace=reuse))

    with pytest.raises(FormalInventoryError):
        operator.main(
            [
                "compare",
                "--generation-a-workspace",
                str(tmp_path / "absent-a"),
                "--generation-b-workspace",
                str(tmp_path / "absent-b"),
            ]
        )


def test_compare_writes_nothing_into_either_workspace(tmp_path: Path, operator: ModuleType) -> None:
    environment = make_environment(tmp_path)
    workspace_a = tmp_path / "cmp-a"
    workspace_b = tmp_path / "cmp-b"
    operator.main(generate_argv(environment, generation="A", workspace=workspace_a))
    operator.main(generate_argv(environment, generation="B", workspace=workspace_b))

    def snapshot(workspace: Path) -> dict[str, bytes]:
        return {entry.name: entry.read_bytes() for entry in sorted(workspace.iterdir())}

    before = (snapshot(workspace_a), snapshot(workspace_b))
    operator.main(
        [
            "compare",
            "--generation-a-workspace",
            str(workspace_a),
            "--generation-b-workspace",
            str(workspace_b),
        ]
    )
    assert (snapshot(workspace_a), snapshot(workspace_b)) == before


# ---------------------------------------------------------------------------
# Authority boundary
# ---------------------------------------------------------------------------


def test_no_public_medscale_export() -> None:
    assert "_formal_split_v1" not in mesc_package.__all__
    assert "_formal_generation_v1" not in mesc_package.__all__
    for name in mesc_package.__all__:
        assert "formal" not in name.lower()
    assert not hasattr(mesc_package, "FormalSplitRequest")
    assert not hasattr(mesc_package, "generate")


def test_no_console_script_or_cli_registration() -> None:
    configuration = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = configuration.get("project", {}).get("scripts", {})
    assert "mesc_p01_04d_operator" not in scripts
    for target in scripts.values():
        assert "formal" not in target
        assert "p01_04d" not in target
    text = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "mesc_p01_04d_operator" not in text


def test_cli_does_not_reference_the_formal_executor() -> None:
    cli_directory = REPOSITORY_ROOT / "src" / "medscale" / "cli"
    for module_path in sorted(cli_directory.glob("*.py")):
        source = module_path.read_text(encoding="utf-8")
        assert "_formal_split_v1" not in source
        assert "_formal_generation_v1" not in source
        assert "mesc_p01_04d_operator" not in source


def test_formal_modules_do_not_import_fixture_tooling() -> None:
    """The prohibition is on the import graph, not on prose that explains it.

    Both modules name the fixture surfaces in their docstrings precisely to record
    that those surfaces have no role in formal execution, so this walks the parsed
    import statements rather than scanning raw text.
    """
    prohibited = {
        "medscale.mesc._fixture_split_v1",
        "medscale.mesc._fixture_publication_v1",
    }
    prohibited_names = {
        "FixtureSplitFacade",
        "FixtureSplitRequest",
        "FixtureSplitResult",
        "SourceDocumentGroupedSplitter",
    }
    for name in ("_formal_split_v1.py", "_formal_generation_v1.py"):
        path = REPOSITORY_ROOT / "src" / "medscale" / "mesc" / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in prohibited
                    assert "_fixture_" not in alias.name
            elif isinstance(node, ast.ImportFrom):
                assert node.module not in prohibited
                assert "_fixture_" not in (node.module or "")
                for alias in node.names:
                    assert alias.name not in prohibited_names
        # No attribute access reaches the fixture facade or the public splitter.
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                assert node.attr not in prohibited_names


def test_help_invocations_perform_no_generation(tmp_path: Path) -> None:
    for argv in (["--help"], ["generate", "--help"], ["compare", "--help"]):
        completed = subprocess.run(
            [sys.executable, str(OPERATOR_PATH), *argv],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(tmp_path),
        )
        assert completed.returncode == 0
        assert "usage:" in completed.stdout
    assert sorted(tmp_path.iterdir()) == []


def test_subprocess_generate_and_compare_are_byte_identical(tmp_path: Path) -> None:
    """Three separate processes: synthetic A, synthetic B, then comparison."""
    environment = make_environment(tmp_path)
    workspace_a = tmp_path / "proc-a"
    workspace_b = tmp_path / "proc-b"

    def run(argv: Sequence[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(OPERATOR_PATH), *argv],
            capture_output=True,
            text=True,
            check=False,
        )

    first = run(generate_argv(environment, generation="A", workspace=workspace_a))
    assert first.returncode == 0, first.stderr
    second = run(generate_argv(environment, generation="B", workspace=workspace_b))
    assert second.returncode == 0, second.stderr
    comparison = run(
        [
            "compare",
            "--generation-a-workspace",
            str(workspace_a),
            "--generation-b-workspace",
            str(workspace_b),
        ]
    )
    assert comparison.returncode == 0, comparison.stderr
    assert "comparison equal: 7 artifacts byte-identical" in comparison.stdout
    for filename in ARTIFACT_FILENAMES:
        assert (workspace_a / filename).read_bytes() == (workspace_b / filename).read_bytes()
    manifest = json.loads((workspace_a / "generation-manifest.json").read_bytes())
    assert (
        manifest["split_fingerprint"]
        == json.loads((workspace_b / "split-summary.json").read_bytes())["split_fingerprint"]
    )


def test_subprocess_failure_is_non_zero_and_leaves_no_workspace(tmp_path: Path) -> None:
    environment = make_environment(tmp_path)
    workspace = tmp_path / "never"
    completed = subprocess.run(
        [
            sys.executable,
            str(OPERATOR_PATH),
            *generate_argv(environment, generation="A", workspace=workspace, commit="0" * 40),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "FormalInputIdentityError" in completed.stderr
    assert not workspace.exists()
