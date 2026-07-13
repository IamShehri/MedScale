"""Task 002 — Evidence Extraction.

Deterministic grounding task: claim support and contradiction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from medscale.bench.spec import TaskType
from medscale.bench.tasks import BaseBenchmarkTask, GoldEvidenceSet, TaskItem


@dataclass(frozen=True)
class Task002EvidenceExtraction(BaseBenchmarkTask):
    task_id: str = "task-002-evidence-extraction"
    task_type: TaskType = TaskType.EVIDENCE_GROUNDING
    version: str = "1.0.0"
    seed: int = 202
    metadata: dict[str, str] = field(
        default_factory=lambda: {
            "category": "grounding",
            "description": (
                "Extract supporting and contradicting evidence for a constrained"
                " decoding claim."
            ),
        }
    )

    def build(self, *, seed: int, context: dict[str, Any]) -> TaskItem:
        support_id = f"syn-eo-{seed:06d}-a"
        contra_id = f"syn-eo-{seed:06d}-b"
        return TaskItem(
            task_id=self.task_id,
            task_type=self.task_type,
            input_text=(
                "Constrained decoding improves validity; identify supporting"
                " and contradicting evidence."
            ),
            gold=GoldEvidenceSet(
                supporting_evidence_ids=(support_id,),
                contradicting_evidence_ids=(contra_id,),
                annotator="synthetic",
                decided_at="2026-07-13T00:00:00+00:00",
            ),
        )
