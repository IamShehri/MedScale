"""The append-only screening log: replay-derived states, enforced legality."""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.litdb import (
    ScreeningDecision,
    ScreeningStage,
    append_decision,
    replay_decisions,
)

_TS = "2026-07-10T00:00:00+00:00"


def _decision(record_id: str, to: ScreeningStage, reason: str | None = None) -> ScreeningDecision:
    return ScreeningDecision(record_id=record_id, to_stage=to, decided_at=_TS, reason=reason)


def test_append_and_replay_roundtrip(tmp_path: Path) -> None:
    log = tmp_path / "screening_log.jsonl"
    append_decision(log, _decision("rec1", ScreeningStage.DEDUPED))
    append_decision(log, _decision("rec1", ScreeningStage.SCREENED))
    state = append_decision(
        log, _decision("rec1", ScreeningStage.EXCLUDED, reason="off-topic-all-rqs")
    )
    assert state.stage is ScreeningStage.EXCLUDED

    replayed = replay_decisions(log.read_text(encoding="utf-8").splitlines())
    assert replayed["rec1"].stage is ScreeningStage.EXCLUDED
    assert replayed["rec1"].reason == "off-topic-all-rqs"


def test_illegal_decision_is_not_appended(tmp_path: Path) -> None:
    log = tmp_path / "screening_log.jsonl"
    append_decision(log, _decision("rec1", ScreeningStage.DEDUPED))
    with pytest.raises(ValueError, match="illegal screening transition"):
        append_decision(log, _decision("rec1", ScreeningStage.INCLUDED))
    # the illegal line must NOT have been written
    assert len(log.read_text(encoding="utf-8").splitlines()) == 1


def test_exclusion_reason_enforced_through_log(tmp_path: Path) -> None:
    log = tmp_path / "screening_log.jsonl"
    with pytest.raises(ValueError, match="reason"):
        append_decision(log, _decision("rec2", ScreeningStage.EXCLUDED))


def test_records_are_independent(tmp_path: Path) -> None:
    log = tmp_path / "screening_log.jsonl"
    append_decision(log, _decision("a", ScreeningStage.DEDUPED))
    append_decision(log, _decision("b", ScreeningStage.DEDUPED))
    append_decision(log, _decision("a", ScreeningStage.SCREENED))
    states = replay_decisions(log.read_text(encoding="utf-8").splitlines())
    assert states["a"].stage is ScreeningStage.SCREENED
    assert states["b"].stage is ScreeningStage.DEDUPED


def test_blank_lines_ignored() -> None:
    assert replay_decisions(["", "  "]) == {}
