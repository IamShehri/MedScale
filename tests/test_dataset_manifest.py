"""Deterministic dataset manifest reproduction.

The same client-supplied inputs must produce the same manifest bytes for the
same created_at, git_sha, software_version, seed, and record set.
"""

from __future__ import annotations

import hashlib
import json

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
