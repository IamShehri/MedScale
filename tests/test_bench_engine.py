"""Benchmark engine: the directive's test matrix — deterministic scoring, corrupted
benchmarks, missing evidence, snapshot mismatch, version compatibility."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale import cli
from medscale.bench import (
    BenchmarkSpec,
    EmptySystem,
    GoldEvidenceSet,
    GoldOracle,
    Statement,
    TaskItem,
    TaskOutput,
    TaskType,
    load_benchmark,
    run_benchmark,
    score_item,
    validate_benchmark,
    write_benchmark,
)
from medscale.bench.scorers import set_precision, set_recall
from medscale.evidence import StudyType, VerificationState
from medscale.evidence_checks import rule_verify_source
from medscale.evidence_store import write_evidence
from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.extract_cli import assemble_evidence
from medscale.litdb.store import write_corpus
from medscale.provenance import Provenance, SourceAPI
from medscale.research.snapshot import capture_snapshot, write_snapshot

_TS = "2026-07-10T00:00:00+00:00"


def _seed_substrate(root: Path) -> tuple[str, str, str]:
    """Corpus + two verified evidence objects + snapshot. Returns (eo1, eo2, snapshot_id)."""
    record = LiteratureRecord(
        identifiers=Identifiers(doi="10.1/src"),
        title="An RCT of constrained decoding",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, "10.1/src", _TS, "d" * 64),
        year=2026,
    )
    write_corpus(root / "corpus" / "records.jsonl", [record])
    corpus_ids = frozenset({record.record_id})
    hashes = frozenset({"d" * 64})
    objects = []
    for claim in ("Constrained decoding improves validity.", "Adapters add content quality."):
        obj = assemble_evidence(
            record, claim=claim, study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL, created_at=_TS
        )
        verified, _ = rule_verify_source(obj, corpus_ids, hashes)
        assert verified.verification is VerificationState.SOURCE_VERIFIED
        objects.append(verified)
    write_evidence(root / "evidence" / "objects.jsonl", objects)
    snapshot = capture_snapshot(root, git_sha="abcdef1", software_version="0.0.0", created_at=_TS)
    write_snapshot(root, snapshot)
    return objects[0].evidence_id, objects[1].evidence_id, snapshot.snapshot_id


def _benchmark(root: Path) -> tuple[str, str, str]:
    eo1, eo2, snapshot_id = _seed_substrate(root)
    spec = BenchmarkSpec(
        benchmark_id="evidence-bench",
        version="0.1",
        description="Test benchmark",
        scientific_objective="Verify evidence grounding is scorable",
        snapshot_id=snapshot_id,
        task_types=(
            TaskType.EVIDENCE_RETRIEVAL,
            TaskType.EVIDENCE_GROUNDING,
            TaskType.EVIDENCE_SUMMARIZATION,
        ),
    )
    items = (
        TaskItem(
            task_id="retrieve-validity",
            task_type=TaskType.EVIDENCE_RETRIEVAL,
            input_text="Does constrained decoding improve validity?",
            gold=GoldEvidenceSet(relevant_evidence_ids=(eo1,), annotator="op", decided_at=_TS),
        ),
        TaskItem(
            task_id="ground-claim",
            task_type=TaskType.EVIDENCE_GROUNDING,
            input_text="Constrained decoding improves validity.",
            gold=GoldEvidenceSet(
                supporting_evidence_ids=(eo1,),
                contradicting_evidence_ids=(eo2,),
                annotator="op",
                decided_at=_TS,
            ),
        ),
        TaskItem(
            task_id="summarize-set",
            task_type=TaskType.EVIDENCE_SUMMARIZATION,
            input_text="Summarize the evidence.",
            input_evidence_ids=(eo1, eo2),
            gold=GoldEvidenceSet(relevant_evidence_ids=(eo1, eo2), annotator="op", decided_at=_TS),
        ),
    )
    write_benchmark(root, spec, items)
    return eo1, eo2, snapshot_id


# ------------------------------------------------------------- deterministic scoring
def test_set_metric_conventions() -> None:
    assert set_precision(frozenset(), frozenset()) == 1.0
    assert set_precision(frozenset(), frozenset({"g"})) == 0.0
    assert set_precision(frozenset({"a", "b"}), frozenset({"a"})) == 0.5
    assert set_recall(frozenset({"a"}), frozenset({"a", "b"})) == 0.5
    assert set_recall(frozenset({"x"}), frozenset()) == 0.0


def test_score_item_retrieval_and_provenance(tmp_path: Path) -> None:
    eo1, eo2, _ = _benchmark(tmp_path)
    _, items = load_benchmark(tmp_path, "evidence-bench")
    retrieval = next(i for i in items if i.task_type is TaskType.EVIDENCE_RETRIEVAL)
    known = frozenset({eo1, eo2})
    perfect = score_item(retrieval, TaskOutput(retrieved_ids=(eo1,)), known)
    assert perfect["precision"] == 1.0 and perfect["recall"] == 1.0 and perfect["f1"] == 1.0
    noisy = score_item(retrieval, TaskOutput(retrieved_ids=(eo1, "0" * 64)), known)
    assert noisy["precision"] == 0.5 and noisy["recall"] == 1.0
    assert noisy["provenance_completeness"] == 0.5  # one cited id doesn't exist


def test_score_summarization_unsupported_detection(tmp_path: Path) -> None:
    eo1, eo2, _ = _benchmark(tmp_path)
    _, items = load_benchmark(tmp_path, "evidence-bench")
    summarize = next(i for i in items if i.task_type is TaskType.EVIDENCE_SUMMARIZATION)
    output = TaskOutput(
        statements=(
            Statement("finding one", (eo1,)),
            Statement("uncited assertion", ()),  # unsupported
        )
    )
    metrics = score_item(summarize, output, frozenset({eo1, eo2}))
    assert metrics["factual_completeness"] == 0.5  # covered eo1 of {eo1, eo2}
    assert metrics["unsupported_statement_rate"] == 0.5


def test_scoring_is_deterministic(tmp_path: Path) -> None:
    eo1, eo2, _ = _benchmark(tmp_path)
    _, items = load_benchmark(tmp_path, "evidence-bench")
    grounding = next(i for i in items if i.task_type is TaskType.EVIDENCE_GROUNDING)
    output = TaskOutput(supporting_ids=(eo2, eo1))  # unsorted input
    a = score_item(grounding, output, frozenset({eo1, eo2}))
    b = score_item(grounding, TaskOutput(supporting_ids=(eo1, eo2)), frozenset({eo1, eo2}))
    assert a == b


# ------------------------------------------------------------------ gold constraints
def test_gold_requires_annotator_and_rejects_contradiction_overlap() -> None:
    with pytest.raises(ValueError, match="annotator"):
        GoldEvidenceSet(relevant_evidence_ids=("x",), annotator=" ", decided_at=_TS)
    with pytest.raises(ValueError, match="both support and contradict"):
        GoldEvidenceSet(
            supporting_evidence_ids=("x",),
            contradicting_evidence_ids=("x",),
            annotator="op",
            decided_at=_TS,
        )


def test_reserved_task_type_rejected() -> None:
    with pytest.raises(ValueError, match="reserved extension point"):
        TaskItem(
            task_id="future",
            task_type=TaskType.CLINICAL_REASONING,
            input_text="reason",
            gold=GoldEvidenceSet(relevant_evidence_ids=("x",), annotator="op", decided_at=_TS),
        )


# --------------------------------------------------------------------- validation
def test_validate_clean_benchmark(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    spec, items = load_benchmark(tmp_path, "evidence-bench")
    assert validate_benchmark(tmp_path, spec, items) == ()


def test_validate_missing_evidence(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    spec, items = load_benchmark(tmp_path, "evidence-bench")
    ghost_gold = GoldEvidenceSet(relevant_evidence_ids=("0" * 64,), annotator="op", decided_at=_TS)
    bad_item = TaskItem(
        task_id="ghost",
        task_type=TaskType.EVIDENCE_RETRIEVAL,
        input_text="?",
        gold=ghost_gold,
    )
    issues = validate_benchmark(tmp_path, spec, (*items, bad_item))
    assert any("not in store" in issue for issue in issues)


def test_validate_snapshot_mismatch_blocks(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    corpus = tmp_path / "corpus" / "records.jsonl"
    corpus.write_text(corpus.read_text(encoding="utf-8") + "\n", encoding="utf-8")  # drift
    spec, items = load_benchmark(tmp_path, "evidence-bench")
    issues = validate_benchmark(tmp_path, spec, items)
    assert any("snapshot drift" in issue for issue in issues)
    with pytest.raises(ValueError, match="not scientifically runnable"):
        run_benchmark(
            tmp_path,
            "evidence-bench",
            GoldOracle(),
            started_at=_TS,
            software_version="0.0.0",
            git_sha="abcdef1",
        )


def test_validate_verification_floor(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    spec, items = load_benchmark(tmp_path, "evidence-bench")
    strict = BenchmarkSpec(
        benchmark_id=spec.benchmark_id,
        version=spec.version,
        description=spec.description,
        scientific_objective=spec.scientific_objective,
        snapshot_id=spec.snapshot_id,
        min_verification=VerificationState.EXTRACTION_VERIFIED,  # above SOURCE_VERIFIED
        task_types=spec.task_types,
    )
    issues = validate_benchmark(tmp_path, strict, items)
    assert any("below required extraction_verified" in issue for issue in issues)


# --------------------------------------------------------- corrupted / compatibility
def test_corrupted_spec_fails_closed(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    spec_path = tmp_path / "benchmarks" / "evidence-bench" / "spec.json"
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    data["scientific_objective"] = "quietly edited"
    spec_path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match recomputed identity"):
        load_benchmark(tmp_path, "evidence-bench")


def test_format_less_spec_still_loads(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    spec_path = tmp_path / "benchmarks" / "evidence-bench" / "spec.json"
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    del data["format"]
    del data["spec_id"]  # legacy file without identity or marker
    spec_path.write_text(json.dumps(data), encoding="utf-8")
    spec, _ = load_benchmark(tmp_path, "evidence-bench")
    assert spec.benchmark_id == "evidence-bench"


# --------------------------------------------------------------------------- runner
def test_gold_oracle_scores_ceiling_and_artifact_reproducible(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    first, path = run_benchmark(
        tmp_path,
        "evidence-bench",
        GoldOracle(),
        started_at=_TS,
        software_version="0.0.0",
        git_sha="abcdef1",
    )
    accuracy_metrics = {
        name: value
        for name, value in first.aggregates.items()
        if name != "unsupported_statement_rate"
    }
    assert all(value == 1.0 for value in accuracy_metrics.values()), first.aggregates
    assert first.aggregates["unsupported_statement_rate"] == 0.0
    # reproducibility: rerun at a different time -> same results_id
    second, _ = run_benchmark(
        tmp_path,
        "evidence-bench",
        GoldOracle(),
        started_at="2035-01-01T00:00:00+00:00",
        software_version="9.9.9",
        git_sha="1234567",
    )
    assert second.results_id == first.results_id
    stored = json.loads(path.read_text(encoding="utf-8"))
    assert stored["results_id"] == first.results_id


def test_empty_system_floor(tmp_path: Path) -> None:
    _benchmark(tmp_path)
    artifact, _ = run_benchmark(
        tmp_path,
        "evidence-bench",
        EmptySystem(),
        started_at=_TS,
        software_version="0.0.0",
        git_sha="abcdef1",
    )
    assert artifact.aggregates["recall"] == 0.0
    assert artifact.aggregates["factual_completeness"] == 0.0
    assert artifact.aggregates["provenance_completeness"] == 1.0  # cited nothing false


# ------------------------------------------------------------------------------ CLI
def test_cli_list_validate_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _benchmark(tmp_path)
    assert cli.main(["bench", "list", "--root", str(tmp_path)]) == 0
    assert "evidence-bench" in capsys.readouterr().out
    assert cli.main(["bench", "validate", "evidence-bench", "--root", str(tmp_path)]) == 0
    assert "VALID" in capsys.readouterr().out
    assert cli.main(["bench", "run", "evidence-bench", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "results_id" in out
    # drift the tree -> validate fails with non-zero exit
    corpus = tmp_path / "corpus" / "records.jsonl"
    corpus.write_text(corpus.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert cli.main(["bench", "validate", "evidence-bench", "--root", str(tmp_path)]) == 1
