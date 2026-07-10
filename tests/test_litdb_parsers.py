"""Parsers: deterministic payload -> record transformation, honest skips, real archives."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.litdb import (
    EvidenceTier,
    RawRetrieval,
    parse_pubmed_esearch_ids,
    parse_records,
)
from medscale.provenance import RetrievalStatus, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"
_DATA = Path(__file__).resolve().parents[1] / "data" / "litdb" / "raw"


def _retrieval(api: SourceAPI, payload: str) -> RawRetrieval:
    return RawRetrieval(source_api=api, query="fixture", retrieved_at=_TS, payload=payload)


# ------------------------------------------------------------------ synthetic fixtures
def test_openalex_parse_and_abstract_reconstruction() -> None:
    payload = json.dumps(
        {
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "doi": "https://doi.org/10.1234/ABC",
                    "ids": {"pmid": "https://pubmed.ncbi.nlm.nih.gov/999/"},
                    "display_name": "FHIR generation under grammar",
                    "publication_year": 2025,
                    "primary_location": {
                        "source": {"display_name": "J. Med. AI", "type": "journal"}
                    },
                    "authorships": [{"author": {"display_name": "A. Author"}}],
                    "abstract_inverted_index": {"Grammar": [0], "wins": [1]},
                },
                {"id": "https://openalex.org/W2", "display_name": "No identifiers here"},
            ]
        }
    )
    outcome = parse_records(_retrieval(SourceAPI.OPENALEX, payload))
    assert len(outcome.records) == 1
    record = outcome.records[0]
    assert record.identifiers.doi == "10.1234/abc"  # URL stripped + normalized
    assert record.identifiers.pmid == "999"
    assert record.evidence_tier is EvidenceTier.PEER_REVIEWED
    assert record.abstract == "Grammar wins"
    assert (
        record.provenance.raw_response_sha256
        == _retrieval(SourceAPI.OPENALEX, payload).payload_sha256()
    )
    assert len(outcome.skipped) == 1
    assert "no resolvable identifier" in outcome.skipped[0]


def test_semantic_scholar_parse_tiers() -> None:
    payload = json.dumps(
        {
            "data": [
                {
                    "paperId": "p1",
                    "externalIds": {"ArXiv": "2401.00001v3", "CorpusId": 42},
                    "title": "Preprint only",
                    "year": 2024,
                    "authors": [{"name": "B. Author"}],
                },
                {
                    "paperId": "p2",
                    "externalIds": {"DOI": "10.5/xyz", "CorpusId": 43},
                    "title": "Journal paper",
                    "venue": "NEJM AI",
                    "year": 2025,
                },
                {"paperId": "p3", "externalIds": {}, "title": "orphan"},
            ]
        }
    )
    outcome = parse_records(_retrieval(SourceAPI.SEMANTIC_SCHOLAR, payload))
    preprint, journal = outcome.records
    assert preprint.identifiers.arxiv_id == "2401.00001"  # version collapsed
    assert preprint.evidence_tier is EvidenceTier.PREPRINT
    assert journal.evidence_tier is EvidenceTier.PEER_REVIEWED
    assert journal.identifiers.s2_corpus_id == "43"
    assert len(outcome.skipped) == 1


def test_pubmed_esummary_parse() -> None:
    payload = json.dumps(
        {
            "result": {
                "uids": ["123", "456"],
                "123": {
                    "title": "An RCT of X",
                    "pubdate": "2026 Jan 15",
                    "fulljournalname": "The Lancet Digital Health",
                    "authors": [{"name": "C. Author"}],
                    "articleids": [{"idtype": "doi", "value": "10.9/rct"}],
                },
                "456": {"error": "cannot get document summary"},
            }
        }
    )
    outcome = parse_records(_retrieval(SourceAPI.PUBMED, payload))
    (record,) = outcome.records
    assert record.identifiers.pmid == "123"
    assert record.identifiers.doi == "10.9/rct"
    assert record.year == 2026
    assert record.evidence_tier is EvidenceTier.PEER_REVIEWED
    assert outcome.skipped == ("pubmed 456: cannot get document summary",)


def test_pubmed_esearch_payload_is_skipped_with_guidance() -> None:
    payload = json.dumps({"esearchresult": {"idlist": ["1", "2"]}})
    outcome = parse_records(_retrieval(SourceAPI.PUBMED, payload))
    assert outcome.records == ()
    assert "esummary" in outcome.skipped[0]
    ids = parse_pubmed_esearch_ids(_retrieval(SourceAPI.PUBMED, payload))
    assert ids == ("1", "2")


def test_arxiv_atom_parse() -> None:
    payload = (
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        "<entry><id>http://arxiv.org/abs/2401.00001v2</id>"
        "<title>Constrained  decoding\n  survey</title>"
        "<summary>All about grammars.</summary>"
        "<published>2024-01-01T00:00:00Z</published>"
        "<author><name>D. Author</name></author></entry></feed>"
    )
    outcome = parse_records(_retrieval(SourceAPI.ARXIV, payload))
    (record,) = outcome.records
    assert record.identifiers.arxiv_id == "2401.00001"
    assert record.title == "Constrained decoding survey"  # whitespace collapsed
    assert record.evidence_tier is EvidenceTier.PREPRINT
    assert record.year == 2024
    assert record.authors == ("D. Author",)


def test_not_found_payload_yields_no_records() -> None:
    retrieval = RawRetrieval(
        source_api=SourceAPI.OPENALEX,
        query="q",
        retrieved_at=_TS,
        payload="",
        status=RetrievalStatus.NOT_FOUND,
    )
    outcome = parse_records(retrieval)
    assert outcome.records == ()
    assert "NOT_FOUND" in outcome.skipped[0]


def test_parsing_is_deterministic() -> None:
    payload = json.dumps({"results": []})
    a = parse_records(_retrieval(SourceAPI.OPENALEX, payload))
    b = parse_records(_retrieval(SourceAPI.OPENALEX, payload))
    assert a == b


# ------------------------------------------------- real committed pilot archives (round 0)
@pytest.mark.skipif(not _DATA.exists(), reason="pilot archives not present")
def test_pilot_openalex_archive_parses() -> None:
    payload = (_DATA / "openalex" / "Q2" / "run0-pilot.json").read_text(encoding="utf-8")
    outcome = parse_records(_retrieval(SourceAPI.OPENALEX, payload))
    assert len(outcome.records) + len(outcome.skipped) == 3
    assert outcome.records, "expected at least one parseable OpenAlex work"
    for record in outcome.records:
        assert record.record_id  # constructible, identified, hashable


@pytest.mark.skipif(not _DATA.exists(), reason="pilot archives not present")
def test_pilot_arxiv_archive_parses() -> None:
    payload = (_DATA / "arxiv" / "Q2" / "run0-pilot.json").read_text(encoding="utf-8")
    outcome = parse_records(_retrieval(SourceAPI.ARXIV, payload))
    assert len(outcome.records) == 3
    assert all(r.evidence_tier is EvidenceTier.PREPRINT for r in outcome.records)


@pytest.mark.skipif(not _DATA.exists(), reason="pilot archives not present")
def test_pilot_pubmed_esearch_ids() -> None:
    payload = (_DATA / "pubmed" / "Q2" / "run0-pilot.json").read_text(encoding="utf-8")
    ids = parse_pubmed_esearch_ids(_retrieval(SourceAPI.PUBMED, payload))
    assert ids == ("42411231", "42406270", "42402007")
