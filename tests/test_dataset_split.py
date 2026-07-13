"""Deterministic split reproducibility."""

from __future__ import annotations

from medscale.dataset.split import DeterministicSplitter


def test_same_seed_produces_identical_split() -> None:
    ids = [f"record-{idx:03d}" for idx in range(40)]
    first = DeterministicSplitter(seed=42).split(ids)
    second = DeterministicSplitter(seed=42).split(ids)
    assert first.train == second.train
    assert first.validation == second.validation
    assert first.test == second.test


def test_different_seed_produces_different_split() -> None:
    ids = [f"record-{idx:03d}" for idx in range(40)]
    first = DeterministicSplitter(seed=42).split(ids)
    second = DeterministicSplitter(seed=43).split(ids)
    assert (first.train, first.validation, first.test) != (
        second.train,
        second.validation,
        second.test,
    )


def test_sorted_order_is_deterministic() -> None:
    ids = ["z-1", "a-1", "m-1"]
    first = DeterministicSplitter(seed=42).split(ids)
    second = DeterministicSplitter(seed=42).split(list(reversed(ids)))
    assert first.train == second.train
    assert first.validation == second.validation
    assert first.test == second.test
