"""Compatibility shim for the legacy ``medscale.evidence`` flat module.

Stability: **public compatibility layer** — preserves historical imports and
data-format compatibility after the evidence subpackage extraction.

Old import paths remain valid::

    from medscale.evidence import EvidenceObject
    from medscale.evidence import VerificationState, StudyType, ExtractionMethod

New code should import from the subpackage directly::

    from medscale.evidence.models import EvidenceObject
    from medscale.evidence import level_from_study_type
"""

from __future__ import annotations

from medscale.evidence.grading import level_from_study_type
from medscale.evidence.models import (
    SCHEMA_VERSION,
    STUDY_DESIGN_LEVEL_SCHEME,
    EvidenceObject,
    EvidenceSystem,
    ExtractionMethod,
    StudyType,
    VerificationState,
)

__all__ = [
    "SCHEMA_VERSION",
    "STUDY_DESIGN_LEVEL_SCHEME",
    "EvidenceObject",
    "EvidenceSystem",
    "ExtractionMethod",
    "StudyType",
    "VerificationState",
    "level_from_study_type",
]
