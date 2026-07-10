"""Screening work-queue: which records await which decision.

Pure views over (corpus, replayed screening log) — no state of their own, so the log
remains the single source of truth for PRISMA position.
"""

from __future__ import annotations

from pathlib import Path

from medscale.litdb.records import LiteratureRecord
from medscale.litdb.screening import ScreeningStage, ScreeningState
from medscale.litdb.screening_log import replay_decisions

__all__ = ["current_states", "pending_at", "stage_counts"]


def current_states(log_path: Path) -> dict[str, ScreeningState]:
    """Replay the log into current states (empty log or missing file -> empty dict)."""
    if not log_path.exists():
        return {}
    return replay_decisions(log_path.read_text(encoding="utf-8").splitlines())


def pending_at(
    records: tuple[LiteratureRecord, ...],
    states: dict[str, ScreeningState],
    stage: ScreeningStage,
) -> tuple[LiteratureRecord, ...]:
    """Records currently sitting at ``stage`` (records absent from the log are IDENTIFIED)."""
    default = ScreeningState(ScreeningStage.IDENTIFIED)
    return tuple(
        record for record in records if states.get(record.record_id, default).stage is stage
    )


def stage_counts(
    records: tuple[LiteratureRecord, ...], states: dict[str, ScreeningState]
) -> dict[str, int]:
    """PRISMA position counts for the whole corpus (deterministic key order by stage)."""
    default = ScreeningState(ScreeningStage.IDENTIFIED)
    counts = dict.fromkeys((stage.value for stage in ScreeningStage), 0)
    for record in records:
        counts[states.get(record.record_id, default).stage.value] += 1
    return counts
