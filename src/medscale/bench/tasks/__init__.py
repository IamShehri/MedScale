"""Task items, gold evidence sets, and the model-agnostic output contract.

Gold is never generated text: it is human-validated evidence references with annotator
attribution and a human-assigned confidence. The ``TaskOutput`` contract is what any
evaluated system must produce — id references and cited statements — so scorers never
inspect model internals and models never shape the benchmark.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass
from typing import Any, Final

from medscale.bench.spec import IMPLEMENTED_TASK_TYPES, TaskType
from medscale.provenance import validate_timestamp

__all__ = [
    "BaseBenchmarkTask",
    "GoldConfidence",
    "GoldEvidenceSet",
    "Statement",
    "TaskItem",
    "TaskOutput",
]

_TASK_ID: Final = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class BaseBenchmarkTask:
    seed: int
    version: str
    metadata: dict[str, str]

    def build(self, *, seed: int, context: dict[str, Any]) -> TaskItem:
        raise NotImplementedError


class GoldConfidence(enum.Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


def _sorted_ids(ids: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(ids)))


@dataclass(frozen=True)
class GoldEvidenceSet:
    """Human-validated answer: evidence references, never prose."""

    relevant_evidence_ids: tuple[str, ...] = ()
    supporting_evidence_ids: tuple[str, ...] = ()
    contradicting_evidence_ids: tuple[str, ...] = ()
    confidence: GoldConfidence = GoldConfidence.HIGH
    annotator: str = ""
    decided_at: str = ""

    def __post_init__(self) -> None:
        for name in (
            "relevant_evidence_ids",
            "supporting_evidence_ids",
            "contradicting_evidence_ids",
        ):
            object.__setattr__(self, name, _sorted_ids(getattr(self, name)))
        if not self.annotator.strip():
            raise ValueError(
                "gold requires an annotator (undocumented human decisions are invalid)"
            )
        validate_timestamp(self.decided_at, "decided_at")
        overlap = set(self.supporting_evidence_ids) & set(self.contradicting_evidence_ids)
        if overlap:
            raise ValueError(f"evidence cannot both support and contradict: {sorted(overlap)}")

    @property
    def all_ids(self) -> frozenset[str]:
        return frozenset(
            self.relevant_evidence_ids
            + self.supporting_evidence_ids
            + self.contradicting_evidence_ids
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "relevant_evidence_ids": list(self.relevant_evidence_ids),
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "contradicting_evidence_ids": list(self.contradicting_evidence_ids),
            "confidence": self.confidence.value,
            "annotator": self.annotator,
            "decided_at": self.decided_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GoldEvidenceSet:
        return cls(
            relevant_evidence_ids=tuple(data.get("relevant_evidence_ids", [])),
            supporting_evidence_ids=tuple(data.get("supporting_evidence_ids", [])),
            contradicting_evidence_ids=tuple(data.get("contradicting_evidence_ids", [])),
            confidence=GoldConfidence(data.get("confidence", "high")),
            annotator=data["annotator"],
            decided_at=data["decided_at"],
        )


@dataclass(frozen=True)
class TaskItem:
    """One benchmark task: input + human gold, typed by task category."""

    task_id: str
    task_type: TaskType
    input_text: str
    gold: GoldEvidenceSet
    input_evidence_ids: tuple[str, ...] = ()  # summarization: the objects handed to the system

    def __post_init__(self) -> None:
        if not _TASK_ID.match(self.task_id):
            raise ValueError(f"task_id must be kebab-case, got {self.task_id!r}")
        if self.task_type not in IMPLEMENTED_TASK_TYPES:
            raise ValueError(
                f"task_type {self.task_type.value!r} is a reserved extension point, "
                "not yet implementable"
            )
        if not self.input_text.strip():
            raise ValueError("input_text must be non-empty")
        object.__setattr__(self, "input_evidence_ids", _sorted_ids(self.input_evidence_ids))
        if self.task_type is TaskType.EVIDENCE_RETRIEVAL and not self.gold.relevant_evidence_ids:
            raise ValueError("retrieval gold requires relevant_evidence_ids")
        if self.task_type is TaskType.EVIDENCE_GROUNDING and not (
            self.gold.supporting_evidence_ids or self.gold.contradicting_evidence_ids
        ):
            raise ValueError("grounding gold requires supporting or contradicting ids")
        if self.task_type is TaskType.EVIDENCE_SUMMARIZATION:
            if not self.input_evidence_ids:
                raise ValueError("summarization requires input_evidence_ids")
            if not self.gold.relevant_evidence_ids:
                raise ValueError("summarization gold requires must-cover relevant_evidence_ids")

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "input_text": self.input_text,
            "input_evidence_ids": list(self.input_evidence_ids),
            "gold": self.gold.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaskItem:
        return cls(
            task_id=data["task_id"],
            task_type=TaskType(data["task_type"]),
            input_text=data["input_text"],
            gold=GoldEvidenceSet.from_dict(data["gold"]),
            input_evidence_ids=tuple(data.get("input_evidence_ids", [])),
        )


@dataclass(frozen=True)
class Statement:
    """One summary statement with its evidence citations."""

    text: str
    cited_evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("statement text must be non-empty")
        object.__setattr__(self, "cited_evidence_ids", _sorted_ids(self.cited_evidence_ids))

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "cited_evidence_ids": list(self.cited_evidence_ids)}


@dataclass(frozen=True)
class TaskOutput:
    """What an evaluated system returns for one item — references, never free claims."""

    retrieved_ids: tuple[str, ...] = ()
    supporting_ids: tuple[str, ...] = ()
    contradicting_ids: tuple[str, ...] = ()
    statements: tuple[Statement, ...] = ()

    def __post_init__(self) -> None:
        for name in ("retrieved_ids", "supporting_ids", "contradicting_ids"):
            object.__setattr__(self, name, _sorted_ids(getattr(self, name)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "retrieved_ids": list(self.retrieved_ids),
            "supporting_ids": list(self.supporting_ids),
            "contradicting_ids": list(self.contradicting_ids),
            "statements": [statement.to_dict() for statement in self.statements],
        }
