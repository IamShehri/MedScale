"""Persisted-format versioning (stress-test F1): markers written, absence tolerated.

The decade contract: every serialized artifact says which format wrote it; every
reader treats a missing marker as format 1 (pre-marker era). Committed logs are never
rewritten - old and new lines coexist.
"""

from __future__ import annotations

import json
from pathlib import Path

from medscale.litdb import (
    EvidenceTier,
    Identifiers,
    LiteratureRecord,
    RunManifest,
    ScreeningDecision,
    ScreeningStage,
)
from medscale.litdb.review import ReviewDecision, make_event, replay_reviews
from medscale.litdb.screening_log import replay_decisions
from medscale.litdb.store import load_corpus, record_from_dict, record_to_dict, write_corpus
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(doi: str = "10.1/x") -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title="A format-versioned record",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, doi, _TS, "a" * 64),
    )


def test_serializers_emit_format_marker() -> None:
    assert record_to_dict(_record())["format"] == 1
    decision = ScreeningDecision("r1", ScreeningStage.DEDUPED, _TS)
    assert decision.to_dict()["format"] == 1
    event = make_event(
        "r1",
        ReviewDecision.INCLUDE,
        reviewer="op",
        decided_at=_TS,
        software_version="0.0.0",
        git_sha="abcdef1",
    )
    assert event.to_dict()["format"] == 1
    manifest = RunManifest("r1", "abcdef1", ())
    assert manifest.to_dict()["format"] == 1


def test_legacy_record_without_marker_loads() -> None:
    legacy = record_to_dict(_record())
    del legacy["format"]  # simulate a pre-marker line
    restored = record_from_dict(legacy)
    assert restored.record_id == _record().record_id


def test_legacy_and_marked_log_lines_coexist(tmp_path: Path) -> None:
    marked = ScreeningDecision("r1", ScreeningStage.DEDUPED, _TS).to_dict()
    legacy = {k: v for k, v in marked.items() if k != "format"}
    legacy["record_id"] = "r2"
    lines = [json.dumps(legacy), json.dumps(marked)]
    states = replay_decisions(lines)
    assert set(states) == {"r1", "r2"}


def test_legacy_review_event_replays() -> None:
    event_dict = make_event(
        "r1",
        ReviewDecision.INCLUDE,
        reviewer="op",
        decided_at=_TS,
        software_version="0.0.0",
        git_sha="abcdef1",
    ).to_dict()
    del event_dict["format"]
    reviews = replay_reviews([json.dumps(event_dict)])
    assert reviews["r1"].decision is ReviewDecision.INCLUDE


def test_corpus_marker_survives_roundtrip(tmp_path: Path) -> None:
    corpus = tmp_path / "records.jsonl"
    write_corpus(corpus, [_record()])
    assert '"format":1' in corpus.read_text(encoding="utf-8")
    (loaded,) = load_corpus(corpus)
    assert loaded == _record()
