"""Literature metadata schema.

A :class:`LiteratureRecord` is the bibliographic *source* row of litdb: identifiers,
minimal metadata, an evidence tier (paper-taxonomy Facet D), and R1 provenance. Claims
extracted from a record live in :mod:`medscale.evidence`, keyed back via ``record_id``.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass

from medscale.provenance import Provenance
from medscale.reproducibility import content_hash

__all__ = ["EvidenceTier", "Identifiers", "LiteratureRecord"]


class EvidenceTier(enum.Enum):
    """How much weight a source can bear (paper taxonomy, Facet D)."""

    PEER_REVIEWED = "peer-reviewed"
    PREPRINT = "preprint"
    BENCHMARK_REPORT = "benchmark-report"
    GREY = "grey"


@dataclass(frozen=True)
class Identifiers:
    """Resolvable identifiers. At least one is required (Rule R1)."""

    doi: str | None = None
    pmid: str | None = None
    arxiv_id: str | None = None
    s2_corpus_id: str | None = None

    def __post_init__(self) -> None:
        normalized = {
            "doi": _normalize(self.doi, lowercase=True),
            "pmid": _normalize(self.pmid),
            "arxiv_id": _normalize(self.arxiv_id),
            "s2_corpus_id": _normalize(self.s2_corpus_id),
        }
        for field_name, value in normalized.items():
            object.__setattr__(self, field_name, value)
        if not any(normalized.values()):
            raise ValueError(
                "a literature record requires at least one resolvable identifier "
                "(doi, pmid, arxiv_id, or s2_corpus_id) — Rule R1"
            )


def _normalize(value: str | None, *, lowercase: bool = False) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    return stripped.lower() if lowercase else stripped


@dataclass(frozen=True)
class LiteratureRecord:
    """One screened bibliographic source."""

    identifiers: Identifiers
    title: str
    evidence_tier: EvidenceTier
    provenance: Provenance
    year: int | None = None
    venue: str | None = None
    authors: tuple[str, ...] = ()
    abstract: str | None = None
    license_spdx: str | None = None
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must be non-empty")

    @property
    def record_id(self) -> str:
        """Identity derived from identifiers only.

        Two fetches of the same DOI — from different APIs, at different times — produce
        the same ``record_id``, so exact-identifier deduplication (the first PRISMA
        dedupe pass) holds by construction. Fuzzy title+year dedupe is a separate,
        documented eligibility-stage step, not part of identity.
        """
        return content_hash(
            {
                "doi": self.identifiers.doi,
                "pmid": self.identifiers.pmid,
                "arxiv_id": self.identifiers.arxiv_id,
                "s2_corpus_id": self.identifiers.s2_corpus_id,
            }
        )
