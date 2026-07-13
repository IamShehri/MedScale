"""Dataset CLI coverage."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from medscale.cli.dataset import main


def test_dataset_init_preview_does_not_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "data" / "datasets"
    root.mkdir(parents=True)
    target = root / "medscale-dataset-v1"
    assert main(["init", "medscale-dataset-v1", "--root", str(root)]) == 0
    assert not target.exists(), "init without --write must not create a dataset directory"


def test_dataset_init_writes_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "data" / "datasets"
    root.mkdir(parents=True)
    target = root / "medscale-dataset-v1"
    assert main(["init", "medscale-dataset-v1", "--root", str(root), "--write"]) == 0
    assert target.exists()
    assert (target / "schema.json").exists()
    assert (target / "splits").exists()


def test_dataset_manifest_exits_nonzero_for_missing_dataset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "data" / "datasets"
    root.mkdir(parents=True)
    assert main(["manifest", "missing", "--root", str(root)]) == 2


def test_dataset_validate_exits_nonzero_for_invalid_dataset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dataset_dir = tmp_path / "medscale-dataset-v1"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "manifest.json").write_text("{}", encoding="utf-8")
    exit_code = main(["validate", str(dataset_dir)])
    assert exit_code in {1, 2}


def test_dataset_validate_exits_zero_for_valid_dataset(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "medscale-dataset-v1"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "manifest.json").write_text(
        json.dumps(
            {
                "dataset_id": "medscale-dataset-v1",
                "created_at": "2026-07-13T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )
    (dataset_dir / "schema.json").write_text("{}", encoding="utf-8")
    (dataset_dir / "splits").mkdir()
    for name in ["train", "validation", "test"]:
        (dataset_dir / "splits" / f"{name}.json").write_text("[]", encoding="utf-8")
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
    checksums.mkdir()
    for path in [
        dataset_dir / "manifest.json",
        dataset_dir / "schema.json",
        dataset_dir / "splits" / "train.json",
        dataset_dir / "splits" / "validation.json",
        dataset_dir / "splits" / "test.json",
    ]:
        checksums.joinpath(path.name + ".sha256").write_text(
            hashlib.sha256(path.read_bytes()).hexdigest() + "\n", encoding="utf-8"
        )
    assert main(["validate", str(dataset_dir)]) == 0
