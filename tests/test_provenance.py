"""Provenance is Rule R1 as a datatype: these tests lock its validation contract."""

from __future__ import annotations

import pytest

from medscale.provenance import Provenance, RetrievalStatus, SourceAPI

_HASH = "a" * 64
_TS = "2026-07-10T00:00:00+00:00"


def test_valid_provenance_constructs() -> None:
    p = Provenance(
        source_api=SourceAPI.PUBMED,
        identifier="12345678",
        verified_at=_TS,
        raw_response_sha256=_HASH,
    )
    assert p.status is RetrievalStatus.FOUND


def test_not_found_is_recordable() -> None:
    p = Provenance(
        source_api=SourceAPI.SEMANTIC_SCHOLAR,
        identifier="10.1000/does-not-exist",
        verified_at=_TS,
        raw_response_sha256=_HASH,
        status=RetrievalStatus.NOT_FOUND,
    )
    assert p.status is RetrievalStatus.NOT_FOUND


def test_empty_identifier_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        Provenance(SourceAPI.ARXIV, "   ", _TS, _HASH)


def test_naive_timestamp_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        Provenance(SourceAPI.ARXIV, "2401.00001", "2026-07-10T00:00:00", _HASH)


def test_malformed_timestamp_rejected() -> None:
    with pytest.raises(ValueError, match="ISO-8601"):
        Provenance(SourceAPI.ARXIV, "2401.00001", "yesterday", _HASH)


@pytest.mark.parametrize("bad", ["", "abc", "A" * 64, "g" * 64])
def test_malformed_hash_rejected(bad: str) -> None:
    with pytest.raises(ValueError, match="64 lowercase hex"):
        Provenance(SourceAPI.OPENALEX, "W1234", _TS, bad)
