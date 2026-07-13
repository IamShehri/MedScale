"""Backward-compatibility shim for the dataset package.

Stability: **public compatibility layer**. Preserves historical helper imports
and API shapes after the dataset package extraction without forking
responsibilities or duplicating business logic.
"""

from __future__ import annotations

from collections.abc import Sequence


def deterministic_hash_split(
    record_ids: Sequence[str],
    *,
    seed: int = 42,
) -> tuple[list[str], list[str], list[str]]:
    """Public shim preserving the old tuple-return split API.

    Preferred path: import the typed splitter from ``medscale.dataset.split``
    and use ``DeterministicSplitter(...).split(...)``.
    """
    from medscale.dataset.split import DeterministicSplitter

    result = DeterministicSplitter(seed=seed).split(list(record_ids))
    return result.train, result.validation, result.test
