"""Operator-safety contract of the CLI: friendly failures, no data loss, corrections.

These tests pin the Research Readiness guarantees: a typo'd --root exits 2 with advice
(never a traceback, never fabricated empty statistics), an interrupted extraction
session keeps every object the operator was told was recorded, and a wrong screening
decision is correctable through an append-only amend event.
"""

from __future__ import annotations

from pathlib import Path
from typing import NoReturn

import pytest

from medscale import cli
from medscale.cli import mesc_eval
from medscale.evidence_store import load_evidence
from medscale.litdb import RawRetrieval
from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.review import ReviewDecision, current_reviews, make_event
from medscale.litdb.review import append_events as append_review_events
from medscale.litdb.store import write_corpus
from medscale.mesc._b0 import B0Config
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult, ModelRef
from medscale.provenance import Provenance, SourceAPI

_B0_MODEL = "meta-llama/Llama-3.2-3B-Instruct"


class _FakeB0Generator:
    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text="yes", model=ModelRef(model_id=_B0_MODEL, revision="rev-1", backend="transformers")
        )


def _fake_b0_factory(config: B0Config) -> _FakeB0Generator:
    return _FakeB0Generator()


def _write_b0_input(path: Path) -> None:
    path.write_text(
        '{"example_id":"e0","row_ordinal":0,"source_document_id":"pmid:1",'
        '"dataset_id":"ds","dataset_revision":"rev-1","configuration":"cfg",'
        '"question":"does aspirin help?","context":["some context"],"decision":"yes"}\n',
        encoding="utf-8",
    )


_TS = "2026-07-12T00:00:00+00:00"


def _seed_corpus(root: Path, *, decision: ReviewDecision | None = None) -> LiteratureRecord:
    retrieval = RawRetrieval(SourceAPI.OPENALEX, "q", _TS, payload="anchored")
    record = LiteratureRecord(
        identifiers=Identifiers(doi="10.1/ux"),
        title="A study of operator ergonomics in screening tools",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, "10.1/ux", _TS, retrieval.payload_sha256()),
        year=2026,
        abstract="We measure decision friction.",
    )
    write_corpus(root / "corpus" / "records.jsonl", [record])
    if decision is not None:
        event = make_event(
            record.record_id,
            decision,
            reviewer="tester",
            decided_at=_TS,
            software_version="0.0.0",
            git_sha="abcdef1",
        )
        append_review_events(root / "screening" / "review_log.jsonl", (event,))
    return record


# ---------------------------------------------------------------- friendly failures
def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--version"]) == 0
    assert capsys.readouterr().out.startswith("medscale ")


@pytest.mark.parametrize(
    "argv",
    [
        ["screen", "status", "--root", "no/such/root"],
        ["extract", "--root", "no/such/root"],
        ["check", "--root", "no/such/root"],
        ["stats", "--root", "no/such/root"],
        ["snapshot", "--root", "no/such/root"],
        ["bench", "list", "--root", "no/such/root"],
    ],
)
def test_missing_root_fails_with_advice_not_traceback(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(argv) == 2
    captured = capsys.readouterr()
    assert "workspace root not found" in captured.err
    # Critically: stats must not fabricate an empty-but-plausible document.
    assert "total_records" not in captured.out


def test_empty_existing_root_is_still_a_valid_fresh_workspace(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["stats", "--root", str(tmp_path)]) == 0
    assert '"total_records":0' in capsys.readouterr().out


def test_snapshot_verify_missing_file_is_friendly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["snapshot", "--root", str(tmp_path), "--verify", "no-such.json"]) == 2
    assert "snapshot file not found" in capsys.readouterr().err


def test_bench_unknown_id_lists_available(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["bench", "validate", "nope", "--root", str(tmp_path)]) == 2
    assert "unknown benchmark" in capsys.readouterr().err


# ---------------------------------------------------------------- no data loss
def test_interrupted_extraction_keeps_recorded_objects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_corpus(tmp_path, decision=ReviewDecision.INCLUDE)
    answers = iter(
        [
            "Ergonomic tooling reduces decision friction.",  # claim
            "10",  # study type -> other
            "",  # population
            "",  # intervention
            "",  # comparator
            "",  # outcome
            "",  # effect measure
            "",  # effect value
        ]
    )

    def fake_input(*_: object) -> str:
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt from None

    monkeypatch.setattr("builtins.input", fake_input)
    assert cli.main(["extract", "--root", str(tmp_path)]) == 0
    (obj,) = load_evidence(tmp_path / "evidence" / "objects.jsonl")
    assert obj.claim == "Ergonomic tooling reduces decision friction."


def test_interrupted_screening_exits_cleanly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_corpus(tmp_path)

    def fake_input(*_: object) -> NoReturn:
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", fake_input)
    assert cli.main(["screen", "next", "--root", str(tmp_path)]) == 0


# ---------------------------------------------------------------- corrections
def test_amend_corrects_a_decision_append_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    record = _seed_corpus(tmp_path, decision=ReviewDecision.INCLUDE)
    answers = iter(["2", "1", "misread the abstract"])  # exclude, first reason, note
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    rc = cli.main(
        [
            "screen",
            "amend",
            "--root",
            str(tmp_path),
            "--record",
            record.record_id[:10],
            "--reviewer",
            "tester",
        ]
    )
    assert rc == 0
    reviews = current_reviews(tmp_path / "screening" / "review_log.jsonl")
    assert reviews[record.record_id].decision is ReviewDecision.EXCLUDE
    # History is append-only: both the original decision and the correction remain.
    log_text = (tmp_path / "screening" / "review_log.jsonl").read_text(encoding="utf-8")
    assert len([line for line in log_text.splitlines() if line.strip()]) == 2


def test_amend_rejects_ambiguous_or_unknown_prefix(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _seed_corpus(tmp_path)
    assert cli.main(["screen", "amend", "--root", str(tmp_path), "--record", "ffffffff"]) == 2
    assert "no record starts with" in capsys.readouterr().err


def test_amend_requires_record_argument(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _seed_corpus(tmp_path)
    assert cli.main(["screen", "amend", "--root", str(tmp_path)]) == 2
    assert "--record" in capsys.readouterr().err


def test_help_lists_every_dispatchable_subcommand(capsys: pytest.CaptureFixture[str]) -> None:
    """`medscale --help` must not omit shipped commands (audit F-10: dataset
    and fhir were dispatchable but undocumented)."""
    from medscale.cli import _SUBCOMMANDS
    from medscale.cli import main as cli_main

    assert cli_main(["--help"]) == 0
    out = capsys.readouterr().out
    for command in _SUBCOMMANDS:
        assert f"  {command}" in out, f"--help must list the {command!r} command"


# ---------------------------------------------------------------- mesc-eval (B0)
def _base_args(tmp_path: Path) -> list[str]:
    return [
        "--input",
        str(tmp_path / "in.jsonl"),
        "--output",
        str(tmp_path / "out.json"),
        "--model-id",
        _B0_MODEL,
        "--model-revision",
        "rev-1",
        "--tokenizer-revision",
        "rev-1",
    ]


def test_mesc_eval_runs_with_injected_generator(tmp_path: Path) -> None:
    _write_b0_input(tmp_path / "in.jsonl")
    rc = mesc_eval.main(_base_args(tmp_path), generator_factory=_fake_b0_factory)
    assert rc == 0
    assert (tmp_path / "out.json").is_file()


def test_mesc_eval_requires_arguments(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert mesc_eval.main(["--output", str(tmp_path / "o.json")]) == 2
    assert "--input is required" in capsys.readouterr().err


def test_mesc_eval_missing_input_file_is_friendly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = mesc_eval.main(_base_args(tmp_path), generator_factory=_fake_b0_factory)
    assert rc == 2
    assert "input file not found" in capsys.readouterr().err


def test_mesc_eval_refuses_to_overwrite_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_b0_input(tmp_path / "in.jsonl")
    (tmp_path / "out.json").write_text("existing", encoding="utf-8")
    rc = mesc_eval.main(_base_args(tmp_path), generator_factory=_fake_b0_factory)
    assert rc == 2
    assert "output already exists" in capsys.readouterr().err


def test_mesc_eval_rejects_unapproved_model(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_b0_input(tmp_path / "in.jsonl")
    args = _base_args(tmp_path)
    args[args.index(_B0_MODEL)] = "Qwen/Qwen2.5-7B-Instruct"
    rc = mesc_eval.main(args, generator_factory=_fake_b0_factory)
    assert rc == 2
    assert "model_id must be one of" in capsys.readouterr().err


def test_mesc_eval_validates_before_constructing_runtime(tmp_path: Path) -> None:
    """A bad model id must fail before the generator factory is ever called."""
    _write_b0_input(tmp_path / "in.jsonl")
    called = {"n": 0}

    def _spy_factory(config: B0Config) -> _FakeB0Generator:
        called["n"] += 1
        return _FakeB0Generator()

    args = _base_args(tmp_path)
    args[args.index(_B0_MODEL)] = "Qwen/Qwen2.5-7B-Instruct"
    assert mesc_eval.main(args, generator_factory=_spy_factory) == 2
    assert called["n"] == 0


def test_mesc_eval_help_makes_no_training_or_clinical_claim() -> None:
    description = mesc_eval.DESCRIPTION.lower()
    assert "no training" in description
    assert "no retrieval" in description
    assert "no real split execution" in description
    assert "no clinical claim" in description
