"""Runtime context helpers — one implementation of "when" and "which commit".

Stability: **internal**. Previously four modules carried private ``_git_sha`` copies
with subtly different semantics; this is the single replacement.
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime

__all__ = ["git_sha", "utc_now"]


def utc_now() -> str:
    """Timezone-aware ISO-8601 timestamp for attribution fields."""
    return datetime.now(UTC).isoformat()


def git_sha(*, strict: bool = False) -> str:
    """Current repository HEAD.

    ``strict=True`` raises when git is unavailable (runs whose manifests must cite a
    real commit); the default degrades to the ``0000000`` placeholder (interactive
    attribution where a missing repo must not crash a session).
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        if strict:
            raise
        return "0000000"
