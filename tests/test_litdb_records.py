"""Literature record schema: R1 identifier requirement and dedupe-by-construction."""

from __future__ import annotations

import pytest

from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _provenance(api: SourceAPI = SourceAPI.PUBMED) -> Provenance:
    return Provenance(api, "10.1000/example", _TS, "c" * 64)


def test_at_least_one_identifier_required() -> None:
    with pytest.raises(ValueError, match="Rule R1"):
        Identifiers()
    with pytest.raises(ValueError, match="Rule R1"):
        Identifiers(doi="   ")


def test_doi_normalized_lowercase() -> None:
    ids = Identifiers(doi="  10.1000/ABC.Def  ")
    assert ids.doi == "10.1000/abc.def"


def test_record_id_deduplicates_across_sources() -> None:
    """Same DOI fetched from two APIs at two times -> one record identity."""
    a = LiteratureRecord(
        identifiers=Identifiers(doi="10.1000/x"),
        title="A study",
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=_provenance(SourceAPI.PUBMED),
    )
    b = LiteratureRecord(
        identifiers=Identifiers(doi="10.1000/X"),
        title="A Study (variant metadata)",
        evidence_tier=EvidenceTier.PREPRINT,
        provenance=Provenance(SourceAPI.OPENALEX, "W99", _TS, "d" * 64),
    )
    assert a.record_id == b.record_id


def test_different_identifiers_different_records() -> None:
    a = LiteratureRecord(
        identifiers=Identifiers(doi="10.1000/x"),
        title="A",
        evidence_tier=EvidenceTier.GREY,
        provenance=_provenance(),
    )
    b = LiteratureRecord(
        identifiers=Identifiers(pmid="123"),
        title="A",
        evidence_tier=EvidenceTier.GREY,
        provenance=_provenance(),
    )
    assert a.record_id != b.record_id


def test_empty_title_rejected() -> None:
    with pytest.raises(ValueError, match="title"):
        LiteratureRecord(
            identifiers=Identifiers(pmid="123"),
            title="  ",
            evidence_tier=EvidenceTier.GREY,
            provenance=_provenance(),
        )


def test_evidence_tier_values_match_taxonomy() -> None:
    assert {t.value for t in EvidenceTier} == {
        "peer-reviewed",
        "preprint",
        "benchmark-report",
        "grey",
    }
