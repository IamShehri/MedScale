"""Fixture-safe deterministic primitives for the P01-04 split algorithm.

This private module implements only the pure, in-memory P01-04B1 core.  It has
no filesystem entry points and does not make the public
``SourceDocumentGroupedSplitter`` executable.  Formal dataset membership and
artifact generation remain separately authorized work.

It also carries the bounded private minimum-deviation correction adopted as
FD-BMD-1 through FD-BMD-14.  The accepted exact allocator
:func:`allocate_indivisible_groups` is preserved unchanged in name, signature,
validation order, error semantics and returned ordering; the correction is an
*additional* private capability reached only through
:func:`_allocate_indivisible_groups_with_minimum_deviation`, and only after the
exact allocator raises the one private typed ranked-boundary failure.  Nothing
here is exported, and no value produced here is promotable.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt
from typing import Final, Literal

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


class _RankedBoundaryAllocationError(SplitAllocationError):
    """Private typed refusal of the bounded indivisible-group correction (FD-BMD-3).

    Inside :func:`allocate_indivisible_groups` this class is raised at exactly
    one site — the ranked-boundary crossing.  The other three allocation
    failures (observed/expected decision-total mismatch, "allocation did not
    exhaust targets" and the controlled-rounding refusal) keep raising the base
    :class:`SplitAllocationError`, so this class *is* the authorized fallback
    trigger and nothing else can reach the resolver.

    FD-BMD-3 permits exactly one private subclass, so the bounded resolver
    reuses it for its own two fail-closed refusals: an input beyond the
    correction boundary, and the absence of any partition-total-feasible
    assignment.  Those refusals are raised outside the exact-first ``try``, so
    they propagate instead of re-entering the fallback.

    The class is module-private, unexported, absent from every ``__all__``, and
    a ``SplitAllocationError``, so every accepted ``except`` and
    ``pytest.raises`` clause keyed to the base class behaves exactly as before.
    """


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
                # The only permitted semantic change to the accepted exact
                # allocator: the ranked-boundary crossing now carries the
                # private typed subclass.  The message is byte-for-byte the
                # accepted one and the class is a SplitAllocationError, so every
                # existing caller and assertion is unaffected.
                raise _RankedBoundaryAllocationError(
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


# ---------------------------------------------------------------------------
# Bounded private global minimum-deviation correction (FD-BMD-1 .. FD-BMD-14)
# ---------------------------------------------------------------------------

#: The correction boundary is a governance limit, not a performance heuristic:
#: an input beyond it is refused, never approximated, truncated or sampled.
_MINIMUM_DEVIATION_MAX_EXAMPLES: Final = 1000
_MINIMUM_DEVIATION_MAX_GROUPS: Final = 1000


@dataclass(frozen=True, slots=True)
class _DecisionLattice:
    """The complete reachable ``(train, validation)`` lattice of one decision.

    A per-decision state is exactly ``(train_count, validation_count)``; the
    third count is forced by ``row_total - train_count - validation_count``, so
    no reachable state is lost by omitting it.  ``suffix_masks[i]`` is a bitset
    over the state grid holding every state that groups ``i`` through the last
    can realize on their own, encoded at bit ``train * stride + validation``.

    ``stride`` is ``row_total + 1`` and every reachable ``train`` and
    ``validation`` value is bounded by ``row_total``, so the encoding is
    injective and a shift can never alias one state onto another.

    The retained suffix sets *are* the canonical predecessor structure.  Storing
    one code vector per state would be equivalent but far larger; the suffix sets
    are lossless, and :func:`_lexicographic_partition_codes` recovers the
    canonical lexicographically smallest vector of any reachable state from them
    deterministically.  This is a memory optimization of the retained structure,
    never a reduction of the reachable set.
    """

    decision: Decision
    groups: tuple[RankedGroup, ...]
    sizes: tuple[int, ...]
    row_total: int
    stride: int
    suffix_masks: tuple[int, ...]

    @property
    def reachable_mask(self) -> int:
        """Return the complete set of states the whole decision can realize."""
        return self.suffix_masks[0]


@dataclass(frozen=True, slots=True)
class _MinimumDeviationSolution:
    """One globally feasible nine-cell matrix and its integer score."""

    score: int
    matrix: tuple[int, ...]
    cells: tuple[tuple[int, int], ...]


def _suffix_state_masks(sizes: Sequence[int], stride: int) -> tuple[int, ...]:
    """Return the reachable-state bitset of every group suffix.

    ``masks[len(sizes)]`` is the single state ``(0, 0)``; each earlier entry adds
    one group by taking the union of the three placements — validation shifts by
    ``size``, train shifts by ``size * stride`` and test leaves the state alone.
    The union is the complete transition, so the retained set is exactly the
    reachable set: no state is pruned and none is invented.
    """
    masks: list[int] = [1]
    for size in reversed(sizes):
        current = masks[-1]
        masks.append(current | (current << size) | (current << (size * stride)))
    masks.reverse()
    return tuple(masks)


def _reachable_state_mask(sizes: Sequence[int], stride: int) -> int:
    """Return only the final reachable-state bitset, without retaining suffixes."""
    mask = 1
    for size in sizes:
        mask |= (mask << size) | (mask << (size * stride))
    return mask


def _state_is_reachable(
    mask: int, train: int, validation: int, stride: int, row_total: int
) -> bool:
    """Return whether ``(train, validation)`` is a member of a state bitset."""
    if train < 0 or validation < 0 or train + validation > row_total:
        return False
    return bool((mask >> (train * stride + validation)) & 1)


def _decode_states(mask: int, stride: int, row_total: int) -> tuple[tuple[int, int], ...]:
    """Return every member of a state bitset in ascending ``(train, validation)`` order.

    The walk is over integer ranges and integer bit operations only, so the
    returned order is fixed by arithmetic and cannot depend on set or dictionary
    iteration order.
    """
    states: list[tuple[int, int]] = []
    for train in range(row_total + 1):
        row = (mask >> (train * stride)) & ((1 << (row_total - train + 1)) - 1)
        while row:
            lowest = row & -row
            states.append((train, lowest.bit_length() - 1))
            row ^= lowest
    return tuple(states)


def _build_lattice(decision: Decision, groups: tuple[RankedGroup, ...]) -> _DecisionLattice:
    """Return the complete reachable lattice of one decision's ranked groups."""
    sizes = tuple(group.example_count for group in groups)
    row_total = sum(sizes)
    stride = row_total + 1
    return _DecisionLattice(
        decision=decision,
        groups=groups,
        sizes=sizes,
        row_total=row_total,
        stride=stride,
        suffix_masks=_suffix_state_masks(sizes, stride),
    )


def _cell_cost(train: int, validation: int, row_total: int, target: LabelTarget) -> int:
    """Return the integer squared deviation contributed by one decision row."""
    return (
        (train - target.train) ** 2
        + (validation - target.validation) ** 2
        + (row_total - train - validation - target.test) ** 2
    )


def _matrix_vector(cells: Sequence[tuple[int, int]], row_totals: Sequence[int]) -> tuple[int, ...]:
    """Return the nine actual cells in the controlling FD-BMD-6 order."""
    vector: list[int] = []
    for (train, validation), row_total in zip(cells, row_totals, strict=True):
        vector.extend((train, validation, row_total - train - validation))
    return tuple(vector)


def _maximum_free_cell_deviation(
    row_totals: Mapping[Decision, int],
    partition_totals: Mapping[Partition, int],
    target_by_decision: Mapping[Decision, LabelTarget],
) -> int:
    """Return the largest deviation any free cell can take.

    The four free cells are ``yes/train``, ``yes/validation``, ``no/train`` and
    ``no/validation``; the other five are forced by the exact row and partition
    totals.  A free cell holds at most ``min(row_total, partition_total)``
    examples and at least zero, so this bound is exact.  Searching that radius
    therefore enumerates every feasible matrix, which is what makes the
    termination of the radius search a completeness statement rather than a
    cutoff.
    """
    maximum = 0
    for decision in DECISIONS[:2]:
        for partition in PARTITIONS[:2]:
            upper = min(row_totals[decision], partition_totals[partition])
            target = target_by_decision[decision].for_partition(partition)
            maximum = max(maximum, target, upper - target)
    return maximum


def _search_free_block(
    radius: int,
    incumbent: _MinimumDeviationSolution | None,
    lattices: Mapping[Decision, _DecisionLattice],
    target_by_decision: Mapping[Decision, LabelTarget],
    partition_totals: Mapping[Partition, int],
    yes_states: Sequence[tuple[int, int]],
    no_states: Sequence[tuple[int, int]],
) -> _MinimumDeviationSolution | None:
    """Return the best solution whose free block lies within ``radius`` of the target.

    Every candidate is a genuine feasible matrix: the ``yes`` and ``no`` cells
    are members of their decision lattices and the forced ``maybe`` cell is
    tested for membership in its own lattice, so exact row totals and exact
    partition totals both hold by construction.
    """
    yes_lattice = lattices["yes"]
    no_lattice = lattices["no"]
    maybe_lattice = lattices["maybe"]
    yes_target = target_by_decision["yes"]
    no_target = target_by_decision["no"]
    maybe_target = target_by_decision["maybe"]
    train_total = partition_totals["train"]
    validation_total = partition_totals["validation"]
    row_totals = (yes_lattice.row_total, no_lattice.row_total, maybe_lattice.row_total)

    yes_candidates = [
        state
        for state in yes_states
        if abs(state[0] - yes_target.train) <= radius
        and abs(state[1] - yes_target.validation) <= radius
    ]
    no_candidates = [
        state
        for state in no_states
        if abs(state[0] - no_target.train) <= radius
        and abs(state[1] - no_target.validation) <= radius
    ]

    best = incumbent
    for yes_train, yes_validation in yes_candidates:
        yes_cost = _cell_cost(yes_train, yes_validation, yes_lattice.row_total, yes_target)
        if best is not None and yes_cost > best.score:
            continue
        for no_train, no_validation in no_candidates:
            no_cost = _cell_cost(no_train, no_validation, no_lattice.row_total, no_target)
            partial = yes_cost + no_cost
            # Every remaining contribution is a sum of squares, so a partial cost
            # already above the incumbent can never produce a better or equal
            # total.  The comparison is strict, so no tied optimum is discarded.
            if best is not None and partial > best.score:
                continue
            maybe_train = train_total - yes_train - no_train
            maybe_validation = validation_total - yes_validation - no_validation
            if not _state_is_reachable(
                maybe_lattice.reachable_mask,
                maybe_train,
                maybe_validation,
                maybe_lattice.stride,
                maybe_lattice.row_total,
            ):
                continue
            score = partial + _cell_cost(
                maybe_train, maybe_validation, maybe_lattice.row_total, maybe_target
            )
            cells = (
                (yes_train, yes_validation),
                (no_train, no_validation),
                (maybe_train, maybe_validation),
            )
            matrix = _matrix_vector(cells, row_totals)
            if best is None or (score, matrix) < (best.score, best.matrix):
                best = _MinimumDeviationSolution(score=score, matrix=matrix, cells=cells)
    return best


def _minimum_deviation_solution(
    lattices: Mapping[Decision, _DecisionLattice],
    target_by_decision: Mapping[Decision, LabelTarget],
    partition_totals: Mapping[Partition, int],
    row_totals: Mapping[Decision, int],
) -> _MinimumDeviationSolution:
    """Return the proven global minimum-deviation matrix.

    The search grows a radius around the target free block.  When a solution
    with score ``s`` has been found and the radius has reached ``isqrt(s)``, the
    search is complete: any matrix scoring below ``s`` would have every cell
    deviating by at most ``isqrt(s - 1) <= isqrt(s)``, and every matrix scoring
    exactly ``s`` deviates by at most ``isqrt(s)``, so both are already inside
    the enumerated region.  The selected matrix is therefore a proven global
    minimum and the lexicographic winner among all minima, not a best-found
    value.  The radius is additionally capped by the exact free-cell bound, at
    which point the region is the whole feasible set.
    """
    yes_lattice = lattices["yes"]
    no_lattice = lattices["no"]
    yes_states = _decode_states(
        yes_lattice.reachable_mask, yes_lattice.stride, yes_lattice.row_total
    )
    no_states = _decode_states(no_lattice.reachable_mask, no_lattice.stride, no_lattice.row_total)
    maximum_radius = _maximum_free_cell_deviation(row_totals, partition_totals, target_by_decision)

    best: _MinimumDeviationSolution | None = None
    radius = 0
    while True:
        best = _search_free_block(
            radius,
            best,
            lattices,
            target_by_decision,
            partition_totals,
            yes_states,
            no_states,
        )
        if best is not None and radius >= isqrt(best.score):
            return best
        if radius >= maximum_radius:
            break
        widened = 1 if radius == 0 else radius * 2
        if best is not None:
            widened = max(widened, isqrt(best.score))
        radius = min(widened, maximum_radius)

    if best is not None:
        return best
    raise _RankedBoundaryAllocationError(
        "no indivisible-group assignment satisfies the exact partition totals "
        f"train={partition_totals['train']}, "
        f"validation={partition_totals['validation']}, "
        f"test={partition_totals['test']}"
    )


def _lexicographic_partition_codes(
    lattice: _DecisionLattice, train: int, validation: int
) -> tuple[int, ...]:
    """Return the lexicographically smallest partition-code vector for one decision.

    Groups are walked in the accepted ``rank_groups`` order and the smallest code
    whose remainder is still completable is taken at every position, which is
    exactly the lexicographic minimum over the assignments realizing
    ``(train, validation)``.  Completability is decided against the retained
    suffix state sets, so the greedy choice is never a guess.
    """
    codes: list[int] = []
    remaining_train = train
    remaining_validation = validation
    for index, size in enumerate(lattice.sizes):
        suffix = lattice.suffix_masks[index + 1]
        if _state_is_reachable(
            suffix, remaining_train - size, remaining_validation, lattice.stride, lattice.row_total
        ):
            codes.append(0)
            remaining_train -= size
        elif _state_is_reachable(
            suffix, remaining_train, remaining_validation - size, lattice.stride, lattice.row_total
        ):
            codes.append(1)
            remaining_validation -= size
        elif _state_is_reachable(
            suffix, remaining_train, remaining_validation, lattice.stride, lattice.row_total
        ):
            codes.append(2)
        else:  # pragma: no cover - the selected cell is reachable by construction
            raise SplitAllocationError(
                f"minimum-deviation reconstruction reached an unreachable "
                f"{lattice.decision!r} state"
            )
    if remaining_train != 0 or remaining_validation != 0:  # pragma: no cover - see above
        raise SplitAllocationError(
            f"minimum-deviation reconstruction did not exhaust {lattice.decision!r}"
        )
    return tuple(codes)


def _target_by_decision(targets: Sequence[LabelTarget]) -> dict[Decision, LabelTarget]:
    """Return the validated target index, using the accepted validation order."""
    by_decision: dict[Decision, LabelTarget] = {}
    for target in targets:
        if target.decision in by_decision:
            raise SplitInputError(f"duplicate target decision: {target.decision}")
        _required_nonnegative_int(target.train, "train")
        _required_nonnegative_int(target.validation, "validation")
        _required_nonnegative_int(target.test, "test")
        by_decision[target.decision] = target
    if set(by_decision) != set(DECISIONS):
        raise SplitInputError(f"targets must contain exactly {DECISIONS}")
    return by_decision


def _verify_minimum_deviation_assignments(
    assignments: Sequence[GroupAssignment],
    ranked: Sequence[RankedGroup],
    examples: Sequence[LabeledExample],
    partition_totals: Mapping[Partition, int],
    row_totals: Mapping[Decision, int],
) -> None:
    """Fail closed unless every FD-BMD-5 constraint holds on the built result."""
    if len(assignments) != len(ranked):
        raise SplitAllocationError("minimum-deviation allocation did not place every group once")

    seen_documents: set[str] = set()
    seen_examples: set[str] = set()
    observed_partitions: dict[Partition, int] = dict.fromkeys(PARTITIONS, 0)
    observed_rows: dict[Decision, int] = dict.fromkeys(DECISIONS, 0)
    for assignment in assignments:
        if assignment.source_document_id in seen_documents:
            raise SplitAllocationError(
                "minimum-deviation allocation placed a source document more than once"
            )
        seen_documents.add(assignment.source_document_id)
        for example_id in assignment.example_ids:
            if example_id in seen_examples:
                raise SplitAllocationError("minimum-deviation allocation duplicated an example")
            seen_examples.add(example_id)
        observed_partitions[assignment.partition] += len(assignment.example_ids)
        observed_rows[assignment.decision] += len(assignment.example_ids)

    if seen_examples != {example.example_id for example in examples}:
        raise SplitAllocationError("minimum-deviation allocation omitted or invented an example")
    if observed_partitions != dict(partition_totals):
        raise SplitAllocationError("minimum-deviation allocation missed the exact partition totals")
    if observed_rows != dict(row_totals):
        raise SplitAllocationError("minimum-deviation allocation missed the exact label row totals")


def _resolve_minimum_deviation(
    examples: Sequence[LabeledExample], targets: Sequence[LabelTarget]
) -> tuple[GroupAssignment, ...]:
    """Return the globally minimum-deviation allocation of indivisible groups.

    Reached only after the accepted exact allocator raised
    :class:`_RankedBoundaryAllocationError`.  Every label row total and both
    remaining partition totals stay exact; only the nine interior cells may
    deviate, and only by the proven global minimum.
    """
    target_by_decision = _target_by_decision(targets)
    ranked = rank_groups(examples)

    if (
        len(examples) > _MINIMUM_DEVIATION_MAX_EXAMPLES
        or len(ranked) > _MINIMUM_DEVIATION_MAX_GROUPS
    ):
        raise _RankedBoundaryAllocationError(
            "the bounded minimum-deviation correction accepts at most "
            f"{_MINIMUM_DEVIATION_MAX_EXAMPLES} examples in at most "
            f"{_MINIMUM_DEVIATION_MAX_GROUPS} source-document groups; received "
            f"{len(examples)} examples in {len(ranked)} groups"
        )

    groups_by_decision = {
        decision: tuple(group for group in ranked if group.decision == decision)
        for decision in DECISIONS
    }
    row_totals: dict[Decision, int] = {}
    for decision in DECISIONS:
        expected = sum(
            target_by_decision[decision].for_partition(partition) for partition in PARTITIONS
        )
        observed = sum(group.example_count for group in groups_by_decision[decision])
        if observed != expected:
            raise SplitAllocationError(
                f"target total for {decision!r} is {expected}, observed {observed} examples"
            )
        row_totals[decision] = observed

    partition_totals: dict[Partition, int] = {
        partition: sum(
            target_by_decision[decision].for_partition(partition) for decision in DECISIONS
        )
        for partition in PARTITIONS
    }

    # Structural feasibility over every group at once.  The reachable set of
    # global (train, validation) counts is exactly the sumset of the three
    # decision lattices, so an unreachable pair proves that no assignment
    # satisfies the exact partition totals and the correction refuses.
    global_stride = len(examples) + 1
    global_mask = _reachable_state_mask(
        tuple(group.example_count for group in ranked), global_stride
    )
    if not _state_is_reachable(
        global_mask,
        partition_totals["train"],
        partition_totals["validation"],
        global_stride,
        len(examples),
    ):
        raise _RankedBoundaryAllocationError(
            "no indivisible-group assignment satisfies the exact partition totals "
            f"train={partition_totals['train']}, "
            f"validation={partition_totals['validation']}, "
            f"test={partition_totals['test']}"
        )

    lattices = {
        decision: _build_lattice(decision, groups_by_decision[decision]) for decision in DECISIONS
    }
    solution = _minimum_deviation_solution(
        lattices, target_by_decision, partition_totals, row_totals
    )

    # The three decision blocks are independent once the matrix is fixed, and the
    # complete assignment vector is their concatenation in the order yes, no,
    # maybe.  Lexicographic order on a concatenation of independent fixed-length
    # blocks is settled block by block, so the per-block minima concatenate to
    # the global minimum and no cross-block search is needed.
    assignments: list[GroupAssignment] = []
    for decision, (train, validation) in zip(DECISIONS, solution.cells, strict=True):
        lattice = lattices[decision]
        codes = _lexicographic_partition_codes(lattice, train, validation)
        for group, code in zip(lattice.groups, codes, strict=True):
            assignments.append(
                GroupAssignment(
                    partition=PARTITIONS[code],
                    source_document_id=group.source_document_id,
                    decision=decision,
                    example_ids=group.example_ids,
                    row_ordinals=group.row_ordinals,
                    partition_key=group.partition_key,
                )
            )

    _verify_minimum_deviation_assignments(
        assignments, ranked, examples, partition_totals, row_totals
    )

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


def _allocate_indivisible_groups_with_minimum_deviation(
    examples: Sequence[LabeledExample], targets: Sequence[LabelTarget]
) -> tuple[GroupAssignment, ...]:
    """Allocate exactly when possible, and by global minimum deviation when not.

    The ``try`` encloses the accepted exact-allocator call and nothing else: not
    the resolver, not result verification, not artifact construction and not any
    caller code.  Selection is by exception class alone — no message, no
    ``args``, no substring and no regular expression participates — and the base
    :class:`SplitAllocationError` is never caught, so every non-boundary
    allocation failure and every unrelated exception propagates untouched.
    """
    try:
        return allocate_indivisible_groups(examples, targets)
    except _RankedBoundaryAllocationError:
        pass

    return _resolve_minimum_deviation(examples, targets)


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
