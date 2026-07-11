"""Benchmark specification: the versioned, snapshot-bound contract.

A spec is invalid without a frozen knowledge state: ``snapshot_id`` names the Research
Snapshot every task and gold answer was authored against. ``spec_id`` is a content hash
of the scientific definition, so any change to objective, tasks, or scoring rules is a
new identity — moving goalposts is structurally visible.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import Any, Final

from medscale.evidence import VerificationState
from medscale.reproducibility import content_hash

__all__ = ["BenchmarkSpec", "TaskType"]

_ID: Final = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_VERSION: Final = re.compile(r"^\d+\.\d+$")
_SHA256: Final = re.compile(r"^[0-9a-f]{64}$")


class TaskType(enum.Enum):
    EVIDENCE_RETRIEVAL = "evidence_retrieval"
    EVIDENCE_GROUNDING = "evidence_grounding"
    EVIDENCE_SUMMARIZATION = "evidence_summarization"
    #: Reserved extension point (directive 2D): defined so the vocabulary is stable,
    #: but validation rejects items of this type until its own directive lands.
    CLINICAL_REASONING = "clinical_reasoning"


#: Task types items may actually use today.
IMPLEMENTED_TASK_TYPES: Final = frozenset(
    {
        TaskType.EVIDENCE_RETRIEVAL,
        TaskType.EVIDENCE_GROUNDING,
        TaskType.EVIDENCE_SUMMARIZATION,
    }
)


@dataclass(frozen=True)
class BenchmarkSpec:
    """The scientific contract of one benchmark version."""

    benchmark_id: str
    version: str
    description: str
    scientific_objective: str
    snapshot_id: str
    min_verification: VerificationState = VerificationState.SOURCE_VERIFIED
    task_types: tuple[TaskType, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not _ID.match(self.benchmark_id):
            raise ValueError(f"benchmark_id must be kebab-case, got {self.benchmark_id!r}")
        if not _VERSION.match(self.version):
            raise ValueError(f"version must be MAJOR.MINOR, got {self.version!r}")
        if not self.description.strip() or not self.scientific_objective.strip():
            raise ValueError("description and scientific_objective must be non-empty")
        if not _SHA256.match(self.snapshot_id):
            raise ValueError("snapshot_id must be a 64-hex Research Snapshot identity")
        if not self.task_types:
            raise ValueError("a benchmark must declare at least one task type")

    @property
    def spec_id(self) -> str:
        """Content identity of the scientific definition."""
        return content_hash(
            {
                "benchmark_id": self.benchmark_id,
                "version": self.version,
                "description": self.description,
                "scientific_objective": self.scientific_objective,
                "snapshot_id": self.snapshot_id,
                "min_verification": self.min_verification.value,
                "task_types": [t.value for t in self.task_types],
                "metadata": dict(sorted(self.metadata.items())),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "spec_id": self.spec_id,
            "benchmark_id": self.benchmark_id,
            "version": self.version,
            "description": self.description,
            "scientific_objective": self.scientific_objective,
            "snapshot_id": self.snapshot_id,
            "min_verification": self.min_verification.value,
            "task_types": [t.value for t in self.task_types],
            "metadata": dict(sorted(self.metadata.items())),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BenchmarkSpec:
        spec = cls(
            benchmark_id=data["benchmark_id"],
            version=data["version"],
            description=data["description"],
            scientific_objective=data["scientific_objective"],
            snapshot_id=data["snapshot_id"],
            min_verification=VerificationState(data["min_verification"]),
            task_types=tuple(TaskType(t) for t in data["task_types"]),
            metadata=dict(data.get("metadata", {})),
        )
        stored = data.get("spec_id")
        if stored is not None and stored != spec.spec_id:
            raise ValueError(
                f"spec file id {stored[:12]}... does not match recomputed identity "
                f"{spec.spec_id[:12]}... (spec tampered or hand-edited)"
            )
        return spec
