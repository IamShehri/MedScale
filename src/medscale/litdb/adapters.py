"""Live-API adapters implementing the :class:`~medscale.litdb.sources.SourceAdapter` protocol.

Each adapter turns a concept query or identifier into exactly one HTTP request and wraps
the raw response in a :class:`RawRetrieval` envelope — the payload is archived and
hashed before any parsing (Rule R1). The HTTP layer is injected (:class:`Fetcher`), so
every adapter is fully testable offline; CI never touches the network.

Transport policy: HTTP 200 → FOUND; 404 → NOT_FOUND (a recorded fact, per R1); 429 and
every other status raise :class:`RetrievalError` — a rate limit aborts a run honestly
rather than degrading it silently.
"""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, Protocol

from medscale.litdb.sources import RawRetrieval
from medscale.provenance import RetrievalStatus, SourceAPI

__all__ = [
    "ArxivAdapter",
    "FetchResult",
    "Fetcher",
    "OpenAlexAdapter",
    "PubMedAdapter",
    "RetrievalError",
    "SemanticScholarAdapter",
    "UrllibFetcher",
]

#: Contact for polite API usage (OpenAlex mailto pool, NCBI tool/email params).
CONTACT_EMAIL: Final = "alshehriofficial@gmail.com"
USER_AGENT: Final = f"MedScale-litdb/0.0 (research; mailto:{CONTACT_EMAIL})"

_S2_FIELDS: Final = "title,year,venue,abstract,authors,externalIds"


class RetrievalError(RuntimeError):
    """A source API failed in a way that must abort the run (e.g. rate limit)."""


@dataclass(frozen=True)
class FetchResult:
    """Raw transport outcome: HTTP status and undecoded-into-anything body text."""

    status: int
    body: str


class Fetcher(Protocol):
    """The injected HTTP layer: one URL in, one raw result out."""

    def __call__(self, url: str) -> FetchResult: ...


class UrllibFetcher:
    """Default stdlib fetcher (keeps ``medscale`` dependency-free)."""

    def __init__(self, timeout_seconds: float = 30.0) -> None:
        self._timeout = timeout_seconds

    def __call__(self, url: str) -> FetchResult:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                return FetchResult(response.status, response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            return FetchResult(exc.code, body)
        except (urllib.error.URLError, OSError) as exc:
            # SSL/DNS/socket failures abort the run honestly, like any other
            # non-retriable transport condition.
            raise RetrievalError(f"transport failure at {url}: {exc}") from exc


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


class _BaseAdapter:
    """Shared request/envelope logic; subclasses only build URLs."""

    _api: SourceAPI

    def __init__(
        self,
        fetcher: Fetcher | None = None,
        now: Callable[[], str] | None = None,
    ) -> None:
        self._fetch: Fetcher = fetcher if fetcher is not None else UrllibFetcher()
        self._now: Callable[[], str] = now if now is not None else _utc_now

    @property
    def api(self) -> SourceAPI:
        return self._api

    def _retrieve(self, url: str) -> RawRetrieval:
        result = self._fetch(url)
        if result.status == 200:
            status = RetrievalStatus.FOUND
        elif result.status == 404:
            status = RetrievalStatus.NOT_FOUND
        elif result.status == 429:
            raise RetrievalError(
                f"{self._api.value}: rate-limited (HTTP 429) at {url} — "
                "back off and re-run; do not degrade the round silently"
            )
        else:
            raise RetrievalError(f"{self._api.value}: HTTP {result.status} at {url}")
        return RawRetrieval(
            source_api=self._api,
            query=url,
            retrieved_at=self._now(),
            payload=result.body,
            status=status,
        )

    def search(self, query: str, *, limit: int) -> Sequence[RawRetrieval]:
        return [self._retrieve(self._search_url(query, limit))]

    def fetch_by_identifier(self, identifier: str) -> RawRetrieval:
        return self._retrieve(self._identifier_url(identifier))

    def _search_url(self, query: str, limit: int) -> str:
        raise NotImplementedError

    def _identifier_url(self, identifier: str) -> str:
        raise NotImplementedError


class SemanticScholarAdapter(_BaseAdapter):
    _api = SourceAPI.SEMANTIC_SCHOLAR

    def _search_url(self, query: str, limit: int) -> str:
        params = urllib.parse.urlencode({"query": query, "limit": str(limit), "fields": _S2_FIELDS})
        return f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"

    def _identifier_url(self, identifier: str) -> str:
        encoded = urllib.parse.quote(identifier, safe=":/")
        params = urllib.parse.urlencode({"fields": _S2_FIELDS})
        return f"https://api.semanticscholar.org/graph/v1/paper/{encoded}?{params}"


class OpenAlexAdapter(_BaseAdapter):
    _api = SourceAPI.OPENALEX

    def _search_url(self, query: str, limit: int) -> str:
        params = urllib.parse.urlencode(
            {"search": query, "per-page": str(limit), "mailto": CONTACT_EMAIL}
        )
        return f"https://api.openalex.org/works?{params}"

    def _identifier_url(self, identifier: str) -> str:
        encoded = urllib.parse.quote(identifier, safe=":/")
        params = urllib.parse.urlencode({"mailto": CONTACT_EMAIL})
        return f"https://api.openalex.org/works/{encoded}?{params}"


class PubMedAdapter(_BaseAdapter):
    _api = SourceAPI.PUBMED

    def _search_url(self, query: str, limit: int) -> str:
        params = urllib.parse.urlencode(
            {
                "db": "pubmed",
                "term": query,
                "retmax": str(limit),
                "retmode": "json",
                "tool": "medscale-litdb",
                "email": CONTACT_EMAIL,
            }
        )
        return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"

    def _identifier_url(self, identifier: str) -> str:
        params = urllib.parse.urlencode(
            {
                "db": "pubmed",
                "id": identifier,
                "retmode": "json",
                "tool": "medscale-litdb",
                "email": CONTACT_EMAIL,
            }
        )
        return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{params}"


class ArxivAdapter(_BaseAdapter):
    _api = SourceAPI.ARXIV

    def _search_url(self, query: str, limit: int) -> str:
        params = urllib.parse.urlencode({"search_query": f"all:{query}", "max_results": str(limit)})
        return f"https://export.arxiv.org/api/query?{params}"

    def _identifier_url(self, identifier: str) -> str:
        params = urllib.parse.urlencode({"id_list": identifier})
        return f"https://export.arxiv.org/api/query?{params}"
