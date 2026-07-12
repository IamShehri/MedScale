"""Grading and level mapping for evidence objects.

Stability: internal. These helpers are re-exported through :mod:`medscale.evidence`
but live here so grading schemes can grow without changing the public data-model
package topology.
"""

from __future__ import annotations

from typing import Final

from medscale.evidence.models import StudyType

_LEVEL_BY_STUDY_TYPE: Final[dict[StudyType, str]] = {
    StudyType.SYSTEMATIC_REVIEW: "1",
    StudyType.META_ANALYSIS: "1",
    StudyType.RANDOMIZED_CONTROLLED_TRIAL: "2",
    StudyType.COHORT: "3",
    StudyType.CASE_CONTROL: "3",
    StudyType.CROSS_SECTIONAL: "4",
    StudyType.CASE_REPORT: "4",
    StudyType.PRECLINICAL: "5",
    StudyType.IN_SILICO: "5",
    StudyType.OTHER: "5",
}


def level_from_study_type(study_type: StudyType) -> str:
    """Deterministically derive the ``medscale-study-design-v1`` level."""
    return _LEVEL_BY_STUDY_TYPE[study_type]


__all__ = ["level_from_study_type"]
