"""Collaboration workflow: reviewer identity, reviewer-scoped logs, deterministic merge.

Stability: internal. All structures are deterministic, append-only, and local-only.
No external calls, no authentication, no cloud sync.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from medscale.litdb.review import (
    ExclusionReason,
    RecordReview,
    ReviewDecision,
    ReviewEvent,
    prisma_summary,
    replay_reviews,
)
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json, content_hash

__all__ = [
    "APPEND_ONLY_POLICY",
    "REVIEWERS_DIR",
    "AppendOnlyError",
    "LogIntegrityReport",
    "MergeConflict",
    "MergeManifest",
    "MergedReviewLog",
    "ReviewerIdentity",
    "ReviewerLog",
    "load_reviewer_events",
    "load_reviewer_identity",
    "load_reviewer_logs",
    "merge_reviewer_logs",
    "merge_summary",
    "prisma_from_merged",
    "reviewer_log_path",
    "validate_merge_references",
    "validate_reviewer_log",
    "write_reviewer_identity",
]

REVIEWERS_DIR: Final = "collaboration/reviewers"
MERGES_DIR: Final = "collaboration/merges"

APPEND_ONLY_POLICY: Final = "events are immutable; append-only"


class AppendOnlyError(Exception):
    """Raised when a log would be mutated instead of appended."""


class ReviewerIdentity:
    """Lightweight immutable reviewer identifier.

    No authentication. The ID is an audit label only.
    """

    __slots__ = ("metadata", "reviewer_id")

    def __init__(self, reviewer_id: str, metadata: dict[str, Any] | None = None) -> None:
        if not reviewer_id.strip():
            raise ValueError("reviewer_id must be non-empty")
        self.reviewer_id = reviewer_id.strip()
        self.metadata = metadata or {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReviewerIdentity):
            return NotImplemented
        return self.reviewer_id == other.reviewer_id and self.metadata == other.metadata

    def __repr__(self) -> str:
        return f"ReviewerIdentity(reviewer_id={self.reviewer_id!r}, metadata={self.metadata!r})"

    def to_dict(self) -> dict[str, Any]:
        return {"reviewer_id": self.reviewer_id, "metadata": self.metadata}


@dataclass(frozen=True)
class ReviewerLog:
    reviewer_id: str
    record_ids: tuple[str, ...]
    decisions: tuple[ReviewDecision, ...]
    created_at: str

    def __post_init__(self) -> None:
        if not self.reviewer_id.strip():
            raise ValueError("reviewer_id must be non-empty")
        validate_timestamp(self.created_at, "created_at")
        if len(self.record_ids) != len(self.decisions):
            raise ValueError("record_ids and decisions length differ")

    def to_dict(self) -> dict[str, Any]:
        return {
            "reviewer_id": self.reviewer_id,
            "record_ids": list(self.record_ids),
            "decisions": [d.value for d in self.decisions],
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class LogIntegrityReport:
    reviewer_id: str
    event_count: int
    issues: tuple[str, ...]
    previous_hash: str | None = None
    current_hash: str | None = None

    @property
    def is_clean(self) -> bool:
        return not self.issues


def reviewer_log_path(root: Path, reviewer_id: str) -> Path:
    return root / REVIEWERS_DIR / f"{reviewer_id}.jsonl"


def write_reviewer_identity(root: Path, identity: ReviewerIdentity) -> Path:
    target = root / REVIEWERS_DIR / f"{identity.reviewer_id}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_json(identity.to_dict()), encoding="utf-8", newline="\n")
    return target


def load_reviewer_identity(path: Path) -> ReviewerIdentity:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ReviewerIdentity(reviewer_id=str(data["reviewer_id"]), metadata=data.get("metadata"))


def _merge_events_for(log_path: Path) -> tuple[ReviewEvent, ...]:
    if not log_path.exists():
        return ()
    return load_reviewer_events(log_path)


def load_reviewer_events(path: Path) -> tuple[ReviewEvent, ...]:
    if not path.exists():
        return ()
    events: list[ReviewEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        events.append(_event_from_dict(json.loads(stripped)))
    return tuple(events)


def validate_reviewer_log(path: Path) -> LogIntegrityReport:
    if not path.exists():
        return LogIntegrityReport(reviewer_id=path.stem, event_count=0, issues=())

    lines = path.read_text(encoding="utf-8").splitlines()
    events: list[ReviewEvent] = []
    issues: list[str] = []
    current: dict[str, ReviewDecision] = {}

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            issues.append(f"line {index + 1}: invalid json: {exc}")
            continue
        try:
            event = _event_from_dict(payload)
        except Exception as exc:
            issues.append(f"line {index + 1}: invalid review event: {exc}")
            continue

        if index == 0:
            if event.previous_decision is not ReviewDecision.PENDING:
                issues.append(f"line {index + 1}: first event must start from PENDING")
        else:
            prev = current.get(event.record_id, ReviewDecision.PENDING)
            if event.previous_decision != prev:
                issues.append(
                    f"line {index + 1}: chain broken for {event.record_id}: "
                    f"expected previous={prev.value}, got {event.previous_decision.value}"
                )

        current[event.record_id] = event.new_decision
        events.append(event)

    return LogIntegrityReport(
        reviewer_id=path.stem,
        event_count=len(events),
        issues=tuple(issues),
        previous_hash=_entry_hash(events[0]) if events else None,
        current_hash=_entry_hash(events[-1]) if events else None,
    )


def _entry_hash(event: ReviewEvent) -> str:
    return content_hash(event.to_dict())


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
class MergeConflict:
    record_id: str
    reviewer_a: str
    reviewer_b: str
    decision_a: ReviewDecision
    decision_b: ReviewDecision

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "reviewer_a": self.reviewer_a,
            "reviewer_b": self.reviewer_b,
            "decision_a": self.decision_a.value,
            "decision_b": self.decision_b.value,
        }


@dataclass(frozen=True)
class MergeManifest:
    reviewer_a: str
    reviewer_b: str
    merged_at: str
    total_records: int
    conflict_count: int
    conflicts: tuple[MergeConflict, ...]
    manifest_hash: str

    def __post_init__(self) -> None:
        if self.conflict_count != len(self.conflicts):
            raise ValueError("conflict_count must match len(conflicts)")

    def to_dict(self) -> dict[str, Any]:
        return {
            "reviewer_a": self.reviewer_a,
            "reviewer_b": self.reviewer_b,
            "merged_at": self.merged_at,
            "total_records": self.total_records,
            "conflict_count": self.conflict_count,
            "conflicts": [c.to_dict() for c in sorted(self.conflicts, key=lambda c: c.record_id)],
            "manifest_hash": self.manifest_hash,
        }


@dataclass(frozen=True)
class MergedReviewLog:
    manifest: MergeManifest
    summaries: dict[str, ReviewerLog]

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest.to_dict(),
            "summaries": {k: v.to_dict() for k, v in sorted(self.summaries.items())},
        }


def load_reviewer_logs(root: Path) -> dict[str, ReviewerLog]:
    reviewers_dir = root / REVIEWERS_DIR
    if not reviewers_dir.exists():
        return {}

    logs: dict[str, ReviewerLog] = {}
    for path in sorted(reviewers_dir.glob("*.jsonl")):
        events = load_reviewer_events(path)
        decisions: list[ReviewDecision] = []
        record_ids: list[str] = []

        for event in events:
            record_ids.append(event.record_id)
            decisions.append(event.new_decision)

        if events:
            logs[path.stem] = ReviewerLog(
                reviewer_id=path.stem,
                record_ids=tuple(record_ids),
                decisions=tuple(decisions),
                created_at=events[0].decided_at,
            )
    return logs


def merge_reviewer_logs(root: Path, reviewer_a: str, reviewer_b: str) -> MergedReviewLog:
    log_a = reviewer_log_path(root, reviewer_a)
    log_b = reviewer_log_path(root, reviewer_b)
    events_a = load_reviewer_events(log_a)
    events_b = load_reviewer_events(log_b)

    reviews_a = replay_reviews([canonical_json(e.to_dict()) for e in events_a])
    reviews_b = replay_reviews([canonical_json(e.to_dict()) for e in events_b])

    all_ids = sorted(set(reviews_a) | set(reviews_b))
    conflicts: list[MergeConflict] = []

    for record_id in all_ids:
        decision_a = reviews_a.get(record_id, RecordReview(ReviewDecision.PENDING)).decision
        decision_b = reviews_b.get(record_id, RecordReview(ReviewDecision.PENDING)).decision
        if decision_a is ReviewDecision.PENDING or decision_b is ReviewDecision.PENDING:
            continue
        if decision_a != decision_b:
            conflicts.append(
                MergeConflict(
                    record_id=record_id,
                    reviewer_a=reviewer_a,
                    reviewer_b=reviewer_b,
                    decision_a=decision_a,
                    decision_b=decision_b,
                )
            )

    summaries = {
        reviewer_a: ReviewerLog(
            reviewer_id=reviewer_a,
            record_ids=tuple(r for r in all_ids if r in reviews_a),
            decisions=tuple(reviews_a[r].decision for r in all_ids if r in reviews_a),
            created_at=events_a[0].decided_at if events_a else "1970-01-01T00:00:00+00:00",
        ),
        reviewer_b: ReviewerLog(
            reviewer_id=reviewer_b,
            record_ids=tuple(r for r in all_ids if r in reviews_b),
            decisions=tuple(reviews_b[r].decision for r in all_ids if r in reviews_b),
            created_at=events_b[0].decided_at if events_b else "1970-01-01T00:00:00+00:00",
        ),
    }

    manifest = MergeManifest(
        reviewer_a=reviewer_a,
        reviewer_b=reviewer_b,
        merged_at="2026-07-13T00:00:00+00:00",
        total_records=len(all_ids),
        conflict_count=len(conflicts),
        conflicts=tuple(conflicts),
        manifest_hash="",
    )
    manifest = MergeManifest(
        reviewer_a=manifest.reviewer_a,
        reviewer_b=manifest.reviewer_b,
        merged_at=manifest.merged_at,
        total_records=manifest.total_records,
        conflict_count=manifest.conflict_count,
        conflicts=manifest.conflicts,
        manifest_hash=content_hash(manifest.to_dict()),
    )
    return MergedReviewLog(manifest=manifest, summaries=summaries)


def merge_summary(merged: MergedReviewLog) -> dict[str, int]:
    counts: dict[str, int] = {}
    for summary in merged.summaries.values():
        for decision in summary.decisions:
            counts[decision.value] = counts.get(decision.value, 0) + 1
    return dict(sorted(counts.items()))


def prisma_from_merged(merged: MergedReviewLog) -> dict[str, Any]:
    all_record_ids = sorted(
        {record_id for summary in merged.summaries.values() for record_id in summary.record_ids}
    )
    combined_reviews: dict[str, RecordReview] = {}
    for summary in merged.summaries.values():
        for record_id, decision in zip(summary.record_ids, summary.decisions, strict=True):
            combined_reviews[record_id] = RecordReview(decision)
    prisma = prisma_summary(all_record_ids, combined_reviews)
    return {
        "included": prisma.included,
        "excluded": prisma.excluded,
        "uncertain": prisma.uncertain,
        "pending": prisma.pending,
        "screened": prisma.screened,
        "exclusion_breakdown": prisma.exclusion_breakdown,
    }


def validate_merge_references(merged: MergedReviewLog, root: Path) -> tuple[bool, list[str]]:
    reviewers_dir = root / REVIEWERS_DIR
    issues: list[str] = []

    for reviewer_id in (merged.manifest.reviewer_a, merged.manifest.reviewer_b):
        if not (reviewers_dir / f"{reviewer_id}.jsonl").exists():
            issues.append(f"missing reviewer log: {reviewer_id}.jsonl")

    ids = {record_id for summary in merged.summaries.values() for record_id in summary.record_ids}
    for conflict in merged.manifest.conflicts:
        if conflict.record_id not in ids:
            issues.append(f"conflict references unknown record: {conflict.record_id}")

    return not issues, issues