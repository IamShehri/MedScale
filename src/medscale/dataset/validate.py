"""Dataset validation.

Stability: **public**. Validation is read-only and fails loudly on any mismatch.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

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


def validate_dataset(dataset_dir: Path) -> DatasetValidationReport:
    """Validate a dataset directory.

    Checks:
    - manifest.json exists and is valid JSON
    - schema.json exists and is valid JSON
    - splits/train.json, splits/validation.json, splits/test.json exist
    - checksums/manifest.json maps artifact paths to sha256 values and matches

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
    checksums_path = dataset_dir / "checksums" / "manifest.json"
    checksums_dir = dataset_dir / "checksums"

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

    checksums_manifest: dict[str, str] | None = None
    if checksums_path.exists():
        try:
            checksums_manifest = _load_json(checksums_path)
        except ValueError as exc:
            issues.append(ValidationIssue("checksums/manifest.json", str(exc)))

    expected_checksums: dict[str, str] = {}
    if checksums_manifest is not None:
        expected_checksums.update(checksums_manifest)
    elif checksums_dir.exists():
        for checksum_file in sorted(checksums_dir.glob("*.sha256")):
            try:
                expected_checksums[checksum_file.name] = (
                    checksum_file.read_text(encoding="utf-8").strip()
                )
            except OSError:
                continue

    if not expected_checksums:
        issues.append(ValidationIssue("checksums/", "missing checksums manifest"))
    else:
        for relative_path, expected_digest in expected_checksums.items():
            artifact_name = (
                relative_path[: -len(".sha256")]
                if relative_path.endswith(".sha256")
                else relative_path
            )
            if artifact_name.endswith(".json"):
                candidate = artifact_name[: -len(".json")]
            else:
                candidate = artifact_name
            if candidate == "manifest":
                artifact_path = dataset_dir / "manifest.json"
            elif candidate == "schema":
                artifact_path = dataset_dir / "schema.json"
            elif candidate in {"train", "validation", "test"}:
                artifact_path = dataset_dir / "splits" / f"{candidate}.json"
            else:
                artifact_path = (dataset_dir / artifact_name).resolve()
            if not artifact_path.exists():
                issues.append(
                    ValidationIssue(str(artifact_path), "missing artifact for checksum")
                )
                continue
            actual_digest = _sha256_file(artifact_path)
            if actual_digest == expected_digest:
                checksum_checks.append(f"{artifact_name}: match")
            else:
                issues.append(
                    ValidationIssue(
                        str(artifact_path),
                        "sha256 mismatch",
                    )
                )
                checksum_checks.append(f"{artifact_name}: mismatch")

    dataset_id = None
    if manifest_path.exists():
        with contextlib.suppress(ValueError):
            dataset_id = _load_json(manifest_path).get("dataset_id")

    return DatasetValidationReport(
        dataset_id=dataset_id,
        passed=not issues,
        issues=issues,
        schema_checks=schema_checks,
        checksum_checks=checksum_checks,
        split_checks=split_checks,
    )
