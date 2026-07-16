"""Deterministic Pilot-01 evaluation metrics."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from medscale.mesc.contracts import PilotRecord

_DECISIONS = ("yes", "no", "maybe", "abstain")


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


@dataclass(frozen=True)
class PilotMetricValue:
    """One deterministic metric value or grouped metric summary."""

    name: str
    value: float | int | None
    count: int | None = None
    note: str | None = None
    status: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "value": self.value,
            "count": self.count,
            "note": self.note,
            "status": self.status,
        }


@dataclass(frozen=True)
class PilotEvaluationResult:
    """Evaluation result for one condition or aggregate."""

    condition: str
    metrics: tuple[PilotMetricValue, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "condition": self.condition,
            "metrics": [metric.to_dict() for metric in self.metrics],
        }


@dataclass(frozen=True)
class PilotEvaluationReport:
    """Deterministic wrapper around ordered evaluation results."""

    results: tuple[PilotEvaluationResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "results": [result.to_dict() for result in self.results],
        }


def pilot_decision_accuracy(
    predictions: Sequence[str],
    references: Sequence[str],
) -> PilotMetricValue:
    if len(predictions) != len(references):
        raise ValueError("predictions and references must have the same length")
    if not predictions:
        return PilotMetricValue(
            name="decision_accuracy",
            value=None,
            count=0,
            note="no examples",
            status="not_applicable",
        )
    correct = sum(
        1
        for prediction, reference in zip(predictions, references, strict=True)
        if prediction == reference
    )
    return PilotMetricValue(
        name="decision_accuracy",
        value=_safe_divide(correct, len(predictions)),
        count=len(predictions),
        status="success",
    )


def pilot_macro_f1(
    predictions: Sequence[str],
    references: Sequence[str],
) -> PilotMetricValue:
    if len(predictions) != len(references):
        raise ValueError("predictions and references must have the same length")
    if not predictions:
        return PilotMetricValue(
            name="macro_f1",
            value=None,
            count=0,
            note="no examples",
            status="not_applicable",
        )

    def _safe_f1(precision: float, recall: float) -> float:
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    f1_scores = []
    for decision in _DECISIONS:
        true_positives = sum(
            1
            for prediction, reference in zip(predictions, references, strict=True)
            if prediction == decision and reference == decision
        )
        predicted_positives = sum(1 for prediction in predictions if prediction == decision)
        actual_positives = sum(1 for reference in references if reference == decision)
        precision = _safe_divide(true_positives, predicted_positives)
        recall = _safe_divide(true_positives, actual_positives)
        f1_scores.append(_safe_f1(precision, recall))

    return PilotMetricValue(
        name="macro_f1",
        value=sum(f1_scores) / len(f1_scores) if f1_scores else None,
        count=len(predictions),
        status="success",
    )


def pilot_valid_json_rate(outputs: Sequence[str]) -> PilotMetricValue:
    if not outputs:
        return PilotMetricValue(
            name="valid_json_rate",
            value=None,
            count=0,
            note="no outputs",
            status="not_applicable",
        )
    import json

    valid = 0
    for output in outputs:
        try:
            json.loads(output)
            valid += 1
        except json.JSONDecodeError:
            pass
    return PilotMetricValue(
        name="valid_json_rate",
        value=_safe_divide(valid, len(outputs)),
        count=len(outputs),
        status="success",
    )


def pilot_evidence_reference_validity(
    records: Sequence[PilotRecord],
    claim_predictions: Sequence[Sequence[tuple[str, tuple[str, ...]]]] | None = None,
) -> PilotMetricValue:
    if claim_predictions is not None and len(claim_predictions) != len(records):
        raise ValueError("claim_predictions and records must have the same length")
    if not records:
        return PilotMetricValue(
            name="evidence_reference_validity",
            value=None,
            count=0,
            note="no records",
            status="not_applicable",
        )
    valid = 0
    total = 0
    for index, record in enumerate(records):
        predictions = claim_predictions[index] if claim_predictions is not None else []
        predicted_claim_ids = {claim_id for claim_id, _ in predictions}
        for claim in record.target.claims:
            total += 1
            if claim.claim_id in predicted_claim_ids:
                valid += 1
    return PilotMetricValue(
        name="evidence_reference_validity",
        value=_safe_divide(valid, total),
        count=total,
        status="success",
    )


def pilot_abstention_precision_recall(
    predictions: Sequence[str],
    references: Sequence[str],
) -> tuple[PilotMetricValue, PilotMetricValue]:
    if len(predictions) != len(references):
        raise ValueError("predictions and references must have the same length")
    predicted_positives = sum(1 for prediction in predictions if prediction == "abstain")
    actual_positives = sum(1 for reference in references if reference == "abstain")
    true_positives = sum(
        1
        for prediction, reference in zip(predictions, references, strict=True)
        if prediction == "abstain" and reference == "abstain"
    )
    precision = _safe_divide(true_positives, predicted_positives)
    recall = _safe_divide(true_positives, actual_positives)
    return (
        PilotMetricValue(
            name="abstention_precision",
            value=precision,
            count=len(predictions),
        ),
        PilotMetricValue(
            name="abstention_recall",
            value=recall,
            count=len(predictions),
        ),
    )


def pilot_supported_claim_metrics(
    records: Sequence[PilotRecord],
    claim_predictions: Sequence[Sequence[tuple[str, tuple[str, ...]]]],
) -> tuple[PilotMetricValue, PilotMetricValue, PilotMetricValue]:
    if len(claim_predictions) != len(records):
        raise ValueError("claim_predictions and records must have the same length")
    if not records:
        return (
            PilotMetricValue(
                name="supported_claim_precision", value=None, count=0, note="no examples"
            ),
            PilotMetricValue(
                name="supported_claim_recall", value=None, count=0, note="no examples"
            ),
            PilotMetricValue(
                name="unsupported_claim_rate", value=None, count=0, note="no examples"
            ),
        )
    true_positives = 0
    predicted_positives = 0
    actual_positives = 0
    unsupported_claims = 0
    total_claims = 0
    for record, predicted_claims in zip(records, claim_predictions, strict=True):
        gold_claims = {
            (claim.claim_id, tuple(claim.evidence_ids)) for claim in record.target.claims
        }
        predicted_set = set(predicted_claims)
        actual_positives += len(gold_claims)
        predicted_positives += len(predicted_set)
        true_positives += len(gold_claims & predicted_set)
        for _, evidence_ids in predicted_set:
            total_claims += 1
            if not evidence_ids:
                unsupported_claims += 1
    precision = _safe_divide(true_positives, predicted_positives)
    recall = _safe_divide(true_positives, actual_positives)
    unsupported_rate = _safe_divide(unsupported_claims, total_claims)
    return (
        PilotMetricValue(name="supported_claim_precision", value=precision, count=total_claims),
        PilotMetricValue(name="supported_claim_recall", value=recall, count=total_claims),
        PilotMetricValue(name="unsupported_claim_rate", value=unsupported_rate, count=total_claims),
    )


def pilot_aggregate_counts(records: Sequence[PilotRecord]) -> dict[str, int]:
    counts = {
        "record_count": 0,
        "evidence_count": 0,
        "claim_count": 0,
        "abstain_count": 0,
        "synthetic_count": 0,
    }
    for record in records:
        counts["record_count"] += 1
        counts["evidence_count"] += len(record.evidence)
        counts["claim_count"] += len(record.target.claims)
        if record.target.abstain:
            counts["abstain_count"] += 1
        if record.provenance.synthetic:
            counts["synthetic_count"] += 1
    return counts
