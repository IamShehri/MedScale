"""Corpus persistence: LiteratureRecords as a deterministic JSONL file.

The corpus file is a committed artifact: canonical JSON per line, LF-terminated,
sorted by ``record_id``, deduplicated by construction on write. Two corpora built from
the same records are byte-identical regardless of input order or platform — the same
byte-stability contract as manifests.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from medscale.litdb.records import EvidenceTier, Identifiers, LiteratureRecord
from medscale.provenance import Provenance, RetrievalStatus, SourceAPI
from medscale.reproducibility import canonical_json

__all__ = ["load_corpus", "record_from_dict", "record_to_dict", "write_corpus"]


def record_to_dict(record: LiteratureRecord) -> dict[str, Any]:
    return {
        "record_id": record.record_id,
        "identifiers": {
            "doi": record.identifiers.doi,
            "pmid": record.identifiers.pmid,
            "arxiv_id": record.identifiers.arxiv_id,
            "s2_corpus_id": record.identifiers.s2_corpus_id,
        },
        "title": record.title,
        "evidence_tier": record.evidence_tier.value,
        "provenance": {
            "source_api": record.provenance.source_api.value,
            "identifier": record.provenance.identifier,
            "verified_at": record.provenance.verified_at,
            "raw_response_sha256": record.provenance.raw_response_sha256,
            "status": record.provenance.status.value,
        },
        "year": record.year,
        "venue": record.venue,
        "authors": list(record.authors),
        "abstract": record.abstract,
        "license_spdx": record.license_spdx,
        "tags": list(record.tags),
    }


def record_from_dict(data: dict[str, Any]) -> LiteratureRecord:
    identifiers = data["identifiers"]
    provenance = data["provenance"]
    return LiteratureRecord(
        identifiers=Identifiers(
            doi=identifiers.get("doi"),
            pmid=identifiers.get("pmid"),
            arxiv_id=identifiers.get("arxiv_id"),
            s2_corpus_id=identifiers.get("s2_corpus_id"),
        ),
        title=data["title"],
        evidence_tier=EvidenceTier(data["evidence_tier"]),
        provenance=Provenance(
            source_api=SourceAPI(provenance["source_api"]),
            identifier=provenance["identifier"],
            verified_at=provenance["verified_at"],
            raw_response_sha256=provenance["raw_response_sha256"],
            status=RetrievalStatus(provenance["status"]),
        ),
        year=data.get("year"),
        venue=data.get("venue"),
        authors=tuple(data.get("authors", [])),
        abstract=data.get("abstract"),
        license_spdx=data.get("license_spdx"),
        tags=tuple(data.get("tags", [])),
    )


def write_corpus(path: Path, records: Iterable[LiteratureRecord]) -> int:
    """Write records deduplicated by ``record_id``, sorted, LF. Returns unique count.

    First occurrence wins on duplicate ids (identifier-exact PRISMA dedupe, pass 1 —
    which provenance survives is immaterial: identity is the identifiers).
    """
    unique: dict[str, LiteratureRecord] = {}
    for record in records:
        unique.setdefault(record.record_id, record)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [canonical_json(record_to_dict(unique[rid])) for rid in sorted(unique)]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8", newline="\n")
    return len(unique)


def load_corpus(path: Path) -> tuple[LiteratureRecord, ...]:
    """Load a corpus file, re-running every record validation."""
    records = [
        record_from_dict(json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return tuple(records)
