"""medscale.research — the Research Intelligence read layer.

Stability: **internal** (except ``ResearchIndex``, re-exposed via the root contract
through ``Workspace.index()``).

Turns stored artifacts into a queryable scientific evidence engine. Everything here is
a *pure read*: no hidden state, no mutation, no caching, no ML, no probabilistic
ranking — deterministic functions over an immutable :class:`ResearchIndex`, so a
researcher in 2035 running the same query over the same snapshot obtains the same
bytes.

Future-API contract (internal call -> eventual REST surface, designed now, served
later):

- ``evidence_where(...)``      -> GET /evidence
- ``records_where(...)``       -> GET /sources
- ``corpus_stats/...``         -> GET /stats
- ``capture_snapshot(...)``    -> GET|POST /snapshots
- research-question filters    -> GET /research/questions

Layer position (ADR-0012): Research Infrastructure, consuming Knowledge (litdb) and
Evidence layers through their public loaders only.
"""

from __future__ import annotations

from medscale.research.index import ResearchIndex, ReviewEventLite
from medscale.research.query import evidence_where, records_where
from medscale.research.snapshot import (
    ResearchSnapshot,
    capture_snapshot,
    load_snapshot,
    verify_snapshot,
    write_snapshot,
)
from medscale.research.stats import (
    CorpusStats,
    EvidenceStats,
    ScreeningStats,
    corpus_stats,
    evidence_stats,
    screening_stats,
)

__all__ = [
    "CorpusStats",
    "EvidenceStats",
    "ResearchIndex",
    "ResearchSnapshot",
    "ReviewEventLite",
    "ScreeningStats",
    "capture_snapshot",
    "corpus_stats",
    "evidence_stats",
    "evidence_where",
    "load_snapshot",
    "records_where",
    "screening_stats",
    "verify_snapshot",
    "write_snapshot",
]
