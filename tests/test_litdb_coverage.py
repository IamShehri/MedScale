"""Coverage ratios: per-source total/retrieved extraction, incl. the real round-1 manifest."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.litdb import RawRetrieval, RunManifest, archive_retrieval, write_manifest
from medscale.litdb.coverage import coverage_for_manifest
from medscale.provenance import SourceAPI

_TS = "2026-07-10T00:00:00+00:00"
_ROOT = Path(__file__).resolve().parents[1] / "data" / "litdb"


def _archive(tmp_path: Path, api: SourceAPI, query_id: str, payload: str) -> object:
    retrieval = RawRetrieval(source_api=api, query="q", retrieved_at=_TS, payload=payload)
    return archive_retrieval(tmp_path, "r1", query_id, retrieval)


def test_counts_per_source(tmp_path: Path) -> None:
    entries = (
        _archive(
            tmp_path,
            SourceAPI.OPENALEX,
            "Q1",
            json.dumps({"meta": {"count": 1000}, "results": [{}, {}]}),
        ),
        _archive(
            tmp_path,
            SourceAPI.PUBMED,
            "Q1",
            json.dumps({"esearchresult": {"count": "449", "idlist": ["1", "2", "3"]}}),
        ),
        _archive(
            tmp_path,
            SourceAPI.PUBMED,
            "Q2",
            json.dumps({"result": {"uids": []}}),  # esummary: no population count
        ),
        _archive(
            tmp_path,
            SourceAPI.ARXIV,
            "Q1",
            '<feed xmlns="http://www.w3.org/2005/Atom" '
            'xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
            "<opensearch:totalResults>77</opensearch:totalResults>"
            "<entry/><entry/></feed>",
        ),
    )
    manifest = RunManifest("r1", "abcdef1", tuple(entries))  # type: ignore[arg-type]
    path = write_manifest(tmp_path, manifest)
    coverage = coverage_for_manifest(tmp_path, path)
    by_source = {(c.query_id, c.source_api): c for c in coverage}
    assert by_source[("Q1", SourceAPI.OPENALEX)].total_matches == 1000
    assert by_source[("Q1", SourceAPI.OPENALEX)].retrieved == 2
    assert by_source[("Q1", SourceAPI.PUBMED)].total_matches == 449
    assert by_source[("Q1", SourceAPI.ARXIV)].coverage_ratio == pytest.approx(2 / 77)
    assert ("Q2", SourceAPI.PUBMED) not in by_source  # esummary skipped


@pytest.mark.skipif(not (_ROOT / "manifests" / "round1.json").exists(), reason="no round1 data")
def test_round1_manifest_coverage_computes() -> None:
    coverage = coverage_for_manifest(_ROOT, _ROOT / "manifests" / "round1.json")
    assert len(coverage) == 30  # 10 queries x 3 successful search sources
    assert all(entry.total_matches >= entry.retrieved for entry in coverage)
    q2_openalex = next(
        entry
        for entry in coverage
        if entry.query_id == "Q2" and entry.source_api is SourceAPI.OPENALEX
    )
    assert q2_openalex.total_matches == 7530  # verified during round 1
