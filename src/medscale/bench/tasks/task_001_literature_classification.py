"""Task 001 — Literature Classification.

Deterministic retrieval task: evidence-grounded relevance for literature classification
queries about constrained decoding validity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from medscale.bench.spec import TaskType
from medscale.bench.tasks import BaseBenchmarkTask, GoldEvidenceSet, TaskItem


@dataclass(frozen=True)
class Task001LiteratureClassification(BaseBenchmarkTask):
    task_id: str = "task-001-literature-classification"
    task_type: TaskType = TaskType.EVIDENCE_RETRIEVAL
    version: str = "1.0.0"
    seed: int = 101
    metadata: dict[str, str] = field(
        default_factory=lambda: {
            "category": "retrieval",
            "description": "Evidence-grounded retrieval for constrained decoding validity literature classification.",
        }
    )

    def build(self, *, seed: int, context: dict[str, Any]) -> TaskItem:
        evidence_id = f"syn-eo-{seed:06d}-001"
        return TaskItem(
            task_id=self.task_id,
            task_type=self.task_type,
            input_text="Does constrained decoding improve classifier validity under distribution shift?",
            gold=GoldEvidenceSet(
                relevant_evidence_ids=(evidence_id,),
                annotator="synthetic",
                decided_at="2026-07-13T00:00:00+00:00",
            ),
        )
