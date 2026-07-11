"""Read-side CLI: `medscale stats` and `medscale snapshot` — machine-readable only.

``stats`` prints one canonical-JSON document (corpus + screening + evidence statistics)
to stdout: pipeable, diffable, byte-stable for a given knowledge state. ``snapshot``
captures (and optionally verifies) the citable knowledge-state identity. No
visualization, no presentation — future consumers (APIs, papers, Afia) parse, humans
can still read.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from medscale import __version__
from medscale.reproducibility import canonical_json
from medscale.research.index import ResearchIndex
from medscale.research.snapshot import (
    capture_snapshot,
    load_snapshot,
    verify_snapshot,
    write_snapshot,
)
from medscale.research.stats import corpus_stats, evidence_stats, screening_stats

_DEFAULT_ROOT: Final = Path("data/litdb")


def _git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0000000"


def stats_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale stats", description=__doc__)
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    args = parser.parse_args(argv)
    index = ResearchIndex.load(args.root)
    document = {
        "corpus": corpus_stats(index).to_dict(),
        "screening": screening_stats(index).to_dict(),
        "evidence": evidence_stats(index).to_dict(),
    }
    print(canonical_json(document))
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

    if args.verify is not None:
        snapshot = load_snapshot(args.verify)
        mismatches = verify_snapshot(args.root, snapshot)
        if mismatches:
            print(f"snapshot {snapshot.snapshot_id[:16]}: MISMATCH")
            for mismatch in mismatches:
                print(f"  ! {mismatch}")
            return 1
        print(f"snapshot {snapshot.snapshot_id[:16]}: VERIFIED (knowledge state matches)")
        return 0

    snapshot = capture_snapshot(
        args.root,
        git_sha=_git_sha(),
        software_version=__version__,
        created_at=datetime.now(UTC).isoformat(),
    )
    path = write_snapshot(args.root, snapshot)
    print(f"snapshot {snapshot.snapshot_id[:16]} written -> {path}")
    print(f"cite as: MedScale knowledge snapshot {snapshot.snapshot_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(stats_main())
