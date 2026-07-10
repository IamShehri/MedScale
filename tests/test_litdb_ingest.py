"""Archival + manifest machinery: verbatim payloads, recorded hashes, byte-stable manifests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.litdb import RawRetrieval, RunManifest, archive_retrieval, write_manifest
from medscale.provenance import RetrievalStatus, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _retrieval(payload: str = '{"results": []}') -> RawRetrieval:
    return RawRetrieval(
        source_api=SourceAPI.OPENALEX,
        query="https://api.openalex.org/works?search=fhir",
        retrieved_at=_TS,
        payload=payload,
    )


def test_archive_writes_payload_verbatim(tmp_path: Path) -> None:
    entry = archive_retrieval(tmp_path, "run1", "Q2", _retrieval())
    stored = tmp_path / entry.relative_path
    assert stored.read_text(encoding="utf-8") == '{"results": []}'
    assert entry.relative_path == "raw/openalex/Q2/run1.json"
    assert entry.payload_sha256 == _retrieval().payload_sha256()
    assert entry.payload_bytes == len('{"results": []}')
    assert entry.status is RetrievalStatus.FOUND


def test_bad_run_id_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="filesystem-safe"):
        archive_retrieval(tmp_path, "run 1/../x", "Q2", _retrieval())


def test_manifest_roundtrip_and_stability(tmp_path: Path) -> None:
    entry = archive_retrieval(tmp_path, "run1", "Q2", _retrieval())
    manifest = RunManifest(run_id="run1", search_strategy_git_sha="3834bfd", entries=(entry,))
    path = write_manifest(tmp_path, manifest)
    first = path.read_bytes()
    write_manifest(tmp_path, manifest)
    assert path.read_bytes() == first  # byte-stable re-serialization
    loaded = json.loads(first)
    assert loaded["run_id"] == "run1"
    assert loaded["entries"][0]["payload_sha256"] == entry.payload_sha256
    assert loaded["entries"][0]["source_api"] == "openalex"


def test_manifest_requires_git_sha() -> None:
    with pytest.raises(ValueError, match="git SHA"):
        RunManifest(run_id="run1", search_strategy_git_sha="not-a-sha", entries=())
