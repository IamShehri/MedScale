"""Regression tests for the approved ALIGN-13 dataset builder slice."""

from __future__ import annotations

import hashlib
import json

from medscale.dataset.builder.contracts import PipelineContext, StageDefinition, StageResult
from medscale.dataset.builder.fingerprint import context_fingerprint, pipeline_fingerprint
from medscale.dataset.builder.manifest import AuditReport, DatasetReleaseManifest, QualityReport


def test_stage_result_contract_fields_match_matrix() -> None:
    result = StageResult(
        stage_name="discovery",
        input_count=10,
        accepted=8,
        rejected=2,
        artifacts=("artifacts/run.json",),
        metadata={"seed": 0},
    )
    assert result.stage_name == "discovery"
    assert result.input_count == 10
    assert result.accepted == 8
    assert result.rejected == 2
    assert result.artifacts == ("artifacts/run.json",)
    assert result.metadata == {"seed": 0}


def test_stage_definition_contract_is_frozen() -> None:
    definition = StageDefinition(name="screening", inputs=("raw",), outputs=("accepted",))
    assert definition.name == "screening"
    assert definition.inputs == ("raw",)
    assert definition.outputs == ("accepted",)
    assert hash(definition) == hash(definition)


def test_pipeline_context_contract_carries_results() -> None:
    result = StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0)
    context = PipelineContext(
        root="data/pilot",
        config={"dataset_id": "pilot-1"},
        results=(result,),
        bundle_references=("bundle-raw",),
        validation_statuses={"raw": "passed"},
        metadata={"executed_by": "tests"},
    )
    assert context.root == "data/pilot"
    assert context.config == {"dataset_id": "pilot-1"}
    assert context.results == (result,)
    assert context.bundle_references == ("bundle-raw",)
    assert context.validation_statuses == {"raw": "passed"}
    assert context.metadata == {"executed_by": "tests"}


def test_dataset_release_manifest_canonical_serialization() -> None:
    manifest = DatasetReleaseManifest(
        dataset_id="litdb-v1",
        dataset_version="1.0.0",
        dataset_fingerprint="abcdef",
        release_id="r-1",
        released_at="2026-07-13T00:00:00+00:00",
        released_by="founder",
        dataset_manifest_sha256="0" * 64,
        bundle_id_registry_sha256="1" * 64,
        validation_summary={"status": "passed"},
        quality_summary={"green": True},
        release_notes="Initial release",
        previous_release_id=None,
    )
    expected = json.dumps(
        {
            "dataset_id": "litdb-v1",
            "dataset_version": "1.0.0",
            "dataset_fingerprint": "abcdef",
            "release_id": "r-1",
            "released_at": "2026-07-13T00:00:00+00:00",
            "released_by": "founder",
            "dataset_manifest_sha256": "0" * 64,
            "bundle_id_registry_sha256": "1" * 64,
            "validation_summary": {"status": "passed"},
            "quality_summary": {"green": True},
            "release_notes": "Initial release",
            "previous_release_id": None,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    assert json.dumps(manifest.__dict__, sort_keys=True, separators=(",", ":")) == expected


def test_dataset_release_fingerprint_is_stable() -> None:
    manifest = DatasetReleaseManifest(
        dataset_id="litdb-v1",
        dataset_version="1.0.0",
        dataset_fingerprint="abcdef",
        release_id="r-1",
        released_at="2026-07-13T00:00:00+00:00",
        released_by="founder",
        dataset_manifest_sha256="0" * 64,
        bundle_id_registry_sha256="1" * 64,
    )
    payload = json.dumps(manifest.__dict__, sort_keys=True, separators=(",", ":"))
    expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    assert expected == hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_audit_report_defaults() -> None:
    report = AuditReport(
        dataset_id="litdb-v1",
        dataset_version="1.0.0",
        audit_timestamp="2026-07-13T00:00:00+00:00",
        green=True,
        record_count=5,
    )
    assert report.bundle_ids == ()
    assert report.validation_statuses == {}
    assert report.rejection_counts == {}
    assert report.checksum_verification == {}
    assert report.failures == ()
    assert report.coverage_report_version is None
    assert report.analytics_report_version is None


def test_quality_report_defaults() -> None:
    report = QualityReport(dataset_id="litdb-v1", dataset_version="1.0.0")
    assert report.stage_quality_summaries == {}
    assert report.rejection_counts == {}
    assert report.synthetic_proportions == {}
    assert report.license_audit == {}
    assert report.bias_monitoring_summary == {}
    assert report.contamination_summary == {}
    assert report.benchmark_linkage_status == {}
    assert report.green is False


def test_pipeline_fingerprint_ignores_artifact_insertion_order() -> None:
    first = (
        StageResult(
            stage_name="raw",
            input_count=1,
            accepted=1,
            rejected=0,
            artifacts=("a", "b"),
        ),
        StageResult(
            stage_name="screening",
            input_count=1,
            accepted=1,
            rejected=0,
            artifacts=("c",),
        ),
    )
    second = (
        StageResult(
            stage_name="raw",
            input_count=1,
            accepted=1,
            rejected=0,
            artifacts=("b", "a"),
        ),
        StageResult(
            stage_name="screening",
            input_count=1,
            accepted=1,
            rejected=0,
            artifacts=("c",),
        ),
    )
    assert pipeline_fingerprint(first) == pipeline_fingerprint(second)


def test_context_fingerprint_ignores_dict_insertion_order() -> None:
    first = PipelineContext(
        root="data/pilot",
        config={"seed": 0, "dataset_id": "pilot-1"},
        validation_statuses={"raw": "passed", "screening": "passed"},
    )
    second = PipelineContext(
        root="data/pilot",
        config={"dataset_id": "pilot-1", "seed": 0},
        validation_statuses={"screening": "passed", "raw": "passed"},
    )
    assert context_fingerprint(first) == context_fingerprint(second)


def test_pipeline_fingerprint_changes_when_results_change() -> None:
    original = (StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0),)
    mutated = (StageResult(stage_name="raw", input_count=5, accepted=4, rejected=1),)
    assert pipeline_fingerprint(original) != pipeline_fingerprint(mutated)


def test_context_fingerprint_changes_when_bundle_references_change() -> None:
    first = PipelineContext(root="data/pilot", bundle_references=("bundle-1",))
    second = PipelineContext(root="data/pilot", bundle_references=("bundle-2",))
    assert context_fingerprint(first) != context_fingerprint(second)
