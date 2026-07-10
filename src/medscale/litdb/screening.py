"""PRISMA screening state machine (paper taxonomy §8).

Every record moves through explicit stages; every exclusion records a mandatory reason.
Transitions are enforced, not documented — an illegal move raises.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Final

__all__ = ["ScreeningStage", "ScreeningState", "advance_stage"]


class ScreeningStage(enum.Enum):
    IDENTIFIED = "identified"
    DEDUPED = "deduped"
    SCREENED = "screened"
    ELIGIBILITY = "eligibility"
    INCLUDED = "included"
    EXCLUDED = "excluded"


_TRANSITIONS: Final[dict[ScreeningStage, frozenset[ScreeningStage]]] = {
    ScreeningStage.IDENTIFIED: frozenset({ScreeningStage.DEDUPED, ScreeningStage.EXCLUDED}),
    ScreeningStage.DEDUPED: frozenset({ScreeningStage.SCREENED, ScreeningStage.EXCLUDED}),
    ScreeningStage.SCREENED: frozenset({ScreeningStage.ELIGIBILITY, ScreeningStage.EXCLUDED}),
    ScreeningStage.ELIGIBILITY: frozenset({ScreeningStage.INCLUDED, ScreeningStage.EXCLUDED}),
    # An included paper may later be excluded (e.g. retraction) — with a reason.
    ScreeningStage.INCLUDED: frozenset({ScreeningStage.EXCLUDED}),
    ScreeningStage.EXCLUDED: frozenset(),
}


@dataclass(frozen=True)
class ScreeningState:
    """A record's position in the PRISMA flow. EXCLUDED carries a mandatory reason."""

    stage: ScreeningStage
    reason: str | None = None

    def __post_init__(self) -> None:
        if self.stage is ScreeningStage.EXCLUDED:
            if self.reason is None or not self.reason.strip():
                raise ValueError("EXCLUDED requires a non-empty reason (paper taxonomy §8)")
        elif self.reason is not None:
            raise ValueError(f"reason is only recorded on EXCLUDED, not {self.stage.value}")


def advance_stage(
    state: ScreeningState,
    to: ScreeningStage,
    *,
    reason: str | None = None,
) -> ScreeningState:
    """Move to the next PRISMA stage, enforcing legal transitions."""
    if to not in _TRANSITIONS[state.stage]:
        raise ValueError(f"illegal screening transition: {state.stage.value} -> {to.value}")
    return ScreeningState(stage=to, reason=reason)
