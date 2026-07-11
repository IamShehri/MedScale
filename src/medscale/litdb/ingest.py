"""Archival and run-manifest machinery for ingestion rounds.

Implements the reproducibility requirements of docs/execution/search_strategy.md §4:
every raw response is written verbatim to ``data/litdb/raw/<source>/<query-id>/`` with
its SHA-256 recorded, and every round produces a committed manifest citing the frozen
query set's git SHA. Replay-exactness comes from the archives; procedure-exactness from
the strategy document.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from medscale.litdb.sources import RawRetrieval
from medscale.provenance import RetrievalStatus, SourceAPI
from medscale.reproducibility import canonical_json

__all__ = ["ArchiveEntry", "RunManifest", "archive_retrieval", "write_manifest"]

_RUN_ID: Final = re.compile(r"^[A-Za-z0-9._-]+$")
_GIT_SHA: Final = re.compile(r"^[0-9a-f]{7,40}$")


def _require_run_id(run_id: str) -> str:
    if not _RUN_ID.match(run_id):
        raise ValueError(f"run_id must be filesystem-safe [A-Za-z0-9._-]+, got {run_id!r}")
    return run_id


@dataclass(frozen=True)
class ArchiveEntry:
    """One archived raw response, as it appears in the run manifest."""

    query_id: str
    source_api: SourceAPI
    status: RetrievalStatus
    retrieved_at: str
    request_url: str
    payload_sha256: str
    payload_bytes: int
    relative_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "source_api": self.source_api.value,
            "status": self.status.value,
            "retrieved_at": self.retrieved_at,
            "request_url": self.request_url,
            "payload_sha256": self.payload_sha256,
            "payload_bytes": self.payload_bytes,
            "relative_path": self.relative_path,
        }


def archive_retrieval(
    root: Path, run_id: str, query_id: str, retrieval: RawRetrieval
) -> ArchiveEntry:
    """Write one raw payload verbatim under ``root`` and return its manifest entry."""
    _require_run_id(run_id)
    if not query_id.strip():
        raise ValueError("query_id must be non-empty")
    relative = Path("raw") / retrieval.source_api.value / query_id / f"{run_id}.json"
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    payload_bytes = retrieval.payload.encode("utf-8")
    target.write_bytes(payload_bytes)
    return ArchiveEntry(
        query_id=query_id,
        source_api=retrieval.source_api,
        status=retrieval.status,
        retrieved_at=retrieval.retrieved_at,
        request_url=retrieval.query,
        payload_sha256=retrieval.payload_sha256(),
        payload_bytes=len(payload_bytes),
        relative_path=relative.as_posix(),
    )


@dataclass(frozen=True)
class RunManifest:
    """The committed record of one ingestion round."""

    run_id: str
    search_strategy_git_sha: str
    entries: tuple[ArchiveEntry, ...]

    def __post_init__(self) -> None:
        _require_run_id(self.run_id)
        if not _GIT_SHA.match(self.search_strategy_git_sha):
            raise ValueError(
                "search_strategy_git_sha must be a git SHA (7-40 hex chars), got "
                f"{self.search_strategy_git_sha!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "run_id": self.run_id,
            "search_strategy_git_sha": self.search_strategy_git_sha,
            "entries": [entry.to_dict() for entry in self.entries],
        }


def write_manifest(root: Path, manifest: RunManifest) -> Path:
    """Serialize the manifest canonically (byte-stable) to ``manifests/<run_id>.json``."""
    target = root / "manifests" / f"{manifest.run_id}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" pins LF on every platform — manifests must be byte-identical
    # regardless of the OS that wrote them.
    target.write_text(canonical_json(manifest.to_dict()) + "\n", encoding="utf-8", newline="\n")
    return target
