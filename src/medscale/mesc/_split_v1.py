"""Fixture-safe deterministic primitives for the P01-04 split algorithm.

This private module implements only the pure, in-memory P01-04B1 core.  It has
no filesystem entry points and does not make the public
``SourceDocumentGroupedSplitter`` executable.  Formal dataset membership and
artifact generation remain separately authorized work.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Literal

Decision = Literal["yes", "no", "maybe"]
Partition = Literal["train", "validation", "test"]

ALGORITHM_VERSION = "mesc-pilot-01-split-algorithm/1"
SPLIT_SEED = "mesc-pilot-01-split-v1"
EXAMPLE_ID_PREFIX = "mesc-pilot-01:"

DECISIONS: tuple[Decision, ...] = ("yes", "no", "maybe")
PARTITIONS: tuple[Partition, ...] = ("train", "validation", "test")


class SplitInputError(ValueError):
    """Raised when a P01-04B1 input cannot be joined unambiguously."""


class SplitAllocationError(ValueError):
    """Raised when indivisible groups cannot satisfy the exact targets."""


@dataclass(frozen=True, slots=True)
class OrderedExampleRow:
    """Identity-only row from the accepted ordered example registry."""

    original_example_id: str
    row_ordinal: int
    source_document_id: str


@dataclass(frozen=True, slots=True)
class SourceLabelRow:
    """Only the identity and label fields retained from a source-record envelope."""

    dataset_id: str
    dataset_revision: str
    configuration: str
    original_example_id: str
    source_document_id: str
    decision: Decision
    source_record_hash: str


@dataclass(frozen=True, slots=True)
class LabeledExample:
    """Joined, label-aware example identity used by the pure split core."""

    example_id: str
    original_example_id: str
    source_document_id: str
    row_ordinal: int
    decision: Decision


@dataclass(frozen=True, slots=True)
class LabelTarget:
    """Exact per-partition targets for one decision stratum."""

    decision: Decision
    train: int
    validation: int
    test: int

    def for_partition(self, partition: Partition) -> int:
        return {
            "train": self.train,
            "validation": self.validation,
            "test": self.test,
        }[partition]


@dataclass(frozen=True, slots=True)
class RankedGroup:
    """One indivisible source-document group in deterministic rank order."""

    source_document_id: str
    decision: Decision
    example_ids: tuple[str, ...]
    row_ordinals: tuple[int, ...]
    partition_key: str

    @property
    def example_count(self) -> int:
        return len(self.example_ids)


@dataclass(frozen=True, slots=True)
class GroupAssignment:
    """Synthetic-fixture assignment returned only by the private B1 core."""

    partition: Partition
    source_document_id: str
    decision: Decision
    example_ids: tuple[str, ...]
    row_ordinals: tuple[int, ...]
    partition_key: str


def canonical_json_bytes(value: object) -> bytes:
    """Return the exact canonical UTF-8 encoding ratified for P01-04."""
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hexdigest(value: object) -> str:
    """Hash a value's canonical bytes with full lowercase SHA-256."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def derive_example_id(
    *,
    dataset_id: str,
    dataset_revision: str,
    configuration: str,
    original_example_id: str,
    source_document_id: str,
    transformation_version: str,
) -> str:
    """Derive the canonical full-SHA-256 Pilot-01 example identifier."""
    payload = {
        "configuration": _required_nonblank(configuration, "configuration"),
        "dataset_id": _required_nonblank(dataset_id, "dataset_id"),
        "dataset_revision": _required_nonblank(dataset_revision, "dataset_revision"),
        "original_example_id": _required_nonblank(original_example_id, "original_example_id"),
        "source_document_id": _required_nonblank(source_document_id, "source_document_id"),
        "transformation_version": _required_nonblank(
            transformation_version, "transformation_version"
        ),
    }
    return EXAMPLE_ID_PREFIX + sha256_hexdigest(payload)


def source_label_from_envelope(envelope: Mapping[str, object]) -> SourceLabelRow:
    """Extract only identity and label fields from one source-record envelope.

    Question, context, answer, and annotation content is deliberately not
    retained by the return type.
    """
    record = envelope.get("record")
    if not isinstance(record, Mapping):
        raise SplitInputError("source record envelope must contain an object field 'record'")
    source_record_hash = _required_nonblank(
        envelope.get("source_record_hash"), "source_record_hash"
    )
    if len(source_record_hash) != 64 or any(
        character not in "0123456789abcdef" for character in source_record_hash
    ):
        raise SplitInputError("source_record_hash must be 64 lowercase hexadecimal characters")
    decision_value = _required_nonblank(record.get("final_decision"), "final_decision")
    if decision_value not in DECISIONS:
        raise SplitInputError(f"final_decision must be one of {DECISIONS}, got {decision_value!r}")
    return SourceLabelRow(
        dataset_id=_required_nonblank(record.get("dataset_id"), "dataset_id"),
        dataset_revision=_required_nonblank(record.get("dataset_revision"), "dataset_revision"),
        configuration=_required_nonblank(record.get("configuration"), "configuration"),
        original_example_id=_required_nonblank(
            record.get("original_example_id"), "original_example_id"
        ),
        source_document_id=_required_nonblank(
            record.get("source_document_id"), "source_document_id"
        ),
        decision=decision_value,
        source_record_hash=source_record_hash,
    )


def join_labels(
    ordered_rows: Sequence[OrderedExampleRow],
    source_labels: Sequence[SourceLabelRow],
    *,
    transformation_version: str,
) -> tuple[LabeledExample, ...]:
    """Join registry identities to labels, rejecting every ambiguous mismatch."""
    _required_nonblank(transformation_version, "transformation_version")
    if not ordered_rows:
        raise SplitInputError("ordered registry must not be empty")
    if not source_labels:
        raise SplitInputError("source label rows must not be empty")

    ordered_by_id: dict[str, OrderedExampleRow] = {}
    seen_ordinals: set[int] = set()
    for row in ordered_rows:
        _required_nonblank(row.original_example_id, "original_example_id")
        _required_nonblank(row.source_document_id, "source_document_id")
        _required_nonnegative_int(row.row_ordinal, "row_ordinal")
        if row.original_example_id in ordered_by_id:
            raise SplitInputError(
                f"duplicate ordered original_example_id: {row.original_example_id}"
            )
        if row.row_ordinal in seen_ordinals:
            raise SplitInputError(f"duplicate row_ordinal: {row.row_ordinal}")
        ordered_by_id[row.original_example_id] = row
        seen_ordinals.add(row.row_ordinal)

    labels_by_id: dict[str, SourceLabelRow] = {}
    dataset_identities: set[tuple[str, str, str]] = set()
    source_hashes: set[str] = set()
    for label in source_labels:
        for value, field in (
            (label.dataset_id, "dataset_id"),
            (label.dataset_revision, "dataset_revision"),
            (label.configuration, "configuration"),
            (label.original_example_id, "original_example_id"),
            (label.source_document_id, "source_document_id"),
        ):
            _required_nonblank(value, field)
        if label.decision not in DECISIONS:
            raise SplitInputError(f"invalid decision: {label.decision!r}")
        if len(label.source_record_hash) != 64 or any(
            character not in "0123456789abcdef" for character in label.source_record_hash
        ):
            raise SplitInputError("source_record_hash must be 64 lowercase hexadecimal characters")
        if label.original_example_id in labels_by_id:
            raise SplitInputError(
                f"duplicate source-label original_example_id: {label.original_example_id}"
            )
        if label.source_record_hash in source_hashes:
            raise SplitInputError(f"duplicate source_record_hash: {label.source_record_hash}")
        labels_by_id[label.original_example_id] = label
        source_hashes.add(label.source_record_hash)
        dataset_identities.add((label.dataset_id, label.dataset_revision, label.configuration))

    if len(dataset_identities) != 1:
        raise SplitInputError("source labels contain inconsistent dataset identities")

    ordered_ids = set(ordered_by_id)
    label_ids = set(labels_by_id)
    missing = sorted(ordered_ids - label_ids)
    unexpected = sorted(label_ids - ordered_ids)
    if missing or unexpected:
        raise SplitInputError(
            f"label join identity mismatch: missing={missing}, unexpected={unexpected}"
        )

    joined: list[LabeledExample] = []
    for row in sorted(ordered_rows, key=lambda item: item.row_ordinal):
        label = labels_by_id[row.original_example_id]
        if row.source_document_id != label.source_document_id:
            raise SplitInputError(
                "source_document_id mismatch for "
                f"{row.original_example_id}: registry={row.source_document_id!r}, "
                f"label={label.source_document_id!r}"
            )
        joined.append(
            LabeledExample(
                example_id=derive_example_id(
                    dataset_id=label.dataset_id,
                    dataset_revision=label.dataset_revision,
                    configuration=label.configuration,
                    original_example_id=label.original_example_id,
                    source_document_id=label.source_document_id,
                    transformation_version=transformation_version,
                ),
                original_example_id=row.original_example_id,
                source_document_id=row.source_document_id,
                row_ordinal=row.row_ordinal,
                decision=label.decision,
            )
        )
    return tuple(joined)


def constrained_apportionment(
    label_totals: Mapping[str, int], partition_totals: Mapping[str, int]
) -> tuple[LabelTarget, ...]:
    """Return the minimum-squared-deviation integer target matrix.

    The ratified 3x3 matrix is a controlled rounding of the exact rational
    proportions.  Enumerating every floor/ceiling combination is complete for
    this transportation rounding problem, avoids floating point arithmetic,
    and makes the specified lexicographic tie-break explicit.
    """
    _validate_exact_keys(label_totals, DECISIONS, "label_totals")
    _validate_exact_keys(partition_totals, PARTITIONS, "partition_totals")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in label_totals.values()
    ):
        raise SplitInputError("label totals must be non-negative integers")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in partition_totals.values()
    ):
        raise SplitInputError("partition totals must be non-negative integers")
    label_grand_total = sum(label_totals.values())
    partition_grand_total = sum(partition_totals.values())
    if label_grand_total == 0 or label_grand_total != partition_grand_total:
        raise SplitInputError("label and partition totals must be equal and greater than zero")

    ideals = tuple(
        Fraction(label_totals[decision] * partition_totals[partition], label_grand_total)
        for decision in DECISIONS
        for partition in PARTITIONS
    )
    choices = tuple(
        (ideal.numerator // ideal.denominator,)
        if ideal.denominator == 1
        else (ideal.numerator // ideal.denominator, ideal.numerator // ideal.denominator + 1)
        for ideal in ideals
    )

    best: tuple[Fraction, tuple[int, ...]] | None = None
    for vector in product(*choices):
        if any(
            sum(vector[label_index * len(PARTITIONS) + offset] for offset in range(3))
            != label_totals[decision]
            for label_index, decision in enumerate(DECISIONS)
        ):
            continue
        if any(
            sum(vector[label_index * len(PARTITIONS) + partition_index] for label_index in range(3))
            != partition_totals[partition]
            for partition_index, partition in enumerate(PARTITIONS)
        ):
            continue
        score = sum(
            ((Fraction(value) - ideal) ** 2 for value, ideal in zip(vector, ideals, strict=True)),
            start=Fraction(0),
        )
        candidate = (score, vector)
        if best is None or candidate < best:
            best = candidate

    if best is None:  # pragma: no cover - controlled rounding guarantees a candidate
        raise SplitAllocationError("no valid controlled-rounding matrix exists")
    vector = best[1]
    return tuple(
        LabelTarget(
            decision=decision,
            train=vector[index * 3],
            validation=vector[index * 3 + 1],
            test=vector[index * 3 + 2],
        )
        for index, decision in enumerate(DECISIONS)
    )


def rank_groups(examples: Sequence[LabeledExample]) -> tuple[RankedGroup, ...]:
    """Build homogeneous source-document groups and return deterministic ranks."""
    if not examples:
        raise SplitInputError("examples must not be empty")
    by_document: defaultdict[str, list[LabeledExample]] = defaultdict(list)
    seen_example_ids: set[str] = set()
    seen_ordinals: set[int] = set()
    for example in examples:
        _required_nonblank(example.example_id, "example_id")
        _required_nonblank(example.original_example_id, "original_example_id")
        _required_nonblank(example.source_document_id, "source_document_id")
        _required_nonnegative_int(example.row_ordinal, "row_ordinal")
        if example.decision not in DECISIONS:
            raise SplitInputError(f"invalid decision: {example.decision!r}")
        if example.example_id in seen_example_ids:
            raise SplitInputError(f"duplicate example_id: {example.example_id}")
        if example.row_ordinal in seen_ordinals:
            raise SplitInputError(f"duplicate row_ordinal: {example.row_ordinal}")
        seen_example_ids.add(example.example_id)
        seen_ordinals.add(example.row_ordinal)
        by_document[example.source_document_id].append(example)

    groups: list[RankedGroup] = []
    for source_document_id, members in by_document.items():
        decisions = {member.decision for member in members}
        if len(decisions) != 1:
            raise SplitInputError(
                f"source-document group {source_document_id!r} crosses decision strata"
            )
        ordered_members = sorted(members, key=lambda item: (item.row_ordinal, item.example_id))
        decision = ordered_members[0].decision
        partition_key = sha256_hexdigest(
            {
                "algorithm_version": ALGORITHM_VERSION,
                "seed": SPLIT_SEED,
                "source_document_id": source_document_id,
                "stratum": decision,
            }
        )
        groups.append(
            RankedGroup(
                source_document_id=source_document_id,
                decision=decision,
                example_ids=tuple(member.example_id for member in ordered_members),
                row_ordinals=tuple(member.row_ordinal for member in ordered_members),
                partition_key=partition_key,
            )
        )
    return tuple(
        sorted(
            groups,
            key=lambda group: (
                group.partition_key,
                group.source_document_id,
                min(group.row_ordinals),
            ),
        )
    )


def allocate_indivisible_groups(
    examples: Sequence[LabeledExample], targets: Sequence[LabelTarget]
) -> tuple[GroupAssignment, ...]:
    """Allocate ranked homogeneous groups without ever crossing a boundary.

    Exact targets are mandatory.  If a ranked multi-example group would cross
    a target boundary, B1 stops instead of splitting, reordering, or silently
    introducing a tolerance that the ratified version-1 policy does not define.
    """
    target_by_decision: dict[Decision, LabelTarget] = {}
    for target in targets:
        if target.decision in target_by_decision:
            raise SplitInputError(f"duplicate target decision: {target.decision}")
        _required_nonnegative_int(target.train, "train")
        _required_nonnegative_int(target.validation, "validation")
        _required_nonnegative_int(target.test, "test")
        target_by_decision[target.decision] = target
    if set(target_by_decision) != set(DECISIONS):
        raise SplitInputError(f"targets must contain exactly {DECISIONS}")

    ranked = rank_groups(examples)
    assignments: list[GroupAssignment] = []
    for decision in DECISIONS:
        decision_groups = [group for group in ranked if group.decision == decision]
        expected = sum(
            target_by_decision[decision].for_partition(partition) for partition in PARTITIONS
        )
        observed = sum(group.example_count for group in decision_groups)
        if observed != expected:
            raise SplitAllocationError(
                f"target total for {decision!r} is {expected}, observed {observed} examples"
            )

        partition_index = 0
        remaining = target_by_decision[decision].for_partition(PARTITIONS[0])
        for group in decision_groups:
            while remaining == 0 and partition_index < len(PARTITIONS) - 1:
                partition_index += 1
                remaining = target_by_decision[decision].for_partition(PARTITIONS[partition_index])
            if group.example_count > remaining:
                raise SplitAllocationError(
                    f"group {group.source_document_id!r} of size {group.example_count} "
                    f"would cross the {decision}/{PARTITIONS[partition_index]} boundary "
                    f"with {remaining} places remaining"
                )
            partition = PARTITIONS[partition_index]
            assignments.append(
                GroupAssignment(
                    partition=partition,
                    source_document_id=group.source_document_id,
                    decision=decision,
                    example_ids=group.example_ids,
                    row_ordinals=group.row_ordinals,
                    partition_key=group.partition_key,
                )
            )
            remaining -= group.example_count
        while remaining == 0 and partition_index < len(PARTITIONS) - 1:
            partition_index += 1
            remaining = target_by_decision[decision].for_partition(PARTITIONS[partition_index])
        if remaining != 0 or partition_index != len(PARTITIONS) - 1:
            raise SplitAllocationError(f"allocation did not exhaust targets for {decision!r}")

    partition_order = {partition: index for index, partition in enumerate(PARTITIONS)}
    decision_order = {decision: index for index, decision in enumerate(DECISIONS)}
    return tuple(
        sorted(
            assignments,
            key=lambda assignment: (
                partition_order[assignment.partition],
                decision_order[assignment.decision],
                assignment.partition_key,
                assignment.source_document_id,
                min(assignment.row_ordinals),
            ),
        )
    )


def _required_nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SplitInputError(f"{field} must be a non-blank string")
    return value


def _validate_exact_keys(values: Mapping[str, int], expected: Sequence[str], field: str) -> None:
    actual = set(values)
    required = set(expected)
    if actual != required:
        raise SplitInputError(
            f"{field} keys must be exactly {tuple(expected)}; "
            f"missing={sorted(required - actual)}, unexpected={sorted(actual - required)}"
        )


def _required_nonnegative_int(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise SplitInputError(f"{field} must be a non-negative integer, got {value!r}")
    if value < 0:
        raise SplitInputError(f"{field} must be a non-negative integer, got {value!r}")
    return value
