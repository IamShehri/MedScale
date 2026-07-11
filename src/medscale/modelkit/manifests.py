"""Deterministic experiment manifests + runner portability.

Implements sections 1-2 of ``docs/research/experiment_framework.md`` as code: every experiment
emits one canonical-JSON, LF-terminated manifest, and the runner (Colab, Kaggle,
RunPod, Lambda, local, cluster) is a *recorded environment detail*, never a result
variable. An experiment with no research question does not construct.
"""

from __future__ import annotations

import enum
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from medscale.modelkit.interfaces import ModelRef
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json, content_hash

__all__ = [
    "DatasetSnapshot",
    "ExperimentManifest",
    "RunnerClass",
    "RunnerEnv",
    "detect_runner",
    "read_manifest",
    "write_manifest",
]

_EXPERIMENT_ID: Final = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_GIT_SHA: Final = re.compile(r"^[0-9a-f]{7,40}$")
_RQ_REF: Final = re.compile(r"^(RQ[1-9][0-9]?|background)$")


class RunnerClass(enum.Enum):
    COLAB = "colab"
    KAGGLE = "kaggle"
    RUNPOD = "runpod"
    LAMBDA = "lambda"
    LOCAL = "local"
    CLUSTER = "cluster"
    OTHER = "other"


def detect_runner(env: Mapping[str, str]) -> RunnerClass:
    """Classify the execution environment from its environment variables.

    Pure and injectable (pass ``os.environ`` at the call site). Providers without a
    reliable marker (e.g. Lambda Labs bare VMs) classify as LOCAL and may be
    overridden explicitly when constructing :class:`RunnerEnv`.
    """
    if "COLAB_RELEASE_TAG" in env or "COLAB_GPU" in env:
        return RunnerClass.COLAB
    if "KAGGLE_KERNEL_RUN_TYPE" in env or "KAGGLE_URL_BASE" in env:
        return RunnerClass.KAGGLE
    if "RUNPOD_POD_ID" in env:
        return RunnerClass.RUNPOD
    if "SLURM_JOB_ID" in env or "KUBERNETES_SERVICE_HOST" in env:
        return RunnerClass.CLUSTER
    return RunnerClass.LOCAL


@dataclass(frozen=True)
class RunnerEnv:
    """The recorded execution environment of one run."""

    runner: RunnerClass
    python: str
    os_name: str
    gpu: str | None = None
    peak_vram_gb: float | None = None

    def __post_init__(self) -> None:
        if not self.python.strip() or not self.os_name.strip():
            raise ValueError("python and os_name must be non-empty")
        if self.peak_vram_gb is not None and self.peak_vram_gb <= 0:
            raise ValueError("peak_vram_gb, when given, must be positive")

    def to_dict(self) -> dict[str, Any]:
        return {
            "runner": self.runner.value,
            "python": self.python,
            "os_name": self.os_name,
            "gpu": self.gpu,
            "peak_vram_gb": self.peak_vram_gb,
        }


@dataclass(frozen=True)
class DatasetSnapshot:
    name: str
    version: str
    content_sha256: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.version.strip():
            raise ValueError("dataset name and version must be non-empty")
        if len(self.content_sha256) != 64:
            raise ValueError("content_sha256 must be a 64-hex content hash")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "content_sha256": self.content_sha256,
        }


@dataclass(frozen=True)
class ExperimentManifest:
    """One experiment run, fully determined (experiment_framework §1)."""

    experiment_id: str
    rq_refs: tuple[str, ...]
    configuration: str  # canonical JSON of the full run configuration
    datasets: tuple[DatasetSnapshot, ...]
    model: ModelRef
    model_tier: int
    code_sha: str
    seeds: tuple[int, ...]
    runner: RunnerEnv
    started_at: str
    results_paths: tuple[str, ...]
    reproduction: str

    def __post_init__(self) -> None:
        if not _EXPERIMENT_ID.match(self.experiment_id):
            raise ValueError(
                f"experiment_id must be kebab-case [a-z0-9-], got {self.experiment_id!r}"
            )
        if not self.rq_refs:
            raise ValueError("an experiment with no research question does not run")
        for ref in self.rq_refs:
            if not _RQ_REF.match(ref):
                raise ValueError(f"invalid rq_ref {ref!r} (expected RQn or 'background')")
        try:
            json.loads(self.configuration)
        except json.JSONDecodeError as exc:
            raise ValueError("configuration must be valid (canonical) JSON") from exc
        if not self.datasets:
            raise ValueError("at least one dataset snapshot is required")
        if self.model_tier not in (1, 2):
            raise ValueError("model_tier must be 1 or 2")
        if not _GIT_SHA.match(self.code_sha):
            raise ValueError("code_sha must be a 7-40 hex git SHA (clean tree)")
        if not self.seeds or any(seed < 0 for seed in self.seeds):
            raise ValueError("seeds must be non-empty and non-negative")
        validate_timestamp(self.started_at, "started_at")
        if not self.reproduction.strip():
            raise ValueError("reproduction command must be non-empty")

    @property
    def configuration_sha256(self) -> str:
        return content_hash(json.loads(self.configuration))

    @property
    def manifest_id(self) -> str:
        return content_hash(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "experiment_id": self.experiment_id,
            "rq_refs": list(self.rq_refs),
            "configuration": self.configuration,
            "configuration_sha256": self.configuration_sha256,
            "datasets": [snapshot.to_dict() for snapshot in self.datasets],
            "model": {
                "model_id": self.model.model_id,
                "revision": self.model.revision,
                "quantization": self.model.quantization,
                "backend": self.model.backend,
            },
            "model_tier": self.model_tier,
            "code_sha": self.code_sha,
            "seeds": list(self.seeds),
            "runner": self.runner.to_dict(),
            "started_at": self.started_at,
            "results_paths": list(self.results_paths),
            "reproduction": self.reproduction,
        }


def write_manifest(directory: Path, manifest: ExperimentManifest) -> Path:
    """Write the manifest as canonical, LF-terminated JSON (byte-stable everywhere)."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"manifest-{manifest.experiment_id}.json"
    target.write_text(canonical_json(manifest.to_dict()) + "\n", encoding="utf-8", newline="\n")
    return target


def read_manifest(path: Path) -> ExperimentManifest:
    """Rebuild a manifest from disk, re-running every validation."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return ExperimentManifest(
        experiment_id=data["experiment_id"],
        rq_refs=tuple(data["rq_refs"]),
        configuration=data["configuration"],
        datasets=tuple(
            DatasetSnapshot(d["name"], d["version"], d["content_sha256"]) for d in data["datasets"]
        ),
        model=ModelRef(
            model_id=data["model"]["model_id"],
            revision=data["model"]["revision"],
            quantization=data["model"]["quantization"],
            backend=data["model"]["backend"],
        ),
        model_tier=data["model_tier"],
        code_sha=data["code_sha"],
        seeds=tuple(data["seeds"]),
        runner=RunnerEnv(
            runner=RunnerClass(data["runner"]["runner"]),
            python=data["runner"]["python"],
            os_name=data["runner"]["os_name"],
            gpu=data["runner"]["gpu"],
            peak_vram_gb=data["runner"]["peak_vram_gb"],
        ),
        started_at=data["started_at"],
        results_paths=tuple(data["results_paths"]),
        reproduction=data["reproduction"],
    )
