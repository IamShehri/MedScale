"""Evaluation helpers for MedScale AI Triage Assistant v0.1.

Metrics:
- Included-paper hit rate: fraction of human-included papers that AI flagged HIGH/MEDIUM.
- False-negative rate: highest-priority failure mode.
- Time-reduction estimate: fraction of corpus sorted into higher priority buckets.
- Agreement / lift over random: simple priority lift.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from medscale.litdb.ai_triage import load_triage_log
from medscale.litdb.review import ReviewDecision, current_reviews
from medscale.reproducibility import canonical_json

__all__ = [
    "EvaluationRun",
    "compute_metrics",
    "evaluate",
    "load_goldset",
    "write_goldset",
]


@dataclass(frozen=True)
class EvaluationRun:
    recommended_medium_plus: int
    human_included_total: int
    human_included_flagged: int
    included_hit_rate: float | None
    false_negative_count: int
    false_negative_rate: float | None
    high_fraction: float | None
    medium_fraction: float | None
    low_fraction: float | None
    uncertain_fraction: float | None
    pending_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "recommended_medium_plus": self.recommended_medium_plus,
            "human_included_total": self.human_included_total,
            "human_included_flagged": self.human_included_flagged,
            "included_hit_rate": self.included_hit_rate,
            "false_negative_count": self.false_negative_count,
            "false_negative_rate": self.false_negative_rate,
            "high_fraction": self.high_fraction,
            "medium_fraction": self.medium_fraction,
            "low_fraction": self.low_fraction,
            "uncertain_fraction": self.uncertain_fraction,
            "pending_count": self.pending_count,
        }


def _decision_bucket(recommendation: str) -> str:
    if recommendation == "review first":
        return "high"
    if recommendation == "review later":
        return "medium"
    if recommendation == "low priority":
        return "low"
    return "uncertain"


def compute_metrics(
    recommendations: Mapping[str, Any],
    reviews: Mapping[str, Any],
) -> EvaluationRun:
    recs: dict[str, Any] = dict(recommendations)
    revs: dict[str, Any] = dict(reviews)
    total = len(recs)
    included_total = 0
    included_flagged = 0
    recommended_medium_plus = 0
    bucket_counts = {"high": 0, "medium": 0, "low": 0, "uncertain": 0}
    for record_id, recommendation in recs.items():
        bucket = _decision_bucket(str(getattr(recommendation, "recommendation", "")))
        bucket_counts[bucket] += 1
        review = revs.get(record_id)
        decision = getattr(review, "decision", None) if review is not None else None
        if decision is ReviewDecision.INCLUDE:
            included_total += 1
            if bucket in {"high", "medium"}:
                included_flagged += 1
        if bucket in {"high", "medium"}:
            recommended_medium_plus += 1
    false_negative_count = max(included_total - included_flagged, 0)
    false_negative_rate = false_negative_count / included_total if included_total else None
    included_hit_rate = included_flagged / included_total if included_total else None
    return EvaluationRun(
        recommended_medium_plus=recommended_medium_plus,
        human_included_total=included_total,
        human_included_flagged=included_flagged,
        included_hit_rate=included_hit_rate,
        false_negative_count=false_negative_count,
        false_negative_rate=false_negative_rate,
        high_fraction=bucket_counts["high"] / total if total else None,
        medium_fraction=bucket_counts["medium"] / total if total else None,
        low_fraction=bucket_counts["low"] / total if total else None,
        uncertain_fraction=bucket_counts["uncertain"] / total if total else None,
        pending_count=total,
    )


def write_goldset(
    path: Path,
    recommendations: Mapping[str, Any],
    reviews: Mapping[str, Any],
) -> None:
    """Write evaluated goldset entries including human decision alignment."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for record_id, recommendation in recommendations.items():
        review = reviews.get(record_id)
        decision_value = None
        if review is not None:
            decision = getattr(review, "decision", None)
            if decision is not None:
                decision_value = decision.value
        entry = {
            "record_id": record_id,
            "recommendation": str(getattr(recommendation, "recommendation", "")),
            "confidence": getattr(recommendation, "confidence", 0.0),
            "human_decision": decision_value,
        }
        lines.append(canonical_json(entry))
    if lines:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def load_goldset(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    entries: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        entries.append(json.loads(stripped))
    return entries


def evaluate(
    triage_log_path: Path,
    review_log_path: Path,
    output_path: Path,
) -> EvaluationRun:
    """Run triage evaluation and write goldset plus metrics."""

    recommendations = load_triage_log(triage_log_path)
    reviews = current_reviews(review_log_path)
    run = compute_metrics(recommendations, reviews)
    write_goldset(output_path, recommendations, reviews)
    return run
