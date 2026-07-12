"""Task 003 — Screening Prioritization.

Deterministic summarization task: coverage of must-cite evidence in prioritization output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from medscale.bench.spec import TaskType
from medscale.bench.tasks import BaseBenchmarkTask, GoldEvidenceSet, Statement, TaskItem


@dataclass(frozen=True)
class Task003ScreeningPrioritization(BaseBenchmarkTask):
    task_id: str = "task-003-screening-prioritization"
    task_type: TaskType = TaskType.EVIDENCE_SUMMARIZATION
    version: str = "1.0.0"
    seed: int = 303
    metadata: dict[str, str] = field(
        default_factory=lambda: {
            "category": "summarization",
            "description": "Prioritize screening queue with required citations from a synthetic evidence set.",
        }
    )

    def build(self, *, seed: int, context: dict[str, Any]) -> TaskItem:
        prefix = f"syn-eo-{seed:06d}"
        ids = (f"{prefix}-1", f"{prefix}-2")
        statements = tuple(
            Statement(text=f"Priority finding {idx}", cited_evidence_ids=(evidence_id,))
            for idx, evidence_id in enumerate(ids, start=1)
        )
        return TaskItem(
            task_id=self.task_id,
            task_type=self.task_type,
            input_text="Summarize the top screening priorities from the provided evidence.",
            input_evidence_ids=ids,
            gold=GoldEvidenceSet(
                relevant_evidence_ids=ids,
                annotator="synthetic",
                decided_at="2026-07-13T00:00:00+00:00",
            ),
            statements=statements,
        )
