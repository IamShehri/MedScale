"""Lightweight dataset snapshot metadata for reproducibility.

Stability: **public-frozen by ADR-0030**. The snapshot fields are a
reproducibility contract; changing them requires a new dataset version and a new
ADR.

DatasetSnapshot must not depend on `medscale.research` or any higher-level
package. It is populated from explicit CLI inputs only.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["DatasetSnapshot"]


@dataclass(frozen=True)
class DatasetSnapshot:
    """Immutable dataset reproducibility snapshot."""

    git_sha: str
    software_version: str
    created_at: str
    fingerprint: str = ""
