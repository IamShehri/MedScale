"""Tests for the reproducibility primitives.

These assertions are themselves deterministic: they encode the byte-stability contract
that the rest of the platform will rely on.
"""

from __future__ import annotations

import random

import pytest

import medscale


def test_canonical_json_is_order_independent() -> None:
    a = medscale.canonical_json({"b": 1, "a": 2})
    b = medscale.canonical_json({"a": 2, "b": 1})
    assert a == b == '{"a":2,"b":1}'


def test_canonical_json_preserves_unicode() -> None:
    assert medscale.canonical_json({"k": "café"}) == '{"k":"café"}'


def test_content_hash_is_stable_and_order_independent() -> None:
    digest = medscale.content_hash({"a": 1, "b": [1, 2, 3]})
    assert digest == medscale.content_hash({"b": [1, 2, 3], "a": 1})
    assert len(digest) == 64


def test_content_hash_differs_on_different_content() -> None:
    assert medscale.content_hash({"a": 1}) != medscale.content_hash({"a": 2})


def test_set_global_seed_is_deterministic() -> None:
    medscale.set_global_seed(0)
    first = [random.random() for _ in range(3)]
    medscale.set_global_seed(0)
    second = [random.random() for _ in range(3)]
    assert first == second


def test_set_global_seed_returns_seed() -> None:
    assert medscale.set_global_seed(42) == 42


def test_set_global_seed_rejects_negative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        medscale.set_global_seed(-1)
