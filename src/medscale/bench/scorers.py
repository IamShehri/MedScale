"""Deterministic scoring engine. No ML, no embeddings, no LLM judging — ever.

Conventions are explicit because hidden evaluator logic makes benchmarks meaningless:

- set precision = |pred ∩ gold| / |pred|; empty pred scores 1.0 iff gold is also empty,
  else 0.0 (predicting nothing when something exists is a miss, not a free pass);
- set recall (= coverage) mirrors precision with roles swapped;
- all rates rounded to 6 decimals — a documented transformation;
- ``provenance_completeness`` measures whether cited ids exist in the frozen evidence
  store at all (integrity), independent of whether they match gold (accuracy).

``SCORER_VERSION`` is recorded in every run artifact; any change to these formulas is a
benchmark-MAJOR event (releases/benchmark_publication.md).
"""

from __future__ import annotations

from typing import Final

from medscale.bench.spec import TaskType
from medscale.bench.tasks import TaskItem, TaskOutput

__all__ = ["SCORER_VERSION", "score_item", "set_precision", "set_recall"]

SCORER_VERSION: Final = "1"


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 1.0


def set_precision(predicted: frozenset[str], gold: frozenset[str]) -> float:
    if not predicted:
        return 1.0 if not gold else 0.0
    return _rate(len(predicted & gold), len(predicted))


def set_recall(predicted: frozenset[str], gold: frozenset[str]) -> float:
    if not gold:
        return 1.0 if not predicted else 0.0
    return _rate(len(predicted & gold), len(gold))


def _f1(precision: float, recall: float) -> float:
    return round(2 * precision * recall / (precision + recall), 6) if precision + recall else 0.0


def _score_retrieval(item: TaskItem, output: TaskOutput) -> dict[str, float]:
    predicted = frozenset(output.retrieved_ids)
    gold = frozenset(item.gold.relevant_evidence_ids)
    precision = set_precision(predicted, gold)
    recall = set_recall(predicted, gold)
    return {
        "precision": precision,
        "recall": recall,
        "f1": _f1(precision, recall),
        "evidence_coverage": recall,
    }


def _score_grounding(item: TaskItem, output: TaskOutput) -> dict[str, float]:
    pred_support = frozenset(output.supporting_ids)
    pred_contra = frozenset(output.contradicting_ids)
    gold_support = frozenset(item.gold.supporting_evidence_ids)
    gold_contra = frozenset(item.gold.contradicting_evidence_ids)
    citation_accuracy = set_precision(pred_support, gold_support)
    support_recall = set_recall(pred_support, gold_support)
    return {
        "citation_accuracy": citation_accuracy,
        "support_recall": support_recall,
        "support_f1": _f1(citation_accuracy, support_recall),
        "contradiction_precision": set_precision(pred_contra, gold_contra),
        "contradiction_recall": set_recall(pred_contra, gold_contra),
    }


def _score_summarization(item: TaskItem, output: TaskOutput) -> dict[str, float]:
    must_cover = frozenset(item.gold.relevant_evidence_ids)
    allowed = frozenset(item.input_evidence_ids)
    cited = frozenset(
        evidence_id
        for statement in output.statements
        for evidence_id in statement.cited_evidence_ids
    )
    covered = len(must_cover & cited)
    unsupported = sum(
        1
        for statement in output.statements
        if not statement.cited_evidence_ids or not set(statement.cited_evidence_ids) <= allowed
    )
    return {
        "factual_completeness": _rate(covered, len(must_cover)),
        "unsupported_statement_rate": (
            round(unsupported / len(output.statements), 6) if output.statements else 0.0
        ),
    }


def provenance_completeness(output: TaskOutput, known_evidence_ids: frozenset[str]) -> float:
    """Fraction of every cited/predicted id that resolves in the frozen evidence store."""
    cited: set[str] = (
        set(output.retrieved_ids) | set(output.supporting_ids) | set(output.contradicting_ids)
    )
    for statement in output.statements:
        cited.update(statement.cited_evidence_ids)
    if not cited:
        return 1.0
    return _rate(len(cited & known_evidence_ids), len(cited))


def score_item(
    item: TaskItem, output: TaskOutput, known_evidence_ids: frozenset[str]
) -> dict[str, float]:
    """Deterministic per-item metrics for the item's task type + integrity metric."""
    if item.task_type is TaskType.EVIDENCE_RETRIEVAL:
        metrics = _score_retrieval(item, output)
    elif item.task_type is TaskType.EVIDENCE_GROUNDING:
        metrics = _score_grounding(item, output)
    elif item.task_type is TaskType.EVIDENCE_SUMMARIZATION:
        metrics = _score_summarization(item, output)
    else:  # pragma: no cover - constructor forbids reserved types
        raise ValueError(f"unscorable task type: {item.task_type}")
    metrics["provenance_completeness"] = provenance_completeness(output, known_evidence_ids)
    return metrics
