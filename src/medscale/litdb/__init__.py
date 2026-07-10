"""medscale.litdb — the literature database (T1).

Schema and workflow machinery for a PRISMA-governed, citation-verified literature
corpus: bibliographic records with R1 provenance, the screening state machine and its
append-only decision log, the frozen query set, live-API adapters with an injectable
HTTP layer (CI stays offline), and archival/manifest machinery for reproducible
ingestion rounds (docs/execution/search_strategy.md).
"""

from __future__ import annotations

from medscale.litdb.adapters import (
    ArxivAdapter,
    Fetcher,
    FetchResult,
    OpenAlexAdapter,
    PubMedAdapter,
    RetrievalError,
    SemanticScholarAdapter,
    UrllibFetcher,
)
from medscale.litdb.ingest import ArchiveEntry, RunManifest, archive_retrieval, write_manifest
from medscale.litdb.parsers import ParseOutcome, parse_pubmed_esearch_ids, parse_records
from medscale.litdb.queries import QUERY_SET, RESULT_CAP, YEAR_FROM, QuerySpec, get_query
from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.screening import ScreeningStage, ScreeningState, advance_stage
from medscale.litdb.screening_log import (
    ScreeningDecision,
    append_decision,
    append_decisions,
    replay_decisions,
)
from medscale.litdb.sources import RawRetrieval, SourceAdapter
from medscale.litdb.store import load_corpus, write_corpus

__all__ = [
    "QUERY_SET",
    "RESULT_CAP",
    "YEAR_FROM",
    "ArchiveEntry",
    "ArxivAdapter",
    "EvidenceTier",
    "FetchResult",
    "Fetcher",
    "Identifiers",
    "LiteratureRecord",
    "OpenAlexAdapter",
    "ParseOutcome",
    "PubMedAdapter",
    "QuerySpec",
    "RawRetrieval",
    "RetrievalError",
    "RunManifest",
    "ScreeningDecision",
    "ScreeningStage",
    "ScreeningState",
    "SemanticScholarAdapter",
    "SourceAdapter",
    "UrllibFetcher",
    "advance_stage",
    "append_decision",
    "append_decisions",
    "archive_retrieval",
    "get_query",
    "load_corpus",
    "parse_pubmed_esearch_ids",
    "parse_records",
    "replay_decisions",
    "write_corpus",
    "write_manifest",
]
