"""Deterministic dataset manifest reproduction.

The same client-supplied inputs must produce the same manifest bytes for the
same created_at, git_sha, software_version, seed, and record set.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from medscale.dataset.manifest import DatasetManifest, compute_dataset_manifest


def test_same_inputs_produce_identical_manifest_bytes() -> None:
    records = [object(), object(), object()]
    manifest = compute_dataset_manifest(
        dataset_id="medscale-dataset-v1",
        version="1.0",
        created_at="2026-07-13T00:00:00+00:00",
        git_sha="abc123",
        records=records,
        license_summary=[{"spdx": "MIT", "count": 2}],
        software_version="0.1.0",
    )
    expected = json.dumps(manifest.to_dict(), sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(expected.encode("utf-8")).hexdigest() == manifest_sha(manifest)


def test_recomputed_manifest_is_stable() -> None:
    records = [object(), object(), object(), object()]
    first = compute_dataset_manifest(
        dataset_id="medscale-dataset-v1",
        version="1.0",
        created_at="2026-07-13T00:00:00+00:00",
        git_sha="def456",
        records=records,
        license_summary=[],
        software_version="0.1.0",
    )
    second = compute_dataset_manifest(
        dataset_id="medscale-dataset-v1",
        version="1.0",
        created_at="2026-07-13T00:00:00+00:00",
        git_sha="def456",
        records=records,
        license_summary=[],
        software_version="0.1.0",
    )
    assert first.to_dict() == second.to_dict()
    assert manifest_sha(first) == manifest_sha(second)


def manifest_sha(manifest: DatasetManifest) -> str:
    payload = json.dumps(manifest.to_dict(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Byte-level determinism (regression: writers omitted newline="\n", so Windows
# text-mode translation produced CRLF bytes and platform-dependent checksums).
# ---------------------------------------------------------------------------


def test_written_manifest_bytes_are_lf_only(tmp_path: Path) -> None:
    from medscale.dataset.manifest import write_manifest

    manifest = DatasetManifest(
        dataset_id="medscale-dataset-v1",
        version="1.0",
        created_at="2026-07-13T00:00:00+00:00",
        git_sha="def456",
        record_count=0,
        license_summary=[],
    )
    path = tmp_path / "manifest.json"
    write_manifest(manifest, path)
    raw = path.read_bytes()
    assert b"\r" not in raw, "manifest bytes must be LF-only on every platform"
    assert raw.endswith(b"\n")


def test_written_checksum_files_are_lf_only(tmp_path: Path) -> None:
    from medscale.dataset.manifest import write_checksums

    write_checksums({"manifest.json": "ab" * 32}, tmp_path / "checksums")
    raw = (tmp_path / "checksums" / "manifest.json.sha256").read_bytes()
    assert raw == ("ab" * 32).encode("ascii") + b"\n"
