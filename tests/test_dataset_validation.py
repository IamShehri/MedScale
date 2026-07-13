"""Dataset validation checksum and metadata failure modes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from medscale.dataset.validate import validate_dataset


def _write_dataset_dir(tmp_path: Path) -> Path:
    dataset_dir = tmp_path / "medscale-dataset-v1"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "manifest.json").write_text(
        json.dumps(
            {
                "dataset_id": "medscale-dataset-v1",
                "version": "1.0",
                "created_at": "2026-07-13T00:00:00+00:00",
                "source_snapshot": "snapshot-1",
                "git_sha": "abc123",
                "record_count": 2,
                "metadata": {},
            }
        ),
        encoding="utf-8",
    )
    (dataset_dir / "schema.json").write_text(
        json.dumps({"version": "1"}), encoding="utf-8"
    )
    splits = dataset_dir / "splits"
    splits.mkdir()
    (splits / "train.json").write_text("[]", encoding="utf-8")
    (splits / "validation.json").write_text("[]", encoding="utf-8")
    (splits / "test.json").write_text("[]", encoding="utf-8")
    checksums = dataset_dir / "checksums"
    checksums.mkdir()
    checksums.joinpath("manifest.json.sha256").write_text(
        hashlib.sha256((dataset_dir / "manifest.json").read_bytes()).hexdigest() + "\n",
        encoding="utf-8",
    )
    return dataset_dir


def test_modified_artifact_fails_checksum_validation(tmp_path: Path) -> None:
    dataset_dir = _write_dataset_dir(tmp_path)
    (dataset_dir / "manifest.json").write_text(
        (dataset_dir / "manifest.json").read_text(encoding="utf-8") + "\n#",
        encoding="utf-8",
    )
    report = validate_dataset(dataset_dir)
    assert report.passed is False
    assert any("mismatch" in str(issue) for issue in report.issues)


def test_missing_required_metadata_fails_validation(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "broken"
    dataset_dir.mkdir()
    (dataset_dir / "manifest.json").write_text("{}", encoding="utf-8")
    report = validate_dataset(dataset_dir)
    assert report.passed is False
    assert any("schema" in str(issue) or "manifest" in str(issue) for issue in report.issues)


def test_valid_dataset_passes(tmp_path: Path) -> None:
    dataset_dir = _write_dataset_dir(tmp_path)
    checksums = dataset_dir / "checksums"
    for name in ["schema", "train", "validation", "test"]:
        if name == "schema":
            path = dataset_dir / "schema.json"
        else:
            path = dataset_dir / "splits" / f"{name}.json"
        checksums.joinpath(f"{name}.sha256").write_text(
            hashlib.sha256(path.read_bytes()).hexdigest() + "\n",
            encoding="utf-8",
        )
    report = validate_dataset(dataset_dir)
    assert report.passed is True
