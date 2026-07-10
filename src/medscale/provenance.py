"""Provenance: Rule R1 as a datatype.

Every claim and every literature record in MedScale carries a provenance chain that is
auditable down to the SHA-256 of the raw API response it came from. A failed lookup is a
recorded fact (``NOT_FOUND``), never backfilled from memory.

See ADR-0009 (docs/adr/0009-evidence-model.md) §3.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Final

__all__ = ["Provenance", "RetrievalStatus", "SourceAPI", "validate_timestamp"]

_SHA256_HEX: Final = re.compile(r"^[0-9a-f]{64}$")


class SourceAPI(enum.Enum):
    """The live APIs evidence may be verified against (Rule R1)."""

    SEMANTIC_SCHOLAR = "semantic_scholar"
    OPENALEX = "openalex"
    PUBMED = "pubmed"
    ARXIV = "arxiv"


class RetrievalStatus(enum.Enum):
    """Outcome of a source lookup. NOT_FOUND is recorded, never papered over."""

    FOUND = "found"
    NOT_FOUND = "not_found"


def validate_timestamp(value: str, field_name: str) -> str:
    """Require an explicit, timezone-aware ISO-8601 timestamp and return it.

    Timestamps are always explicit inputs (never an implicit ``now()``), so that every
    object that embeds one is reproducible byte-for-byte.
    """
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} is not ISO-8601: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must be timezone-aware, got naive {value!r}")
    return value


@dataclass(frozen=True)
class Provenance:
    """Where a fact came from, when it was verified, and the hash of what came back."""

    source_api: SourceAPI
    identifier: str
    verified_at: str
    raw_response_sha256: str
    status: RetrievalStatus = RetrievalStatus.FOUND

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("provenance identifier must be non-empty")
        validate_timestamp(self.verified_at, "verified_at")
        if not _SHA256_HEX.match(self.raw_response_sha256):
            raise ValueError(
                f"raw_response_sha256 must be 64 lowercase hex chars, got "
                f"{self.raw_response_sha256!r}"
            )
