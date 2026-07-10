"""The frozen query set stays consistent with the search strategy and taxonomy."""

from __future__ import annotations

import pytest

from medscale.litdb import QUERY_SET, RESULT_CAP, YEAR_FROM, get_query

_TAXONOMY_DOMAIN_TAGS = {
    "fhir-clinical-modeling",
    "constrained-decoding",
    "clinical-llm",
    "clinical-ie",
    "medical-benchmark",
    "eval-methodology",
    "peft-efficiency",
    "terminology-ontology",
    "synthetic-clinical-data",
    "faithfulness-hallucination",
    "safety-governance",
}

_VALID_RQ_REFS = {f"RQ{i}" for i in range(1, 8)} | {"background"}


def test_query_set_has_ten_unique_queries() -> None:
    ids = [q.query_id for q in QUERY_SET]
    assert ids == [f"Q{i}" for i in range(1, 11)]
    assert len(set(ids)) == 10


def test_domain_tags_come_from_taxonomy_facet_a() -> None:
    for q in QUERY_SET:
        assert q.domain_tag in _TAXONOMY_DOMAIN_TAGS, q.query_id


def test_rq_refs_are_valid() -> None:
    for q in QUERY_SET:
        assert q.rq_refs, q.query_id
        assert set(q.rq_refs) <= _VALID_RQ_REFS, q.query_id


def test_execution_parameters_match_strategy() -> None:
    assert RESULT_CAP == 200
    assert YEAR_FROM == 2019


def test_get_query_roundtrip_and_unknown() -> None:
    assert get_query("Q2").domain_tag == "fhir-clinical-modeling"
    with pytest.raises(ValueError, match="unknown query_id"):
        get_query("Q99")
