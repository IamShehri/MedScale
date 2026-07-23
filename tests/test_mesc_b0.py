"""Deterministic B0 orchestration tests using fake injected generators.

No real model, dataset, inference, training, or network is invoked; no P01-04
partition membership is required or produced. Library versions are injected.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.backends.transformers.backend import TransformersGenerateError
from medscale.mesc._b0 import (
    B0_EVIDENCE_CONDITION,
    PROMPT_TEMPLATE_VERSION,
    B0Config,
    B0ConfigError,
    B0Generator,
    B0Report,
    B0RuntimeManifest,
    build_b0_prompt,
    capture_runtime_manifest,
    parse_b0_output,
    report_to_document,
    run_b0,
    write_b0_report,
)
from medscale.mesc._pilot_loader import B0InputDataset, load_b0_inputs_from_records
from medscale.mesc._split_v1 import sha256_hexdigest
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult, ModelRef

_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
_SHA = "a" * 40
_SHA2 = "b" * 40
_COMMIT = "c" * 40

_VERSIONS = {
    "medscale": "0.2.0",
    "transformers": "5.13.1",
    "torch": "2.3.0",
    "tokenizers": "0.22.2",
    "huggingface-hub": "0.24.0",
    "safetensors": "0.4.0",
}


def _versions(package: str) -> str:
    return _VERSIONS[package]


def _b0config(**overrides: object) -> B0Config:
    base: dict[str, object] = {
        "experiment_version": "mesc-b0/1",
        "model_id": _MODEL,
        "model_revision": _SHA,
        "tokenizer_revision": _SHA,
        "max_new_tokens": 8,
        "seed": 0,
    }
    base.update(overrides)
    return B0Config(**base)  # type: ignore[arg-type]


def _manifest(
    config: B0Config,
    *,
    code_commit: str = _COMMIT,
    version_source: object = None,
) -> B0RuntimeManifest:
    source = version_source if version_source is not None else _versions
    return capture_runtime_manifest(
        code_commit=code_commit,
        config=config,
        device="cpu",
        dtype="float32",
        quantization="none",
        version_source=source,  # type: ignore[arg-type]
    )


def _raw_manifest(**overrides: object) -> B0RuntimeManifest:
    base: dict[str, object] = {
        "code_commit": _COMMIT,
        "python_version": "3.11.0",
        "medscale_version": "0",
        "transformers_version": "0",
        "torch_version": "0",
        "tokenizers_version": "0",
        "huggingface_hub_version": "0",
        "safetensors_version": "0",
        "model_revision": _SHA,
        "tokenizer_revision": _SHA,
        "device": "cpu",
        "dtype": "float32",
        "quantization": "none",
        "seed": 0,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
        "evidence_condition": B0_EVIDENCE_CONDITION,
    }
    base.update(overrides)
    return B0RuntimeManifest(**base)  # type: ignore[arg-type]


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
    def __init__(self, response: str = "yes") -> None:
        self.requests: list[GenerationRequest] = []
        self._response = response

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.requests.append(request)
        return GenerationResult(
            text=self._response,
            model=ModelRef(model_id=_MODEL, revision=_SHA, backend="transformers"),
        )


class _FailingGenerator:
    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise TransformersGenerateError("injected failure")


def _run(
    config: B0Config,
    dataset: B0InputDataset,
    generator: B0Generator,
    *,
    code_commit: str = _COMMIT,
    version_source: object = None,
) -> B0Report:
    manifest = _manifest(config, code_commit=code_commit, version_source=version_source)
    return run_b0(config, dataset, generator, manifest=manifest)


# --------------------------------------------------------------- parsing
def test_parse_recognizes_exactly_one_decision() -> None:
    assert parse_b0_output("The answer is yes.") == ("yes", "parsed")
    assert parse_b0_output("no") == ("no", "parsed")
    assert parse_b0_output("Maybe.") == ("maybe", "parsed")


def test_parse_rejects_ambiguous_and_unparseable() -> None:
    assert parse_b0_output("yes and no") == (None, "ambiguous")
    assert parse_b0_output("banana") == (None, "unparseable")
    assert parse_b0_output("none of these apply") == (None, "unparseable")


# --------------------------------------------------------------- determinism
def test_identical_inputs_produce_identical_digest() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    first = _run(_b0config(), dataset, _FakeGenerator("yes"))
    second = _run(_b0config(), dataset, _FakeGenerator("yes"))
    assert first.run_digest == second.run_digest
    assert first.run_id == second.run_id


def test_input_reordering_cannot_change_results() -> None:
    forward = _run(
        _b0config(), _dataset([_record(0, "yes"), _record(1, "no")]), _FakeGenerator("yes")
    )
    reverse = _run(
        _b0config(), _dataset([_record(1, "no"), _record(0, "yes")]), _FakeGenerator("yes")
    )
    assert forward.run_digest == reverse.run_digest


# --------------------------------------------------------------- manifest / reproducibility
def test_capture_runtime_manifest_uses_injected_versions() -> None:
    manifest = _manifest(_b0config())
    assert manifest.transformers_version == "5.13.1"
    assert manifest.torch_version == "2.3.0"
    assert manifest.code_commit == _COMMIT
    assert manifest.model_revision == _SHA


def test_capture_requires_full_sha_code_commit() -> None:
    for bad in ("main", "abc123", "C" * 40, "", "c" * 39):
        with pytest.raises(B0ConfigError, match="code_commit"):
            _manifest(_b0config(), code_commit=bad)


def test_digest_changes_with_model_revision() -> None:
    ds = _dataset([_record(0, "yes")])
    a = _run(_b0config(model_revision=_SHA), ds, _FakeGenerator("yes"))
    b = _run(_b0config(model_revision=_SHA2), ds, _FakeGenerator("yes"))
    assert a.run_digest != b.run_digest


def test_digest_changes_with_code_commit() -> None:
    ds = _dataset([_record(0, "yes")])
    a = _run(_b0config(), ds, _FakeGenerator("yes"), code_commit=_COMMIT)
    b = _run(_b0config(), ds, _FakeGenerator("yes"), code_commit="d" * 40)
    assert a.run_digest != b.run_digest


def test_digest_changes_with_dependency_version() -> None:
    ds = _dataset([_record(0, "yes")])
    a = _run(_b0config(), ds, _FakeGenerator("yes"))

    def bumped(package: str) -> str:
        return "9.9.9" if package == "torch" else _versions(package)

    b = _run(_b0config(), ds, _FakeGenerator("yes"), version_source=bumped)
    assert a.run_digest != b.run_digest


def test_manifest_config_mismatch_fails_closed() -> None:
    ds = _dataset([_record(0, "yes")])
    with pytest.raises(B0ConfigError, match="model_revision"):
        run_b0(
            _b0config(model_revision=_SHA),
            ds,
            _FakeGenerator("yes"),
            manifest=_raw_manifest(model_revision=_SHA2),
        )


# --------------------------------------------------------------- gold isolation
def test_gold_decision_never_enters_the_prompt() -> None:
    records = [
        _record(0, "yes", question="identical question"),
        _record(1, "no", question="identical question"),
    ]
    records[0]["context"] = ["identical context"]
    records[1]["context"] = ["identical context"]
    spy = _FakeGenerator("maybe")
    _run(_b0config(), _dataset(records), spy)
    assert spy.requests[0].prompt == spy.requests[1].prompt


def test_prompt_uses_only_question_and_context() -> None:
    dataset = _dataset([_record(0, "yes", question="does X help?")])
    prompt = build_b0_prompt(dataset.records[0])
    assert "does X help?" in prompt
    assert "ctx" in prompt


# --------------------------------------------------------------- scoring
def test_scoring_marks_only_matching_parsed_predictions_correct() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    report = _run(_b0config(), dataset, _FakeGenerator("yes"))
    assert report.aggregate.total == 2
    assert report.aggregate.parsed_count == 2
    assert report.aggregate.correct_count == 1
    assert report.config.evidence_condition == B0_EVIDENCE_CONDITION


def test_unsupported_model_fails_before_generator_invocation() -> None:
    spy = _FakeGenerator()
    with pytest.raises(B0ConfigError, match="model_id must be one of"):
        _run(_b0config(model_id="Qwen/Qwen2.5-7B-Instruct"), _dataset([_record(0, "yes")]), spy)
    assert spy.requests == []


def test_generation_failure_is_deterministic_and_never_correct() -> None:
    dataset = _dataset([_record(0, "yes"), _record(1, "no")])
    report = _run(_b0config(), dataset, _FailingGenerator())
    assert report.aggregate.generation_failed_count == 2
    assert report.aggregate.correct_count == 0
    assert all(p.parse_state == "generation_failed" for p in report.predictions)
    assert all(p.predicted_decision is None for p in report.predictions)


def test_ambiguous_and_unparseable_outputs_are_never_correct() -> None:
    dataset = _dataset([_record(0, "yes")])
    ambiguous = _run(_b0config(), dataset, _FakeGenerator("yes or no"))
    assert ambiguous.aggregate.ambiguous_count == 1
    assert ambiguous.aggregate.correct_count == 0
    unparseable = _run(_b0config(), dataset, _FakeGenerator("banana"))
    assert unparseable.aggregate.unparseable_count == 1
    assert unparseable.aggregate.correct_count == 0


# --------------------------------------------------------------- artifacts / atomic write
def test_run_writes_no_artifact(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    _run(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    assert set(tmp_path.iterdir()) == before


def test_write_report_is_explicit_and_reproducible(tmp_path: Path) -> None:
    report = _run(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    path_a = tmp_path / "a.json"
    path_b = tmp_path / "b.json"
    write_b0_report(report, path_a)
    write_b0_report(report, path_b)
    assert path_a.read_bytes() == path_b.read_bytes()
    document = report_to_document(report)
    assert document["run_id"] == report.run_id
    assert sha256_hexdigest(document["canonical"]) == report.run_digest


def test_write_report_refuses_to_overwrite(tmp_path: Path) -> None:
    report = _run(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    out = tmp_path / "out.json"
    out.write_text("existing", encoding="utf-8")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        write_b0_report(report, out)
    assert out.read_text(encoding="utf-8") == "existing"


def test_write_report_cleans_up_on_rename_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _run(_b0config(), _dataset([_record(0, "yes")]), _FakeGenerator("yes"))
    out = tmp_path / "out.json"

    def boom(self: Path, target: object) -> None:
        raise OSError("simulated rename failure")

    monkeypatch.setattr(Path, "replace", boom)
    with pytest.raises(OSError, match="simulated rename failure"):
        write_b0_report(report, out)
    assert not out.exists()
    assert not (tmp_path / "out.json.partial").exists()
