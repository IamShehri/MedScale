"""The benchmark runner: validated substrate in, content-addressed run artifact out.

``EvidenceSystem`` is the model-agnostic plug (ADR-0015 pattern): any future system —
retrieval pipeline, constrained LLM, human team — implements one method and identifies
itself with a :class:`~medscale.modelkit.interfaces.ModelRef`. The runner refuses an
invalid benchmark, scores deterministically, and writes an artifact whose ``results``
are a pure function of (benchmark, system outputs, scorer version) — the 2035
reproduction guarantee.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Protocol

from medscale.bench.scorers import SCORER_VERSION, score_item
from medscale.bench.store import benchmark_dir, load_benchmark
from medscale.bench.tasks import TaskItem, TaskOutput
from medscale.bench.validate import validate_benchmark
from medscale.evidence_store import load_evidence
from medscale.modelkit.interfaces import ModelRef
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json, content_hash
from medscale.research.index import ResearchIndex

__all__ = ["BenchmarkRunArtifact", "EvidenceSystem", "run_benchmark"]

_GIT_SHA: Final = re.compile(r"^[0-9a-f]{7,40}$")


class EvidenceSystem(Protocol):
    """What any evaluated system must implement (structural typing, no inheritance)."""

    @property
    def system(self) -> ModelRef: ...

    def solve(self, item: TaskItem, index: ResearchIndex) -> TaskOutput: ...


@dataclass(frozen=True)
class BenchmarkRunArtifact:
    """One benchmark run, fully determined and reproducible."""

    benchmark_id: str
    benchmark_version: str
    spec_id: str
    snapshot_id: str
    system: ModelRef
    parameters: str  # canonical JSON of system parameters
    started_at: str
    software_version: str
    git_sha: str
    scorer_version: str
    per_item: dict[str, dict[str, float]]
    aggregates: dict[str, float]

    def __post_init__(self) -> None:
        validate_timestamp(self.started_at, "started_at")
        if not _GIT_SHA.match(self.git_sha):
            raise ValueError("git_sha must be 7-40 hex chars")

    @property
    def results_id(self) -> str:
        """Identity of the scientific result (volatile fields excluded by design)."""
        return content_hash(
            {
                "spec_id": self.spec_id,
                "snapshot_id": self.snapshot_id,
                "system": {
                    "model_id": self.system.model_id,
                    "revision": self.system.revision,
                    "quantization": self.system.quantization,
                    "backend": self.system.backend,
                },
                "parameters": self.parameters,
                "scorer_version": self.scorer_version,
                "per_item": self.per_item,
                "aggregates": self.aggregates,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "results_id": self.results_id,
            "benchmark_id": self.benchmark_id,
            "benchmark_version": self.benchmark_version,
            "spec_id": self.spec_id,
            "snapshot_id": self.snapshot_id,
            "system": {
                "model_id": self.system.model_id,
                "revision": self.system.revision,
                "quantization": self.system.quantization,
                "backend": self.system.backend,
            },
            "parameters": self.parameters,
            "started_at": self.started_at,
            "software_version": self.software_version,
            "git_sha": self.git_sha,
            "scorer_version": self.scorer_version,
            "per_item": self.per_item,
            "aggregates": self.aggregates,
        }


def _aggregate(per_item: dict[str, dict[str, float]]) -> dict[str, float]:
    """Unweighted mean per metric across the items that report it (documented rule)."""
    sums: dict[str, list[float]] = {}
    for metrics in per_item.values():
        for name, value in metrics.items():
            sums.setdefault(name, []).append(value)
    return {name: round(sum(values) / len(values), 6) for name, values in sorted(sums.items())}


def run_benchmark(
    root: Path,
    benchmark_id: str,
    system: EvidenceSystem,
    *,
    parameters: dict[str, Any] | None = None,
    started_at: str,
    software_version: str,
    git_sha: str,
) -> tuple[BenchmarkRunArtifact, Path]:
    """Validate, execute, score, persist. Raises on an invalid benchmark — no partial science."""
    spec, items = load_benchmark(root, benchmark_id)
    issues = validate_benchmark(root, spec, items)
    if issues:
        raise ValueError("benchmark is not scientifically runnable:\n  " + "\n  ".join(issues))
    index = ResearchIndex.load(root)
    known_ids = frozenset(
        obj.evidence_id for obj in load_evidence(root / "evidence" / "objects.jsonl")
    )
    per_item: dict[str, dict[str, float]] = {}
    for item in sorted(items, key=lambda i: i.task_id):
        output = system.solve(item, index)
        per_item[item.task_id] = score_item(item, output, known_ids)

    artifact = BenchmarkRunArtifact(
        benchmark_id=spec.benchmark_id,
        benchmark_version=spec.version,
        spec_id=spec.spec_id,
        snapshot_id=spec.snapshot_id,
        system=system.system,
        parameters=canonical_json(parameters or {}),
        started_at=started_at,
        software_version=software_version,
        git_sha=git_sha,
        scorer_version=SCORER_VERSION,
        per_item=per_item,
        aggregates=_aggregate(per_item),
    )
    runs_dir = benchmark_dir(root, benchmark_id) / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    path = runs_dir / f"{artifact.results_id[:16]}.json"
    path.write_text(canonical_json(artifact.to_dict()) + "\n", encoding="utf-8", newline="\n")
    return artifact, path
