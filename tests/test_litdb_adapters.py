"""Adapters: URL construction, envelope wrapping, and transport-status policy — offline."""

from __future__ import annotations

import pytest

from medscale.litdb import (
    ArxivAdapter,
    FetchResult,
    OpenAlexAdapter,
    PubMedAdapter,
    RetrievalError,
    SemanticScholarAdapter,
)
from medscale.provenance import RetrievalStatus, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


class FakeFetcher:
    def __init__(self, status: int = 200, body: str = "{}") -> None:
        self.status = status
        self.body = body
        self.urls: list[str] = []

    def __call__(self, url: str) -> FetchResult:
        self.urls.append(url)
        return FetchResult(self.status, self.body)


def _now() -> str:
    return _TS


def test_search_wraps_payload_with_request_url() -> None:
    fetcher = FakeFetcher(body='{"data": []}')
    adapter = SemanticScholarAdapter(fetcher=fetcher, now=_now)
    (result,) = adapter.search("FHIR validation", limit=5)
    assert result.source_api is SourceAPI.SEMANTIC_SCHOLAR
    assert result.payload == '{"data": []}'
    assert result.retrieved_at == _TS
    assert result.query == fetcher.urls[0]
    assert "api.semanticscholar.org/graph/v1/paper/search" in result.query
    assert "limit=5" in result.query


def test_openalex_search_url_is_polite_and_field_trimmed() -> None:
    fetcher = FakeFetcher()
    (result,) = OpenAlexAdapter(fetcher=fetcher, now=_now).search("fhir", limit=3)
    assert "api.openalex.org/works" in result.query
    assert "per-page=3" in result.query
    assert "mailto=" in result.query
    # ADR-0016: request only parser-consumed fields (archive-volume control)
    assert "select=" in result.query
    for field in ("doi", "display_name", "abstract_inverted_index", "authorships"):
        assert field in result.query


def test_pubmed_urls() -> None:
    fetcher = FakeFetcher()
    adapter = PubMedAdapter(fetcher=fetcher, now=_now)
    (search,) = adapter.search("fhir AND llm", limit=7)
    assert "esearch.fcgi" in search.query
    assert "retmax=7" in search.query
    fetched = adapter.fetch_by_identifier("12345678")
    assert "esummary.fcgi" in fetched.query
    assert "id=12345678" in fetched.query


def test_arxiv_urls() -> None:
    fetcher = FakeFetcher(body="<feed/>")
    adapter = ArxivAdapter(fetcher=fetcher, now=_now)
    (search,) = adapter.search("constrained decoding", limit=4)
    assert "export.arxiv.org/api/query" in search.query
    assert "max_results=4" in search.query
    fetched = adapter.fetch_by_identifier("2401.00001")
    assert "id_list=2401.00001" in fetched.query


def test_404_maps_to_not_found() -> None:
    adapter = OpenAlexAdapter(fetcher=FakeFetcher(status=404, body=""), now=_now)
    result = adapter.fetch_by_identifier("doi:10.1/none")
    assert result.status is RetrievalStatus.NOT_FOUND


def test_429_raises_retrieval_error() -> None:
    adapter = SemanticScholarAdapter(fetcher=FakeFetcher(status=429), now=_now)
    with pytest.raises(RetrievalError, match="rate-limited"):
        adapter.search("fhir", limit=1)


def test_other_errors_raise() -> None:
    adapter = PubMedAdapter(fetcher=FakeFetcher(status=500), now=_now)
    with pytest.raises(RetrievalError, match="HTTP 500"):
        adapter.fetch_by_identifier("1")


def test_urllib_fetcher_wraps_transport_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.error
    import urllib.request

    from medscale.litdb import UrllibFetcher

    def boom(*args: object, **kwargs: object) -> object:
        raise urllib.error.URLError("certificate verify failed")

    monkeypatch.setattr(urllib.request, "urlopen", boom)
    with pytest.raises(RetrievalError, match="transport failure"):
        UrllibFetcher()("https://example.org/x")
