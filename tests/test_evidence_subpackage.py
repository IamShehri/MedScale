"""M2 evidence-subpackage contract: imports, serialization, and import safety.

The migration extracts the old ``medscale.evidence`` flat module into a package.
These tests pin the compatibility guarantees so the public surface never quietly
drifts.
"""

from __future__ import annotations

import sys


def test_public_import_paths_surface_evidence_object() -> None:
    """``EvidenceObject`` remains importable from the historical namespace."""
    from medscale.evidence import EvidenceObject

    assert EvidenceObject is not None


def test_subpackage_exports_match_compat_shim() -> None:
    """Public symbols are identical between package and flat module."""
    import medscale.evidence as flat_evidence
    from medscale.evidence import __all__ as fresh_all

    assert set(fresh_all) == set(flat_evidence.__all__)


def test_format_1_artifact_loads_and_roundtrips() -> None:
    """Old ``format: 1`` evidence artifacts load through the new package."""
    from medscale.evidence_store import evidence_from_dict, evidence_to_dict

    legacy_payload = {
        "format": 1,
        "evidence_id": "abc123",
        "claim": "Compatibility claim",
        "study_type": "systematic_review",
        "provenance": {
            "source_api": "openalex",
            "identifier": "10.1/x",
            "verified_at": "2026-07-12T00:00:00+00:00",
            "raw_response_sha256": "0" * 64,
            "status": "found",
        },
        "created_at": "2026-07-12T00:00:00+00:00",
        "source_record_id": "rec-1",
        "population": None,
        "intervention": None,
        "comparator": None,
        "outcome": None,
        "effect_measure": None,
        "effect_value": None,
        "grading_scheme": "medscale-study-design-v1",
        "evidence_level": "1",
        "extraction_method": "human",
        "verification": "unverified",
        "schema_version": "1",
    }

    evidence_object = evidence_from_dict(legacy_payload)
    assert evidence_object.evidence_id != "abc123"
    dumped = evidence_to_dict(evidence_object)
    assert dumped["evidence_id"] == evidence_object.evidence_id
    assert dumped["claim"] == "Compatibility claim"
    assert dumped["study_type"] == "systematic_review"
    assert dumped["verification"] == "unverified"
    assert dumped["format"] == 1


def test_subpackage_does_not_introduce_optional_runtime_deps() -> None:
    """Importing the evidence package must not mutate sys.modules with backends."""
    before = set(sys.modules)
    import medscale.evidence  # noqa: F401

    after = set(sys.modules)
    new_modules = after - before
    assert all("backend" not in name for name in new_modules)
