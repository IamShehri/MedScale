"""Leakage primitive contract tests for P01-04B2B (FD-B2B-1 .. FD-B2B-10).

Every input here is an obvious synthetic literal.  No real or canonical record,
dataset, registry, model or evidence root is touched, and no test constructs a
snapshot containing real text.

The golden vectors are written as explicit byte and digest literals derived by
hand from the adopted contract rather than recomputed with the code under test.
A vector regenerated from the implementation would agree with whatever the
implementation happens to do, which is exactly the drift these vectors exist to
detect.
"""

from __future__ import annotations

import builtins
import hashlib
import io
import math
import os
import pathlib
import socket
from pathlib import Path

import pytest

from medscale.mesc._canonical_json_v1 import (
    FloatingPointValueProhibitedError,
    canonical_json_bytes,
)
from medscale.mesc._leakage_v1 import (
    CONTEXT_OVERLAP_THRESHOLD_PERCENT,
    DETECTION_METHODS,
    FINDING_ID_PREFIX,
    FINDING_SCHEMA_VERSION,
    FINDING_TYPES,
    NEAR_DUPLICATE_THRESHOLD_PERCENT,
    SCORE_REPRESENTATION_NONE,
    SCORE_REPRESENTATION_NOT_EVALUABLE,
    SHARED_SURFACE_MARKERS,
    InvalidClassificationError,
    InvalidEvidenceReferenceError,
    InvalidFindingIdentifierError,
    InvalidFindingTypeError,
    InvalidPrimitiveInputError,
    InvalidReportInvariantError,
    InvalidScoreError,
    LeakageAuditReport,
    LeakageFinding,
    RawTextBearingValueError,
    SuppressionAttemptError,
    derive_finding_id,
    exact_context_equality,
    exact_example_identity,
    exact_question_equality,
    exact_source_document_identity,
    finding_identity_bytes,
    finding_identity_document,
    is_empty_normalized_question_pair,
    normalize_question,
    normalized_question_equality,
    question_token_set,
    token_set_jaccard,
    tokenize,
    validate_score_representation,
)

# --------------------------------------------------------------------------
# Golden vectors (literal; independently derived)
# --------------------------------------------------------------------------

GOLDEN_FINDING_TYPE = "near_duplicate_question"
GOLDEN_EXAMPLE_IDS = ("mesc-pilot-01:aaa", "mesc-pilot-01:bbb")
GOLDEN_SOURCE_DOCUMENT_IDS = ("doc-1",)
GOLDEN_PARTITIONS = ("train",)
GOLDEN_SCORE_REPRESENTATION = "jaccard:2/3"

GOLDEN_IDENTITY_DOCUMENT: dict[str, object] = {
    "schema": "mesc-pilot-01-leakage-finding/1",
    "finding_type": "near_duplicate_question",
    "example_ids": ["mesc-pilot-01:aaa", "mesc-pilot-01:bbb"],
    "source_document_ids": ["doc-1"],
    "partitions": ["train"],
    "score_representation": "jaccard:2/3",
}

GOLDEN_IDENTITY_BYTES = (
    b'{"example_ids":["mesc-pilot-01:aaa","mesc-pilot-01:bbb"],'
    b'"finding_type":"near_duplicate_question",'
    b'"partitions":["train"],'
    b'"schema":"mesc-pilot-01-leakage-finding/1",'
    b'"score_representation":"jaccard:2/3",'
    b'"source_document_ids":["doc-1"]}\n'
)

GOLDEN_DIGEST = "b9927be348a406b19d437c5c66e177ce4bd1941ec8f90e28ed1e08b3acafae39"

GOLDEN_FINDING_ID = (
    "mesc-pilot-01-leakage-finding/1:sha256:"
    "b9927be348a406b19d437c5c66e177ce4bd1941ec8f90e28ed1e08b3acafae39"
)


# --------------------------------------------------------------------------
# Synthetic helpers
# --------------------------------------------------------------------------


def _tokens(count: int, extra: str | None = None) -> frozenset[str]:
    """Return a synthetic token set of ``count`` shared tokens plus one optional extra."""
    tokens = {f"t{index}" for index in range(count)}
    if extra is not None:
        tokens.add(extra)
    return frozenset(tokens)


def _golden_finding() -> LeakageFinding:
    return LeakageFinding.create(
        finding_type=GOLDEN_FINDING_TYPE,
        example_ids=list(GOLDEN_EXAMPLE_IDS),
        source_document_ids=list(GOLDEN_SOURCE_DOCUMENT_IDS),
        partitions=list(GOLDEN_PARTITIONS),
        score_representation=GOLDEN_SCORE_REPRESENTATION,
        score=2 / 3,
        shared_surface=["question_token_set"],
        classification="unresolved",
    )


def _finding(
    *,
    example_ids: object = ("mesc-pilot-01:aaa",),
    finding_type: object = "exact_example",
    score_representation: object = SCORE_REPRESENTATION_NONE,
    classification: object = "unresolved",
    evidence_reference: object = None,
    score: object = None,
) -> LeakageFinding:
    return LeakageFinding.create(
        finding_type=finding_type,
        example_ids=example_ids,
        source_document_ids=("doc-1",),
        partitions=("train",),
        score_representation=score_representation,
        score=score,
        shared_surface=("example_id",),
        classification=classification,
        evidence_reference=evidence_reference,
    )


class _StrSubclass(str):
    """A ``str`` subclass, which the exact primitive domain must reject."""


# ==========================================================================
# 23.1 Canonical score representation
# ==========================================================================


def test_golden_vector_six_over_nine_reduces_to_two_thirds() -> None:
    left = frozenset(_tokens(6) | {"x1", "x2", "x3"})
    right = _tokens(6)
    result = token_set_jaccard(left, right)
    assert (result.intersection_size, result.union_size) == (6, 9)
    assert result.score_representation == "jaccard:2/3"
    assert result.score == pytest.approx(2 / 3)
    assert result.near_duplicate_threshold_passed is False


def test_golden_vector_nine_over_nine_is_full_match() -> None:
    tokens = _tokens(9)
    result = token_set_jaccard(tokens, tokens)
    assert (result.intersection_size, result.union_size) == (9, 9)
    assert result.score_representation == "jaccard:1/1"
    assert result.score == 1.0
    assert result.near_duplicate_threshold_passed is True
    assert result.context_overlap_threshold_passed is True


def test_golden_vector_two_non_empty_disjoint_sets() -> None:
    result = token_set_jaccard(frozenset({"a"}), frozenset({"b"}))
    assert result.intersection_size == 0
    assert result.union_size == 2
    assert result.score_representation == "jaccard:0/1"
    assert result.score == 0.0
    assert result.near_duplicate_threshold_passed is False
    assert result.context_overlap_threshold_passed is False


def test_exact_method_binds_none() -> None:
    finding = _finding(score_representation=SCORE_REPRESENTATION_NONE)
    assert finding.score_representation == "none"
    assert finding.score is None
    assert finding.identity_document()["score_representation"] == "none"


def test_non_evaluable_comparison_binds_not_evaluable() -> None:
    finding = _finding(
        finding_type="empty_normalized_question",
        score_representation=SCORE_REPRESENTATION_NOT_EVALUABLE,
    )
    assert finding.score_representation == "not_evaluable"
    assert finding.identity_document()["score_representation"] == "not_evaluable"


def test_canonical_finding_document_contains_no_float() -> None:
    finding = _golden_finding()
    assert finding.score == pytest.approx(2 / 3)
    document = finding.to_canonical_document()
    assert not any(isinstance(value, float) for value in document.values())
    assert "score" not in document
    assert document["score_representation"] == "jaccard:2/3"


def test_b2a_serialization_succeeds_for_score_bearing_findings() -> None:
    finding = _golden_finding()
    assert finding.to_canonical_bytes().endswith(b"\n")
    assert finding.identity_bytes() == GOLDEN_IDENTITY_BYTES


def test_direct_runtime_float_serialization_remains_prohibited() -> None:
    with pytest.raises(FloatingPointValueProhibitedError):
        canonical_json_bytes({"score": 2 / 3})


def test_runtime_score_cannot_change_canonical_bytes() -> None:
    with_score = _golden_finding()
    without_score = LeakageFinding.create(
        finding_type=GOLDEN_FINDING_TYPE,
        example_ids=GOLDEN_EXAMPLE_IDS,
        source_document_ids=GOLDEN_SOURCE_DOCUMENT_IDS,
        partitions=GOLDEN_PARTITIONS,
        score_representation=GOLDEN_SCORE_REPRESENTATION,
        score=None,
        shared_surface=["question_token_set"],
        classification="unresolved",
    )
    assert with_score.score != without_score.score
    assert with_score.identity_bytes() == without_score.identity_bytes()
    assert with_score.to_canonical_bytes() == without_score.to_canonical_bytes()
    assert with_score.finding_id == without_score.finding_id


@pytest.mark.parametrize(
    "representation",
    [
        "jaccard:0/0",
        "jaccard:2/4",
        "jaccard:+1/2",
        "jaccard:-1/2",
        "jaccard:01/2",
        "jaccard:1/02",
        "jaccard:3/2",
        "jaccard:1",
        "jaccard:1/2/3",
        "jaccard:/2",
        "jaccard:1/",
        "jaccard: 1/2",
        "jaccard:1_0/20",
        "Jaccard:1/2",
        "none ",
        "NOT_EVALUABLE",
        "",
    ],
)
def test_malformed_score_representations_fail_closed(representation: str) -> None:
    with pytest.raises(InvalidScoreError):
        validate_score_representation(representation)


def test_non_ascii_decimal_digits_are_rejected() -> None:
    # Arabic-Indic digits satisfy ``str.isdigit`` and ``int``; the unsigned
    # base-10 ASCII rule does not admit them.  Built with ``chr`` so the source
    # of this file stays ASCII-only and unambiguous.
    arabic_indic = f"jaccard:{chr(0x0661)}/{chr(0x0662)}"
    assert arabic_indic[len("jaccard:")].isdigit()
    with pytest.raises(InvalidScoreError):
        validate_score_representation(arabic_indic)


@pytest.mark.parametrize("representation", ["none", "not_evaluable", "jaccard:0/1", "jaccard:2/3"])
def test_well_formed_score_representations_are_accepted(representation: str) -> None:
    assert validate_score_representation(representation) == representation


# ==========================================================================
# 23.2 Finding-ID golden vectors
# ==========================================================================


def test_identity_document_matches_golden_vector() -> None:
    document = finding_identity_document(
        GOLDEN_FINDING_TYPE,
        GOLDEN_EXAMPLE_IDS,
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert document == GOLDEN_IDENTITY_DOCUMENT


def test_identity_document_has_exactly_six_members() -> None:
    document = finding_identity_document(
        GOLDEN_FINDING_TYPE,
        GOLDEN_EXAMPLE_IDS,
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert set(document) == {
        "schema",
        "finding_type",
        "example_ids",
        "source_document_ids",
        "partitions",
        "score_representation",
    }
    assert len(document) == 6


def test_identity_bytes_match_golden_vector() -> None:
    assert (
        finding_identity_bytes(
            GOLDEN_FINDING_TYPE,
            GOLDEN_EXAMPLE_IDS,
            GOLDEN_SOURCE_DOCUMENT_IDS,
            GOLDEN_PARTITIONS,
            GOLDEN_SCORE_REPRESENTATION,
        )
        == GOLDEN_IDENTITY_BYTES
    )


def test_identity_bytes_carry_exactly_one_terminal_line_feed() -> None:
    payload = finding_identity_bytes(
        GOLDEN_FINDING_TYPE,
        GOLDEN_EXAMPLE_IDS,
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert payload.endswith(b"\n")
    assert payload.count(b"\n") == 1
    assert b"\r" not in payload
    assert not payload.startswith(b"\xef\xbb\xbf")


def test_digest_and_finding_id_match_golden_vector() -> None:
    payload = finding_identity_bytes(
        GOLDEN_FINDING_TYPE,
        GOLDEN_EXAMPLE_IDS,
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert hashlib.sha256(payload).hexdigest() == GOLDEN_DIGEST
    finding_id = derive_finding_id(
        GOLDEN_FINDING_TYPE,
        GOLDEN_EXAMPLE_IDS,
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert finding_id == GOLDEN_FINDING_ID
    assert finding_id.startswith(FINDING_ID_PREFIX)
    assert len(finding_id[len(FINDING_ID_PREFIX) :]) == 64
    assert _golden_finding().finding_id == GOLDEN_FINDING_ID


def test_alias_key_produces_different_bytes_and_is_never_generated() -> None:
    aliased = dict(GOLDEN_IDENTITY_DOCUMENT)
    aliased["type"] = aliased.pop("finding_type")
    assert canonical_json_bytes(aliased) != GOLDEN_IDENTITY_BYTES
    assert hashlib.sha256(canonical_json_bytes(aliased)).hexdigest() != GOLDEN_DIGEST


def test_missing_identity_member_produces_different_bytes() -> None:
    missing = dict(GOLDEN_IDENTITY_DOCUMENT)
    del missing["partitions"]
    assert canonical_json_bytes(missing) != GOLDEN_IDENTITY_BYTES


def test_additional_identity_member_produces_different_bytes() -> None:
    extended = dict(GOLDEN_IDENTITY_DOCUMENT)
    extended["detected_at"] = "2026-01-01"
    assert canonical_json_bytes(extended) != GOLDEN_IDENTITY_BYTES


def test_manual_concatenation_cannot_substitute_for_canonical_serialization() -> None:
    manual = (
        b"mesc-pilot-01-leakage-finding/1"
        b"near_duplicate_question"
        b"mesc-pilot-01:aaamesc-pilot-01:bbb"
        b"doc-1"
        b"train"
        b"jaccard:2/3"
    )
    assert manual != GOLDEN_IDENTITY_BYTES
    assert hashlib.sha256(manual).hexdigest() != GOLDEN_DIGEST


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("finding_type", "context_overlap"),
        ("example_ids", ("mesc-pilot-01:aaa", "mesc-pilot-01:bbc")),
        ("source_document_ids", ("doc-2",)),
        ("partitions", ("test",)),
        ("score_representation", "jaccard:1/2"),
    ],
)
def test_semantic_change_changes_the_finding_id(field: str, value: object) -> None:
    arguments: dict[str, object] = {
        "finding_type": GOLDEN_FINDING_TYPE,
        "example_ids": GOLDEN_EXAMPLE_IDS,
        "source_document_ids": GOLDEN_SOURCE_DOCUMENT_IDS,
        "partitions": GOLDEN_PARTITIONS,
        "score_representation": GOLDEN_SCORE_REPRESENTATION,
    }
    arguments[field] = value
    changed = derive_finding_id(
        arguments["finding_type"],
        arguments["example_ids"],
        arguments["source_document_ids"],
        arguments["partitions"],
        arguments["score_representation"],
    )
    assert changed != GOLDEN_FINDING_ID


def test_repeated_execution_produces_identical_bytes_and_identifiers() -> None:
    payloads = {
        finding_identity_bytes(
            GOLDEN_FINDING_TYPE,
            GOLDEN_EXAMPLE_IDS,
            GOLDEN_SOURCE_DOCUMENT_IDS,
            GOLDEN_PARTITIONS,
            GOLDEN_SCORE_REPRESENTATION,
        )
        for _ in range(8)
    }
    identifiers = {_golden_finding().finding_id for _ in range(8)}
    assert payloads == {GOLDEN_IDENTITY_BYTES}
    assert identifiers == {GOLDEN_FINDING_ID}


@pytest.mark.parametrize(
    "identifier",
    [
        "sha256:" + GOLDEN_DIGEST,
        FINDING_ID_PREFIX + GOLDEN_DIGEST.upper(),
        FINDING_ID_PREFIX + GOLDEN_DIGEST[:-1],
        FINDING_ID_PREFIX + GOLDEN_DIGEST[:-1] + "z",
        FINDING_ID_PREFIX + "0" * 64,
    ],
)
def test_caller_supplied_identifier_is_regenerated_and_rejected(identifier: str) -> None:
    with pytest.raises(InvalidFindingIdentifierError):
        LeakageFinding(
            finding_id=identifier,
            finding_type=GOLDEN_FINDING_TYPE,
            example_ids=GOLDEN_EXAMPLE_IDS,
            source_document_ids=GOLDEN_SOURCE_DOCUMENT_IDS,
            partitions=GOLDEN_PARTITIONS,
            score_representation=GOLDEN_SCORE_REPRESENTATION,
            score=None,
            shared_surface=("question_token_set",),
            classification="unresolved",
            evidence_reference=None,
        )


# ==========================================================================
# 23.3 Identity-array multiplicity
# ==========================================================================


def test_permuted_example_ids_yield_identical_identity() -> None:
    forward = derive_finding_id(
        GOLDEN_FINDING_TYPE,
        ("mesc-pilot-01:aaa", "mesc-pilot-01:bbb"),
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    reversed_order = derive_finding_id(
        GOLDEN_FINDING_TYPE,
        ("mesc-pilot-01:bbb", "mesc-pilot-01:aaa"),
        GOLDEN_SOURCE_DOCUMENT_IDS,
        GOLDEN_PARTITIONS,
        GOLDEN_SCORE_REPRESENTATION,
    )
    assert forward == reversed_order == GOLDEN_FINDING_ID


def test_permuted_source_document_ids_yield_identical_identity() -> None:
    forward = derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1", "doc-2"), ("train",), "none"
    )
    backward = derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-2", "doc-1"), ("train",), "none"
    )
    assert forward == backward


def test_permuted_partitions_yield_identical_identity() -> None:
    forward = derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("train", "validation"), "none"
    )
    backward = derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("validation", "train"), "none"
    )
    assert forward == backward
    document = finding_identity_document(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("validation", "train"), "none"
    )
    assert document["partitions"] == ["train", "validation"]


@pytest.mark.parametrize(
    ("example_ids", "source_document_ids", "partitions"),
    [
        (("mesc-pilot-01:aaa", "mesc-pilot-01:aaa"), ("doc-1",), ("train",)),
        (("mesc-pilot-01:aaa",), ("doc-1", "doc-1"), ("train",)),
        (("mesc-pilot-01:aaa",), ("doc-1",), ("train", "train")),
    ],
)
def test_duplicate_identity_values_fail_closed(
    example_ids: tuple[str, ...],
    source_document_ids: tuple[str, ...],
    partitions: tuple[str, ...],
) -> None:
    with pytest.raises(InvalidFindingIdentifierError):
        derive_finding_id("exact_example", example_ids, source_document_ids, partitions, "none")


def test_duplicates_are_never_silently_deduplicated() -> None:
    unique = derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("train",), "none"
    )
    with pytest.raises(InvalidFindingIdentifierError):
        # A collapsing implementation would have produced ``unique`` here.
        derive_finding_id(
            "exact_example",
            ("mesc-pilot-01:aaa", "mesc-pilot-01:aaa"),
            ("doc-1",),
            ("train",),
            "none",
        )
    assert unique == derive_finding_id(
        "exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("train",), "none"
    )


@pytest.mark.parametrize(
    "container",
    [
        frozenset({"mesc-pilot-01:aaa"}),
        {"mesc-pilot-01:aaa"},
        "mesc-pilot-01:aaa",
        iter(("mesc-pilot-01:aaa",)),
        None,
    ],
)
def test_identity_arrays_reject_non_sequence_containers(container: object) -> None:
    with pytest.raises(InvalidFindingIdentifierError):
        derive_finding_id("exact_example", container, ("doc-1",), ("train",), "none")


def test_empty_identity_array_fails_closed() -> None:
    with pytest.raises(InvalidFindingIdentifierError):
        derive_finding_id("exact_example", (), ("doc-1",), ("train",), "none")


def test_partition_outside_the_canonical_domain_fails_closed() -> None:
    with pytest.raises(InvalidFindingIdentifierError):
        derive_finding_id("exact_example", ("mesc-pilot-01:aaa",), ("doc-1",), ("holdout",), "none")


# ==========================================================================
# 23.4 Type and validation
# ==========================================================================


@pytest.mark.parametrize(
    "value",
    [b"bytes", 1, 1.0, True, None, ["list"], _StrSubclass("subclass")],
)
def test_exact_equality_rejects_inexact_input_types(value: object) -> None:
    with pytest.raises(InvalidPrimitiveInputError):
        exact_question_equality(value, "question")
    with pytest.raises(InvalidPrimitiveInputError):
        exact_question_equality("question", value)


@pytest.mark.parametrize("value", [b"bytes", 1, True, None, _StrSubclass("subclass")])
def test_normalization_and_tokenization_reject_inexact_input_types(value: object) -> None:
    with pytest.raises(InvalidPrimitiveInputError):
        normalize_question(value)
    with pytest.raises(InvalidPrimitiveInputError):
        tokenize(value)


def test_identifier_primitives_reject_empty_strings() -> None:
    with pytest.raises(InvalidPrimitiveInputError):
        exact_example_identity("", "")
    with pytest.raises(InvalidPrimitiveInputError):
        exact_source_document_identity("doc-1", "")


@pytest.mark.parametrize(
    "value", [{"a"}, ["a"], ("a",), "a", None, frozenset({""}), frozenset({1})]
)
def test_token_set_jaccard_requires_an_exact_frozenset_of_tokens(value: object) -> None:
    with pytest.raises(InvalidPrimitiveInputError):
        token_set_jaccard(value, frozenset({"a"}))


def test_lone_surrogate_fails_closed() -> None:
    with pytest.raises(InvalidPrimitiveInputError):
        normalize_question("bad\ud800surrogate")


def test_invalid_finding_type_is_rejected() -> None:
    with pytest.raises(InvalidFindingTypeError):
        _finding(finding_type="exact_context")
    with pytest.raises(InvalidFindingTypeError):
        _finding(finding_type="")


def test_invalid_classification_is_rejected() -> None:
    with pytest.raises(InvalidClassificationError):
        _finding(classification="clean")
    with pytest.raises(InvalidClassificationError):
        _finding(classification="")


@pytest.mark.parametrize("score", [float("nan"), float("inf"), float("-inf")])
def test_nan_and_infinity_scores_are_rejected(score: float) -> None:
    with pytest.raises(InvalidScoreError):
        _finding(score_representation="jaccard:1/2", score=score)


@pytest.mark.parametrize("score", [0, 1, True, "0.5"])
def test_non_float_runtime_scores_are_rejected(score: object) -> None:
    with pytest.raises(InvalidScoreError):
        _finding(score_representation="jaccard:1/2", score=score)


def test_runtime_score_must_agree_with_the_authoritative_fraction() -> None:
    with pytest.raises(InvalidScoreError):
        _finding(score_representation="jaccard:1/2", score=0.4)
    assert _finding(score_representation="jaccard:1/2", score=0.5).score == 0.5


@pytest.mark.parametrize("representation", ["none", "not_evaluable"])
def test_non_evaluable_representations_cannot_carry_a_runtime_score(representation: str) -> None:
    with pytest.raises(InvalidScoreError):
        _finding(
            finding_type="empty_normalized_question",
            score_representation=representation,
            score=0.0,
        )


def test_false_positive_requires_supporting_evidence() -> None:
    with pytest.raises(InvalidEvidenceReferenceError):
        _finding(classification="false_positive")
    supported = _finding(classification="false_positive", evidence_reference="evidence:dec-0001")
    assert supported.evidence_reference == "evidence:dec-0001"


@pytest.mark.parametrize(
    "reference",
    [
        "",
        "  ",
        " evidence:x",
        "evidence:x ",
        "/var/tmp/evidence",
        "./evidence",
        "../evidence",
        "~/evidence",
        "C:\\evidence",
        "evidence\\local",
    ],
)
def test_unstable_or_path_shaped_evidence_references_are_rejected(reference: str) -> None:
    with pytest.raises(InvalidEvidenceReferenceError):
        _finding(classification="false_positive", evidence_reference=reference)


def test_suppression_attempts_fail_closed() -> None:
    finding = _finding()
    assert finding.suppressed is False
    with pytest.raises(SuppressionAttemptError):
        LeakageFinding(
            finding_id=finding.finding_id,
            finding_type=finding.finding_type,
            example_ids=finding.example_ids,
            source_document_ids=finding.source_document_ids,
            partitions=finding.partitions,
            score_representation=finding.score_representation,
            score=None,
            shared_surface=finding.shared_surface,
            classification=finding.classification,
            evidence_reference=None,
            suppressed=True,
        )


@pytest.mark.parametrize(
    "surface",
    [
        ("who invented the stethoscope?",),
        ("stethoscope",),
        ("example_id", "example_id"),
        (1,),
        "example_id",
        None,
    ],
)
def test_raw_text_bearing_shared_surface_fails_closed(surface: object) -> None:
    with pytest.raises(RawTextBearingValueError):
        LeakageFinding.create(
            finding_type="exact_example",
            example_ids=("mesc-pilot-01:aaa",),
            source_document_ids=("doc-1",),
            partitions=("train",),
            score_representation="none",
            shared_surface=surface,
            classification="unresolved",
        )


def test_shared_surface_allowlist_is_exactly_the_ratified_markers() -> None:
    assert set(SHARED_SURFACE_MARKERS) == {
        "example_id",
        "source_document_id",
        "question_bytes",
        "normalized_question",
        "question_token_set",
        "context_bytes",
        "context_token_set",
        "empty_normalized_question",
    }


def test_finding_type_domain_is_exactly_the_senior_enumeration() -> None:
    assert set(FINDING_TYPES) == {
        "exact_example",
        "source_document",
        "exact_question",
        "normalized_question",
        "near_duplicate_question",
        "context_overlap",
        "empty_normalized_question",
    }


def test_identity_arrays_are_normalized_on_direct_construction() -> None:
    finding = LeakageFinding(
        finding_id=GOLDEN_FINDING_ID,
        finding_type=GOLDEN_FINDING_TYPE,
        example_ids=("mesc-pilot-01:bbb", "mesc-pilot-01:aaa"),
        source_document_ids=GOLDEN_SOURCE_DOCUMENT_IDS,
        partitions=GOLDEN_PARTITIONS,
        score_representation=GOLDEN_SCORE_REPRESENTATION,
        score=None,
        shared_surface=("question_token_set",),
        classification="unresolved",
        evidence_reference=None,
    )
    assert finding.example_ids == GOLDEN_EXAMPLE_IDS


# ==========================================================================
# 23.5 Exact equality
# ==========================================================================


def test_exact_equality_accepts_identical_bytes() -> None:
    assert exact_example_identity("mesc-pilot-01:aaa", "mesc-pilot-01:aaa") is True
    assert exact_source_document_identity("doc-1", "doc-1") is True
    assert exact_question_equality("Who?", "Who?") is True
    assert exact_context_equality("Context.", "Context.") is True


def test_exact_equality_rejects_case_differences() -> None:
    assert exact_question_equality("Who?", "who?") is False
    assert exact_context_equality("Context.", "context.") is False
    assert exact_example_identity("mesc-pilot-01:aaa", "mesc-pilot-01:AAA") is False


def test_exact_equality_rejects_unicode_normalization_differences() -> None:
    composed = "e\u0301tude"
    precomposed = "\u00e9tude"
    assert composed != precomposed
    assert exact_question_equality(composed, precomposed) is False
    assert exact_context_equality("\ufb01le", "file") is False
    assert normalized_question_equality(composed, precomposed) is True


def test_exact_equality_rejects_whitespace_differences() -> None:
    assert exact_question_equality("who? ", "who?") is False
    assert exact_question_equality("who  ?", "who ?") is False
    assert exact_context_equality("a\tb", "a b") is False


# ==========================================================================
# 23.6 Normalization
# ==========================================================================


def test_normalization_applies_nfkc() -> None:
    assert normalize_question("\ufb01le") == "file"
    assert normalize_question("\u2460") == "1"


def test_normalization_case_folds() -> None:
    assert normalize_question("WHO") == "who"
    assert normalize_question("Stra\u00dfe") == "strasse"


def test_normalization_collapses_unicode_whitespace_runs() -> None:
    assert normalize_question("a\u00a0\u2003b\tc\n\nd") == "a b c d"


def test_normalization_strips_leading_and_trailing_whitespace() -> None:
    assert normalize_question("  \u3000who?  \n") == "who?"


def test_normalization_is_stable_for_arabic_and_latin_inputs() -> None:
    arabic = "\u0645\u0627 \u0647\u0648 \u0627\u0644\u062a\u0634\u062e\u064a\u0635\u061f"
    assert normalize_question(f"  {arabic}  ") == arabic
    assert normalize_question(arabic) == normalize_question(normalize_question(arabic))
    assert normalize_question("  Diagnosis?  ") == "diagnosis?"


def test_normalization_retains_punctuation() -> None:
    assert normalize_question("who, what; why?") == "who, what; why?"
    assert tokenize(normalize_question("who, what; why?")) == frozenset({"who", "what", "why"})


def test_normalization_does_not_depend_on_locale_or_timezone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline = normalize_question("  \u0130STANBUL Stra\u00dfe  ")
    for value in ("C", "tr_TR.UTF-8", "de_DE.UTF-8"):
        monkeypatch.setenv("LC_ALL", value)
        monkeypatch.setenv("LANG", value)
        monkeypatch.setenv("LC_COLLATE", value)
        monkeypatch.setenv("TZ", "Pacific/Kiritimati")
        assert normalize_question("  \u0130STANBUL Stra\u00dfe  ") == baseline


# ==========================================================================
# 23.7 Tokenization, Jaccard and empty-input precedence
# ==========================================================================


def test_tokenization_uses_maximal_unicode_alphanumeric_runs() -> None:
    assert tokenize("ab12 cd") == frozenset({"ab12", "cd"})
    assert tokenize("\u0645\u0631\u06482 x") == frozenset({"\u0645\u0631\u06482", "x"})


def test_tokenization_treats_punctuation_and_underscore_as_boundaries() -> None:
    assert tokenize("a-b.c,d") == frozenset({"a", "b", "c", "d"})
    assert tokenize("a_b") == frozenset({"a", "b"})


def test_tokenization_is_a_set_and_not_a_multiset() -> None:
    assert tokenize("who who who") == frozenset({"who"})
    assert len(tokenize("who who who")) == 1


def test_near_duplicate_threshold_passes_at_exactly_the_ratified_ratio() -> None:
    shared = _tokens(9)
    result = token_set_jaccard(shared, frozenset(shared | {"extra"}))
    assert (result.intersection_size, result.union_size) == (9, 10)
    # Exact integer comparison at the ratified boundary: 100 * 9 == 90 * 10.
    assert 100 * result.intersection_size == NEAR_DUPLICATE_THRESHOLD_PERCENT * result.union_size
    assert result.near_duplicate_threshold_passed is True
    assert result.context_overlap_threshold_passed is False


def test_near_duplicate_threshold_fails_immediately_below_the_ratified_ratio() -> None:
    shared = _tokens(8)
    result = token_set_jaccard(shared, frozenset(shared | {"extra"}))
    assert (result.intersection_size, result.union_size) == (8, 9)
    assert result.near_duplicate_threshold_passed is False


def test_context_overlap_threshold_passes_at_exactly_the_ratified_ratio() -> None:
    shared = _tokens(19)
    result = token_set_jaccard(shared, frozenset(shared | {"extra"}))
    assert (result.intersection_size, result.union_size) == (19, 20)
    assert result.context_overlap_threshold_passed is True


def test_context_overlap_threshold_fails_immediately_below_the_ratified_ratio() -> None:
    shared = _tokens(18)
    result = token_set_jaccard(shared, frozenset(shared | {"extra"}))
    assert (result.intersection_size, result.union_size) == (18, 19)
    assert result.context_overlap_threshold_passed is False


def test_threshold_percentages_are_the_ratified_integers() -> None:
    assert NEAR_DUPLICATE_THRESHOLD_PERCENT == 90
    assert CONTEXT_OVERLAP_THRESHOLD_PERCENT == 95


def test_both_token_sets_empty_is_the_union_zero_case() -> None:
    result = token_set_jaccard(frozenset(), frozenset())
    assert result.intersection_size == 0
    assert result.union_size == 0
    assert result.score_representation == SCORE_REPRESENTATION_NOT_EVALUABLE
    assert result.score is None
    assert result.evaluable is False
    assert result.near_duplicate_threshold_passed is False
    assert result.context_overlap_threshold_passed is False


def test_punctuation_only_inputs_produce_two_empty_token_sets() -> None:
    left = "!!! ???"
    right = "***"
    assert normalize_question(left) != ""
    assert normalize_question(right) != ""
    assert question_token_set(left) == frozenset()
    assert question_token_set(right) == frozenset()
    result = token_set_jaccard(question_token_set(left), question_token_set(right))
    assert result.score_representation == SCORE_REPRESENTATION_NOT_EVALUABLE
    assert result.union_size == 0
    assert is_empty_normalized_question_pair(left, right) is False


def test_symbol_only_inputs_are_not_empty_normalized_questions() -> None:
    assert question_token_set("\u00a9 \u00ae") == frozenset()
    assert is_empty_normalized_question_pair("\u00a9", "\u00ae") is False
    assert is_empty_normalized_question_pair("   ", "\t\n") is True


def test_exactly_one_token_set_empty_left_operand() -> None:
    result = token_set_jaccard(frozenset(), frozenset({"x"}))
    assert result.intersection_size == 0
    assert result.union_size == 1
    assert result.score_representation == SCORE_REPRESENTATION_NOT_EVALUABLE
    assert result.score is None
    assert result.near_duplicate_threshold_passed is False
    assert result.context_overlap_threshold_passed is False


def test_exactly_one_token_set_empty_right_operand() -> None:
    result = token_set_jaccard(frozenset({"x"}), frozenset())
    assert result.intersection_size == 0
    assert result.union_size == 1
    assert result.score_representation == SCORE_REPRESENTATION_NOT_EVALUABLE
    assert result.score is None
    assert result.near_duplicate_threshold_passed is False
    assert result.context_overlap_threshold_passed is False


def test_exactly_one_empty_never_enters_the_general_zero_intersection_branch() -> None:
    for left, right in ((frozenset(), frozenset({"x"})), (frozenset({"x"}), frozenset())):
        result = token_set_jaccard(left, right)
        # A general "intersection 0, union positive -> jaccard:0/1" rule would
        # have produced a fraction here; the empty-input rule controls instead.
        assert result.union_size > 0
        assert result.score_representation == SCORE_REPRESENTATION_NOT_EVALUABLE
        assert result.score_representation != "jaccard:0/1"


def test_jaccard_zero_over_zero_is_never_constructed() -> None:
    for left, right in (
        (frozenset(), frozenset()),
        (frozenset(), frozenset({"x"})),
        (frozenset({"x"}), frozenset()),
        (frozenset({"a"}), frozenset({"b"})),
    ):
        assert token_set_jaccard(left, right).score_representation != "jaccard:0/0"
    with pytest.raises(InvalidScoreError):
        validate_score_representation("jaccard:0/0")


def test_jaccard_zero_over_one_is_never_emitted_when_either_set_is_empty() -> None:
    for left, right in (
        (frozenset(), frozenset()),
        (frozenset(), frozenset({"x"})),
        (frozenset({"x"}), frozenset()),
    ):
        assert token_set_jaccard(left, right).score_representation != "jaccard:0/1"


def test_not_evaluable_is_never_emitted_for_two_non_empty_disjoint_sets() -> None:
    for left, right in (
        (frozenset({"a"}), frozenset({"b"})),
        (frozenset({"a", "b"}), frozenset({"c", "d"})),
    ):
        result = token_set_jaccard(left, right)
        assert result.score_representation == "jaccard:0/1"
        assert result.score_representation != SCORE_REPRESENTATION_NOT_EVALUABLE
        assert result.score == 0.0


def test_no_score_is_fabricated_for_an_empty_operand() -> None:
    for left, right in (
        (frozenset(), frozenset()),
        (frozenset(), frozenset({"x"})),
        (frozenset({"x"}), frozenset()),
    ):
        result = token_set_jaccard(left, right)
        assert result.score is None
        assert result.evaluable is False


# ==========================================================================
# 23.8 Findings
# ==========================================================================


def test_finding_identifier_is_deterministic_across_reruns() -> None:
    assert {_golden_finding().finding_id for _ in range(5)} == {GOLDEN_FINDING_ID}


def test_finding_identity_is_independent_of_caller_ordering() -> None:
    forward = LeakageFinding.create(
        finding_type=GOLDEN_FINDING_TYPE,
        example_ids=["mesc-pilot-01:bbb", "mesc-pilot-01:aaa"],
        source_document_ids=["doc-1"],
        partitions=["train"],
        score_representation=GOLDEN_SCORE_REPRESENTATION,
        classification="unresolved",
    )
    assert forward.finding_id == GOLDEN_FINDING_ID
    assert forward.example_ids == GOLDEN_EXAMPLE_IDS


def test_score_representation_is_bound_into_the_identity_document() -> None:
    finding = _golden_finding()
    assert finding.identity_document()["score_representation"] == finding.score_representation
    assert finding.to_canonical_document()["score_representation"] == finding.score_representation


def test_one_character_semantic_change_alters_the_identifier() -> None:
    baseline = _finding(example_ids=("mesc-pilot-01:aaa",))
    changed = _finding(example_ids=("mesc-pilot-01:aab",))
    assert baseline.finding_id != changed.finding_id


def test_report_findings_are_sorted_by_ascending_identifier() -> None:
    findings = [
        _finding(example_ids=("mesc-pilot-01:aaa",)),
        _finding(example_ids=("mesc-pilot-01:bbb",)),
        _finding(example_ids=("mesc-pilot-01:ccc",)),
    ]
    report = LeakageAuditReport.create(list(reversed(findings)))
    identifiers = [finding.finding_id for finding in report.findings]
    assert identifiers == sorted(identifiers)


def test_no_raw_text_reaches_the_canonical_document_or_bytes() -> None:
    question = "Which zzsecretzz drug treats it?"
    result = token_set_jaccard(question_token_set(question), question_token_set(question))
    finding = LeakageFinding.create(
        finding_type="near_duplicate_question",
        example_ids=("mesc-pilot-01:aaa",),
        source_document_ids=("doc-1",),
        partitions=("train",),
        score_representation=result.score_representation,
        score=result.score,
        shared_surface=("question_token_set",),
        classification="unresolved",
    )
    payload = finding.to_canonical_bytes()
    assert b"zzsecretzz" not in payload
    assert b"zzsecretzz" not in finding.identity_bytes()
    assert b"zzsecretzz" not in repr(finding).encode()
    assert "zzsecretzz" not in str(finding.to_canonical_document())


# ==========================================================================
# 23.9 Classification and report
# ==========================================================================


def test_unresolved_finding_sets_leaked_true() -> None:
    report = LeakageAuditReport.create([_finding(classification="unresolved")])
    assert report.leaked is True
    assert report.finding_count == 1


def test_confirmed_leakage_sets_leaked_true() -> None:
    report = LeakageAuditReport.create([_finding(classification="confirmed_leakage")])
    assert report.leaked is True


def test_all_supported_false_positives_set_leaked_false() -> None:
    findings = [
        _finding(
            example_ids=("mesc-pilot-01:aaa",),
            classification="false_positive",
            evidence_reference="evidence:dec-0001",
        ),
        _finding(
            example_ids=("mesc-pilot-01:bbb",),
            classification="false_positive",
            evidence_reference="evidence:dec-0002",
        ),
    ]
    report = LeakageAuditReport.create(findings)
    assert report.leaked is False
    assert report.finding_count == 2


def test_empty_report_behaviour_is_explicit() -> None:
    report = LeakageAuditReport.create([])
    assert report.findings == ()
    assert report.finding_count == 0
    assert report.leaked is False
    assert report.to_canonical_document()["findings"] == []


def test_finding_count_must_be_exact() -> None:
    finding = _finding()
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport(findings=(finding,), leaked=True, finding_count=2)
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport(findings=(finding,), leaked=True, finding_count=True)


def test_report_rejects_an_inconsistent_aggregate() -> None:
    finding = _finding(classification="unresolved")
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport(findings=(finding,), leaked=False, finding_count=1)


def test_report_rejects_unsorted_or_repeated_findings() -> None:
    first = _finding(example_ids=("mesc-pilot-01:aaa",))
    second = _finding(example_ids=("mesc-pilot-01:bbb",))
    ordered = sorted((first, second), key=lambda item: item.finding_id)
    unsorted = tuple(reversed(ordered))
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport(findings=unsorted, leaked=True, finding_count=2)
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport(findings=(first, first), leaked=True, finding_count=2)


def test_report_rejects_non_findings_and_unknown_detection_methods() -> None:
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport.create(["not-a-finding"])
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport.create([], ("real_dataset_scan",))
    with pytest.raises(InvalidReportInvariantError):
        LeakageAuditReport.create([], ("tokenize", "tokenize"))
    accepted = LeakageAuditReport.create([], list(DETECTION_METHODS))
    assert accepted.detection_methods == DETECTION_METHODS


def test_suppression_cannot_be_represented_in_a_report() -> None:
    report = LeakageAuditReport.create([_finding()])
    assert all(finding.suppressed is False for finding in report.findings)
    assert report.to_canonical_document()["finding_count"] == len(report.findings)


def test_leakage_positive_fixture_cannot_produce_a_vacuous_report() -> None:
    positive = [
        _finding(example_ids=("mesc-pilot-01:aaa",), classification="confirmed_leakage"),
        _finding(example_ids=("mesc-pilot-01:bbb",), classification="unresolved"),
    ]
    report = LeakageAuditReport.create(positive)
    assert report.finding_count == 2
    assert report.findings != ()
    assert report.leaked is True


def test_report_canonical_document_records_the_normalization_pipeline() -> None:
    document = LeakageAuditReport.create([]).to_canonical_document()
    record = document["normalization_record"]
    assert isinstance(record, dict)
    assert record["unicode_normalization"] == "NFKC"
    assert record["case_folding"] == "unicode_case_folding"
    assert "whitespace_collapse" in record


# ==========================================================================
# 23.10 Determinism and safety
# ==========================================================================


def test_repeated_canonical_bytes_are_identical() -> None:
    finding = _golden_finding()
    report = LeakageAuditReport.create([finding], ("token_set_jaccard",))
    assert len({finding.to_canonical_bytes() for _ in range(8)}) == 1
    assert len({report.to_canonical_bytes() for _ in range(8)}) == 1


@pytest.mark.parametrize(
    "fragment",
    [b"timestamp", b"_at", b"date", b"path", b"username", b"hostname", b"environ", b"cwd"],
)
def test_canonical_documents_carry_no_runtime_or_temporal_metadata(fragment: bytes) -> None:
    report = LeakageAuditReport.create([_golden_finding()], ("token_set_jaccard",))
    assert fragment not in report.to_canonical_bytes()
    assert fragment not in _golden_finding().identity_bytes()


def test_caller_owned_mutable_collections_are_not_retained() -> None:
    example_ids = ["mesc-pilot-01:aaa", "mesc-pilot-01:bbb"]
    surface = ["question_token_set"]
    finding = LeakageFinding.create(
        finding_type=GOLDEN_FINDING_TYPE,
        example_ids=example_ids,
        source_document_ids=["doc-1"],
        partitions=["train"],
        score_representation=GOLDEN_SCORE_REPRESENTATION,
        shared_surface=surface,
        classification="unresolved",
    )
    example_ids.append("mesc-pilot-01:zzz")
    surface.append("context_bytes")
    assert finding.example_ids == GOLDEN_EXAMPLE_IDS
    assert finding.shared_surface == ("question_token_set",)
    assert finding.finding_id == GOLDEN_FINDING_ID
    assert isinstance(finding.example_ids, tuple)


def test_findings_are_immutable() -> None:
    finding = _golden_finding()
    with pytest.raises(AttributeError):
        finding.classification = "false_positive"  # type: ignore[misc]
    report = LeakageAuditReport.create([finding])
    with pytest.raises(AttributeError):
        report.leaked = False  # type: ignore[misc]


def test_no_filesystem_access(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("filesystem access is prohibited")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(io, "open", forbidden)
    monkeypatch.setattr(os, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_bytes", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_text", forbidden)
    _exercise_every_primitive()


def test_no_network_access(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("network access is prohibited")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    _exercise_every_primitive()


def test_no_temporary_files_are_created(tmp_path: Path) -> None:
    before = set(tmp_path.iterdir())
    _exercise_every_primitive()
    assert set(tmp_path.iterdir()) == before


def test_module_declares_no_public_export() -> None:
    import medscale.mesc as package

    assert "LeakageFinding" not in package.__all__
    assert "LeakageAuditReport" not in package.__all__
    assert not hasattr(package, "LeakageFinding")
    assert not hasattr(package, "token_set_jaccard")


def test_schema_and_prefix_are_the_authorized_identifiers() -> None:
    assert FINDING_SCHEMA_VERSION == "mesc-pilot-01-leakage-finding/1"
    assert FINDING_ID_PREFIX == "mesc-pilot-01-leakage-finding/1:sha256:"


def _exercise_every_primitive() -> None:
    """Run every primitive and model once, for the side-effect assertions."""
    assert exact_example_identity("mesc-pilot-01:aaa", "mesc-pilot-01:aaa") is True
    assert exact_source_document_identity("doc-1", "doc-2") is False
    assert exact_question_equality("who?", "who?") is True
    assert exact_context_equality("ctx", "ctx") is True
    assert normalize_question("  WHO?  ") == "who?"
    assert tokenize("who?") == frozenset({"who"})
    assert normalized_question_equality("WHO", "who") is True
    assert is_empty_normalized_question_pair("", "") is True
    result = token_set_jaccard(frozenset({"a"}), frozenset({"a", "b"}))
    assert result.score_representation == "jaccard:1/2"
    assert math.isclose(result.score or 0.0, 0.5)
    finding = _golden_finding()
    assert finding.finding_id == GOLDEN_FINDING_ID
    assert finding.identity_bytes() == GOLDEN_IDENTITY_BYTES
    report = LeakageAuditReport.create([finding], ("token_set_jaccard",))
    assert report.to_canonical_bytes().endswith(b"\n")
