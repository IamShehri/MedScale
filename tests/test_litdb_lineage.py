"""Query lineage: merge-chain resolution and tag rebuilding from manifests."""

from __future__ import annotations

import json
from pathlib import Path

from medscale.litdb import RawRetrieval, RunManifest, archive_retrieval, write_manifest
from medscale.litdb.integrity import Merge
from medscale.litdb.lineage import build_query_tags, resolve_lineage
from medscale.provenance import SourceAPI
from medscale.reproducibility import canonical_json

_TS = "2026-07-10T00:00:00+00:00"


def test_resolve_lineage_direct_and_chained() -> None:
    merges = (
        Merge("m1", ("a", "b")),
        Merge("m2", ("m1", "c")),  # chain: a -> m1 -> m2
    )
    lineage = resolve_lineage(merges)
    assert lineage["a"] == "m2"
    assert lineage["b"] == "m2"
    assert lineage["c"] == "m2"
    assert lineage["m1"] == "m2"


def test_resolve_lineage_cycle_safe() -> None:
    # pathological input must not loop forever
    merges = (Merge("x", ("y",)), Merge("y", ("x",)))
    lineage = resolve_lineage(merges)
    assert set(lineage) == {"x", "y"}


def _openalex_payload(doi: str, title: str) -> str:
    return json.dumps(
        {
            "meta": {"count": 1},
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "doi": f"https://doi.org/{doi}",
                    "display_name": title,
                    "publication_year": 2025,
                    "primary_location": {"source": {"display_name": "J", "type": "journal"}},
                }
            ],
        }
    )


def test_build_query_tags_from_manifests(tmp_path: Path) -> None:
    # two queries retrieve the same DOI -> record gets both tags
    entries = []
    for query_id in ("Q1", "Q2"):
        retrieval = RawRetrieval(
            source_api=SourceAPI.OPENALEX,
            query=f"https://api.openalex.org/works?search={query_id}",
            retrieved_at=_TS,
            payload=_openalex_payload("10.1/x", "A grammar constrained decoding study"),
        )
        entries.append(archive_retrieval(tmp_path, "r1", query_id, retrieval))
    write_manifest(tmp_path, RunManifest("r1", "abcdef1", tuple(entries)))

    tags = build_query_tags(tmp_path)
    assert len(tags) == 1
    (record_tags,) = tags.values()
    assert record_tags == {"Q1", "Q2"}


def test_build_query_tags_follows_merge_lineage(tmp_path: Path) -> None:
    retrieval = RawRetrieval(
        source_api=SourceAPI.OPENALEX,
        query="https://api.openalex.org/works?search=q",
        retrieved_at=_TS,
        payload=_openalex_payload("10.1/y", "Another grammar constrained decoding study"),
    )
    entry = archive_retrieval(tmp_path, "r1", "Q3", retrieval)
    write_manifest(tmp_path, RunManifest("r1", "abcdef1", (entry,)))

    # pretend the parsed record was merged away into "merged-id"
    from medscale.litdb.parsers import parse_records

    (parsed,) = parse_records(retrieval).records
    merge_log = tmp_path / "screening" / "merge_log.jsonl"
    merge_log.parent.mkdir(parents=True, exist_ok=True)
    merge_log.write_text(
        canonical_json(
            {
                "merged_record_id": "merged-id",
                "source_record_ids": [parsed.record_id, "other-src"],
                "source_records": [],
                "reason": "test",
            }
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    tags = build_query_tags(tmp_path)
    assert tags == {"merged-id": {"Q3"}}  # tag landed on the MERGED id, not the source
