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
from medscale.workspace import Workspace

_DEFAULT_ROOT: Final = _layout.DEFAULT_ROOT
_REFERENCE_SYSTEMS: Final[dict[str, type]] = {
    "gold-oracle": GoldOracle,
    "empty": EmptySystem,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale bench", description=__doc__)
    parser.add_argument("command", choices=["list", "validate", "run"])
    parser.add_argument("benchmark_id", nargs="?", default=None)
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    parser.add_argument(
        "--system",
        choices=sorted(_REFERENCE_SYSTEMS),
        default="gold-oracle",
        help="reference system to run (models plug in via the EvidenceSystem API later)",
    )
    args = parser.parse_args(argv)
    workspace = Workspace.open(args.root)

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
        print("benchmark_id required for this command")
        return 2

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
