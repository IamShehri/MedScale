"""Deterministic B1 evidence-cued baseline orchestration tests.

Fake injected generators only: no real model, dataset, inference, training,
network, retrieval, or P01-04 partition membership. Library versions are
injected. Evidence-layer failures must raise typed errors before the generator
is invoked and must never surface as model parse states.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from medscale.backends.transformers.backend import TransformersGenerateError
from medscale.mesc._b0 import B0Generator, parse_b0_output
from medscale.mesc._b1 import (
    B1_EVIDENCE_CONDITION,
    B1_EXPERIMENT_ID,
    B1_PROMPT_TEMPLATE_VERSION,
    B1Config,
    B1ConfigError,
    B1EvidenceJoinError,
    B1Report,
    B1RuntimeManifest,
    build_b1_prompt,
    capture_b1_runtime_manifest,
    join_b1_inputs,
    report_to_document,
    run_b1,
    write_b1_report,
)
from medscale.mesc._b1_evidence import (
    B1AnnotationComparison,
    B1EvidenceCue,
    B1EvidenceError,
    B1EvidencePack,
    B1SourceRecord,
    build_evidence_pack,
    build_final_cue_from_agreement,
    make_annotation_submission,
)
from medscale.mesc._pilot_loader import B0InputDataset, load_b0_inputs_from_records
from medscale.mesc._split_v1 import sha256_hexdigest
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult, ModelRef

_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
_SHA = "a" * 40
_SHA2 = "b" * 40
_COMMIT = "c" * 40
_SPLIT_FINGERPRINT = "43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91"
_SUBSET = "d" * 64

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


def _source_record(ordinal: int, *, context: list[str] | None = None) -> B1SourceRecord:
    return B1SourceRecord(
        example_id=f"e{ordinal}",
        source_document_id=f"pmid:{ordinal}",
        question=f"question {ordinal}?",
        context=tuple(context if context is not None else [f"ctx-{ordinal}"]),
    )


def _cue(record: B1SourceRecord, *, indices: list[int], status: str = "AVAILABLE") -> B1EvidenceCue:
    submission = make_annotation_submission(
        reviewer_id="r1",
        example_id=record.example_id,
        source_document_id=record.source_document_id,
        selected_segment_indices=indices,
        annotation_status=status,
    )
    comparison = B1AnnotationComparison(
        example_id=submission.example_id,
        source_document_id=submission.source_document_id,
        outcome="AGREED",
        submission_a=submission,
        submission_b=submission,
    )
    return build_final_cue_from_agreement(comparison, source_record=record)


def _pack(cues: list[B1EvidenceCue]) -> B1EvidencePack:
    return build_evidence_pack(
        cues,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
        subset_digest=_SUBSET,
    )


def _b0record(
    ordinal: int, decision: str, *, context: list[str] | None = None
) -> dict[str, object]:
    return {
        "example_id": f"e{ordinal}",
        "row_ordinal": ordinal,
        "source_document_id": f"pmid:{ordinal}",
        "dataset_id": "ds",
        "dataset_revision": "rev-1",
        "configuration": "cfg",
        "question": f"question {ordinal}?",
        "context": context if context is not None else [f"ctx-{ordinal}"],
        "decision": decision,
    }


def _dataset(records: list[dict[str, object]]) -> B0InputDataset:
    return load_b0_inputs_from_records(records)


def _config(pack: B1EvidencePack, **overrides: object) -> B1Config:
    base: dict[str, object] = {
        "experiment_version": "mesc-b1/1",
        "model_id": _MODEL,
        "model_revision": _SHA,
        "tokenizer_revision": _SHA,
        "max_new_tokens": 8,
        "seed": 0,
        "evidence_pack_sha256": pack.pack_sha256,
        "evidence_pack_size": pack.record_count,
        "subset_digest": pack.subset_digest,
    }
    base.update(overrides)
    return B1Config(**base)  # type: ignore[arg-type]


def _manifest(config: B1Config, *, code_commit: str = _COMMIT) -> B1RuntimeManifest:
    return capture_b1_runtime_manifest(
        code_commit=code_commit,
        config=config,
        device="cpu",
        dtype="float32",
        quantization="none",
        version_source=_versions,
    )


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
    config: B1Config,
    dataset: B0InputDataset,
    pack: B1EvidencePack,
    generator: B0Generator,
    *,
    code_commit: str = _COMMIT,
) -> B1Report:
    return run_b1(
        config, dataset, pack, generator, manifest=_manifest(config, code_commit=code_commit)
    )


def _scenario(
    ordinal: int = 0, decision: str = "yes"
) -> tuple[B1Config, B0InputDataset, B1EvidencePack]:
    record = _source_record(ordinal)
    cue = _cue(record, indices=[0])
    pack = _pack([cue])
    config = _config(pack)
    dataset = _dataset([_b0record(ordinal, decision)])
    return config, dataset, pack


# --------------------------------------------------------------- prompt
def test_b1_prompt_is_b0_input_plus_cue_block() -> None:
    record = _source_record(0)
    cue = _cue(record, indices=[0])
    prompt = build_b1_prompt(_dataset([_b0record(0, "yes")]).records[0], cue)
    assert "question 0?" in prompt
    assert "ctx-0" in prompt
    assert "Supplied evidence cue status: AVAILABLE" in prompt
    assert "Respond with exactly one word: yes, no, or maybe." in prompt
    assert prompt.endswith("Answer:")
    assert record.question in prompt


def test_b1_prompt_embeds_segments_verbatim() -> None:
    record = _source_record(0, context=["alpha segment", "beta segment", "gamma segment"])
    cue = _cue(record, indices=[0, 2])
    dataset = _dataset(
        [_b0record(0, "yes", context=["alpha segment", "beta segment", "gamma segment"])]
    )
    prompt = build_b1_prompt(dataset.records[0], cue)
    assert "alpha segment" in prompt
    assert "gamma segment" in prompt
    assert "beta segment" not in prompt.split("Supplied evidence segments:")[1]


def test_b1_prompt_insufficient_cue_has_no_segments() -> None:
    record = _source_record(0)
    cue = _cue(record, indices=[], status="INSUFFICIENT")
    prompt = build_b1_prompt(_dataset([_b0record(0, "yes")]).records[0], cue)
    assert "Supplied evidence cue status: INSUFFICIENT" in prompt
    assert "Supplied evidence segments:" not in prompt


def test_gold_decision_never_enters_the_prompt() -> None:
    first = _dataset([_b0record(0, "yes", context=["identical context"])])
    second = _dataset([_b0record(0, "no", context=["identical context"])])
    record = _source_record(0, context=["identical context"])
    cue = _cue(record, indices=[0])
    prompt_a = build_b1_prompt(first.records[0], cue)
    prompt_b = build_b1_prompt(second.records[0], cue)
    assert prompt_a == prompt_b


# --------------------------------------------------------------- join
def test_join_aligns_one_cue_per_input_example() -> None:
    source0 = _source_record(0)
    source1 = _source_record(1)
    cues = [_cue(source0, indices=[0]), _cue(source1, indices=[0])]
    pack = _pack(cues)
    dataset = _dataset([_b0record(0, "yes"), _b0record(1, "no")])
    joined = join_b1_inputs(dataset, pack.cues)
    assert [cue.example_id for cue in joined] == ["e0", "e1"]
    run_b1(_config(pack), dataset, pack, _FakeGenerator("yes"), manifest=_manifest(_config(pack)))


def test_join_missing_cue_fails_closed() -> None:
    source0 = _source_record(0)
    pack = _pack([_cue(source0, indices=[0])])
    dataset = _dataset([_b0record(0, "yes"), _b0record(1, "no")])
    with pytest.raises(B1EvidenceJoinError, match="missing evidence cue"):
        join_b1_inputs(dataset, pack.cues)


def test_join_extra_cue_fails_closed() -> None:
    source0 = _source_record(0)
    source1 = _source_record(1)
    pack = _pack([_cue(source0, indices=[0]), _cue(source1, indices=[0])])
    dataset = _dataset([_b0record(0, "yes")])
    with pytest.raises(B1EvidenceJoinError, match="not consumed"):
        join_b1_inputs(dataset, pack.cues)


def test_join_duplicate_cue_fails_closed() -> None:
    source0 = _source_record(0, context=["ctx-a", "ctx-b"])
    cues = [_cue(source0, indices=[0]), _cue(source0, indices=[1])]
    with pytest.raises(B1EvidenceJoinError, match="duplicate cue"):
        join_b1_inputs(_dataset([_b0record(0, "yes", context=["ctx-a", "ctx-b"])]), cues)


# --------------------------------------------------------------- run / determinism
def test_identical_runs_produce_identical_digest() -> None:
    config, dataset, pack = _scenario()
    first = _run(config, dataset, pack, _FakeGenerator("yes"))
    second = _run(config, dataset, pack, _FakeGenerator("yes"))
    assert first.run_digest == second.run_digest
    assert first.run_id == second.run_id


def test_digest_changes_with_pack_identity() -> None:
    config, dataset, pack = _scenario()
    a = _run(config, dataset, pack, _FakeGenerator("yes"))
    record = _source_record(0)
    other_pack = build_evidence_pack(
        [_cue(record, indices=[0])],
        source_split_fingerprint="f" * 64,
        subset_digest=_SUBSET,
    )
    assert other_pack.pack_sha256 != pack.pack_sha256
    b = _run(_config(other_pack), dataset, other_pack, _FakeGenerator("yes"))
    assert a.run_digest != b.run_digest


def test_digest_changes_with_cue_status() -> None:
    config, dataset, pack = _scenario()
    a = _run(config, dataset, pack, _FakeGenerator("yes"))
    record = _source_record(0)
    insufficient_pack = _pack([_cue(record, indices=[], status="INSUFFICIENT")])
    b = _run(_config(insufficient_pack), dataset, insufficient_pack, _FakeGenerator("yes"))
    assert a.run_digest != b.run_digest


def test_digest_changes_with_subset_digest() -> None:
    config, dataset, pack = _scenario()
    a = _run(config, dataset, pack, _FakeGenerator("yes"))
    record = _source_record(0)
    cue = _cue(record, indices=[0])
    other_pack = build_evidence_pack(
        [cue], source_split_fingerprint=_SPLIT_FINGERPRINT, subset_digest="e" * 64
    )
    b = _run(_config(other_pack), dataset, other_pack, _FakeGenerator("yes"))
    assert a.run_digest != b.run_digest


def test_digest_changes_with_code_commit() -> None:
    config, dataset, pack = _scenario()
    a = _run(config, dataset, pack, _FakeGenerator("yes"))
    b = _run(config, dataset, pack, _FakeGenerator("yes"), code_commit="f" * 40)
    assert a.run_digest != b.run_digest


def test_digest_changes_with_model_revision() -> None:
    config, dataset, pack = _scenario()
    a = _run(config, dataset, pack, _FakeGenerator("yes"))
    b = _run(_config(pack, model_revision=_SHA2), dataset, pack, _FakeGenerator("yes"))
    assert a.run_digest != b.run_digest


# --------------------------------------------------------------- config / manifest
def test_config_pins_b1_identity() -> None:
    config, _, pack = _scenario()
    assert config.experiment_id == B1_EXPERIMENT_ID
    assert config.prompt_template_version == B1_PROMPT_TEMPLATE_VERSION
    assert config.evidence_condition == B1_EVIDENCE_CONDITION
    assert config.evidence_pack_sha256 == pack.pack_sha256
    assert config.evidence_pack_size == pack.record_count
    assert config.subset_digest == pack.subset_digest


def test_manifest_config_mismatch_fails_closed() -> None:
    config, dataset, pack = _scenario()
    bad = replace(_manifest(config), evidence_pack_sha256="f" * 64)
    with pytest.raises(B1ConfigError, match="evidence_pack_sha256"):
        run_b1(config, dataset, pack, _FakeGenerator("yes"), manifest=bad)


def test_pack_config_mismatch_fails_closed() -> None:
    config, dataset, _ = _scenario()
    record = _source_record(0)
    other_pack = build_evidence_pack(
        [_cue(record, indices=[0])],
        source_split_fingerprint="f" * 64,
        subset_digest=_SUBSET,
    )
    with pytest.raises(B1ConfigError, match="pack SHA-256"):
        run_b1(config, dataset, other_pack, _FakeGenerator("yes"), manifest=_manifest(config))


def test_capture_manifest_requires_full_sha_code_commit() -> None:
    config, _, _ = _scenario()
    for bad in ("main", "abc123", "C" * 40, "", "c" * 39):
        with pytest.raises(B1ConfigError, match="code_commit"):
            capture_b1_runtime_manifest(
                code_commit=bad,
                config=config,
                device="cpu",
                dtype="float32",
                quantization="none",
                version_source=_versions,
            )


# --------------------------------------------------------------- fail-closed evidence
def test_evidence_failure_happens_before_generator_invocation() -> None:
    _, dataset, _ = _scenario()
    bad_record = _source_record(0, context=["TAMPERED context"])
    bad_pack = _pack([_cue(bad_record, indices=[0])])
    spy = _FakeGenerator("yes")
    with pytest.raises(B1EvidenceError):
        run_b1(_config(bad_pack), dataset, bad_pack, spy, manifest=_manifest(_config(bad_pack)))
    assert spy.requests == []


def test_evidence_failures_never_become_generation_failed() -> None:
    config, dataset, pack = _scenario()
    bad_record = _source_record(0, context=["TAMPERED context"])
    bad_pack = _pack([_cue(bad_record, indices=[0])])
    with pytest.raises(B1EvidenceError):
        _run(_config(bad_pack), dataset, bad_pack, _FakeGenerator("yes"))
    report = _run(config, dataset, pack, _FailingGenerator())
    assert report.aggregate.generation_failed_count == 1
    assert report.aggregate.correct_count == 0


# --------------------------------------------------------------- scoring
def test_scoring_marks_only_matching_parsed_predictions_correct() -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    assert report.aggregate.total == 1
    assert report.aggregate.parsed_count == 1
    assert report.aggregate.correct_count == 1


def test_ambiguous_and_unparseable_outputs_are_never_correct() -> None:
    config, dataset, pack = _scenario()
    ambiguous = _run(config, dataset, pack, _FakeGenerator("yes or no"))
    assert ambiguous.aggregate.ambiguous_count == 1
    assert ambiguous.aggregate.correct_count == 0
    unparseable = _run(config, dataset, pack, _FakeGenerator("banana"))
    assert unparseable.aggregate.unparseable_count == 1
    assert unparseable.aggregate.correct_count == 0


# --------------------------------------------------------------- report / artifacts
def test_report_binds_input_and_pack_identity() -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    assert report.input_sha256 == dataset.input_sha256
    assert report.input_size == dataset.input_size
    assert report.evidence_pack_sha256 == pack.pack_sha256
    assert report.evidence_pack_size == pack.record_count
    assert report.subset_digest == pack.subset_digest
    assert report.run_id == f"mesc-b1-run-{report.run_digest}"


def test_report_canonical_hash_matches_digest() -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    document = report_to_document(report)
    assert document["run_id"] == report.run_id
    assert sha256_hexdigest(document["canonical"]) == report.run_digest


def test_report_never_persists_raw_prompts() -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    serialized = str(report_to_document(report))
    assert "question 0?" not in serialized
    assert "ctx-0" not in serialized


def test_run_writes_no_artifact(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    config, dataset, pack = _scenario()
    _run(config, dataset, pack, _FakeGenerator("yes"))
    assert set(tmp_path.iterdir()) == before


def test_write_report_is_explicit_and_reproducible(tmp_path: Path) -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    path_a = tmp_path / "a.json"
    path_b = tmp_path / "b.json"
    write_b1_report(report, path_a)
    write_b1_report(report, path_b)
    assert path_a.read_bytes() == path_b.read_bytes()


def test_write_report_refuses_to_overwrite(tmp_path: Path) -> None:
    config, dataset, pack = _scenario()
    report = _run(config, dataset, pack, _FakeGenerator("yes"))
    out = tmp_path / "out.json"
    out.write_text("existing", encoding="utf-8")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        write_b1_report(report, out)
    assert out.read_text(encoding="utf-8") == "existing"


def test_parse_b0_output_reused_unchanged() -> None:
    assert parse_b0_output("yes") == ("yes", "parsed")
    assert parse_b0_output("yes and no") == (None, "ambiguous")
