"""Fuzzy deduplication: PRISMA dedupe pass 2 (scientific review finding S2).

Pass 1 (identifier-exact) happens by construction in the corpus store. This pass finds
*cross-identifier* duplicates — classically an arXiv preprint and its published DOI
twin — by deterministic normalized-title + year matching, and merges them
conflict-safely:

- **Auto-merge** only when titles normalize identically, both years are present and
  within one year, the title is long enough to be discriminating, and the identifier
  union is conflict-free (no two different DOIs, PMIDs, arXiv ids, or corpus ids).
- Everything else that matches on title is reported as **uncertain** for human
  confirmation — never merged silently.
- Every merge is logged with both source records retained verbatim (the merge log is
  part of the auditable PRISMA trail).

Merging unions the identifiers, so the merged record gets a *new* ``record_id`` —
which is why this pass must run **before** screening decisions reference ids.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final

from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.store import record_to_dict

__all__ = ["DedupeResult", "MergeEntry", "UncertainEntry", "dedupe_records", "normalize_title"]

_NON_ALNUM: Final = re.compile(r"[^a-z0-9]+")
#: Below these thresholds a normalized title is too generic to auto-merge on.
_MIN_CHARS: Final = 20
_MIN_TOKENS: Final = 4


def normalize_title(title: str) -> str:
    """Casefold, strip punctuation, collapse whitespace — deterministic and cheap."""
    return " ".join(_NON_ALNUM.sub(" ", title.casefold()).split())


@dataclass(frozen=True)
class MergeEntry:
    """One executed merge: lineage from source records to the merged record."""

    merged_record_id: str
    source_record_ids: tuple[str, ...]
    source_records: tuple[dict[str, Any], ...]
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "merged_record_id": self.merged_record_id,
            "source_record_ids": list(self.source_record_ids),
            "source_records": list(self.source_records),
            "reason": self.reason,
        }


@dataclass(frozen=True)
class UncertainEntry:
    """A title-match group NOT auto-merged; needs a human decision."""

    record_ids: tuple[str, ...]
    normalized_title: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_ids": list(self.record_ids),
            "normalized_title": self.normalized_title,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class DedupeResult:
    records: tuple[LiteratureRecord, ...]
    merges: tuple[MergeEntry, ...]
    uncertain: tuple[UncertainEntry, ...]


def _identifier_conflict(group: list[LiteratureRecord]) -> bool:
    for field in ("doi", "pmid", "arxiv_id", "s2_corpus_id"):
        values = {
            getattr(record.identifiers, field)
            for record in group
            if getattr(record.identifiers, field) is not None
        }
        if len(values) > 1:
            return True
    return False


def _years_compatible(group: list[LiteratureRecord]) -> bool:
    years = [record.year for record in group]
    if any(year is None for year in years):
        return False
    concrete = [year for year in years if year is not None]
    return max(concrete) - min(concrete) <= 1


def _merge_base(group: list[LiteratureRecord]) -> LiteratureRecord:
    """Deterministic base choice: DOI-bearing beats not; peer-reviewed beats preprint;
    then smallest record_id."""

    def key(record: LiteratureRecord) -> tuple[int, int, str]:
        return (
            0 if record.identifiers.doi else 1,
            0 if record.evidence_tier is EvidenceTier.PEER_REVIEWED else 1,
            record.record_id,
        )

    return sorted(group, key=key)[0]


def _merged_record(group: list[LiteratureRecord]) -> LiteratureRecord:
    base = _merge_base(group)

    def first(field: str) -> str | None:
        for record in [base, *group]:
            value: str | None = getattr(record.identifiers, field)
            if value is not None:
                return value
        return None

    return LiteratureRecord(
        identifiers=Identifiers(
            doi=first("doi"),
            pmid=first("pmid"),
            arxiv_id=first("arxiv_id"),
            s2_corpus_id=first("s2_corpus_id"),
        ),
        title=base.title,
        evidence_tier=base.evidence_tier,
        provenance=base.provenance,
        year=base.year,
        venue=base.venue or next((r.venue for r in group if r.venue), None),
        authors=base.authors or next((r.authors for r in group if r.authors), ()),
        abstract=base.abstract or next((r.abstract for r in group if r.abstract), None),
        license_spdx=base.license_spdx,
        tags=base.tags,
    )


def dedupe_records(records: tuple[LiteratureRecord, ...]) -> DedupeResult:
    """Run the fuzzy pass over an identifier-unique corpus. Deterministic throughout."""
    by_title: dict[str, list[LiteratureRecord]] = {}
    for record in sorted(records, key=lambda r: r.record_id):
        by_title.setdefault(normalize_title(record.title), []).append(record)

    kept: list[LiteratureRecord] = []
    merges: list[MergeEntry] = []
    uncertain: list[UncertainEntry] = []

    for title, group in sorted(by_title.items()):
        if len(group) == 1:
            kept.append(group[0])
            continue
        ids = tuple(record.record_id for record in group)
        if len(title) < _MIN_CHARS or len(title.split()) < _MIN_TOKENS:
            uncertain.append(UncertainEntry(ids, title, "title too generic to auto-merge"))
            kept.extend(group)
        elif _identifier_conflict(group):
            uncertain.append(UncertainEntry(ids, title, "conflicting identifiers of the same type"))
            kept.extend(group)
        elif not _years_compatible(group):
            uncertain.append(
                UncertainEntry(ids, title, "years missing or more than one year apart")
            )
            kept.extend(group)
        else:
            merged = _merged_record(group)
            merges.append(
                MergeEntry(
                    merged_record_id=merged.record_id,
                    source_record_ids=ids,
                    source_records=tuple(record_to_dict(record) for record in group),
                    reason="normalized title match; years within 1; identifier union conflict-free",
                )
            )
            kept.append(merged)

    return DedupeResult(tuple(kept), tuple(merges), tuple(uncertain))
