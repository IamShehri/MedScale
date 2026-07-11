"""Deterministic query engine: pure conjunctive filters over the research index.

Design rules (PostgreSQL-planner-minded, decade-stable):

- every filter is optional; given filters combine with AND;
- results are always tuples in content-addressed id order — input order, dict order,
  and platform never change a result;
- text matching is *documented* normalization (casefold substring), never fuzzy magic;
- research-question and medical-domain filters resolve through the frozen query set
  (Q-id -> domain tag, RQ refs), so the science vocabulary is queryable directly.
"""

from __future__ import annotations

from typing import Final

from medscale.evidence import EvidenceObject, StudyType, VerificationState
from medscale.litdb.queries import QUERY_SET
from medscale.litdb.records import EvidenceTier, LiteratureRecord
from medscale.litdb.review import ReviewDecision
from medscale.provenance import SourceAPI
from medscale.research.index import ResearchIndex

__all__ = [
    "domain_of_query",
    "evidence_where",
    "queries_for_domain",
    "queries_for_rq",
    "records_where",
]

_DOMAIN_BY_QUERY: Final[dict[str, str]] = {q.query_id: q.domain_tag for q in QUERY_SET}


def domain_of_query(query_id: str) -> str | None:
    return _DOMAIN_BY_QUERY.get(query_id)


def queries_for_domain(domain: str) -> frozenset[str]:
    return frozenset(q.query_id for q in QUERY_SET if q.domain_tag == domain)


def queries_for_rq(rq: str) -> frozenset[str]:
    return frozenset(q.query_id for q in QUERY_SET if rq in q.rq_refs)


def _text_match(haystack: str | None, needle: str) -> bool:
    return needle.casefold() in (haystack or "").casefold()


def records_where(
    index: ResearchIndex,
    *,
    query_id: str | None = None,
    rq: str | None = None,
    domain: str | None = None,
    source: SourceAPI | None = None,
    tier: EvidenceTier | None = None,
    decision: ReviewDecision | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    venue_contains: str | None = None,
    text: str | None = None,
) -> tuple[LiteratureRecord, ...]:
    """Filter corpus records; ``text`` searches title+abstract (casefold substring).

    ``decision`` filters on the latest review state; ``ReviewDecision.PENDING`` selects
    records with no review event. Future surface: ``GET /sources``.
    """
    wanted_queries: frozenset[str] | None = None
    if query_id is not None:
        wanted_queries = frozenset({query_id})
    if rq is not None:
        rq_queries = queries_for_rq(rq)
        wanted_queries = rq_queries if wanted_queries is None else wanted_queries & rq_queries
    if domain is not None:
        domain_queries = queries_for_domain(domain)
        wanted_queries = (
            domain_queries if wanted_queries is None else wanted_queries & domain_queries
        )

    selected: list[LiteratureRecord] = []
    for record in index.records:  # already id-sorted
        if wanted_queries is not None and not (set(record.tags) & wanted_queries):
            continue
        if source is not None and record.provenance.source_api is not source:
            continue
        if tier is not None and record.evidence_tier is not tier:
            continue
        if decision is not None:
            review = index.reviews.get(record.record_id)
            current = review.decision if review else ReviewDecision.PENDING
            if current is not decision:
                continue
        if year_min is not None and (record.year is None or record.year < year_min):
            continue
        if year_max is not None and (record.year is None or record.year > year_max):
            continue
        if venue_contains is not None and not _text_match(record.venue, venue_contains):
            continue
        if text is not None and not (
            _text_match(record.title, text) or _text_match(record.abstract, text)
        ):
            continue
        selected.append(record)
    return tuple(selected)


def evidence_where(
    index: ResearchIndex,
    *,
    study_type: StudyType | None = None,
    verification: VerificationState | None = None,
    evidence_level: str | None = None,
    source_record_id: str | None = None,
    domain: str | None = None,
    claim_contains: str | None = None,
    population_contains: str | None = None,
    intervention_contains: str | None = None,
    comparator_contains: str | None = None,
    outcome_contains: str | None = None,
) -> tuple[EvidenceObject, ...]:
    """Filter evidence objects; PICO filters are per-slot casefold substrings.

    ``domain`` joins through the source record's query tags. Future surface:
    ``GET /evidence`` / ``GET /claims``.
    """
    domain_queries = queries_for_domain(domain) if domain is not None else None
    selected: list[EvidenceObject] = []
    for obj in index.evidence:  # already id-sorted
        if study_type is not None and obj.study_type is not study_type:
            continue
        if verification is not None and obj.verification is not verification:
            continue
        if evidence_level is not None and obj.evidence_level != evidence_level:
            continue
        if source_record_id is not None and obj.source_record_id != source_record_id:
            continue
        if domain_queries is not None:
            record = index.by_record_id.get(obj.source_record_id or "")
            if record is None or not (set(record.tags) & domain_queries):
                continue
        if claim_contains is not None and not _text_match(obj.claim, claim_contains):
            continue
        if population_contains is not None and not _text_match(obj.population, population_contains):
            continue
        if intervention_contains is not None and not _text_match(
            obj.intervention, intervention_contains
        ):
            continue
        if comparator_contains is not None and not _text_match(obj.comparator, comparator_contains):
            continue
        if outcome_contains is not None and not _text_match(obj.outcome, outcome_contains):
            continue
        selected.append(obj)
    return tuple(selected)
