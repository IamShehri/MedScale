"""Parsers: archived raw payloads -> LiteratureRecords (the T1 pipeline's parse stage).

Source -> Raw Artifact -> **Parser** -> LiteratureRecord -> Evidence Candidate -> Verification

Parsers are pure functions over :class:`RawRetrieval` envelopes: same payload, same
records, byte-for-byte. Every produced record carries per-record provenance anchored to
the SHA-256 of the exact archived payload it came from (R1). Items that cannot become a
valid record (e.g. no resolvable identifier) are *skipped with a recorded reason*,
never dropped silently — the skip list is part of the deterministic output.

Evidence-tier assignment here is a deterministic *proposal* from source metadata;
screening (a human decision of record) may correct it.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, Final

from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.sources import RawRetrieval
from medscale.provenance import Provenance, RetrievalStatus, SourceAPI

__all__ = ["ParseOutcome", "parse_pubmed_esearch_ids", "parse_records"]

_DOI_URL_PREFIX: Final = re.compile(r"^https?://(dx\.)?doi\.org/", re.IGNORECASE)
_PMID_URL_PREFIX: Final = re.compile(r"^https?://pubmed\.ncbi\.nlm\.nih\.gov/", re.IGNORECASE)
_ARXIV_ABS_PREFIX: Final = re.compile(r"^https?://arxiv\.org/abs/", re.IGNORECASE)
_ARXIV_VERSION: Final = re.compile(r"v\d+$")
_ATOM_NS: Final = {"a": "http://www.w3.org/2005/Atom"}


@dataclass(frozen=True)
class ParseOutcome:
    """Parsed records plus the honest remainder: what was skipped, and why."""

    records: tuple[LiteratureRecord, ...]
    skipped: tuple[str, ...]


def parse_records(retrieval: RawRetrieval) -> ParseOutcome:
    """Parse an archived payload into records, dispatching on the source API."""
    if retrieval.status is not RetrievalStatus.FOUND:
        return ParseOutcome(
            (), (f"{retrieval.source_api.value}: NOT_FOUND payload has no records",)
        )
    if retrieval.source_api is SourceAPI.OPENALEX:
        return _parse_openalex(retrieval)
    if retrieval.source_api is SourceAPI.SEMANTIC_SCHOLAR:
        return _parse_semantic_scholar(retrieval)
    if retrieval.source_api is SourceAPI.PUBMED:
        return _parse_pubmed(retrieval)
    return _parse_arxiv(retrieval)


def parse_pubmed_esearch_ids(retrieval: RawRetrieval) -> tuple[str, ...]:
    """Extract PMIDs from an E-utilities *esearch* payload (ids only, no metadata)."""
    data = json.loads(retrieval.payload)
    id_list = data.get("esearchresult", {}).get("idlist", [])
    return tuple(str(pmid) for pmid in id_list)


def _provenance(retrieval: RawRetrieval, identifier: str) -> Provenance:
    return Provenance(
        source_api=retrieval.source_api,
        identifier=identifier,
        verified_at=retrieval.retrieved_at,
        raw_response_sha256=retrieval.payload_sha256(),
        status=RetrievalStatus.FOUND,
    )


def _strip_doi(value: str | None) -> str | None:
    if not value:
        return None
    return _DOI_URL_PREFIX.sub("", value.strip())


def _strip_arxiv(value: str | None) -> str | None:
    if not value:
        return None
    bare = _ARXIV_ABS_PREFIX.sub("", value.strip())
    return _ARXIV_VERSION.sub("", bare)  # versions collapse so dedupe holds


def _year(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and len(value) >= 4 and value[:4].isdigit():
        return int(value[:4])
    return None


# --------------------------------------------------------------------------- OpenAlex
def _openalex_abstract(inverted: dict[str, list[int]] | None) -> str | None:
    if not inverted:
        return None
    positions: dict[int, str] = {}
    for word, indexes in inverted.items():
        for index in indexes:
            positions[index] = word
    return " ".join(positions[index] for index in sorted(positions))


def _parse_openalex(retrieval: RawRetrieval) -> ParseOutcome:
    data = json.loads(retrieval.payload)
    records: list[LiteratureRecord] = []
    skipped: list[str] = []
    for item in data.get("results", []):
        doi = _strip_doi(item.get("doi"))
        ids = item.get("ids") or {}
        pmid_url = ids.get("pmid")
        pmid = _PMID_URL_PREFIX.sub("", pmid_url).strip("/") if pmid_url else None
        title = (item.get("display_name") or item.get("title") or "").strip()
        openalex_id = str(item.get("id", "unknown"))
        if not (doi or pmid):
            skipped.append(f"openalex {openalex_id}: no resolvable identifier (doi/pmid)")
            continue
        if not title:
            skipped.append(f"openalex {openalex_id}: missing title")
            continue
        location = item.get("primary_location") or {}
        source = location.get("source") or {}
        source_type = source.get("type")
        tier = (
            EvidenceTier.PEER_REVIEWED
            if source_type in ("journal", "conference")
            else EvidenceTier.PREPRINT
        )
        records.append(
            LiteratureRecord(
                identifiers=Identifiers(doi=doi, pmid=pmid),
                title=title,
                evidence_tier=tier,
                provenance=_provenance(retrieval, doi or pmid or openalex_id),
                year=_year(item.get("publication_year")),
                venue=source.get("display_name"),
                authors=tuple(
                    author["author"]["display_name"]
                    for author in item.get("authorships", [])
                    if author.get("author", {}).get("display_name")
                ),
                abstract=_openalex_abstract(item.get("abstract_inverted_index")),
            )
        )
    return ParseOutcome(tuple(records), tuple(skipped))


# ------------------------------------------------------------------- Semantic Scholar
def _parse_semantic_scholar(retrieval: RawRetrieval) -> ParseOutcome:
    data = json.loads(retrieval.payload)
    records: list[LiteratureRecord] = []
    skipped: list[str] = []
    for item in data.get("data", []):
        external = item.get("externalIds") or {}
        doi = _strip_doi(external.get("DOI"))
        pmid = str(external["PubMed"]) if external.get("PubMed") else None
        arxiv_id = _strip_arxiv(external.get("ArXiv"))
        corpus_id = str(external["CorpusId"]) if external.get("CorpusId") else None
        title = (item.get("title") or "").strip()
        label = str(item.get("paperId", "unknown"))
        if not (doi or pmid or arxiv_id or corpus_id):
            skipped.append(f"semantic_scholar {label}: no resolvable identifier")
            continue
        if not title:
            skipped.append(f"semantic_scholar {label}: missing title")
            continue
        venue = (item.get("venue") or "").strip() or None
        if arxiv_id and not doi:
            tier = EvidenceTier.PREPRINT
        elif venue:
            tier = EvidenceTier.PEER_REVIEWED
        else:
            tier = EvidenceTier.PREPRINT
        records.append(
            LiteratureRecord(
                identifiers=Identifiers(
                    doi=doi, pmid=pmid, arxiv_id=arxiv_id, s2_corpus_id=corpus_id
                ),
                title=title,
                evidence_tier=tier,
                provenance=_provenance(retrieval, doi or pmid or arxiv_id or corpus_id or label),
                year=_year(item.get("year")),
                venue=venue,
                authors=tuple(
                    author["name"] for author in item.get("authors", []) if author.get("name")
                ),
                abstract=(item.get("abstract") or None),
            )
        )
    return ParseOutcome(tuple(records), tuple(skipped))


# ----------------------------------------------------------------------------- PubMed
def _parse_pubmed(retrieval: RawRetrieval) -> ParseOutcome:
    data = json.loads(retrieval.payload)
    if "esearchresult" in data:
        return ParseOutcome(
            (),
            (
                "pubmed esearch payload contains PMIDs only; fetch esummary per id "
                "(parse_pubmed_esearch_ids + fetch_by_identifier)",
            ),
        )
    result = data.get("result") or {}
    records: list[LiteratureRecord] = []
    skipped: list[str] = []
    for uid in result.get("uids", []):
        item = result.get(str(uid)) or {}
        if "error" in item:
            skipped.append(f"pubmed {uid}: {item['error']}")
            continue
        title = (item.get("title") or "").strip()
        if not title:
            skipped.append(f"pubmed {uid}: missing title")
            continue
        doi = next(
            (
                _strip_doi(str(article_id.get("value")))
                for article_id in item.get("articleids", [])
                if article_id.get("idtype") == "doi" and article_id.get("value")
            ),
            None,
        )
        records.append(
            LiteratureRecord(
                identifiers=Identifiers(doi=doi, pmid=str(uid)),
                title=title,
                evidence_tier=EvidenceTier.PEER_REVIEWED,
                provenance=_provenance(retrieval, str(uid)),
                year=_year(item.get("pubdate")),
                venue=(item.get("fulljournalname") or item.get("source") or None),
                authors=tuple(
                    author["name"] for author in item.get("authors", []) if author.get("name")
                ),
            )
        )
    return ParseOutcome(tuple(records), tuple(skipped))


# ------------------------------------------------------------------------------ arXiv
def _parse_arxiv(retrieval: RawRetrieval) -> ParseOutcome:
    root = ET.fromstring(retrieval.payload)
    records: list[LiteratureRecord] = []
    skipped: list[str] = []
    for entry in root.findall("a:entry", _ATOM_NS):
        arxiv_id = _strip_arxiv(entry.findtext("a:id", default="", namespaces=_ATOM_NS))
        title = " ".join((entry.findtext("a:title", default="", namespaces=_ATOM_NS)).split())
        if not arxiv_id:
            skipped.append("arxiv entry: missing id")
            continue
        if not title:
            skipped.append(f"arxiv {arxiv_id}: missing title")
            continue
        summary = entry.findtext("a:summary", default="", namespaces=_ATOM_NS)
        published = entry.findtext("a:published", default="", namespaces=_ATOM_NS)
        records.append(
            LiteratureRecord(
                identifiers=Identifiers(arxiv_id=arxiv_id),
                title=title,
                evidence_tier=EvidenceTier.PREPRINT,
                provenance=_provenance(retrieval, arxiv_id),
                year=_year(published),
                authors=tuple(
                    name.text.strip()
                    for name in entry.findall("a:author/a:name", _ATOM_NS)
                    if name.text and name.text.strip()
                ),
                abstract=" ".join(summary.split()) or None,
            )
        )
    return ParseOutcome(tuple(records), tuple(skipped))
