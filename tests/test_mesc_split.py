"""Tests for Pilot-01 deterministic split and leakage contracts."""

from __future__ import annotations

import json

from medscale.mesc.split import (
    PilotLeakageAuditReport,
    PilotLeakageFinding,
    PilotSplitAssignment,
    PilotSplitManifest,
    SourceDocumentGroupedSplitter,
)


def test_split_assignment_properties() -> None:
    assignment = PilotSplitAssignment(
        example_id="e1", split="train", source_document_id="d1", partition_key="p1"
    )
    assert assignment.is_train is True
    assert assignment.is_validation is False
    assert assignment.is_test is False


def test_split_manifest_properties() -> None:
    assignment = PilotSplitAssignment(
        example_id="e1", split="train", source_document_id="d1", partition_key="p1"
    )
    manifest = PilotSplitManifest(split_assignments=(assignment,), split_seed="seed-1")
    assert manifest.train_example_ids == ("e1",)
    assert manifest.validation_example_ids == ()
    assert manifest.test_example_ids == ()
    assert manifest.holdout_example_ids == ()
    assert manifest.split_hash == ""
    assert manifest.computed_split_hash != ""
    assert len(manifest.computed_split_hash) == 16


def test_split_manifest_splits_examples() -> None:
    assignments = [
        PilotSplitAssignment(
            example_id="e1", split="train", source_document_id="d1", partition_key="p1"
        ),
        PilotSplitAssignment(
            example_id="e2", split="validation", source_document_id="d2", partition_key="p2"
        ),
        PilotSplitAssignment(
            example_id="e3", split="test", source_document_id="d3", partition_key="p3"
        ),
    ]
    manifest = PilotSplitManifest(split_assignments=tuple(assignments), split_seed="seed-2")
    assert manifest.train_example_ids == ("e1",)
    assert manifest.validation_example_ids == ("e2",)
    assert manifest.test_example_ids == ("e3",)
    assert manifest.holdout_example_ids == ()


def test_split_manifest_product_split_assignments_three_way() -> None:
    assignments = [
        PilotSplitAssignment(
            example_id="e1", split="train", source_document_id="d1", partition_key="p1"
        ),
        PilotSplitAssignment(
            example_id="e2", split="validation", source_document_id="d2", partition_key="p2"
        ),
        PilotSplitAssignment(
            example_id="e3", split="test", source_document_id="d3", partition_key="p3"
        ),
    ]
    manifest = PilotSplitManifest(split_assignments=tuple(assignments), split_seed="seed-3")
    assert manifest.train_example_ids == ("e1",)
    assert manifest.validation_example_ids == ("e2",)
    assert manifest.test_example_ids == ("e3",)
    assert manifest.holdout_example_ids == ()


def test_grouped_splitter_assigns_all_examples() -> None:
    splitter = SourceDocumentGroupedSplitter(seed="grouped-seed")
    manifest = splitter.assign(["e1", "e2", "e3"], ["d1", "d2", "d3"])
    assert len(manifest.train_example_ids) == 3
    assert manifest.validation_example_ids == ()
    assert manifest.test_example_ids == ()
    assert manifest.holdout_example_ids == ()
    assert manifest.split_hash == ""
    assert manifest.computed_split_hash != ""
    assert len(manifest.computed_split_hash) == 16


def test_leakage_audit_reports_findings() -> None:
    finding = PilotLeakageFinding(
        example_id="e1",
        duplicate_type="exact",
        match_example_id="e2",
        similarity=1.0,
        shared_surface=("question",),
    )
    audit = PilotLeakageAuditReport(findings=(finding,), leaked=True)
    assert audit.leaked is True
    assert audit.finding_count == 1
    serialized = json.loads(
        json.dumps(
            audit, default=lambda obj: obj.to_dict() if hasattr(obj, "to_dict") else obj.__dict__
        )
    )
    assert serialized["leaked"] is True
    assert len(serialized["findings"]) == 1


def test_leakage_audit_report_canonical_name() -> None:
    from medscale.mesc.split import PilotLeakageAudit, PilotLeakageAuditReport

    assert PilotLeakageAudit is PilotLeakageAuditReport


def test_leakage_audit_report_zero_findings() -> None:
    report = PilotLeakageAuditReport(findings=())
    assert report.finding_count == 0
    assert report.leaked is False
    payload = report.to_dict()
    assert payload["findings"] == []
    assert payload["finding_count"] == 0


def test_leakage_audit_report_is_immutable() -> None:
    import dataclasses

    report = PilotLeakageAuditReport(findings=())
    try:
        report.leaked = True  # type: ignore[misc]
    except (AttributeError, dataclasses.FrozenInstanceError):
        pass
    else:
        raise AssertionError("expected immutable audit report to reject assignment")


def test_leakage_audit_report_count_matches_findings() -> None:
    findings = (
        PilotLeakageFinding(
            example_id="e1",
            duplicate_type="exact",
            match_example_id="e2",
            similarity=1.0,
            shared_surface=("question",),
        ),
        PilotLeakageFinding(
            example_id="e3",
            duplicate_type="near_duplicate",
            match_example_id="e4",
            similarity=0.8,
            shared_surface=("question", "context"),
        ),
    )
    report = PilotLeakageAuditReport(findings=findings, leaked=True)
    assert report.finding_count == 2
    payload = report.to_dict()
    assert payload["finding_count"] == 2
    assert len(payload["findings"]) == 2
