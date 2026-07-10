"""Source abstraction: the retrieval envelope and the adapter protocol."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence

import pytest

from medscale.litdb import RawRetrieval, SourceAdapter
from medscale.provenance import RetrievalStatus, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def test_payload_hash_matches_sha256() -> None:
    r = RawRetrieval(SourceAPI.ARXIV, "cat:cs.CL", _TS, payload='{"ok": true}')
    assert r.payload_sha256() == hashlib.sha256(b'{"ok": true}').hexdigest()


def test_to_provenance_binds_identifier_and_hash() -> None:
    r = RawRetrieval(SourceAPI.PUBMED, "pmid:123", _TS, payload="{}")
    p = r.to_provenance("123")
    assert p.source_api is SourceAPI.PUBMED
    assert p.identifier == "123"
    assert p.verified_at == _TS
    assert p.raw_response_sha256 == r.payload_sha256()
    assert p.status is RetrievalStatus.FOUND


def test_not_found_flows_into_provenance() -> None:
    r = RawRetrieval(
        SourceAPI.OPENALEX, "doi:10.1/none", _TS, payload="", status=RetrievalStatus.NOT_FOUND
    )
    assert r.to_provenance("10.1/none").status is RetrievalStatus.NOT_FOUND


def test_empty_query_rejected() -> None:
    with pytest.raises(ValueError, match="query"):
        RawRetrieval(SourceAPI.ARXIV, "  ", _TS, payload="{}")


class _StubAdapter:
    """A network-free stand-in proving the protocol is implementable."""

    @property
    def api(self) -> SourceAPI:
        return SourceAPI.SEMANTIC_SCHOLAR

    def fetch_by_identifier(self, identifier: str) -> RawRetrieval:
        return RawRetrieval(self.api, f"id:{identifier}", _TS, payload="{}")

    def search(self, query: str, *, limit: int) -> Sequence[RawRetrieval]:
        return [RawRetrieval(self.api, query, _TS, payload="{}")][:limit]


def test_stub_satisfies_protocol() -> None:
    adapter: SourceAdapter = _StubAdapter()
    assert adapter.api is SourceAPI.SEMANTIC_SCHOLAR
    assert adapter.fetch_by_identifier("x").query == "id:x"
    assert len(adapter.search("fhir", limit=1)) == 1
