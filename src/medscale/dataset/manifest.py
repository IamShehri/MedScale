"""Deterministic dataset manifest generation.

Stability: **public-frozen by ADR-0030**. The manifest fields and hashing rules
are part of the dataset contract; changing them requires a new dataset version.
"""

from __future__ import annotations

import hashlib
import json
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
    schema_version: str
    split_strategy: str
    split_seed: int
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
            "split_seed": self.split_seed,
            "hash_algorithm": self.hash_algorithm,
        }


def _sha256_of(value: object) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_dataset_manifest(
    *,
    dataset_id: str,
    version: str,
    source_snapshot: str,
    git_sha: str,
    records: list[object],
    license_summary: list[dict[str, object]],
    schema_version: str = "1",
    split_strategy: str = "deterministic_hash_split",
    split_seed: int = 42,
    created_at: str,
) -> DatasetManifest:
    """Build a deterministic dataset manifest from the current corpus state.

    ``created_at`` is intentionally explicit so manifests remain byte-for-byte
    reproducible across machines and runs.
    """
    return DatasetManifest(
        dataset_id=dataset_id,
        version=version,
        created_at=created_at,
        source_snapshot=source_snapshot,
        git_sha=git_sha,
        record_count=len(records),
        license_summary=license_summary,
        schema_version=schema_version,
        split_strategy=split_strategy,
        split_seed=split_seed,
    )


def write_manifest(manifest: DatasetManifest, path: Path) -> Path:
    """Write manifest.json atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = manifest.to_dict()
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
