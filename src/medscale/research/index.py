"""The immutable research index: one load, joined read views, deterministic order.

Loads corpus, review state, review events, and evidence objects through their public
loaders, sorts everything by content-addressed id, and exposes derived lookups. The
index is a value, not a service — build it, query it, discard it. Same tree in, same
index out.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

import medscale._layout as _layout
from medscale.evidence import EvidenceObject
from medscale.evidence_store import load_evidence
from medscale.litdb.records import LiteratureRecord
from medscale.litdb.review import RecordReview, current_reviews
from medscale.litdb.store import load_corpus

__all__ = ["ResearchIndex", "ReviewEventLite"]

_CORPUS: Final = _layout.CORPUS
_REVIEW_LOG: Final = _layout.REVIEW_LOG
_EVIDENCE: Final = _layout.EVIDENCE


@dataclass(frozen=True)
class ReviewEventLite:
    """The agreement-relevant projection of a review event (attribution triple)."""

    record_id: str
    reviewer: str
    decision: str


def _load_review_events(path: Path) -> tuple[ReviewEventLite, ...]:
    if not path.exists():
        return ()
    events: list[ReviewEventLite] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        events.append(
            ReviewEventLite(
                record_id=str(data["record_id"]),
                reviewer=str(data["reviewer"]),
                decision=str(data["new_decision"]),
            )
        )
    return tuple(events)  # log order preserved: replay semantics, latest-wins downstream


@dataclass(frozen=True)
class ResearchIndex:
    """Joined, immutable view over the litdb + evidence stores."""

    records: tuple[LiteratureRecord, ...]
    reviews: dict[str, RecordReview]
    review_events: tuple[ReviewEventLite, ...]
    evidence: tuple[EvidenceObject, ...]
    by_record_id: dict[str, LiteratureRecord] = field(default_factory=dict)

    @classmethod
    def load(cls, root: Path) -> ResearchIndex:
        corpus_path = root / _CORPUS
        loaded = load_corpus(corpus_path) if corpus_path.exists() else ()
        records = tuple(sorted(loaded, key=lambda r: r.record_id))
        evidence = tuple(sorted(load_evidence(root / _EVIDENCE), key=lambda e: e.evidence_id))
        return cls(
            records=records,
            reviews=current_reviews(root / _REVIEW_LOG),
            review_events=_load_review_events(root / _REVIEW_LOG),
            evidence=evidence,
            by_record_id={record.record_id: record for record in records},
        )
