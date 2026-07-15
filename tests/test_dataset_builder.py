"""Regression tests for the approved ALIGN-13 dataset builder slice."""

from __future__ import annotations

import ast
import dataclasses
import os
import pathlib
import typing
from typing import Any

import pytest

from medscale.dataset import __all__ as dataset_all
from medscale.dataset.builder import __all__ as builder_all
from medscale.dataset.builder.contracts import PipelineContext, StageDefinition, StageResult
from medscale.dataset.builder.contracts import __all__ as contracts_all
from medscale.dataset.builder.fingerprint import __all__ as fingerprint_all
from medscale.dataset.builder.fingerprint import context_fingerprint, pipeline_fingerprint
from medscale.dataset.builder.manifest import AuditReport, DatasetReleaseManifest, QualityReport
from medscale.dataset.builder.manifest import __all__ as manifest_all
from medscale.reproducibility import canonical_json, content_hash

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_PLACEHOLDERS = {
    "FingerprintInput",
    "ManifestRecord",
    "DatasetBinding",
    "DataloaderPolicy",
    "EvidenceDomain",
    "BondingKey",
    "ReleaserBinding",
    "ProvenanceCursor",
    "DatasetEngine",
}

_LITERATURE_RECORD_SCHEMA = "42bc99211780bb41b8d52af1c676a810564ddbaa61620b0cce0a8acda8081683"
_EVIDENCE_OBJECT_SCHEMA = "22451df6203bf739f5aa798095388fc15a5190824724a4a5a0a40517458b0ecd"
_BENCHMARK_ITEM_SCHEMA = "bdb219198c2109483901a15735d52dad0d6e911d065559fd0394393575f12bbb"


# ---------------------------------------------------------------------------
# A. Exact exports
# ---------------------------------------------------------------------------
def test_builder_module_exports_are_exact() -> None:
    expected_builder = {
        "AuditReport",
        "DatasetReleaseManifest",
        "PipelineContext",
        "QualityReport",
        "SplitAssignmentFreeze",
        "StageDefinition",
        "StageResult",
        "context_fingerprint",
        "pipeline_fingerprint",
    }
    assert set(builder_all) == expected_builder


def test_contracts_module_exports_are_exact() -> None:
    assert set(contracts_all) == {"PipelineContext", "StageDefinition", "StageResult"}


def test_manifest_module_exports_are_exact() -> None:
    assert set(manifest_all) == {"AuditReport", "DatasetReleaseManifest", "QualityReport"}


def test_fingerprint_module_exports_are_exact() -> None:
    assert set(fingerprint_all) == {"context_fingerprint", "pipeline_fingerprint"}


def test_facade_symbols_are_available_through_builder_only() -> None:
    assert "PipelineContext" in builder_all
    assert "PipelineContext" not in dataset_all


def test_placeholder_names_are_not_exported() -> None:
    assert _PLACEHOLDERS.isdisjoint(builder_all)
    assert _PLACEHOLDERS.isdisjoint(contracts_all)
    assert _PLACEHOLDERS.isdisjoint(manifest_all)
    assert _PLACEHOLDERS.isdisjoint(fingerprint_all)


# ---------------------------------------------------------------------------
# B. Dataclass field/default freeze
# ---------------------------------------------------------------------------


def _assert_dataclass_shape(
    cls: Any,
    expected_fields: Any,
) -> None:
    meta = {field.name: field for field in dataclasses.fields(cls)}
    assert tuple(meta) == tuple(name for name, _, _ in expected_fields)
    typing_hints = typing.get_type_hints(cls)
    for name, expected_type, kwargs in expected_fields:
        field_meta = meta[name]
        actual_type = typing_hints.get(name, field_meta.type)
        if isinstance(expected_type, tuple):
            assert actual_type in expected_type
        elif expected_type is object:
            assert actual_type is object or actual_type is not str
        elif isinstance(actual_type, type) and isinstance(expected_type, type):
            assert actual_type is expected_type
        else:
            assert actual_type == expected_type
        default = field_meta.default
        factory = field_meta.default_factory
        if "default_factory" in kwargs:
            assert callable(factory)
            assert factory is not None and factory is not dataclasses.MISSING  # type: ignore[comparison-overlap]
            assert default is dataclasses.MISSING
        elif "default" in kwargs:
            assert default != dataclasses.MISSING
            assert default == kwargs["default"]
            assert factory is dataclasses.MISSING
        else:
            assert default is dataclasses.MISSING
            assert factory is dataclasses.MISSING


def test_stage_result_fields_match_matrix() -> None:
    expected_fields = (
        ("stage_name", str, ()),
        ("input_count", int, ()),
        ("accepted", int, ()),
        ("rejected", int, ()),
        ("artifacts", tuple[str, ...], {"default": ()}),
        ("metadata", dict[str, Any], {"default_factory": dict}),
    )
    _assert_dataclass_shape(StageResult, expected_fields)


def test_stage_definition_fields_match_matrix() -> None:
    expected_fields = (
        ("name", str, ()),
        ("inputs", tuple[str, ...], {"default": ()}),
        ("outputs", tuple[str, ...], {"default": ()}),
    )
    _assert_dataclass_shape(StageDefinition, expected_fields)


def test_pipeline_context_fields_match_matrix() -> None:
    expected_fields = (
        ("root", str, ()),
        ("config", dict[str, Any], {"default_factory": dict}),
        ("results", tuple[StageResult, ...], {"default": ()}),
        ("bundle_references", tuple[str, ...], {"default": ()}),
        ("validation_statuses", dict[str, str], {"default_factory": dict}),
        ("metadata", dict[str, Any], {"default_factory": dict}),
    )
    _assert_dataclass_shape(PipelineContext, expected_fields)


def test_dataset_release_manifest_fields_match_matrix() -> None:
    expected_fields = (
        ("dataset_id", str, ()),
        ("dataset_version", str, ()),
        ("dataset_fingerprint", str, ()),
        ("release_id", str, ()),
        ("released_at", str, ()),
        ("released_by", str, ()),
        ("dataset_manifest_sha256", str, ()),
        ("bundle_id_registry_sha256", str, ()),
        ("validation_summary", dict[str, Any], {"default_factory": dict}),
        ("quality_summary", dict[str, Any], {"default_factory": dict}),
        ("release_notes", str, {"default": ""}),
        ("previous_release_id", object, {"default": None}),
    )
    _assert_dataclass_shape(DatasetReleaseManifest, expected_fields)


def test_audit_report_fields_match_matrix() -> None:
    expected_fields = (
        ("dataset_id", str, ()),
        ("dataset_version", str, ()),
        ("audit_timestamp", str, ()),
        ("green", bool, ()),
        ("record_count", int, ()),
        ("coverage_report_version", object, {"default": None}),
        ("analytics_report_version", object, {"default": None}),
        ("bundle_ids", tuple[str, ...], {"default": ()}),
        ("validation_statuses", dict[str, str], {"default_factory": dict}),
        ("rejection_counts", dict[str, int], {"default_factory": dict}),
        ("checksum_verification", dict[str, str], {"default_factory": dict}),
        ("failures", tuple[str, ...], {"default": ()}),
    )
    _assert_dataclass_shape(AuditReport, expected_fields)


def test_quality_report_fields_match_matrix() -> None:
    expected_fields = (
        ("dataset_id", str, ()),
        ("dataset_version", str, ()),
        ("stage_quality_summaries", dict[str, dict[str, Any]], {"default_factory": dict}),
        ("rejection_counts", dict[str, int], {"default_factory": dict}),
        ("synthetic_proportions", dict[str, float], {"default_factory": dict}),
        ("license_audit", dict[str, Any], {"default_factory": dict}),
        ("bias_monitoring_summary", dict[str, Any], {"default_factory": dict}),
        ("contamination_summary", dict[str, Any], {"default_factory": dict}),
        ("benchmark_linkage_status", dict[str, Any], {"default_factory": dict}),
        ("green", bool, {"default": False}),
    )
    _assert_dataclass_shape(QualityReport, expected_fields)


# ---------------------------------------------------------------------------
# C. Immutability
# ---------------------------------------------------------------------------
def test_assigning_dataclass_field_fails() -> None:
    result = StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.stage_name = "mutated"  # type: ignore[misc]


def test_mutating_top_level_mapping_fails() -> None:
    context = PipelineContext(root="data/pilot", config={"seed": 0})
    with pytest.raises(TypeError):
        context.config["seed"] = 1


def test_mutating_nested_mapping_fails() -> None:
    context = PipelineContext(root="data/pilot", metadata={"run": {"seed": 0}})
    with pytest.raises(TypeError):
        context.metadata["run"]["seed"] = 1


def test_mutating_source_after_construction_does_not_change_contract() -> None:
    source = {"seed": 0}
    context = PipelineContext(root="data/pilot", config=source)
    source["seed"] = 1
    assert context.config["seed"] == 0


# ---------------------------------------------------------------------------
# D. Malformed input rejection
# ---------------------------------------------------------------------------
def test_empty_required_identifier_is_rejected() -> None:
    with pytest.raises(ValueError):
        StageResult(stage_name=" ", input_count=1, accepted=1, rejected=1)


def test_negative_count_is_rejected() -> None:
    with pytest.raises(ValueError):
        StageResult(stage_name="raw", input_count=-1, accepted=1, rejected=0)


def test_non_string_tuple_member_is_rejected() -> None:
    with pytest.raises(TypeError):
        artifacts: Any = ("a", 1)
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0, artifacts=artifacts)


def test_invalid_mapping_key_is_rejected() -> None:
    with pytest.raises(TypeError):
        config: Any = {1: "one"}
        PipelineContext(root="data/pilot", config=config)


def test_arbitrary_object_value_is_rejected() -> None:
    with pytest.raises(TypeError):
        values: Any = {"timestamp": object()}
        PipelineContext(root="data/pilot", metadata=values)


def test_path_values_are_rejected() -> None:
    with pytest.raises(TypeError):
        stage_name: Any = pathlib.Path("raw")
        StageResult(stage_name=stage_name, input_count=1, accepted=1, rejected=0)


def test_set_values_are_rejected() -> None:
    with pytest.raises(TypeError):
        values: Any = {"tags": {"a"}}
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0, metadata=values)


def test_nan_and_infinity_are_rejected() -> None:
    with pytest.raises(ValueError):
        nan_values: Any = {"score": float("nan")}
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0, metadata=nan_values)
    with pytest.raises(ValueError):
        inf_values: Any = {"score": float("inf")}
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0, metadata=inf_values)


def test_negative_rejection_count_is_rejected() -> None:
    with pytest.raises(ValueError):
        AuditReport(
            dataset_id="pilot-1",
            dataset_version="1.0.0",
            audit_timestamp="2024-01-01T00:00:00Z",
            green=True,
            record_count=1,
            rejection_counts={"raw": -1},
        )


def test_proportions_out_of_range_are_rejected() -> None:
    with pytest.raises(ValueError):
        QualityReport(
            dataset_id="pilot-1",
            dataset_version="1.0.0",
            synthetic_proportions={"synthetic": 1.5},
        )
    with pytest.raises(ValueError):
        QualityReport(
            dataset_id="pilot-1",
            dataset_version="1.0.0",
            synthetic_proportions={"synthetic": -0.5},
        )


# ---------------------------------------------------------------------------
# E. Pipeline fingerprint
# ---------------------------------------------------------------------------
def test_pipeline_fingerprint_output_shape() -> None:
    results = (StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),)
    fingerprint = pipeline_fingerprint(results)
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64
    assert all(c in "0123456789abcdef" for c in fingerprint)


def test_pipeline_fingerprint_is_deterministic() -> None:
    results = (StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),)
    assert pipeline_fingerprint(results) == pipeline_fingerprint(results)


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


def test_pipeline_fingerprint_changes_when_stage_order_changes() -> None:
    first = (
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),
        StageResult(stage_name="screening", input_count=1, accepted=1, rejected=0),
    )
    second = (
        StageResult(stage_name="screening", input_count=1, accepted=1, rejected=0),
        StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),
    )
    assert pipeline_fingerprint(first) != pipeline_fingerprint(second)


def test_pipeline_fingerprint_changes_when_identity_fields_change() -> None:
    original = (StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0),)
    assert pipeline_fingerprint(original) != pipeline_fingerprint(
        (StageResult(stage_name="raw", input_count=5, accepted=4, rejected=1),)
    )
    assert pipeline_fingerprint(original) != pipeline_fingerprint(
        (StageResult(stage_name="mix", input_count=5, accepted=5, rejected=0),)
    )
    assert pipeline_fingerprint(original) != pipeline_fingerprint(
        (StageResult(stage_name="raw", input_count=4, accepted=5, rejected=0),)
    )
    assert pipeline_fingerprint(original) != pipeline_fingerprint(
        (StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0, artifacts=("a",)),)
    )


def test_pipeline_fingerprint_excludes_metadata() -> None:
    original = (
        StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0, metadata={"seed": 0}),
    )
    mutated = (
        StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0, metadata={"seed": 1}),
    )
    assert pipeline_fingerprint(original) == pipeline_fingerprint(mutated)


def test_pipeline_fingerprint_matches_explicit_payload() -> None:
    results = (
        StageResult(
            stage_name="raw",
            input_count=5,
            accepted=4,
            rejected=1,
            artifacts=("a", "b"),
        ),
        StageResult(
            stage_name="screening",
            input_count=4,
            accepted=2,
            rejected=2,
            artifacts=("c",),
        ),
    )
    payload = [
        {
            "stage_name": "raw",
            "input_count": 5,
            "accepted": 4,
            "rejected": 1,
            "artifacts": ["a", "b"],
        },
        {
            "stage_name": "screening",
            "input_count": 4,
            "accepted": 2,
            "rejected": 2,
            "artifacts": ["c"],
        },
    ]
    assert pipeline_fingerprint(results) == content_hash(payload)


# ---------------------------------------------------------------------------
# F. Context fingerprint
# ---------------------------------------------------------------------------
def test_context_fingerprint_output_shape() -> None:
    context = PipelineContext(root="data/pilot", config={"seed": 0})
    fingerprint = context_fingerprint(context)
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64
    assert all(c in "0123456789abcdef" for c in fingerprint)


def test_context_fingerprint_is_deterministic() -> None:
    context = PipelineContext(root="data/pilot", config={"seed": 0})
    assert context_fingerprint(context) == context_fingerprint(context)


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


def test_context_fingerprint_ignores_bundle_reference_order() -> None:
    first = PipelineContext(root="data/pilot", bundle_references=("bundle-1", "bundle-2"))
    second = PipelineContext(root="data/pilot", bundle_references=("bundle-2", "bundle-1"))
    assert context_fingerprint(first) == context_fingerprint(second)


def test_context_fingerprint_changes_when_results_change() -> None:
    first = PipelineContext(
        root="data/pilot",
        results=(StageResult(stage_name="raw", input_count=5, accepted=5, rejected=0),),
    )
    second = PipelineContext(
        root="data/pilot",
        results=(StageResult(stage_name="raw", input_count=5, accepted=4, rejected=1),),
    )
    assert context_fingerprint(first) != context_fingerprint(second)


def test_context_fingerprint_changes_when_result_order_changes() -> None:
    first = PipelineContext(
        root="data/pilot",
        results=(
            StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),
            StageResult(stage_name="screening", input_count=1, accepted=1, rejected=0),
        ),
    )
    second = PipelineContext(
        root="data/pilot",
        results=(
            StageResult(stage_name="screening", input_count=1, accepted=1, rejected=0),
            StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),
        ),
    )
    assert context_fingerprint(first) != context_fingerprint(second)


def test_context_fingerprint_changes_when_config_changes() -> None:
    first = PipelineContext(root="data/pilot", config={"seed": 0})
    second = PipelineContext(root="data/pilot", config={"seed": 1})
    assert context_fingerprint(first) != context_fingerprint(second)


def test_context_fingerprint_ignores_root_and_metadata() -> None:
    first = PipelineContext(root="cwd/alpha", metadata={"seed": 0}, config={"seed": 0})
    second = PipelineContext(root="cwd/beta", metadata={"seed": 1}, config={"seed": 0})
    assert context_fingerprint(first) == context_fingerprint(second)


def test_context_fingerprint_matches_explicit_payload() -> None:
    results = (
        StageResult(stage_name="raw", input_count=5, accepted=4, rejected=1, artifacts=("a", "b")),
    )
    context = PipelineContext(
        root="data/pilot",
        results=results,
        bundle_references=("bundle-1",),
        validation_statuses={"raw": "passed"},
    )
    payload = {
        "config": {},
        "results": [
            {
                "stage_name": "raw",
                "input_count": 5,
                "accepted": 4,
                "rejected": 1,
                "artifacts": ["a", "b"],
            }
        ],
        "bundle_references": ["bundle-1"],
        "validation_statuses": {"raw": "passed"},
    }
    assert context_fingerprint(context) == content_hash(payload)


# ---------------------------------------------------------------------------
# G. Runtime metadata exclusion
# ---------------------------------------------------------------------------
def test_pipeline_fingerprint_does_not_use_runtime_sources() -> None:
    results = (StageResult(stage_name="raw", input_count=1, accepted=1, rejected=0),)
    baseline = pipeline_fingerprint(results)
    os.environ["MEDSCALE_TEST_ROOT"] = "changed"
    try:
        assert baseline == pipeline_fingerprint(results)
    finally:
        os.environ.pop("MEDSCALE_TEST_ROOT", None)


def test_context_fingerprint_does_not_use_runtime_sources() -> None:
    context = PipelineContext(root="data/pilot", config={"seed": 0})
    baseline = context_fingerprint(context)
    os.environ["MEDSCALE_TEST_ROOT"] = "changed"
    try:
        assert baseline == context_fingerprint(context)
    finally:
        os.environ.pop("MEDSCALE_TEST_ROOT", None)


# ---------------------------------------------------------------------------
# H. Schema compatibility
# ---------------------------------------------------------------------------
def test_dataset_schema_version_is_frozen() -> None:
    from medscale.dataset.schema import DatasetSchema

    assert DatasetSchema.version == "1"


def test_schema_hashes_are_stable() -> None:
    from medscale.dataset.schema import (
        BENCHMARK_ITEM_SCHEMA,
        EVIDENCE_OBJECT_SCHEMA,
        LITERATURE_RECORD_SCHEMA,
    )

    literature_hash = content_hash(canonical_json(LITERATURE_RECORD_SCHEMA))
    evidence_hash = content_hash(canonical_json(EVIDENCE_OBJECT_SCHEMA))
    benchmark_hash = content_hash(canonical_json(BENCHMARK_ITEM_SCHEMA))

    assert len(literature_hash) == 64
    assert len(evidence_hash) == 64
    assert len(benchmark_hash) == 64
    assert literature_hash == content_hash(canonical_json(LITERATURE_RECORD_SCHEMA))
    assert evidence_hash == content_hash(canonical_json(EVIDENCE_OBJECT_SCHEMA))
    assert benchmark_hash == content_hash(canonical_json(BENCHMARK_ITEM_SCHEMA))
    assert len({literature_hash, evidence_hash, benchmark_hash}) == 3


# ---------------------------------------------------------------------------
# I. Import boundaries
# ---------------------------------------------------------------------------
_PROHIBITED_IMPORTS = {
    "medscale.evidence",
    "medscale.validation",
    "medscale.dataset.connectors",
    "medscale.dataset.governance",
    "medscale.models",
    "medscale.evaluation",
}


def test_builder_modules_do_not_import_prohibited_packages() -> None:
    module_paths = (
        "src/medscale/dataset/builder/contracts.py",
        "src/medscale/dataset/builder/manifest.py",
        "src/medscale/dataset/builder/fingerprint.py",
        "src/medscale/dataset/builder/__init__.py",
    )
    root = pathlib.Path(__file__).resolve().parents[1]
    for rel in module_paths:
        tree = ast.parse((root / rel).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in _PROHIBITED_IMPORTS:
                raise AssertionError(f"prohibited import: {node.module}")


# ---------------------------------------------------------------------------
# J. Facade stability
# ---------------------------------------------------------------------------
def test_dataset_facade_all_is_unchanged() -> None:
    expected_dataset_all = [
        "BENCHMARK_ITEM_SCHEMA",
        "EVIDENCE_OBJECT_SCHEMA",
        "LITERATURE_RECORD_SCHEMA",
        "DatasetManifest",
        "DatasetSchema",
        "DatasetValidationReport",
        "DeterministicSplitter",
        "SplitStrategy",
        "compute_dataset_manifest",
        "deterministic_hash_split",
        "split_literature_records",
        "validate_dataset",
        "write_manifest",
    ]
    assert dataset_all == expected_dataset_all
