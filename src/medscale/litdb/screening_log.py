"""Append-only PRISMA screening log.

Screening decisions are facts with provenance: each is one canonical-JSON line in a
committed JSONL file. Current states are *replayed* from the log through the
:mod:`~medscale.litdb.screening` state machine, so an illegal decision can neither be
appended nor smuggled into history — the log is the audit trail the PRISMA counts are
computed from.

Records enter the corpus at ``identified``; the log holds every transition after that.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from medscale.litdb.screening import ScreeningStage, ScreeningState, advance_stage
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json

__all__ = ["ScreeningDecision", "append_decision", "replay_decisions"]


@dataclass(frozen=True)
class ScreeningDecision:
    """One human screening decision (no model-as-judge: the decider is the operator)."""

    record_id: str
    to_stage: ScreeningStage
    decided_at: str
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must be non-empty")
        validate_timestamp(self.decided_at, "decided_at")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "to_stage": self.to_stage.value,
            "decided_at": self.decided_at,
            "reason": self.reason,
        }


def _decision_from_dict(payload: dict[str, Any]) -> ScreeningDecision:
    return ScreeningDecision(
        record_id=str(payload["record_id"]),
        to_stage=ScreeningStage(payload["to_stage"]),
        decided_at=str(payload["decided_at"]),
        reason=payload.get("reason"),
    )


def replay_decisions(lines: Iterable[str]) -> dict[str, ScreeningState]:
    """Rebuild every record's current state by replaying the log through the state machine."""
    states: dict[str, ScreeningState] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        decision = _decision_from_dict(json.loads(stripped))
        current = states.get(decision.record_id, ScreeningState(ScreeningStage.IDENTIFIED))
        states[decision.record_id] = advance_stage(
            current, decision.to_stage, reason=decision.reason
        )
    return states


def append_decision(log_path: Path, decision: ScreeningDecision) -> ScreeningState:
    """Validate ``decision`` against the replayed log, then append it. Returns the new state."""
    existing = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
    states = replay_decisions(existing)
    current = states.get(decision.record_id, ScreeningState(ScreeningStage.IDENTIFIED))
    new_state = advance_stage(current, decision.to_stage, reason=decision.reason)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(decision.to_dict()) + "\n")
    return new_state
