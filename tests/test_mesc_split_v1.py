"""Synthetic-fixture tests for the private P01-04B1 deterministic split core.

The second half of this module qualifies the bounded private minimum-deviation
correction (FD-BMD-1 .. FD-BMD-14): that the accepted exact allocator is
preserved byte-for-byte, that the fallback is reachable only through the one
private typed ranked-boundary class, and that the resolver returns a proven
global optimum under both tie-breaks.
"""

from __future__ import annotations

import inspect
import math
from collections.abc import Iterable
from itertools import product
from pathlib import Path
from typing import cast

import pytest

from medscale import mesc as mesc_package
from medscale.mesc import _split_v1
from medscale.mesc._split_v1 import (
    _MINIMUM_DEVIATION_MAX_EXAMPLES,
    _MINIMUM_DEVIATION_MAX_GROUPS,
    ALGORITHM_VERSION,
    DECISIONS,
    PARTITIONS,
    SPLIT_SEED,
    Decision,
    GroupAssignment,
    LabeledExample,
    LabelTarget,
    OrderedExampleRow,
    SourceLabelRow,
    SplitAllocationError,
    SplitInputError,
    _allocate_indivisible_groups_with_minimum_deviation,
    _RankedBoundaryAllocationError,
    _resolve_minimum_deviation,
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


def test_boundary_crossing_message_is_byte_identical_to_the_accepted_literal() -> None:
    """The accepted crossing message is preserved verbatim (contract C-15)."""
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
    with pytest.raises(SplitAllocationError) as caught:
        allocate_indivisible_groups(examples, targets)
    assert str(caught.value) == (
        "group 'yes-group' of size 2 would cross the yes/train boundary with 1 places remaining"
    )
    assert isinstance(caught.value, _RankedBoundaryAllocationError)
    assert isinstance(caught.value, SplitAllocationError)


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
    _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    correction_examples, correction_targets = _minimum_deviation_case("unique-optimum")
    _allocate_indivisible_groups_with_minimum_deviation(correction_examples, correction_targets)
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
        row_ordinal=cast(int, value),
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
            row_ordinal=cast(int, value),
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
        ("validation", False),
        ("validation", 0.5),
        ("validation", 1.0),
        ("validation", "1"),
        ("validation", None),
        ("validation", -1),
        ("test", True),
        ("test", False),
        ("test", 0.5),
        ("test", 1.0),
        ("test", "1"),
        ("test", None),
        ("test", -1),
    ],
)
def test_allocate_indivisible_groups_rejects_non_integer_targets(field: str, value: object) -> None:
    examples = _joined(
        [
            (0, "doc", "yes"),
            (1, "doc", "no"),
            (2, "doc", "maybe"),
        ]
    )
    base_targets = {
        "yes": LabelTarget("yes", train=1, validation=0, test=0),
        "no": LabelTarget("no", train=0, validation=1, test=0),
        "maybe": LabelTarget("maybe", train=0, validation=0, test=1),
    }
    if field == "train":
        yes_target = LabelTarget("yes", cast(int, value), 0, 0)
    elif field == "validation":
        yes_target = LabelTarget("yes", 0, cast(int, value), 0)
    else:
        yes_target = LabelTarget("yes", 0, 0, cast(int, value))
    targets = (yes_target, base_targets["no"], base_targets["maybe"])
    with pytest.raises(SplitInputError, match=field):
        allocate_indivisible_groups(examples, targets)


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


# ===========================================================================
# Bounded private minimum-deviation correction (FD-BMD-1 .. FD-BMD-14)
# ===========================================================================

#: ``(name, (document, decision, size)..., (yes, no, maybe) targets)`` for every
#: tiny synthetic correction case.  Each one is small enough for the test-only
#: exhaustive oracle below.
_MINIMUM_DEVIATION_CASES: dict[
    str, tuple[tuple[tuple[str, str, int], ...], tuple[tuple[int, int, int], ...]]
] = {
    # One group of two examples against a train target of one: the exact target
    # is unreachable and exactly one feasible matrix attains the minimum.
    "unique-optimum": (
        (("y0", "yes", 2), ("n0", "no", 1), ("m0", "maybe", 1)),
        ((1, 1, 0), (1, 0, 0), (0, 0, 1)),
    ),
    # Two feasible matrices tie at the minimum score, so the nine-cell
    # lexicographic tie-break decides.
    "two-minimum-matrices": (
        (("ya", "yes", 2), ("yb", "yes", 2), ("n0", "no", 1), ("m0", "maybe", 1)),
        ((3, 1, 0), (1, 0, 0), (1, 0, 0)),
    ),
    # One minimum matrix is realized by two different assignments, so the
    # partition-code tie-break decides.
    "assignment-tie-break": (
        (("ya", "yes", 2), ("yb", "yes", 2), ("n0", "no", 1), ("m0", "maybe", 1)),
        ((3, 1, 0), (0, 1, 0), (0, 0, 1)),
    ),
    # A wider lattice with mixed group sizes, kept inside the oracle's reach.
    "mixed-group-sizes": (
        (
            ("ya", "yes", 3),
            ("yb", "yes", 2),
            ("n0", "no", 2),
            ("n1", "no", 1),
            ("m0", "maybe", 2),
        ),
        ((3, 1, 1), (2, 1, 0), (1, 0, 1)),
    ),
}


def _grouped(specification: Iterable[tuple[str, str, int]]) -> tuple[LabeledExample, ...]:
    """Build joined examples from ``(document, decision, size)`` triples."""
    rows: list[tuple[int, str, str]] = []
    ordinal = 0
    for document, decision, size in specification:
        for _ in range(size):
            rows.append((ordinal, document, decision))
            ordinal += 1
    return _joined(rows)


def _targets(values: tuple[tuple[int, int, int], ...]) -> tuple[LabelTarget, ...]:
    return tuple(
        LabelTarget(decision, *counts) for decision, counts in zip(DECISIONS, values, strict=True)
    )


def _minimum_deviation_case(
    name: str,
) -> tuple[tuple[LabeledExample, ...], tuple[LabelTarget, ...]]:
    specification, values = _MINIMUM_DEVIATION_CASES[name]
    return _grouped(specification), _targets(values)


def _actual_matrix(assignments: tuple[GroupAssignment, ...]) -> tuple[int, ...]:
    """Return the nine actual cells in the controlling FD-BMD-6 order."""
    counts = {(decision, partition): 0 for decision in DECISIONS for partition in PARTITIONS}
    for assignment in assignments:
        counts[(assignment.decision, assignment.partition)] += len(assignment.example_ids)
    return tuple(
        counts[(decision, partition)] for decision in DECISIONS for partition in PARTITIONS
    )


def _target_matrix(targets: tuple[LabelTarget, ...]) -> tuple[int, ...]:
    by_decision = {target.decision: target for target in targets}
    return tuple(
        by_decision[decision].for_partition(partition)
        for decision in DECISIONS
        for partition in PARTITIONS
    )


def _score(assignments: tuple[GroupAssignment, ...], targets: tuple[LabelTarget, ...]) -> int:
    return sum(
        (actual - target) ** 2
        for actual, target in zip(_actual_matrix(assignments), _target_matrix(targets), strict=True)
    )


def _ordered_groups(examples: tuple[LabeledExample, ...]) -> list[str]:
    """Return every source document in decision order, then ``rank_groups`` order."""
    ranked = rank_groups(examples)
    return [
        group.source_document_id
        for decision in DECISIONS
        for group in ranked
        if group.decision == decision
    ]


def _code_vector(
    examples: tuple[LabeledExample, ...], assignments: tuple[GroupAssignment, ...]
) -> tuple[int, ...]:
    """Return the canonical concatenated partition-code vector (FD-BMD-8)."""
    partition_by_document = {
        assignment.source_document_id: assignment.partition for assignment in assignments
    }
    return tuple(
        PARTITIONS.index(partition_by_document[document]) for document in _ordered_groups(examples)
    )


def _exhaustive_optimum(
    examples: tuple[LabeledExample, ...], targets: tuple[LabelTarget, ...]
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """TEST-ONLY brute-force oracle for tiny group counts.

    It enumerates every code vector, keeps the ones with exact partition totals
    (exact row totals hold structurally because a group never leaves its
    decision), and returns the minimum ``(score, matrix, codes)`` triple.  The
    triple comparison *is* the three-level tie-break.

    This oracle exists only in this test module, is never called by production
    code, is never run against the 500-group qualification fixture, and is not a
    replacement algorithm: it is exponential by construction and is hard-capped
    at eight groups.
    """
    ordered_documents = _ordered_groups(examples)
    assert len(ordered_documents) <= 8, "test-only oracle: tiny group counts only"
    sizes = {
        group.source_document_id: (group.decision, group.example_count)
        for group in rank_groups(examples)
    }
    target_matrix = _target_matrix(targets)
    partition_totals = [
        sum(target.for_partition(partition) for target in targets) for partition in PARTITIONS
    ]

    best: tuple[int, tuple[int, ...], tuple[int, ...]] | None = None
    for codes in product(range(3), repeat=len(ordered_documents)):
        cells = {(decision, partition): 0 for decision in DECISIONS for partition in PARTITIONS}
        totals = [0, 0, 0]
        for document, code in zip(ordered_documents, codes, strict=True):
            decision, size = sizes[document]
            cells[(decision, PARTITIONS[code])] += size
            totals[code] += size
        if totals != partition_totals:
            continue
        matrix = tuple(
            cells[(decision, partition)] for decision in DECISIONS for partition in PARTITIONS
        )
        score = sum(
            (actual - target) ** 2 for actual, target in zip(matrix, target_matrix, strict=True)
        )
        candidate = (score, matrix, codes)
        if best is None or candidate < best:
            best = candidate
    assert best is not None, "the oracle case must be feasible"
    return best


# -- exact allocator preservation -------------------------------------------


def test_the_private_subclass_is_a_split_allocation_error() -> None:
    assert issubclass(_RankedBoundaryAllocationError, SplitAllocationError)
    assert _RankedBoundaryAllocationError.__bases__ == (SplitAllocationError,)
    assert _RankedBoundaryAllocationError.__name__.startswith("_")


def test_the_correction_adds_no_public_or_re_exported_name() -> None:
    for name in (
        "_RankedBoundaryAllocationError",
        "_allocate_indivisible_groups_with_minimum_deviation",
        "_resolve_minimum_deviation",
    ):
        assert name not in mesc_package.__all__
        assert not hasattr(mesc_package, name)
    assert not any(name.startswith("_") for name in mesc_package.__all__)


def test_exactly_one_new_private_exception_class_exists() -> None:
    subclasses = [
        name
        for name, value in vars(_split_v1).items()
        if isinstance(value, type)
        and issubclass(value, SplitAllocationError)
        and value is not SplitAllocationError
    ]
    assert subclasses == ["_RankedBoundaryAllocationError"], (
        f"exactly one private SplitAllocationError subclass is authorized, found {subclasses}"
    )


def test_exact_feasible_allocation_is_returned_unchanged_by_the_resolver() -> None:
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
    accepted = allocate_indivisible_groups(examples, targets)
    assert _allocate_indivisible_groups_with_minimum_deviation(examples, targets) == accepted
    assert _assignment_signature(accepted) == (
        ("train", "yes-group", accepted[0].example_ids),
        ("validation", "no-group", accepted[1].example_ids),
        ("test", "maybe-group", accepted[2].example_ids),
    )


def test_a_non_boundary_allocation_failure_stays_the_base_error() -> None:
    """Only the ranked-boundary crossing carries the private subclass."""
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    targets = (
        LabelTarget("yes", train=2, validation=0, test=0),
        LabelTarget("no", train=0, validation=1, test=0),
        LabelTarget("maybe", train=0, validation=0, test=1),
    )
    with pytest.raises(SplitAllocationError) as caught:
        allocate_indivisible_groups(examples, targets)
    assert type(caught.value) is SplitAllocationError
    assert not isinstance(caught.value, _RankedBoundaryAllocationError)


# -- typed trigger isolation ------------------------------------------------


def test_the_exact_first_wrapper_wraps_only_the_accepted_allocator_call() -> None:
    """Structural proof of the FD-BMD-4 control flow and of NB-1."""
    source = inspect.getsource(_allocate_indivisible_groups_with_minimum_deviation)
    body = source.split('"""', 2)[2]
    guarded = body.split("try:", 1)[1].split("except", 1)[0]
    statements = [line.strip() for line in guarded.strip().splitlines() if line.strip()]
    assert statements == ["return allocate_indivisible_groups(examples, targets)"], (
        "the try must enclose the accepted exact-allocator call and nothing else"
    )
    assert "except _RankedBoundaryAllocationError:" in body
    assert "except SplitAllocationError" not in body
    assert "except Exception" not in body
    assert "except BaseException" not in body
    for token in ("str(", ".args", "startswith", "endswith", "re.", "match(", "search("):
        assert token not in body, f"fallback selection must not inspect {token!r}"


@pytest.mark.parametrize(
    "error",
    [
        SplitInputError("malformed input"),
        SplitAllocationError("observed/expected mismatch"),
        RuntimeError("unknown exception"),
        ValueError("unrelated value error"),
        KeyError("unrelated key error"),
    ],
)
def test_the_resolver_is_not_reached_for_any_non_boundary_error(
    monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    calls: list[int] = []

    def refuse(*args: object, **kwargs: object) -> object:
        calls.append(1)
        raise AssertionError("the minimum-deviation resolver must not be reached")

    def raise_error(*args: object, **kwargs: object) -> object:
        raise error

    monkeypatch.setattr(_split_v1, "_resolve_minimum_deviation", refuse)
    monkeypatch.setattr(_split_v1, "allocate_indivisible_groups", raise_error)
    with pytest.raises(type(error)):
        _allocate_indivisible_groups_with_minimum_deviation((), ())
    assert calls == []


def test_the_resolver_is_reached_only_for_the_private_boundary_subclass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []
    sentinel: tuple[GroupAssignment, ...] = ()

    def record(*args: object, **kwargs: object) -> tuple[GroupAssignment, ...]:
        calls.append(1)
        return sentinel

    def raise_boundary(*args: object, **kwargs: object) -> object:
        raise _RankedBoundaryAllocationError("would cross")

    monkeypatch.setattr(_split_v1, "_resolve_minimum_deviation", record)
    monkeypatch.setattr(_split_v1, "allocate_indivisible_groups", raise_boundary)
    assert _allocate_indivisible_groups_with_minimum_deviation((), ()) is sentinel
    assert calls == [1]


def test_a_resolver_refusal_propagates_without_re_entering_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The except clause does not enclose the resolver, so there is no recursion."""
    calls: list[int] = []

    def refuse(*args: object, **kwargs: object) -> object:
        calls.append(1)
        raise _RankedBoundaryAllocationError("bounded refusal")

    def raise_boundary(*args: object, **kwargs: object) -> object:
        raise _RankedBoundaryAllocationError("would cross")

    monkeypatch.setattr(_split_v1, "_resolve_minimum_deviation", refuse)
    monkeypatch.setattr(_split_v1, "allocate_indivisible_groups", raise_boundary)
    with pytest.raises(_RankedBoundaryAllocationError, match="bounded refusal"):
        _allocate_indivisible_groups_with_minimum_deviation((), ())
    assert calls == [1], "the resolver must run exactly once and never be retried"


def _spy_on_resolver(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    calls: list[int] = []

    def refuse(*args: object, **kwargs: object) -> object:
        calls.append(1)
        raise AssertionError("the minimum-deviation resolver must not be reached")

    monkeypatch.setattr(_split_v1, "_resolve_minimum_deviation", refuse)
    return calls


def test_invalid_target_keys_never_activate_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    targets = (
        LabelTarget("yes", 1, 0, 0),
        LabelTarget("no", 0, 1, 0),
    )
    with pytest.raises(SplitInputError, match="targets must contain exactly"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert calls == []


def test_a_duplicate_target_decision_never_activates_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    targets = (
        LabelTarget("yes", 1, 0, 0),
        LabelTarget("yes", 0, 1, 0),
        LabelTarget("no", 0, 1, 0),
        LabelTarget("maybe", 0, 0, 1),
    )
    with pytest.raises(SplitInputError, match="duplicate target decision"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert calls == []


def test_a_negative_target_value_never_activates_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    targets = (
        LabelTarget("yes", -1, 0, 0),
        LabelTarget("no", 0, 1, 0),
        LabelTarget("maybe", 0, 0, 1),
    )
    with pytest.raises(SplitInputError, match="train"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert calls == []


def test_a_decision_total_mismatch_never_activates_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    targets = (
        LabelTarget("yes", 2, 0, 0),
        LabelTarget("no", 0, 1, 0),
        LabelTarget("maybe", 0, 0, 1),
    )
    with pytest.raises(SplitAllocationError, match="target total for 'yes'"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert calls == []


def test_a_mixed_decision_group_never_activates_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    examples = _joined(
        [(0, "mixed-group", "yes"), (1, "mixed-group", "no"), (2, "maybe-doc", "maybe")]
    )
    targets = (
        LabelTarget("yes", 1, 0, 0),
        LabelTarget("no", 0, 1, 0),
        LabelTarget("maybe", 0, 0, 1),
    )
    with pytest.raises(SplitInputError, match="crosses decision strata"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert calls == []


def test_a_duplicate_identity_never_activates_the_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _spy_on_resolver(monkeypatch)
    example = LabeledExample(
        example_id="mesc-pilot-01:" + "a0" * 32,
        original_example_id="fixture-example-0",
        source_document_id="yes-doc",
        row_ordinal=0,
        decision="yes",
    )
    targets = (
        LabelTarget("yes", 2, 0, 0),
        LabelTarget("no", 0, 0, 0),
        LabelTarget("maybe", 0, 0, 0),
    )
    with pytest.raises(SplitInputError, match="duplicate example_id"):
        _allocate_indivisible_groups_with_minimum_deviation((example, example), targets)
    assert calls == []


def test_the_resolver_revalidates_its_targets_when_called_directly() -> None:
    """The resolver never trusts a caller that bypassed the exact allocator."""
    examples = _joined([(0, "yes-doc", "yes"), (1, "no-doc", "no"), (2, "maybe-doc", "maybe")])
    with pytest.raises(SplitInputError, match="duplicate target decision"):
        _resolve_minimum_deviation(
            examples,
            (
                LabelTarget("yes", 1, 0, 0),
                LabelTarget("yes", 0, 1, 0),
                LabelTarget("maybe", 0, 0, 1),
            ),
        )
    with pytest.raises(SplitInputError, match="targets must contain exactly"):
        _resolve_minimum_deviation(examples, (LabelTarget("yes", 1, 0, 0),))


# -- optimizer correctness --------------------------------------------------


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_exact_allocator_refuses_every_correction_case_at_a_boundary(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    with pytest.raises(_RankedBoundaryAllocationError, match="would cross"):
        allocate_indivisible_groups(examples, targets)


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_resolver_matches_the_test_only_exhaustive_oracle(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    score, matrix, codes = _exhaustive_optimum(examples, targets)
    assert _score(assignments, targets) == score, f"{name}: score is not the global minimum"
    assert _actual_matrix(assignments) == matrix, f"{name}: matrix tie-break drifted"
    assert _code_vector(examples, assignments) == codes, f"{name}: assignment tie-break drifted"


def test_a_single_globally_feasible_non_exact_matrix_is_selected() -> None:
    examples, targets = _minimum_deviation_case("unique-optimum")
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert _actual_matrix(assignments) == (2, 0, 0, 0, 1, 0, 0, 0, 1)
    assert _target_matrix(targets) == (1, 1, 0, 1, 0, 0, 0, 0, 1)
    assert _score(assignments, targets) == 4
    optima = _feasible_matrices_at_minimum(examples, targets)
    assert len(optima) == 1, "this case must have exactly one minimum-score matrix"


def test_equal_score_matrices_are_broken_by_the_nine_cell_lexicographic_order() -> None:
    examples, targets = _minimum_deviation_case("two-minimum-matrices")
    optima = _feasible_matrices_at_minimum(examples, targets)
    assert optima == ((4, 0, 0, 0, 1, 0, 1, 0, 0), (4, 0, 0, 1, 0, 0, 0, 1, 0)), (
        "this case must have exactly two minimum-score matrices"
    )
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    assert _actual_matrix(assignments) == optima[0], "the lexicographic winner must be selected"
    assert _score(assignments, targets) == 4


def test_equal_matrices_are_broken_by_the_partition_code_vector() -> None:
    examples, targets = _minimum_deviation_case("assignment-tie-break")
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    matrix = _actual_matrix(assignments)
    assert matrix == (2, 2, 0, 1, 0, 0, 0, 0, 1)
    vectors = _code_vectors_for_matrix(examples, targets, matrix)
    assert len(vectors) > 1, "this case must admit more than one assignment for its matrix"
    assert _code_vector(examples, assignments) == min(vectors), (
        "the lexicographically smallest partition-code vector must be selected"
    )
    assert _code_vector(examples, assignments)[:2] == (0, 1), (
        "the earlier-ranked yes group must take the smaller code"
    )


def test_no_partition_total_feasible_assignment_fails_closed() -> None:
    examples = _grouped((("y0", "yes", 2), ("n0", "no", 2), ("m0", "maybe", 2)))
    targets = _targets(((1, 1, 0), (1, 1, 0), (1, 1, 0)))
    with pytest.raises(_RankedBoundaryAllocationError, match="exact partition totals"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)


def test_an_input_beyond_the_correction_boundary_fails_closed() -> None:
    """The bound is refused, never approximated, truncated or sampled."""
    assert _MINIMUM_DEVIATION_MAX_EXAMPLES == 1000
    assert _MINIMUM_DEVIATION_MAX_GROUPS == 1000
    specification = [(f"y{index:04d}", "yes", 2) for index in range(500)]
    specification.append(("n0", "no", 1))
    specification.append(("m0", "maybe", 1))
    examples = _grouped(specification)
    assert len(examples) == 1002
    targets = _targets(((999, 1, 0), (1, 0, 0), (0, 1, 0)))
    with pytest.raises(_RankedBoundaryAllocationError, match="accepts at most"):
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets)


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_correction_is_input_order_independent(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    forward = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    reverse = _allocate_indivisible_groups_with_minimum_deviation(
        tuple(reversed(examples)), targets
    )
    assert forward == reverse, f"{name}: input order must not affect the correction"


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_correction_is_repeatable(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    runs = [
        _allocate_indivisible_groups_with_minimum_deviation(examples, targets) for _ in range(3)
    ]
    assert runs[0] == runs[1] == runs[2], f"{name}: repeated runs must be identical"


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_correction_preserves_every_hard_constraint(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    ranked = rank_groups(examples)
    assert len(assignments) == len(ranked), "every ranked group must be assigned exactly once"

    documents = [assignment.source_document_id for assignment in assignments]
    assert len(set(documents)) == len(documents), "no source document may cross partitions"

    assigned = [example_id for assignment in assignments for example_id in assignment.example_ids]
    assert sorted(assigned) == sorted(example.example_id for example in examples), (
        "every example must be assigned exactly once, with none omitted or duplicated"
    )

    matrix = _actual_matrix(assignments)
    for index, target in enumerate(_targets(_MINIMUM_DEVIATION_CASES[name][1])):
        row = matrix[index * 3 : index * 3 + 3]
        assert sum(row) == target.train + target.validation + target.test, (
            "label row totals must stay exact"
        )
    for offset, partition in enumerate(PARTITIONS):
        expected = sum(target.for_partition(partition) for target in targets)
        assert sum(matrix[offset::3]) == expected, "overall partition totals must stay exact"


@pytest.mark.parametrize("name", sorted(_MINIMUM_DEVIATION_CASES))
def test_the_correction_returns_the_accepted_final_ordering(name: str) -> None:
    examples, targets = _minimum_deviation_case(name)
    assignments = _allocate_indivisible_groups_with_minimum_deviation(examples, targets)
    partition_order = {partition: index for index, partition in enumerate(PARTITIONS)}
    decision_order = {decision: index for index, decision in enumerate(DECISIONS)}
    assert list(assignments) == sorted(
        assignments,
        key=lambda assignment: (
            partition_order[assignment.partition],
            decision_order[assignment.decision],
            assignment.partition_key,
            assignment.source_document_id,
            min(assignment.row_ordinals),
        ),
    ), f"{name}: the accepted final ordering must be preserved"


def _feasible_matrices_at_minimum(
    examples: tuple[LabeledExample, ...], targets: tuple[LabelTarget, ...]
) -> tuple[tuple[int, ...], ...]:
    """TEST-ONLY: every minimum-score matrix, in ascending lexicographic order."""
    ordered_documents = _ordered_groups(examples)
    assert len(ordered_documents) <= 8, "test-only oracle: tiny group counts only"
    sizes = {
        group.source_document_id: (group.decision, group.example_count)
        for group in rank_groups(examples)
    }
    target_matrix = _target_matrix(targets)
    partition_totals = [
        sum(target.for_partition(partition) for target in targets) for partition in PARTITIONS
    ]
    scored: dict[tuple[int, ...], int] = {}
    for codes in product(range(3), repeat=len(ordered_documents)):
        cells = {(decision, partition): 0 for decision in DECISIONS for partition in PARTITIONS}
        totals = [0, 0, 0]
        for document, code in zip(ordered_documents, codes, strict=True):
            decision, size = sizes[document]
            cells[(decision, PARTITIONS[code])] += size
            totals[code] += size
        if totals != partition_totals:
            continue
        matrix = tuple(
            cells[(decision, partition)] for decision in DECISIONS for partition in PARTITIONS
        )
        scored[matrix] = sum(
            (actual - target) ** 2 for actual, target in zip(matrix, target_matrix, strict=True)
        )
    minimum = min(scored.values())
    return tuple(sorted(matrix for matrix, score in scored.items() if score == minimum))


def _code_vectors_for_matrix(
    examples: tuple[LabeledExample, ...],
    targets: tuple[LabelTarget, ...],
    wanted: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """TEST-ONLY: every code vector realizing one matrix, in ascending order."""
    ordered_documents = _ordered_groups(examples)
    assert len(ordered_documents) <= 8, "test-only oracle: tiny group counts only"
    sizes = {
        group.source_document_id: (group.decision, group.example_count)
        for group in rank_groups(examples)
    }
    partition_totals = [
        sum(target.for_partition(partition) for target in targets) for partition in PARTITIONS
    ]
    vectors: list[tuple[int, ...]] = []
    for codes in product(range(3), repeat=len(ordered_documents)):
        cells = {(decision, partition): 0 for decision in DECISIONS for partition in PARTITIONS}
        totals = [0, 0, 0]
        for document, code in zip(ordered_documents, codes, strict=True):
            decision, size = sizes[document]
            cells[(decision, PARTITIONS[code])] += size
            totals[code] += size
        if totals != partition_totals:
            continue
        matrix = tuple(
            cells[(decision, partition)] for decision in DECISIONS for partition in PARTITIONS
        )
        if matrix == wanted:
            vectors.append(codes)
    return tuple(sorted(vectors))
