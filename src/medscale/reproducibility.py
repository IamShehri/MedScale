"""Deterministic, reproducible primitives for MedScale.

MedScale headlines only deterministic, executable results (see
``docs/research/reproducibility_policy.md``). Every reproducible artifact needs two
byte-stable operations - canonical serialization and content hashing - plus one entry
point for seeding process-level randomness. Those three live here.

No research logic lives in this module; it is foundational infrastructure only.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
from typing import Any

__all__ = ["canonical_json", "content_hash", "set_global_seed"]


def canonical_json(obj: Any) -> str:
    """Serialize ``obj`` to a byte-stable JSON string.

    The output is independent of dict insertion order and of locale: keys are sorted,
    separators are fixed, and non-ASCII characters are preserved rather than escaped.
    Two equal objects always produce identical bytes, which is what makes a committed
    result artifact reproducible.
    """
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def content_hash(obj: Any) -> str:
    """Return the SHA-256 hex digest of ``obj``'s canonical JSON encoding.

    Used to fingerprint configs, datasets, and result artifacts so a run can assert it
    operated on identical inputs (provenance and contamination control).
    """
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def set_global_seed(seed: int) -> int:
    """Seed process-level randomness deterministically and return ``seed``.

    Seeds the standard-library RNG and ``PYTHONHASHSEED``. Numerical libraries (NumPy,
    PyTorch) are deliberately not touched here: they are not yet dependencies, and their
    seeding will be added alongside the training stack, behind explicit imports.
    """
    if seed < 0:
        raise ValueError(f"seed must be non-negative, got {seed}")
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    return seed
