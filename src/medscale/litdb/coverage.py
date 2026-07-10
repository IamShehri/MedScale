"""Search-coverage ratios from archived payloads (scientific review finding S1).

Relevance-ranked APIs plus a result cap make a round a *sample* of the matching
population. This module computes, per archived search payload, the total match count
the source reported versus the number retrieved — so every round report states its
coverage honestly instead of implying completeness.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from medscale.provenance import SourceAPI

__all__ = ["CoverageEntry", "coverage_for_manifest"]

_OPENSEARCH_NS: Final = "{http://a9.com/-/spec/opensearch/1.1/}totalResults"
_ATOM_ENTRY: Final = "{http://www.w3.org/2005/Atom}entry"


@dataclass(frozen=True)
class CoverageEntry:
    query_id: str
    source_api: SourceAPI
    total_matches: int
    retrieved: int

    @property
    def coverage_ratio(self) -> float:
        return self.retrieved / self.total_matches if self.total_matches else 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "source_api": self.source_api.value,
            "total_matches": self.total_matches,
            "retrieved": self.retrieved,
            "coverage_ratio": round(self.coverage_ratio, 6),
        }


def _counts(source: SourceAPI, payload: str) -> tuple[int, int] | None:
    """(total_matches, retrieved) for a *search* payload; None for non-search payloads."""
    if source is SourceAPI.ARXIV:
        root = ET.fromstring(payload)
        total_text = root.findtext(_OPENSEARCH_NS)
        if total_text is None:
            return None
        return int(total_text), len(root.findall(_ATOM_ENTRY))
    data = json.loads(payload)
    if source is SourceAPI.OPENALEX:
        if "meta" not in data:
            return None
        return int(data["meta"]["count"]), len(data.get("results", []))
    if source is SourceAPI.PUBMED:
        if "esearchresult" not in data:
            return None  # esummary payloads carry no population count
        result = data["esearchresult"]
        return int(result["count"]), len(result.get("idlist", []))
    if "total" not in data:
        return None
    return int(data["total"]), len(data.get("data", []))


def coverage_for_manifest(root: Path, manifest_path: Path) -> tuple[CoverageEntry, ...]:
    """Compute coverage for every search payload recorded in a round manifest."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries: list[CoverageEntry] = []
    for item in manifest["entries"]:
        source = SourceAPI(item["source_api"])
        payload = (root / item["relative_path"]).read_text(encoding="utf-8")
        counts = _counts(source, payload)
        if counts is None:
            continue
        total, retrieved = counts
        entries.append(CoverageEntry(item["query_id"], source, total, retrieved))
    return tuple(sorted(entries, key=lambda e: (e.query_id, e.source_api.value)))
