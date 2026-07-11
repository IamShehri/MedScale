"""Benchmark persistence: spec + items, canonical and content-addressed on disk.

Layout under the litdb root:

    benchmarks/<benchmark_id>/spec.json      (canonical JSON, format-marked)
    benchmarks/<benchmark_id>/items.jsonl    (one item per line, task_id-sorted)
    benchmarks/<benchmark_id>/runs/<id>.json (run artifacts, written by the runner)
"""

from __future__ import annotations

import json
from pathlib import Path

import medscale._layout as _layout
from medscale.bench.spec import BenchmarkSpec
from medscale.bench.tasks import TaskItem
from medscale.reproducibility import canonical_json

__all__ = ["benchmark_dir", "list_benchmarks", "load_benchmark", "write_benchmark"]


def benchmark_dir(root: Path, benchmark_id: str) -> Path:
    return _layout.benchmarks_dir(root) / benchmark_id


def write_benchmark(root: Path, spec: BenchmarkSpec, items: tuple[TaskItem, ...]) -> Path:
    """Persist a benchmark; duplicate task ids are rejected, items sorted for stability."""
    task_ids = [item.task_id for item in items]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("duplicate task_id in benchmark items")
    target = benchmark_dir(root, spec.benchmark_id)
    target.mkdir(parents=True, exist_ok=True)
    (target / "spec.json").write_text(
        canonical_json(spec.to_dict()) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [canonical_json(item.to_dict()) for item in sorted(items, key=lambda i: i.task_id)]
    (target / "items.jsonl").write_text(
        "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8", newline="\n"
    )
    return target


def load_benchmark(root: Path, benchmark_id: str) -> tuple[BenchmarkSpec, tuple[TaskItem, ...]]:
    """Load and re-validate a benchmark (every constructor check re-runs)."""
    target = benchmark_dir(root, benchmark_id)
    spec = BenchmarkSpec.from_dict(json.loads((target / "spec.json").read_text(encoding="utf-8")))
    items = tuple(
        TaskItem.from_dict(json.loads(line))
        for line in (target / "items.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    return spec, items


def list_benchmarks(root: Path) -> tuple[str, ...]:
    base = _layout.benchmarks_dir(root)
    if not base.exists():
        return ()
    return tuple(sorted(entry.name for entry in base.iterdir() if (entry / "spec.json").exists()))
