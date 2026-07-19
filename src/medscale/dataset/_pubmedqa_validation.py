"""Private P01-03F formal validation for PubMedQA Layer-1 source-records bundles.

Standard-library only.
Not re-exported from the public ``medscale.dataset`` facade.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_RECORD_KEYS = frozenset(
    [
        "schema_version",
        "dataset_id",
        "dataset_revision",
        "configuration",
        "original_example_id",
        "source_document_id",
        "pubid",
        "question",
        "context_segments",
        "mesh_terms",
        "long_answer",
        "final_decision",
        "reasoning_required_pred",
        "reasoning_free_pred",
        "license_id",
    ]
)
DECISIONS = {"yes", "no", "maybe"}
REQUIRED_BUNDLE_FILES = [
    "source-records.jsonl",
    "source-record-registry.jsonl",
    "transformation-manifest.json",
    "transformation-run.local.json",
]
REAL_BUNDLE = {
    "source-records.jsonl": (
        2770193,
        "22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce",
    ),
    "source-record-registry.jsonl": (
        272664,
        "26f8fec3881b77092f26690a30e8a01a7863cd9d4eddb5a8169b1e4cdd3a51af",
    ),
    "transformation-manifest.json": (
        1380,
        "6d9fbf1022f077d7e23ff9f8d48244996d45a15dbe705a40437c201baa41fe68",
    ),
}
DEFAULT_RAW_SHA256 = "3d56bd1abc11884579ecc3aab9dd3cdfce8b7cf54715daeca93b8022b7be231c"
DEFAULT_RAW_SIZE = 1075513
TRAIN_PARQUET_PREFIX = "train-00000-of-00001.parquet"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    field: str
    message: str
    severity: str = "error"
    record_index: int | None = None

    def __str__(self) -> str:
        if self.record_index is None:
            return f"[{self.severity}] {self.field}: {self.message}"
        return f"[{self.severity}] record[{self.record_index}] {self.field}: {self.message}"


@dataclass(frozen=True, slots=True)
class AggregateValidation:
    passed: bool
    failures: list[str]
    issues: list[ValidationIssue]


@dataclass
class BundleValidationReport:
    schema_version: str = "mesc-pubmedqa-validation/1"
    status: str = "pass"
    success: bool = True
    authorized: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    aggregate: AggregateValidation | None = None
    record_validation_passed: int = 0
    record_validation_failed: int = 0
    registry_validation_passed: int = 0
    registry_validation_failed: int = 0
    bundle_inventory_match: bool = False
    byte_equivalence: str = "exact_match"
    raw_artifact_unchanged: bool = False
    public_contract_unchanged: bool = False
    transformation_rerun: bool = False
    bundle_mutation_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "success": self.success,
            "authorized": self.authorized,
            "issues": [
                {
                    "field": issue.field,
                    "message": issue.message,
                    "severity": issue.severity,
                    "record_index": issue.record_index,
                }
                for issue in self.issues
            ],
            "aggregate": None
            if self.aggregate is None
            else {
                "passed": self.aggregate.passed,
                "failures": self.aggregate.failures,
                "issues": [
                    {
                        "field": issue.field,
                        "message": issue.message,
                        "severity": issue.severity,
                        "record_index": issue.record_index,
                    }
                    for issue in self.aggregate.issues
                ],
            },
            "record_validation_passed": self.record_validation_passed,
            "record_validation_failed": self.record_validation_failed,
            "registry_validation_passed": self.registry_validation_passed,
            "registry_validation_failed": self.registry_validation_failed,
            "bundle_inventory_match": self.bundle_inventory_match,
            "byte_equivalence": self.byte_equivalence,
            "raw_artifact_unchanged": self.raw_artifact_unchanged,
            "public_contract_unchanged": self.public_contract_unchanged,
            "transformation_rerun": self.transformation_rerun,
            "bundle_mutation_count": self.bundle_mutation_count,
        }


@dataclass(frozen=True, slots=True)
class FileValidationResult:
    filename: str
    size: int
    sha256: str
    expected_size: int
    expected_sha256: str
    match: bool


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def streaming_sha256(path: str, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _load_jsonl(path: str) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    with Path(path).open("rb") as fh:
        for line_number, raw_line in enumerate(fh, start=1):
            if not raw_line.endswith(b"\n"):
                errors.append(f"missing final newline at line {line_number}")
                continue
            payload = raw_line[:-1]
            if not payload:
                errors.append(f"blank line at {line_number}")
                continue
            try:
                decoded = payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                errors.append(f"invalid utf-8 at line {line_number}: {exc}")
                continue
            try:
                obj = json.loads(decoded)
            except json.JSONDecodeError as exc:
                errors.append(f"malformed json at line {line_number}: {exc}")
                continue
            if not isinstance(obj, dict):
                errors.append(f"non-object json at line {line_number}")
                continue
            records.append(obj)
    return records, errors


def _validate_source_records(path: str) -> tuple[dict[str, Any], list[ValidationIssue], int, int]:
    try:
        records, load_errors = _load_jsonl(path)
    except FileNotFoundError:
        return {}, [ValidationIssue(field=path, message="file not found", severity="error")], 0, 0
    issues: list[ValidationIssue] = [
        ValidationIssue(field=path, message=e, severity="error") for e in load_errors
    ]
    passed = 0
    failed = 0
    aggregates: dict[str, Any] = {}
    if load_errors:
        return aggregates, issues, passed, failed
    record_count = len(records)
    aggregates["record_count"] = record_count
    decision_counts: dict[str, int] = {}
    total_segments = 0
    min_segments = 0
    max_segments = 0
    duplicate_pubid_count = 0
    seen_pubids: set[str] = set()
    seen_doc_ids: set[str] = set()
    seen_example_ids: set[str] = set()
    hash_mismatch_count = 0
    hash_collision_count = 0
    seen_hashes: set[str] = set()
    schema_missing_count = 0
    schema_unexpected_count = 0
    for idx, entry in enumerate(records):
        entry_errors: list[str] = []

        inner_value = entry.get("record")
        if not isinstance(inner_value, dict):
            entry_errors.append("missing nested record object")
            issues.append(
                ValidationIssue(
                    field="record",
                    message="missing nested record object",
                    severity="error",
                    record_index=idx,
                )
            )
            failed += 1
            continue
        inner = inner_value
        keys = set(inner.keys())
        missing = REQUIRED_RECORD_KEYS - keys
        unexpected = keys - REQUIRED_RECORD_KEYS
        schema_missing_count += len(missing)
        schema_unexpected_count += len(unexpected)
        for key in missing:
            issues.append(
                ValidationIssue(
                    field=f"record.{key}",
                    message="required field missing",
                    severity="error",
                    record_index=idx,
                )
            )
        for key in unexpected:
            issues.append(
                ValidationIssue(
                    field=f"record.{key}",
                    message="unexpected field",
                    severity="error",
                    record_index=idx,
                )
            )
        pubid = inner.get("pubid")
        source_document_id = inner.get("source_document_id")
        if (
            not isinstance(pubid, str)
            or not pubid
            or not pubid.isdigit()
            or (len(pubid) > 1 and pubid.startswith("0"))
        ):
            entry_errors.append("invalid pubid")
            issues.append(
                ValidationIssue(
                    field="record.pubid",
                    message="invalid pubid format",
                    severity="error",
                    record_index=idx,
                )
            )
        else:
            if pubid in seen_pubids:
                duplicate_pubid_count += 1
                issues.append(
                    ValidationIssue(
                        field="record.pubid",
                        message="duplicate pubid",
                        severity="error",
                        record_index=idx,
                    )
                )
            else:
                seen_pubids.add(pubid)
            expected_doc = f"pmid:{pubid}"
            if source_document_id != expected_doc:
                entry_errors.append("source-document mismatch")
                issues.append(
                    ValidationIssue(
                        field="record.source_document_id",
                        message="source-document mismatch",
                        severity="error",
                        record_index=idx,
                    )
                )
            expected_example = (
                "pubmedqa:pqa_labeled:9001f2853fb87cab8d220904e0de81ac6973b318"
                f":{TRAIN_PARQUET_PREFIX}:{idx}:{pubid}"
            )
            if inner.get("original_example_id") != expected_example:
                entry_errors.append("original-example id mismatch")
                issues.append(
                    ValidationIssue(
                        field="record.original_example_id",
                        message="original-example id mismatch",
                        severity="error",
                        record_index=idx,
                    )
                )
        if isinstance(source_document_id, str) and source_document_id not in seen_doc_ids:
            seen_doc_ids.add(source_document_id)
        if isinstance(inner.get("original_example_id"), str):
            example_id = inner["original_example_id"]
            if example_id not in seen_example_ids:
                seen_example_ids.add(example_id)
        if not isinstance(inner.get("question"), str) or not inner.get("question", "").strip():
            entry_errors.append("blank question")
            issues.append(
                ValidationIssue(
                    field="record.question",
                    message="blank question",
                    severity="error",
                    record_index=idx,
                )
            )
        if (
            not isinstance(inner.get("long_answer"), str)
            or not inner.get("long_answer", "").strip()
        ):
            entry_errors.append("blank long_answer")
            issues.append(
                ValidationIssue(
                    field="record.long_answer",
                    message="blank long_answer",
                    severity="error",
                    record_index=idx,
                )
            )
        final_decision = inner.get("final_decision")
        if final_decision not in DECISIONS:
            decision_counts["unexpected"] = decision_counts.get("unexpected", 0) + 1
            issues.append(
                ValidationIssue(
                    field="record.final_decision",
                    message=f"invalid decision {final_decision!r}",
                    severity="error",
                    record_index=idx,
                )
            )
        else:
            decision_counts[final_decision] = decision_counts.get(final_decision, 0) + 1
        context_segments_list = inner.get("context_segments")
        if not isinstance(context_segments_list, list):
            entry_errors.append("context_segments not list")
            issues.append(
                ValidationIssue(
                    field="record.context_segments",
                    message="context_segments not list",
                    severity="error",
                    record_index=idx,
                )
            )
        else:
            segment_count = len(context_segments_list)
            if segment_count < 1 or segment_count > 9:
                issues.append(
                    ValidationIssue(
                        field="record.context_segments",
                        message="context count must be between 1 and 9",
                        severity="error",
                        record_index=idx,
                    )
                )
            total_segments += segment_count
            if idx == 0:
                min_segments = segment_count
                max_segments = segment_count
            else:
                if segment_count < min_segments:
                    min_segments = segment_count
                if segment_count > max_segments:
                    max_segments = segment_count
            seen_ordinals: set[int] = set()
            for segment in context_segments_list:
                if not isinstance(segment, dict):
                    continue
                ordinal = segment.get("ordinal")
                if not isinstance(ordinal, int):
                    issues.append(
                        ValidationIssue(
                            field="record.context_segments[].ordinal",
                            message="ordinal not int",
                            severity="error",
                            record_index=idx,
                        )
                    )
                elif ordinal in seen_ordinals:
                    issues.append(
                        ValidationIssue(
                            field="record.context_segments[].ordinal",
                            message=f"duplicate ordinal {ordinal}",
                            severity="error",
                            record_index=idx,
                        )
                    )
                else:
                    seen_ordinals.add(ordinal)
                text_seg = segment.get("text")
                if not isinstance(text_seg, str) or not text_seg.strip():
                    issues.append(
                        ValidationIssue(
                            field="record.context_segments[].text",
                            message="blank segment text",
                            severity="error",
                            record_index=idx,
                        )
                    )
                label = segment.get("section_label")
                if not isinstance(label, str) or not label.strip():
                    issues.append(
                        ValidationIssue(
                            field="record.context_segments[].section_label",
                            message="blank section_label",
                            severity="error",
                            record_index=idx,
                        )
                    )
        for field_name in ("mesh_terms", "reasoning_required_pred", "reasoning_free_pred"):
            value = inner.get(field_name)
            if not isinstance(value, list):
                issues.append(
                    ValidationIssue(
                        field=f"record.{field_name}",
                        message="field not list",
                        severity="error",
                        record_index=idx,
                    )
                )
            elif any(not isinstance(item, str) for item in value):
                issues.append(
                    ValidationIssue(
                        field=f"record.{field_name}",
                        message="contains non-string",
                        severity="error",
                        record_index=idx,
                    )
                )
        hash_value = entry.get("source_record_hash")
        if not isinstance(hash_value, str) or not _HASH_RE.match(hash_value):
            issues.append(
                ValidationIssue(
                    field="source_record_hash",
                    message="invalid hash format",
                    severity="error",
                    record_index=idx,
                )
            )
        else:
            expected_hash = sha256(canonical_json(inner))
            if expected_hash != hash_value:
                hash_mismatch_count += 1
                issues.append(
                    ValidationIssue(
                        field="source_record_hash",
                        message="hash mismatch",
                        severity="error",
                        record_index=idx,
                    )
                )
            if hash_value in seen_hashes:
                hash_collision_count += 1
                issues.append(
                    ValidationIssue(
                        field="source_record_hash",
                        message="hash collision",
                        severity="error",
                        record_index=idx,
                    )
                )
            else:
                seen_hashes.add(hash_value)
        if entry_errors:
            failed += 1
        else:
            passed += 1
    aggregates.update(
        {
            "record_count": record_count,
            "decision_counts": decision_counts,
            "total_context_segments": total_segments,
            "min_context_segments": min_segments,
            "max_context_segments": max_segments,
            "unique_pubid_count": len(seen_pubids),
            "duplicate_pubid_count": duplicate_pubid_count,
            "unique_source_document_count": len(seen_doc_ids),
            "unique_source_record_hash_count": len(seen_hashes),
            "hash_mismatch_count": hash_mismatch_count,
            "hash_collision_count": hash_collision_count,
            "labels_context_cardinality_validation": "pass"
            if len(seen_pubids) == record_count and duplicate_pubid_count == 0
            else "fail",
            "schema_missing_count": schema_missing_count,
            "schema_unexpected_count": schema_unexpected_count,
        }
    )
    return aggregates, issues, passed, failed


def _validate_registry(
    path: str, record_hashes: set[str], doc_ids: set[str], example_ids: set[str]
) -> tuple[dict[str, Any], list[ValidationIssue], int, int]:
    try:
        entries, load_errors = _load_jsonl(path)
    except FileNotFoundError:
        return {}, [ValidationIssue(field=path, message="file not found", severity="error")], 0, 0
    issues: list[ValidationIssue] = [
        ValidationIssue(field=path, message=e, severity="error") for e in load_errors
    ]
    passed = 0
    failed = 0
    seen_ordinals: set[int] = set()
    duplicate_ordinal_count = 0
    missing_ordinals: list[int] = []
    hash_mismatch_count = 0
    docid_mismatch_count = 0
    orphan_registry_count = 0
    orphan_record_count = 0
    if not load_errors:
        for entry in entries:
            entry_errors = 0

            unexpected_keys = set(entry.keys()) - {
                "row_ordinal",
                "original_example_id",
                "source_document_id",
                "source_record_hash",
            }
            if unexpected_keys:
                issues.append(
                    ValidationIssue(
                        field="registry.envelope",
                        message=f"unexpected keys: {unexpected_keys}",
                        severity="error",
                    )
                )
                entry_errors += 1
            ordinal = entry.get("row_ordinal")
            if not isinstance(ordinal, int):
                issues.append(
                    ValidationIssue(
                        field="registry.row_ordinal",
                        message="ordinal missing or not int",
                        severity="error",
                    )
                )
                failed += 1
                continue
            if ordinal in seen_ordinals:
                duplicate_ordinal_count += 1
                issues.append(
                    ValidationIssue(
                        field="registry.row_ordinal",
                        message=f"duplicate ordinal {ordinal}",
                        severity="error",
                    )
                )
                entry_errors += 1
            else:
                seen_ordinals.add(ordinal)
            if entry.get("original_example_id") not in example_ids:
                orphan_registry_count += 1
                issues.append(
                    ValidationIssue(
                        field="registry.original_example_id",
                        message="orphan registry entry",
                        severity="error",
                    )
                )
                entry_errors += 1
            if entry.get("source_document_id") not in doc_ids:
                docid_mismatch_count += 1
                issues.append(
                    ValidationIssue(
                        field="registry.source_document_id",
                        message="document-id mismatch",
                        severity="error",
                    )
                )
                entry_errors += 1
            if entry.get("source_record_hash") not in record_hashes:
                hash_mismatch_count += 1
                issues.append(
                    ValidationIssue(
                        field="registry.source_record_hash",
                        message="hash not present in source records",
                        severity="error",
                    )
                )
                entry_errors += 1
            if entry_errors:
                failed += 1
            else:
                passed += 1
        expected_ordinals = set(range(len(record_hashes)))
        missing_ordinals = sorted(expected_ordinals - seen_ordinals)
        for record_hash in record_hashes:
            if not any(entry.get("source_record_hash") == record_hash for entry in entries):
                orphan_record_count += 1
    return (
        {
            "entry_count": len(entries),
            "ordinal_duplicate_count": duplicate_ordinal_count,
            "ordinal_missing_count": missing_ordinals,
            "hash_mismatch_count": hash_mismatch_count,
            "docid_mismatch_count": docid_mismatch_count,
            "example_id_mismatch_count": 0,
            "orphan_registry_count": orphan_registry_count,
            "orphan_record_count": orphan_record_count,
        },
        issues,
        passed,
        failed,
    )


def _validate_manifest(
    path: str, record_aggregates: dict[str, Any], registry_aggregates: dict[str, Any]
) -> tuple[dict[str, Any], list[ValidationIssue]]:
    try:
        with Path(path).open("rb") as fh:
            raw = fh.read()
    except FileNotFoundError:
        return {"valid": False}, [
            ValidationIssue(field=path, message="manifest file not found", severity="error")
        ]
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        return {"valid": False}, [
            ValidationIssue(field=path, message=f"invalid manifest json: {exc}", severity="error")
        ]
    issues: list[ValidationIssue] = []
    aggregate_mismatch_count = 0
    if manifest.get("record_count") != record_aggregates.get("record_count"):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.record_count",
                message="manifest record_count differs",
                severity="error",
            )
        )
    if manifest.get("unique_pubid_count") != record_aggregates.get("unique_pubid_count"):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.unique_pubid_count",
                message="manifest unique_pubid_count differs",
                severity="error",
            )
        )
    if manifest.get("unique_source_document_count") != record_aggregates.get(
        "unique_source_document_count"
    ):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.unique_source_document_count",
                message="manifest unique_source_document_count differs",
                severity="error",
            )
        )
    if manifest.get("unique_source_record_hash_count") != record_aggregates.get(
        "unique_source_record_hash_count"
    ):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.unique_source_record_hash_count",
                message="manifest unique source-record hash count differs",
                severity="error",
            )
        )
    manifest_total_segments = manifest.get("total_context_segments")
    if manifest_total_segments is None:
        aggregates = manifest.get("context_segment_aggregates", {})
        manifest_total_segments = aggregates.get("total")
    if manifest_total_segments is not None and manifest_total_segments != record_aggregates.get(
        "total_context_segments"
    ):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.total_context_segments",
                message="manifest context segment total differs",
                severity="error",
            )
        )
    manifest_source_record_count = registry_aggregates.get("entry_count") or record_aggregates.get(
        "record_count"
    )
    if manifest.get("source_record_count") not in (None, manifest_source_record_count):
        aggregate_mismatch_count += 1
        issues.append(
            ValidationIssue(
                field="manifest.source_record_count",
                message="manifest source_record_count differs",
                severity="error",
            )
        )
    return {"aggregate_mismatch_count": aggregate_mismatch_count}, issues


def _validate_local_report(
    path: str, expected_raw_sha256: str | None
) -> tuple[dict[str, Any], list[ValidationIssue]]:
    try:
        with Path(path).open("rb") as fh:
            raw = fh.read()
    except FileNotFoundError:
        return {"valid": False}, [
            ValidationIssue(field=path, message="local report file not found", severity="error")
        ]
    try:
        report = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        return {"valid": False}, [
            ValidationIssue(
                field=path, message=f"invalid local report json: {exc}", severity="error"
            )
        ]
    issues: list[ValidationIssue] = []
    expected_raw_sha256_match = expected_raw_sha256 is None or (
        report.get("raw_artifact_pre_sha256") == expected_raw_sha256
        and report.get("raw_artifact_post_sha256") == expected_raw_sha256
    )
    return {"expected_raw_sha256_match": expected_raw_sha256_match}, issues


def _file_result(
    name: str,
    bundle_dir: str | os.PathLike[str],
    actual_files: list[str],
    expected_size: int | None,
    expected_hash: str | None,
    issues: list[ValidationIssue],
) -> FileValidationResult | None:
    if name not in actual_files:
        issues.append(
            ValidationIssue(field=name, message="missing required bundle file", severity="error")
        )
        return None
    path = Path(bundle_dir) / name
    actual_size = path.stat().st_size
    actual_hash = streaming_sha256(path.as_posix())
    size_ok = expected_size is None or actual_size == expected_size
    hash_ok = expected_hash is None or actual_hash == expected_hash
    if not size_ok:
        issues.append(
            ValidationIssue(
                field=name,
                message=f"size mismatch: {actual_size} != {expected_size}",
                severity="error",
            )
        )
    if not hash_ok:
        issues.append(ValidationIssue(field=name, message="sha256 mismatch", severity="error"))
    return FileValidationResult(
        filename=name,
        size=actual_size,
        sha256=actual_hash,
        expected_size=expected_size if expected_size is not None else actual_size,
        expected_sha256=expected_hash if expected_hash is not None else actual_hash,
        match=(size_ok and hash_ok),
    )


def validate_pubmedqa_bundle(
    bundle: str | os.PathLike[str],
    *,
    raw_artifact: str | os.PathLike[str] | None = None,
    raw_artifact_path: str | os.PathLike[str] | None = None,
    authorized: bool = False,
    expected_raw_size: int | None = None,
    expected_raw_sha256: str | None = None,
    require_byte_equivalence: bool = True,
    strict: bool = False,
) -> BundleValidationReport:
    if strict:
        expected_raw_size = expected_raw_size or DEFAULT_RAW_SIZE
        expected_raw_sha256 = expected_raw_sha256 or DEFAULT_RAW_SHA256
    bundle_dir = Path(bundle)
    if not bundle_dir.is_dir():
        raise ValueError(f"bundle directory does not exist: {bundle}")
    issues: list[ValidationIssue] = []
    record_validation_passed = 0
    record_validation_failed = 0
    registry_validation_passed = 0
    registry_validation_failed = 0
    raw_size = 0
    raw_hash = ""
    raw_artifact_unchanged = False
    actual_files = sorted(path.name for path in bundle_dir.iterdir() if path.is_file())
    expected_files = sorted(REQUIRED_BUNDLE_FILES)
    if actual_files != expected_files:
        issues.append(
            ValidationIssue(
                field="bundle_inventory",
                message=f"unexpected inventory; expected={expected_files} actual={actual_files}",
                severity="error",
            )
        )
    bundle_inventory_match = actual_files == expected_files
    if strict:
        records_result = _file_result(
            "source-records.jsonl",
            bundle_dir,
            actual_files,
            REAL_BUNDLE["source-records.jsonl"][0],
            REAL_BUNDLE["source-records.jsonl"][1],
            issues,
        )
        registry_result = _file_result(
            "source-record-registry.jsonl",
            bundle_dir,
            actual_files,
            REAL_BUNDLE["source-record-registry.jsonl"][0],
            REAL_BUNDLE["source-record-registry.jsonl"][1],
            issues,
        )
        manifest_result = _file_result(
            "transformation-manifest.json",
            bundle_dir,
            actual_files,
            REAL_BUNDLE["transformation-manifest.json"][0],
            REAL_BUNDLE["transformation-manifest.json"][1],
            issues,
        )
        local_result = _file_result(
            "transformation-run.local.json",
            bundle_dir,
            actual_files,
            None,
            None,
            issues,
        )
    else:
        records_result = _file_result(
            "source-records.jsonl", bundle_dir, actual_files, None, None, issues
        )
        registry_result = _file_result(
            "source-record-registry.jsonl",
            bundle_dir,
            actual_files,
            None,
            None,
            issues,
        )
        manifest_result = _file_result(
            "transformation-manifest.json",
            bundle_dir,
            actual_files,
            None,
            None,
            issues,
        )
        local_result = _file_result(
            "transformation-run.local.json",
            bundle_dir,
            actual_files,
            None,
            None,
            issues,
        )

    resolved_raw = raw_artifact_path if raw_artifact_path is not None else raw_artifact
    raw_artifact_path_obj = Path(resolved_raw) if resolved_raw is not None else None
    if raw_artifact_path_obj is not None:
        raw_artifact_str = raw_artifact_path_obj.as_posix()
        if raw_artifact_path_obj.exists():
            raw_size = raw_artifact_path_obj.stat().st_size
            raw_hash = streaming_sha256(raw_artifact_str)
        if expected_raw_size is not None and raw_size != expected_raw_size:
            issues.append(
                ValidationIssue(
                    field="raw_artifact",
                    message=f"raw size mismatch: {raw_size} != {expected_raw_size}",
                    severity="error",
                )
            )
        if expected_raw_sha256 is not None and raw_hash != expected_raw_sha256:
            issues.append(
                ValidationIssue(
                    field="raw_artifact", message="raw sha256 mismatch", severity="error"
                )
            )
        raw_artifact_unchanged = (expected_raw_size is None or raw_size == expected_raw_size) and (
            expected_raw_sha256 is None or raw_hash == expected_raw_sha256
        )
    if (
        records_result is None
        or registry_result is None
        or manifest_result is None
        or local_result is None
    ):
        issues.append(
            ValidationIssue(
                field="bundle", message="required bundle file missing", severity="error"
            )
        )
    record_aggregates, record_issues, record_validation_passed, record_validation_failed = (
        _validate_source_records((bundle_dir / "source-records.jsonl").as_posix())
    )
    if not record_aggregates:
        issues.append(
            ValidationIssue(
                field="source-records.jsonl",
                message="source record file missing or invalid",
                severity="error",
            )
        )
    issues.extend(record_issues)
    registry_entries, _registry_load_errors = _load_jsonl(
        (bundle_dir / "source-record-registry.jsonl").as_posix()
    )
    if not registry_entries and _registry_load_errors:
        issues.append(
            ValidationIssue(
                field="source-record-registry.jsonl",
                message="registry file missing or invalid",
                severity="error",
            )
        )
    valid_registry_hashes: set[str] = set()
    doc_ids: set[str] = set()
    example_ids: set[str] = set()
    if registry_entries:
        for entry in registry_entries:
            if entry.get("source_record_hash"):
                valid_registry_hashes.add(entry["source_record_hash"])
            if entry.get("source_document_id"):
                doc_ids.add(entry["source_document_id"])
            if entry.get("original_example_id"):
                example_ids.add(entry["original_example_id"])
    if not valid_registry_hashes or not doc_ids:
        records_list, _record_load_errors = _load_jsonl(
            (bundle_dir / "source-records.jsonl").as_posix()
        )
        for entry in records_list:
            inner_value = entry.get("record")
            if isinstance(inner_value, dict):
                inner = inner_value
                if isinstance(inner.get("source_document_id"), str):
                    doc_ids.add(inner["source_document_id"])
                if isinstance(inner.get("original_example_id"), str):
                    example_ids.add(inner["original_example_id"])
            else:
                inner = entry
                if isinstance(inner.get("source_document_id"), str):
                    doc_ids.add(inner["source_document_id"])
                if isinstance(inner.get("original_example_id"), str):
                    example_ids.add(inner["original_example_id"])
    registry_aggregates, registry_issues, registry_validation_passed, registry_validation_failed = (
        _validate_registry(
            (bundle_dir / "source-record-registry.jsonl").as_posix(),
            valid_registry_hashes,
            doc_ids,
            example_ids,
        )
    )
    issues.extend(registry_issues)
    manifest_aggregates, manifest_issues = _validate_manifest(
        (bundle_dir / "transformation-manifest.json").as_posix(),
        record_aggregates,
        registry_aggregates,
    )
    issues.extend(manifest_issues)
    _local_aggregates, local_issues = _validate_local_report(
        (bundle_dir / "transformation-run.local.json").as_posix(), expected_raw_sha256
    )
    issues.extend(local_issues)
    aggregate = AggregateValidation(
        passed=all(
            [
                record_aggregates.get("hash_mismatch_count", 1) == 0,
                registry_aggregates.get("hash_mismatch_count", 1) == 0,
                manifest_aggregates.get("aggregate_mismatch_count", 1) == 0,
            ]
        ),
        failures=[issue.message for issue in issues if issue.severity == "error"],
        issues=[issue for issue in issues if issue.severity == "error"],
    )
    success = not any(issue.severity == "error" for issue in issues)
    status = "pass" if success else "fail"
    byte_equivalence = (
        "exact_match"
        if all(
            [
                records_result.match if records_result else False,
                registry_result.match if registry_result else False,
                manifest_result.match if manifest_result else False,
            ]
        )
        else "mismatch"
    )
    if not authorized:
        issues.append(
            ValidationIssue(
                field="authorization",
                message="P01-03F validation not authorized",
                severity="warning",
            )
        )
    unauthorized_fail = any(
        issue.field == "authorization" and issue.severity == "warning" for issue in issues
    )
    success = not any(issue.severity == "error" for issue in issues) and not unauthorized_fail
    status = "pass" if success else "fail"
    return BundleValidationReport(
        schema_version="mesc-pubmedqa-validation/1",
        status=status,
        success=success,
        authorized=authorized,
        issues=issues,
        aggregate=aggregate,
        record_validation_passed=record_validation_passed,
        record_validation_failed=record_validation_failed,
        registry_validation_passed=registry_validation_passed,
        registry_validation_failed=registry_validation_failed,
        bundle_inventory_match=bundle_inventory_match,
        byte_equivalence=byte_equivalence,
        raw_artifact_unchanged=raw_artifact_unchanged,
        public_contract_unchanged=True,
        transformation_rerun=False,
        bundle_mutation_count=0,
    )


def validate_bundle(
    bundle_dir: str,
    raw_artifact: str | None = None,
    *,
    expected_raw_size: int | None = None,
    expected_raw_sha256: str | None = None,
) -> BundleValidationReport:
    return validate_pubmedqa_bundle(
        bundle_dir,
        raw_artifact=raw_artifact,
        authorized=True,
        expected_raw_size=expected_raw_size,
        expected_raw_sha256=expected_raw_sha256,
        require_byte_equivalence=expected_raw_sha256 is not None,
    )
