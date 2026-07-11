"""Read-side CLI: `medscale stats` and `medscale snapshot` — thin over the Core Library.

Stability: transport adapter. All engine behavior comes from :class:`medscale.Workspace`;
this module only parses arguments and prints.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Final

import medscale._layout as _layout
from medscale.reproducibility import canonical_json
from medscale.research.snapshot import load_snapshot
from medscale.workspace import Workspace

_DEFAULT_ROOT: Final = _layout.DEFAULT_ROOT


def stats_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale stats", description=__doc__)
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    args = parser.parse_args(argv)
    print(canonical_json(Workspace.open(args.root).stats()))
    return 0


def snapshot_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale snapshot", description=__doc__)
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    parser.add_argument(
        "--verify",
        type=Path,
        default=None,
        help="verify the tree against an existing snapshot file instead of capturing",
    )
    args = parser.parse_args(argv)
    workspace = Workspace.open(args.root)

    if args.verify is not None:
        snapshot = load_snapshot(args.verify)
        mismatches = workspace.verify(snapshot)
        if mismatches:
            print(f"snapshot {snapshot.snapshot_id[:16]}: MISMATCH")
            for mismatch in mismatches:
                print(f"  ! {mismatch}")
            return 1
        print(f"snapshot {snapshot.snapshot_id[:16]}: VERIFIED (knowledge state matches)")
        return 0

    snapshot = workspace.snapshot()
    path = _layout.snapshots_dir(args.root) / f"{snapshot.snapshot_id[:16]}.json"
    print(f"snapshot {snapshot.snapshot_id[:16]} written -> {path}")
    print(f"cite as: MedScale knowledge snapshot {snapshot.snapshot_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(stats_main())
