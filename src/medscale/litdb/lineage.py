"""Query lineage: which frozen queries retrieved each corpus record.

Records are parsed from per-query archives, then possibly merged by dedupe (which mints
a new ``record_id``). This module rebuilds the record → query-ids mapping from the
committed manifests and merge log, resolving every parse-time id through merge lineage
so merged records inherit the union of their sources' query tags.

Why it matters operationally: screening can then be batched by research topic
(`medscale screen next --query Q2`), and scientifically: per-query PRISMA slices become
computable.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from pathlib import Path

from medscale.litdb.integrity import Merge
from medscale.litdb.parsers import parse_records
from medscale.litdb.sources import RawRetrieval
from medscale.provenance import RetrievalStatus, SourceAPI

__all__ = ["build_query_tags", "resolve_lineage"]


def resolve_lineage(merges: Iterable[Merge]) -> dict[str, str]:
    """source record_id -> final merged record_id, following chains across rounds."""
    one_hop = {
        source: merge.merged_record_id for merge in merges for source in merge.source_record_ids
    }

    def final(record_id: str) -> str:
        seen: set[str] = set()
        while record_id in one_hop and record_id not in seen:
            seen.add(record_id)
            record_id = one_hop[record_id]
        return record_id

    return {source: final(source) for source in one_hop}


def _load_merges(path: Path) -> tuple[Merge, ...]:
    if not path.exists():
        return ()
    return tuple(
        Merge(str(d["merged_record_id"]), tuple(d["source_record_ids"]))
        for d in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    )


def build_query_tags(root: Path) -> dict[str, set[str]]:
    """final record_id -> query ids, rebuilt from every committed round manifest."""
    lineage = resolve_lineage(_load_merges(root / "screening" / "merge_log.jsonl"))
    tags: dict[str, set[str]] = {}
    for manifest_path in sorted((root / "manifests").glob("*.json")):
        manifest: Mapping[str, object] = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest["entries"]
        assert isinstance(entries, list)
        for entry in entries:
            payload_path = root / str(entry["relative_path"])
            if not payload_path.exists():
                continue
            retrieval = RawRetrieval(
                source_api=SourceAPI(str(entry["source_api"])),
                query=str(entry["request_url"]),
                retrieved_at=str(entry["retrieved_at"]),
                payload=payload_path.read_text(encoding="utf-8"),
                status=RetrievalStatus(str(entry["status"])),
            )
            query_id = str(entry["query_id"])
            for record in parse_records(retrieval).records:
                final_id = lineage.get(record.record_id, record.record_id)
                tags.setdefault(final_id, set()).add(query_id)
    return tags
