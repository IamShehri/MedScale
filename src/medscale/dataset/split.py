"""Deterministic dataset splitting.

Stability: **public**. Split assignments are reproducible for a fixed seed and
sorted record-id order. No global random state is used.
"""

from __future__ import annotations

import enum
from collections.abc import Sequence
from dataclasses import dataclass

from medscale.reproducibility import content_hash

__all__ = ["DeterministicSplitter", "SplitResult", "SplitStrategy", "split_literature_records"]


class SplitStrategy(enum.StrEnum):
    DETERMINISTIC_HASH_SPLIT = "deterministic_hash_split"


@dataclass(frozen=True)
class SplitResult:
    """Deterministic split output for a fixed record set."""

    strategy: SplitStrategy
    seed: int
    train: list[str]
    validation: list[str]
    test: list[str]

    @property
    def total(self) -> int:
        return len(self.train) + len(self.validation) + len(self.test)


class DeterministicSplitter:
    """Deterministic splitter for stable record identifiers."""

    def __init__(self, *, seed: int = 42) -> None:
        self.seed = seed

    def split(self, record_ids: Sequence[str]) -> SplitResult:
        """Assign record ids to train/validation/test deterministically.

        The assignment hashes the salted record id and maps the result into the
        configured train/validation/test ratio band.
        """
        if not record_ids:
            return SplitResult(
                strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
                seed=self.seed,
                train=[],
                validation=[],
                test=[],
            )

        sorted_ids = sorted(set(record_ids))
        train: list[str] = []
        validation: list[str] = []
        test: list[str] = []
        for record_id in sorted_ids:
            digest = content_hash({"seed": self.seed, "record_id": record_id})
            bucket = int(digest[:8], 16) % 100
            if bucket < 70:
                train.append(record_id)
            elif bucket < 85:
                validation.append(record_id)
            else:
                test.append(record_id)
        return SplitResult(
            strategy=SplitStrategy.DETERMINISTIC_HASH_SPLIT,
            seed=self.seed,
            train=train,
            validation=validation,
            test=test,
        )


from typing import Protocol, Sequence, runtime_checkable


@runtime_checkable
class _HasRecordId(Protocol):
    record_id: str


def split_literature_records(records: Sequence[_HasRecordId], *, seed: int = 42) -> SplitResult:
    """Split literature records by stable ``record_id``."""
    record_ids = [record.record_id for record in records]
    return DeterministicSplitter(seed=seed).split(record_ids)
