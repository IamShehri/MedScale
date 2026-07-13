"""Deterministic dataset generation utilities.

Stability: **public**. These helpers create frozen dataset artifacts from the
internal corpus. No external data sources are used.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from medscale.dataset.manifest import DatasetManifest, write_manifest
from medscale.dataset.split import DeterministicSplitter, SplitResult
from medscale.litdb.records import LiteratureRecord
from medscale.provenance import Provenance

__all__ = [
    "LiteratureRecord",
    "Provenance",
    "load_corpus_records",
    "filter_format1_records",
    "write_dataset_records",
    "write_split_files",
    "write_licenses_metadata",
    "write_dataset",
]


def _sha256_of(value: object) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _record_id(record: LiteratureRecord) -> str:
    return getattr(record, "record_id")


def load_corpus_records(corpus_path: Path) -> list[LiteratureRecord]:
    """Load a JSONL corpus into deterministic literature records."""
    records: list[LiteratureRecord] = []
    with corpus_path.open(encoding="utf-8") as source:
        for line in source:
            text = line.strip()
            if not text:
                continue
            payload = json.loads(text)
            provenance = Provenance(
                source_api=payload["provenance"]["source_api"],
                identifier=payload["provenance"]["identifier"],
                status=payload["provenance"]["status"],
                verified_at=payload["provenance"]["verified_at"],
                raw_response_sha256=payload["provenance"]["raw_response_sha256"],
            )
            record = LiteratureRecord(
                record_id=payload["record_id"],
                title=payload.get("title"),
                abstract=payload.get("abstract"),
                authors=payload.get("authors") or [],
                year=payload.get("year"),
                venue=payload.get("venue"),
                identifiers=payload.get("identifiers") or {},
                tags=payload.get("tags") or [],
                evidence_tier=payload.get("evidence_tier"),
                license_spdx=payload.get("license_spdx"),
                format=payload.get("format"),
                provenance=provenance,
            )
            records.append(record)
    return records


def filter_format1_records(records: Iterable[LiteratureRecord]) -> tuple[LiteratureRecord, ...]:
    return tuple(record for record in records if record.format == 1)


@dataclass(frozen=True)
class _LicenseSummary:
    spdx: str | None
    count: int


def _coalesce_record_license(record: LiteratureRecord) -> str | None:
    license_spdx = getattr(record, "license_spdx", None)
    if isinstance(license_spdx, str) and license_spdx.strip():
        return license_spdx.strip()
    return None


def build_license_summary(records: Iterable[LiteratureRecord]) -> tuple[_LicenseSummary, ...]:
    counts: Counter[str | None] = Counter()
    for record in records:
        counts[_coalesce_record_license(record)] += 1
    return tuple(
        _LicenseSummary(spdx=key, count=value)
        for key, value in sorted(counts.items(), key=lambda item: (item[0] is None, item[0] or ""))
    )


def write_licenses_metadata(dataset_dir: Path, records: Iterable[LiteratureRecord]) -> Path:
    license_dir = dataset_dir / "metadata"
    license_dir.mkdir(parents=True, exist_ok=True)
    summary = build_license_summary(records)
    payload = {
        "dataset_id": dataset_dir.name,
        "license_summary": [
            {"spdx": item.spdx or "unknown", "count": item.count} for item in summary
        ],
        "unknown_count": sum(item.count for item in summary if item.spdx is None),
    }
    path = license_dir / "licenses.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_dataset_records(
    dataset_dir: Path,
    records: Iterable[LiteratureRecord],
) -> None:
    dataset_dir.mkdir(parents=True, exist_ok=True)
    path = dataset_dir / "records.json"
    payload = [
        {
            "record_id": record.record_id,
            "title": record.title,
            "abstract": record.abstract,
            "authors": record.authors,
            "year": record.year,
            "venue": record.venue,
            "identifiers": record.identifiers,
            "tags": record.tags,
            "evidence_tier": record.evidence_tier,
            "license_spdx": record.license_spdx,
        }
        for record in records
    ]
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_split_files(
    dataset_dir: Path,
    split_result: SplitResult,
    records: Sequence[LiteratureRecord],
) -> None:
    splits_dir = dataset_dir / "splits"
    splits_dir.mkdir(parents=True, exist_ok=True)
    mapping = {record.record_id: record for record in records}
    for partition in ("train", "validation", "test"):
        items = [mapping[record_id] for record_id in getattr(split_result, partition) if record_id in mapping]
        write_dataset_records(splits_dir / f"{partition}.json", items)


def write_dataset(
    dataset_dir: Path,
    corpus_path: Path,
    *,
    dataset_id: str = "medscale-dataset-v1",
    version: str = "1.0",
    dataset_version_seed: int = 42,
    dataset_split_seed: int = 42,
    write_manifest_file: bool = True,
) -> SplitResult:
    if not corpus_path.exists():
        raise FileNotFoundError(f"missing corpus: {corpus_path}")
