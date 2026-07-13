"""Benchmark task contracts: frozen dataclass invariants, serialization, round-trip."""

from __future__ import annotations

from typing import Any

import pytest

from medscale.bench.spec import TaskType
from medscale.bench.tasks import (
    BaseBenchmarkTask,
    GoldConfidence,
    GoldEvidenceSet,
    Statement,
    TaskItem,
    TaskOutput,
)


class DummyTask(BaseBenchmarkTask):
    version = "1.0.0"
    seed = 1

    def build(self, *, seed: int, context: dict[str, Any]) -> TaskItem:
        return TaskItem(
            task_id="dummy",
            task_type=TaskType.EVIDENCE_GROUNDING,
            input_text="dummy",
            input_evidence_ids=(),
            gold=GoldEvidenceSet(
                supporting_evidence_ids=("syn-eo-dummy",),
                contradicting_evidence_ids=(),
                annotator="synthetic",
                decided_at="2026-07-13T00:00:00+00:00",
            ),
        )


def test_dummy_task_produces_item() -> None:
    task = DummyTask()
    item = task.build(seed=1, context={})
    assert item.task_id == "dummy"
    assert item.task_type is TaskType.EVIDENCE_GROUNDING
    assert item.gold.annotator == "synthetic"
    assert item.gold.supporting_evidence_ids == ("syn-eo-dummy",)


_TS = "2026-07-13T00:00:00+00:00"


def test_task_item_validates_kebab_case_id() -> None:
    with pytest.raises(ValueError, match="kebab-case"):
        TaskItem(
            task_id="InvalidCamel",
            task_type=TaskType.EVIDENCE_GROUNDING,
            input_text="t",
            gold=GoldEvidenceSet(
                supporting_evidence_ids=("x",),
                contradicting_evidence_ids=(),
                annotator="op",
                decided_at=_TS,
            ),
        )


def test_task_item_validates_non_empty_input() -> None:
    with pytest.raises(ValueError, match="input_text must be non-empty"):
        TaskItem(
            task_id="ok-id",
            task_type=TaskType.EVIDENCE_GROUNDING,
            input_text="   ",
            gold=GoldEvidenceSet(
                supporting_evidence_ids=("x",),
                contradicting_evidence_ids=(),
                annotator="op",
                decided_at=_TS,
            ),
        )


def test_task_item_retrieval_requires_relevant_ids() -> None:
    with pytest.raises(ValueError, match="retrieval gold requires relevant_evidence_ids"):
        TaskItem(
            task_id="ok-id",
            task_type=TaskType.EVIDENCE_RETRIEVAL,
            input_text="q",
            gold=GoldEvidenceSet(
                relevant_evidence_ids=(),
                annotator="op",
                decided_at=_TS,
            ),
        )


def test_task_item_grounding_requires_support_or_contradict() -> None:
    with pytest.raises(ValueError, match="grounding gold requires supporting or contradicting ids"):
        TaskItem(
            task_id="ok-id",
            task_type=TaskType.EVIDENCE_GROUNDING,
            input_text="q",
            gold=GoldEvidenceSet(
                relevant_evidence_ids=("x",),
                annotator="op",
                decided_at=_TS,
            ),
        )


def test_task_item_summarization_requires_input_evidence_and_relevant_ids() -> None:
    with pytest.raises(ValueError, match="summarization requires input_evidence_ids"):
        TaskItem(
            task_id="ok-id",
            task_type=TaskType.EVIDENCE_SUMMARIZATION,
            input_text="q",
            input_evidence_ids=(),
            gold=GoldEvidenceSet(
                relevant_evidence_ids=("x",),
                annotator="op",
                decided_at=_TS,
            ),
        )
    with pytest.raises(
        ValueError,
        match="summarization gold requires must-cover relevant_evidence_ids",
    ):
        TaskItem(
            task_id="ok-id",
            task_type=TaskType.EVIDENCE_SUMMARIZATION,
            input_text="q",
            input_evidence_ids=("x",),
            gold=GoldEvidenceSet(
                relevant_evidence_ids=(),
                annotator="op",
                decided_at=_TS,
            ),
        )


def test_gold_evidence_set_rejects_empty_annotator() -> None:
    with pytest.raises(ValueError, match="annotator"):
        GoldEvidenceSet(
            relevant_evidence_ids=("x",),
            annotator="   ",
            decided_at=_TS,
        )


def test_gold_evidence_set_rejects_contradiction_overlap() -> None:
    with pytest.raises(ValueError, match="both support and contradict"):
        GoldEvidenceSet(
            supporting_evidence_ids=("x",),
            contradicting_evidence_ids=("x",),
            annotator="op",
            decided_at=_TS,
        )


def test_gold_evidence_set_round_trip() -> None:
    gold = GoldEvidenceSet(
        relevant_evidence_ids=("b", "a", "c"),
        supporting_evidence_ids=("s",),
        contradicting_evidence_ids=(),
        confidence=GoldConfidence.MODERATE,
        annotator="annotator",
        decided_at=_TS,
    )
    data = gold.to_dict()
    assert data["relevant_evidence_ids"] == ["a", "b", "c"]
    assert data["supporting_evidence_ids"] == ["s"]
    assert GoldEvidenceSet.from_dict(data) == gold


def test_task_item_round_trip() -> None:
    item = TaskItem(
        task_id="sort-inputs",
        task_type=TaskType.EVIDENCE_GROUNDING,
        input_text="t",
        input_evidence_ids=("c", "a", "b"),
        gold=GoldEvidenceSet(
            supporting_evidence_ids=("s",),
            contradicting_evidence_ids=(),
            annotator="op",
            decided_at=_TS,
        ),
    )
    data = item.to_dict()
    restored = TaskItem.from_dict(data)
    assert restored == item
    assert restored.input_evidence_ids == ("a", "b", "c")


def test_task_output_sorts_ids() -> None:
    output = TaskOutput(
        retrieved_ids=("b", "a"),
        supporting_ids=("z",),
        contradicting_ids=(),
        statements=(Statement("text", ("x", "y")),),
    )
    assert output.retrieved_ids == ("a", "b")
    assert output.statements[0].cited_evidence_ids == ("x", "y")
