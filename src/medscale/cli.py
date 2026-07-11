"""The `medscale` command-line entry point.

A thin dispatcher over subcommands. Today the only subcommand is ``screen`` (the human
literature-screening workflow); more land as their phases arrive. Kept deliberately
minimal — no framework, just argv dispatch.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from medscale.litdb import integrity, screen_cli

_SUBCOMMANDS = {"screen": screen_cli.main, "check": integrity.main}


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print("usage: medscale <command> [options]")
        print("\ncommands:\n  screen   human literature screening")
        print("  check    verify corpus/log referential integrity")
        return 0 if args else 1
    command, rest = args[0], args[1:]
    handler = _SUBCOMMANDS.get(command)
    if handler is None:
        print(
            f"unknown command {command!r}; known: {', '.join(sorted(_SUBCOMMANDS))}",
            file=sys.stderr,
        )
        return 2
    return handler(rest)


if __name__ == "__main__":
    raise SystemExit(main())
