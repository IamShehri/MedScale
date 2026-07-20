"""P01-03F PubMedQA bundle validation tests."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from medscale.dataset._pubmedqa_validation import (
    AggregateValidation,
    ValidationIssue,
    _load_jsonl,
    _validate_local_report,
    _validate_registry,
    _validate_source_records,
    validate_pubmedqa_bundle,
)


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _minimal_record(record_index: int = 0) -> dict[str, Any]:
    scientific = {
        "schema_version": "mesc-pubmedqa-source/1",
        "dataset_id": "qiaojin/PubMedQA",
        "dataset_revision": "9001f2853fb87cab8d220904e0de81ac6973b318",
        "configuration": "pqa_labeled",
        "original_example_id": (
            "pubmedqa:pqa_labeled:9001f2853fb87cab8d220904e0de81ac6973b318"
            f":train-00000-of-00001.parquet:{record_index}:12345"
        ),
        "source_document_id": "pmid:12345",
        "pubid": "12345",
        "question": "q",
        "context_segments": [{"ordinal": 0, "text": "text", "section_label": "BACKGROUND"}],
        "mesh_terms": ["mesh"],
        "long_answer": "answer",
        "final_decision": "yes",
        "reasoning_required_pred": ["r"],
        "reasoning_free_pred": ["f"],
        "license_id": "PubMedQA-PQA-L",
    }
    return {
        "record": scientific,
        "source_record_hash": _sha256(_canonical(scientific)),
    }


def _minimal_manifest(record_count: int = 1) -> dict[str, Any]:
    return {
        "manifest_schema_version": "mesc-pubmedqa-manifest/1",
        "transformation_version": "mesc-pubmedqa-transform/1",
        "internal_source_record_schema_version": "mesc-pubmedqa-source/1",
        "dataset_identity": {
            "dataset_id": "qiaojin/PubMedQA",
            "configuration": "pqa_labeled",
            "revision": "9001f2853fb87cab8d220904e0de81ac6973b318",
            "license_id": "PubMedQA-PQA-L",
        },
        "source_artifact": {
            "repository_path": "train-00000-of-00001.parquet",
            "byte_size": 8,
            "sha256": _sha256(b"rawartifact"),
        },
        "record_count": record_count,
        "decision_counts": {"yes": 1, "no": 0, "maybe": 0, "unexpected": 0},
        "unique_pubid_count": record_count,
        "duplicate_pubid_count": 0,
        "unique_source_document_count": record_count,
        "unique_source_record_hash_count": record_count,
        "source_record_hash_collision_count": 0,
        "context_segment_aggregates": {"total": 1, "minimum": 1, "maximum": 1},
        "labels_context_cardinality_validation": "pass",
        "duplicate_preservation_policy": "preserve_duplicates",
        "public_pilot_record_status": "deferred",
        "public_example_id_status": "deferred",
        "p01_03f_status": "not_authorized",
    }


def _build_valid_bundle(tmp_path: Path, record_count: int = 1) -> tuple[Path, dict[str, Any]]:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    manifest = _minimal_manifest(record_count)
    records = []
    registry = []
    for i in range(record_count):
        rec = _minimal_record(i)
        records.append(rec)
        registry.append(
            {
                "row_ordinal": i,
                "original_example_id": rec["record"]["original_example_id"],
                "source_document_id": rec["record"]["source_document_id"],
                "source_record_hash": rec["source_record_hash"],
            }
        )
    _write(bundle / "source-records.jsonl", b"".join(_canonical(r) + b"\n" for r in records))
    _write(
        bundle / "source-record-registry.jsonl", b"".join(_canonical(r) + b"\n" for r in registry)
    )
    _write(bundle / "transformation-manifest.json", _canonical(manifest) + b"\n")
    _write(bundle / "transformation-run.local.json", _canonical({"status": "complete"}) + b"\n")
    return bundle, manifest


# ---------------------------------------------------------------------------
# Import isolation
# ---------------------------------------------------------------------------


class TestImportIsolation:
    def test_private_module_import_does_not_introduce_pyarrow(self) -> None:
        code = """
import sys
import medscale.dataset._pubmedqa_validation
polluted = [name for name in sys.modules if name == "pyarrow" or name.startswith("pyarrow.")]
raise SystemExit(1 if polluted else 0)
"""
        completed = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr

    def test_not_reexported_from_public_api(self) -> None:
        public = getattr(
            __import__("medscale.dataset", fromlist=["__all__"]),
            "__all__",
            [],
        )
        assert "_pubmedqa_validation" not in public
        assert "validate_pubmedqa_bundle" not in public


# ---------------------------------------------------------------------------
# Unit-level structure checks
# ---------------------------------------------------------------------------


class TestValidationIssue:
    def test_str_without_record(self) -> None:
        issue = ValidationIssue(field="x", message="bad", severity="error")
        assert str(issue) == "[error] x: bad"

    def test_str_with_record(self) -> None:
        issue = ValidationIssue(field="x", message="bad", severity="error", record_index=2)
        assert str(issue) == "[error] record[2] x: bad"

    def test_default_severity(self) -> None:
        issue = ValidationIssue(field="x", message="bad")
        assert issue.severity == "error"


# ---------------------------------------------------------------------------
# Aggregate validation
# ---------------------------------------------------------------------------


class TestAggregateValidation:
    def test_perfect_aggregate(self) -> None:
        aggregate = AggregateValidation(
            passed=True,
            failures=[],
            issues=[],
        )
        assert aggregate.passed is True


# ---------------------------------------------------------------------------
# Report schema and serialization
# ---------------------------------------------------------------------------


class TestValidationReport:
    def test_report_is_json_serializable(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        raw = tmp_path / "raw.parquet"
        raw.write_bytes(b"rawartifact")
        report = validate_pubmedqa_bundle(bundle, raw_artifact=raw, authorized=True)
        data = report.to_dict()
        json.dumps(data, sort_keys=True, ensure_ascii=False, allow_nan=False)

    def test_report_schema_version_present(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.schema_version == "mesc-pubmedqa-validation/1"

    def test_unauthorized_emits_warning(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=False)
        assert any(issue.field == "authorization" for issue in report.issues)


# ---------------------------------------------------------------------------
# Bundle boundary
# ---------------------------------------------------------------------------


class TestBundleBoundary:
    def test_missing_bundle_directory_raises(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            validate_pubmedqa_bundle(tmp_path / "missing", authorized=True)

    def test_exact_four_file_inventory_passes(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.bundle_inventory_match is True
        assert report.success is True

    def test_unexpected_fifth_file_detected(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "unexpected.txt").write_bytes(b"x")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("unexpected inventory" in issue.message for issue in report.issues)
        assert not report.success

    def test_missing_required_file_raises(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-record-registry.jsonl").unlink()
        with pytest.raises(FileNotFoundError):
            validate_pubmedqa_bundle(bundle, authorized=True)

    def test_bundle_mutation_count_zero_on_success(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        expected = {
            name: _sha256_file(bundle / name)
            for name in [
                "source-records.jsonl",
                "source-record-registry.jsonl",
                "transformation-manifest.json",
                "transformation-run.local.json",
            ]
        }
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        actual = {
            name: _sha256_file(bundle / name)
            for name in [
                "source-records.jsonl",
                "source-record-registry.jsonl",
                "transformation-manifest.json",
                "transformation-run.local.json",
            ]
        }
        assert actual == expected
        assert report.bundle_mutation_count == 0

    def test_raw_size_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        raw = tmp_path / "raw.parquet"
        raw.write_bytes(b"12345")
        report = validate_pubmedqa_bundle(
            bundle, raw_artifact=raw, authorized=True, expected_raw_size=4
        )
        assert any("raw size mismatch" in issue.message for issue in report.issues)
        assert not report.success

    def test_raw_sha256_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        raw = tmp_path / "raw.parquet"
        raw.write_bytes(b"12345")
        report = validate_pubmedqa_bundle(
            bundle, raw_artifact=raw, authorized=True, expected_raw_sha256="bad"
        )
        assert any("raw sha256 mismatch" in issue.message for issue in report.issues)
        assert not report.success


# ---------------------------------------------------------------------------
# JSON parsing helpers
# ---------------------------------------------------------------------------


class TestJsonParsing:
    def test_invalid_utf8_in_records_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        lines[0] = b'{"record": "\xff\xfe"}\n'
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid utf-8" in issue.message for issue in report.issues)
        assert not report.success

    def test_blank_line_in_records_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        lines.insert(1, b"\n")
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("blank line" in issue.message for issue in report.issues)
        assert not report.success

    def test_missing_final_newline_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-records.jsonl").write_bytes(
            (bundle / "source-records.jsonl").read_bytes().rstrip(b"\n")
        )
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("missing final newline" in issue.message for issue in report.issues)
        assert not report.success

    def test_malformed_json_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-records.jsonl").write_bytes(b"{bad\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("malformed json" in issue.message for issue in report.issues)
        assert not report.success

    def test_non_object_json_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-records.jsonl").write_bytes(b"[1, 2, 3]\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("non-object json" in issue.message for issue in report.issues)
        assert not report.success

    def test_records_loader_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            _load_jsonl(str(tmp_path / "missing.jsonl"))

    def test_loader_blank_line_records_error(self, tmp_path: Path) -> None:
        path = tmp_path / "blank.jsonl"
        path.write_bytes(b"\n")
        records, errors = _load_jsonl(str(path))
        assert records == []
        assert errors == ["blank line at 1"]

    def test_loader_missing_newline_records_error(self, tmp_path: Path) -> None:
        path = tmp_path / "nonewline.jsonl"
        path.write_bytes(b'{"a":1}')
        records, errors = _load_jsonl(str(path))
        assert records == []
        assert errors == ["missing final newline at line 1"]


# ---------------------------------------------------------------------------
# Source-record validation
# ---------------------------------------------------------------------------


class TestSourceRecordValidation:
    def test_malformed_json_emits_issue(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.jsonl"
        path.write_bytes(b"{bad\n")
        _aggregates, issues, passed, failed = _validate_source_records(str(path))
        assert any("malformed json at line 1" in issue.message for issue in issues)
        assert failed == 0 and passed == 0

    def test_entry_not_object_fails(self, tmp_path: Path) -> None:
        path = tmp_path / "nondict.jsonl"
        path.write_bytes(b"null\n")
        _aggregates, issues, passed, failed = _validate_source_records(str(path))
        assert any("non-object json at line 1" in issue.message for issue in issues)
        assert failed == 0 and passed == 0

    def test_missing_nested_record_object_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        lines[0] = _canonical({"record": []}) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("missing nested record object" in issue.message for issue in report.issues)
        assert not report.success

    def test_unexpected_record_key_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["extra"] = 1
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("unexpected field" in issue.message for issue in report.issues)
        assert not report.success

    def test_invalid_pubid_format_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["pubid"] = "abc"
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid pubid format" in issue.message for issue in report.issues)
        assert not report.success

    def test_leading_zero_pubid_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["pubid"] = "01"
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid pubid format" in issue.message for issue in report.issues)
        assert not report.success

    def test_duplicate_pubid_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=2)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entries = [json.loads(line) for line in lines]
        entries[1]["record"]["pubid"] = entries[0]["record"]["pubid"]
        entries[1]["record"]["source_document_id"] = entries[0]["record"]["source_document_id"]
        entries[1]["record"]["original_example_id"] = entries[0]["record"]["original_example_id"]
        entries[1]["source_record_hash"] = _sha256(_canonical(entries[1]["record"]))
        (bundle / "source-records.jsonl").write_bytes(
            b"".join(_canonical(entry) + b"\n" for entry in entries)
        )
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("duplicate pubid" in issue.message for issue in report.issues)
        assert not report.success

    def test_source_document_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["source_document_id"] = "pmid:999"
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("source-document mismatch" in issue.message for issue in report.issues)
        assert not report.success

    def test_original_example_id_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["original_example_id"] = "wrong:id"
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("original-example id mismatch" in issue.message for issue in report.issues)
        assert not report.success

    def test_blank_question_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["question"] = "   "
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("blank question" in issue.message for issue in report.issues)
        assert not report.success

    def test_blank_long_answer_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["long_answer"] = ""
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("blank long_answer" in issue.message for issue in report.issues)
        assert not report.success

    def test_context_segments_not_list_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["context_segments"] = "bad"
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("context_segments not list" in issue.message for issue in report.issues)
        assert not report.success

    def test_zero_context_segments_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["context_segments"] = []
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any(
            "context count must be between 1 and 9" in issue.message for issue in report.issues
        )
        assert not report.success

    def test_ten_context_segments_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["context_segments"] = [
            {"ordinal": i, "text": "t", "section_label": "BG"} for i in range(10)
        ]
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any(
            "context count must be between 1 and 9" in issue.message for issue in report.issues
        )
        assert not report.success

    def test_invalid_mesh_type_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["mesh_terms"] = [1]
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("contains non-string" in issue.message for issue in report.issues)
        assert not report.success

    def test_invalid_hash_format_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["source_record_hash"] = "abc"
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid hash format" in issue.message for issue in report.issues)
        assert not report.success

    def test_hash_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"]["question"] = "mutated"
        entry["source_record_hash"] = "a" * 64
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("hash mismatch" in issue.message for issue in report.issues)
        assert not report.success

    def test_hash_collision_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=2)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entries = [json.loads(line) for line in lines]
        entries[1]["record"]["pubid"] = entries[0]["record"]["pubid"]
        entries[1]["record"]["source_document_id"] = entries[0]["record"]["source_document_id"]
        entries[1]["record"]["original_example_id"] = entries[0]["record"]["original_example_id"]
        entries[1]["source_record_hash"] = entries[0]["source_record_hash"]
        (bundle / "source-records.jsonl").write_bytes(
            b"".join(_canonical(entry) + b"\n" for entry in entries)
        )
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("hash collision" in issue.message for issue in report.issues)
        assert not report.success

    def test_missing_required_scientific_field_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["record"].pop("schema_version", None)
        entry["source_record_hash"] = _sha256(_canonical(entry["record"]))
        lines[0] = _canonical(entry) + b"\n"
        (bundle / "source-records.jsonl").write_bytes(b"".join(lines))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("required field missing" in issue.message for issue in report.issues)
        assert not report.success


# ---------------------------------------------------------------------------
# Registry validation
# ---------------------------------------------------------------------------


class TestRegistryValidation:
    def test_registry_non_object_json_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-record-registry.jsonl").write_bytes(b"[1, 2]\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("non-object json at line 1" in issue.message for issue in report.issues)
        assert not report.success

    def test_registry_ordinal_not_int_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["row_ordinal"] = "one"
        (bundle / "source-record-registry.jsonl").write_bytes(_canonical(entry) + b"\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("ordinal missing or not int" in issue.message for issue in report.issues)
        assert not report.success

    def test_registry_duplicate_ordinal_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=2)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entries = [json.loads(line) for line in lines]
        entries[1]["row_ordinal"] = entries[0]["row_ordinal"]
        (bundle / "source-record-registry.jsonl").write_bytes(
            b"".join(_canonical(entry) + b"\n" for entry in entries)
        )
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("duplicate ordinal" in issue.message for issue in report.issues)
        assert not report.success

    def test_registry_missing_ordinal_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=2)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entries = [json.loads(line) for line in lines]
        del entries[1]["row_ordinal"]
        (bundle / "source-record-registry.jsonl").write_bytes(
            b"".join(_canonical(entry) + b"\n" for entry in entries)
        )
        reg_path = str(bundle / "source-record-registry.jsonl")
        records = [
            json.loads(line)
            for line in (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        ]
        _, issues, passed, failed = _validate_registry(
            reg_path,
            {r["source_record_hash"] for r in records},
            {r["record"]["source_document_id"] for r in records},
            {r["record"]["original_example_id"] for r in records},
        )
        assert any("ordinal missing or not int" in issue.message for issue in issues)
        assert failed == 1 and passed == 1

    def test_registry_orphan_entry_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["original_example_id"] = "missing:example:id"
        (bundle / "source-record-registry.jsonl").write_bytes(_canonical(entry) + b"\n")
        reg_path = str(bundle / "source-record-registry.jsonl")
        records = [
            json.loads(line)
            for line in (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        ]
        _, issues, passed, failed = _validate_registry(
            reg_path,
            {r["source_record_hash"] for r in records},
            {r["record"]["source_document_id"] for r in records},
            {r["record"]["original_example_id"] for r in records},
        )
        assert any("orphan registry entry" in issue.message for issue in issues)
        assert failed == 1 and passed == 0

    def test_registry_document_id_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["source_document_id"] = "missing:doc"
        (bundle / "source-record-registry.jsonl").write_bytes(_canonical(entry) + b"\n")
        reg_path = str(bundle / "source-record-registry.jsonl")
        records = [
            json.loads(line)
            for line in (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        ]
        _, issues, passed, failed = _validate_registry(
            reg_path,
            {r["source_record_hash"] for r in records},
            {r["record"]["source_document_id"] for r in records},
            {r["record"]["original_example_id"] for r in records},
        )
        assert any("document-id mismatch" in issue.message for issue in issues)
        assert failed == 1 and passed == 0

    def test_registry_hash_not_present_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        lines = (bundle / "source-record-registry.jsonl").read_bytes().splitlines(keepends=True)
        entry = json.loads(lines[0])
        entry["source_record_hash"] = (
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
        (bundle / "source-record-registry.jsonl").write_bytes(_canonical(entry) + b"\n")
        reg_path = str(bundle / "source-record-registry.jsonl")
        records = [
            json.loads(line)
            for line in (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        ]
        _, issues, passed, failed = _validate_registry(
            reg_path,
            {r["source_record_hash"] for r in records},
            {r["record"]["source_document_id"] for r in records},
            {r["record"]["original_example_id"] for r in records},
        )
        assert any("hash not present in source records" in issue.message for issue in issues)
        assert failed == 1 and passed == 0


# ---------------------------------------------------------------------------
# Manifest validation
# ---------------------------------------------------------------------------


class TestManifestValidation:
    def test_manifest_json_decode_error_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "transformation-manifest.json").write_bytes(b"{invalid json\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid manifest json" in issue.message for issue in report.issues)
        assert not report.success

    def test_manifest_source_record_count_mismatch_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        data = json.loads((bundle / "transformation-manifest.json").read_text(encoding="utf-8"))
        data["source_record_count"] = 999
        (bundle / "transformation-manifest.json").write_bytes(_canonical(data) + b"\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("source_record_count" in issue.field for issue in report.issues)
        assert not report.success


# ---------------------------------------------------------------------------
# Local report validation
# ---------------------------------------------------------------------------


class TestOperationalReport:
    def test_local_report_json_decode_error_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "transformation-run.local.json").write_bytes(b"{bad\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid local report json" in issue.message for issue in report.issues)
        assert not report.success

    def test_local_report_missing_raw_pre_post_does_not_crash(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "transformation-run.local.json"
        path.write_bytes(b'{"status":"complete"}')
        agg, issues = _validate_local_report(str(path), "a" * 64)
        assert agg.get("expected_raw_sha256_match") is False
        assert any(
            "does not attest the expected raw-artifact hash" in issue.message for issue in issues
        )

    def test_local_report_matching_attestation_passes(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "transformation-run.local.json"
        data = {
            "status": "complete",
            "input_sha256_pre": "a" * 64,
            "input_sha256_post": "a" * 64,
        }
        path.write_bytes(_canonical(data) + b"\n")
        agg, issues = _validate_local_report(str(path), "a" * 64)
        assert issues == []
        assert agg.get("expected_raw_sha256_match") is True

    def test_local_report_secret_like_key_does_not_crash(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        data = {
            "status": "complete",
            "raw_artifact_pre_sha256": "a" * 64,
            "raw_artifact_post_sha256": "a" * 64,
            "notes": "token=abc123 cookie=xyz",
        }
        (bundle / "transformation-run.local.json").write_bytes(_canonical(data) + b"\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.success is True


# ---------------------------------------------------------------------------
# Read-only and redaction behavior
# ---------------------------------------------------------------------------


class TestReadOnlyAndRedaction:
    def test_bundle_not_mutated_and_raw_artifact_unchanged(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        raw = tmp_path / "raw.parquet"
        raw.write_bytes(b"rawartifact")
        pre = {
            name: _sha256_file(bundle / name)
            for name in [
                "source-records.jsonl",
                "source-record-registry.jsonl",
                "transformation-manifest.json",
                "transformation-run.local.json",
            ]
        }
        report = validate_pubmedqa_bundle(bundle, raw_artifact=raw, authorized=True)
        post = {
            name: _sha256_file(bundle / name)
            for name in [
                "source-records.jsonl",
                "source-record-registry.jsonl",
                "transformation-manifest.json",
                "transformation-run.local.json",
            ]
        }
        assert report.success is True
        assert report.bundle_mutation_count == 0
        assert report.raw_artifact_unchanged is True
        assert report.transformation_rerun is False
        assert pre == post

    def test_stdout_contains_no_source_text(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        raw = tmp_path / "raw.parquet"
        raw.write_bytes(b"rawartifact")
        report = validate_pubmedqa_bundle(bundle, raw_artifact=raw, authorized=True)
        stdout = json.dumps(report.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False)
        assert "pmid:12345" not in stdout
        assert "answer" not in stdout
        assert "BACKGROUND" not in stdout


# ---------------------------------------------------------------------------
# Source-record semantic fail-closed branches
# ---------------------------------------------------------------------------


class TestSourceRecordSemanticFailClosed:
    def test_invalid_final_decision_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["final_decision"] = "unknown"
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid decision" in issue.message for issue in report.issues)
        assert not report.success

    def test_blank_context_segment_text_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["context_segments"][0]["text"] = "   "
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("blank segment text" in issue.message for issue in report.issues)
        assert not report.success

    def test_blank_section_label_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["context_segments"][0]["section_label"] = "  "
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("blank section_label" in issue.message for issue in report.issues)
        assert not report.success

    def test_non_integer_context_ordinal_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["context_segments"][0]["ordinal"] = "zero"
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("ordinal not int" in issue.message for issue in report.issues)
        assert not report.success

    def test_duplicate_context_ordinal_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["context_segments"].append(
            {"ordinal": 0, "text": "dup", "section_label": "BG"}
        )
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("duplicate ordinal 0" in issue.message for issue in report.issues)
        assert not report.success


# ---------------------------------------------------------------------------
# Registry fail-closed branches
# ---------------------------------------------------------------------------


class TestRegistryFailClosed:
    def test_missing_registry_file_returns_error_issue(self, tmp_path: Path) -> None:
        aggregates, issues, passed, failed = _validate_registry(
            str(tmp_path / "missing.jsonl"),
            set(),
            set(),
            set(),
        )
        assert aggregates == {}
        assert any("file not found" in issue.message for issue in issues)
        assert passed == 0 and failed == 0

    def test_non_object_registry_entry_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "source-record-registry.jsonl").write_bytes(b"[1]\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("non-object json at line 1" in issue.message for issue in report.issues)
        assert not report.success

    def test_unexpected_registry_keys_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-record-registry.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["extra"] = 1
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("unexpected keys:" in issue.message for issue in report.issues)
        assert not report.success

    def test_registry_record_hash_not_present_updates_orphan_count(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-record-registry.jsonl"
        path.write_bytes(
            _canonical(
                {
                    "row_ordinal": 0,
                    "original_example_id": (
                        "pubmedqa:pqa_labeled:9001f2853fb87cab8d220904e0de81ac6973b318"
                        ":train-00000-of-00001.parquet:0:12345"
                    ),
                    "source_document_id": "pmid:12345",
                    "source_record_hash": "a" * 64,
                }
            )
            + b"\n"
        )
        reg_path = str(path)
        records = [
            json.loads(line)
            for line in (bundle / "source-records.jsonl").read_bytes().splitlines(keepends=True)
        ]
        aggregates, issues, _, _ = _validate_registry(
            reg_path,
            {r["source_record_hash"] for r in records},
            {r["record"]["source_document_id"] for r in records},
            {r["record"]["original_example_id"] for r in records},
        )
        assert any("hash not present in source records" in issue.message for issue in issues)
        assert aggregates["orphan_record_count"] == 1


# ---------------------------------------------------------------------------
# Manifest and local-report fail-closed branches
# ---------------------------------------------------------------------------


class TestManifestAndLocalReportFailClosed:
    def test_missing_manifest_file_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "transformation-manifest.json").unlink()
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("manifest file not found" in issue.message for issue in report.issues)
        assert not report.success

    def test_invalid_manifest_json_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "transformation-manifest.json").write_bytes(b"{invalid\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("invalid manifest json" in issue.message for issue in report.issues)
        assert not report.success

    def test_missing_local_report_file_sets_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        (bundle / "transformation-run.local.json").unlink()
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("local report file not found" in issue.message for issue in report.issues)
        assert not report.success

    def test_record_count_mismatch_sets_manifest_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "transformation-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["record_count"] = 0
        path.write_bytes(_canonical(manifest) + b"\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any("manifest record_count differs" in issue.message for issue in report.issues)
        assert not report.success

    def test_context_segment_total_mismatch_sets_manifest_error(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "transformation-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["context_segment_aggregates"] = {"total": 0, "minimum": 0, "maximum": 0}
        path.write_bytes(_canonical(manifest) + b"\n")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert any(
            "manifest context segment total differs" in issue.message for issue in report.issues
        )
        assert not report.success


# ---------------------------------------------------------------------------
# Aggregate invariant tests
# ---------------------------------------------------------------------------


class TestAggregateInvariants:
    def test_perfect_aggregate_marked_passed(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.aggregate is not None
        assert report.aggregate.passed is True

    def test_any_error_marks_aggregate_failed(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        path = bundle / "source-records.jsonl"
        entries = [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)]
        entries[0]["record"]["final_decision"] = "unknown"
        entries[0]["source_record_hash"] = _sha256(_canonical(entries[0]["record"]))
        path.write_bytes(b"".join(_canonical(entry) + b"\n" for entry in entries))
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.aggregate is not None
        assert any("invalid decision" in failure for failure in report.aggregate.failures)
        assert report.success is False

    def test_report_schema_version_fixed(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.schema_version == "mesc-pubmedqa-validation/1"


# ---------------------------------------------------------------------------
# Registry cross-check through the PUBLIC API (regression: cross-check sets
# used to be harvested from the registry itself, so registry-vs-records
# validation was circular and a corrupted registry passed formal validation).
# ---------------------------------------------------------------------------


class TestRegistryCrossCheckPublicApi:
    def _tamper_registry_field(self, bundle: Path, field_name: str, value: str) -> None:
        path = bundle / "source-record-registry.jsonl"
        entry = json.loads(path.read_bytes().splitlines()[0])
        entry[field_name] = value
        path.write_bytes(_canonical(entry) + b"\n")

    def test_corrupted_registry_hash_fails_via_public_api(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        assert validate_pubmedqa_bundle(bundle, authorized=True).success is True
        self._tamper_registry_field(bundle, "source_record_hash", "0" * 64)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.success is False
        assert any("hash not present in source records" in i.message for i in report.issues)
        assert report.registry_validation_failed == 1

    def test_orphan_registry_example_id_fails_via_public_api(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        self._tamper_registry_field(bundle, "original_example_id", "missing:example:id")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.success is False
        assert any("orphan registry entry" in i.message for i in report.issues)

    def test_registry_document_id_mismatch_fails_via_public_api(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        self._tamper_registry_field(bundle, "source_document_id", "pmid:999999")
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.success is False
        assert any("document-id mismatch" in i.message for i in report.issues)

    def test_pristine_bundle_still_passes_via_public_api(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        report = validate_pubmedqa_bundle(bundle, authorized=True)
        assert report.success is True
        assert report.registry_validation_passed == 1
        assert report.registry_validation_failed == 0

    def test_local_report_attestation_enforced_via_public_api(self, tmp_path: Path) -> None:
        bundle, _ = _build_valid_bundle(tmp_path, record_count=1)
        # Helper's local report is {"status": "complete"} with no hash keys.
        report = validate_pubmedqa_bundle(bundle, authorized=True, expected_raw_sha256="a" * 64)
        assert report.success is False
        assert any(
            "does not attest the expected raw-artifact hash" in i.message for i in report.issues
        )
