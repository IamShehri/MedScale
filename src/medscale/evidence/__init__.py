"""Public evidence-data package (M2 extraction).

Stability: **public-frozen data model** — ``EvidenceObject`` and its identity
derivation are contract (ADR-0017); constructors and field semantics do not change
without an ADR + migration.

This package preserves the historical public surface::

    from medscale.evidence import (
        EvidenceObject,
        ExtractionMethod,
        STUDY_DESIGN_LEVEL_SCHEME,
        StudyType,
        VerificationState,
        level_from_study_type,
    )
"""

from __future__ import annotations

from medscale.evidence.grading import level_from_study_type
from medscale.evidence.models import (
    SCHEMA_VERSION,
    STUDY_DESIGN_LEVEL_SCHEME,
    EvidenceObject,
    ExtractionMethod,
    StudyType,
    VerificationState,
)

__all__ = [
    "SCHEMA_VERSION",
    "STUDY_DESIGN_LEVEL_SCHEME",
    "EvidenceObject",
    "ExtractionMethod",
    "StudyType",
    "VerificationState",
    "level_from_study_type",
]
