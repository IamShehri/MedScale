"""Tests for Pilot-01 run and evaluation manifest dataclasses."""

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
    PilotEvaluationReport,
    PilotEvaluationResult,
    PilotMetricValue,
    pilot_supported_claim_metrics,
)
from medscale.mesc.manifests import PilotRunManifest


def test_run_manifest_from_gold_claims() -> None:
    source = PilotSourceIdentity(
        dataset_id="qiaojin/PubMedQA",
        dataset_revision="pqa-labeled-immutable",
        configuration="pqa_labeled",
        original_example_id="run-manifest-gold",
        source_document_id="run-manifest-gold",
        license_id="PubMedQA-PQA-L",
    )
    evidence = (
        PilotEvidence(
            evidence_id="E1",
            sentence_index=0,
            text="Evidence text.",
            source_document_id="run-manifest-gold",
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
    record = PilotRecord(
        schema_version=SCHEMA_VERSION,
        example_id="run-manifest-gold",
        source=source,
        question="Question?",
        evidence=evidence,
        target=target,
        provenance=provenance,
    )

    manifest = PilotRunManifest(
        schema_version=SCHEMA_VERSION,
        run_id="run-manifest-gold",
        records=(record,),
        model_family="Llama",
        primary_model_id="meta-llama/Llama-3.2-3B-Instruct",
    )
    assert manifest.to_dict()["record_count"] == 1

    metrics = pilot_supported_claim_metrics([record], [[("C1", ("E1",))]])
    metric = PilotEvaluationResult(
        condition="pilot-run",
        metrics=(
            PilotMetricValue(
                name="supported_claim_precision",
                value=metrics[0].value,
                count=metrics[0].count,
                status=metrics[0].status,
            ),
            PilotMetricValue(
                name="supported_claim_recall",
                value=metrics[1].value,
                count=metrics[1].count,
                status=metrics[1].status,
            ),
            PilotMetricValue(
                name="unsupported_claim_rate",
                value=metrics[2].value,
                count=metrics[2].count,
                status=metrics[2].status,
            ),
        ),
    )
    report = PilotEvaluationReport(results=(metric,))
    serialized = json.dumps(report.to_dict(), sort_keys=True)
    assert json.loads(serialized)["results"][0]["metrics"][0]["name"] == "supported_claim_precision"
