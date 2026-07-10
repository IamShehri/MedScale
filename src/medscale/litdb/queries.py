"""The frozen v1 query set (docs/execution/search_strategy.md §2, frozen by commit).

This module is the *code twin* of the search-strategy document: run manifests cite the
git SHA, and tests assert this table stays consistent with the taxonomy. Changing a
query here is a new, versioned search round — never a silent edit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = ["QUERY_SET", "RESULT_CAP", "YEAR_FROM", "QuerySpec", "get_query"]

#: Maximum results requested per query per source (search_strategy §2).
RESULT_CAP: Final = 200

#: Publication-year lower bound (standards background exempt at screening).
YEAR_FROM: Final = 2019


@dataclass(frozen=True)
class QuerySpec:
    """One frozen concept query, mapped to its taxonomy domain and research questions."""

    query_id: str
    domain_tag: str
    concept_query: str
    rq_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.query_id.strip() or not self.concept_query.strip():
            raise ValueError("query_id and concept_query must be non-empty")


QUERY_SET: Final[tuple[QuerySpec, ...]] = (
    QuerySpec(
        "Q1",
        "constrained-decoding",
        '("constrained decoding" OR "grammar-constrained" OR "structured output" OR GBNF) '
        'AND ("language model" OR LLM)',
        ("RQ1",),
    ),
    QuerySpec(
        "Q2",
        "fhir-clinical-modeling",
        '(FHIR OR "HL7 FHIR") AND ("language model" OR LLM OR generation OR validation)',
        ("RQ1", "RQ3"),
    ),
    QuerySpec(
        "Q3",
        "clinical-ie",
        '("clinical information extraction" OR "clinical NER" OR "note to structured") '
        'AND ("language model" OR transformer)',
        ("RQ5",),
    ),
    QuerySpec(
        "Q4",
        "eval-methodology",
        '("LLM-as-judge" OR "evaluation methodology" OR "benchmark contamination") '
        "AND (medical OR clinical)",
        ("RQ2", "RQ5"),
    ),
    QuerySpec(
        "Q5",
        "peft-efficiency",
        '(QLoRA OR LoRA OR "parameter-efficient fine-tuning") '
        "AND (clinical OR biomedical OR medical)",
        ("RQ2",),
    ),
    QuerySpec(
        "Q6",
        "medical-benchmark",
        '("medical benchmark" OR "clinical benchmark" OR MedQA OR "clinical evaluation suite")',
        ("RQ2",),
    ),
    QuerySpec(
        "Q7",
        "synthetic-clinical-data",
        '(Synthea OR "synthetic patient" OR "synthetic EHR" OR "synthetic clinical data")',
        ("RQ3", "RQ6"),
    ),
    QuerySpec(
        "Q8",
        "faithfulness-hallucination",
        "(hallucination OR faithfulness OR attribution) AND (clinical OR medical) "
        'AND ("language model" OR LLM)',
        ("RQ5",),
    ),
    QuerySpec(
        "Q9",
        "terminology-ontology",
        '(SNOMED OR LOINC OR RxNorm OR UMLS) AND ("language model" OR "value set" OR grounding)',
        ("RQ7",),
    ),
    QuerySpec(
        "Q10",
        "clinical-llm",
        '("clinical language model" OR "medical LLM" OR "biomedical language model")',
        ("background",),
    ),
)


def get_query(query_id: str) -> QuerySpec:
    """Look up a frozen query by id."""
    for spec in QUERY_SET:
        if spec.query_id == query_id:
            return spec
    raise ValueError(f"unknown query_id {query_id!r}; known: {[q.query_id for q in QUERY_SET]}")
