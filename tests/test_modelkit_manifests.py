"""Experiment manifests: round-trip fidelity, byte-stability, runner detection."""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.modelkit import (
    DatasetSnapshot,
    ExperimentManifest,
    ModelRef,
    RunnerClass,
    RunnerEnv,
    detect_runner,
    read_manifest,
    write_manifest,
)
from medscale.reproducibility import canonical_json

_TS = "2026-07-10T00:00:00+00:00"
_RUNNER = RunnerEnv(runner=RunnerClass.COLAB, python="3.11.15", os_name="linux", gpu="T4")


def _manifest(**overrides: object) -> ExperimentManifest:
    base: dict[str, object] = {
        "experiment_id": "t4-rq1-qwen3-8b-2x2",
        "rq_refs": ("RQ1",),
        "configuration": canonical_json({"grammar": True, "shots": 0}),
        "datasets": (DatasetSnapshot("medscale-bench-data", "v0.1", "b" * 64),),
        "model": ModelRef(model_id="qwen3-8b", revision="abc123", backend="transformers"),
        "model_tier": 1,
        "code_sha": "1c00b73",
        "seeds": (0, 1, 2),
        "runner": _RUNNER,
        "started_at": _TS,
        "results_paths": ("experiments/t4-rq1-2x2/results/qwen3-8b.json",),
        "reproduction": "uv run medscale-experiment t4-rq1-qwen3-8b-2x2",
    }
    base.update(overrides)
    return ExperimentManifest(**base)  # type: ignore[arg-type]


def test_write_read_roundtrip(tmp_path: Path) -> None:
    manifest = _manifest()
    path = write_manifest(tmp_path, manifest)
    loaded = read_manifest(path)
    assert loaded == manifest
    assert loaded.manifest_id == manifest.manifest_id


def test_manifest_bytes_are_stable_and_lf(tmp_path: Path) -> None:
    path = write_manifest(tmp_path, _manifest())
    first = path.read_bytes()
    write_manifest(tmp_path, _manifest())
    assert path.read_bytes() == first
    assert b"\r\n" not in first


def test_no_rq_no_run() -> None:
    with pytest.raises(ValueError, match="no research question"):
        _manifest(rq_refs=())
    with pytest.raises(ValueError, match="invalid rq_ref"):
        _manifest(rq_refs=("vibes",))


def test_dirty_tree_shapes_rejected() -> None:
    with pytest.raises(ValueError, match="git SHA"):
        _manifest(code_sha="dirty!")


def test_configuration_must_be_json() -> None:
    with pytest.raises(ValueError, match="valid"):
        _manifest(configuration="not json")


def test_seeds_required() -> None:
    with pytest.raises(ValueError, match="seeds"):
        _manifest(seeds=())
    with pytest.raises(ValueError, match="seeds"):
        _manifest(seeds=(0, -1))


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({"COLAB_RELEASE_TAG": "release"}, RunnerClass.COLAB),
        ({"KAGGLE_KERNEL_RUN_TYPE": "Interactive"}, RunnerClass.KAGGLE),
        ({"RUNPOD_POD_ID": "pod-1"}, RunnerClass.RUNPOD),
        ({"SLURM_JOB_ID": "42"}, RunnerClass.CLUSTER),
        ({"KUBERNETES_SERVICE_HOST": "10.0.0.1"}, RunnerClass.CLUSTER),
        ({"PATH": "/usr/bin"}, RunnerClass.LOCAL),
    ],
)
def test_runner_detection(env: dict[str, str], expected: RunnerClass) -> None:
    assert detect_runner(env) is expected


def test_runner_env_validation() -> None:
    with pytest.raises(ValueError, match="peak_vram_gb"):
        RunnerEnv(runner=RunnerClass.LOCAL, python="3.11", os_name="win", peak_vram_gb=0)
