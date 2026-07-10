"""Fuzzy dedupe: conflict-safe auto-merge, honest uncertainty, determinism."""

from __future__ import annotations

from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.dedupe import dedupe_records, normalize_title
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(
    title: str,
    *,
    doi: str | None = None,
    arxiv_id: str | None = None,
    pmid: str | None = None,
    year: int | None = 2025,
    tier: EvidenceTier = EvidenceTier.PREPRINT,
) -> LiteratureRecord:
    identifier = doi or arxiv_id or pmid or "x"
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi, arxiv_id=arxiv_id, pmid=pmid),
        title=title,
        evidence_tier=tier,
        provenance=Provenance(SourceAPI.OPENALEX, identifier, _TS, "f" * 64),
        year=year,
        abstract="a",
    )


_TITLE = "Grammar constrained decoding for clinical FHIR generation"


def test_preprint_published_twin_merges() -> None:
    preprint = _record(_TITLE, arxiv_id="2401.00001", year=2024)
    published = _record(_TITLE.upper(), doi="10.1/twin", year=2025, tier=EvidenceTier.PEER_REVIEWED)
    result = dedupe_records((preprint, published))
    assert len(result.records) == 1
    (merged,) = result.records
    assert merged.identifiers.doi == "10.1/twin"  # union
    assert merged.identifiers.arxiv_id == "2401.00001"
    assert merged.evidence_tier is EvidenceTier.PEER_REVIEWED  # DOI-bearing base wins
    (merge,) = result.merges
    assert set(merge.source_record_ids) == {preprint.record_id, published.record_id}
    assert merged.record_id == merge.merged_record_id
    assert result.uncertain == ()


def test_conflicting_dois_never_auto_merge() -> None:
    a = _record(_TITLE, doi="10.1/a")
    b = _record(_TITLE, doi="10.1/b")
    result = dedupe_records((a, b))
    assert len(result.records) == 2
    assert result.merges == ()
    (entry,) = result.uncertain
    assert "conflicting identifiers" in entry.reason


def test_generic_titles_flagged_not_merged() -> None:
    a = _record("Editorial", doi="10.1/e1", year=2025)
    b = _record("Editorial", arxiv_id="2401.9", year=2025)
    result = dedupe_records((a, b))
    assert len(result.records) == 2
    (entry,) = result.uncertain
    assert "too generic" in entry.reason


def test_missing_or_distant_years_block_merge() -> None:
    a = _record(_TITLE, doi="10.1/x", year=None)
    b = _record(_TITLE, arxiv_id="2401.1", year=2025)
    assert dedupe_records((a, b)).merges == ()
    c = _record(_TITLE, doi="10.1/y", year=2020)
    d = _record(_TITLE + " ", arxiv_id="2401.2", year=2025)
    result = dedupe_records((c, d))
    assert result.merges == ()
    assert any("year" in entry.reason for entry in result.uncertain)


def test_distinct_titles_pass_through() -> None:
    a = _record("A completely different paper about terminology grounding", doi="10.1/p")
    b = _record(_TITLE, doi="10.1/q")
    result = dedupe_records((a, b))
    assert len(result.records) == 2
    assert result.merges == () and result.uncertain == ()


def test_dedupe_is_deterministic_under_input_order() -> None:
    records = (
        _record(_TITLE, arxiv_id="2401.00001", year=2024),
        _record(_TITLE, doi="10.1/twin", year=2025),
        _record("Another unrelated title entirely for this test", pmid="7"),
    )
    forward = dedupe_records(records)
    backward = dedupe_records(tuple(reversed(records)))
    assert {r.record_id for r in forward.records} == {r.record_id for r in backward.records}
    assert forward.merges[0].merged_record_id == backward.merges[0].merged_record_id


def test_normalize_title() -> None:
    assert normalize_title("  FHIR: Generation!!  (2025) ") == "fhir generation 2025"
