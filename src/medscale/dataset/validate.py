"""Dataset validation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["DatasetValidationReport", "ValidationIssue", "validate_dataset"]

_DATASET_ID_RE = re.compile(r"^[a-z][a-z0-9-]{3,63}$")
_SYNTHETIC_FIRST = True
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)?$")


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str
    severity: str = "error"

    def __str__(self) -> str:
        return f"[{self.severity}] {self.field}: {self.message}"


@dataclass(frozen=True)
class DatasetValidationReport:
    dataset_id: str | None
    passed: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    schema_checks: list[str] = field(default_factory=list)
    checksum_checks: list[str] = field(default_factory=list)
    split_checks: list[str] = field(default_factory=list)

    def to_summary(self) -> str:
        lines = [
            f"Dataset: {self.dataset_id or '(unknown)'}",
            f"Passed: {self.passed}",
            "",
            "Schema:",
            "  " + ("PASS" if all(self.schema_checks) or not self.schema_checks else "FAIL"),
            "",
            "Checksums:",
            "  " + ("PASS" if all(self.checksum_checks) or not self.checksum_checks else "FAIL"),
            "",
            "Splits:",
            "  " + ("PASS" if all(self.split_checks) or not self.split_checks else "FAIL"),
            "",
        ]
        if self.issues:
            lines.extend(["Issues:", *(f"  ! {issue}" for issue in self.issues)])
        return "\n".join(lines)


def _sha256_of(value: object) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def _inside_dataset_root(path: Path, dataset_dir: Path) -> bool:
    try:
        path_resolved = path.resolve()
    except OSError:
        return False
    return path_resolved.is_relative_to(dataset_dir.resolve())


def _timestamp_value(manifest: dict[str, Any], field_name: str) -> str | None:
    value = manifest.get(field_name)
    dataset_snapshot = manifest.get("dataset_snapshot") or {}
    dataset_snapshot_value = (
        dataset_snapshot.get(field_name) if isinstance(dataset_snapshot, dict) else None
    )
    selected = dataset_snapshot_value or (value if isinstance(value, str) else None)
    return selected if isinstance(selected, str) else None


def _validate_timestamps(manifest: dict[str, Any], issues: list[ValidationIssue]) -> None:
    created_at = _timestamp_value(manifest, "created_at")
    if not created_at or not _TIMESTAMP_RE.match(created_at):
        issues.append(ValidationIssue("created_at", "missing or invalid ISO-8601 timestamp"))


def _validate_dataset_id(manifest: dict[str, Any], issues: list[ValidationIssue]) -> None:
    dataset_id = manifest.get("dataset_id")
    if not isinstance(dataset_id, str) or not _DATASET_ID_RE.match(dataset_id):
        issues.append(ValidationIssue("dataset_id", "must match ^[a-z][a-z0-9-]{3,63}$"))


def _validate_synthetic_first(
    manifest: dict[str, Any],
    dataset_dir: Path,
    issues: list[ValidationIssue],
) -> None:
    license_path = dataset_dir / "metadata" / "license.json"
    if not license_path.exists():
        issues.append(ValidationIssue("metadata/license.json", "missing license metadata"))
        return
    try:
        license_data = _load_json(license_path)
    except ValueError as exc:
        issues.append(ValidationIssue("metadata/license.json", str(exc)))
        return
    if not isinstance(license_data, dict):
        issues.append(ValidationIssue("metadata/license.json", "must be a JSON object"))
        return
    source_scope = license_data.get("source_scope")
    if not isinstance(source_scope, list) or "synthetic" not in source_scope:
        issues.append(
            ValidationIssue(
                "metadata/license.json",
                "source_scope must include 'synthetic'",
            )
        )


def validate_dataset(dataset_dir: Path) -> DatasetValidationReport:
    issues: list[ValidationIssue] = []
    schema_checks: list[str] = []
    checksum_checks: list[str] = []
    split_checks: list[str] = []

    dataset_dir = dataset_dir.resolve()
    manifest_path = dataset_dir / "manifest.json"
    schema_path = dataset_dir / "schema.json"
    train_path = dataset_dir / "splits" / "train.json"
    validation_path = dataset_dir / "splits" / "validation.json"
    test_path = dataset_dir / "splits" / "test.json"
    checksums_dir = dataset_dir / "checksums"

    manifest: dict[str, Any] | None = None
    if not manifest_path.exists():
        issues.append(ValidationIssue("manifest.json", "missing manifest"))
    else:
        try:
            manifest = _load_json(manifest_path)
            schema_checks.append("manifest.json: present")
            if not isinstance(manifest, dict):
                issues.append(ValidationIssue("manifest.json", "must be a JSON object"))
                manifest = None
        except ValueError as exc:
            issues.append(ValidationIssue("manifest.json", str(exc)))

    if not schema_path.exists():
        issues.append(ValidationIssue("schema.json", "missing schema"))
    else:
        try:
            _load_json(schema_path)
            schema_checks.append("schema.json: present")
        except ValueError as exc:
            issues.append(ValidationIssue("schema.json", str(exc)))

    for name, path in [
        ("train.json", train_path),
        ("validation.json", validation_path),
        ("test.json", test_path),
    ]:
        if not path.exists():
            issues.append(ValidationIssue(name, f"missing split file: {path.name}"))
            continue
        try:
            _load_json(path)
            split_checks.append(f"{name}: present")
        except ValueError as exc:
            issues.append(ValidationIssue(name, str(exc)))

    expected_checksums: dict[str, str] = {}
    if checksums_dir.exists():
        for checksum_file in sorted(checksums_dir.glob("*.sha256")):
            relative_name = checksum_file.name[: -len(".sha256")]
            expected_checksums[relative_name] = checksum_file.read_text(encoding="utf-8").strip()

    if not expected_checksums:
        issues.append(ValidationIssue("checksums/", "missing sibling .sha256 files"))
    else:
        for relative_name, expected_digest in expected_checksums.items():
            # Accept both writer-style names ("schema.json") and the ADR-0030
            # extensionless spellings ("schema"): normalize before lookup.
            if relative_name.endswith(".json") or relative_name == "README.md":
                artifact_name = relative_name
            else:
                artifact_name = f"{relative_name}.json"
            # Location table mirrors compute_dataset_checksums: metadata files
            # live under metadata/, splits under splits/, the rest at the root.
            if artifact_name in {"manifest.json", "schema.json", "README.md"}:
                artifact_path = dataset_dir / artifact_name
            elif artifact_name in {
                "train.json",
                "validation.json",
                "test.json",
            }:
                artifact_path = dataset_dir / "splits" / artifact_name
            elif artifact_name in {"license.json", "statistics.json"}:
                artifact_path = dataset_dir / "metadata" / artifact_name
            else:
                artifact_path = (dataset_dir / artifact_name).resolve()
            if not _inside_dataset_root(artifact_path, dataset_dir):
                issues.append(ValidationIssue(artifact_name, "path escaped dataset root"))
                continue
            if not artifact_path.exists():
                issues.append(ValidationIssue(artifact_name, "missing artifact for checksum"))
                continue
            actual_digest = _sha256_file(artifact_path)
            if actual_digest == expected_digest:
                checksum_checks.append(f"{relative_name}: match")
            else:
                issues.append(
                    ValidationIssue(
                        artifact_name,
                        "sha256 mismatch: expected "
                        f"{expected_digest[:12]}... actual "
                        f"{actual_digest[:12]}...",
                    )
                )
                checksum_checks.append(f"{relative_name}: mismatch")

    if manifest is not None:
        _validate_timestamps(manifest, issues)
        _validate_dataset_id(manifest, issues)
        _validate_synthetic_first(manifest, dataset_dir, issues)

    return DatasetValidationReport(
        dataset_id=manifest.get("dataset_id") if isinstance(manifest, dict) else None,
        passed=not issues,
        issues=issues,
        schema_checks=schema_checks,
        checksum_checks=checksum_checks,
        split_checks=split_checks,
    )
