"""Benchmark CLI: `medscale bench {list|validate|run}` — thin over the Core Library.

Stability: transport adapter. ``run`` accepts only the deterministic reference systems
today (``gold-oracle``, ``empty``); model systems plug in through the
``EvidenceSystem`` API when their phase arrives. Exit codes are CI-gateable.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Final

import medscale._layout as _layout
from medscale.bench.baselines import EmptySystem, GoldOracle
from medscale.bench.run import EvidenceSystem
from medscale.cli import _common
from medscale.cli.bench_init import main as bench_init_main
from medscale.cli.bench_replay import main as bench_replay_main
from medscale.workspace import Workspace

_DEFAULT_ROOT: Final = _layout.DEFAULT_ROOT
_REFERENCE_SYSTEMS: Final[dict[str, type]] = {
    "gold-oracle": GoldOracle,
    "empty": EmptySystem,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="medscale bench",
        description="List, validate, and run snapshot-bound evidence benchmarks. "
        "`validate` proves the benchmark's knowledge state still matches the tree "
        "(exit 1 if not); `run` executes a reference system and writes a "
        "reproducible run artifact.",
        epilog="example:\n  medscale bench run my-benchmark --system gold-oracle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", choices=["list", "validate", "run", "init", "replay"])
    parser.add_argument("benchmark_id", nargs="?", default=None)
    parser.add_argument(
        "artifact_path", nargs="?", default=None, help="path to a run artifact for replay"
    )
    parser.add_argument(
        "--root", type=Path, default=_DEFAULT_ROOT, help="workspace root (default: data/litdb)"
    )
    parser.add_argument(
        "--system",
        choices=sorted(_REFERENCE_SYSTEMS),
        default="gold-oracle",
        help="reference system to run (models plug in via the EvidenceSystem API later)",
    )
    args = parser.parse_args(argv)
    guard = _common.require_root(args.root)
    if guard is not None:
        return guard
    workspace = Workspace.open(args.root)

    if args.command == "init":
        return bench_init_main(
            [
                args.benchmark_id,
                args.description or "",
                "--root",
                str(args.root),
                "--version",
                args.version,
                "--snapshot-id",
                "0" * 64,
            ]
        )

    if args.command == "replay":
        if args.artifact_path is None:
            return _common.fail("artifact_path required for replay")
        return bench_replay_main([str(args.artifact_path)])

    if args.command == "list":
        names = workspace.benchmarks()
        if not names:
            print("no benchmarks defined")
            return 0
        for name in names:
            benchmark = workspace.benchmark(name)
            print(
                f"{name}  v{benchmark.spec.version}  items={len(benchmark.items)}  "
                f"snapshot={benchmark.spec.snapshot_id[:12]}"
            )
        return 0

    if args.benchmark_id is None:
        return _common.fail(
            "benchmark_id required for this command",
            hint="see `medscale bench list` for what exists",
        )

    available = workspace.benchmarks()
    if args.benchmark_id not in available:
        return _common.fail(
            f"unknown benchmark {args.benchmark_id!r}",
            hint=f"available: {', '.join(available) or '(none defined yet)'}",
        )

    benchmark = workspace.benchmark(args.benchmark_id)

    if args.command == "validate":
        issues = benchmark.validate()
        if issues:
            print(f"{args.benchmark_id}: INVALID ({len(issues)} issue(s))")
            for issue in issues:
                print(f"  ! {issue}")
            return 1
        print(f"{args.benchmark_id}: VALID (snapshot verified, all evidence resolves)")
        return 0

    system: EvidenceSystem = _REFERENCE_SYSTEMS[args.system]()
    artifact = benchmark.run(system)
    print(
        f"run complete: {args.benchmark_id} v{artifact.benchmark_version} "
        f"system={artifact.system.model_id}"
    )
    for name, value in artifact.aggregates.items():
        print(f"  {name}: {value}")
    run_path = (
        _layout.benchmarks_dir(args.root)
        / args.benchmark_id
        / "runs"
        / f"{artifact.results_id[:16]}.json"
    )
    print(f"artifact: {run_path}")
    print(f"results_id: {artifact.results_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
