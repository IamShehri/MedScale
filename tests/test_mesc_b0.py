"""Deterministic B0 orchestration tests using fake injected generators.

No real model, dataset, inference, training, or network is invoked; no P01-04
partition membership is required or produced.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.backends.transformers.backend import TransformersGenerateError
from medscale.mesc._b0 import (
    B0_EVIDENCE_CONDITION,
    B0Config,
    B0ConfigError,
    B0Environment,
    build_b0_prompt,
    parse_b0_output,
    report_to_document,
    run_b0,
    write_b0_report,
)
from medscale.mesc._pilot_loader import B0InputDataset, load_b0_inputs_from_records
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult, ModelRef

_MODEL = "meta-llama/Llama-3.2-3B-Instruct"


def _b0config(**overrides: object) -> B0Config:
    base: dict[str, object] = {
        "experiment_version": "mesc-b0/1",
        "model_id": _MODEL,
        "model_revision": "rev-1",
        "tokenizer_revision": "rev-1",
        "max_new_tokens": 8,
        "seed": 0,
    }
    base.update(overrides)
    return B0Config(**base)  # type: ignore[arg-type]


def _record(ordinal: int, decision: str, *, question: str | None = None) -> dict[str, object]:
    return {
        "example_id": f"e{ordinal}",
        "row_ordinal": ordinal,
        "source_document_id": f"pmid:{ordinal}",
        "dataset_id": "ds",
        "dataset_revision": "rev-1",
        "configuration": "cfg",
        "question": question if question is not None else f"question {ordinal}?",
        "context": ["ctx"],
        "decision": decision,
    }


def _dataset(records: list[dict[str, object]]) -> B0InputDataset:
    return load_b0_inputs_from_records(records)


class _FakeGenerator:
    """Deterministic generator that records the requests it received."""

    def __init__(self, response: str = "yes") -> None:
        self.requests: list[GenerationRequest] = []
        self._response = response

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.requests.append(request)
        return GenerationResult(
            text=self._response,
            model=ModelRef(model_id=_MODEL, revision="rev-1", backend="transformers"),
        )


class _FailingGenerator:
    def __init__(self) -> None:
        self.requests: list[GenerationRequest] = []

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.requests.append(request)
        raise TransformersGenerateError("injected failure")


# --------------------------------------------------------------- parsing
def test_parse_recognizes_exactly_one_decision() -> None:
    assert parse_b0_output("The answer is yes.") == ("yes", "parsed")
    assert parse_b0_output("no") == ("no", "parsed")
    assert parse_b0_output("Maybe.") == ("maybe", "parsed")


def test_parse_rejects_ambiguous_and_unparseable() -> None:
    assert parse_b0_output("yes and no") == (None, "ambiguous")
    assert parse_b0_output("banana") == (None, "unparseable")
    # substring safety: "none" must not be read as "no".
    assert parse_b0_output("none of these apply") == (None, "unparseable")


# --------------------------------------------------------------- determinism
def test_identical_inputs_produce_identical_digest() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    first = run_b0(_b0config(), dataset, _FakeGenerator("yes"))
    second = run_b0(_b0config(), dataset, _FakeGenerator("yes"))
    assert first.run_digest == second.run_digest
    assert first.run_id == second.run_id


def test_digest_excludes_environment() -> None:
    dataset = _dataset([_record(0, "yes")])
    a = run_b0(
        _b0config(), dataset, _FakeGenerator("yes"), environment=B0Environment("3.11.0", "CPython")
    )
    b = run_b0(
        _b0config(),
        dataset,
        _FakeGenerator("yes"),
        environment=B0Environment("9.9.9", "OtherPy", code_commit="deadbeef"),
    )
    assert a.run_digest == b.run_digest


def test_input_reordering_cannot_change_results() -> None:
    forward = run_b0(
        _b0config(), _dataset([_record(0, "yes"), _record(1, "no")]), _FakeGenerator("yes")
    )
    reverse = run_b0(
        _b0config(), _dataset([_record(1, "no"), _record(0, "yes")]), _FakeGenerator("yes")
    )
    assert forward.run_digest == reverse.run_digest


# --------------------------------------------------------------- no gold leakage
def test_gold_decision_never_enters_the_prompt() -> None:
    records = [
        _record(0, "yes", question="identical question"),
        _record(1, "no", question="identical question"),
    ]
    records[0]["context"] = ["identical context"]
    records[1]["context"] = ["identical context"]
    spy = _FakeGenerator("maybe")
    run_b0(_b0config(), _dataset(records), spy)
    # Same question/context, different gold -> identical prompt: the gold cannot leak.
    assert spy.requests[0].prompt == spy.requests[1].prompt


def test_prompt_uses_only_question_and_context() -> None:
    dataset = _dataset([_record(0, "yes", question="does X help?")])
    prompt = build_b0_prompt(dataset.records[0])
    assert "does X help?" in prompt
    assert "ctx" in prompt


# --------------------------------------------------------------- scoring
def test_scoring_marks_only_matching_parsed_predictions_correct() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    report = run_b0(_b0config(), dataset, _FakeGenerator("yes"))
    assert report.aggregate.total == 2
    assert report.aggregate.parsed_count == 2
    assert report.aggregate.correct_count == 1  # only the gold "yes" matches
    assert report.config.evidence_condition == B0_EVIDENCE_CONDITION


def test_unsupported_model_fails_before_generator_invocation() -> None:
    spy = _FakeGenerator()
    with pytest.raises(B0ConfigError, match="model_id must be one of"):
        run_b0(_b0config(model_id="Qwen/Qwen2.5-7B-Instruct"), _dataset([_record(0, "yes")]), spy)
    assert spy.requests == []


def test_generation_failure_is_deterministic_and_never_correct() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    report = run_b0(_b0config(), dataset, _FailingGenerator())
    assert report.aggregate.generation_failed_count == 2
    assert report.aggregate.correct_count == 0
    assert all(p.parse_state == "generation_failed" for p in report.predictions)
    assert all(p.predicted_decision is None for p in report.predictions)
    assert all(not s.correct for s in report.scores)


def test_ambiguous_and_unparseable_outputs_are_never_correct() -> None:
    dataset = _dataset([_record(0, "yes")])
    ambiguous = run_b0(_b0config(), dataset, _FakeGenerator("yes or no"))
    assert ambiguous.aggregate.ambiguous_count == 1
    assert ambiguous.aggregate.correct_count == 0
    unparseable = run_b0(_b0config(), dataset, _FakeGenerator("banana"))
    assert unparseable.aggregate.unparseable_count == 1
    assert unparseable.aggregate.correct_count == 0


# --------------------------------------------------------------- artifacts
def test_run_writes_no_artifact(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    run_b0(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    assert set(tmp_path.iterdir()) == before


def test_write_report_is_explicit_and_reproducible(tmp_path: Path) -> None:
    report = run_b0(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    path_a = tmp_path / "a.json"
    path_b = tmp_path / "b.json"
    write_b0_report(report, path_a)
    write_b0_report(report, path_b)
    assert path_a.read_bytes() == path_b.read_bytes()
    document = report_to_document(report)
    assert document["run_id"] == report.run_id
    assert document["run_digest"] == report.run_digest


def test_document_canonical_matches_run_digest() -> None:
    from medscale.mesc._split_v1 import sha256_hexdigest

    report = run_b0(
        _b0config(), _dataset([_record(0, "yes"), _record(1, "maybe")]), _FakeGenerator("no")
    )
    document = report_to_document(report)
    assert sha256_hexdigest(document["canonical"]) == report.run_digest
