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

__all__ = [
    "filter_format1_records",
    "load_corpus_records",
    "write_dataset",
    "write_dataset_records",
    "write_licenses_metadata",
    "write_split_files",
]


def _coalesce(value: str | None) -> str | None:
    value = value.strip() if isinstance(value, str) else ""
    return value or None


def load_corpus_records(corpus_path: Path) -> list[dict[str, object]]:
    """Load a JSONL corpus into typed dictionaries."""
    records: list[dict[str, object]] = []
    with corpus_path.open(encoding="utf-8") as source:
        for line in source:
            text = line.strip()
            if not text:
                continue
            try:
                records.append(json.loads(text))
            except json.JSONDecodeError as exc:
                raise ValueError(f"line is not valid JSON in {corpus_path}: {exc}") from exc
    return records


def filter_format1_records(records: Iterable[dict[str, object]]) -> tuple[dict[str, object], ...]:
    return tuple(record for record in records if record.get("format") == 1)


@dataclass(frozen=True)
class _LicenseSummary:
    spdx: str | None
    count: int


def build_license_summary(records: Iterable[dict[str, object]]) -> dict[str, int]:
    counts: Counter[str | None] = Counter()
    for record in records:
        license_spdx = record.get("license_spdx")
        spdx = _coalesce(license_spdx) if isinstance(license_spdx, str) else None
        counts[spdx] += 1
    summary: dict[str, int] = {}
    for key, value in counts.items():
        if key is None:
            summary["unknown"] = value
        else:
            summary[key] = value
    return summary


def write_licenses_metadata(
    dataset_dir: Path,
    records: Iterable[dict[str, object]],
) -> Path:
    license_dir = dataset_dir / "metadata"
    license_dir.mkdir(parents=True, exist_ok=True)
    summary = build_license_summary(records)
    payload = {
        "dataset_id": dataset_dir.name,
        "license_summary": [
            {"spdx": key, "count": value} for key, value in sorted(summary.items())
        ],
        "unknown_count": summary.get("unknown", 0),
    }
    path = license_dir / "licenses.json"
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    return path


def write_dataset_records(
    dataset_dir: Path,
    records: Iterable[dict[str, object]],
) -> None:
    dataset_dir.mkdir(parents=True, exist_ok=True)
    path = dataset_dir / "records.json"
    path.write_text(
        json.dumps(list(records), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_split_files(
    dataset_dir: Path,
    split_result: object,
    records: Sequence[dict[str, object]],
) -> None:
    splits_dir = dataset_dir / "splits"
    splits_dir.mkdir(parents=True, exist_ok=True)
    mapping = {str(record.get("record_id")): record for record in records}
    for partition in ("train", "validation", "test"):
        ids = list(getattr(split_result, partition))
        items = [mapping[record_id] for record_id in ids if record_id in mapping]
        # splits/<partition>.json is a FILE in the ADR-0030 layout; routing it
        # through write_dataset_records used to create a directory of that name,
        # which crashed validate_dataset and broke fingerprints/checksums.
        (splits_dir / f"{partition}.json").write_text(
            json.dumps(items, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def write_dataset(
    dataset_dir: Path,
    corpus_path: Path,
    *,
    dataset_id: str = "medscale-dataset-v1",
    version: str = "1.0",
    seed: int = 42,
) -> list[str]:
    if not corpus_path.exists():
        raise FileNotFoundError(f"missing corpus: {corpus_path}")

    records = load_corpus_records(corpus_path)
    filtered = filter_format1_records(records)
    record_ids = [str(record.get("record_id")) for record in filtered]

    write_dataset_records(dataset_dir, filtered)
    write_split_files(dataset_dir, _DeterministicSplitResult(seed, record_ids), filtered)
    write_licenses_metadata(dataset_dir, filtered)
    return record_ids


@dataclass(frozen=True)
class _DeterministicSplitResult:
    seed: int
    train: list[str]
    validation: list[str]
    test: list[str]

    def __init__(self, seed: int, record_ids: Sequence[str]) -> None:
        object.__setattr__(self, "seed", seed)
        sorted_ids = sorted(set(record_ids))
        train: list[str] = []
        validation: list[str] = []
        test: list[str] = []
        for record_id in sorted_ids:
            digest = hashlib.sha256(f"{seed}:{record_id}".encode()).hexdigest()
            bucket = int(digest[:8], 16) % 100
            if bucket < 70:
                train.append(record_id)
            elif bucket < 85:
                validation.append(record_id)
            else:
                test.append(record_id)
        object.__setattr__(self, "train", train)
        object.__setattr__(self, "validation", validation)
        object.__setattr__(self, "test", test)
