"""Synthetic-fixture tests for the private P01-04B1 deterministic split core."""

from __future__ import annotations

import math
from collections.abc import Iterable
from pathlib import Path
from typing import cast

import pytest

from medscale.mesc._split_v1 import (
    ALGORITHM_VERSION,
    SPLIT_SEED,
    Decision,
    GroupAssignment,
    LabeledExample,
    LabelTarget,
    OrderedExampleRow,
    SourceLabelRow,
    SplitAllocationError,
    SplitInputError,
    allocate_indivisible_groups,
    canonical_json_bytes,
    constrained_apportionment,
    derive_example_id,
    join_labels,
    rank_groups,
    sha256_hexdigest,
    source_label_from_envelope,
)
from medscale.mesc.split import (
    PilotSplitNotAuthorizedError,
    SourceDocumentGroupedSplitter,
)


def _source_label(
    ordinal: int,
    *,
    decision: str = "yes",
    source_document_id: str | None = None,
) -> SourceLabelRow:
    assert decision in {"yes", "no", "maybe"}
    return SourceLabelRow(
        dataset_id="fixture/dataset",
        dataset_revision="fixture-revision",
        configuration="fixture-config",
        original_example_id=f"fixture-example-{ordinal}",
        source_document_id=source_document_id or f"fixture-document-{ordinal}",
        decision=cast(Decision, decision),
        source_record_hash=f"{ordinal + 1:064x}",
    )


def _ordered(ordinal: int, *, source_document_id: str | None = None) -> OrderedExampleRow:
    return OrderedExampleRow(
        original_example_id=f"fixture-example-{ordinal}",
        row_ordinal=ordinal,
        source_document_id=source_document_id or f"fixture-document-{ordinal}",
    )


def _joined(
    rows: Iterable[tuple[int, str, str]],
) -> tuple[LabeledExample, ...]:
    rows = tuple(rows)
    ordered = [
        _ordered(ordinal, source_document_id=source_document_id)
        for ordinal, source_document_id, _ in rows
    ]
    labels = [
        _source_label(
            ordinal,
            decision=decision,
            source_document_id=source_document_id,
        )
        for ordinal, source_document_id, decision in rows
    ]
    return join_labels(
        ordered,
        labels,
        transformation_version="fixture-transform/1",
    )


def _assignment_signature(
    assignments: tuple[GroupAssignment, ...],
) -> tuple[tuple[str, str, tuple[str, ...]], ...]:
    return tuple(
        (assignment.partition, assignment.source_document_id, assignment.example_ids)
        for assignment in assignments
    )


def test_canonical_json_bytes_are_exact_unicode_and_newline_free() -> None:
    assert canonical_json_bytes({"z": "café", "a": [2, 1]}) == (b'{"a":[2,1],"z":"caf\xc3\xa9"}')
    assert not canonical_json_bytes({"a": 1}).endswith(b"\n")
    with pytest.raises(ValueError, match="Out of range float values"):
        canonical_json_bytes({"not_finite": math.nan})


def test_example_id_uses_full_sha256_and_exact_payload() -> None:
    example_id = derive_example_id(
        dataset_id="fixture/dataset",
        dataset_revision="fixture-revision",
        configuration="fixture-config",
        original_example_id="fixture-example-0",
        source_document_id="fixture-document-0",
        transformation_version="fixture-transform/1",
    )
    assert example_id == (
        "mesc-pilot-01:a27d07b66aea852b7dfb26c12a6af9ec871518cc3771112a3ad75ba21e50e8bc"
    )
    assert len(example_id.removeprefix("mesc-pilot-01:")) == 64


def test_source_label_envelope_retains_only_identity_and_label() -> None:
    envelope: dict[str, object] = {
        "record": {
            "dataset_id": "fixture/dataset",
            "dataset_revision": "fixture-revision",
            "configuration": "fixture-config",
            "original_example_id": "fixture-example-0",
            "source_document_id": "fixture-document-0",
            "final_decision": "yes",
            "question": "content that must not cross the bridge",
            "long_answer": "content that must not cross the bridge",
        },
        "source_record_hash": "a" * 64,
    }
    row = source_label_from_envelope(envelope)
    assert row.decision == "yes"
    assert row.original_example_id == "fixture-example-0"
    assert not hasattr(row, "question")
    assert not hasattr(row, "long_answer")


@pytest.mark.parametrize(
    ("envelope", "message"),
    [
        ({}, "object field 'record'"),
        ({"record": {}}, "source_record_hash"),
        (
            {
                "record": {
                    "dataset_id": "d",
                    "dataset_revision": "r",
                    "configuration": "c",
                    "original_example_id": "e",
                    "source_document_id": "s",
                    "final_decision": "abstain",
                },
                "source_record_hash": "a" * 64,
            },
            "final_decision",
        ),
    ],
)
def test_source_label_envelope_fails_closed(envelope: dict[str, object], message: str) -> None:
    with pytest.raises(SplitInputError, match=message):
        source_label_from_envelope(envelope)


def test_label_join_is_order_independent_and_sorted_by_ordinal() -> None:
    ordered = [_ordered(1), _ordered(0)]
    labels = [_source_label(1, decision="no"), _source_label(0)]
    forward = join_labels(
        ordered,
        labels,
        transformation_version="fixture-transform/1",
    )
    reverse = join_labels(
        list(reversed(ordered)),
        list(reversed(labels)),
        transformation_version="fixture-transform/1",
    )
    assert forward == reverse
    assert [example.row_ordinal for example in forward] == [0, 1]
    assert [example.decision for example in forward] == ["yes", "no"]


@pytest.mark.parametrize(
    ("ordered", "labels", "message"),
    [
        ([_ordered(0), _ordered(0)], [_source_label(0)], "duplicate ordered"),
        ([_ordered(0)], [_source_label(0), _source_label(0)], "duplicate source-label"),
        ([_ordered(0), _ordered(1)], [_source_label(0)], "missing"),
        ([_ordered(0)], [_source_label(0), _source_label(1)], "unexpected"),
        (
            [_ordered(0, source_document_id="registry-doc")],
            [_source_label(0, source_document_id="label-doc")],
            "source_document_id mismatch",
        ),
    ],
)
def test_label_join_rejects_duplicate_missing_unexpected_and_mismatched_rows(
    ordered: list[OrderedExampleRow], labels: list[SourceLabelRow], message: str
) -> None:
    with pytest.raises(SplitInputError, match=message):
        join_labels(
            ordered,
            labels,
            transformation_version="fixture-transform/1",
        )


def test_label_join_rejects_mixed_dataset_identities() -> None:
    second = _source_label(1)
    second = SourceLabelRow(
        dataset_id="other/dataset",
        dataset_revision=second.dataset_revision,
        configuration=second.configuration,
        original_example_id=second.original_example_id,
        source_document_id=second.source_document_id,
        decision=second.decision,
        source_record_hash=second.source_record_hash,
    )
    with pytest.raises(SplitInputError, match="inconsistent dataset identities"):
        join_labels(
            [_ordered(0), _ordered(1)],
            [_source_label(0), second],
            transformation_version="fixture-transform/1",
        )


def test_constrained_apportionment_matches_ratified_aggregate_matrix() -> None:
    targets = constrained_apportionment(
        {"yes": 552, "no": 338, "maybe": 110},
        {"train": 700, "validation": 150, "test": 150},
    )
    assert targets == (
        LabelTarget(decision="yes", train=386, validation=83, test=83),
        LabelTarget(decision="no", train=237, validation=50, test=51),
        LabelTarget(decision="maybe", train=77, validation=17, test=16),
    )
    assert sum(target.train for target in targets) == 700
    assert sum(target.validation for target in targets) == 150
    assert sum(target.test for target in targets) == 150


def test_apportionment_rejects_unknown_keys_and_inconsistent_totals() -> None:
    with pytest.raises(SplitInputError, match="keys must be exactly"):
        constrained_apportionment(
            {"yes": 1, "no": 1, "maybe": 1, "abstain": 1},
            {"train": 2, "validation": 1, "test": 1},
        )
    with pytest.raises(SplitInputError, match="equal and greater than zero"):
        constrained_apportionment(
            {"yes": 1, "no": 1, "maybe": 1},
            {"train": 1, "validation": 1, "test": 0},
        )


def test_group_ranking_uses_ratified_payload_and_is_order_independent() -> None:
    examples = _joined(
        [
            (0, "fixture-document-a", "yes"),
            (1, "fixture-document-b", "yes"),
            (2, "fixture-document-c", "no"),
        ]
    )
    forward = rank_groups(examples)
    reverse = rank_groups(tuple(reversed(examples)))
    assert forward == reverse
    for group in forward:
        assert group.partition_key == sha256_hexdigest(
            {
                "algorithm_version": ALGORITHM_VERSION,
                "seed": SPLIT_SEED,
                "source_document_id": group.source_document_id,
                "stratum": group.decision,
            }
        )
    assert list(forward) == sorted(
        forward,
        key=lambda group: (
            group.partition_key,
            group.source_document_id,
            min(group.row_ordinals),
        ),
    )


def test_multi_example_group_is_indivisible() -> None:
    examples = _joined(
        [
            (0, "yes-group", "yes"),
            (1, "yes-group", "yes"),
            (2, "no-group", "no"),
            (3, "no-group", "no"),
            (4, "maybe-group", "maybe"),
            (5, "maybe-group", "maybe"),
        ]
    )
    targets = (
        LabelTarget("yes", train=2, validation=0, test=0),
        LabelTarget("no", train=0, validation=2, test=0),
        LabelTarget("maybe", train=0, validation=0, test=2),
    )
    assignments = allocate_indivisible_groups(examples, targets)
    assert _assignment_signature(assignments) == (
        ("train", "yes-group", assignments[0].example_ids),
        ("validation", "no-group", assignments[1].example_ids),
        ("test", "maybe-group", assignments[2].example_ids),
    )
    assert all(len(assignment.example_ids) == 2 for assignment in assignments)
    assert allocate_indivisible_groups(tuple(reversed(examples)), targets) == assignments


def test_group_crossing_target_boundary_fails_closed() -> None:
    examples = _joined(
        [
            (0, "yes-group", "yes"),
            (1, "yes-group", "yes"),
            (2, "no-group", "no"),
            (3, "maybe-group", "maybe"),
        ]
    )
    targets = (
        LabelTarget("yes", train=1, validation=1, test=0),
        LabelTarget("no", train=1, validation=0, test=0),
        LabelTarget("maybe", train=1, validation=0, test=0),
    )
    with pytest.raises(SplitAllocationError, match="would cross"):
        allocate_indivisible_groups(examples, targets)


def test_group_with_multiple_decisions_fails_closed() -> None:
    examples = _joined(
        [
            (0, "mixed-group", "yes"),
            (1, "mixed-group", "no"),
            (2, "maybe-group", "maybe"),
        ]
    )
    with pytest.raises(SplitInputError, match="crosses decision strata"):
        rank_groups(examples)


def test_private_core_writes_no_artifacts(tmp_path: Path) -> None:
    # The API is value-only: exercising all stages cannot name or mutate a path.
    examples = _joined(
        [
            (0, "yes-doc", "yes"),
            (1, "no-doc", "no"),
            (2, "maybe-doc", "maybe"),
        ]
    )
    targets = (
        LabelTarget("yes", 1, 0, 0),
        LabelTarget("no", 0, 1, 0),
        LabelTarget("maybe", 0, 0, 1),
    )
    allocate_indivisible_groups(examples, targets)
    assert list(tmp_path.iterdir()) == []


def test_public_splitter_remains_fail_closed() -> None:
    with pytest.raises(PilotSplitNotAuthorizedError, match="P01-04B"):
        SourceDocumentGroupedSplitter().assign(["fixture"], ["fixture-document"])


@pytest.mark.parametrize(
    ("value",),
    [
        (True,),
        (False,),
        (0.5,),
        (1.0,),
        ("1",),
        (None,),
        (-1,),
    ],
)
def test_join_labels_rejects_non_integer_row_ordinals(value: object) -> None:
    valid = _ordered(0, source_document_id="doc")
    invalid = OrderedExampleRow(
        original_example_id="fixture-example-1",
        row_ordinal=value,
        source_document_id="doc",
    )
    labels = [_source_label(0), _source_label(1)]
    with pytest.raises(SplitInputError, match="row_ordinal"):
        join_labels(
            [valid, invalid],
            labels,
            transformation_version="fixture-transform/1",
        )


@pytest.mark.parametrize(
    ("value",),
    [
        (True,),
        (False,),
        (0.5,),
        (1.0,),
        ("1",),
        (None,),
        (-1,),
    ],
)
def test_rank_groups_rejects_non_integer_labeled_example_ordinals(value: object) -> None:
    examples = (
        LabeledExample(
            example_id="mesc-pilot-01:" + "a0" * 32,
            original_example_id="fixture-example-0",
            source_document_id="doc",
            row_ordinal=value,
            decision="yes",
        ),
    )
    with pytest.raises(SplitInputError, match="row_ordinal"):
        rank_groups(examples)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("train", True),
        ("train", False),
        ("train", 0.5),
        ("train", 1.0),
        ("train", "1"),
        ("train", None),
        ("train", -1),
        ("validation", True),
        ("validation", 0.5),
        ("test", 1.0),
        ("test", "1"),
        ("test", None),
        ("test", -1),
    ],
)
def test_constrained_apportionment_rejects_non_integer_targets(field: str, value: object) -> None:
    targets = {
        "yes": 1,
        "no": 1,
        "maybe": 1,
    }
    partitions = {
        "train": 1,
        "validation": 1,
        "test": 1,
    }
    partitions[field] = value
    with pytest.raises(SplitInputError, match="non-negative integer"):
        constrained_apportionment(targets, partitions)


def test_non_negative_integers_accept_zero_and_positive_across_entrypoints() -> None:
    # row_ordinals and labeled-example ordinals
    examples = _joined(
        [
            (0, "doc", "yes"),
            (1, "doc", "yes"),
        ]
    )
    assert rank_groups(examples)

    # valid zero/positive partition targets execute without raising.
    constrained_apportionment(
        {"yes": 2, "no": 2, "maybe": 2},
        {"train": 2, "validation": 2, "test": 2},
    )
