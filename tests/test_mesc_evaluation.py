"""Tests for Pilot-01 deterministic evaluation metrics."""

from __future__ import annotations

import json

from medscale.mesc.contracts import (
    SCHEMA_VERSION,
    PilotClaim,
    PilotEvidence,
    PilotProvenance,
    PilotRecord,
    PilotSourceIdentity,
    PilotTarget,
)
from medscale.mesc.evaluation import (
    PilotEvaluationResult,
    PilotMetricValue,
    pilot_abstention_precision_recall,
    pilot_decision_accuracy,
    pilot_evidence_reference_validity,
    pilot_macro_f1,
    pilot_supported_claim_metrics,
    pilot_valid_json_rate,
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


def test_decision_accuracy_determinism() -> None:
    metric = pilot_decision_accuracy(["yes", "no"], ["yes", "no"])
    assert metric.value == 1.0


def test_macro_f1_determinism() -> None:
    metric = pilot_macro_f1(["yes", "no"], ["yes", "no"])
    assert metric.value == 0.5


def test_valid_json_rate_determinism() -> None:
    metric = pilot_valid_json_rate(['{"a":1}', "not-json"])
    assert metric.value == 0.5


def test_evidence_reference_validity_determinism() -> None:
    record = _build_record("evidence-validity")
    metric = pilot_evidence_reference_validity([record], [[("C1", ("E1",))]])
    assert metric.value == 1.0


def test_abstention_precision_recall_determinism() -> None:
    precision, recall = pilot_abstention_precision_recall(
        ["abstain", "yes"], ["abstain", "abstain"]
    )
    assert precision.value == 1.0
    assert recall.value == 0.5


def test_supported_claim_metrics_determinism() -> None:
    record = _build_record("supported-claims")
    metrics = pilot_supported_claim_metrics([record], [[("C1", ("E1",))]])
    assert metrics[0].value == 1.0
    assert metrics[1].value == 1.0
    assert metrics[2].value == 0.0


def test_empty_records_returns_not_applicable() -> None:
    metric = pilot_decision_accuracy([], [])
    assert metric.status == "not_applicable"
    assert metric.value is None


def test_serialization_determinism() -> None:
    metric = PilotMetricValue(name="x", value=1.0, count=1, note="ok", status="success")
    result = PilotEvaluationResult(condition="baseline", metrics=(metric,))
    assert result.to_dict() == json.loads(json.dumps(result.to_dict(), sort_keys=True))
