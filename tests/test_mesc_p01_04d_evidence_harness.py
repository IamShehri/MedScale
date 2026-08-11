"""Synthetic qualification of the P01-04D external execution-evidence harness.

Every fixture here is constructed inside ``tmp_path``.  No test reads P01-03G,
an external source record, a real dataset, a real generation workspace or real
external evidence.  No test executes the frozen canonical operator: the operator
is read for identity only, and every child process is a synthetic runner
injected through the harness's internal boundary.  Nothing here authorizes
P01-04D entry or execution.

The identifiers ``A`` and ``B`` exercise the harness contract only; they are not
formal P01-04D Generation A or Generation B.

``resolve_repository_commit`` is the sole formal execution-module import
permitted at test scope (evidence-contract §27, ``PIC-CORR-15``).  It is used
only as a differential reference oracle over synthetic repositories.  Every
contract literal below is an expected value taken from the P-A1 documents, never
one discovered by importing a formal module.
"""

from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from medscale.mesc._formal_generation_v1 import resolve_repository_commit

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = REPOSITORY_ROOT / "scripts" / "mesc_p01_04d_evidence_harness.py"
OPERATOR_PATH = REPOSITORY_ROOT / "scripts" / "mesc_p01_04d_operator.py"

# --- expected contract literals, taken from the P-A1 documents ---------------

EPISODE_ID = "episode-alpha"
SYNTHETIC_COMMIT = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
MOVED_COMMIT = "ffeeddccbbaa99887766554433221100aabbccdd"
SYNTHETIC_FINGERPRINT = "9f" * 32

EXPECTED_COMMANDS = ("open", "generate", "compare", "verify", "invalidate", "finalize")

EXPECTED_EVIDENCE_FILENAMES = (
    "episode-core.json",
    "stage-generate-a.jsonl",
    "stage-generate-b.jsonl",
    "stage-compare.jsonl",
    "stage-verify.jsonl",
    "episode-invalidation.jsonl",
    "episode-manifest.json",
)

PROHIBITED_EVIDENCE_FILENAMES = (
    "episode-control.jsonl",
    "repository-observation.jsonl",
    "preflight.jsonl",
    "failure.jsonl",
    "control.json",
    "status.json",
    "state.json",
    "lock.json",
    "retry.json",
    "repair.json",
    "crash.json",
    "containment.json",
    "terminal-failure.json",
    "structural-unseal.json",
)

EXPECTED_CANDIDATE_FILENAMES = (
    "split-policy.json",
    "group-registry.jsonl",
    "example-registry.jsonl",
    "excluded-ledger.json",
    "split-summary-identity-core.json",
    "split-summary.json",
    "generation-manifest.json",
)

EXPECTED_INPUT_SURFACES = (
    "ordered_example_registry",
    "source_document_registry",
    "transformed_dataset_identity",
    "source_records",
    "decision_record",
)

EXPECTED_PATH_ROLES = (
    "FORMAL_INPUT_ORDERED_EXAMPLE_REGISTRY",
    "FORMAL_INPUT_SOURCE_DOCUMENT_REGISTRY",
    "FORMAL_INPUT_TRANSFORMED_DATASET_IDENTITY",
    "FORMAL_INPUT_SOURCE_RECORDS",
    "FORMAL_INPUT_DECISION_RECORD",
)

EXPECTED_VOCABULARY_SIZES = {
    "root_cause_class": 15,
    "causal_stage": 8,
    "failure_class": 21,
    "remediation_disposition": 4,
    "record_integrity": 2,
    "comparison_disposition": 4,
    "terminal_disposition": 5,
    "operator_error_class": 11,
    "stage_disposition": 3,
    "path_role": 5,
}

EXPECTED_REFUSAL_FAILURE_CLASSES = frozenset(
    {
        "CANONICAL_MAIN_MISMATCH",
        "HARNESS_IDENTITY_MISMATCH",
        "OPERATOR_IDENTITY_MISMATCH",
        "RUNTIME_IDENTITY_MISMATCH",
        "INPUT_IDENTITY_MISMATCH",
    }
)

# The exact §19.1 table, transcribed from the P-A1 contract.
EXPECTED_FAILURE_TRIAD = {
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
    "EPISODE_PATH_IDENTITY_DRIFT": ("PATH_SAFETY_FAILURE", "FOUNDER_DISPOSITION_REQUIRED"),
    "UNCLASSIFIED": ("UNDETERMINED", "FOUNDER_DISPOSITION_REQUIRED"),
}

# The exact §19.2 table, total over the eleven operator_error_class values.
EXPECTED_CHILD_NONZERO_TRIAD = {
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
    "NO_ERROR": ("UNDETERMINED", "FOUNDER_DISPOSITION_REQUIRED"),
}

# The exact ten allowlisted tokens of §20.8.1.
EXPECTED_EXCEPTION_TOKENS = {
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

EXPECTED_EXCEPTION_MODULE = "medscale.mesc._formal_split_v1"
EXPECTED_EXCEPTION_PREFIX = b"medscale.mesc._formal_split_v1."

TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")

_MODULE_COUNTER = itertools.count()


# ---------------------------------------------------------------------------
# Synthetic fixtures — every byte is constructed here
# ---------------------------------------------------------------------------


def load_harness(path: Path) -> ModuleType:
    """Import a harness script by path, exactly as an operator would run it."""
    name = f"_mesc_p01_04d_evidence_harness_under_test_{next(_MODULE_COUNTER)}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_synthetic_git(root: Path, commit: str = SYNTHETIC_COMMIT) -> None:
    """Create a synthetic ``.git`` directory on a normal branch."""
    heads = root / ".git" / "refs" / "heads"
    heads.mkdir(parents=True, exist_ok=True)
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (heads / "main").write_text(f"{commit}\n", encoding="utf-8")


def write_synthetic_repository(root: Path, commit: str = SYNTHETIC_COMMIT) -> None:
    """Create a synthetic repository carrying its own harness and operator copies."""
    write_synthetic_git(root, commit)
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HARNESS_PATH, scripts / HARNESS_PATH.name)
    shutil.copyfile(OPERATOR_PATH, scripts / OPERATOR_PATH.name)


def write_workspace(
    workspace: Path,
    *,
    fingerprint: str = SYNTHETIC_FINGERPRINT,
    drift: str | None = None,
    omit: str | None = None,
    manifest_payload: bytes | None = None,
) -> None:
    """Materialize a synthetic seven-file candidate bundle."""
    workspace.mkdir(parents=True, exist_ok=True)
    for filename in EXPECTED_CANDIDATE_FILENAMES:
        if filename == omit:
            continue
        if filename == "generation-manifest.json":
            payload = (
                manifest_payload
                if manifest_payload is not None
                else json.dumps({"split_fingerprint": fingerprint}, sort_keys=True).encode("utf-8")
                + b"\n"
            )
        else:
            payload = f"synthetic {filename}\n".encode()
        if filename == drift:
            payload += b"synthetic drift\n"
        (workspace / filename).write_bytes(payload)


def digest_tree(root: Path) -> dict[str, str]:
    """Return a filename to SHA-256 map for every file under a directory."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _event_of(payload: bytes) -> str:
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ""
    return str(decoded.get("event", "")) if isinstance(decoded, dict) else ""


def make_store(
    module: ModuleType,
    *,
    clean_failures: Iterable[str] = (),
    partial_failures: Iterable[str] = (),
) -> Any:
    """Return an evidence store that injects controlled append failures.

    ``clean_failures`` add or change no byte, so the journal stays well formed.
    ``partial_failures`` leave partial bytes, which must be preserved exactly.
    """
    clean = set(clean_failures)
    partial = set(partial_failures)

    class _InjectingStore(module.EvidenceStore):  # type: ignore[misc,name-defined]
        def append(self, path: Path, payload: bytes) -> None:
            event = _event_of(payload)
            if event in clean:
                raise OSError("synthetic clean append failure")
            if event in partial:
                super().append(path, payload[: len(payload) // 2])
                raise OSError("synthetic partial append failure")
            super().append(path, payload)

    return _InjectingStore()


def make_runner(
    module: ModuleType,
    *,
    exit_code: int = 0,
    stdout: bytes = b"synthetic stdout\n",
    stderr: bytes = b"",
    launch_failure: bool = False,
    on_run: Callable[[Sequence[str]], None] | None = None,
) -> Any:
    """Return a synthetic child runner. The frozen operator is never executed."""

    class _SyntheticRunner(module.ChildRunner):  # type: ignore[misc,name-defined]
        def run(self, command: Sequence[str]) -> Any:
            if launch_failure:
                raise module.ChildLaunchFailureError("synthetic process creation failure")
            if on_run is not None:
                on_run(command)
            return module.ChildOutcome(
                pid=4242,
                started_at="2026-01-01T00:00:00.000000Z",
                exited_at="2026-01-01T00:00:01.500000Z",
                exit_code=exit_code,
                elapsed_ms=1500,
                stdout=stdout,
                stderr=stderr,
            )

    return _SyntheticRunner()


@dataclass
class Lab:
    """One synthetic repository, evidence root, workspace pair and input set."""

    module: ModuleType
    repository_root: Path
    evidence_root: Path
    workspace_a: Path
    workspace_b: Path
    future_evidence_root: Path
    inputs: dict[str, Path]
    episode_id: str = EPISODE_ID
    _extra: dict[str, Path] = field(default_factory=dict)
    #: The operator's custody of the continuity token. It lives here, in the
    #: caller, exactly as it lives in the operator's hands in production — never
    #: inside the episode directory (founder-authorization.md §8D).
    continuity: str = ""

    def _continuity_tail(self, continuity: str | None) -> list[str]:
        return ["--expect-continuity", self.continuity if continuity is None else continuity]

    @property
    def directory(self) -> Path:
        return self.evidence_root / self.episode_id

    def set_head(self, commit: str) -> None:
        (self.repository_root / ".git" / "refs" / "heads" / "main").write_text(
            f"{commit}\n", encoding="utf-8"
        )

    def open_argv(self, commit: str = SYNTHETIC_COMMIT) -> list[str]:
        return [
            "open",
            "--episode-id",
            self.episode_id,
            "--repository-root",
            str(self.repository_root),
            "--external-evidence-root",
            str(self.evidence_root),
            "--expected-canonical-commit",
            commit,
        ]

    def generate_argv(self, generation: str, *, continuity: str | None = None) -> list[str]:
        workspace = self.workspace_a if generation == "A" else self.workspace_b
        argv = [
            "generate",
            "--episode-id",
            self.episode_id,
            "--repository-root",
            str(self.repository_root),
            "--external-evidence-root",
            str(self.evidence_root),
            "--generation",
            generation,
            "--workspace",
            str(workspace),
            "--future-evidence-root",
            str(self.future_evidence_root),
        ]
        argv.extend(self._continuity_tail(continuity))
        for surface in EXPECTED_INPUT_SURFACES:
            argv.extend([f"--{surface.replace('_', '-')}", str(self.inputs[surface])])
        return argv

    def _comparison_argv(self, command: str, continuity: str | None = None) -> list[str]:
        return [
            command,
            "--episode-id",
            self.episode_id,
            "--repository-root",
            str(self.repository_root),
            "--external-evidence-root",
            str(self.evidence_root),
            "--generation-a-workspace",
            str(self.workspace_a),
            "--generation-b-workspace",
            str(self.workspace_b),
            *self._continuity_tail(continuity),
        ]

    def compare_argv(self, *, continuity: str | None = None) -> list[str]:
        return self._comparison_argv("compare", continuity)

    def verify_argv(self, *, continuity: str | None = None) -> list[str]:
        return self._comparison_argv("verify", continuity)

    def invalidate_argv(
        self,
        *,
        failure_class: str,
        causal_stage: str,
        operator_error_class: str | None = None,
        workspace: Path | None = None,
        continuity: str | None = None,
    ) -> list[str]:
        argv = [
            "invalidate",
            "--episode-id",
            self.episode_id,
            "--repository-root",
            str(self.repository_root),
            "--external-evidence-root",
            str(self.evidence_root),
            "--failure-class",
            failure_class,
            "--causal-stage",
            causal_stage,
            *self._continuity_tail(continuity),
        ]
        if operator_error_class is not None:
            argv.extend(["--operator-error-class", operator_error_class])
        if workspace is not None:
            argv.extend(["--affected-candidate-workspace", str(workspace)])
        return argv

    def finalize_argv(self, *, continuity: str | None = None) -> list[str]:
        return [
            "finalize",
            "--episode-id",
            self.episode_id,
            "--repository-root",
            str(self.repository_root),
            "--external-evidence-root",
            str(self.evidence_root),
            *self._continuity_tail(continuity),
        ]

    def run(
        self,
        argv: Sequence[str],
        *,
        store: Any = None,
        runner: Any = None,
    ) -> int:
        """Dispatch one command, taking custody of any continuity token it emits.

        Capturing stdout here is what models the operator: the next token is read
        off the command's output and held by the caller. Nothing reads it back
        from the episode directory, because nothing ever writes it there.
        """
        arguments = self.module.build_parser().parse_args(list(argv))
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exit_code: int = self.module.dispatch(
                    arguments,
                    store=store if store is not None else self.module.EvidenceStore(),
                    runner=runner if runner is not None else self.module.ChildRunner(),
                )
        finally:
            reported = buffer.getvalue()
            sys.stdout.write(reported)
            self._take_continuity(reported)
        return exit_code

    def resync_continuity(self) -> None:
        """Re-derive the operator's token from the episode as it now stands.

        Scaffolding for tests whose subject is something *other* than continuity
        — TM-1 classification, structural barriers, stage-open residue, injected
        identity drift — which reach their fixture by editing the episode
        directory out of band. In production the operator would simply be holding
        the token the last legitimate command emitted for that state.

        It is never used by a test that exercises the continuity control itself:
        calling it there would hand the attacker the very value the anchor exists
        to withhold, and the test would prove nothing.
        """
        identity = self.module.measure_episode_path_identity(self.directory)
        self.continuity = self.module.measure_continuity_token(self.directory, identity)

    def _take_continuity(self, reported: str) -> None:
        # ``getattr`` so the same driver can also run a build that predates the
        # anchor, which is how the discriminator exercises the vulnerable base.
        label = getattr(self.module, "CONTINUITY_TOKEN_LABEL", "continuity_token")
        for line in reported.splitlines():
            head, _, value = line.partition(" ")
            if head == label:
                self.continuity = value.strip()

    def emitted_tokens(self, argv: Sequence[str], **kwargs: Any) -> list[str]:
        """Run a command and return every continuity token it printed."""
        buffer = io.StringIO()
        arguments = self.module.build_parser().parse_args(list(argv))
        with contextlib.redirect_stdout(buffer):
            self.module.dispatch(
                arguments,
                store=kwargs.get("store") or self.module.EvidenceStore(),
                runner=kwargs.get("runner") or self.module.ChildRunner(),
            )
        label = self.module.CONTINUITY_TOKEN_LABEL
        found = [
            line.partition(" ")[2].strip()
            for line in buffer.getvalue().splitlines()
            if line.partition(" ")[0] == label
        ]
        if found:
            self.continuity = found[-1]
        return found

    def journal(self, filename: str) -> list[dict[str, object]]:
        payload = (self.directory / filename).read_bytes()
        return [json.loads(line) for line in payload.split(b"\n") if line]

    def core(self) -> dict[str, object]:
        decoded = json.loads((self.directory / "episode-core.json").read_text(encoding="utf-8"))
        assert isinstance(decoded, dict)
        return decoded

    def manifest(self) -> dict[str, object]:
        decoded = json.loads((self.directory / "episode-manifest.json").read_text(encoding="utf-8"))
        assert isinstance(decoded, dict)
        return decoded

    # -- composite drivers ---------------------------------------------------

    def producing_runner(self, generation: str, **kwargs: Any) -> Any:
        workspace = self.workspace_a if generation == "A" else self.workspace_b
        fingerprint = str(kwargs.pop("fingerprint", SYNTHETIC_FINGERPRINT))
        drift = kwargs.pop("drift", None)
        return make_runner(
            self.module,
            on_run=lambda _command: write_workspace(
                workspace,
                fingerprint=fingerprint,
                drift=str(drift) if drift is not None else None,
            ),
            **kwargs,
        )

    def open_episode(self) -> None:
        assert self.run(self.open_argv()) == 0

    def generate_both(self, *, drift: str | None = None, fingerprint_b: str | None = None) -> None:
        assert self.run(self.generate_argv("A"), runner=self.producing_runner("A")) == 0
        runner_b = self.producing_runner(
            "B",
            drift=drift,
            fingerprint=fingerprint_b if fingerprint_b is not None else SYNTHETIC_FINGERPRINT,
        )
        assert self.run(self.generate_argv("B"), runner=runner_b) == 0

    def complete_success(self) -> None:
        self.open_episode()
        self.generate_both()
        assert self.run(self.compare_argv(), runner=make_runner(self.module)) == 0
        assert self.run(self.verify_argv(), runner=make_runner(self.module)) == 0


@pytest.fixture
def lab(tmp_path: Path) -> Lab:
    """Build a fresh synthetic laboratory whose harness runs from the synthetic repo."""
    repository_root = tmp_path / "repo"
    write_synthetic_repository(repository_root)
    module = load_harness(repository_root / "scripts" / HARNESS_PATH.name)

    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    future_evidence_root = tmp_path / "future-evidence"
    future_evidence_root.mkdir()
    inputs_directory = tmp_path / "inputs"
    inputs_directory.mkdir()
    inputs: dict[str, Path] = {}
    for surface in EXPECTED_INPUT_SURFACES:
        path = inputs_directory / f"{surface}.jsonl"
        path.write_bytes(f"synthetic {surface}\n".encode())
        inputs[surface] = path
    return Lab(
        module=module,
        repository_root=repository_root,
        evidence_root=evidence_root,
        workspace_a=tmp_path / "workspace-a",
        workspace_b=tmp_path / "workspace-b",
        future_evidence_root=future_evidence_root,
        inputs=inputs,
    )


@pytest.fixture
def harness() -> ModuleType:
    """The real repository harness, for pure-function qualification."""
    return load_harness(HARNESS_PATH)


def try_symlink(link: Path, target: Path, *, directory: bool = True) -> bool:
    """Create a symlink where the platform permits it, reporting whether it exists."""
    try:
        link.symlink_to(target, target_is_directory=directory)
    except (OSError, NotImplementedError):
        return False
    return link.is_symlink()


# ===========================================================================
# A. CLI surface
# ===========================================================================


def test_exactly_six_commands(harness: ModuleType) -> None:
    assert harness.COMMANDS == EXPECTED_COMMANDS
    assert len(harness.COMMANDS) == 6


def test_parser_exposes_exactly_the_six_commands(harness: ModuleType) -> None:
    parser = harness.build_parser()
    actions = [action for action in parser._subparsers._group_actions if hasattr(action, "choices")]
    assert tuple(actions[0].choices) == EXPECTED_COMMANDS


@pytest.mark.parametrize(
    "name",
    [
        "run",
        "execute",
        "repair",
        "resume",
        "recover",
        "status",
        "inspect",
        "replay",
        "seal",
        "retry",
        "record-freeze",
    ],
)
def test_prohibited_command_is_absent(harness: ModuleType, name: str) -> None:
    with pytest.raises(SystemExit) as caught:
        harness.build_parser().parse_args([name, "--episode-id", "x"])
    assert caught.value.code == 2


def test_missing_required_argument_is_refused(harness: ModuleType) -> None:
    with pytest.raises(SystemExit) as caught:
        harness.build_parser().parse_args(["open", "--episode-id", EPISODE_ID])
    assert caught.value.code == 2


def test_no_command_prints_usage(harness: ModuleType) -> None:
    assert harness.main([]) == 2


def test_argument_refusal_creates_no_evidence(lab: Lab) -> None:
    argv = lab.open_argv()
    argv[argv.index(lab.episode_id)] = "Bad_Episode_ID"
    with pytest.raises(lab.module.ArgumentRefusalError):
        lab.run(argv)
    assert list(lab.evidence_root.iterdir()) == []


def test_main_reports_closed_vocabulary_and_fails_closed(
    lab: Lab, capsys: pytest.CaptureFixture[str]
) -> None:
    argv = lab.open_argv(commit="not-a-commit")
    assert lab.module.main(argv) == 1
    assert "ARGUMENT_REFUSAL" in capsys.readouterr().err
    assert list(lab.evidence_root.iterdir()) == []


# ===========================================================================
# B. Evidence inventory
# ===========================================================================


def test_evidence_inventory_is_exactly_seven(harness: ModuleType) -> None:
    assert harness.EVIDENCE_FILENAMES == EXPECTED_EVIDENCE_FILENAMES
    assert len(harness.EVIDENCE_FILENAMES) == 7


def test_successful_episode_creates_no_eighth_file(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    present = sorted(entry.name for entry in lab.directory.iterdir())
    assert present == sorted(set(EXPECTED_EVIDENCE_FILENAMES) - {"episode-invalidation.jsonl"})


@pytest.mark.parametrize("filename", PROHIBITED_EVIDENCE_FILENAMES)
def test_prohibited_evidence_file_is_never_created(lab: Lab, filename: str) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert not (lab.directory / filename).exists()


def test_evidence_is_written_only_under_the_evidence_root(lab: Lab) -> None:
    before = digest_tree(lab.repository_root)
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert digest_tree(lab.repository_root) == before
    assert list(lab.future_evidence_root.iterdir()) == []


# ===========================================================================
# C. Canonical serialization
# ===========================================================================


def test_episode_core_bytes_are_canonical(lab: Lab) -> None:
    lab.open_episode()
    payload = (lab.directory / "episode-core.json").read_bytes()
    assert b"\r" not in payload
    assert payload.endswith(b"\n")
    assert payload.count(b"\n") == 1
    decoded = json.loads(payload.decode("utf-8"))
    assert (
        payload
        == json.dumps(decoded, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        + b"\n"
    )


def test_journal_lines_are_canonical_jsonl(lab: Lab) -> None:
    lab.complete_success()
    for filename in ("stage-generate-a.jsonl", "stage-compare.jsonl", "stage-verify.jsonl"):
        payload = (lab.directory / filename).read_bytes()
        assert b"\r" not in payload
        assert payload.endswith(b"\n")
        assert b"\n\n" not in payload
        for line in payload.split(b"\n")[:-1]:
            decoded = json.loads(line.decode("utf-8"))
            assert line == json.dumps(
                decoded, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode("utf-8")


def test_manifest_bytes_are_canonical(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    payload = (lab.directory / "episode-manifest.json").read_bytes()
    assert b"\r" not in payload
    assert payload.endswith(b"\n")
    assert payload.count(b"\n") == 1


def test_every_timestamp_uses_the_exact_utc_form(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert TIMESTAMP_PATTERN.match(str(lab.manifest()["manifest_sealed_at"]))
    for event in lab.journal("stage-generate-a.jsonl"):
        for key in ("started_at", "exited_at"):
            if key in event:
                assert TIMESTAMP_PATTERN.match(str(event[key]))
    assert TIMESTAMP_PATTERN.match(lab.module.utc_timestamp())


def test_serialization_is_deterministic_across_key_order(harness: ModuleType) -> None:
    first = harness.build_episode_core(
        episode_id=EPISODE_ID,
        expected_canonical_commit=SYNTHETIC_COMMIT,
        repository_root=Path("/synthetic/repo"),
        external_evidence_root=Path("/synthetic/evidence"),
        operator=harness.ArtifactIdentity("0" * 64, 11),
        harness=harness.ArtifactIdentity("1" * 64, 22),
        runtime=harness.RuntimeIdentity("/python", "2" * 64, 33, "3.11.15", "CPython"),
    )
    second = dict(reversed(list(first.items())))
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    assert canonical_json_bytes(first) == canonical_json_bytes(second)


# ===========================================================================
# D. Episode open
# ===========================================================================


def test_open_creates_the_exact_closed_core_field_set(lab: Lab) -> None:
    lab.open_episode()
    core = lab.core()
    assert tuple(sorted(core)) == tuple(sorted(lab.module.EPISODE_CORE_FIELDS))
    assert core["schema_version"] == "mesc-p01-04d-execution-evidence/episode-core/v1"
    assert core["operator_relative_path"] == "scripts/mesc_p01_04d_operator.py"
    assert "/" in str(core["operator_relative_path"])
    assert core["expected_canonical_commit"] == SYNTHETIC_COMMIT


def test_core_carries_no_repository_observation_field(lab: Lab) -> None:
    lab.open_episode()
    core = lab.core()
    assert "observed_canonical_commit" not in core
    assert "identity_match" not in core


def test_open_is_write_once(lab: Lab) -> None:
    lab.open_episode()
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.open_argv())


def test_open_refuses_on_canonical_main_mismatch_and_creates_nothing(lab: Lab) -> None:
    lab.set_head(MOVED_COMMIT)
    with pytest.raises(lab.module.CanonicalMainMismatchError):
        lab.run(lab.open_argv())
    assert not lab.directory.exists()
    assert list(lab.evidence_root.iterdir()) == []


@pytest.mark.parametrize(
    "episode_id", ["ab", "UPPER", "has space", "../escape", "..", "a" * 65, "a/b", "a\b"]
)
def test_open_refuses_an_unsafe_episode_id(lab: Lab, episode_id: str) -> None:
    lab.episode_id = episode_id
    with pytest.raises(lab.module.ArgumentRefusalError):
        lab.run(lab.open_argv())
    assert list(lab.evidence_root.iterdir()) == []


@pytest.mark.parametrize("episode_id", ["-leading", "ab", "UPPER", "../escape", "a" * 65])
def test_episode_id_rule_refuses_unsafe_identifiers(harness: ModuleType, episode_id: str) -> None:
    with pytest.raises(harness.ArgumentRefusalError):
        harness.require_episode_id(episode_id)


@pytest.mark.parametrize("episode_id", ["abc", "episode-alpha", "a1b2", "0start", "a" * 64])
def test_episode_id_rule_accepts_safe_identifiers(harness: ModuleType, episode_id: str) -> None:
    assert harness.require_episode_id(episode_id) == episode_id


def test_episode_identity_is_the_digest_of_the_core_bytes(lab: Lab) -> None:
    lab.open_episode()
    payload = (lab.directory / "episode-core.json").read_bytes()
    expected = hashlib.sha256(payload).hexdigest()
    lab.generate_both()
    assert lab.journal("stage-generate-a.jsonl")[0]["episode_identity"] == expected


# ===========================================================================
# E. Repository identity — differential oracle
# ===========================================================================


def test_resolver_matches_oracle_on_a_normal_branch(harness: ModuleType, tmp_path: Path) -> None:
    write_synthetic_git(tmp_path)
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


def test_resolver_matches_oracle_on_detached_head(harness: ModuleType, tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "HEAD").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


def test_resolver_matches_oracle_on_packed_refs(harness: ModuleType, tmp_path: Path) -> None:
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git / "packed-refs").write_text(
        f"# pack-refs with: peeled\n{SYNTHETIC_COMMIT} refs/heads/main\n", encoding="utf-8"
    )
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


def test_resolver_matches_oracle_on_a_tag_reference(harness: ModuleType, tmp_path: Path) -> None:
    git = tmp_path / ".git"
    (git / "refs" / "tags").mkdir(parents=True)
    (git / "HEAD").write_text("ref: refs/tags/v1\n", encoding="utf-8")
    (git / "refs" / "tags" / "v1").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


def test_resolver_matches_oracle_on_gitdir_pointer_with_commondir(
    harness: ModuleType, tmp_path: Path
) -> None:
    common = tmp_path / "common.git"
    (common / "refs" / "heads").mkdir(parents=True)
    (common / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")
    worktree_git = tmp_path / "worktrees" / "one"
    worktree_git.mkdir(parents=True)
    (worktree_git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (worktree_git / "commondir").write_text(f"{common}\n", encoding="utf-8")
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / ".git").write_text(f"gitdir: {worktree_git}\n", encoding="utf-8")
    assert harness.resolve_canonical_commit(checkout) == resolve_repository_commit(checkout)


@pytest.mark.parametrize(
    "shape",
    ["not-a-repository", "missing-head", "unresolvable-ref", "malformed-commit", "bad-gitdir"],
)
def test_resolver_and_oracle_both_fail_closed(
    harness: ModuleType, tmp_path: Path, shape: str
) -> None:
    root = tmp_path / shape
    root.mkdir()
    if shape == "missing-head":
        (root / ".git").mkdir()
    elif shape == "unresolvable-ref":
        (root / ".git").mkdir()
        (root / ".git" / "HEAD").write_text("ref: refs/heads/absent\n", encoding="utf-8")
    elif shape == "malformed-commit":
        (root / ".git").mkdir()
        (root / ".git" / "HEAD").write_text("zz\n", encoding="utf-8")
    elif shape == "bad-gitdir":
        (root / ".git").write_text("not a pointer\n", encoding="utf-8")
    with pytest.raises(harness.HarnessError):
        harness.resolve_canonical_commit(root)
    with pytest.raises(Exception, match=r".*"):
        resolve_repository_commit(root)


def test_resolver_refuses_a_reparse_shape_the_oracle_resolves(
    harness: ModuleType, tmp_path: Path
) -> None:
    real = tmp_path / "real"
    real.mkdir()
    write_synthetic_git(real)
    link = tmp_path / "linked"
    if not try_symlink(link, real):
        pytest.skip("this platform does not permit unprivileged directory symlinks")
    # The oracle resolves the redirect; the harness is required to refuse it.
    assert resolve_repository_commit(link) == SYNTHETIC_COMMIT
    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(link)


def test_resolver_reads_refs_without_invoking_git(harness: ModuleType, tmp_path: Path) -> None:
    write_synthetic_git(tmp_path, commit=MOVED_COMMIT)
    assert harness.resolve_canonical_commit(tmp_path) == MOVED_COMMIT


# ===========================================================================
# F. Path safety
# ===========================================================================


def test_evidence_root_inside_the_repository_is_refused(lab: Lab) -> None:
    inside = lab.repository_root / "evidence"
    inside.mkdir()
    lab.evidence_root = inside
    with pytest.raises(lab.module.PathSeparationRefusalError):
        lab.run(lab.open_argv())


def test_sibling_prefix_directory_is_not_treated_as_inside(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    write_synthetic_repository(repository_root)
    module = load_harness(repository_root / "scripts" / HARNESS_PATH.name)
    sibling = tmp_path / "repository-other"
    sibling.mkdir()
    assert not module.is_within(sibling.resolve(), repository_root.resolve())
    module.validate_evidence_root(sibling.resolve(), repository_root.resolve())


def test_workspace_overlapping_the_evidence_root_is_refused(lab: Lab) -> None:
    lab.open_episode()
    lab.workspace_a = lab.evidence_root / "workspace-a"
    with pytest.raises(lab.module.PathSeparationRefusalError):
        lab.run(lab.generate_argv("A"))


def test_future_evidence_root_overlapping_the_evidence_root_is_refused(lab: Lab) -> None:
    lab.open_episode()
    lab.future_evidence_root = lab.evidence_root / "future"
    lab.future_evidence_root.mkdir()
    with pytest.raises(lab.module.PathSeparationRefusalError):
        lab.run(lab.generate_argv("A"))


def test_relative_path_is_refused(lab: Lab) -> None:
    with pytest.raises(lab.module.PathSeparationRefusalError):
        lab.module.resolve_safe_path("relative/evidence")


def test_absent_evidence_root_is_refused(lab: Lab) -> None:
    lab.evidence_root = lab.evidence_root.parent / "absent-evidence"
    with pytest.raises(lab.module.ArgumentRefusalError):
        lab.run(lab.open_argv())


def test_reparse_evidence_root_is_refused(lab: Lab, tmp_path: Path) -> None:
    link = tmp_path / "evidence-link"
    if not try_symlink(link, lab.evidence_root):
        pytest.skip("this platform does not permit unprivileged directory symlinks")
    lab.evidence_root = link
    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.run(lab.open_argv())


def test_reparse_detection_walks_every_path_component(
    harness: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Cover the reparse refusal where the platform forbids creating a real symlink."""
    target = tmp_path / "outer" / "inner" / "leaf"
    target.mkdir(parents=True)
    flagged = tmp_path / "outer"
    monkeypatch.setattr(harness, "is_reparse_point", lambda path: path == flagged)
    with pytest.raises(harness.ReparsePointRefusalError):
        harness.require_no_reparse(target)
    monkeypatch.setattr(harness, "is_reparse_point", lambda path: False)
    assert harness.require_no_reparse(target) == target


def test_reparse_refusal_blocks_the_resolver(
    harness: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_synthetic_git(tmp_path)
    assert harness.resolve_canonical_commit(tmp_path) == SYNTHETIC_COMMIT
    monkeypatch.setattr(harness, "is_reparse_point", lambda path: path == tmp_path / ".git")
    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(tmp_path)


def test_reparse_refusal_blocks_open(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    evidence_root = lab.evidence_root
    monkeypatch.setattr(lab.module, "is_reparse_point", lambda path: path == evidence_root)
    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.run(lab.open_argv())
    assert list(lab.evidence_root.iterdir()) == []


def test_reparse_refusal_maps_to_the_path_safety_triad(harness: ModuleType) -> None:
    assert harness.ReparsePointRefusalError.failure_class == "REPARSE_POINT_REFUSAL"
    assert harness.derive_failure_triad("REPARSE_POINT_REFUSAL") == (
        "REPARSE_POINT_REFUSAL",
        "PATH_SAFETY_FAILURE",
        "NEW_EPISODE_REQUIRED",
    )


def test_containment_is_component_based(harness: ModuleType) -> None:
    assert harness.is_within(Path("/tmp/repo/inner"), Path("/tmp/repo"))
    assert harness.is_within(Path("/tmp/repo"), Path("/tmp/repo"))
    assert not harness.is_within(Path("/tmp/repository-other"), Path("/tmp/repo"))


# ===========================================================================
# G. Harness, operator and runtime identity
# ===========================================================================


def test_harness_identity_binds_the_running_bytes(lab: Lab) -> None:
    identity = lab.module.resolve_harness_identity(lab.repository_root)
    running = Path(str(lab.module.__file__)).resolve()
    assert identity.sha256 == hashlib.sha256(running.read_bytes()).hexdigest()
    assert identity.byte_size == running.stat().st_size


def test_harness_identity_refuses_a_foreign_repository(lab: Lab, tmp_path: Path) -> None:
    other = tmp_path / "other-repo"
    write_synthetic_repository(other)
    with pytest.raises(lab.module.HarnessIdentityMismatchError):
        lab.module.resolve_harness_identity(other)


def test_missing_operator_is_refused(lab: Lab, tmp_path: Path) -> None:
    bare = tmp_path / "bare"
    (bare / "scripts").mkdir(parents=True)
    with pytest.raises(lab.module.OperatorIdentityMismatchError):
        lab.module.resolve_operator_identity(bare)


def test_operator_is_never_imported_only_hashed(lab: Lab) -> None:
    identity = lab.module.resolve_operator_identity(lab.repository_root)
    operator = lab.repository_root / "scripts" / OPERATOR_PATH.name
    assert identity.sha256 == hashlib.sha256(operator.read_bytes()).hexdigest()
    assert not any(
        "operator" in name for name in sys.modules if name.startswith("_mesc_p01_04d_op")
    )


def test_runtime_identity_has_exactly_five_fields(lab: Lab) -> None:
    fields = lab.module.resolve_runtime_identity().as_fields()
    assert tuple(sorted(fields)) == (
        "python_executable_byte_size",
        "python_executable_sha256",
        "python_implementation",
        "python_version",
        "resolved_python_executable_path",
    )
    assert len(fields) == 5


def _rewrite_core(lab: Lab, **changes: object) -> None:
    """Simulate identity drift by canonically rewriting the already-created core."""
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    core = lab.core()
    core.update(changes)
    (lab.directory / "episode-core.json").write_bytes(canonical_json_bytes(core))
    lab.resync_continuity()


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"harness_sha256": "0" * 64}, "HARNESS_IDENTITY_MISMATCH"),
        ({"operator_sha256": "0" * 64}, "OPERATOR_IDENTITY_MISMATCH"),
        ({"python_version": "0.0.0"}, "RUNTIME_IDENTITY_MISMATCH"),
    ],
)
def test_identity_drift_seals_stage_refused(
    lab: Lab, changes: dict[str, object], expected: str
) -> None:
    lab.open_episode()
    _rewrite_core(lab, **changes)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert events[-2]["failure_class"] == expected
    assert events[-1]["stage_disposition"] == "STAGE_REFUSED"


# ===========================================================================
# H. Input identity
# ===========================================================================


def test_inputs_hashed_covers_all_five_surfaces_with_path_roles(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    entries = next(
        event
        for event in lab.journal("stage-generate-a.jsonl")
        if event["event"] == "inputs_hashed"
    )["inputs"]
    assert isinstance(entries, list)
    assert tuple(str(entry["surface"]) for entry in entries) == EXPECTED_INPUT_SURFACES
    assert tuple(str(entry["path_role"]) for entry in entries) == EXPECTED_PATH_ROLES
    for entry in entries:
        assert tuple(sorted(entry)) == ("byte_size", "path_role", "sha256", "surface")


def test_input_bytes_and_locations_are_never_persisted(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    entries = next(
        event
        for event in lab.journal("stage-generate-a.jsonl")
        if event["event"] == "inputs_hashed"
    )["inputs"]
    assert isinstance(entries, list)
    serialized = json.dumps(entries)
    for surface in EXPECTED_INPUT_SURFACES:
        assert f"synthetic {surface}" not in serialized
        assert str(lab.inputs[surface]) not in serialized


def test_unreadable_input_seals_stage_failed(lab: Lab) -> None:
    lab.open_episode()
    lab.inputs["source_records"].unlink()
    lab.inputs["source_records"].mkdir()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert events[-2]["failure_class"] == "INPUT_HASH_FAILURE"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"


def test_input_identity_drift_between_generations_seals_stage_refused(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    lab.inputs["decision_record"].write_bytes(b"different synthetic decision record\n")
    assert lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B")) == 1
    events = lab.journal("stage-generate-b.jsonl")
    assert events[-2]["failure_class"] == "INPUT_IDENTITY_MISMATCH"
    assert events[-1]["stage_disposition"] == "STAGE_REFUSED"


# ===========================================================================
# I. Stage lifecycle
# ===========================================================================


def test_stage_lifecycle_order_and_ordinals(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    events = lab.journal("stage-generate-a.jsonl")
    assert [event["event"] for event in events] == [
        "stage_opened",
        "repository_identity_observed",
        "inputs_hashed",
        "repository_identity_observed",
        "child_started",
        "child_exited",
        "outputs_hashed",
        "split_fingerprint_observed",
        "stage_sealed",
    ]
    assert [event["event_ordinal"] for event in events] == list(range(1, len(events) + 1))
    assert events[0]["generation_identity"] == "A"
    assert events[-1]["stage_disposition"] == "STAGE_COMPLETE"


def test_verify_records_exactly_one_repository_observation(lab: Lab) -> None:
    lab.complete_success()
    observations = [
        event
        for event in lab.journal("stage-verify.jsonl")
        if event["event"] == "repository_identity_observed"
    ]
    assert len(observations) == 1
    compare_observations = [
        event
        for event in lab.journal("stage-compare.jsonl")
        if event["event"] == "repository_identity_observed"
    ]
    assert len(compare_observations) == 2


def test_generation_identity_is_absent_rather_than_null_for_comparison(lab: Lab) -> None:
    lab.complete_success()
    opened = lab.journal("stage-compare.jsonl")[0]
    assert "generation_identity" not in opened
    argv = opened["argv"]
    assert isinstance(argv, list)
    assert argv[2] == "compare"


def test_stage_opened_records_the_complete_child_argv(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    argv = lab.journal("stage-generate-a.jsonl")[0]["argv"]
    assert isinstance(argv, list)
    assert argv[2] == "generate"
    assert "--expected-canonical-commit" in argv
    assert SYNTHETIC_COMMIT in argv
    for surface in EXPECTED_INPUT_SURFACES:
        assert f"--{surface.replace('_', '-')}" in argv


def test_repository_observation_carries_mode_and_match(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    observation = lab.journal("stage-generate-a.jsonl")[1]
    assert observation["mode"] == "CONTINUATION"
    assert observation["identity_match"] is True
    assert observation["expected_canonical_commit"] == SYNTHETIC_COMMIT
    assert observation["observed_canonical_commit"] == SYNTHETIC_COMMIT


def test_canonical_main_movement_seals_stage_refused(lab: Lab) -> None:
    lab.open_episode()
    lab.set_head(MOVED_COMMIT)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert events[1]["identity_match"] is False
    assert events[-2]["failure_class"] == "CANONICAL_MAIN_MISMATCH"
    assert events[-1]["stage_disposition"] == "STAGE_REFUSED"
    assert not lab.workspace_a.exists()


def test_no_continuation_after_a_sealed_failure(lab: Lab) -> None:
    lab.open_episode()
    lab.set_head(MOVED_COMMIT)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    lab.set_head(SYNTHETIC_COMMIT)
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B"))


def test_same_stage_retry_is_prohibited(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A"))


def test_compare_requires_both_completed_generations(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.compare_argv(), runner=make_runner(lab.module))


def test_verify_requires_a_completed_comparison(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both()
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.verify_argv(), runner=make_runner(lab.module))


# ===========================================================================
# J. STAGE_REFUSED boundary
# ===========================================================================


def test_refusal_failure_class_set_is_exactly_five(harness: ModuleType) -> None:
    assert harness.REFUSAL_FAILURE_CLASSES == EXPECTED_REFUSAL_FAILURE_CLASSES
    assert len(harness.REFUSAL_FAILURE_CLASSES) == 5


def _opened_journal(module: ModuleType, path: Path) -> Any:
    module.EvidenceStore().create_exclusive(path, b"")
    journal = module.StageJournal(
        store=module.EvidenceStore(),
        path=path,
        stage="GENERATE_A",
        episode_identity="0" * 64,
    )
    journal.append("stage_opened", {"argv": []})
    return journal


@pytest.mark.parametrize("failure_class", sorted(EXPECTED_REFUSAL_FAILURE_CLASSES))
def test_refusal_set_seals_stage_refused(
    harness: ModuleType, tmp_path: Path, failure_class: str
) -> None:
    journal = _opened_journal(harness, tmp_path / "journal.jsonl")
    assert harness.seal_after_failure(journal, failure_class, None) == "STAGE_REFUSED"


@pytest.mark.parametrize(
    "failure_class",
    [
        "ARGUMENT_REFUSAL",
        "PATH_SEPARATION_REFUSAL",
        "REPARSE_POINT_REFUSAL",
        "INPUT_HASH_FAILURE",
        "CHILD_LAUNCH_FAILURE",
        "OUTPUT_INVENTORY_MISMATCH",
        "OUTPUT_HASH_FAILURE",
        "BYTE_INEQUALITY",
        "COMPARE_CONTRADICTION",
        "FINGERPRINT_MISMATCH",
        "EVIDENCE_WRITE_FAILURE",
        "EVIDENCE_MALFORMED_PRESERVED",
        "VERIFY_FAILURE",
        "UNCLASSIFIED",
    ],
)
def test_every_other_failure_seals_stage_failed(
    harness: ModuleType, tmp_path: Path, failure_class: str
) -> None:
    journal = _opened_journal(harness, tmp_path / "journal.jsonl")
    assert harness.seal_after_failure(journal, failure_class, None) == "STAGE_FAILED"


def test_a_started_child_can_never_seal_stage_refused(harness: ModuleType, tmp_path: Path) -> None:
    journal = _opened_journal(harness, tmp_path / "journal.jsonl")
    journal.child_started = True
    assert harness.seal_after_failure(journal, "CANONICAL_MAIN_MISMATCH", None) == "STAGE_FAILED"


# ===========================================================================
# K. Complete twenty-one-value failure mapping
# ===========================================================================


def test_failure_class_enumeration_is_exactly_twenty_one(harness: ModuleType) -> None:
    assert len(harness.FAILURE_CLASSES) == 21
    assert set(harness.FAILURE_CLASSES) == set(EXPECTED_FAILURE_TRIAD) | {"CHILD_NONZERO_EXIT"}


@pytest.mark.parametrize(("failure_class", "expected"), sorted(EXPECTED_FAILURE_TRIAD.items()))
def test_failure_triad_mapping(
    harness: ModuleType, failure_class: str, expected: tuple[str, str]
) -> None:
    observed, root_cause, remediation = harness.derive_failure_triad(failure_class)
    assert observed == failure_class
    assert (root_cause, remediation) == expected


def test_failure_mapping_is_total_over_twenty_one(harness: ModuleType) -> None:
    covered = set()
    for failure_class in harness.FAILURE_CLASSES:
        if failure_class == "CHILD_NONZERO_EXIT":
            for error_class in harness.OPERATOR_ERROR_CLASSES:
                covered.add(harness.derive_failure_triad(failure_class, error_class)[0])
        else:
            covered.add(harness.derive_failure_triad(failure_class)[0])
    assert covered == set(harness.FAILURE_CLASSES)


def test_later_stage_governance_is_never_derived(harness: ModuleType) -> None:
    derived = {triad[1] for triad in harness.FAILURE_TRIAD.values()}
    derived |= {triad[1] for triad in harness.CHILD_NONZERO_EXIT_TRIAD.values()}
    assert "LATER_STAGE_GOVERNANCE_REQUIRED" not in derived
    assert "LATER_STAGE_GOVERNANCE_REQUIRED" in harness.REMEDIATION_DISPOSITIONS


def test_a_value_outside_the_enumeration_is_rejected(harness: ModuleType) -> None:
    with pytest.raises(ValueError, match="closed enumeration"):
        harness.derive_failure_triad("NOT_A_FAILURE_CLASS")


# ===========================================================================
# L. CHILD_NONZERO_EXIT — eleven branches
# ===========================================================================


def test_operator_error_class_enumeration_is_exactly_eleven(harness: ModuleType) -> None:
    assert len(harness.OPERATOR_ERROR_CLASSES) == 11
    assert set(harness.OPERATOR_ERROR_CLASSES) == set(EXPECTED_CHILD_NONZERO_TRIAD)


@pytest.mark.parametrize(("error_class", "expected"), sorted(EXPECTED_CHILD_NONZERO_TRIAD.items()))
def test_child_nonzero_exit_derivation(
    harness: ModuleType, error_class: str, expected: tuple[str, str]
) -> None:
    observed, root_cause, remediation = harness.derive_failure_triad(
        "CHILD_NONZERO_EXIT", error_class
    )
    assert observed == "CHILD_NONZERO_EXIT"
    assert (root_cause, remediation) == expected


def test_no_error_with_nonzero_exit_is_a_contract_contradiction(harness: ModuleType) -> None:
    _, root_cause, remediation = harness.derive_failure_triad("CHILD_NONZERO_EXIT", "NO_ERROR")
    assert root_cause == "UNDETERMINED"
    assert remediation == "FOUNDER_DISPOSITION_REQUIRED"


def test_child_nonzero_exit_requires_an_operator_error_class(harness: ModuleType) -> None:
    with pytest.raises(ValueError, match="requires an operator_error_class"):
        harness.derive_failure_triad("CHILD_NONZERO_EXIT")


def test_child_nonzero_exit_seals_stage_failed_with_child_provenance(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(
        lab.module,
        exit_code=1,
        stderr=b"medscale.mesc._formal_split_v1.FormalGenerationError: synthetic\n",
    )
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    events = lab.journal("stage-generate-a.jsonl")
    names = [event["event"] for event in events]
    assert names[-4:] == ["child_started", "child_exited", "stage_failed", "stage_sealed"]
    assert events[-3]["error_class"] == "GENERATION_ERROR"
    assert events[-2]["failure_class"] == "CHILD_NONZERO_EXIT"
    assert events[-2]["root_cause_class"] == "CHILD_PROCESS_FAILURE"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"


# ===========================================================================
# M. stderr classifier
# ===========================================================================


def test_exception_module_literal_is_exact(harness: ModuleType) -> None:
    assert harness.FORMAL_EXCEPTION_MODULE == EXPECTED_EXCEPTION_MODULE
    assert harness.EXCEPTION_TOKEN_CLASSES == EXPECTED_EXCEPTION_TOKENS
    assert len(harness.EXCEPTION_TOKEN_CLASSES) == 10


@pytest.mark.parametrize(("token", "expected"), sorted(EXPECTED_EXCEPTION_TOKENS.items()))
def test_each_allowlisted_token_classifies(harness: ModuleType, token: str, expected: str) -> None:
    line = EXPECTED_EXCEPTION_PREFIX + token.encode("ascii")
    assert harness.classify_operator_stderr(line) == expected
    assert harness.classify_operator_stderr(line + b": message") == expected
    assert harness.classify_operator_stderr(b"Traceback\n" + line + b"\n") == expected
    assert harness.classify_operator_stderr(b"Traceback\r\n" + line + b"\r\n") == expected


@pytest.mark.parametrize(
    "stderr",
    [
        b"",
        b"\n\n\n",
        b"medscale.mesc._other_module.FormalGenerationError\n",
        b"medscale.mesc._formal_split_v1.NotAllowlistedError\n",
        b"a message mentioning medscale.mesc._formal_split_v1.FormalGenerationError inside\n",
        b" medscale.mesc._formal_split_v1.FormalGenerationError\n",
        b"medscale.mesc._formal_split_v1.FormalGenerationErrorX\n",
        b"medscale.mesc._formal_split_v1.Formal\xffGenerationError\n",
        b"medscale.mesc._formal_split_v1.\n",
        b"first\rmedscale.mesc._formal_split_v1.FormalGenerationError",
        b"medscale.mesc._formal_split_v1.FormalGenerationError extra\n",
    ],
)
def test_unclassifiable_stderr_fails_closed(harness: ModuleType, stderr: bytes) -> None:
    assert harness.classify_operator_stderr(stderr) == "UNCLASSIFIED"


def test_lf_and_crlf_classify_identically(harness: ModuleType) -> None:
    body = b"Traceback (most recent call last):\n  File x\nmedscale.mesc._formal_split_v1."
    token = b"FormalByteEqualityError: workspaces differ"
    lf = body + token + b"\n"
    crlf = body.replace(b"\n", b"\r\n") + token + b"\r\n"
    assert harness.classify_operator_stderr(lf) == harness.classify_operator_stderr(crlf)
    assert harness.classify_operator_stderr(lf) == "BYTE_EQUALITY_ERROR"


def test_undecodable_message_bytes_do_not_block_classification(harness: ModuleType) -> None:
    stderr = EXPECTED_EXCEPTION_PREFIX + b"FormalMetadataError:\xff\xfe not utf-8\n"
    assert harness.classify_operator_stderr(stderr) == "METADATA_ERROR"


def test_trailing_blank_lines_are_discarded(harness: ModuleType) -> None:
    stderr = EXPECTED_EXCEPTION_PREFIX + b"FormalInventoryError\n\n\n"
    assert harness.classify_operator_stderr(stderr) == "INVENTORY_ERROR"


def test_exit_code_zero_is_always_no_error(harness: ModuleType) -> None:
    stderr = EXPECTED_EXCEPTION_PREFIX + b"FormalGenerationError\n"
    assert harness.operator_error_class_for(0, stderr) == "NO_ERROR"
    assert harness.operator_error_class_for(1, stderr) == "GENERATION_ERROR"
    assert harness.operator_error_class_for(2, b"usage: ...\n") == "UNCLASSIFIED"


# ===========================================================================
# N. CHILD_LAUNCH_FAILURE
# ===========================================================================


def test_child_launch_failure_fabricates_no_child_evidence(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(lab.module, launch_failure=True)
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    events = lab.journal("stage-generate-a.jsonl")
    names = [event["event"] for event in events]
    assert "child_started" not in names
    assert "child_exited" not in names
    assert names[-2:] == ["stage_failed", "stage_sealed"]
    assert events[-2]["failure_class"] == "CHILD_LAUNCH_FAILURE"
    assert events[-2]["root_cause_class"] == "CHILD_PROCESS_FAILURE"
    assert events[-2]["remediation_disposition"] == "NEW_EPISODE_REQUIRED"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"
    serialized = json.dumps(events)
    assert "pid" not in serialized


# ===========================================================================
# O. Evidence-write cases A, B and C
# ===========================================================================


def test_case_a_recoverable_write_failure_seals_stage_failed(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert [event["event"] for event in events][-2:] == ["stage_failed", "stage_sealed"]
    assert events[-2]["failure_class"] == "EVIDENCE_WRITE_FAILURE"
    assert events[-2]["root_cause_class"] == "EVIDENCE_INTEGRITY_FAILURE"
    assert events[-2]["remediation_disposition"] == "NO_REMEDIATION_AUTHORIZED"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"
    assert [event["event_ordinal"] for event in events] == list(range(1, len(events) + 1))


def test_case_b_partial_bytes_are_preserved_exactly(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    payload = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert not payload.endswith(b"\n")
    assert b"stage_failed" not in payload
    assert b"stage_sealed" not in payload
    scan = lab.module.scan_journal(lab.directory / "stage-generate-a.jsonl")
    assert scan.record_integrity == "MALFORMED_PRESERVED"
    assert scan.event_count is None
    # Nothing may be appended after malformed bytes, so the bytes never change again.
    frozen = payload
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B"))
    assert (lab.directory / "stage-generate-a.jsonl").read_bytes() == frozen


def test_case_c_structural_unseal_fabricates_nothing(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed", "stage_failed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    payload = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert b"stage_failed" not in payload
    assert b"stage_sealed" not in payload
    scan = lab.module.scan_journal(lab.directory / "stage-generate-a.jsonl")
    assert scan.record_integrity == "WELL_FORMED"
    assert scan.structurally_unsealed is True
    assert scan.event_count == 2


def test_case_c_prohibits_every_continuation(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed", "stage_failed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B"))
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.compare_argv(), runner=make_runner(lab.module))


def test_case_b_prohibits_every_continuation(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B"))


def test_a_failed_seal_never_advances_the_ordinal(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert [event["event_ordinal"] for event in events] == list(range(1, len(events) + 1))
    assert events[-1]["event_ordinal"] == len(events)


# ===========================================================================
# P. Structural unseal at finalize
# ===========================================================================


def test_structural_unseal_seals_evidence_corrupt(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed", "stage_failed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    before = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert lab.run(lab.finalize_argv()) == 0
    assert (lab.directory / "stage-generate-a.jsonl").read_bytes() == before
    manifest = lab.manifest()
    assert manifest["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"
    records = manifest["records"]
    assert isinstance(records, list)
    binding = records[0]
    # Syntax and lifecycle completeness are separate properties.
    assert binding["record_integrity"] == "WELL_FORMED"
    assert binding["event_count"] == 2


def test_malformed_record_seals_evidence_corrupt_without_event_count(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    assert lab.run(lab.finalize_argv()) == 0
    manifest = lab.manifest()
    assert manifest["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"
    records = manifest["records"]
    assert isinstance(records, list)
    assert records[0]["record_integrity"] == "MALFORMED_PRESERVED"
    assert "event_count" not in records[0]


def test_structurally_unsealed_episode_can_never_be_complete_equal(lab: Lab) -> None:
    lab.complete_success()
    scan = lab.module.scan_journal(lab.directory / "stage-verify.jsonl")
    assert scan.structurally_unsealed is False
    assert scan.sealed_disposition == "STAGE_COMPLETE"


# ===========================================================================
# Q. Invalidation
# ===========================================================================


def test_non_material_invalidation_omits_the_movement_block(lab: Lab) -> None:
    lab.open_episode()
    assert (
        lab.run(lab.invalidate_argv(failure_class="INPUT_HASH_FAILURE", causal_stage="PREFLIGHT"))
        == 0
    )
    events = lab.journal("episode-invalidation.jsonl")
    assert len(events) == 1
    record = events[0]
    assert "canonical_main_movement" not in record
    assert record["schema_version"] == "mesc-p01-04d-execution-evidence/invalidation-event/v1"
    assert record["root_cause_class"] == "INPUT_IDENTITY_FAILURE"
    assert record["remediation_disposition"] == "NEW_EPISODE_REQUIRED"
    assert record["new_episode_required"] is True
    assert record["event_ordinal"] == 1
    assert "identity_match" not in record
    assert "stage" not in record


def test_invalidation_record_has_the_exact_closed_field_set(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN")) == 0
    record = lab.journal("episode-invalidation.jsonl")[0]
    assert tuple(sorted(record)) == (
        "affected_candidates",
        "causal_stage",
        "episode_identity",
        "event_ordinal",
        "failure_class",
        "new_episode_required",
        "originating_episode_identity",
        "recorded_at",
        "remediation_disposition",
        "root_cause_class",
        "schema_version",
    )


def test_material_invalidation_records_the_exact_movement_pair(lab: Lab) -> None:
    lab.open_episode()
    lab.set_head(MOVED_COMMIT)
    argv = lab.invalidate_argv(failure_class="CANONICAL_MAIN_MISMATCH", causal_stage="GENERATE_A")
    assert lab.run(argv) == 0
    record = lab.journal("episode-invalidation.jsonl")[0]
    assert record["root_cause_class"] == "CANONICAL_MAIN_MOVEMENT"
    assert record["canonical_main_movement"] == {
        "expected_canonical_commit": SYNTHETIC_COMMIT,
        "observed_canonical_commit": MOVED_COMMIT,
    }


def test_claimed_movement_without_movement_is_refused(lab: Lab) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(failure_class="CANONICAL_MAIN_MISMATCH", causal_stage="GENERATE_A")
    with pytest.raises(lab.module.ArgumentRefusalError):
        lab.run(argv)
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


def test_affected_candidates_carry_only_identity(lab: Lab) -> None:
    lab.open_episode()
    write_workspace(lab.workspace_a)
    argv = lab.invalidate_argv(
        failure_class="BYTE_INEQUALITY", causal_stage="COMPARE", workspace=lab.workspace_a
    )
    assert lab.run(argv) == 0
    candidates = lab.journal("episode-invalidation.jsonl")[0]["affected_candidates"]
    assert isinstance(candidates, list)
    assert len(candidates) == 7
    for entry in candidates:
        assert tuple(sorted(entry)) == ("byte_size", "filename", "sha256")


def test_a_stage_failure_never_creates_an_invalidation_record(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(lab.module, exit_code=1, stderr=b"unclassifiable\n")
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


def test_invalidation_ordinals_are_contiguous(lab: Lab) -> None:
    lab.open_episode()
    for _ in range(3):
        assert lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN")) == 0
    events = lab.journal("episode-invalidation.jsonl")
    assert [event["event_ordinal"] for event in events] == [1, 2, 3]


def test_invalidate_accepts_child_nonzero_exit_with_a_valid_operator_error_class(lab: Lab) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(
        failure_class="CHILD_NONZERO_EXIT",
        causal_stage="GENERATE_A",
        operator_error_class="INVENTORY_ERROR",
    )
    assert lab.run(argv) == 0
    record = lab.journal("episode-invalidation.jsonl")[0]
    assert record["root_cause_class"] == "OUTPUT_INVENTORY_FAILURE"


# ===========================================================================
# R. Comparison
# ===========================================================================


def test_equal_comparison_is_equal_verified(lab: Lab) -> None:
    lab.complete_success()
    derived = next(
        event
        for event in lab.journal("stage-compare.jsonl")
        if event["event"] == "comparison_derived"
    )
    assert derived["byte_equality"] == "EQUAL"
    assert derived["unequal_filenames"] == []
    assert derived["operator_exit_code"] == 0
    assert derived["comparison_disposition"] == "EQUAL_VERIFIED"


def test_byte_inequality_is_recorded_and_sealed_failed(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both(drift="split-summary.json")
    runner = make_runner(
        lab.module,
        exit_code=1,
        stderr=b"medscale.mesc._formal_split_v1.FormalByteEqualityError: differ\n",
    )
    assert lab.run(lab.compare_argv(), runner=runner) == 1
    events = lab.journal("stage-compare.jsonl")
    derived = next(event for event in events if event["event"] == "comparison_derived")
    assert derived["byte_equality"] == "UNEQUAL"
    assert derived["unequal_filenames"] == ["split-summary.json"]
    assert derived["comparison_disposition"] == "BYTE_INEQUALITY"
    assert events[-2]["failure_class"] == "BYTE_INEQUALITY"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"


def test_contradiction_is_a_hard_stop(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both(drift="excluded-ledger.json")
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 1
    events = lab.journal("stage-compare.jsonl")
    derived = next(event for event in events if event["event"] == "comparison_derived")
    assert derived["comparison_disposition"] == "CONTRADICTION"
    assert events[-2]["failure_class"] == "COMPARE_CONTRADICTION"
    assert events[-2]["remediation_disposition"] == "FOUNDER_DISPOSITION_REQUIRED"


def test_integrity_failure_keeps_child_provenance(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both()
    runner = make_runner(
        lab.module,
        exit_code=1,
        stderr=b"medscale.mesc._formal_split_v1.FormalMetadataError: synthetic\n",
    )
    assert lab.run(lab.compare_argv(), runner=runner) == 1
    events = lab.journal("stage-compare.jsonl")
    derived = next(event for event in events if event["event"] == "comparison_derived")
    assert derived["comparison_disposition"] == "INTEGRITY_FAILURE"
    assert events[-2]["failure_class"] == "CHILD_NONZERO_EXIT"
    assert events[-2]["root_cause_class"] == "EVIDENCE_INTEGRITY_FAILURE"


def test_fingerprint_disagreement_is_a_fingerprint_failure(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both(fingerprint_b="ab" * 32)
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 1
    events = lab.journal("stage-compare.jsonl")
    assert not any(event["event"] == "comparison_derived" for event in events)
    assert events[-2]["failure_class"] == "FINGERPRINT_MISMATCH"
    assert events[-2]["root_cause_class"] == "FINGERPRINT_FAILURE"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"


def test_inventory_mismatch_omits_the_comparison_event(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both()
    (lab.workspace_b / "split-policy.json").unlink()
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 1
    events = lab.journal("stage-compare.jsonl")
    assert not any(event["event"] == "comparison_derived" for event in events)
    assert events[-2]["failure_class"] == "OUTPUT_INVENTORY_MISMATCH"


def test_output_hash_failure_omits_the_outputs_event(lab: Lab) -> None:
    lab.open_episode()

    def _produce_unreadable(_command: Sequence[str]) -> None:
        write_workspace(lab.workspace_a, omit="split-policy.json")
        (lab.workspace_a / "split-policy.json").mkdir()

    runner = make_runner(lab.module, on_run=_produce_unreadable)
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert not any(event["event"] == "outputs_hashed" for event in events)
    assert events[-2]["failure_class"] == "OUTPUT_HASH_FAILURE"


def test_outputs_hashed_carries_exactly_seven_entries(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    outputs = next(
        event
        for event in lab.journal("stage-generate-a.jsonl")
        if event["event"] == "outputs_hashed"
    )["outputs"]
    assert isinstance(outputs, list)
    assert tuple(str(entry["filename"]) for entry in outputs) == EXPECTED_CANDIDATE_FILENAMES
    for entry in outputs:
        assert tuple(sorted(entry)) == ("byte_size", "filename", "sha256")


def test_verify_disagreement_is_a_verify_failure(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both()
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 0
    # The rerun observes drift that the sealed comparison did not.
    (lab.workspace_b / "split-summary.json").write_bytes(b"synthetic drift\n")
    assert lab.run(lab.verify_argv(), runner=make_runner(lab.module)) == 1
    events = lab.journal("stage-verify.jsonl")
    assert events[-2]["failure_class"] == "VERIFY_FAILURE"
    assert events[-2]["root_cause_class"] == "EVIDENCE_INTEGRITY_FAILURE"
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"


def test_comparison_disposition_table_is_total(harness: ModuleType) -> None:
    observed = {
        (equality, exit_code): harness.comparison_disposition_for(equality, exit_code)
        for equality in ("EQUAL", "UNEQUAL")
        for exit_code in (0, 1)
    }
    assert observed == {
        ("EQUAL", 0): "EQUAL_VERIFIED",
        ("EQUAL", 1): "INTEGRITY_FAILURE",
        ("UNEQUAL", 1): "BYTE_INEQUALITY",
        ("UNEQUAL", 0): "CONTRADICTION",
    }


# ===========================================================================
# S. Finalize and terminal precedence
# ===========================================================================


def test_finalize_seals_complete_equal(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    manifest = lab.manifest()
    assert manifest["terminal_disposition"] == "EPISODE_COMPLETE_EQUAL"
    assert tuple(sorted(manifest)) == tuple(sorted(lab.module.EPISODE_MANIFEST_FIELDS))
    records = manifest["records"]
    assert isinstance(records, list)
    assert [record["filename"] for record in records] == [
        "stage-generate-a.jsonl",
        "stage-generate-b.jsonl",
        "stage-compare.jsonl",
        "stage-verify.jsonl",
    ]
    assert all(record["record_integrity"] == "WELL_FORMED" for record in records)


def test_finalize_seals_failed(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(lab.module, exit_code=1, stderr=b"unclassifiable\n")
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_FAILED"


def test_finalize_seals_refused(lab: Lab) -> None:
    lab.open_episode()
    _rewrite_core(lab, operator_sha256="0" * 64)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_REFUSED"


def test_finalize_seals_invalidated(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN")) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_INVALIDATED"


def test_finalize_seals_evidence_corrupt(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"


def test_corruption_outranks_invalidation(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    assert (
        lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="GENERATE_A")) == 0
    )
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"


def test_invalidation_outranks_refusal_and_failure(lab: Lab) -> None:
    lab.open_episode()
    _rewrite_core(lab, operator_sha256="0" * 64)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 1
    assert (
        lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="GENERATE_A")) == 0
    )
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_INVALIDATED"


def test_incomplete_but_clean_episode_is_failed_not_complete(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_FAILED"


def test_terminal_precedence_selection(harness: ModuleType) -> None:
    def survey(**flags: bool) -> Any:
        return harness.EpisodeSurvey(
            core_binding={},
            record_bindings=[],
            corrupt=flags.get("corrupt", False),
            invalidated=flags.get("invalidated", False),
            refused=flags.get("refused", False),
            failed=flags.get("failed", False),
            complete_equal=flags.get("complete_equal", False),
        )

    assert (
        harness.select_terminal_disposition(survey(corrupt=True, invalidated=True, refused=True))
        == "EPISODE_EVIDENCE_CORRUPT"
    )
    assert (
        harness.select_terminal_disposition(survey(corrupt=True, complete_equal=True))
        == "EPISODE_EVIDENCE_CORRUPT"
    )
    assert (
        harness.select_terminal_disposition(survey(invalidated=True, refused=True, failed=True))
        == "EPISODE_INVALIDATED"
    )
    assert (
        harness.select_terminal_disposition(survey(refused=True, failed=True)) == "EPISODE_REFUSED"
    )
    assert harness.select_terminal_disposition(survey(failed=True)) == "EPISODE_FAILED"
    assert (
        harness.select_terminal_disposition(survey(complete_equal=True)) == "EPISODE_COMPLETE_EQUAL"
    )


def test_all_five_terminal_dispositions_are_reachable(harness: ModuleType) -> None:
    assert len(harness.TERMINAL_DISPOSITIONS) == 5


def test_manifest_binds_the_episode_core_separately(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    core_binding = lab.manifest()["episode_core"]
    assert isinstance(core_binding, dict)
    assert tuple(sorted(core_binding)) == ("byte_size", "filename", "record_integrity", "sha256")
    payload = (lab.directory / "episode-core.json").read_bytes()
    assert core_binding["sha256"] == hashlib.sha256(payload).hexdigest()
    assert core_binding["byte_size"] == len(payload)


def test_manifest_never_embeds_its_own_digest(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    payload = (lab.directory / "episode-manifest.json").read_bytes()
    assert hashlib.sha256(payload).hexdigest().encode() not in payload
    assert b"record_integrity" in payload
    manifest = lab.manifest()
    assert "terminal_identity" not in manifest


# ===========================================================================
# T. TM-0
# ===========================================================================


def test_tm0_is_the_absent_path(lab: Lab) -> None:
    lab.open_episode()
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_ABSENT
    with pytest.raises(lab.module.EpisodeStateError):
        lab.module.terminal_identity(lab.directory)


def test_tm0_permits_a_containment_retry(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, clean_failures={"inputs_hashed", "stage_failed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1

    class _RefusingStore(lab.module.EvidenceStore):  # type: ignore[misc,name-defined]
        def create_exclusive(self, path: Path, payload: bytes) -> None:
            raise OSError("synthetic unwritable evidence root")

    with pytest.raises(OSError, match="unwritable"):
        lab.run(lab.finalize_argv(), store=_RefusingStore())
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_ABSENT
    # Storage recovers: the retry is permitted and remains evidence preserving.
    before = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert lab.run(lab.finalize_argv()) == 0
    assert (lab.directory / "stage-generate-a.jsonl").read_bytes() == before
    assert lab.manifest()["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"


def test_tm0_retry_after_canonical_main_movement_requires_invalidate(lab: Lab) -> None:
    lab.complete_success()
    lab.set_head(MOVED_COMMIT)
    with pytest.raises(lab.module.CanonicalMainMismatchError):
        lab.run(lab.finalize_argv())
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_ABSENT
    argv = lab.invalidate_argv(failure_class="CANONICAL_MAIN_MISMATCH", causal_stage="FINALIZE")
    assert lab.run(argv) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_INVALIDATED"


def test_finalize_refuses_a_further_movement_after_invalidate(lab: Lab) -> None:
    lab.complete_success()
    lab.set_head(MOVED_COMMIT)
    argv = lab.invalidate_argv(failure_class="CANONICAL_MAIN_MISMATCH", causal_stage="FINALIZE")
    assert lab.run(argv) == 0
    lab.set_head("c" * 40)
    with pytest.raises(lab.module.CanonicalMainMismatchError):
        lab.run(lab.finalize_argv())
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_ABSENT


def test_finalize_never_appends_invalidation_evidence_itself(lab: Lab) -> None:
    lab.complete_success()
    lab.set_head(MOVED_COMMIT)
    with pytest.raises(lab.module.CanonicalMainMismatchError):
        lab.run(lab.finalize_argv())
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


# ===========================================================================
# U. TM-1
# ===========================================================================


def _tm1_payloads(lab: Lab) -> dict[str, bytes]:
    """Return payloads that must every one classify TM-1."""
    lab_manifest = {
        "schema_version": "mesc-p01-04d-execution-evidence/episode-manifest/v1",
        "episode_identity": "0" * 64,
        "episode_core": {
            "filename": "episode-core.json",
            "sha256": "0" * 64,
            "byte_size": 1,
            "record_integrity": "WELL_FORMED",
        },
        "records": [],
        "terminal_disposition": "EPISODE_FAILED",
        "manifest_sealed_at": "2026-01-01T00:00:00.000000Z",
    }
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    canonical = canonical_json_bytes(lab_manifest)
    wrong_version = dict(lab_manifest, schema_version="wrong/v9")
    missing_field = {
        key: value for key, value in lab_manifest.items() if key != "terminal_disposition"
    }
    bad_disposition = dict(lab_manifest, terminal_disposition="EPISODE_UNKNOWN")
    extra_field = dict(lab_manifest, tm_state="TM-2")
    return {
        "zero-byte": b"",
        "partial-json": canonical[: len(canonical) // 2],
        "malformed-json": b"{not json at all}\n",
        "wrong-schema-version": canonical_json_bytes(wrong_version),
        "missing-mandatory-field": canonical_json_bytes(missing_field),
        "invalid-terminal-disposition": canonical_json_bytes(bad_disposition),
        "prohibited-extra-field": canonical_json_bytes(extra_field),
        "noncanonical": json.dumps(lab_manifest, indent=2).encode("utf-8") + b"\n",
        "incomplete-binding": canonical,
    }


TM1_CASES = (
    "zero-byte",
    "partial-json",
    "malformed-json",
    "wrong-schema-version",
    "missing-mandatory-field",
    "invalid-terminal-disposition",
    "prohibited-extra-field",
    "noncanonical",
    "incomplete-binding",
)


@pytest.mark.parametrize("case", TM1_CASES)
def test_tm1_classification_and_immutability(lab: Lab, case: str) -> None:
    lab.complete_success()
    payload = _tm1_payloads(lab)[case]
    (lab.directory / "episode-manifest.json").write_bytes(payload)
    lab.resync_continuity()
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_INVALID
    with pytest.raises(lab.module.EpisodeStateError, match="irrecoverably failed"):
        lab.run(lab.finalize_argv())
    # The exact bytes are preserved; no retry, repair, truncation or replacement.
    assert (lab.directory / "episode-manifest.json").read_bytes() == payload
    with pytest.raises(lab.module.EpisodeStateError):
        lab.module.terminal_identity(lab.directory)


def test_zero_byte_manifest_is_tm1_not_tm0(lab: Lab) -> None:
    lab.complete_success()
    (lab.directory / "episode-manifest.json").write_bytes(b"")
    assert (lab.directory / "episode-manifest.json").exists()
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_INVALID


def test_tm1_prohibits_every_scientific_continuation(lab: Lab) -> None:
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    (lab.directory / "episode-manifest.json").write_bytes(b"partial")
    lab.resync_continuity()
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B"))
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.compare_argv(), runner=make_runner(lab.module))
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="FINALIZE"))


# ===========================================================================
# V. TM-2
# ===========================================================================


def test_tm2_establishes_the_terminal_identity(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_VALID
    payload = (lab.directory / "episode-manifest.json").read_bytes()
    digest, size = lab.module.terminal_identity(lab.directory)
    assert digest == hashlib.sha256(payload).hexdigest()
    assert size == len(payload)


def test_terminal_identity_is_recomputable_read_only_after_a_crash(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    before = (lab.directory / "episode-manifest.json").read_bytes()
    first = lab.module.terminal_identity(lab.directory)
    second = lab.module.terminal_identity(lab.directory)
    assert first == second
    assert (lab.directory / "episode-manifest.json").read_bytes() == before


def test_post_seal_immutability_is_absolute(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    snapshot = digest_tree(lab.directory)
    # Even an operator holding a perfectly current token cannot continue a sealed
    # episode: post-seal immutability is not enforced by token scarcity.
    lab.resync_continuity()
    with pytest.raises(lab.module.EpisodeStateError, match="already sealed"):
        lab.run(lab.finalize_argv())
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="FINALIZE"))
    with pytest.raises(lab.module.EpisodeStateError):
        lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A"))
    assert digest_tree(lab.directory) == snapshot


def test_manifest_binding_drift_demotes_the_manifest_to_tm1(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_VALID
    with (lab.directory / "stage-verify.jsonl").open("ab") as handle:
        handle.write(b"{}\n")
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_INVALID


# ===========================================================================
# W. Import boundaries
# ===========================================================================


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_production_never_imports_the_formal_modules() -> None:
    imported = _imported_modules(HARNESS_PATH)
    assert "medscale.mesc._formal_generation_v1" not in imported
    assert "medscale.mesc._formal_split_v1" not in imported


def test_production_medscale_imports_are_only_the_canonical_serializer() -> None:
    imported = {name for name in _imported_modules(HARNESS_PATH) if name.startswith("medscale")}
    assert imported == {"medscale.mesc._canonical_json_v1"}


def test_production_imports_only_canonical_serializer_symbols() -> None:
    tree = ast.parse(HARNESS_PATH.read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "medscale.mesc._canonical_json_v1"
        for alias in node.names
    }
    assert imported == {"canonical_json_bytes", "sha256_of_bytes"}


def test_test_scope_formal_import_is_exactly_the_oracle() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    formal: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and "_formal_" in node.module:
            formal.setdefault(node.module, set()).update(alias.name for alias in node.names)
    assert formal == {"medscale.mesc._formal_generation_v1": {"resolve_repository_commit"}}
    assert "medscale.mesc._formal_split_v1" not in _imported_modules(Path(__file__))


def test_no_frozen_formal_test_helper_is_imported() -> None:
    imported = _imported_modules(Path(__file__))
    assert not any(name.startswith("test_mesc_formal") for name in imported)
    assert "test_mesc_p01_04d_operator" not in imported


def test_production_uses_no_shell_and_no_dynamic_execution() -> None:
    source = HARNESS_PATH.read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "shell=False" in source
    tree = ast.parse(source)
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "eval" not in called
    assert "exec" not in called


# ===========================================================================
# X. Sensitive-data minimization
# ===========================================================================


def test_no_raw_stream_bytes_reach_durable_evidence(lab: Lab) -> None:
    lab.open_episode()
    secret_stdout = b"SYNTHETIC-STDOUT-MARKER\n"
    secret_stderr = b"SYNTHETIC-STDERR-MARKER\n"
    runner = make_runner(
        lab.module,
        stdout=secret_stdout,
        stderr=secret_stderr,
        on_run=lambda _command: write_workspace(lab.workspace_a),
    )
    assert lab.run(lab.generate_argv("A"), runner=runner) == 0
    payload = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert b"SYNTHETIC-STDOUT-MARKER" not in payload
    assert b"SYNTHETIC-STDERR-MARKER" not in payload
    exited = next(
        event for event in lab.journal("stage-generate-a.jsonl") if event["event"] == "child_exited"
    )
    assert exited["stdout_sha256"] == hashlib.sha256(secret_stdout).hexdigest()
    assert exited["stderr_sha256"] == hashlib.sha256(secret_stderr).hexdigest()
    assert exited["stdout_byte_size"] == len(secret_stdout)
    assert exited["error_class"] == "NO_ERROR"
    assert tuple(
        sorted(
            set(exited) - {"schema_version", "episode_identity", "stage", "event", "event_ordinal"}
        )
    ) == (
        "elapsed_ms",
        "error_class",
        "exit_code",
        "exited_at",
        "stderr_byte_size",
        "stderr_sha256",
        "stdout_byte_size",
        "stdout_sha256",
    )


def test_no_exception_message_reaches_durable_evidence(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(
        lab.module,
        exit_code=1,
        stderr=(
            b"medscale.mesc._formal_split_v1.FormalInputIdentityError: PROTECTED-IDENTIFIER-12345\n"
        ),
    )
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    payload = (lab.directory / "stage-generate-a.jsonl").read_bytes()
    assert b"PROTECTED-IDENTIFIER-12345" not in payload
    assert b"FormalInputIdentityError" not in payload
    assert b"INPUT_IDENTITY_ERROR" in payload


def test_no_environment_or_credential_material_is_persisted(lab: Lab) -> None:
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    for path in sorted(lab.directory.iterdir()):
        payload = path.read_bytes()
        for marker in (b"hostname", b"username", b"USERNAME", b"PATH=", b"token", b"secret"):
            assert marker not in payload
    core = lab.core()
    assert "hostname" not in core
    assert "username" not in core


def test_required_paths_are_not_redacted(lab: Lab) -> None:
    lab.open_episode()
    core = lab.core()
    assert core["repository_root"] == str(lab.repository_root.resolve())
    assert core["external_evidence_root"] == str(lab.evidence_root.resolve())
    assert Path(str(core["resolved_python_executable_path"])).is_file()


# ===========================================================================
# Y. Scientific isolation
# ===========================================================================


def test_workspaces_are_byte_identical_after_harness_observation(lab: Lab) -> None:
    lab.open_episode()
    lab.generate_both()
    before_a = digest_tree(lab.workspace_a)
    before_b = digest_tree(lab.workspace_b)
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 0
    assert lab.run(lab.verify_argv(), runner=make_runner(lab.module)) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert digest_tree(lab.workspace_a) == before_a
    assert digest_tree(lab.workspace_b) == before_b
    assert len(before_a) == 7


def test_the_harness_never_pre_creates_a_generation_workspace(lab: Lab) -> None:
    lab.open_episode()
    runner = make_runner(lab.module, launch_failure=True)
    assert lab.run(lab.generate_argv("A"), runner=runner) == 1
    assert not lab.workspace_a.exists()


def test_candidate_inventory_literals_are_exact(harness: ModuleType) -> None:
    assert harness.CANDIDATE_FILENAMES == EXPECTED_CANDIDATE_FILENAMES
    assert len(harness.CANDIDATE_FILENAMES) == 7


def test_input_surface_literals_are_exact(harness: ModuleType) -> None:
    assert harness.INPUT_SURFACES == EXPECTED_INPUT_SURFACES
    assert tuple(harness.SURFACE_PATH_ROLES[s] for s in harness.INPUT_SURFACES) == (
        EXPECTED_PATH_ROLES
    )


# ===========================================================================
# Z. Closed vocabulary ledger and determinism
# ===========================================================================


def test_named_closed_enumeration_ledger(harness: ModuleType) -> None:
    sizes = {name: len(values) for name, values in harness.CLOSED_VOCABULARIES.items()}
    assert sizes == EXPECTED_VOCABULARY_SIZES
    assert len(harness.CLOSED_VOCABULARIES) == 10
    assert sum(sizes.values()) == 78


@pytest.mark.parametrize("name", sorted(EXPECTED_VOCABULARY_SIZES))
def test_each_enumeration_has_no_duplicate_values(harness: ModuleType, name: str) -> None:
    values = harness.CLOSED_VOCABULARIES[name]
    assert len(set(values)) == len(values)


def test_no_enumeration_value_exists_for_a_structural_condition(harness: ModuleType) -> None:
    forbidden = {
        "TM-0",
        "TM-1",
        "TM-2",
        "STRUCTURALLY_UNSEALED",
        "CONTAINMENT",
        "RETRY",
        "TERMINALIZATION_FAILED",
        "REPAIR",
        "CRASH",
    }
    for values in harness.CLOSED_VOCABULARIES.values():
        assert not forbidden & set(values)


def test_inline_domains_stay_outside_the_named_ledger(harness: ModuleType) -> None:
    assert harness.STAGES == ("GENERATE_A", "GENERATE_B", "COMPARE", "VERIFY")
    assert harness.GENERATION_IDENTITIES == ("A", "B")
    assert harness.BYTE_EQUALITIES == ("EQUAL", "UNEQUAL")
    assert harness.OBSERVATION_MODES == ("CONTINUATION", "CONTAINMENT")
    named = {value for values in harness.CLOSED_VOCABULARIES.values() for value in values}
    assert "CONTINUATION" not in named
    assert "EQUAL" not in named


def test_episode_core_is_deterministic_for_identical_inputs(harness: ModuleType) -> None:
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes

    def build() -> bytes:
        return canonical_json_bytes(
            harness.build_episode_core(
                episode_id=EPISODE_ID,
                expected_canonical_commit=SYNTHETIC_COMMIT,
                repository_root=Path("/synthetic/repo"),
                external_evidence_root=Path("/synthetic/evidence"),
                operator=harness.ArtifactIdentity("0" * 64, 11),
                harness=harness.ArtifactIdentity("1" * 64, 22),
                runtime=harness.RuntimeIdentity("/python", "2" * 64, 33, "3.11.15", "CPython"),
            )
        )

    assert build() == build()
    assert b"\r" not in build()


def test_two_identical_episodes_share_one_episode_identity(tmp_path: Path) -> None:
    identities: list[str] = []
    for index in range(2):
        root = tmp_path / f"repo-{index}"
        write_synthetic_repository(root)
        module = load_harness(root / "scripts" / HARNESS_PATH.name)
        evidence = tmp_path / f"evidence-{index}"
        evidence.mkdir()
        core = module.build_episode_core(
            episode_id=EPISODE_ID,
            expected_canonical_commit=SYNTHETIC_COMMIT,
            repository_root=Path("/synthetic/repo"),
            external_evidence_root=Path("/synthetic/evidence"),
            operator=module.ArtifactIdentity("0" * 64, 11),
            harness=module.ArtifactIdentity("1" * 64, 22),
            runtime=module.RuntimeIdentity("/python", "2" * 64, 33, "3.11.15", "CPython"),
        )
        from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes

        identities.append(sha256_of_bytes(canonical_json_bytes(core)))
    assert identities[0] == identities[1]


def test_episode_core_carries_no_timestamp(lab: Lab) -> None:
    lab.open_episode()
    payload = (lab.directory / "episode-core.json").read_bytes()
    assert not TIMESTAMP_PATTERN.search(payload.decode("utf-8"))
    assert b"sealed_at" not in payload
    assert b"recorded_at" not in payload


def test_no_repository_file_is_created_by_qualification(lab: Lab) -> None:
    before = sorted(path.name for path in (lab.repository_root / "scripts").iterdir())
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    after = sorted(path.name for path in (lab.repository_root / "scripts").iterdir())
    assert before == after
    assert os.path.commonpath([str(lab.directory), str(lab.evidence_root)]) == str(
        lab.evidence_root
    )


# ===========================================================================
# AA. Review-correction regression — derived continuation barriers
# ===========================================================================


@dataclass
class ContinuationSpy:
    """Counts the operations that must never run before a continuation refusal."""

    input_hashes: int = 0
    child_launches: int = 0


def install_spy(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> tuple[ContinuationSpy, Any]:
    """Instrument protected-input hashing and child launch through the real code paths.

    The counting child runner raises rather than returning, so a launch cannot be
    silently tolerated even if the counter were never asserted.
    """
    spy = ContinuationSpy()
    real_hash = lab.module.hash_input_surfaces

    def counting_hash(inputs: Any) -> Any:
        spy.input_hashes += 1
        return real_hash(inputs)

    monkeypatch.setattr(lab.module, "hash_input_surfaces", counting_hash)

    class _CountingRunner(lab.module.ChildRunner):  # type: ignore[misc,name-defined]
        def run(self, command: Sequence[str]) -> Any:
            spy.child_launches += 1
            raise AssertionError("no child may launch after a continuation refusal")

    return spy, _CountingRunner()


def _stage_open_residue(lab: Lab) -> bytes:
    """Fail the first required ``stage_opened`` append cleanly and return the residue."""
    store = make_store(lab.module, clean_failures={"stage_opened"})
    with pytest.raises(lab.module.EvidenceWriteFailureError):
        lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A"))
    lab.resync_continuity()
    return (lab.directory / "stage-generate-a.jsonl").read_bytes()


# --- PA2-R1: a valid durable invalidation bars scientific continuation -------


def test_valid_invalidation_bars_generate_before_any_scientific_work(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(failure_class="INPUT_HASH_FAILURE", causal_stage="PREFLIGHT")
    assert lab.run(argv) == 0
    spy, runner = install_spy(lab, monkeypatch)
    with pytest.raises(lab.module.EpisodeStateError, match="durable invalidation"):
        lab.run(lab.generate_argv("A"), runner=runner)
    assert spy.input_hashes == 0
    assert spy.child_launches == 0
    assert not lab.workspace_a.exists()
    assert not (lab.directory / "stage-generate-a.jsonl").exists()


def test_valid_invalidation_bars_compare_and_verify(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    lab.open_episode()
    lab.generate_both()
    argv = lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="COMPARE")
    assert lab.run(argv) == 0
    spy, runner = install_spy(lab, monkeypatch)
    with pytest.raises(lab.module.EpisodeStateError, match="durable invalidation"):
        lab.run(lab.compare_argv(), runner=runner)
    assert not (lab.directory / "stage-compare.jsonl").exists()
    with pytest.raises(lab.module.EpisodeStateError, match="durable invalidation"):
        lab.run(lab.verify_argv(), runner=runner)
    assert not (lab.directory / "stage-verify.jsonl").exists()
    assert spy.input_hashes == 0
    assert spy.child_launches == 0


def test_movement_invalidation_also_bars_continuation(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    lab.open_episode()
    lab.set_head(MOVED_COMMIT)
    argv = lab.invalidate_argv(failure_class="CANONICAL_MAIN_MISMATCH", causal_stage="GENERATE_A")
    assert lab.run(argv) == 0
    lab.set_head(SYNTHETIC_COMMIT)
    spy, runner = install_spy(lab, monkeypatch)
    # Even with canonical main restored, the invalidation is not undone and there
    # is no automatic re-pin, resume or repair.
    with pytest.raises(lab.module.EpisodeStateError, match="durable invalidation"):
        lab.run(lab.generate_argv("A"), runner=runner)
    assert spy.input_hashes == 0
    assert spy.child_launches == 0


@pytest.mark.parametrize("residue", [b"", b'{"partial"'])
def test_uninterpretable_invalidation_bytes_bar_continuation(
    lab: Lab, monkeypatch: pytest.MonkeyPatch, residue: bytes
) -> None:
    lab.open_episode()
    (lab.directory / "episode-invalidation.jsonl").write_bytes(residue)
    lab.resync_continuity()
    spy, runner = install_spy(lab, monkeypatch)
    with pytest.raises(lab.module.EpisodeStateError, match="cannot be safely interpreted"):
        lab.run(lab.generate_argv("A"), runner=runner)
    assert spy.input_hashes == 0
    assert spy.child_launches == 0
    # Unsafe invalidation bytes are refused, never repaired.
    assert (lab.directory / "episode-invalidation.jsonl").read_bytes() == residue


def test_finalize_remains_permitted_after_valid_invalidation(lab: Lab) -> None:
    lab.complete_success()
    argv = lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="COMPARE")
    assert lab.run(argv) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_INVALIDATED"


def test_invalidation_barrier_does_not_outrank_evidence_corruption(lab: Lab) -> None:
    lab.open_episode()
    store = make_store(lab.module, partial_failures={"inputs_hashed"})
    assert lab.run(lab.generate_argv("A"), store=store, runner=lab.producing_runner("A")) == 1
    argv = lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="GENERATE_A")
    assert lab.run(argv) == 0
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_EVIDENCE_CORRUPT"


def test_invalidate_itself_is_not_barred_by_a_prior_invalidation(lab: Lab) -> None:
    lab.open_episode()
    for _ in range(2):
        argv = lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN")
        assert lab.run(argv) == 0
    assert [event["event_ordinal"] for event in lab.journal("episode-invalidation.jsonl")] == [1, 2]


# --- PA2-R2: a stage journal that never durably opened bars continuation -----


def test_failed_first_stage_opened_leaves_exact_zero_byte_residue(lab: Lab) -> None:
    lab.open_episode()
    residue = _stage_open_residue(lab)
    journal = lab.directory / "stage-generate-a.jsonl"
    assert journal.exists()
    assert residue == b""
    assert b"stage_opened" not in residue
    assert b"stage_failed" not in residue
    assert b"stage_sealed" not in residue
    scan = lab.module.scan_journal(journal)
    assert scan.opened is False
    assert scan.record_integrity == "WELL_FORMED"
    assert scan.event_count == 0
    # The canonical structural-unseal definition needs stage_opened, so this
    # residue is deliberately not called structurally unsealed.
    assert scan.structurally_unsealed is False


def test_stage_open_residue_bars_every_later_continuation(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    lab.open_episode()
    frozen = _stage_open_residue(lab)
    spy, runner = install_spy(lab, monkeypatch)
    with pytest.raises(lab.module.EpisodeStateError, match="never durably opened"):
        lab.run(lab.generate_argv("B"), runner=runner)
    assert not lab.workspace_b.exists()
    assert not (lab.directory / "stage-generate-b.jsonl").exists()
    with pytest.raises(lab.module.EpisodeStateError, match="never durably opened"):
        lab.run(lab.compare_argv(), runner=runner)
    with pytest.raises(lab.module.EpisodeStateError, match="never durably opened"):
        lab.run(lab.verify_argv(), runner=runner)
    assert spy.input_hashes == 0
    assert spy.child_launches == 0
    assert (lab.directory / "stage-generate-a.jsonl").read_bytes() == frozen


def test_finalize_binds_the_stage_open_residue_without_mutating_it(lab: Lab) -> None:
    lab.open_episode()
    frozen = _stage_open_residue(lab)
    assert lab.run(lab.finalize_argv()) == 0
    assert (lab.directory / "stage-generate-a.jsonl").read_bytes() == frozen
    manifest = lab.manifest()
    disposition = manifest["terminal_disposition"]
    assert disposition in lab.module.TERMINAL_DISPOSITIONS
    assert disposition != "EPISODE_COMPLETE_EQUAL"
    records = manifest["records"]
    assert isinstance(records, list)
    binding = next(record for record in records if record["filename"] == "stage-generate-a.jsonl")
    assert binding["byte_size"] == 0
    assert binding["record_integrity"] == "WELL_FORMED"
    assert binding["event_count"] == 0


def test_no_barrier_state_is_ever_persisted(lab: Lab) -> None:
    lab.open_episode()
    _stage_open_residue(lab)
    argv = lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="GENERATE_A")
    assert lab.run(argv) == 0
    assert lab.run(lab.finalize_argv()) == 0
    for path in sorted(lab.directory.iterdir()):
        payload = path.read_bytes()
        for marker in (
            b"stage_open_failed",
            b"continuation_blocked",
            b"residue_state",
            b"CONTINUATION_BARRIER",
            b"BARRIER",
        ):
            assert marker not in payload
    present = sorted(entry.name for entry in lab.directory.iterdir())
    assert set(present) <= set(EXPECTED_EVIDENCE_FILENAMES)


def test_a_completed_stage_never_bars_the_next_stage(lab: Lab) -> None:
    """The barrier is narrowly targeted: valid STAGE_COMPLETE sequencing still runs."""
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_COMPLETE_EQUAL"


# --- PA2-R3: controlled pre-mutation argument refusal ------------------------


def test_child_nonzero_exit_without_operator_error_class_is_an_argument_refusal(lab: Lab) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(failure_class="CHILD_NONZERO_EXIT", causal_stage="GENERATE_A")
    with pytest.raises(lab.module.ArgumentRefusalError, match="operator_error_class"):
        lab.run(argv)
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


def test_child_nonzero_exit_with_an_invalid_operator_error_class_is_refused(lab: Lab) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(
        failure_class="CHILD_NONZERO_EXIT",
        causal_stage="GENERATE_A",
        operator_error_class="NOT_AN_OPERATOR_ERROR_CLASS",
    )
    with pytest.raises(SystemExit) as caught:
        lab.run(argv)
    assert caught.value.code == 2
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


def test_argument_refusal_surface_carries_no_traceback(
    lab: Lab, capsys: pytest.CaptureFixture[str]
) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(failure_class="CHILD_NONZERO_EXIT", causal_stage="GENERATE_A")
    assert lab.module.main(argv) == 1
    captured = capsys.readouterr()
    assert "ARGUMENT_REFUSAL" in captured.err
    assert "Traceback" not in captured.err
    assert "ValueError" not in captured.err
    assert not (lab.directory / "episode-invalidation.jsonl").exists()


@pytest.mark.parametrize("error_class", sorted(EXPECTED_CHILD_NONZERO_TRIAD))
def test_invalidate_preserves_all_eleven_child_nonzero_branches(lab: Lab, error_class: str) -> None:
    lab.open_episode()
    argv = lab.invalidate_argv(
        failure_class="CHILD_NONZERO_EXIT",
        causal_stage="GENERATE_A",
        operator_error_class=error_class,
    )
    assert lab.run(argv) == 0
    record = lab.journal("episode-invalidation.jsonl")[0]
    root_cause, remediation = EXPECTED_CHILD_NONZERO_TRIAD[error_class]
    assert record["failure_class"] == "CHILD_NONZERO_EXIT"
    assert record["root_cause_class"] == root_cause
    assert record["remediation_disposition"] == remediation


def test_derive_failure_triad_closed_table_is_not_weakened(harness: ModuleType) -> None:
    """The controlled CLI refusal does not relax the internal closed-table contract."""
    with pytest.raises(ValueError, match="requires an operator_error_class"):
        harness.derive_failure_triad("CHILD_NONZERO_EXIT")
    with pytest.raises(ValueError, match="outside enumeration"):
        harness.derive_failure_triad("CHILD_NONZERO_EXIT", "NOT_AN_OPERATOR_ERROR_CLASS")


# ===========================================================================
# BB. Greptile P1 security regressions — G1 / G2 / G3
# ===========================================================================

#: A syntactically valid commit that must never become repository identity.
EXTERNAL_COMMIT = "dead" * 10


def try_reparse_dir(link: Path, target: Path) -> bool:
    """Create a directory reparse point, reporting whether the host permitted it.

    A Windows junction needs no elevation, so the reparse contract is exercised
    for real on hosts that refuse unprivileged symlinks.
    """
    if os.name == "nt":
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            check=False,
        )
        return completed.returncode == 0 and link.exists()
    return try_symlink(link, target)


def require_reparse_dir(link: Path, target: Path) -> None:
    """Create a directory reparse point or skip when the host genuinely cannot."""
    if not try_reparse_dir(link, target):
        pytest.skip("this host cannot create a directory reparse point")


# --- GREPTILE-G1: symbolic ref must not escape the metadata base ------------


@pytest.mark.parametrize(
    "reference",
    [
        "refs/heads/main",
        "refs/tags/v1",
        "refs/remotes/origin/main",
    ],
)
def test_safe_metadata_reference_accepts_ordinary_refs(harness: ModuleType, reference: str) -> None:
    assert harness.require_safe_metadata_reference(reference) == Path(*reference.split("/"))


@pytest.mark.parametrize(
    "reference",
    [
        "C:/attacker/ref",
        "C:\\attacker\\ref",
        "/etc/attacker-ref",
        "\\\\server\\share\\ref",
        "C:ref",
        "../../../attacker/ref",
        "refs/../../../attacker/ref",
        "refs/heads/../../../../attacker",
    ],
)
def test_safe_metadata_reference_refuses_escapes(harness: ModuleType, reference: str) -> None:
    with pytest.raises(harness.PathSeparationRefusalError):
        harness.require_safe_metadata_reference(reference)


def test_g1_absolute_symbolic_ref_is_refused(harness: ModuleType, tmp_path: Path) -> None:
    external = tmp_path / "outside"
    external.mkdir()
    planted = external / "attacker-ref"
    planted.write_text(f"{EXTERNAL_COMMIT}\n", encoding="utf-8")

    root = tmp_path / "repo"
    write_synthetic_git(root)
    (root / ".git" / "HEAD").write_text(f"ref: {planted}\n", encoding="utf-8")

    with pytest.raises(harness.PathSeparationRefusalError):
        harness.resolve_canonical_commit(root)
    # The planted external file is never accepted as repository identity.
    assert planted.read_text(encoding="utf-8").strip() == EXTERNAL_COMMIT


def test_g1_parent_traversal_symbolic_ref_is_refused(harness: ModuleType, tmp_path: Path) -> None:
    external = tmp_path / "outside"
    external.mkdir()
    (external / "attacker-ref").write_text(f"{EXTERNAL_COMMIT}\n", encoding="utf-8")

    root = tmp_path / "repo"
    write_synthetic_git(root)
    (root / ".git" / "HEAD").write_text("ref: ../../outside/attacker-ref\n", encoding="utf-8")

    with pytest.raises(harness.PathSeparationRefusalError):
        harness.resolve_canonical_commit(root)


def test_g1_escaped_reference_never_becomes_repository_identity(
    harness: ModuleType, tmp_path: Path
) -> None:
    """No escape shape may yield the external commit, whatever the refusal class."""
    external = tmp_path / "outside"
    external.mkdir()
    planted = external / "attacker-ref"
    planted.write_text(f"{EXTERNAL_COMMIT}\n", encoding="utf-8")

    for index, reference in enumerate(
        [str(planted), "../../outside/attacker-ref", "refs/../../../outside/attacker-ref"]
    ):
        root = tmp_path / f"repo-{index}"
        write_synthetic_git(root)
        (root / ".git" / "HEAD").write_text(f"ref: {reference}\n", encoding="utf-8")
        with pytest.raises(harness.HarnessError) as caught:
            harness.resolve_canonical_commit(root)
        assert EXTERNAL_COMMIT not in str(caught.value)


def test_g1_ordinary_loose_ref_still_resolves(harness: ModuleType, tmp_path: Path) -> None:
    write_synthetic_git(tmp_path)
    assert harness.resolve_canonical_commit(tmp_path) == SYNTHETIC_COMMIT
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


def test_g1_packed_refs_still_resolves(harness: ModuleType, tmp_path: Path) -> None:
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (git / "packed-refs").write_text(
        f"# pack-refs with: peeled\n{SYNTHETIC_COMMIT} refs/heads/main\n", encoding="utf-8"
    )
    assert harness.resolve_canonical_commit(tmp_path) == SYNTHETIC_COMMIT
    assert harness.resolve_canonical_commit(tmp_path) == resolve_repository_commit(tmp_path)


# --- GREPTILE-G2: reparse components must not be resolved away --------------


def test_g2_relative_gitdir_through_a_reparse_component_is_refused(
    harness: ModuleType, tmp_path: Path
) -> None:
    real = tmp_path / "real-meta"
    (real / "refs" / "heads").mkdir(parents=True)
    (real / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (real / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")

    root = tmp_path / "repo"
    root.mkdir()
    require_reparse_dir(root / "linked-meta", real)
    (root / ".git").write_text("gitdir: linked-meta\n", encoding="utf-8")

    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(root)


def test_g2_relative_commondir_through_a_reparse_component_is_refused(
    harness: ModuleType, tmp_path: Path
) -> None:
    common = tmp_path / "real-common"
    (common / "refs" / "heads").mkdir(parents=True)
    (common / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")

    git_dir = tmp_path / "repo" / ".git"
    git_dir.mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    require_reparse_dir(git_dir / "linked-common", common)
    (git_dir / "commondir").write_text("linked-common\n", encoding="utf-8")

    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(tmp_path / "repo")


def test_g2_reparse_git_metadata_entry_is_refused(harness: ModuleType, tmp_path: Path) -> None:
    real = tmp_path / "real-git"
    (real / "refs" / "heads").mkdir(parents=True)
    (real / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (real / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")

    root = tmp_path / "repo"
    root.mkdir()
    require_reparse_dir(root / ".git", real)

    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(root)


def test_g2_reparse_ref_component_is_refused(harness: ModuleType, tmp_path: Path) -> None:
    external = tmp_path / "outside-refs"
    (external / "heads").mkdir(parents=True)
    (external / "heads" / "main").write_text(f"{EXTERNAL_COMMIT}\n", encoding="utf-8")

    root = tmp_path / "repo"
    git = root / ".git"
    git.mkdir(parents=True)
    (git / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    require_reparse_dir(git / "refs", external)

    with pytest.raises(harness.ReparsePointRefusalError):
        harness.resolve_canonical_commit(root)


def test_g2_normal_git_directory_still_passes(harness: ModuleType, tmp_path: Path) -> None:
    write_synthetic_git(tmp_path)
    assert harness.resolve_canonical_commit(tmp_path) == SYNTHETIC_COMMIT


def test_g2_worktree_relative_commondir_is_preserved(harness: ModuleType, tmp_path: Path) -> None:
    """A legitimate worktree ``commondir`` of ``../..`` must not be rejected."""
    repo = tmp_path / "repo"
    git = repo / ".git"
    (git / "refs" / "heads").mkdir(parents=True)
    (git / "refs" / "heads" / "main").write_text(f"{SYNTHETIC_COMMIT}\n", encoding="utf-8")
    worktree_meta = git / "worktrees" / "wt"
    worktree_meta.mkdir(parents=True)
    (worktree_meta / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (worktree_meta / "commondir").write_text("../..\n", encoding="utf-8")

    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / ".git").write_text(f"gitdir: {worktree_meta}\n", encoding="utf-8")

    assert harness.resolve_canonical_commit(checkout) == SYNTHETIC_COMMIT


def test_g2_lexical_dot_segments_are_honoured(harness: ModuleType, tmp_path: Path) -> None:
    write_synthetic_git(tmp_path)
    walked = harness.resolve_metadata_path(tmp_path / ".git", Path("refs/./heads/../heads/main"))
    assert walked == tmp_path / ".git" / "refs" / "heads" / "main"


# --- GREPTILE-G3: episode directory redirect --------------------------------


def _redirect_episode_directory(lab: Lab, tmp_path: Path) -> Path:
    """Move a valid episode outside the evidence root and redirect to it."""
    external = tmp_path / "outside-evidence"
    external.mkdir(exist_ok=True)
    target = external / lab.episode_id
    shutil.move(str(lab.directory), str(target))
    require_reparse_dir(lab.directory, target)
    return target


def test_g3_redirected_episode_directory_refuses_every_command(
    lab: Lab, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lab.open_episode()
    target = _redirect_episode_directory(lab, tmp_path)
    before = digest_tree(target)

    spy, runner = install_spy(lab, monkeypatch)
    for argv in (lab.generate_argv("A"), lab.compare_argv(), lab.verify_argv()):
        with pytest.raises(lab.module.ReparsePointRefusalError):
            lab.run(argv, runner=runner)
    assert spy.input_hashes == 0
    assert spy.child_launches == 0
    assert not lab.workspace_a.exists()

    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.run(lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN"))
    assert not (target / "episode-invalidation.jsonl").exists()

    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.run(lab.finalize_argv())
    assert not (target / "episode-manifest.json").exists()

    # The redirect target is never read from, written to or repaired.
    assert digest_tree(target) == before


def test_g3_redirected_episode_directory_writes_nothing_outside_the_root(
    lab: Lab, tmp_path: Path
) -> None:
    lab.open_episode()
    target = _redirect_episode_directory(lab, tmp_path)
    before = digest_tree(target)
    for argv in (
        lab.finalize_argv(),
        lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="FINALIZE"),
    ):
        with pytest.raises(lab.module.ReparsePointRefusalError):
            lab.run(argv)
    assert digest_tree(target) == before
    assert sorted(entry.name for entry in target.iterdir()) == ["episode-core.json"]


def test_g3_normal_episode_directory_remains_functional(lab: Lab) -> None:
    """The G3 guard is narrowly targeted: an ordinary episode still completes."""
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_COMPLETE_EQUAL"


def test_g3_episode_directory_guard_requires_containment(lab: Lab, tmp_path: Path) -> None:
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    with pytest.raises(lab.module.PathSeparationRefusalError):
        lab.module.require_safe_episode_directory(outside, lab.evidence_root)
    inside = lab.evidence_root / "ep"
    inside.mkdir()
    identity = lab.module.require_safe_episode_directory(inside, lab.evidence_root)
    assert isinstance(identity, str)
    assert len(identity) == 64
    # The gate is stable for an unchanged directory.
    assert (
        lab.module.require_safe_episode_directory(inside, lab.evidence_root, identity) == identity
    )


def test_g3_redirected_evidence_file_is_never_appended(lab: Lab, tmp_path: Path) -> None:
    lab.open_episode()
    external = tmp_path / "outside-file"
    external.mkdir()
    planted = external / "stolen.jsonl"
    planted.write_bytes(b"")
    journal = lab.directory / "stage-generate-a.jsonl"
    if not try_symlink(journal, planted, directory=False):
        pytest.skip("this host cannot create a file reparse point")
    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.module.append_canonical_event(
            lab.module.EvidenceStore(), journal, {"schema_version": "x", "event": "y"}
        )
    assert planted.read_bytes() == b""


# ===========================================================================
# CC. PA2G-R1 — in-flight episode-path TOCTOU
# ===========================================================================


def _unpinned(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    """Disable the OS-level directory pin to exercise the detection layer alone.

    Windows blocks the swap outright while the harness holds the episode
    directory open, so the ordered gate would otherwise never be reached here.
    Platforms without that guarantee rely on the gate, and this is how that path
    is exercised deterministically.
    """
    monkeypatch.setattr(lab.module.EpisodeContext, "pinned", lambda self: contextlib.nullcontext())


def _swapping_runner(lab: Lab, tmp_path: Path, swapped: dict[str, Any]) -> Any:
    """A child that, while running, lets the episode directory be swapped."""
    external = tmp_path / "attacker"
    external.mkdir(exist_ok=True)
    stolen = external / lab.episode_id
    swapped["stolen"] = stolen

    def _swap_while_running(_command: Sequence[str]) -> None:
        try:
            shutil.move(str(lab.directory), str(stolen))
            swapped["ok"] = try_reparse_dir(lab.directory, stolen)
        except OSError as error:
            swapped["ok"] = False
            swapped["blocked"] = type(error).__name__
        write_workspace(lab.workspace_a)

    return make_runner(lab.module, on_run=_swap_while_running)


def _sealed_anywhere(*roots: Path) -> bool:
    return any(
        b"stage_sealed" in path.read_bytes()
        for root in roots
        if root.exists()
        for path in root.rglob("*.jsonl")
    )


def test_r1_t1_midflight_swap_refuses_without_sealing(
    lab: Lab, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """R1-T1: a swap while the child is in flight must not produce a sealed stage."""
    lab.open_episode()
    _unpinned(lab, monkeypatch)
    swapped: dict[str, Any] = {}
    runner = _swapping_runner(lab, tmp_path, swapped)
    with pytest.raises(lab.module.HarnessError):
        lab.run(lab.generate_argv("A"), runner=runner)
    assert swapped["ok"] is True
    assert not _sealed_anywhere(lab.evidence_root, swapped["stolen"].parent)


def test_r1_t1_midflight_swap_is_prevented_while_pinned(lab: Lab, tmp_path: Path) -> None:
    """R1-T1 (prevention): the held pin blocks the swap where the OS honours it."""
    lab.open_episode()
    swapped: dict[str, Any] = {}
    runner = _swapping_runner(lab, tmp_path, swapped)
    exit_code = lab.run(lab.generate_argv("A"), runner=runner)
    if swapped.get("ok"):
        pytest.skip("this platform does not pin an open directory against rename")
    # The swap was refused by the OS, so the stage completes inside the root.
    assert exit_code == 0
    events = [event["event"] for event in lab.journal("stage-generate-a.jsonl")]
    assert events[-1] == "stage_sealed"
    assert lab.directory.is_dir()


def test_r1_t2_swap_after_inputs_hashed_refuses_at_the_next_gate(
    lab: Lab, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """R1-T2: a swap after inputs_hashed is caught before the next durable write."""
    lab.open_episode()
    _unpinned(lab, monkeypatch)
    external = tmp_path / "attacker-t2"
    external.mkdir()
    stolen = external / lab.episode_id
    real_append = lab.module.StageJournal.append
    state = {"done": False}

    def swapping_append(self: Any, event: str, fields: Any = None) -> None:
        real_append(self, event, fields)
        if event == "inputs_hashed" and not state["done"]:
            state["done"] = True
            shutil.move(str(lab.directory), str(stolen))
            require_reparse_dir(lab.directory, stolen)

    monkeypatch.setattr(lab.module.StageJournal, "append", swapping_append)
    with pytest.raises(lab.module.HarnessError):
        lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A"))
    assert state["done"] is True
    assert not _sealed_anywhere(lab.evidence_root, external)


def test_r1_t3_parent_component_swap_is_refused(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    """R1-T3: a reparse introduced at a parent component of the episode path refuses."""
    lab.open_episode()
    _unpinned(lab, monkeypatch)
    directory = lab.directory
    monkeypatch.setattr(lab.module, "is_reparse_point", lambda path: path == directory.parent)
    with pytest.raises(lab.module.ReparsePointRefusalError):
        lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A"))
    assert not _sealed_anywhere(lab.evidence_root)


def test_r1_t4_non_reparse_identity_swap_is_refused(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    """R1-T4: a real-directory-for-real-directory swap inside the root still refuses.

    Reparse and containment both pass here, so the measured path identity is the
    only thing that can detect it.
    """
    lab.open_episode()
    _unpinned(lab, monkeypatch)
    original = lab.directory
    parked = lab.evidence_root / "parked"
    real_append = lab.module.StageJournal.append
    state = {"done": False}

    def swapping_append(self: Any, event: str, fields: Any = None) -> None:
        real_append(self, event, fields)
        if event == "stage_opened" and not state["done"]:
            state["done"] = True
            shutil.move(str(original), str(parked))
            shutil.copytree(str(parked), str(original))

    monkeypatch.setattr(lab.module.StageJournal, "append", swapping_append)
    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A"))
    assert state["done"] is True
    assert not _sealed_anywhere(lab.evidence_root)


def test_r1_t4_drift_class_maps_to_the_path_safety_triad(harness: ModuleType) -> None:
    assert harness.EpisodePathIdentityDriftError.failure_class == "EPISODE_PATH_IDENTITY_DRIFT"
    assert harness.derive_failure_triad("EPISODE_PATH_IDENTITY_DRIFT") == (
        "EPISODE_PATH_IDENTITY_DRIFT",
        "PATH_SAFETY_FAILURE",
        "FOUNDER_DISPOSITION_REQUIRED",
    )
    # The drift class is fatal, so it never reaches the stage-sealing helper.
    assert "EPISODE_PATH_IDENTITY_DRIFT" not in harness.REFUSAL_FAILURE_CLASSES


def test_r1_t5_negative_control_ordinary_run_seals_normally(lab: Lab) -> None:
    """R1-T5: with no swap, the stage seals normally and identity is stable."""
    lab.open_episode()
    identity = lab.module.require_safe_episode_directory(lab.directory, lab.evidence_root)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    events = [event["event"] for event in lab.journal("stage-generate-a.jsonl")]
    assert len(events) == 9
    assert events[-1] == "stage_sealed"
    after = lab.module.require_safe_episode_directory(lab.directory, lab.evidence_root)
    assert after == identity
    assert lab.module.is_within(lab.directory, lab.evidence_root)


def test_r1_t6_identity_is_recomputable_and_detects_a_swap(lab: Lab) -> None:
    """R1-T6: the measured identity is independently recomputable and swap-sensitive."""
    lab.open_episode()
    pinned = lab.module.measure_episode_path_identity(lab.directory)
    assert pinned == lab.module.measure_episode_path_identity(lab.directory)
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes

    info = lab.directory.stat(follow_symlinks=False)
    expected = sha256_of_bytes(
        canonical_json_bytes({"st_dev": int(info.st_dev), "st_ino": int(info.st_ino)})
    )
    assert pinned == expected
    # No host device or inode number is exposed by the measured value.
    assert str(info.st_ino) not in pinned
    replacement = lab.evidence_root / "replacement"
    replacement.mkdir()
    assert lab.module.measure_episode_path_identity(replacement) != pinned
    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.module.require_safe_episode_directory(replacement, lab.evidence_root, pinned)


def test_r1_every_stage_event_is_gated(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> None:
    """The ordered gate fires before each of the nine stage events, not only at seal.

    Instrumented at the *store*, so "gated" means the gate was the last thing to
    run before the durable write. Hooking ``StageJournal.append`` instead would
    only show that a gate ran somewhere inside the call, which is the weaker
    property `F-2` found insufficient.
    """
    lab.open_episode()
    gated: list[str] = []
    inside_gate = [0]
    real_store_append = lab.module.EvidenceStore.append
    real_guard = lab.module.EpisodeContext.require_safe_directory

    def counting_guard(self: Any) -> Any:
        gated.append("gate")
        inside_gate[0] += 1
        try:
            return real_guard(self)
        finally:
            inside_gate[0] -= 1

    def recording_append(self: Any, path: Path, payload: bytes) -> None:
        event = _event_of(payload)
        if event:
            gated.append(event)
        real_store_append(self, path, payload)

    monkeypatch.setattr(lab.module.EpisodeContext, "require_safe_directory", counting_guard)
    monkeypatch.setattr(lab.module.EvidenceStore, "append", recording_append)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    events = [entry for entry in gated if entry != "gate"]
    assert len(events) == 9
    # Every durable event write is immediately preceded by a gate run.
    for index, entry in enumerate(gated):
        if entry != "gate":
            assert index > 0, f"{entry} was written before any gate ran"
            assert gated[index - 1] == "gate", f"{entry} was not gated immediately"


# ===========================================================================
# AC. PA3-R1 / PA3-R2 — cross-command continuity anchor and seal ordering
#
# F-1: episode path identity was measured fresh by every command, so a
# real-directory-for-real-directory substitution *between* commands passed
# reparse and containment, presented a copied core, and silently established a
# fresh trust root.  F-2: the gate authorizing ``stage_sealed`` ran before the
# record was even built, leaving Python-level work between the check and the
# write it guarded.
# ===========================================================================

#: The founder-amended seven-field manifest set, transcribed from
#: ``evidence-contract.md`` §15.4 as amended by ``PA3-AMD-2``.  It is an expected
#: value taken from the P-A1 document, never one discovered from the module.
EXPECTED_MANIFEST_FIELDS = (
    "schema_version",
    "episode_identity",
    "episode_path_identity",
    "episode_core",
    "records",
    "terminal_disposition",
    "manifest_sealed_at",
)

EXPECTED_MANIFEST_SCHEMA_VERSION = "mesc-p01-04d-execution-evidence/episode-manifest/v1"


def _park_and_substitute_real_directory(lab: Lab) -> Path:
    """Substitute a *different* real directory carrying byte-identical contents.

    This is the F-1 attacker: not a symlink, not a junction, not an escape from
    the evidence root.  A genuine directory, inside the root, whose every byte
    was copied from the real episode — including ``episode-core.json``.  Reparse
    and containment cannot see it, and neither can any check that reads only what
    lies inside the directory.

    The parked original keeps its inode, because a same-volume move is a rename.
    That is deliberate: path identity names the directory *object*, so the
    returned path is still the authorized episode and the substitute is not.
    """
    original = lab.directory
    parked = lab.evidence_root / f"{lab.episode_id}-parked"
    shutil.move(str(original), str(parked))
    shutil.copytree(str(parked), str(original))
    return parked


def test_s2_t1_between_command_directory_replacement_is_refused(lab: Lab) -> None:
    """S2-T1: a swap between two commands cannot bootstrap itself as the continuation."""
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    held = lab.continuity

    parked = _park_and_substitute_real_directory(lab)
    # Invisible to every in-directory check: the bytes are identical.
    assert digest_tree(lab.directory) == digest_tree(parked)
    assert lab.module.measure_episode_path_identity(lab.directory) != (
        lab.module.measure_episode_path_identity(parked)
    )

    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("B", continuity=held), runner=lab.producing_runner("B"))
    # No new stage was opened or sealed in the substitute. Its copy of the
    # Generation A journal is of course still a copy — that is the attack, and
    # what matters is that it can never be advanced or terminalized.
    assert not (lab.directory / "stage-generate-b.jsonl").exists()
    assert digest_tree(lab.directory) == digest_tree(parked)

    # The replacement can never be terminalized either.
    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.finalize_argv(continuity=held))
    assert not (lab.directory / "episode-manifest.json").exists()


def test_s2_t2_history_rewind_by_replacement_is_refused(lab: Lab) -> None:
    """S2-T2: erasing a sealed history by directory replacement does not replay it."""
    lab.open_episode()
    failing = make_runner(lab.module, exit_code=3, stderr=b"synthetic operator failure\n")
    assert lab.run(lab.generate_argv("A"), runner=failing) == 1
    events = lab.journal("stage-generate-a.jsonl")
    assert events[-1]["stage_disposition"] == "STAGE_FAILED"
    held = lab.continuity

    # The attacker rewinds to a fresh directory holding only the copied core.
    original = lab.directory
    parked = lab.evidence_root / f"{lab.episode_id}-rewound"
    shutil.move(str(original), str(parked))
    original.mkdir()
    shutil.copy2(parked / "episode-core.json", original / "episode-core.json")

    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("A", continuity=held), runner=lab.producing_runner("A"))
    assert not (original / "stage-generate-a.jsonl").exists()
    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.finalize_argv(continuity=held))
    assert not (original / "episode-manifest.json").exists()


def test_s2_t2b_in_place_history_rewind_is_refused_by_the_digest_chain(lab: Lab) -> None:
    """S2-T2b: the rewind identity alone cannot see — same object, deleted history.

    ``st_ino`` is unchanged here, so a continuity anchor built on path identity
    alone would accept this.  Covering the exact bytes of every record present is
    what refuses it, which is why the digest chain is not optional.
    """
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    held = lab.continuity
    before = lab.module.measure_episode_path_identity(lab.directory)

    (lab.directory / "stage-generate-a.jsonl").unlink()
    assert lab.module.measure_episode_path_identity(lab.directory) == before

    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("A", continuity=held), runner=lab.producing_runner("A"))
    assert not (lab.directory / "stage-generate-a.jsonl").exists()


def _write_call_trace(lab: Lab, monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record gate runs, preparation steps and durable writes in real order.

    Instrumenting the *store* is what makes this discriminating.  A gate that
    merely ran somewhere earlier still appears before the write; only the
    preparation steps showing up between the two reveal that the check was
    authorizing a write in its own future.

    Work performed *inside* the gate is not work between the gate and the write,
    so nested calls are suppressed while the guard is on the stack — the gate
    itself serializes a ``(st_dev, st_ino)`` pair to measure identity.
    """
    trace: list[str] = []
    inside_gate = [0]
    real_guard = lab.module.EpisodeContext.require_safe_directory
    real_serialize = lab.module.canonical_json_bytes
    real_safe_path = lab.module.require_safe_evidence_path
    real_size = lab.module._byte_size
    real_append = lab.module.EvidenceStore.append

    def record_step(name: str) -> None:
        if not inside_gate[0]:
            trace.append(name)

    def guard(self: Any) -> Any:
        trace.append("GATE")
        inside_gate[0] += 1
        try:
            return real_guard(self)
        finally:
            inside_gate[0] -= 1

    def serialize(record: Any) -> Any:
        record_step("SERIALIZE")
        return real_serialize(record)

    def safe_path(path: Path) -> Any:
        record_step("PATH")
        return real_safe_path(path)

    def size(path: Path) -> Any:
        record_step("SIZE")
        return real_size(path)

    def append(self: Any, path: Path, payload: bytes) -> None:
        trace.append(f"WRITE:{_event_of(payload)}")
        real_append(self, path, payload)

    monkeypatch.setattr(lab.module.EpisodeContext, "require_safe_directory", guard)
    monkeypatch.setattr(lab.module, "canonical_json_bytes", serialize)
    monkeypatch.setattr(lab.module, "require_safe_evidence_path", safe_path)
    monkeypatch.setattr(lab.module, "_byte_size", size)
    monkeypatch.setattr(lab.module.EvidenceStore, "append", append)
    return trace


def test_s2_t3_the_gate_is_the_last_step_before_every_durable_write(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    """S2-T3: nothing runs between the authorizing gate and the write it guards."""
    lab.open_episode()
    trace = _write_call_trace(lab, monkeypatch)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0

    seal = trace.index("WRITE:stage_sealed")
    assert trace[seal - 1] == "GATE", trace[max(0, seal - 6) : seal + 1]
    for position, entry in enumerate(trace):
        if entry.startswith("WRITE:"):
            assert trace[position - 1] == "GATE", f"{entry} was not gated immediately"


def test_s2_t4_the_post_write_gate_is_defence_in_depth_only(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    """S2-T4: security does not rest on noticing drift after the bytes landed.

    The seal keeps a gate after the write, but it is a reporter.  What must hold
    is that the authorizing gate already ran with no preparation between it and
    the write, so deleting the post-write gate could not make an unauthorized
    seal durable.
    """
    lab.open_episode()
    trace = _write_call_trace(lab, monkeypatch)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0

    seal = trace.index("WRITE:stage_sealed")
    before_seal = trace[:seal]
    last_gate = len(before_seal) - 1 - before_seal[::-1].index("GATE")
    # Preparation completes before the authorizing gate, never after it.
    assert not any(step in trace[last_gate + 1 : seal] for step in ("SERIALIZE", "PATH", "SIZE"))
    # A gate does follow the write, and it is not what authorized it.
    assert "GATE" in trace[seal + 1 :]


def test_s2_t5_the_expected_token_comes_from_argv_and_nowhere_else(lab: Lab) -> None:
    """S2-T5: no episode-local file carries a value that could stand in for the token."""
    lab.complete_success()
    held = lab.continuity
    assert len(held) == 64

    for path in sorted(lab.directory.iterdir()):
        payload = path.read_bytes()
        assert held.encode() not in payload, f"{path.name} carries the continuity token"
        assert b"expect-continuity" not in payload
        assert b"continuity_token" not in payload

    assert lab.run(lab.finalize_argv()) == 0
    for path in sorted(lab.directory.iterdir()):
        assert held.encode() not in path.read_bytes()


def test_s2_t5b_a_missing_token_is_refused_and_never_defaulted(lab: Lab) -> None:
    """S2-T5b: the argument is required, so no command can fall back to a default."""
    lab.open_episode()
    for argv in (
        lab.generate_argv("A"),
        lab.compare_argv(),
        lab.verify_argv(),
        lab.invalidate_argv(failure_class="UNCLASSIFIED", causal_stage="OPEN"),
        lab.finalize_argv(),
    ):
        stripped = list(argv)
        position = stripped.index("--expect-continuity")
        del stripped[position : position + 2]
        with pytest.raises(SystemExit) as refusal:
            lab.module.build_parser().parse_args(stripped)
        assert refusal.value.code == 2
    # ``open`` is the one command with no predecessor, so it accepts no token.
    with pytest.raises(SystemExit):
        lab.module.build_parser().parse_args([*lab.open_argv(), "--expect-continuity", "0" * 64])


@pytest.mark.parametrize("case", ["wrong", "stale", "foreign", "pre-swap"])
def test_s2_t6_token_substitution_and_replay_are_refused(lab: Lab, case: str) -> None:
    """S2-T6: wrong, stale, foreign and pre-swap tokens each fail closed."""
    lab.open_episode()
    genesis = lab.continuity
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    current = lab.continuity

    if case == "wrong":
        supplied = "0" * 64
    elif case == "stale":
        # token_0 replayed at step 1: the state has advanced past it.
        supplied = genesis
        assert supplied != current
    elif case == "foreign":
        other = Lab(
            module=lab.module,
            repository_root=lab.repository_root,
            evidence_root=lab.evidence_root,
            workspace_a=lab.workspace_a,
            workspace_b=lab.workspace_b,
            future_evidence_root=lab.future_evidence_root,
            inputs=lab.inputs,
            episode_id="episode-foreign",
        )
        other.open_episode()
        supplied = other.continuity
    else:
        # The token derived from the genuine directory, offered against a copy.
        _park_and_substitute_real_directory(lab)
        supplied = current

    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("B", continuity=supplied), runner=lab.producing_runner("B"))
    assert not (lab.directory / "stage-generate-b.jsonl").exists()


def test_s2_t7_negative_control_ordinary_continuation_seals_normally(lab: Lab) -> None:
    """S2-T7: the honest sequence advances a token at every step and seals EQUAL."""
    tokens: list[str] = []
    lab.open_episode()
    tokens.append(lab.continuity)
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    tokens.append(lab.continuity)
    assert lab.run(lab.generate_argv("B"), runner=lab.producing_runner("B")) == 0
    tokens.append(lab.continuity)
    assert lab.run(lab.compare_argv(), runner=make_runner(lab.module)) == 0
    tokens.append(lab.continuity)
    assert lab.run(lab.verify_argv(), runner=make_runner(lab.module)) == 0
    tokens.append(lab.continuity)

    assert len(set(tokens)) == len(tokens), "the token must advance at every step"
    assert all(len(token) == 64 for token in tokens)
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.manifest()["terminal_disposition"] == "EPISODE_COMPLETE_EQUAL"


def test_s2_t8_manifest_binds_path_identity_at_seven_fields_on_v1(lab: Lab) -> None:
    """S2-T8: the founder-authorized seven-field manifest, still on the v1 literal."""
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    manifest = lab.manifest()

    assert len(EXPECTED_MANIFEST_FIELDS) == 7
    assert tuple(sorted(manifest)) == tuple(sorted(EXPECTED_MANIFEST_FIELDS))
    assert lab.module.EPISODE_MANIFEST_FIELDS == EXPECTED_MANIFEST_FIELDS
    assert manifest["schema_version"] == EXPECTED_MANIFEST_SCHEMA_VERSION
    assert lab.module.EPISODE_MANIFEST_SCHEMA_VERSION == EXPECTED_MANIFEST_SCHEMA_VERSION
    assert "v2" not in str(manifest["schema_version"])
    assert manifest["episode_path_identity"] == (
        lab.module.measure_episode_path_identity(lab.directory)
    )


def test_s2_t8b_a_relocated_manifest_has_no_terminal_identity(lab: Lab) -> None:
    """S2-T8b: §15.4's verifier obligation — a copied manifest is TM-1 where it sits."""
    lab.complete_success()
    assert lab.run(lab.finalize_argv()) == 0
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_VALID

    parked = _park_and_substitute_real_directory(lab)
    assert (parked / "episode-manifest.json").read_bytes() == (
        (lab.directory / "episode-manifest.json").read_bytes()
    )
    # The substitute holds identical bytes and has no terminal identity at all.
    assert lab.module.classify_terminal_manifest(lab.directory) == lab.module.TM_INVALID
    with pytest.raises(lab.module.EpisodeStateError):
        lab.module.terminal_identity(lab.directory)
    # The binding follows the directory object, not the path: the renamed
    # original is still the sealed episode.
    assert lab.module.classify_terminal_manifest(parked) == lab.module.TM_VALID


def test_s2_t9_an_in_directory_anchor_never_becomes_a_trust_source(lab: Lab) -> None:
    """S2-T9: planting the token inside the episode does not let a command use it."""
    lab.open_episode()
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0
    held = lab.continuity

    _park_and_substitute_real_directory(lab)
    # The attacker plants the anchor the abandoned design would have trusted.
    for name in ("episode-path-identity.json", ".continuity", "episode-continuity.json"):
        (lab.directory / name).write_text(
            json.dumps({"episode_path_identity": held, "continuity_token": held}),
            encoding="utf-8",
        )

    with pytest.raises(lab.module.EpisodePathIdentityDriftError):
        lab.run(lab.generate_argv("B", continuity=held), runner=lab.producing_runner("B"))
    assert "episode-path-identity.json" not in EXPECTED_EVIDENCE_FILENAMES
    assert len(EXPECTED_EVIDENCE_FILENAMES) == 7


def test_s2_t9b_the_token_covers_only_the_closed_inventory(lab: Lab) -> None:
    """S2-T9b: a planted non-evidence file cannot perturb the anchor either way."""
    lab.open_episode()
    before = lab.continuity
    (lab.directory / "episode-path-identity.json").write_text("{}", encoding="utf-8")
    identity = lab.module.measure_episode_path_identity(lab.directory)
    assert lab.module.measure_continuity_token(lab.directory, identity) == before
    assert lab.run(lab.generate_argv("A"), runner=lab.producing_runner("A")) == 0


def _fresh_context(lab: Lab) -> Any:
    return lab.module.open_episode_context(
        episode_id=lab.episode_id,
        repository_root=lab.repository_root,
        evidence_root=lab.evidence_root,
        store=lab.module.EvidenceStore(),
        expected_continuity=lab.continuity,
    )


def test_s2_pin_failure_on_a_capable_platform_is_terminal(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F-5: acquisition failure where pinning works is a refusal, never a silent yield."""
    lab.open_episode()
    context = _fresh_context(lab)
    monkeypatch.setattr(lab.module, "_PIN_CAPABLE_PLATFORM", True)
    (lab.directory / "episode-core.json").unlink()
    with pytest.raises(lab.module.EpisodePathIdentityDriftError), context.pinned():
        pytest.fail("the write-bearing span must not run unpinned on a capable platform")


def test_s2_pin_incapable_platform_is_an_explicit_documented_branch(
    lab: Lab, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F-5: the incapable branch is chosen by capability, not by catching OSError."""
    lab.open_episode()
    context = _fresh_context(lab)
    monkeypatch.setattr(lab.module, "_PIN_CAPABLE_PLATFORM", False)
    (lab.directory / "episode-core.json").unlink()
    entered = False
    with context.pinned():
        entered = True
    assert entered, "the incapable platform proceeds detection-only"

    source = HARNESS_PATH.read_text(encoding="utf-8")
    pinned = source.split("    def pinned(")[1].split("\n    def ")[0]
    assert "_PIN_CAPABLE_PLATFORM" in pinned
    assert "raise EpisodePathIdentityDriftError" in pinned
    # No bare swallow: the only OSError handler re-raises.
    assert "except OSError:" not in pinned


def test_s2_continuity_token_is_derived_through_the_frozen_serializer(lab: Lab) -> None:
    """The token is a pure function of the directory object and its exact bytes."""
    from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes

    lab.open_episode()
    identity = lab.module.measure_episode_path_identity(lab.directory)
    evidence = lab.module.evidence_state_digests(lab.directory)
    expected = sha256_of_bytes(
        canonical_json_bytes(
            {
                "schema": lab.module.CONTINUITY_TOKEN_SCHEMA,
                "episode_path_identity": identity,
                "evidence": list(evidence),
            }
        )
    )
    assert lab.module.measure_continuity_token(lab.directory, identity) == expected
    assert lab.continuity == expected
