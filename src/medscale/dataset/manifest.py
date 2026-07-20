"""Deterministic dataset manifest generation.

Stability: **public-frozen by ADR-0030**. The manifest fields and hashing rules
are part of the dataset contract; changing them requires a new dataset version
and a new ADR.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from medscale.reproducibility import canonical_json, content_hash

__all__ = [
    "DatasetManifest",
    "compute_dataset_checksums",
    "compute_dataset_fingerprint",
    "compute_dataset_manifest",
    "write_checksums",
    "write_manifest",
]


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    version: str
    created_at: str
    git_sha: str
    record_count: int
    license_summary: list[dict[str, object]]
    schema_version: str = "1"
    split_strategy: str = "deterministic_hash_split"
    hash_algorithm: str = "sha256"
    seed: int = 42
    dataset_fingerprint: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "dataset_id": self.dataset_id,
            "version": self.version,
            "created_at": self.created_at,
            "git_sha": self.git_sha,
            "dataset_fingerprint": self.dataset_fingerprint,
            "record_count": self.record_count,
            "license_summary": self.license_summary,
            "schema_version": self.schema_version,
            "split_strategy": self.split_strategy,
            "hash_algorithm": self.hash_algorithm,
            "seed": self.seed,
        }


def compute_dataset_manifest(
    *,
    dataset_id: str,
    version: str,
    created_at: str,
    git_sha: str,
    records: Sequence[Any],
    license_summary: list[dict[str, object]],
    schema_version: str = "1",
    split_strategy: str = "deterministic_hash_split",
    hash_algorithm: str = "sha256",
    seed: int = 42,
    software_version: str = "",
) -> DatasetManifest:
    record_count = len(list(records))
    return DatasetManifest(
        dataset_id=dataset_id,
        version=version,
        created_at=created_at,
        git_sha=git_sha,
        record_count=record_count,
        license_summary=license_summary,
        schema_version=schema_version,
        split_strategy=split_strategy,
        hash_algorithm=hash_algorithm,
        seed=seed,
    )


def _serialize_manifest(manifest: DatasetManifest) -> str:
    return json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n"


def write_manifest(manifest: DatasetManifest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # LF is pinned: checksum files hash these exact bytes, so Windows CRLF
    # translation would make dataset checksums platform-dependent (ADR-0030).
    path.write_text(_serialize_manifest(manifest), encoding="utf-8", newline="\n")


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_dataset_fingerprint(dataset_dir: Path) -> str:
    """Compute dataset fingerprint from canonical artifact contents."""
    dataset_dir = dataset_dir.resolve()
    components: dict[str, str] = {}

    manifest_path = dataset_dir / "manifest.json"
    if manifest_path.exists():
        components["manifest"] = canonical_json(_load_json(manifest_path))

    schema_path = dataset_dir / "schema.json"
    if schema_path.exists():
        components["schema"] = canonical_json(_load_json(schema_path))

    for split_name in ("train", "validation", "test"):
        split_path = dataset_dir / "splits" / f"{split_name}.json"
        if split_path.exists():
            components[split_name] = canonical_json(_load_json(split_path))

    license_path = dataset_dir / "metadata" / "license.json"
    if license_path.exists():
        components["license"] = canonical_json(_load_json(license_path))

    statistics_path = dataset_dir / "metadata" / "statistics.json"
    if statistics_path.exists():
        components["statistics"] = canonical_json(_load_json(statistics_path))

    return content_hash(components)


def compute_dataset_checksums(dataset_dir: Path) -> dict[str, str]:
    """Compute deterministic sibling-file checksums for dataset artifacts."""
    dataset_dir = dataset_dir.resolve()
    artifacts: list[tuple[str, Path]] = []

    for name in ("manifest.json", "schema.json"):
        path = dataset_dir / name
        if path.exists():
            artifacts.append((name, path))

    for split_name in ("train", "validation", "test"):
        path = dataset_dir / "splits" / f"{split_name}.json"
        if path.exists():
            artifacts.append((f"{split_name}.json", path))

    for name in ("license.json", "statistics.json"):
        path = dataset_dir / "metadata" / name
        if path.exists():
            artifacts.append((name, path))

    readme_path = dataset_dir / "README.md"
    if readme_path.exists():
        artifacts.append(("README.md", readme_path))

    checksums: dict[str, str] = {}
    for relative_name, path in sorted(artifacts, key=lambda item: item[0]):
        checksums[relative_name] = hashlib.sha256(path.read_bytes()).hexdigest()

    return checksums


def write_checksums(checksums: dict[str, str], checksums_dir: Path) -> None:
    """Write sibling `.sha256` checksum files."""
    checksums_dir.mkdir(parents=True, exist_ok=True)
    for relative_name, digest in sorted(checksums.items()):
        target = checksums_dir / f"{Path(relative_name).name}.sha256"
        target.write_text(f"{digest}\n", encoding="utf-8", newline="\n")
