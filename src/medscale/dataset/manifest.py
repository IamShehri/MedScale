"""Deterministic dataset manifest generation.

Stability: **public-frozen by ADR-0030**. The manifest fields and hashing rules
are part of the dataset contract; changing them requires a new dataset version
and a new ADR.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

__all__ = ["DatasetManifest", "compute_dataset_manifest", "write_manifest"]


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    version: str
    created_at: str
    source_snapshot: str
    git_sha: str
    record_count: int
    license_summary: list[dict[str, object]]
    schema_version: str = "1"
    split_strategy: str = "deterministic_hash_split"
    hash_algorithm: str = "sha256"

    def to_dict(self) -> dict[str, object]:
        return {
            "dataset_id": self.dataset_id,
            "version": self.version,
            "created_at": self.created_at,
            "source_snapshot": self.source_snapshot,
            "git_sha": self.git_sha,
            "record_count": self.record_count,
            "license_summary": self.license_summary,
            "schema_version": self.schema_version,
            "split_strategy": self.split_strategy,
            "hash_algorithm": self.hash_algorithm,
        }


def compute_dataset_manifest(
    *,
    dataset_id: str,
    version: str,
    created_at: str,
    source_snapshot: str,
    git_sha: str,
    records: Sequence[object],
    license_summary: list[dict[str, object]],
    schema_version: str = "1",
    split_strategy: str = "deterministic_hash_split",
) -> DatasetManifest:
    record_count = len(list(records))
    return DatasetManifest(
        dataset_id=dataset_id,
        version=version,
        created_at=created_at,
        source_snapshot=source_snapshot,
        git_sha=git_sha,
        record_count=record_count,
        license_summary=license_summary,
        schema_version=schema_version,
        split_strategy=split_strategy,
    )


def _serialize_manifest(manifest: DatasetManifest) -> str:
    return json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n"


def write_manifest(manifest: DatasetManifest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_serialize_manifest(manifest), encoding="utf-8")
