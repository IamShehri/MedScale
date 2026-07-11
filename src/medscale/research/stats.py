"""Scientific statistics: deterministic, machine-readable, nothing visual.

Every number here is a pure function of the index; every ``to_dict`` is
canonical-JSON-ready with sorted keys, so two labs computing statistics over the same
snapshot produce identical bytes. Rates are rounded to six decimals (a documented
transformation, not a hidden one).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from medscale.litdb.review import prisma_summary
from medscale.research.index import ResearchIndex
from medscale.research.query import domain_of_query

__all__ = [
    "CorpusStats",
    "EvidenceStats",
    "ScreeningStats",
    "corpus_stats",
    "evidence_stats",
    "screening_stats",
]


def _sorted_counts(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


@dataclass(frozen=True)
class CorpusStats:
    total_records: int
    by_source: dict[str, int]
    by_query: dict[str, int]
    by_domain: dict[str, int]
    by_year: dict[str, int]
    by_tier: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_records": self.total_records,
            "by_source": self.by_source,
            "by_query": self.by_query,
            "by_domain": self.by_domain,
            "by_year": self.by_year,
            "by_tier": self.by_tier,
        }


def corpus_stats(index: ResearchIndex) -> CorpusStats:
    by_source: Counter[str] = Counter()
    by_query: Counter[str] = Counter()
    by_domain: Counter[str] = Counter()
    by_year: Counter[str] = Counter()
    by_tier: Counter[str] = Counter()
    for record in index.records:
        by_source[record.provenance.source_api.value] += 1
        by_tier[record.evidence_tier.value] += 1
        by_year[str(record.year) if record.year is not None else "unknown"] += 1
        for tag in record.tags:
            by_query[tag] += 1
            domain = domain_of_query(tag)
            if domain is not None:
                by_domain[domain] += 1
    return CorpusStats(
        total_records=len(index.records),
        by_source=_sorted_counts(by_source),
        by_query=_sorted_counts(by_query),
        by_domain=_sorted_counts(by_domain),
        by_year=_sorted_counts(by_year),
        by_tier=_sorted_counts(by_tier),
    )


@dataclass(frozen=True)
class ScreeningStats:
    prisma: dict[str, Any]
    inclusion_rate: float | None
    exclusion_reasons: dict[str, int]
    agreement_eligible_records: int
    agreement_rate: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "prisma": self.prisma,
            "inclusion_rate": self.inclusion_rate,
            "exclusion_reasons": self.exclusion_reasons,
            "reviewer_agreement": {
                "eligible_records": self.agreement_eligible_records,
                "agreement_rate": self.agreement_rate,
            },
        }


def screening_stats(index: ResearchIndex) -> ScreeningStats:
    summary = prisma_summary([record.record_id for record in index.records], index.reviews)
    decided = summary.included + summary.excluded
    inclusion_rate = round(summary.included / decided, 6) if decided else None

    # Reviewer agreement: among records reviewed by >=2 distinct reviewers, the record
    # agrees iff every reviewer's LATEST decision is identical (washout protocol, S3).
    latest_by_reviewer: dict[str, dict[str, str]] = {}
    for event in index.review_events:
        latest_by_reviewer.setdefault(event.record_id, {})[event.reviewer] = event.decision
    eligible = {
        record_id: decisions
        for record_id, decisions in latest_by_reviewer.items()
        if len(decisions) >= 2
    }
    agreed = sum(1 for decisions in eligible.values() if len(set(decisions.values())) == 1)
    agreement_rate = round(agreed / len(eligible), 6) if eligible else None

    return ScreeningStats(
        prisma=summary.to_dict(),
        inclusion_rate=inclusion_rate,
        exclusion_reasons=dict(sorted(summary.exclusion_breakdown.items())),
        agreement_eligible_records=len(eligible),
        agreement_rate=agreement_rate,
    )


@dataclass(frozen=True)
class EvidenceStats:
    total_objects: int
    by_study_type: dict[str, int]
    by_verification: dict[str, int]
    by_level: dict[str, int]
    by_domain: dict[str, int]
    source_records_covered: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_objects": self.total_objects,
            "by_study_type": self.by_study_type,
            "by_verification": self.by_verification,
            "by_level": self.by_level,
            "by_domain": self.by_domain,
            "source_records_covered": self.source_records_covered,
        }


def evidence_stats(index: ResearchIndex) -> EvidenceStats:
    by_study_type: Counter[str] = Counter()
    by_verification: Counter[str] = Counter()
    by_level: Counter[str] = Counter()
    by_domain: Counter[str] = Counter()
    sources: set[str] = set()
    for obj in index.evidence:
        by_study_type[obj.study_type.value] += 1
        by_verification[obj.verification.value] += 1
        by_level[obj.evidence_level] += 1
        if obj.source_record_id:
            sources.add(obj.source_record_id)
            record = index.by_record_id.get(obj.source_record_id)
            if record is not None:
                for tag in record.tags:
                    domain = domain_of_query(tag)
                    if domain is not None:
                        by_domain[domain] += 1
    return EvidenceStats(
        total_objects=len(index.evidence),
        by_study_type=_sorted_counts(by_study_type),
        by_verification=_sorted_counts(by_verification),
        by_level=_sorted_counts(by_level),
        by_domain=_sorted_counts(by_domain),
        source_records_covered=len(sources),
    )
