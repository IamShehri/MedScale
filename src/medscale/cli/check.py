"""Integrity CLI: `medscale check` — exits non-zero on any violation (CI gate, ADR-0017).

Stability: transport adapter. Deliberately does NOT go through :class:`medscale.Workspace`:
a corruption checker must run against trees too broken for the index to load, so it
calls the integrity library directly (fail-closed diagnosis, never fail-open loading).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import medscale._layout as _layout
from medscale.litdb.integrity import check_litdb, format_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale check", description=__doc__)
    parser.add_argument("--root", type=Path, default=_layout.DEFAULT_ROOT)
    args = parser.parse_args(argv)
    report = check_litdb(args.root)
    print(format_report(report))
    return 0 if report.is_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
