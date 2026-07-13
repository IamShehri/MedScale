"""Initialize a new benchmark scaffold.

Stability: **public**. Creates a deterministic benchmark skeleton under the
workspace root's ``benchmarks/`` directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import medscale._layout as _layout
from medscale.bench.spec import BenchmarkSpec, TaskType
from medscale.bench.store import write_benchmark
from medscale.bench.tasks import GoldEvidenceSet, TaskItem
from medscale.cli import _common


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale bench init")
    parser.add_argument("benchmark_id", help="kebab-case identifier")
    parser.add_argument("description", nargs="?", default="", help="scientific objective")
    parser.add_argument("--root", type=Path, default=_layout.DEFAULT_ROOT)
    parser.add_argument("--version", default="1.0")
    parser.add_argument(
        "--snapshot-id",
        default="0" * 64,
        help="64-hex research snapshot identity",
    )
    args = parser.parse_args(argv)
    guard = _common.require_root(args.root)
    if guard is not None:
        return guard
    target = _layout.benchmarks_dir(args.root) / args.benchmark_id
    if target.exists():
        return _common.fail(
            f"benchmark {args.benchmark_id!r} already exists",
            hint="remove it first",
        )

    description = args.description or f"{args.benchmark_id} synthetic benchmark"
    spec = BenchmarkSpec(
        benchmark_id=args.benchmark_id,
        version=args.version,
        description=description,
        scientific_objective=description,
        snapshot_id=args.snapshot_id,
        task_types=(TaskType.EVIDENCE_GROUNDING, TaskType.EVIDENCE_SUMMARIZATION),
    )
    item = TaskItem(
        task_id="task-001-benchmark-initialization",
        task_type=TaskType.EVIDENCE_GROUNDING,
        input_text="Initialization task placeholder.",
        input_evidence_ids=(),
        gold=GoldEvidenceSet(
            supporting_evidence_ids=(),
            contradicting_evidence_ids=(),
            annotator="synthetic",
            decided_at="2026-07-13T00:00:00+00:00",
        ),
    )
    write_benchmark(args.root, spec, (item,))
    print(f"initialized: {target}")
    return 0
