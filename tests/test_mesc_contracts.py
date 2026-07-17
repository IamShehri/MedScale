"""Tests for Pilot-01 deterministic record contracts."""

from __future__ import annotations

import json
from pathlib import Path

from medscale.mesc.contracts import (
    SCHEMA_VERSION,
    PilotClaim,
    PilotEvidence,
    PilotProvenance,
    PilotRecord,
    PilotSourceIdentity,
    PilotTarget,
)


def _build_record(example_id: str) -> PilotRecord:
    source = PilotSourceIdentity(
        dataset_id="qiaojin/PubMedQA",
        dataset_revision="pqa-labeled-immutable",
        configuration="pqa_labeled",
        original_example_id=example_id,
        source_document_id=example_id,
        license_id="PubMedQA-PQA-L",
    )
    evidence = (
        PilotEvidence(
            evidence_id="E1", sentence_index=0, text="Evidence text.", source_document_id=example_id
        ),
    )
    claim = PilotClaim(
        claim_id="C1", text="Claim text.", evidence_ids=("E1",), annotation_status="gold"
    )
    target = PilotTarget(
        decision="yes",
        answer="Yes.",
        claims=(claim,),
        evidence_sufficiency="sufficient",
        uncertainty="low",
        abstain=False,
    )
    provenance = PilotProvenance(
        transformation_version="mesc-pilot-01/1",
        annotation_method="manual",
        annotation_revision="smoke-v1",
        synthetic=False,
    )
    return PilotRecord(
        schema_version=SCHEMA_VERSION,
        example_id=example_id,
        source=source,
        question="Question text?",
        evidence=evidence,
        target=target,
        provenance=provenance,
    )


def test_content_hash_is_deterministic() -> None:
    record = _build_record("stable-hash")
    first = record.content_hash()
    second = record.content_hash()
    assert first == second
    assert len(first) == 16


def test_frozen_record_rejects_assignment() -> None:
    record = _build_record("immutable-field")
    try:
        record.example_id = "other"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("expected immutable record to reject assignment")


def test_invalid_decision_accepted_by_literal_type() -> None:
    target = PilotTarget(
        decision="maybe",
        answer="Maybe.",
        claims=(),
        evidence_sufficiency="insufficient",
        uncertainty="high",
        abstain=False,
    )
    assert target.decision == "maybe"


def test_record_serialization_matches_schema_version() -> None:
    record = _build_record("schema-version")
    payload = json.loads(json.dumps(record, default=lambda obj: obj.__dict__))
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["source"]["license_id"] == "PubMedQA-PQA-L"


def test_required_contracts_are_exported_from_package() -> None:
    expected = {
        "SCHEMA_VERSION",
        "PilotClaim",
        "PilotEvaluationReport",
        "PilotEvaluationResult",
        "PilotEvidence",
        "PilotLeakageAuditReport",
        "PilotMetricValue",
        "PilotProvenance",
        "PilotRecord",
        "PilotRunManifest",
        "PilotSourceIdentity",
        "PilotSplitAssignment",
        "PilotSplitManifest",
        "PilotTarget",
        "SourceDocumentGroupedSplitter",
        "pilot_abstention_precision_recall",
        "pilot_aggregate_counts",
        "pilot_decision_accuracy",
        "pilot_evidence_reference_validity",
        "pilot_macro_f1",
        "pilot_supported_claim_metrics",
        "pilot_valid_json_rate",
    }
    import medscale.mesc as package

    missing = expected - set(package.__all__)
    assert not missing, f"missing exports: {sorted(missing)}"


def test_smoke_fixture_records_are_valid() -> None:
    fixture = Path("tests/fixtures/mesc/pilot_smoke.jsonl")
    lines = [line for line in fixture.read_text(encoding="utf-8").splitlines() if line.strip()]
    records = [json.loads(line) for line in lines]
    assert len(records) == 5
    example_ids = [record["example_id"] for record in records]
    assert len(example_ids) == len(set(example_ids))
    decisions = [record["target"]["decision"] for record in records]
    assert "yes" in decisions
    assert "no" in decisions
    assert "maybe" in decisions
    assert decisions.count("abstain") == 2
