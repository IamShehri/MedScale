"""Source abstraction: the adapter protocol and the raw-retrieval envelope.

Design only — no network code lives in this module or this phase. Concrete adapters for
the live APIs (Semantic Scholar, OpenAlex, PubMed, arXiv) are implemented when the
search strategy is frozen; they must return :class:`RawRetrieval` envelopes so that the
raw payload is archived and hashed before any parsing (Rule R1 audit trail).
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from medscale.provenance import (
    Provenance,
    RetrievalStatus,
    SourceAPI,
    validate_timestamp,
)

__all__ = ["RawRetrieval", "SourceAdapter"]


@dataclass(frozen=True)
class RawRetrieval:
    """Exactly what a source API returned, before any interpretation."""

    source_api: SourceAPI
    query: str
    retrieved_at: str
    payload: str
    status: RetrievalStatus = RetrievalStatus.FOUND

    def __post_init__(self) -> None:
        if not self.query.strip():
            raise ValueError("query must be non-empty")
        validate_timestamp(self.retrieved_at, "retrieved_at")

    def payload_sha256(self) -> str:
        """SHA-256 of the raw payload — the anchor of the provenance chain."""
        return hashlib.sha256(self.payload.encode("utf-8")).hexdigest()

    def to_provenance(self, identifier: str) -> Provenance:
        """Bind this retrieval to a resolvable identifier as R1 provenance."""
        return Provenance(
            source_api=self.source_api,
            identifier=identifier,
            verified_at=self.retrieved_at,
            raw_response_sha256=self.payload_sha256(),
            status=self.status,
        )


class SourceAdapter(Protocol):
    """What every live-API adapter must look like (structural typing).

    Implementations perform I/O; everything downstream of :class:`RawRetrieval` is pure
    and deterministic.
    """

    @property
    def api(self) -> SourceAPI: ...

    def fetch_by_identifier(self, identifier: str) -> RawRetrieval: ...

    def search(self, query: str, *, limit: int) -> Sequence[RawRetrieval]: ...
