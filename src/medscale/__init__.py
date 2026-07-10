"""MedScale: open research intelligence infrastructure for medicine.

The top-level surface exposes reproducibility primitives. Pillar-2 foundations live in
:mod:`medscale.provenance`, :mod:`medscale.evidence` (ADR-0009), and
:mod:`medscale.litdb` (T1). FHIR, grammar, validation, benchmark, and model APIs are
added in their own phases (see docs/vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md).
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
