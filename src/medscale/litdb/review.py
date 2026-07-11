"""Human screening decisions: the operator's append-only evidence-review layer.

This is where collected literature becomes *validated* evidence — by human decision, no
model in the loop. It sits on top of the PRISMA stage vocabulary
(:mod:`medscale.litdb.screening`) without mutating it: the operator records a controlled
**decision** per record, and the PRISMA **stage** is a pure function of that decision
(``_STAGE_FOR``). Corrections are new events that change the decision; history is never
edited. Every counted number is reproducible by replaying the log.

Decision -> stage mapping (single-stage title/abstract screening for the scoping round):

    PENDING / UNCERTAIN   -> DEDUPED   (still in the queue)
    INCLUDE               -> SCREENED  (passed title/abstract; provisionally included)
    EXCLUDE               -> EXCLUDED  (with a machine-readable reason)
    DUPLICATE_CONFIRMED   -> EXCLUDED  (reason = DUPLICATE)
"""

from __future__ import annotations

import enum
import json
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from medscale.litdb.screening import ScreeningStage
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json

__all__ = [
    "ExclusionReason",
    "PrismaSummary",
    "RecordReview",
    "ReviewDecision",
    "ReviewEvent",
    "append_events",
    "current_reviews",
    "make_event",
    "pending_queue",
    "prisma_summary",
    "replay_reviews",
    "stage_for_decision",
]

_GIT_SHA: Final = re.compile(r"^[0-9a-f]{7,40}$")


class ReviewDecision(enum.Enum):
    """Controlled decision states — never free-form."""

    PENDING = "pending"
    INCLUDE = "include"
    EXCLUDE = "exclude"
    UNCERTAIN = "uncertain"
    DUPLICATE_CONFIRMED = "duplicate_confirmed"


class ExclusionReason(enum.Enum):
    """Machine-readable exclusion taxonomy (required for EXCLUDE / DUPLICATE_CONFIRMED)."""

    NOT_RELEVANT = "not_relevant"
    WRONG_POPULATION = "wrong_population"
    WRONG_INTERVENTION = "wrong_intervention"
    WRONG_OUTCOME = "wrong_outcome"
    NOT_MEDICAL_AI = "not_medical_ai"
    NO_PRIMARY_EVIDENCE = "no_primary_evidence"
    DUPLICATE = "duplicate"
    OTHER = "other"


_STAGE_FOR: Final[dict[ReviewDecision, ScreeningStage]] = {
    ReviewDecision.PENDING: ScreeningStage.DEDUPED,
    ReviewDecision.UNCERTAIN: ScreeningStage.DEDUPED,
    ReviewDecision.INCLUDE: ScreeningStage.SCREENED,
    ReviewDecision.EXCLUDE: ScreeningStage.EXCLUDED,
    ReviewDecision.DUPLICATE_CONFIRMED: ScreeningStage.EXCLUDED,
}

_TERMINAL: Final = frozenset(
    {ReviewDecision.INCLUDE, ReviewDecision.EXCLUDE, ReviewDecision.DUPLICATE_CONFIRMED}
)


def stage_for_decision(decision: ReviewDecision) -> ScreeningStage:
    """The PRISMA stage implied by a decision (pure, total)."""
    return _STAGE_FOR[decision]


@dataclass(frozen=True)
class ReviewEvent:
    """One human decision, with the full audit trail the directive mandates."""

    record_id: str
    previous_decision: ReviewDecision
    new_decision: ReviewDecision
    reviewer: str
    decided_at: str
    software_version: str
    git_sha: str
    exclusion_reason: ExclusionReason | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must be non-empty")
        if self.new_decision is ReviewDecision.PENDING:
            raise ValueError("PENDING is the default, not an applied decision")
        if not self.reviewer.strip():
            raise ValueError("reviewer must be non-empty")
        validate_timestamp(self.decided_at, "decided_at")
        if not self.software_version.strip():
            raise ValueError("software_version must be non-empty")
        if not _GIT_SHA.match(self.git_sha):
            raise ValueError(f"git_sha must be a 7-40 hex git SHA, got {self.git_sha!r}")
        if self.new_decision in (ReviewDecision.EXCLUDE, ReviewDecision.DUPLICATE_CONFIRMED):
            if self.exclusion_reason is None:
                raise ValueError(f"{self.new_decision.value} requires an exclusion_reason")
        elif self.exclusion_reason is not None:
            raise ValueError(
                f"exclusion_reason is only valid for EXCLUDE/DUPLICATE_CONFIRMED, "
                f"not {self.new_decision.value}"
            )
        if self.new_decision is ReviewDecision.DUPLICATE_CONFIRMED and (
            self.exclusion_reason is not ExclusionReason.DUPLICATE
        ):
            raise ValueError("DUPLICATE_CONFIRMED requires exclusion_reason=DUPLICATE")

    @property
    def previous_stage(self) -> ScreeningStage:
        return stage_for_decision(self.previous_decision)

    @property
    def new_stage(self) -> ScreeningStage:
        return stage_for_decision(self.new_decision)

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "record_id": self.record_id,
            "previous_decision": self.previous_decision.value,
            "new_decision": self.new_decision.value,
            "previous_stage": self.previous_stage.value,
            "new_stage": self.new_stage.value,
            "reviewer": self.reviewer,
            "decided_at": self.decided_at,
            "exclusion_reason": self.exclusion_reason.value if self.exclusion_reason else None,
            "notes": self.notes,
            "software_version": self.software_version,
            "git_sha": self.git_sha,
        }


def _event_from_dict(data: dict[str, Any]) -> ReviewEvent:
    reason = data.get("exclusion_reason")
    return ReviewEvent(
        record_id=str(data["record_id"]),
        previous_decision=ReviewDecision(data["previous_decision"]),
        new_decision=ReviewDecision(data["new_decision"]),
        reviewer=str(data["reviewer"]),
        decided_at=str(data["decided_at"]),
        software_version=str(data["software_version"]),
        git_sha=str(data["git_sha"]),
        exclusion_reason=ExclusionReason(reason) if reason else None,
        notes=str(data.get("notes", "")),
    )


@dataclass(frozen=True)
class RecordReview:
    """A record's current review state (latest decision wins on replay)."""

    decision: ReviewDecision
    exclusion_reason: ExclusionReason | None = None


def make_event(
    record_id: str,
    new_decision: ReviewDecision,
    *,
    reviewer: str,
    decided_at: str,
    software_version: str,
    git_sha: str,
    current: ReviewDecision = ReviewDecision.PENDING,
    exclusion_reason: ExclusionReason | None = None,
    notes: str = "",
) -> ReviewEvent:
    """Construct a validated event from the record's current decision to a new one."""
    return ReviewEvent(
        record_id=record_id,
        previous_decision=current,
        new_decision=new_decision,
        reviewer=reviewer,
        decided_at=decided_at,
        software_version=software_version,
        git_sha=git_sha,
        exclusion_reason=exclusion_reason,
        notes=notes,
    )


def replay_reviews(lines: Iterable[str]) -> dict[str, RecordReview]:
    """Rebuild each record's current review from the append-only log (latest wins)."""
    reviews: dict[str, RecordReview] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        event = _event_from_dict(json.loads(stripped))
        reviews[event.record_id] = RecordReview(event.new_decision, event.exclusion_reason)
    return reviews


def current_reviews(log_path: Path) -> dict[str, RecordReview]:
    if not log_path.exists():
        return {}
    return replay_reviews(log_path.read_text(encoding="utf-8").splitlines())


def append_events(log_path: Path, events: Sequence[ReviewEvent]) -> None:
    """Append events to the review log (canonical JSON, LF). History is never rewritten."""
    if not events:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [canonical_json(event.to_dict()) for event in events]
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def pending_queue(record_ids: Sequence[str], reviews: dict[str, RecordReview]) -> tuple[str, ...]:
    """Record ids still needing a decision: never-decided (PENDING) or UNCERTAIN (revisit).

    Order is preserved from ``record_ids`` (the caller controls corpus order), with
    UNCERTAIN records placed after never-seen ones so first-pass work comes first.
    """
    never: list[str] = []
    uncertain: list[str] = []
    for record_id in record_ids:
        review = reviews.get(record_id)
        if review is None:
            never.append(record_id)
        elif review.decision is ReviewDecision.UNCERTAIN:
            uncertain.append(record_id)
    return tuple(never + uncertain)


@dataclass(frozen=True)
class PrismaSummary:
    identified: int | None
    deduplicated: int
    screened: int
    included: int
    excluded: int
    uncertain: int
    pending: int
    exclusion_breakdown: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "identified": self.identified,
            "deduplicated": self.deduplicated,
            "screened": self.screened,
            "included": self.included,
            "excluded": self.excluded,
            "uncertain": self.uncertain,
            "pending": self.pending,
            "exclusion_breakdown": self.exclusion_breakdown,
        }


def prisma_summary(
    record_ids: Sequence[str],
    reviews: dict[str, RecordReview],
    *,
    identified: int | None = None,
) -> PrismaSummary:
    """Reproducible PRISMA counts over the deduplicated corpus and its review log.

    ``screened`` = records with a terminal decision (looked at and decided);
    ``included`` = INCLUDE (passed title/abstract); ``excluded`` = EXCLUDE +
    DUPLICATE_CONFIRMED, with a per-reason breakdown.
    """
    included = excluded = uncertain = pending = 0
    breakdown: dict[str, int] = {}
    for record_id in record_ids:
        review = reviews.get(record_id)
        decision = review.decision if review else ReviewDecision.PENDING
        if decision is ReviewDecision.INCLUDE:
            included += 1
        elif decision in (ReviewDecision.EXCLUDE, ReviewDecision.DUPLICATE_CONFIRMED):
            excluded += 1
            if review is not None and review.exclusion_reason is not None:
                key = review.exclusion_reason.value
                breakdown[key] = breakdown.get(key, 0) + 1
        elif decision is ReviewDecision.UNCERTAIN:
            uncertain += 1
        else:
            pending += 1
    return PrismaSummary(
        identified=identified,
        deduplicated=len(record_ids),
        screened=included + excluded,
        included=included,
        excluded=excluded,
        uncertain=uncertain,
        pending=pending,
        exclusion_breakdown=dict(sorted(breakdown.items())),
    )
