"""Work-queue views and batch decision appends."""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.litdb import (
    EvidenceTier,
    Identifiers,
    LiteratureRecord,
    ScreeningDecision,
    ScreeningStage,
    append_decisions,
)
from medscale.litdb.workqueue import current_states, pending_at, stage_counts
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(doi: str) -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title=f"Paper {doi}",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, doi, _TS, "a" * 64),
    )


def _decision(record_id: str, to: ScreeningStage, reason: str | None = None) -> ScreeningDecision:
    return ScreeningDecision(record_id=record_id, to_stage=to, decided_at=_TS, reason=reason)


def test_batch_append_bulk_advance(tmp_path: Path) -> None:
    log = tmp_path / "log.jsonl"
    records = tuple(_record(f"10.1/{i}") for i in range(5))
    states = append_decisions(
        log, [_decision(r.record_id, ScreeningStage.DEDUPED) for r in records]
    )
    assert len(states) == 5
    assert stage_counts(records, current_states(log))["deduped"] == 5


def test_batch_is_all_or_nothing(tmp_path: Path) -> None:
    log = tmp_path / "log.jsonl"
    record = _record("10.1/x")
    with pytest.raises(ValueError, match="illegal screening transition"):
        append_decisions(
            log,
            [
                _decision(record.record_id, ScreeningStage.DEDUPED),
                _decision(record.record_id, ScreeningStage.INCLUDED),  # illegal jump
            ],
        )
    assert not log.exists()  # nothing written


def test_pending_at_and_counts(tmp_path: Path) -> None:
    log = tmp_path / "log.jsonl"
    records = tuple(_record(f"10.1/{i}") for i in range(3))
    append_decisions(log, [_decision(records[0].record_id, ScreeningStage.DEDUPED)])
    states = current_states(log)
    assert pending_at(records, states, ScreeningStage.IDENTIFIED) == records[1:]
    assert pending_at(records, states, ScreeningStage.DEDUPED) == records[:1]
    counts = stage_counts(records, states)
    assert counts["identified"] == 2 and counts["deduped"] == 1


def test_missing_log_means_all_identified(tmp_path: Path) -> None:
    records = (_record("10.1/a"),)
    states = current_states(tmp_path / "absent.jsonl")
    assert states == {}
    assert pending_at(records, states, ScreeningStage.IDENTIFIED) == records
