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
                "dataset_snapshot": {
                    "git_sha": "abc123",
                    "software_version": "0.1.0",
                    "created_at": "2026-07-13T00:00:00+00:00",
                    "fingerprint": "",
                },
                "git_sha": "abc123",
                "record_count": 2,
                "license_summary": [{"spdx": "MIT", "count": 2}],
            }
        ),
        encoding="utf-8",
    )
    (dataset_dir / "schema.json").write_text(json.dumps({"version": "1"}), encoding="utf-8")
    splits = dataset_dir / "splits"
    splits.mkdir()
    (splits / "train.json").write_text("[]", encoding="utf-8")
    (splits / "validation.json").write_text("[]", encoding="utf-8")
    (splits / "test.json").write_text("[]", encoding="utf-8")
    metadata = dataset_dir / "metadata"
    metadata.mkdir(parents=True, exist_ok=True)
    (metadata / "license.json").write_text(
        json.dumps(
            {
                "spdx_id": "MIT",
                "source_scope": ["synthetic"],
                "redistribution_allowed": True,
                "attribution_required": False,
                "commercial_allowed": True,
            }
        ),
        encoding="utf-8",
    )
    checksums = dataset_dir / "checksums"
    checksums.mkdir(parents=True, exist_ok=True)
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
            hashlib.sha256(path.read_bytes()).hexdigest() + "\n", encoding="utf-8"
        )
    report = validate_dataset(dataset_dir)
    assert report.passed is True


# ---------------------------------------------------------------------------
# Regressions from the stabilization audit (F-5, F-7, F-4):
# generated splits must be FILES, checksum names for metadata/README must
# resolve, and generated artifacts must be LF-only.
# ---------------------------------------------------------------------------


def _write_corpus(tmp_path: Path) -> Path:
    corpus = tmp_path / "records.jsonl"
    rows = [
        {"record_id": "r-1", "format": 1, "license_spdx": "MIT"},
        {"record_id": "r-2", "format": 1, "license_spdx": "MIT"},
    ]
    corpus.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8", newline="\n"
    )
    return corpus


def test_generated_splits_are_files_and_validation_does_not_crash(tmp_path: Path) -> None:
    from medscale.dataset.generate import write_dataset

    dataset_dir = tmp_path / "gen-dataset"
    write_dataset(dataset_dir, _write_corpus(tmp_path))
    for name in ("train", "validation", "test"):
        split_path = dataset_dir / "splits" / f"{name}.json"
        assert split_path.is_file(), f"splits/{name}.json must be a file, not a directory"
        assert isinstance(json.loads(split_path.read_text(encoding="utf-8")), list)
    report = validate_dataset(dataset_dir)  # must not raise on the generated layout
    assert isinstance(report.passed, bool)


def test_generated_artifacts_are_lf_only(tmp_path: Path) -> None:
    from medscale.dataset.generate import write_dataset

    dataset_dir = tmp_path / "gen-dataset"
    write_dataset(dataset_dir, _write_corpus(tmp_path))
    for path in sorted(dataset_dir.rglob("*.json")):
        assert b"\r" not in path.read_bytes(), f"{path.name} must be LF-only on every platform"


def test_checksummed_license_metadata_resolves(tmp_path: Path) -> None:
    dataset_dir = _write_dataset_dir(tmp_path)
    license_path = dataset_dir / "metadata" / "license.json"
    (dataset_dir / "checksums" / "license.json.sha256").write_text(
        hashlib.sha256(license_path.read_bytes()).hexdigest() + "\n", encoding="utf-8"
    )
    report = validate_dataset(dataset_dir)
    assert "license.json: match" in report.checksum_checks
    assert not any("missing artifact for checksum" in issue.message for issue in report.issues)


def test_checksummed_readme_resolves(tmp_path: Path) -> None:
    dataset_dir = _write_dataset_dir(tmp_path)
    readme = dataset_dir / "README.md"
    readme.write_text("# demo dataset\n", encoding="utf-8", newline="\n")
    (dataset_dir / "checksums" / "README.md.sha256").write_text(
        hashlib.sha256(readme.read_bytes()).hexdigest() + "\n", encoding="utf-8"
    )
    report = validate_dataset(dataset_dir)
    assert "README.md: match" in report.checksum_checks
    assert not any("missing artifact for checksum" in issue.message for issue in report.issues)
