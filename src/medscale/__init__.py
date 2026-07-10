"""MedScale: an open research platform for verifiable clinical AI.

This is the foundational public surface. It intentionally exposes only reproducibility
primitives at v0; FHIR, grammar, validation, benchmark, and model APIs are added in
their own phases (see docs/vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md).
"""

from __future__ import annotations

from medscale.__about__ import __version__
from medscale.reproducibility import canonical_json, content_hash, set_global_seed

__all__ = [
    "__version__",
    "canonical_json",
    "content_hash",
    "set_global_seed",
]
