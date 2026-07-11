"""The Core Library contract: the researcher script works verbatim, storage stays hidden."""

from __future__ import annotations

from pathlib import Path

from medscale import Benchmark, Corpus, Evidence, Workspace
from medscale.bench import GoldEvidenceSet, GoldOracle, TaskItem, TaskType, write_benchmark
from medscale.bench.spec import BenchmarkSpec
from medscale.evidence import StudyType, VerificationState
from medscale.evidence_checks import rule_verify_source
from medscale.evidence_store import write_evidence
from medscale.litdb import (
    EvidenceTier,
    Identifiers,
    LiteratureRecord,
    RawRetrieval,
    RunManifest,
    archive_retrieval,
    write_manifest,
)
from medscale.litdb.extract_cli import assemble_evidence
from medscale.litdb.review import ReviewDecision, append_events, make_event
from medscale.litdb.store import write_corpus
from medscale.provenance import Provenance, SourceAPI
from medscale.research.snapshot import capture_snapshot, write_snapshot

_TS = "2026-07-10T00:00:00+00:00"


def _seed(root: Path) -> tuple[str, str]:
    """Full substrate: record -> review -> verified evidence -> snapshot -> benchmark."""
    # archive a payload first so the provenance anchor check has real bytes to bind to
    retrieval = RawRetrieval(SourceAPI.OPENALEX, "q", _TS, payload="core-anchor")
    entry = archive_retrieval(root, "r1", "Q2", retrieval)
    write_manifest(root, RunManifest("r1", "abcdef1", (entry,)))
    anchor = retrieval.payload_sha256()
    record = LiteratureRecord(
        identifiers=Identifiers(doi="10.1/core"),
        title="An RCT of grammar-constrained decoding",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, "10.1/core", _TS, anchor),
        year=2026,
        tags=("Q2",),
    )
    write_corpus(root / "corpus" / "records.jsonl", [record])
    append_events(
        root / "screening" / "review_log.jsonl",
        (
            make_event(
                record.record_id,
                ReviewDecision.INCLUDE,
                reviewer="op",
                decided_at=_TS,
                software_version="0",
                git_sha="abcdef1",
            ),
        ),
    )
    obj = assemble_evidence(
        record,
        claim="Constrained decoding improves validity.",
        study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL,
        created_at=_TS,
    )
    verified, _ = rule_verify_source(obj, frozenset({record.record_id}), frozenset({anchor}))
    write_evidence(root / "evidence" / "objects.jsonl", [verified])
    snapshot = capture_snapshot(root, git_sha="abcdef1", software_version="0", created_at=_TS)
    write_snapshot(root, snapshot)
    spec = BenchmarkSpec(
        benchmark_id="core-bench",
        version="0.1",
        description="Core library test benchmark",
        scientific_objective="Prove the facade runs the engine",
        snapshot_id=snapshot.snapshot_id,
        task_types=(TaskType.EVIDENCE_RETRIEVAL,),
    )
    items = (
        TaskItem(
            task_id="retrieve",
            task_type=TaskType.EVIDENCE_RETRIEVAL,
            input_text="Does constrained decoding improve validity?",
            gold=GoldEvidenceSet(
                relevant_evidence_ids=(verified.evidence_id,), annotator="op", decided_at=_TS
            ),
        ),
    )
    write_benchmark(root, spec, items)
    return record.record_id, verified.evidence_id


def test_the_researcher_contract_verbatim(tmp_path: Path) -> None:
    """The exact usage pattern the library promises, end to end."""
    _seed(tmp_path)

    corpus = Corpus.load(tmp_path)
    evidence = corpus.evidence()
    results = evidence.query(study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL)
    snapshot = results.snapshot()
    benchmark = Benchmark.load(tmp_path, "core-bench")
    report = benchmark.run(GoldOracle())

    assert len(corpus) == 1
    assert len(results) == 1
    assert snapshot.snapshot_id  # citable identity
    assert report.aggregates["f1"] == 1.0
    assert report.results_id  # reproducible result identity


def test_workspace_is_the_single_handle(tmp_path: Path) -> None:
    record_id, evidence_id = _seed(tmp_path)
    workspace = Workspace.open(str(tmp_path))  # str or Path both accepted
    assert len(workspace.corpus) == 1
    assert len(workspace.evidence) == 1
    assert workspace.benchmarks() == ("core-bench",)
    assert workspace.integrity().is_clean
    stats = workspace.stats()
    assert stats["corpus"]["total_records"] == 1
    assert stats["evidence"]["total_objects"] == 1
    (obj,) = workspace.evidence.query(source_record_id=record_id)
    assert obj.evidence_id == evidence_id


def test_query_results_are_iterable_values(tmp_path: Path) -> None:
    _seed(tmp_path)
    corpus = Corpus.load(tmp_path)
    result = corpus.query(query_id="Q2")
    assert len(result) == 1
    assert [record.identifiers.doi for record in result] == ["10.1/core"]
    assert corpus.query(query_id="Q9").records == ()


def test_snapshot_capture_and_verify_roundtrip(tmp_path: Path) -> None:
    _seed(tmp_path)
    workspace = Workspace.open(tmp_path)
    snapshot = workspace.snapshot()
    assert workspace.verify(snapshot) == ()
    # drift the corpus -> verify names it
    corpus_file = tmp_path / "corpus" / "records.jsonl"
    corpus_file.write_text(corpus_file.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    fresh = Workspace.open(tmp_path)
    assert any(m.startswith("corpus:") for m in fresh.verify(snapshot))


def test_verification_engine_facade(tmp_path: Path) -> None:
    record_id, _ = _seed(tmp_path)
    workspace = Workspace.open(tmp_path)
    (existing,) = workspace.evidence.objects()
    record = workspace.index().by_record_id[record_id]
    fresh = assemble_evidence(
        record,
        claim="A second claim from the same trial.",
        study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL,
        created_at=_TS,
    )
    verified, checks = workspace.verification.verify(fresh)
    assert all(check.passed for check in checks)
    assert verified.verification is VerificationState.SOURCE_VERIFIED
    assert existing.verification is VerificationState.SOURCE_VERIFIED


def test_benchmark_validate_through_facade(tmp_path: Path) -> None:
    _seed(tmp_path)
    benchmark = Benchmark.load(tmp_path, "core-bench")
    assert benchmark.validate() == ()
    assert benchmark.spec.version == "0.1"
    assert len(benchmark.items) == 1


def test_evidence_load_direct(tmp_path: Path) -> None:
    _seed(tmp_path)
    evidence = Evidence.load(tmp_path)
    assert len(evidence) == 1
    assert isinstance(next(iter(evidence)).claim, str)


def test_empty_workspace_opens(tmp_path: Path) -> None:
    workspace = Workspace.open(tmp_path)
    assert len(workspace.corpus) == 0
    assert len(workspace.evidence) == 0
    assert workspace.benchmarks() == ()
    assert workspace.stats()["corpus"]["total_records"] == 0
