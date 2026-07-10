"""medscale.litdb — the literature database foundation (T1).

Schema and workflow machinery for a PRISMA-governed, citation-verified literature
corpus: bibliographic records with R1 provenance, the screening state machine, and the
source-adapter protocol. Network adapters for the live APIs land only when the search
strategy (docs/execution/search_strategy.md) is frozen; nothing in this package
performs I/O.
"""

from __future__ import annotations

from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.screening import ScreeningStage, ScreeningState, advance_stage
from medscale.litdb.sources import RawRetrieval, SourceAdapter

__all__ = [
    "EvidenceTier",
    "Identifiers",
    "LiteratureRecord",
    "RawRetrieval",
    "ScreeningStage",
    "ScreeningState",
    "SourceAdapter",
    "advance_stage",
]
