"""ADR-0009 invariants: identity, state machine, self-verification guard, grading."""

from __future__ import annotations

import pytest

from medscale.evidence import (
    STUDY_DESIGN_LEVEL_SCHEME,
    EvidenceObject,
    ExtractionMethod,
    StudyType,
    VerificationState,
    level_from_study_type,
)
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _provenance(identifier: str = "10.1000/example") -> Provenance:
    return Provenance(SourceAPI.PUBMED, identifier, _TS, "b" * 64)


def _evidence(**overrides: object) -> EvidenceObject:
    base: dict[str, object] = {
        "claim": "Drug X reduces systolic blood pressure in adults with hypertension.",
        "study_type": StudyType.RANDOMIZED_CONTROLLED_TRIAL,
        "provenance": _provenance(),
        "created_at": _TS,
    }
    base.update(overrides)
    return EvidenceObject(**base)  # type: ignore[arg-type]


def test_evidence_id_is_deterministic() -> None:
    assert _evidence().evidence_id == _evidence().evidence_id


def test_evidence_id_ignores_verification_state() -> None:
    a = _evidence()
    b = a.with_verification(VerificationState.SOURCE_VERIFIED)
    assert a.evidence_id == b.evidence_id


def test_evidence_id_changes_with_claim() -> None:
    assert _evidence().evidence_id != _evidence(claim="Drug X has no effect.").evidence_id


def test_empty_claim_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        _evidence(claim="   ")


def test_default_grading_derived_from_study_type() -> None:
    assert _evidence().evidence_level == "2"  # RCT
    assert _evidence(study_type=StudyType.SYSTEMATIC_REVIEW).evidence_level == "1"


def test_all_study_types_have_a_level() -> None:
    for st in StudyType:
        assert level_from_study_type(st) in {"1", "2", "3", "4", "5"}


def test_non_default_scheme_requires_explicit_level() -> None:
    with pytest.raises(ValueError, match="evidence_level is required"):
        _evidence(grading_scheme="grade")
    graded = _evidence(grading_scheme="grade", evidence_level="moderate")
    assert graded.grading_scheme != STUDY_DESIGN_LEVEL_SCHEME


def test_legal_verification_path() -> None:
    e = _evidence()
    e = e.with_verification(VerificationState.SOURCE_VERIFIED)
    e = e.with_verification(
        VerificationState.EXTRACTION_VERIFIED, checked_by=ExtractionMethod.HUMAN
    )
    e = e.with_verification(VerificationState.DISPUTED)
    e = e.with_verification(VerificationState.RETRACTED)
    assert e.verification is VerificationState.RETRACTED


def test_illegal_transition_rejected() -> None:
    with pytest.raises(ValueError, match="illegal verification transition"):
        _evidence().with_verification(VerificationState.EXTRACTION_VERIFIED)


def test_retracted_is_terminal() -> None:
    e = _evidence().with_verification(VerificationState.SOURCE_VERIFIED)
    e = e.with_verification(VerificationState.RETRACTED)
    with pytest.raises(ValueError, match="illegal verification transition"):
        e.with_verification(VerificationState.SOURCE_VERIFIED)


def test_model_cannot_verify_its_own_extraction() -> None:
    e = _evidence(extraction_method=ExtractionMethod.MODEL)
    e = e.with_verification(VerificationState.SOURCE_VERIFIED)
    with pytest.raises(ValueError, match="cannot verify its own extraction"):
        e.with_verification(
            VerificationState.EXTRACTION_VERIFIED, checked_by=ExtractionMethod.MODEL
        )
    with pytest.raises(ValueError, match="cannot verify its own extraction"):
        e.with_verification(VerificationState.EXTRACTION_VERIFIED)
    checked = e.with_verification(
        VerificationState.EXTRACTION_VERIFIED, checked_by=ExtractionMethod.RULE
    )
    assert checked.verification is VerificationState.EXTRACTION_VERIFIED


def test_naive_created_at_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        _evidence(created_at="2026-07-10T00:00:00")
