"""Deterministic reference systems: the ceiling and the floor every run is read against.

A benchmark never ships bare (releases/benchmark_publication.md): ``GoldOracle`` replays
the human gold (must score 1.0 on accuracy metrics — a scorer sanity anchor), and
``EmptySystem`` returns nothing (the floor under the documented empty-set conventions).
Neither is a model; both are part of the benchmark's own verification.
"""

from __future__ import annotations

from medscale.bench.spec import TaskType
from medscale.bench.tasks import Statement, TaskItem, TaskOutput
from medscale.modelkit.interfaces import ModelRef
from medscale.research.index import ResearchIndex

__all__ = ["EmptySystem", "GoldOracle"]


class GoldOracle:
    """Replays the human gold: the reproducibility ceiling, not a competitor."""

    @property
    def system(self) -> ModelRef:
        return ModelRef(model_id="gold-oracle", backend="reference")

    def solve(self, item: TaskItem, index: ResearchIndex) -> TaskOutput:
        if item.task_type is TaskType.EVIDENCE_RETRIEVAL:
            return TaskOutput(retrieved_ids=item.gold.relevant_evidence_ids)
        if item.task_type is TaskType.EVIDENCE_GROUNDING:
            return TaskOutput(
                supporting_ids=item.gold.supporting_evidence_ids,
                contradicting_ids=item.gold.contradicting_evidence_ids,
            )
        statements = tuple(
            Statement(text=f"gold finding {evidence_id[:8]}", cited_evidence_ids=(evidence_id,))
            for evidence_id in item.gold.relevant_evidence_ids
        )
        return TaskOutput(statements=statements)


class EmptySystem:
    """Returns nothing everywhere: the floor of every metric under stated conventions."""

    @property
    def system(self) -> ModelRef:
        return ModelRef(model_id="empty-baseline", backend="reference")

    def solve(self, item: TaskItem, index: ResearchIndex) -> TaskOutput:
        return TaskOutput()
