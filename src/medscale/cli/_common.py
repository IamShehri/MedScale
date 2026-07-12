"""Shared transport guards: a typo'd path must fail with advice, never a traceback.

Stability: internal. Nothing here contains engine logic - only argument sanity checks
so a researcher who mistypes ``--root`` gets an actionable message (exit 2) instead of
a stack trace or, worse, a fabricated empty result that looks like real data.
"""

from __future__ import annotations

import sys
from pathlib import Path

import medscale._layout as _layout

#: Exit code for operator errors (bad path, unknown id) - distinct from engine
#: failures (1: dirty tree, invalid benchmark, snapshot mismatch).
USAGE_ERROR = 2


def fail(message: str, *, hint: str | None = None) -> int:
    """Print an operator-facing error (and optional hint) to stderr; return exit 2."""
    print(f"error: {message}", file=sys.stderr)
    if hint:
        print(f"hint : {hint}", file=sys.stderr)
    return USAGE_ERROR


def require_root(root: Path) -> int | None:
    """The workspace directory must exist. None = proceed; int = exit code.

    An *empty* existing directory is a valid fresh workspace (stats are all zero,
    nothing to screen); a *nonexistent* one is almost always a typo and must never
    be reported as an empty corpus.
    """
    if not root.is_dir():
        return fail(
            f"workspace root not found: {root}",
            hint="pass --root <path to your litdb tree> (the default is data/litdb, "
            "relative to where you run the command)",
        )
    return None


def require_corpus(root: Path) -> int | None:
    """Root must exist *and* contain an ingested corpus. None = proceed."""
    guard = require_root(root)
    if guard is not None:
        return guard
    corpus = _layout.corpus_path(root)
    if not corpus.is_file():
        return fail(
            f"no corpus at {corpus}",
            hint="this workspace has no ingested records yet - see "
            "docs/guides/research_quickstart.md",
        )
    return None
