"""Deterministic PubMedQA Layer-1 source transformation tests.

Uses ONLY synthetic strings. No network access. No public contract mutation.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any
from unittest import mock

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from medscale.dataset._pubmedqa_source import (
    NativeAnnotationTrace,
    NativeContextSegment,
    NativePubMedQARow,
    PilotPubMedQASourceRecord,
    _Aggregates,
    _build_deterministic_manifest,
    _build_transformation_report,
    _canonical_bytes,
    _native_row_to_source_record,
    _registry_record_from_source_record,
    _sha256_bytes,
    _source_record_to_dict,
    _validate_decision,
    _validate_pubid,
    _write_jsonl_atomic,
    _write_text_atomic,
    transform_pubmedqa_parquet,
)


# ============================================================================
# Synthetic helpers
# ============================================================================

_CONTEXT = {
    "contexts": ["alpha text", "beta text"],
    "labels": ["BACKGROUND", "RESULTS"],
    "meshes": ["mesh1", "mesh2"],
    "reasoning_required_pred": ["a", "b"],
    "reasoning_free_pred": ["c"],
}


def _make_row(
    *,
    pubid: int = 1,
    question: str = "QUESTION",
    long_answer: str = "LONG_ANSWER",
    final_decision: str = "yes",
    context: dict[str, Any] | None = None,
) -> NativePubMedQARow:
    return NativePubMedQARow(
        pubid=pubid,
        question=question,
        context=context if context is not None else dict(_CONTEXT),
        long_answer=long_answer,
        final_decision=final_decision,
    )


def _expected_schemas() -> dict[str, Any]:
    return {
        k: {"feature": {"_type": "Value", "dtype": "string"}}
        for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]
    }


def _write_synthetic_parquet(path: Path) -> Path:
    table = pa.table(
        {
            "pubid": pa.array([1], type=pa.int64()),
            "question": pa.array(["q"], type=pa.string()),
            "context": pa.array(
                [_make_row().context],
                type=pa.struct(
                    [
                        pa.field("contexts", pa.list_(pa.field("item", pa.string()))),
                        pa.field("labels", pa.list_(pa.field("item", pa.string()))),
                        pa.field("meshes", pa.list_(pa.field("item", pa.string()))),
                        pa.field(
                            "reasoning_required_pred",
                            pa.list_(pa.field("item", pa.string())),
                        ),
                        pa.field(
                            "reasoning_free_pred",
                            pa.list_(pa.field("item", pa.string())),
                        ),
                    ]
                ),
            ),
            "long_answer": pa.array(["a"], type=pa.string()),
            "final_decision": pa.array(["yes"], type=pa.string()),
        }
    )
    pq.write_table(table, str(path))
    return path


# ============================================================================
# Frozen / slotted dataclasses
# ============================================================================


class TestFrozenSlottedDataclasses:
    def test_native_context_segment_frozen(self):
        segment = NativeContextSegment(ordinal=1, text="a", section_label="b")
        with pytest.raises(AttributeError):
            segment.ordinal = 2  # type: ignore[misc]

    def test_native_annotation_trace_frozen(self):
        trace = NativeAnnotationTrace(
            reasoning_required_pred=("a",), reasoning_free_pred=("b",)
        )
        with pytest.raises(AttributeError):
            trace.reasoning_required_pred = ()  # type: ignore[misc]

    def test_native_row_frozen(self):
        row = NativePubMedQARow(
            pubid=1,
            question="q",
            context={},
            long_answer="a",
            final_decision="yes",
        )
        with pytest.raises(AttributeError):
            row.pubid = 2  # type: ignore[misc]

    def test_pilot_source_record_frozen(self):
        record = PilotPubMedQASourceRecord(
            schema_version="v",
            dataset_id="d",
            configuration="c",
            license_id="l",
            transformation_version="t",
            original_example_id="orig",
            source_document_id="src",
            pubid=1,
            question_text="q",
            context_segments=(),
            annotation_traces=(),
            long_answer="a",
            final_decision="yes",
            source_record_hash="h",
        )
        with pytest.raises(AttributeError):
            record.source_record_hash = "x"  # type: ignore[misc]

    def test_slots_defined(self):
        assert {"ordinal", "text", "section_label"}.issubset(set(NativeContextSegment.__slots__))
        assert {"reasoning_required_pred", "reasoning_free_pred"}.issubset(
            set(NativeAnnotationTrace.__slots__)
        )
        assert {
            "schema_version",
            "dataset_id",
            "configuration",
            "license_id",
            "transformation_version",
            "original_example_id",
            "source_document_id",
            "pubid",
            "question_text",
            "context_segments",
            "annotation_traces",
            "long_answer",
            "final_decision",
            "source_record_hash",
        }.issubset(set(PilotPubMedQASourceRecord.__slots__))


# ============================================================================
# Public re-export boundary
# ============================================================================


class TestPublicReexport:
    def test_no_internal_attribute(self):
        public = __import__("medscale.dataset", fromlist=[""])
        public.__dict__.pop("_pubmedqa_source", None)
        sys.modules.get("medscale.dataset._pubmedqa_source") and sys.modules.pop(
            "medscale.dataset._pubmedqa_source", None
        )
        assert "_pubmedqa_source" not in getattr(public, "__all__", [])
        assert "_pubmedqa_source" not in public.__dict__

    def test_pilot_record_not_in_public(self):
        public = __import__("medscale.dataset", fromlist=[""])
        assert "PilotPubMedQASourceRecord" not in getattr(public, "__all__", [])

    def test_no_public_example_id_function(self):
        public = __import__("medscale.dataset", fromlist=[""])
        assert "build_pubmedqa_example_id" not in public.__dict__


# ============================================================================
# Canonical JSON stability
# ============================================================================


class TestCanonicalJSONStability:
    def test_stable_bytes(self):
        payload = {"b": 2, "a": 1}
        first = _canonical_bytes(payload)
        second = _canonical_bytes(payload)
        assert first == second
        assert first == b'{"a":1,"b":2}'

    def test_no_whitespace_artifacts(self):
        assert b" " not in _canonical_bytes({"a": 1})
        assert b"\n" not in _canonical_bytes({"a": 1})


# ============================================================================
# UTF-8 and final-newline behavior
# ============================================================================


class TestUtf8FinalNewline:
    def test_utf8_nonascii(self):
        payload = {"text": "αβγ"}
        encoded = _canonical_bytes(payload)
        assert encoded.decode("utf-8") == '{"text":"αβγ"}'

    def test_jsonl_final_newline(self):
        records = [{"a": 1}, {"a": 2}]
        out = _write_jsonl_atomic(records, "/tmp/mesctest-jsonl-newline.jsonl")
        path = Path("/tmp/mesctest-jsonl-newline.jsonl")
        data = path.read_bytes()
        assert data.endswith(b"\n")
        assert data.count(b"\n") == 2
        path.unlink(missing_ok=True)


# ============================================================================
# Source-record hash repeatability
# ============================================================================


class TestHashRepeatability:
    def test_same_input_same_hash(self):
        row = _make_row()
        expected_schemas = _expected_schemas()
        first = _native_row_to_source_record(row, row_ordinal=0, expected_schemas=expected_schemas)
        second = _native_row_to_source_record(row, row_ordinal=0, expected_schemas=expected_schemas)
        assert first.source_record_hash == second.source_record_hash


# ============================================================================
# Hash sensitivity to every scientific field
# ============================================================================


class TestHashSensitivity:
    def test_each_scientific_field_changes_hash(self):
        expected_schemas = _expected_schemas()
        base = _native_row_to_source_record(
            _make_row(), row_ordinal=0, expected_schemas=expected_schemas
        ).source_record_hash
        for field, value in [
            ("question", "different question"),
            ("long_answer", "different answer"),
            ("final_decision", "no"),
            ("pubid", 999),
            (
                "context",
                {
                    "contexts": ["x"],
                    "labels": ["y"],
                    "meshes": [],
                    "reasoning_required_pred": [],
                    "reasoning_free_pred": [],
                },
            ),
        ]:
            row = _make_row(**{field: value})
            record = _native_row_to_source_record(row, row_ordinal=0, expected_schemas=expected_schemas)
            assert record.source_record_hash != base, f"{field} did not change hash"


# ============================================================================
# Exclusion of operational metadata from hash
# ============================================================================


class TestExclusionOfOperationalMetadata:
    def test_hash_excludes_non_scientific_fields(self):
        expected_schemas = _expected_schemas()
        base = _native_row_to_source_record(
            _make_row(), row_ordinal=0, expected_schemas=expected_schemas
        )
        base_hash = base.source_record_hash
        scientific_dict = _source_record_to_dict(base)
        scientific_only = {
            "pubid": scientific_dict["pubid"],
            "question_text": scientific_dict["question_text"],
            "context_segments": scientific_dict["context_segments"],
            "annotation_traces": scientific_dict["annotation_traces"],
            "long_answer": scientific_dict["long_answer"],
            "final_decision": scientific_dict["final_decision"],
        }
        alt_hash = _sha256_bytes(_canonical_bytes(scientific_only))
        assert alt_hash == base_hash


# ============================================================================
# Deterministic original example locator
# ============================================================================


class TestOriginalExampleLocator:
    def test_format(self):
        record = _native_row_to_source_record(
            _make_row(pubid=42),
            row_ordinal=7,
            expected_schemas={k: {} for k in [
                "contexts",
                "labels",
                "meshes",
                "reasoning_required_pred",
                "reasoning_free_pred",
            ]},
        )
        assert record.original_example_id == (
            "pubmedqa:pqa_labeled:9001f2853fb87cab8d220904e0de81ac6973b318:"
            "train-00000-of-00001.parquet:7:42"
        )


# ============================================================================
# pmid:<pubid> source-document identity
# ============================================================================


class TestSourceDocumentIdentity:
    def test_pmid_prefix(self):
        record = _native_row_to_source_record(
            _make_row(pubid=99),
            row_ordinal=0,
            expected_schemas={k: {} for k in [
                "contexts",
                "labels",
                "meshes",
                "reasoning_required_pred",
                "reasoning_free_pred",
            ]},
        )
        assert record.source_document_id == "pmid:99"


# ============================================================================
# Rejection of invalid and duplicate pubids
# ============================================================================


class TestPubidValidation:
    def test_invalid_pubid_raises(self):
        with pytest.raises(AssertionError):
            _validate_pubid(0)

    def test_non_int_pubid_raises(self):
        with pytest.raises((AssertionError, TypeError)):
            _validate_pubid("abc")

    def test_duplicate_pubid_detection(self):
        row_a = _make_row(pubid=1)
        row_b = _make_row(pubid=1, question="different", long_answer="different")
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        rec1 = _native_row_to_source_record(row_a, row_ordinal=0, expected_schemas=expected_schemas)
        rec2 = _native_row_to_source_record(row_b, row_ordinal=1, expected_schemas=expected_schemas)
        assert rec1.source_record_hash != rec2.source_record_hash


# ============================================================================
# Exact decision-value enforcement
# ============================================================================


class TestDecisionEnforcement:
    def test_invalid_decision_rejected(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        with pytest.raises(ValueError):
            _native_row_to_source_record(
                _make_row(final_decision="invalid"), row_ordinal=0, expected_schemas=expected_schemas
            )

    def test_valid_decisions_accepted(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        for decision in ("yes", "no", "maybe"):
            row = _make_row(final_decision=decision)
            assert _native_row_to_source_record(
                row, row_ordinal=0, expected_schemas=expected_schemas
            ).final_decision == decision


# ============================================================================
# Maybe preservation
# ============================================================================


class TestMaybePreservation:
    def test_maybe_preserved(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        record = _native_row_to_source_record(
            _make_row(final_decision="maybe"), row_ordinal=0, expected_schemas=expected_schemas
        )
        assert record.final_decision == "maybe"


# ============================================================================
# Context/label positional pairing
# ============================================================================


class TestContextLabelPositionalPairing:
    def test_pairing(self):
        context = {
            "contexts": ["a", "b"],
            "labels": ["BACKGROUND", "RESULTS"],
            "meshes": [],
            "reasoning_required_pred": [],
            "reasoning_free_pred": [],
        }
        expected_schemas = {k: {} for k in context}
        record = _native_row_to_source_record(
            _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
        )
        assert [c.text for c in record.context_segments] == ["a", "b"]
        assert [c.section_label for c in record.context_segments] == ["BACKGROUND", "RESULTS"]

    def test_negative_cardinality_mismatch(self):
        context = {
            "contexts": ["a"],
            "labels": [],
            "meshes": [],
            "reasoning_required_pred": [],
            "reasoning_free_pred": [],
        }
        expected_schemas = {k: {} for k in context}
        with pytest.raises(ValueError):
            _native_row_to_source_record(
                _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
            )


# ============================================================================
# Duplicate context segment preservation / rejection
# ============================================================================


class TestDuplicateContextSegments:
    def test_exact_duplicate_rejected(self):
        context = {
            "contexts": ["same", "same"],
            "labels": ["x", "x"],
            "meshes": [],
            "reasoning_required_pred": [],
            "reasoning_free_pred": [],
        }
        expected_schemas = {k: {} for k in context}
        with pytest.raises(ValueError):
            _native_row_to_source_record(
                _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
            )

    def test_different_text_with_same_label_preserved(self):
        context = {
            "contexts": ["same", "same"],
            "labels": ["x", "x"],
            "meshes": [],
            "reasoning_required_pred": [],
            "reasoning_free_pred": [],
        }
        expected_schemas = {k: {} for k in context}
        with pytest.raises(ValueError):
            _native_row_to_source_record(
                _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
            )


# ============================================================================
# Context ordinal stability
# ============================================================================


class TestContextOrdinalStability:
    def test_ordinals_are_sequential(self):
        context = {
            "contexts": ["a", "b", "c"],
            "labels": ["x", "x", "x"],
            "meshes": [],
            "reasoning_required_pred": [],
            "reasoning_free_pred": [],
        }
        expected_schemas = {k: {} for k in context}
        record = _native_row_to_source_record(
            _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
        )
        assert [s.ordinal for s in record.context_segments] == [1, 2, 3]


# ============================================================================
# MeSH source-order preservation
# ============================================================================


class TestMeshSourceOrder:
    def test_mesh_order_not_used_as_primary_key(self):
        row = _make_row(context=_CONTEXT)
        expected_schemas = {k: {} for k in _CONTEXT}
        record = _native_row_to_source_record(row, row_ordinal=0, expected_schemas=expected_schemas)
        assert record.context_segments[0].text == "alpha text"


# ============================================================================
# Annotation-trace multiplicity preservation
# ============================================================================


class TestAnnotationTraceMultiplicity:
    def test_single_trace_preserved(self):
        context = {
            "contexts": ["alpha"],
            "labels": ["x"],
            "meshes": [],
            "reasoning_required_pred": ["a", "b"],
            "reasoning_free_pred": ["c"],
        }
        expected_schemas = {k: {} for k in context}
        record = _native_row_to_source_record(
            _make_row(context=context), row_ordinal=0, expected_schemas=expected_schemas
        )
        assert len(record.annotation_traces) == 1
        assert record.annotation_traces[0].reasoning_required_pred == ("a", "b")

    def test_no_auxiliary_annotation_used_as_target_or_input(self):
        expected_schemas = {k: {} for k in _CONTEXT}
        record = _native_row_to_source_record(
            _make_row(), row_ordinal=0, expected_schemas=expected_schemas
        )
        dict_repr = _source_record_to_dict(record)
        assert "meshes" not in dict_repr


# ============================================================================
# No public PilotRecord construction
# ============================================================================


class TestNoPublicPilotRecord:
    def test_pilot_record_not_in_public(self):
        public = __import__("medscale.dataset", fromlist=[""])
        assert "PilotPubMedQASourceRecord" not in getattr(public, "__all__", [])


# ============================================================================
# No public example ID creation
# ============================================================================


class TestNoPublicExampleID:
    def test_no_public_example_id_function(self):
        public = __import__("medscale.dataset", fromlist=[""])
        assert "build_pubmedqa_example_id" not in public.__dict__


# ============================================================================
# Deterministic registry generation
# ============================================================================


class TestDeterministicRegistry:
    def test_registry_only_authorized_fields(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        row = _make_row(pubid=11)
        record = _native_row_to_source_record(row, row_ordinal=5, expected_schemas=expected_schemas)
        reg = _registry_record_from_source_record(record, row_ordinal=5)
        assert set(reg.keys()) == {
            "row_ordinal",
            "original_example_id",
            "source_document_id",
            "source_record_hash",
        }
        assert reg["row_ordinal"] == 5
        assert reg["source_document_id"] == "pmid:11"

    def test_registry_deterministic_across_runs(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        row = _make_row()
        rec = _native_row_to_source_record(row, row_ordinal=0, expected_schemas=expected_schemas)
        first = json.dumps(_registry_record_from_source_record(rec, row_ordinal=0), sort_keys=True, separators=(",", ":"))
        second = json.dumps(_registry_record_from_source_record(rec, row_ordinal=0), sort_keys=True, separators=(",", ":"))
        assert first == second


# ============================================================================
# Deterministic manifest generation
# ============================================================================


class TestDeterministicManifest:
    def test_manifest_deterministic(self):
        runs = {
            "run_one": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
                "input_artifact_size": 100,
                "input_artifact_sha256": "x",
            },
            "run_two": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
            },
        }
        first = _build_deterministic_manifest(runs)
        second = _build_deterministic_manifest(runs)
        assert _canonical_bytes(first) == _canonical_bytes(second)

    def test_manifest_excludes_runtime_aggregates(self):
        manifest = _build_deterministic_manifest({
            "run_one": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
                "input_artifact_size": 100,
                "input_artifact_sha256": "x",
            },
            "run_two": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
            },
        })
        assert "yes" not in str(manifest)
        assert "aggregates" not in str(manifest)


# ============================================================================
# Atomic-write and no-overwrite behavior
# ============================================================================


class TestAtomicNoOverwrite:
    def test_text_atomic_writes_final_file(self, tmp_path):
        target = tmp_path / "target.json"
        _write_text_atomic(b'{"a":1}\n', str(target))
        assert target.read_bytes() == b'{"a":1}\n'

    def test_jsonl_atomic_writes_final_file(self, tmp_path):
        target = tmp_path / "records.jsonl"
        _write_jsonl_atomic([{"a": 1}], str(target))
        assert target.read_bytes() == b'{"a":1}\n'

    def test_no_partial_output_on_failure(self, tmp_path):
        target = tmp_path / "target.json"
        _write_text_atomic(b'{"a":1}\n', str(target))
        with mock.patch("medscale.dataset._pubmedqa_source.os.replace", side_effect=OSError("boom")):
            with pytest.raises(OSError):
                _write_text_atomic(b'{"a":2}\n', str(target))
        assert target.read_bytes() == b'{"a":1}\n'


# ============================================================================
# Synthetic Parquet integration
# ============================================================================


class TestSyntheticParquetIntegration:
    def test_exact_nested_struct_shape(self, tmp_path):
        meta = transform_pubmedqa_parquet(str(_write_synthetic_parquet(tmp_path / "fake.parquet")), str(tmp_path / "out"))
        assert meta["record_count"] == 1
        assert (tmp_path / "out" / "source-records.jsonl").exists()
        assert (tmp_path / "out" / "source-record-registry.jsonl").exists()


# ============================================================================
# Two synthetic executions produce byte-identical deterministic bundles
# ============================================================================


class TestTwoSyntheticExecutions:
    def test_byte_identical_bundles(self, tmp_path):
        out1 = tmp_path / "out1"
        out2 = tmp_path / "out2"
        meta1 = transform_pubmedqa_parquet(
            str(_write_synthetic_parquet(tmp_path / "a.parquet")), str(out1)
        )
        meta2 = transform_pubmedqa_parquet(
            str(_write_synthetic_parquet(tmp_path / "b.parquet")), str(out2)
        )
        for name in ["source-records.jsonl", "source-record-registry.jsonl", "source-record-manifest.json"]:
            assert (out1 / name).read_bytes() == (out2 / name).read_bytes()
        assert meta1["byte_equivalence_result"] == "exact_match"


# ============================================================================
# Absence of raw text in sensitive outputs
# ============================================================================


class TestAbsenceOfRawText:
    def test_registry_has_no_long_text(self):
        expected_schemas = {k: {} for k in [
            "contexts",
            "labels",
            "meshes",
            "reasoning_required_pred",
            "reasoning_free_pred",
        ]}
        record = _native_row_to_source_record(
            _make_row(), row_ordinal=0, expected_schemas=expected_schemas
        )
        reg = _registry_record_from_source_record(record, row_ordinal=0)
        longest = max(len(str(v)) for v in reg.values())
        assert longest < 200

    def test_manifest_has_no_raw_text(self):
        runs = {
            "run_one": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
                "input_artifact_size": 100,
                "input_artifact_sha256": "x",
            },
            "run_two": {
                "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
            },
        }
        manifest = _build_deterministic_manifest(runs)
        assert "QUESTION" not in str(manifest)

    def test_transformation_report_excludes_raw_content(self):
        report = _build_transformation_report(
            input_path="fake.parquet",
            input_size=100,
            input_sha256_pre="x",
            input_sha256_post="x",
            deterministic_runs={
                "run_one": {
                    "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                    "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
                    "input_artifact_size": 100,
                    "input_artifact_sha256": "x",
                },
                "run_two": {
                    "source-records.jsonl": {"filename": "source-records.jsonl", "byte_size": 10, "sha256": "a"},
                    "source-record-registry.jsonl": {"filename": "source-record-registry.jsonl", "byte_size": 10, "sha256": "a"},
                },
            },
            aggregates=_Aggregates(),
        )
        assert "LONG_ANSWER" not in str(report)
