"""Non-promotable synthetic fixture generator for the P01-04B2D qualification suite.

This module is qualification infrastructure, not product code.  It lives under
``tests/`` on purpose (FD-B2D-1): it is never shipped in the wheel, never enters
the ``medscale`` public surface, is not importable from ``medscale``, is
referenced by no production file, and its filename does not match ``test_*.py``
so pytest does not collect it while mypy still type-checks it.

Everything it builds is **synthetic, fixture-only, non-evidence** identity data.
No dataset is read, no path is opened, no registry is consulted, and no network,
subprocess, clock, environment variable, locale, timezone, cache, logger,
temporary file or random source is used.  Nothing here is a real split, real
partition membership, a real leakage audit or clinical evidence.

Three independence boundaries are load-bearing (FD-B2D-10):

*The D6 ranking oracle is independent.*  :func:`d6_partition_key` re-implements
the ratified canonical payload and its no-terminal-LF serialization locally.
While a fixture is being constructed this module never calls ``rank_groups``,
``allocate_indivisible_groups`` or ``FixtureSplitFacade``, so the expected
grouping plan can never be a restatement of the code under test.

*The generator-spec proof precedes the facade.*  :func:`synthetic_identity_proof`
digests the generator **specification** only.  It binds no fixture digest, no
request identifier, no split hash, no fingerprint and no runtime value, so it is
computable before the facade runs.

*The minimum-deviation oracle is independent.*  :func:`minimum_deviation_result`
derives the feasible even-cell lattice directly from the ratified target matrix
and never consults ``constrained_apportionment``.

Raw synthetic question and context surfaces exist **only** in this module.  They
are inputs to the accepted B2B primitives and never reach a promotable byte
surface (FD-B2D-6 §8.5).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from itertools import product
from typing import Final

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._leakage_v1 import LeakageFinding
from medscale.mesc._split_v1 import Decision, OrderedExampleRow, Partition, SourceLabelRow

# ---------------------------------------------------------------------------
# Shared frozen identity contract (FD-B2D-3)
# ---------------------------------------------------------------------------

#: Ratified B1 algorithm version, restated locally so the D6 oracle stays independent.
ALGORITHM_VERSION: Final = "mesc-pilot-01-split-algorithm/1"

#: Ratified B1 split seed, restated locally for the same reason.
SEED: Final = "mesc-pilot-01-split-v1"

DATASET_ID: Final = "mesc-pilot-01-synthetic-qualification"
DATASET_REVISION: Final = "p01-04b2d-v1"
CONFIGURATION: Final = "b2d-synthetic-qualification"
TRANSFORMATION_VERSION: Final = "mesc-pilot-01-b2d-transform/1"
POLICY_ID: Final = "mesc-pilot-01-split-policy/1"
EXECUTION_EVIDENCE_REF: Final = "mesc-pilot-01-b2d-qualification/1"

FIXTURE_SCHEMA_VERSION: Final = "1"
FIXTURE_NAMESPACE_PREFIX: Final = "mesc-fixture/p01-04b2/1/"
SYNTHETIC_PROOF_PREFIX: Final = "mesc-synthetic-batch/1:sha256:"

GENERATOR_SPEC_SCHEMA: Final = "mesc-pilot-01-b2d-generator-spec/1"
GENERATOR_VERSION: Final = "mesc-pilot-01-b2d-generator/1"

#: The exact ``source_record_hash`` domain prefix (FD-B2D-3).
SOURCE_RECORD_DOMAIN: Final = "mesc-pilot-01-b2d-source-record-v1"

#: The exact evidence-reference namespace for the leakage scenarios (FD-B2D-6 §8.4).
SCENARIO_REFERENCE_PREFIX: Final = "mesc-pilot-01-b2d-leakage-scenario/1/"

ROW_COUNT: Final = 1000

DECISIONS: Final[tuple[Decision, ...]] = ("yes", "no", "maybe")
PARTITIONS: Final[tuple[Partition, ...]] = ("train", "validation", "test")

PARTITION_TOTALS: Final[Mapping[str, int]] = {"train": 700, "validation": 150, "test": 150}
LABEL_TOTALS: Final[Mapping[str, int]] = {"yes": 552, "no": 338, "maybe": 110}

#: The ratified 3x3 target matrix, indexed decision then partition (FD-B2D-3).
RATIFIED_MATRIX: Final[Mapping[str, Mapping[str, int]]] = {
    "yes": {"train": 386, "validation": 83, "test": 83},
    "no": {"train": 237, "validation": 50, "test": 51},
    "maybe": {"train": 77, "validation": 17, "test": 16},
}

#: The three ratified fixture identifiers, in their canonical qualification order.
EXACT_REFERENCE_FIXTURE_ID: Final = "exact-reference-1000-v1"
CONSTRAINT_STRESS_FIXTURE_ID: Final = "constraint-stress-1000-v1"
LEAKAGE_POSITIVE_FIXTURE_ID: Final = "leakage-positive-v1"
FIXTURE_IDS: Final[tuple[str, ...]] = (
    EXACT_REFERENCE_FIXTURE_ID,
    CONSTRAINT_STRESS_FIXTURE_ID,
    LEAKAGE_POSITIVE_FIXTURE_ID,
)

#: The exact detection-method tuple in the ratified caller order (FD-B2D-6 §8.3).
DETECTION_METHODS: Final[tuple[str, ...]] = (
    "exact_context_equality",
    "exact_example_identity",
    "exact_question_equality",
    "exact_source_document_identity",
    "normalize_question",
    "normalized_question_equality",
    "token_set_jaccard",
    "tokenize",
)


class IndependentAllocationInfeasibleError(Exception):
    """Raised when the independent oracle cannot place a group without crossing.

    This is the *oracle's* fail-closed signal.  It is deliberately not a B1,
    B2A, B2B or B2C exception, so the qualification suite can always tell an
    independent-oracle refusal apart from the accepted implementation's own
    typed refusal.
    """


# ---------------------------------------------------------------------------
# Independent D6 ranking oracle (FD-B2D-4 §6.2, FD-B2D-10)
# ---------------------------------------------------------------------------


def d6_payload(decision: str, document_id: str) -> dict[str, str]:
    """Return the exact ratified D6 partition-key payload."""
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "seed": SEED,
        "source_document_id": document_id,
        "stratum": decision,
    }


def d6_serialized(decision: str, document_id: str) -> bytes:
    """Return the D6 payload under the ratified **no-terminal-LF** contract.

    Recursively sorted keys, UTF-8, ``ensure_ascii=False``, ``allow_nan=False``,
    separators ``(",", ":")``, no indentation, no BOM and no terminal newline.
    This is spelled out locally rather than delegated, because delegating to the
    implementation under test is exactly the circularity FD-B2D-10 forbids.
    """
    text = json.dumps(
        d6_payload(decision, document_id),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        indent=None,
    )
    return text.encode("utf-8")


def d6_partition_key(decision: str, document_id: str) -> str:
    """Return the independently computed lowercase D6 partition key."""
    return hashlib.sha256(d6_serialized(decision, document_id)).hexdigest()


def source_document_id(fixture_id: str, decision: str, candidate_ordinal: int) -> str:
    """Return the deterministic candidate source-document identifier."""
    return f"mesc-b2d-{fixture_id}-{decision}-doc-{candidate_ordinal:04d}"


def original_example_id(fixture_id: str, row_ordinal: int) -> str:
    """Return the exact ratified original-example identifier (FD-B2D-3)."""
    return f"mesc-b2d-{fixture_id}-example-{row_ordinal:04d}"


def source_record_hash(fixture_id: str, original_id: str, document_id: str, decision: str) -> str:
    """Return the lowercase SHA-256 of the exact ratified ASCII domain string."""
    domain = f"{SOURCE_RECORD_DOMAIN}|{fixture_id}|{original_id}|{document_id}|{decision}"
    return hashlib.sha256(domain.encode("utf-8")).hexdigest()


@cache
def ranked_candidates(fixture_id: str, decision: str, candidate_count: int) -> tuple[str, ...]:
    """Return the candidate documents in independent D6 rank order.

    Sorted by digest ascending, then source-document identifier ascending, then
    the defensive candidate ordinal ascending (FD-B2D-4 §6.2 step 4).
    """
    candidates = sorted(
        (
            d6_partition_key(decision, source_document_id(fixture_id, decision, ordinal)),
            source_document_id(fixture_id, decision, ordinal),
            ordinal,
        )
        for ordinal in range(candidate_count)
    )
    return tuple(document for _, document, _ in candidates)


# ---------------------------------------------------------------------------
# exact-reference-1000-v1 group-size vectors (FD-B2D-4 §6.1)
# ---------------------------------------------------------------------------


def _repeat(size: int, count: int) -> tuple[int, ...]:
    """Return ``count`` groups of ``size`` — the ``13x29`` notation, spelled out."""
    return (size,) * count


#: Founder-frozen group-size vectors, keyed decision then partition.
GROUP_SIZE_VECTORS: Final[Mapping[str, Mapping[str, tuple[int, ...]]]] = {
    "yes": {
        "train": (*_repeat(13, 29), 8, 1),
        "validation": (*_repeat(13, 6), 5),
        "test": (*_repeat(13, 6), 5),
    },
    "no": {
        "train": (*_repeat(13, 18), 2, 1),
        "validation": (*_repeat(13, 3), 8, 3),
        "test": (*_repeat(13, 3), 8, 3, 1),
    },
    "maybe": {
        "train": (*_repeat(13, 5), 8, 3, 1),
        "validation": (13, 3, 1),
        "test": (13, 3),
    },
}

#: The six group sizes FD-B2-7 Fixture A requires to be present.
REQUIRED_GROUP_SIZES: Final[tuple[int, ...]] = (1, 2, 3, 5, 8, 13)

#: Founder-frozen group counts per decision, keyed by fixture.
GROUP_COUNTS: Final[Mapping[str, Mapping[str, int]]] = {
    EXACT_REFERENCE_FIXTURE_ID: {"yes": 45, "no": 31, "maybe": 13},
    CONSTRAINT_STRESS_FIXTURE_ID: {"yes": 276, "no": 169, "maybe": 55},
    LEAKAGE_POSITIVE_FIXTURE_ID: {"yes": 551, "no": 338, "maybe": 110},
}

#: Founder-frozen total group counts, keyed by fixture.
TOTAL_GROUP_COUNTS: Final[Mapping[str, int]] = {
    EXACT_REFERENCE_FIXTURE_ID: 89,
    CONSTRAINT_STRESS_FIXTURE_ID: 500,
    LEAKAGE_POSITIVE_FIXTURE_ID: 999,
}


def concatenated_size_vector(decision: str) -> tuple[int, ...]:
    """Return the train, validation and test vectors concatenated in that order."""
    vectors = GROUP_SIZE_VECTORS[decision]
    return (*vectors["train"], *vectors["validation"], *vectors["test"])


# ---------------------------------------------------------------------------
# leakage-positive-v1 frozen structural selection (FD-B2D-6)
# ---------------------------------------------------------------------------

#: The lowest-indexed candidate whose independently computed D6 rank places the
#: two-example group strictly inside a partition run — never touching either
#: edge, and therefore never straddling a boundary.  Derived once in untracked
#: implementation scratch, then frozen here as literal constants.
PAIR_CANDIDATE_ORDINAL: Final = 0
PAIR_SOURCE_DOCUMENT_ID: Final = "mesc-b2d-leakage-positive-v1-yes-doc-0000"
PAIR_DECISION: Final = "yes"
PAIR_D6_RANK: Final = 230
PAIR_PARTITION: Final = "train"
PAIR_ROW_ORDINALS: Final[tuple[int, int]] = (230, 231)


# ---------------------------------------------------------------------------
# Fixture plans
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class GroupPlan:
    """One independently derived source-document group, in D6 rank order."""

    source_document_id: str
    decision: Decision
    row_ordinals: tuple[int, ...]

    @property
    def size(self) -> int:
        return len(self.row_ordinals)


@dataclass(frozen=True, slots=True)
class FixturePlan:
    """The complete independently derived plan for one qualification fixture."""

    fixture_id: str
    groups: tuple[GroupPlan, ...]
    ordered_rows: tuple[OrderedExampleRow, ...]
    source_labels: tuple[SourceLabelRow, ...]

    @property
    def group_count(self) -> int:
        return len(self.groups)

    def groups_for(self, decision: str) -> tuple[GroupPlan, ...]:
        return tuple(group for group in self.groups if group.decision == decision)

    def group_sizes(self) -> tuple[int, ...]:
        return tuple(group.size for group in self.groups)

    def decision_of_row(self) -> dict[int, str]:
        return {ordinal: group.decision for group in self.groups for ordinal in group.row_ordinals}

    def document_of_row(self) -> dict[int, str]:
        return {
            ordinal: group.source_document_id
            for group in self.groups
            for ordinal in group.row_ordinals
        }


def _size_vector(fixture_id: str, decision: str, documents: Sequence[str]) -> tuple[int, ...]:
    """Return the group sizes bound positionally to the ranked candidates."""
    if fixture_id == EXACT_REFERENCE_FIXTURE_ID:
        return concatenated_size_vector(decision)
    if fixture_id == CONSTRAINT_STRESS_FIXTURE_ID:
        return _repeat(2, len(documents))
    return tuple(2 if document == PAIR_SOURCE_DOCUMENT_ID else 1 for document in documents)


@cache
def build_plan(fixture_id: str) -> FixturePlan:
    """Return the independently derived plan for one fixture.

    Row ordinals are generated consecutively across all groups, walking the
    decisions in the ratified order ``yes``, ``no``, ``maybe`` and, within each
    decision, the candidates in independent D6 rank order.  Nothing here calls
    ``rank_groups``, ``allocate_indivisible_groups`` or ``FixtureSplitFacade``.
    """
    if fixture_id not in FIXTURE_IDS:
        raise ValueError(f"unknown qualification fixture id: {fixture_id!r}")
    counts = GROUP_COUNTS[fixture_id]
    groups: list[GroupPlan] = []
    rows: list[OrderedExampleRow] = []
    labels: list[SourceLabelRow] = []
    next_ordinal = 0
    for decision in DECISIONS:
        documents = ranked_candidates(fixture_id, decision, counts[decision])
        sizes = _size_vector(fixture_id, decision, documents)
        if len(sizes) != len(documents):
            raise ValueError(f"{fixture_id}: size vector does not match the candidate count")
        for document, size in zip(documents, sizes, strict=True):
            ordinals: list[int] = []
            for _ in range(size):
                original_id = original_example_id(fixture_id, next_ordinal)
                rows.append(
                    OrderedExampleRow(
                        original_example_id=original_id,
                        row_ordinal=next_ordinal,
                        source_document_id=document,
                    )
                )
                labels.append(
                    SourceLabelRow(
                        dataset_id=DATASET_ID,
                        dataset_revision=DATASET_REVISION,
                        configuration=CONFIGURATION,
                        original_example_id=original_id,
                        source_document_id=document,
                        decision=decision,
                        source_record_hash=source_record_hash(
                            fixture_id, original_id, document, decision
                        ),
                    )
                )
                ordinals.append(next_ordinal)
                next_ordinal += 1
            groups.append(
                GroupPlan(
                    source_document_id=document,
                    decision=decision,
                    row_ordinals=tuple(ordinals),
                )
            )
    return FixturePlan(
        fixture_id=fixture_id,
        groups=tuple(groups),
        ordered_rows=tuple(rows),
        source_labels=tuple(labels),
    )


def independent_partition_by_row(plan: FixturePlan) -> dict[int, str]:
    """Return the independently derived partition of every row ordinal.

    The walk is the ratified exact-target one: for each decision, consume the
    ranked groups against ``train``, then ``validation``, then ``test``.  A group
    that would cross a boundary raises
    :class:`IndependentAllocationInfeasibleError`; the oracle never splits,
    reorders or applies a tolerance.
    """
    placement: dict[int, str] = {}
    for decision in DECISIONS:
        remaining = [RATIFIED_MATRIX[decision][partition] for partition in PARTITIONS]
        index = 0
        for group in plan.groups_for(decision):
            while remaining[index] == 0 and index < len(PARTITIONS) - 1:
                index += 1
            if group.size > remaining[index]:
                raise IndependentAllocationInfeasibleError(
                    f"group {group.source_document_id!r} of size {group.size} would cross the "
                    f"{decision}/{PARTITIONS[index]} boundary with {remaining[index]} "
                    f"places remaining"
                )
            for ordinal in group.row_ordinals:
                placement[ordinal] = PARTITIONS[index]
            remaining[index] -= group.size
        if any(value != 0 for value in remaining):
            raise IndependentAllocationInfeasibleError(
                f"independent allocation did not exhaust the targets for {decision!r}"
            )
    return placement


def independent_label_matrix(plan: FixturePlan) -> dict[str, dict[str, int]]:
    """Return the independently derived partition-by-label matrix."""
    placement = independent_partition_by_row(plan)
    decisions = plan.decision_of_row()
    matrix: dict[str, dict[str, int]] = {}
    for partition in PARTITIONS:
        # Built with explicit ``str`` keys rather than ``dict.fromkeys`` so every
        # decision is an explicit zero and the mapping stays plainly string-keyed.
        row: dict[str, int] = {}
        for decision in DECISIONS:
            row[decision] = 0
        matrix[partition] = row
    for ordinal, placed in placement.items():
        matrix[placed][decisions[ordinal]] += 1
    return matrix


# ---------------------------------------------------------------------------
# Generator-specification identity (FD-B2D-3 §5.1)
# ---------------------------------------------------------------------------


def _grouping_contract(fixture_id: str) -> dict[str, object]:
    counts = GROUP_COUNTS[fixture_id]
    counts_document = {decision: counts[decision] for decision in sorted(counts)}
    if fixture_id == EXACT_REFERENCE_FIXTURE_ID:
        return {
            "kind": "explicit-group-size-vectors",
            "group_count": TOTAL_GROUP_COUNTS[fixture_id],
            "group_counts_by_decision": counts_document,
            "group_size_vectors": {
                decision: {
                    partition: list(GROUP_SIZE_VECTORS[decision][partition])
                    for partition in PARTITIONS
                }
                for decision in DECISIONS
            },
            "required_group_sizes": list(REQUIRED_GROUP_SIZES),
        }
    if fixture_id == CONSTRAINT_STRESS_FIXTURE_ID:
        return {
            "kind": "uniform-two-example-groups",
            "group_count": TOTAL_GROUP_COUNTS[fixture_id],
            "group_counts_by_decision": counts_document,
            "uniform_group_size": 2,
            "exact_matrix_feasible": False,
        }
    return {
        "kind": "single-two-example-group-and-singletons",
        "group_count": TOTAL_GROUP_COUNTS[fixture_id],
        "group_counts_by_decision": counts_document,
        "multi_example_group_count": 1,
        "multi_example_group_size": 2,
        "singleton_group_count": 998,
    }


def _leakage_scenario_contract(fixture_id: str) -> dict[str, object]:
    if fixture_id != LEAKAGE_POSITIVE_FIXTURE_ID:
        return {"kind": "none", "scenario_count": 0, "scenario_slugs": []}
    return {
        "kind": "nine-deterministic-scenarios",
        "scenario_count": 9,
        "false_positive_count": 3,
        "unresolved_count": 6,
        "scenario_slugs": [scenario.slug for scenario in LEAKAGE_SCENARIOS],
    }


def generator_spec_document(fixture_id: str) -> dict[str, object]:
    """Return the exact fourteen-member generator specification (FD-B2D-3 §5.1).

    The document binds the **specification** only.  It carries no fixture
    digest, request identifier, split hash, fingerprint, runtime, operating
    system, Python version, timestamp, path or workflow identifier, so it is
    computable before the facade runs.
    """
    if fixture_id not in FIXTURE_IDS:
        raise ValueError(f"unknown qualification fixture id: {fixture_id!r}")
    return {
        "schema": GENERATOR_SPEC_SCHEMA,
        "fixture_id": fixture_id,
        "fixture_schema_version": FIXTURE_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "dataset_id": DATASET_ID,
        "dataset_revision": DATASET_REVISION,
        "configuration": CONFIGURATION,
        "transformation_version": TRANSFORMATION_VERSION,
        "policy_id": POLICY_ID,
        "row_count": ROW_COUNT,
        "partition_totals": {partition: PARTITION_TOTALS[partition] for partition in PARTITIONS},
        "label_totals": {decision: LABEL_TOTALS[decision] for decision in DECISIONS},
        "grouping_contract": _grouping_contract(fixture_id),
        "leakage_scenario_contract": _leakage_scenario_contract(fixture_id),
    }


def synthetic_identity_proof(fixture_id: str) -> str:
    """Return the ``mesc-synthetic-batch/1`` proof over the generator specification."""
    return SYNTHETIC_PROOF_PREFIX + sha256_of_bytes(
        canonical_json_bytes(generator_spec_document(fixture_id))
    )


# ---------------------------------------------------------------------------
# Independent global minimum-deviation oracle (FD-B2D-5 §7.2)
# ---------------------------------------------------------------------------

#: Enumeration radius for the four free deviation cells.  Any feasible matrix
#: whose squared-deviation score is at most 6 has every individual cell
#: deviation bounded by ``|d| <= 2``, because ``3 ** 2 = 9 > 6``; and a matrix is
#: uniquely determined by its free 2x2 block once the row and column totals are
#: fixed.  A radius of 6 therefore strictly contains every matrix scoring 6 or
#: better, which is what makes this bounded enumeration a complete derivation.
FREE_BLOCK_RADIUS: Final = 6

#: The proven per-cell deviation bound implied by a score of at most 6.
SCORE_SIX_CELL_BOUND: Final = 2

#: Founder-frozen minimum squared-deviation score for ``constraint-stress-1000-v1``.
MINIMUM_DEVIATION_SCORE: Final = 6

#: Founder-frozen lexicographic winner — Matrix A.
MATRIX_A: Final[tuple[int, ...]] = (386, 82, 84, 238, 50, 50, 76, 18, 16)

#: Founder-frozen score-6 runner-up — Matrix B.
MATRIX_B: Final[tuple[int, ...]] = (386, 84, 82, 236, 50, 52, 78, 16, 16)


@dataclass(frozen=True, slots=True)
class MinimumDeviationResult:
    """The complete outcome of the independent minimum-deviation derivation."""

    minimum_score: int
    optimal_matrices: tuple[tuple[int, ...], ...]
    feasible_count: int
    exact_matrix_feasible: bool

    @property
    def selected(self) -> tuple[int, ...]:
        """Return the lexicographically smallest minimum-deviation vector."""
        return self.optimal_matrices[0]


def ratified_vector() -> tuple[int, ...]:
    """Return the ratified target matrix flattened in the controlling order."""
    return tuple(
        RATIFIED_MATRIX[decision][partition] for decision in DECISIONS for partition in PARTITIONS
    )


def odd_target_cells() -> tuple[tuple[str, str, int], ...]:
    """Return every odd-valued cell of the ratified target matrix."""
    return tuple(
        (decision, partition, RATIFIED_MATRIX[decision][partition])
        for decision in DECISIONS
        for partition in PARTITIONS
        if RATIFIED_MATRIX[decision][partition] % 2 == 1
    )


def matrix_from_free_block(deltas: Sequence[int]) -> tuple[int, ...] | None:
    """Return the feasible matrix implied by four free deviation cells, or ``None``.

    The free block is ``yes/train``, ``yes/validation``, ``no/train`` and
    ``no/validation``.  Every remaining cell is forced by the exact row and
    column totals, so those four values determine the matrix completely and the
    totals hold by construction.  ``None`` marks a matrix that is negative
    somewhere or has an odd cell, and is therefore not feasible for indivisible
    two-example groups.
    """
    yes_train, yes_validation, no_train, no_validation = deltas
    full = (
        yes_train,
        yes_validation,
        -(yes_train + yes_validation),
        no_train,
        no_validation,
        -(no_train + no_validation),
        -(yes_train + no_train),
        -(yes_validation + no_validation),
        yes_train + yes_validation + no_train + no_validation,
    )
    matrix = tuple(base + delta for base, delta in zip(ratified_vector(), full, strict=True))
    if any(value < 0 or value % 2 == 1 for value in matrix):
        return None
    return matrix


def squared_deviation(matrix: Sequence[int]) -> int:
    """Return the sum of squared deviations from the ratified target matrix."""
    return sum((value - base) ** 2 for value, base in zip(matrix, ratified_vector(), strict=True))


@cache
def minimum_deviation_result() -> MinimumDeviationResult:
    """Derive every minimum-deviation feasible matrix independently.

    A feasible matrix has exact row totals ``552 / 338 / 110``, exact column
    totals ``700 / 150 / 150`` and a non-negative **even** value in every cell.
    The row and column totals are enforced structurally by the free-block
    construction; parity and non-negativity are filtered explicitly.
    """
    span = range(-FREE_BLOCK_RADIUS, FREE_BLOCK_RADIUS + 1)
    feasible: list[tuple[int, tuple[int, ...]]] = []
    for deltas in product(span, span, span, span):
        matrix = matrix_from_free_block(deltas)
        if matrix is not None:
            feasible.append((squared_deviation(matrix), matrix))
    minimum = min(score for score, _ in feasible)
    optimal = sorted(matrix for score, matrix in feasible if score == minimum)
    return MinimumDeviationResult(
        minimum_score=minimum,
        optimal_matrices=tuple(optimal),
        feasible_count=len(feasible),
        exact_matrix_feasible=any(matrix == ratified_vector() for _, matrix in feasible),
    )


def matrix_totals(matrix: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the row totals and column totals of a flattened 3x3 matrix."""
    rows = tuple(sum(matrix[index * 3 : index * 3 + 3]) for index in range(3))
    columns = tuple(sum(matrix[offset::3]) for offset in range(3))
    return rows, columns


# ---------------------------------------------------------------------------
# leakage-positive-v1 scenarios (FD-B2D-6 §8.1 .. §8.4)
# ---------------------------------------------------------------------------

_BASE_QUESTION: Final = "does alpha therapy reduce beta outcome?"

#: Scenario 4's left surface is composed from explicit code points rather than
#: written as a literal line, because its two leading and two trailing ASCII
#: spaces are significant and invisible whitespace must never depend on how this
#: file is copied, trimmed or reformatted.  The composition is, in order:
#: U+0020, U+0020, "Does", U+00A0, "ALPHA", U+0020, the remaining words, U+0020,
#: U+0020.
SCENARIO_FOUR_LEFT: Final = (
    "\u0020\u0020Does\u00a0ALPHA\u0020Therapy reduce beta outcome?\u0020\u0020"
)

#: ASCII space, then horizontal tab, then line feed.
SCENARIO_NINE_LEFT: Final = "\u0020\u0009\u000a"

#: EM SPACE, then NO-BREAK SPACE.
SCENARIO_NINE_RIGHT: Final = "\u2003\u00a0"

_JACCARD_TOKENS: Final[tuple[str, ...]] = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lambda",
)
_CONTEXT_TOKENS: Final[tuple[str, ...]] = tuple(f"ctx{index:02d}" for index in range(1, 21))
_EXACT_CONTEXT: Final = "alpha therapy trial context for beta outcome"


@dataclass(frozen=True, slots=True)
class LeakageScenario:
    """One frozen deterministic leakage scenario.

    ``left_surface`` and ``right_surface`` are the raw synthetic question or
    context strings.  They are inputs to the accepted B2B primitives and are
    deliberately absent from every promotable value: the finding carries only
    allowlisted ``shared_surface`` markers.
    """

    index: int
    slug: str
    finding_type: str
    surface_kind: str
    left_surface: str
    right_surface: str
    example_ids: tuple[str, ...]
    source_document_ids: tuple[str, ...]
    partitions: tuple[str, ...]
    row_ordinals: tuple[int, ...]
    score_representation: str
    shared_surface: tuple[str, ...]
    classification: str
    evidence_reference: str | None

    @property
    def evidence_reference_outcome(self) -> str:
        """Return the frozen evidence-reference outcome, for the qualification report."""
        return "absent" if self.evidence_reference is None else self.evidence_reference


#: Frozen derived identities for the same-partition self-identity control:
#: the lowest row ordinal that is not a member of the two-example group.
SCENARIO_ONE_ROW_ORDINAL: Final = 0
SCENARIO_ONE_SOURCE_DOCUMENT_ID: Final = "mesc-b2d-leakage-positive-v1-yes-doc-0411"
SCENARIO_ONE_EXAMPLE_ID: Final = (
    "mesc-pilot-01:11d5d817ea798203d08bda0e4d5eaf66813bd43db85400eb5fcffde47bd5083e"
)
SCENARIO_ONE_PARTITION: Final = "train"

#: Frozen derived identities of the single homogeneous two-example group.
PAIR_EXAMPLE_IDS: Final[tuple[str, str]] = (
    "mesc-pilot-01:9f998468243a1418dc15fbc7d1100eb447d5f2d644917e306f3d183d2787ef26",
    "mesc-pilot-01:1e5080b4656e07a69aaf121dca7d07ac55f92ec7387765e21fa9fd28a726b260",
)

#: Frozen scenario pairs for scenarios 3 through 9, selected as the ascending
#: unused ``train`` example paired with the ascending unused ``test`` example.
#: Each entry is ``(train ordinal, train document, train example, test ordinal,
#: test document, test example)``.
SCENARIO_PAIRS: Final[tuple[tuple[int, str, str, int, str, str], ...]] = (
    (
        1,
        "mesc-b2d-leakage-positive-v1-yes-doc-0033",
        "mesc-pilot-01:6bc9dca66f8f56b2e1e35b5bb64d1ce4d6995c606ecc51b5760cbbc75d2716a9",
        469,
        "mesc-b2d-leakage-positive-v1-yes-doc-0255",
        "mesc-pilot-01:8b24fba0026b3d66627366eab88fa94e48ea15f58b393a9ac753b2a4d4a3c2af",
    ),
    (
        2,
        "mesc-b2d-leakage-positive-v1-yes-doc-0311",
        "mesc-pilot-01:5a3186c8e8711cdaed9ce84adfbd3a9293c015539a60853ecc30fc266c7f636b",
        470,
        "mesc-b2d-leakage-positive-v1-yes-doc-0129",
        "mesc-pilot-01:78b7f0589e92cb810ad3eff4d252904c670c80d8a484f49b5165b5c6ef3af1cd",
    ),
    (
        3,
        "mesc-b2d-leakage-positive-v1-yes-doc-0046",
        "mesc-pilot-01:2c89bf43b5cc3a918ebc145f1a8d0349af7d14e951551b65c18fda3b13b5f08b",
        471,
        "mesc-b2d-leakage-positive-v1-yes-doc-0317",
        "mesc-pilot-01:05966b4e20d93fa62685360f9c93c3a8bade6eff9faef041a5ecb19dd2ba3e5e",
    ),
    (
        4,
        "mesc-b2d-leakage-positive-v1-yes-doc-0429",
        "mesc-pilot-01:2813e6a99b6041c7f126ffe2db15f56e4924616c4852a9bb3c7836d13c0a0b38",
        472,
        "mesc-b2d-leakage-positive-v1-yes-doc-0008",
        "mesc-pilot-01:aa5b027058230cc1c0972d54216ae78221d4a3d3ada9b59a676972f314bfbde0",
    ),
    (
        5,
        "mesc-b2d-leakage-positive-v1-yes-doc-0380",
        "mesc-pilot-01:ed27b84da021829cfcb8449987419a09caa794ed5562621fe2d9fe3bb5925e2d",
        473,
        "mesc-b2d-leakage-positive-v1-yes-doc-0047",
        "mesc-pilot-01:d1321e7dfb2a20868b4a55e2c76051903586310d1db66b17507fc7176cff5ca0",
    ),
    (
        6,
        "mesc-b2d-leakage-positive-v1-yes-doc-0323",
        "mesc-pilot-01:ccec3bdf10189e59e604425fcfe277121c44f31a912add591913a33178efe910",
        474,
        "mesc-b2d-leakage-positive-v1-yes-doc-0072",
        "mesc-pilot-01:c140bc900237a6943420fc93dafdee3234d0f3a18fc8b70e700a72c59c1458b1",
    ),
    (
        7,
        "mesc-b2d-leakage-positive-v1-yes-doc-0111",
        "mesc-pilot-01:d189723ce9fea9dc5901e3444ede482715f2dac84b31c5f0c3261bc9cab190b4",
        475,
        "mesc-b2d-leakage-positive-v1-yes-doc-0017",
        "mesc-pilot-01:61ef5e60e58fb4f5cd013c1a56af302a7090de28201f9e715a931d285bce0666",
    ),
)


def _pair_scenario(
    index: int,
    slug: str,
    finding_type: str,
    surface_kind: str,
    left_surface: str,
    right_surface: str,
    score_representation: str,
    shared_surface: tuple[str, ...],
    classification: str,
    evidence_reference: str | None,
) -> LeakageScenario:
    """Return one scenario bound to the frozen pair for scenarios 3 through 9."""
    left_ordinal, left_document, left_example, right_ordinal, right_document, right_example = (
        SCENARIO_PAIRS[index - 3]
    )
    return LeakageScenario(
        index=index,
        slug=slug,
        finding_type=finding_type,
        surface_kind=surface_kind,
        left_surface=left_surface,
        right_surface=right_surface,
        example_ids=tuple(sorted((left_example, right_example))),
        source_document_ids=tuple(sorted((left_document, right_document))),
        partitions=("test", "train"),
        row_ordinals=(left_ordinal, right_ordinal),
        score_representation=score_representation,
        shared_surface=shared_surface,
        classification=classification,
        evidence_reference=evidence_reference,
    )


LEAKAGE_SCENARIOS: Final[tuple[LeakageScenario, ...]] = (
    LeakageScenario(
        index=1,
        slug="exact-example-self-control",
        finding_type="exact_example",
        surface_kind="identity",
        left_surface="",
        right_surface="",
        example_ids=(SCENARIO_ONE_EXAMPLE_ID,),
        source_document_ids=(SCENARIO_ONE_SOURCE_DOCUMENT_ID,),
        partitions=(SCENARIO_ONE_PARTITION,),
        row_ordinals=(SCENARIO_ONE_ROW_ORDINAL,),
        score_representation="none",
        shared_surface=("example_id",),
        classification="false_positive",
        evidence_reference=f"{SCENARIO_REFERENCE_PREFIX}exact-example-self-control",
    ),
    LeakageScenario(
        index=2,
        slug="expected-same-group-source-document",
        finding_type="source_document",
        surface_kind="identity",
        left_surface="",
        right_surface="",
        example_ids=tuple(sorted(PAIR_EXAMPLE_IDS)),
        source_document_ids=(PAIR_SOURCE_DOCUMENT_ID,),
        partitions=(PAIR_PARTITION,),
        row_ordinals=PAIR_ROW_ORDINALS,
        score_representation="none",
        shared_surface=("source_document_id",),
        classification="false_positive",
        evidence_reference=f"{SCENARIO_REFERENCE_PREFIX}expected-same-group-source-document",
    ),
    _pair_scenario(
        3,
        "exact-question-equality",
        "exact_question",
        "question",
        _BASE_QUESTION,
        _BASE_QUESTION,
        "none",
        ("question_bytes",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        4,
        "normalized-question-equality",
        "normalized_question",
        "question",
        SCENARIO_FOUR_LEFT,
        _BASE_QUESTION,
        "none",
        ("normalized_question",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        5,
        "question-jaccard-at-threshold",
        "near_duplicate_question",
        "question",
        " ".join(_JACCARD_TOKENS[:10]),
        " ".join(_JACCARD_TOKENS[:9]),
        "jaccard:9/10",
        ("question_token_set",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        6,
        "question-jaccard-above-threshold",
        "near_duplicate_question",
        "question",
        " ".join(_JACCARD_TOKENS[:11]),
        " ".join(_JACCARD_TOKENS[:10]),
        "jaccard:10/11",
        ("question_token_set",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        7,
        "exact-context-equality",
        "context_overlap",
        "context",
        _EXACT_CONTEXT,
        _EXACT_CONTEXT,
        "none",
        ("context_bytes",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        8,
        "approximate-context-overlap",
        "context_overlap",
        "context",
        " ".join(_CONTEXT_TOKENS),
        " ".join(_CONTEXT_TOKENS[:19]),
        "jaccard:19/20",
        ("context_token_set",),
        "unresolved",
        None,
    ),
    _pair_scenario(
        9,
        "whitespace-only-control",
        "empty_normalized_question",
        "question",
        SCENARIO_NINE_LEFT,
        SCENARIO_NINE_RIGHT,
        "not_evaluable",
        ("empty_normalized_question",),
        "false_positive",
        f"{SCENARIO_REFERENCE_PREFIX}whitespace-only-control",
    ),
)

#: The distinctive raw substrings that must never reach a promotable surface.
RAW_SURFACE_PROBES: Final[tuple[str, ...]] = (
    _BASE_QUESTION,
    SCENARIO_FOUR_LEFT,
    _EXACT_CONTEXT,
    " ".join(_CONTEXT_TOKENS),
    "alpha",
    "gamma",
    "delta",
    "epsilon",
    "kappa",
    "lambda",
    "therapy",
    "outcome",
    "ctx01",
    "ctx20",
)


def leakage_findings() -> tuple[LeakageFinding, ...]:
    """Return the nine frozen findings, built with the accepted B2B constructor."""
    return tuple(
        LeakageFinding.create(
            finding_type=scenario.finding_type,
            example_ids=scenario.example_ids,
            source_document_ids=scenario.source_document_ids,
            partitions=scenario.partitions,
            score_representation=scenario.score_representation,
            classification=scenario.classification,
            shared_surface=scenario.shared_surface,
            evidence_reference=scenario.evidence_reference,
        )
        for scenario in LEAKAGE_SCENARIOS
    )


# ---------------------------------------------------------------------------
# Assembled fixture inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FixtureInputs:
    """Every request input for one fixture except its three frozen identity values.

    ``fixture_sha256``, ``request_id`` and ``synthetic_identity_proof`` are
    deliberately absent: the qualification suite supplies them as committed
    literal constants, so no expected identity is ever taken from the code under
    test (FD-B2D-7, FD-B2D-10).
    """

    fixture_id: str
    fixture_namespace: str
    plan: FixturePlan
    partition_totals: Mapping[str, int]
    leakage_findings: tuple[LeakageFinding, ...]
    detection_methods: tuple[str, ...]
    execution_evidence_ref: str


def fixture_inputs(fixture_id: str) -> FixtureInputs:
    """Return the assembled synthetic inputs for one qualification fixture."""
    plan = build_plan(fixture_id)
    findings = leakage_findings() if fixture_id == LEAKAGE_POSITIVE_FIXTURE_ID else ()
    return FixtureInputs(
        fixture_id=fixture_id,
        fixture_namespace=FIXTURE_NAMESPACE_PREFIX + fixture_id,
        plan=plan,
        partition_totals={partition: PARTITION_TOTALS[partition] for partition in PARTITIONS},
        leakage_findings=findings,
        detection_methods=DETECTION_METHODS,
        execution_evidence_ref=EXECUTION_EVIDENCE_REF,
    )
