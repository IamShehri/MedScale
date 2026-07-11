"""Research Intelligence layer: queries, stats, snapshots — the directive's test matrix.

Covers: deterministic results, empty-corpus behavior, corrupted artifacts (fail
closed), backward compatibility (format-less lines), and reproducibility (same tree ->
same bytes; tamper -> named mismatch)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale import cli
from medscale.evidence import StudyType, VerificationState
from medscale.evidence_store import write_evidence
from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.extract_cli import assemble_evidence
from medscale.litdb.review import ReviewDecision, append_events, make_event
from medscale.litdb.store import write_corpus
from medscale.provenance import Provenance, SourceAPI
from medscale.reproducibility import canonical_json
from medscale.research import (
    ResearchIndex,
    capture_snapshot,
    corpus_stats,
    evidence_stats,
    evidence_where,
    load_snapshot,
    records_where,
    screening_stats,
    verify_snapshot,
    write_snapshot,
)

_TS = "2026-07-10T00:00:00+00:00"


def _record(
    doi: str,
    *,
    title: str = "Grammar constrained decoding for FHIR",
    year: int = 2025,
    tags: tuple[str, ...] = ("Q2",),
    api: SourceAPI = SourceAPI.OPENALEX,
    tier: EvidenceTier = EvidenceTier.PEER_REVIEWED,
) -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title=title,
        evidence_tier=tier,
        provenance=Provenance(api, doi, _TS, "c" * 64),
        year=year,
        venue="J Med AI",
        abstract="Constrained decoding and validators.",
        tags=tags,
    )


def _seed(root: Path) -> tuple[LiteratureRecord, LiteratureRecord]:
    fhir = _record("10.1/fhir", tags=("Q2",))
    bench = _record(
        "10.1/bench",
        title="A medical benchmark study",
        year=2024,
        tags=("Q6",),
        api=SourceAPI.PUBMED,
        tier=EvidenceTier.PREPRINT,
    )
    write_corpus(root / "corpus" / "records.jsonl", [fhir, bench])
    append_events(
        root / "screening" / "review_log.jsonl",
        (
            make_event(
                fhir.record_id,
                ReviewDecision.INCLUDE,
                reviewer="op",
                decided_at=_TS,
                software_version="0",
                git_sha="abcdef1",
            ),
        ),
    )
    obj = assemble_evidence(
        fhir,
        claim="Grammar guarantees structural validity.",
        study_type=StudyType.RANDOMIZED_CONTROLLED_TRIAL,
        created_at=_TS,
        intervention="grammar-constrained decoding",
        outcome="validity",
    )
    write_evidence(root / "evidence" / "objects.jsonl", [obj])
    return fhir, bench


# --------------------------------------------------------------------- query engine
def test_records_where_filters_conjunctively(tmp_path: Path) -> None:
    fhir, bench = _seed(tmp_path)
    index = ResearchIndex.load(tmp_path)
    assert records_where(index, query_id="Q2") == (fhir,)
    assert records_where(index, domain="medical-benchmark") == (bench,)
    assert records_where(index, rq="RQ1") == (fhir,)  # Q2 bears on RQ1
    assert records_where(index, source=SourceAPI.PUBMED) == (bench,)
    assert records_where(index, tier=EvidenceTier.PREPRINT) == (bench,)
    assert records_where(index, year_min=2025) == (fhir,)
    assert records_where(index, decision=ReviewDecision.INCLUDE) == (fhir,)
    assert records_where(index, decision=ReviewDecision.PENDING) == (bench,)
    assert records_where(index, text="benchmark") == (bench,)
    assert records_where(index, query_id="Q2", source=SourceAPI.PUBMED) == ()


def test_evidence_where_filters(tmp_path: Path) -> None:
    _seed(tmp_path)
    index = ResearchIndex.load(tmp_path)
    assert len(evidence_where(index)) == 1
    assert evidence_where(index, study_type=StudyType.COHORT) == ()
    (obj,) = evidence_where(index, intervention_contains="GRAMMAR")  # casefold
    assert obj.evidence_level == "2"
    assert evidence_where(index, evidence_level="2", domain="fhir-clinical-modeling") == (obj,)
    assert evidence_where(index, domain="medical-benchmark") == ()
    assert evidence_where(index, verification=VerificationState.UNVERIFIED) == (obj,)


def test_query_results_reproducible(tmp_path: Path) -> None:
    _seed(tmp_path)
    first = records_where(ResearchIndex.load(tmp_path), text="decoding")
    second = records_where(ResearchIndex.load(tmp_path), text="decoding")
    assert first == second


# --------------------------------------------------------------------------- stats
def test_stats_counts_and_bytes_stable(tmp_path: Path) -> None:
    _seed(tmp_path)
    index = ResearchIndex.load(tmp_path)
    corpus = corpus_stats(index)
    assert corpus.total_records == 2
    assert corpus.by_source == {"openalex": 1, "pubmed": 1}
    assert corpus.by_domain == {"fhir-clinical-modeling": 1, "medical-benchmark": 1}
    screening = screening_stats(index)
    assert screening.prisma["included"] == 1
    assert screening.inclusion_rate == 1.0  # 1 included / 1 decided
    assert screening.agreement_rate is None  # no multi-reviewer records yet
    evidence = evidence_stats(index)
    assert evidence.total_objects == 1
    assert evidence.by_study_type == {"randomized_controlled_trial": 1}
    assert evidence.source_records_covered == 1
    # byte stability across loads
    a = canonical_json(corpus_stats(ResearchIndex.load(tmp_path)).to_dict())
    b = canonical_json(corpus_stats(ResearchIndex.load(tmp_path)).to_dict())
    assert a == b


def test_reviewer_agreement_computed(tmp_path: Path) -> None:
    fhir, _ = _seed(tmp_path)
    append_events(
        tmp_path / "screening" / "review_log.jsonl",
        (
            make_event(
                fhir.record_id,
                ReviewDecision.INCLUDE,
                reviewer="second",
                decided_at=_TS,
                software_version="0",
                git_sha="abcdef1",
                current=ReviewDecision.INCLUDE,
            ),
        ),
    )
    stats = screening_stats(ResearchIndex.load(tmp_path))
    assert stats.agreement_eligible_records == 1
    assert stats.agreement_rate == 1.0


# ------------------------------------------------------------------- empty corpus
def test_empty_tree_everything_zero(tmp_path: Path) -> None:
    index = ResearchIndex.load(tmp_path)
    assert index.records == () and index.evidence == ()
    assert records_where(index, text="anything") == ()
    assert corpus_stats(index).total_records == 0
    assert screening_stats(index).inclusion_rate is None
    assert evidence_stats(index).total_objects == 0


# --------------------------------------------------------------- corrupted artifacts
def test_corrupted_evidence_fails_closed(tmp_path: Path) -> None:
    _seed(tmp_path)
    path = tmp_path / "evidence" / "objects.jsonl"
    path.write_text(path.read_text(encoding="utf-8") + "{not json\n", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        ResearchIndex.load(tmp_path)  # corruption is an error, never a silent skip


# ------------------------------------------------------------------------ snapshots
def test_snapshot_identity_depends_on_knowledge_not_capture_time(tmp_path: Path) -> None:
    _seed(tmp_path)
    early = capture_snapshot(tmp_path, git_sha="abcdef1", software_version="0.0.0", created_at=_TS)
    later = capture_snapshot(
        tmp_path,
        git_sha="1234567",
        software_version="9.9.9",
        created_at="2035-01-01T00:00:00+00:00",
    )
    assert early.snapshot_id == later.snapshot_id  # same knowledge state, same identity


def test_snapshot_roundtrip_and_verify(tmp_path: Path) -> None:
    _seed(tmp_path)
    snapshot = capture_snapshot(
        tmp_path, git_sha="abcdef1", software_version="0.0.0", created_at=_TS
    )
    path = write_snapshot(tmp_path, snapshot)
    loaded = load_snapshot(path)
    assert loaded.snapshot_id == snapshot.snapshot_id
    assert verify_snapshot(tmp_path, loaded) == ()  # the 2035 guarantee


def test_snapshot_detects_tampering(tmp_path: Path) -> None:
    _seed(tmp_path)
    snapshot = capture_snapshot(
        tmp_path, git_sha="abcdef1", software_version="0.0.0", created_at=_TS
    )
    corpus = tmp_path / "corpus" / "records.jsonl"
    corpus.write_text(corpus.read_text(encoding="utf-8").replace("2025", "2026"), encoding="utf-8")
    mismatches = verify_snapshot(tmp_path, snapshot)
    assert any(m.startswith("corpus:") for m in mismatches)  # names the drifted artifact


def test_snapshot_file_tamper_detected_on_load(tmp_path: Path) -> None:
    _seed(tmp_path)
    snapshot = capture_snapshot(
        tmp_path, git_sha="abcdef1", software_version="0.0.0", created_at=_TS
    )
    path = write_snapshot(tmp_path, snapshot)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["artifact_hashes"]["corpus"] = "f" * 64
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match recomputed identity"):
        load_snapshot(path)


# ----------------------------------------------------------------------------- CLI
def test_cli_stats_emits_canonical_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _seed(tmp_path)
    assert cli.main(["stats", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out.strip()
    document = json.loads(out)
    assert document["corpus"]["total_records"] == 2
    assert out == canonical_json(document)  # canonical on the wire


def test_cli_snapshot_capture_then_verify(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _seed(tmp_path)
    assert cli.main(["snapshot", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    snapshot_file = next((tmp_path / "snapshots").glob("*.json"))
    assert "cite as" in out
    assert cli.main(["snapshot", "--root", str(tmp_path), "--verify", str(snapshot_file)]) == 0
    assert "VERIFIED" in capsys.readouterr().out
    # tamper -> non-zero exit (CI-gateable)
    corpus = tmp_path / "corpus" / "records.jsonl"
    corpus.write_text(corpus.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert cli.main(["snapshot", "--root", str(tmp_path), "--verify", str(snapshot_file)]) == 1
