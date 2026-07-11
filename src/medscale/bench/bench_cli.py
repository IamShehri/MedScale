"""Benchmark CLI: `medscale bench {list|validate|run}` — no UI, machine-honest output.

``run`` accepts only the deterministic reference systems today (``gold-oracle``,
``empty``); model systems plug in through the ``EvidenceSystem`` API when their phase
arrives. Exit codes are CI-gateable: validate returns non-zero on any issue.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from medscale import __version__
from medscale.bench.baselines import EmptySystem, GoldOracle
from medscale.bench.run import EvidenceSystem, run_benchmark
from medscale.bench.store import list_benchmarks, load_benchmark
from medscale.bench.validate import validate_benchmark

_DEFAULT_ROOT: Final = Path("data/litdb")
_REFERENCE_SYSTEMS: Final[dict[str, type]] = {
    "gold-oracle": GoldOracle,
    "empty": EmptySystem,
}


def _git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0000000"


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

    if args.command == "list":
        names = list_benchmarks(args.root)
        if not names:
            print("no benchmarks defined")
            return 0
        for name in names:
            spec, items = load_benchmark(args.root, name)
            print(f"{name}  v{spec.version}  items={len(items)}  snapshot={spec.snapshot_id[:12]}")
        return 0

    if args.benchmark_id is None:
        print("benchmark_id required for this command")
        return 2

    if args.command == "validate":
        spec, items = load_benchmark(args.root, args.benchmark_id)
        issues = validate_benchmark(args.root, spec, items)
        if issues:
            print(f"{args.benchmark_id}: INVALID ({len(issues)} issue(s))")
            for issue in issues:
                print(f"  ! {issue}")
            return 1
        print(f"{args.benchmark_id}: VALID (snapshot verified, all evidence resolves)")
        return 0

    system: EvidenceSystem = _REFERENCE_SYSTEMS[args.system]()
    artifact, path = run_benchmark(
        args.root,
        args.benchmark_id,
        system,
        started_at=datetime.now(UTC).isoformat(),
        software_version=__version__,
        git_sha=_git_sha(),
    )
    print(
        f"run complete: {args.benchmark_id} v{artifact.benchmark_version} "
        f"system={artifact.system.model_id}"
    )
    for name, value in artifact.aggregates.items():
        print(f"  {name}: {value}")
    print(f"artifact: {path}")
    print(f"results_id: {artifact.results_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
