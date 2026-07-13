"""Dataset validation.

Stability: **public**. Validation is read-only and fails loudly on any mismatch.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from medscale.dataset.schema import DatasetSchema

__all__ = ["DatasetValidationReport", "ValidationIssue", "validate_dataset"]


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


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def validate_dataset(dataset_dir: Path) -> DatasetValidationReport:
    """Validate a dataset directory.

    Checks:
    - manifest.json exists and is valid JSON
    - schema.json exists and is valid JSON
    - splits/train.json, splits/validation.json, splits/test.json exist
    - checksums/*.sha256 match sibling artifact hashes

    Returns a report; does not raise on validation failure.
    """
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

    if not manifest_path.exists():
        issues.append(ValidationIssue("manifest.json", "missing manifest"))
    else:
        try:
            manifest = _load_json(manifest_path)
            schema_checks.append("manifest.json: present")
            if not isinstance(manifest, dict):
                issues.append(ValidationIssue("manifest.json", "must be a JSON object"))
        except ValueError as exc:
            issues.append(ValidationIssue("manifest.json", str(exc)))

    if not schema_path.exists():
        issues.append(ValidationIssue("schema.json", "missing schema"))
    else:
        try:
            schema = _load_json(schema_path)
            schema_checks.append("schema.json: present")
            if not isinstance(schema, dict):
                issues.append(ValidationIssue("schema.json", "must be a JSON object"))
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

    checksums_dir = dataset_dir / "checksums"
    if checksums_dir.exists():
        for checksum_file in sorted(checksums_dir.glob("*.sha256")):
            artifact_name = checksum_file.name[: -len(".sha256")]
            artifact_path = checksum_file.parent.parent / checksum_file.name.replace(
                ".sha256", ""
            )
            if not artifact_path.exists():
                issues.append(ValidationIssue(str(artifact_path), "missing artifact for checksum"))
                continue
            expected = checksum_file.read_text(encoding="utf-8").strip()
            actual = _sha256_file(artifact_path)
            if expected == actual:
                checksum_checks.append(f"{artifact_name}: match")
            else:
                issues.append(
                    ValidationIssue(
                        str(artifact_path),
                        "sha256 mismatch",
                    )
                )
                checksum_checks.append(f"{artifact_name}: mismatch")
    else:
        issues.append(ValidationIssue("checksums/", "missing checksums directory"))

    dataset_id = None
    if manifest_path.exists():
        try:
            dataset_id = _load_json(manifest_path).get("dataset_id")
        except ValueError:
            pass

    return DatasetValidationReport(
        dataset_id=dataset_id,
        passed=not issues,
        issues=issues,
        schema_checks=schema_checks,
        checksum_checks=checksum_checks,
        split_checks=split_checks,
    )
