"""Dataset release manifest, audit report, and quality report contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from medscale.dataset.builder.contracts import (
    _validate_boolean,
    _validate_counts,
    _validate_identifier,
    _validate_json_compatible_mapping,
    _validate_mapping,
    _validate_proportions,
    _validate_tuple_members,
)

__all__ = [
    "AuditReport",
    "DatasetReleaseManifest",
    "QualityReport",
]


def _freeze_mapping(value: dict[str, Any]) -> Any:
    return _deep_freeze(value)


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return _FrozenMapping({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    if isinstance(value, set):
        raise TypeError(f"sets are not JSON-compatible: {value!r}")
    return value


class _FrozenMapping(dict[str, Any]):
    """Immutable, JSON-compatible mapping."""

    def __setitem__(self, key: object, value: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def __delitem__(self, key: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def pop(self, *args: object, **kwargs: object) -> Any:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def popitem(self, *args: object, **kwargs: object) -> tuple[Any, Any]:
        raise TypeError("FrozenMapping objects do not support item assignment")

    def setdefault(
        self,
        *args: object,
        **kwargs: object,
    ) -> Any:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def update(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")

    def clear(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - always raises
        raise TypeError("FrozenMapping objects do not support item assignment")


@dataclass(frozen=True)
class DatasetReleaseManifest:
    """Immutable release metadata for a published dataset."""

    dataset_id: str
    dataset_version: str
    dataset_fingerprint: str
    release_id: str
    released_at: str
    released_by: str
    dataset_manifest_sha256: str
    bundle_id_registry_sha256: str
    validation_summary: dict[str, Any] = field(default_factory=dict)
    quality_summary: dict[str, Any] = field(default_factory=dict)
    release_notes: str = ""
    previous_release_id: str | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.dataset_id, "dataset_id")
        _validate_identifier(self.dataset_version, "dataset_version")
        _validate_identifier(self.dataset_fingerprint, "dataset_fingerprint")
        _validate_identifier(self.release_id, "release_id")
        _validate_identifier(self.released_at, "released_at")
        _validate_identifier(self.released_by, "released_by")
        _validate_identifier(self.dataset_manifest_sha256, "dataset_manifest_sha256")
        _validate_identifier(self.bundle_id_registry_sha256, "bundle_id_registry_sha256")
        _validate_json_compatible_mapping(self.validation_summary, "validation_summary")
        _validate_json_compatible_mapping(self.quality_summary, "quality_summary")
        object.__setattr__(self, "validation_summary", _deep_freeze(self.validation_summary))
        object.__setattr__(self, "quality_summary", _deep_freeze(self.quality_summary))


@dataclass(frozen=True)
class AuditReport:
    """Immutable audit report for a dataset pipeline run."""

    dataset_id: str
    dataset_version: str
    audit_timestamp: str
    green: bool
    record_count: int
    coverage_report_version: str | None = None
    analytics_report_version: str | None = None
    bundle_ids: tuple[str, ...] = ()
    validation_statuses: dict[str, str] = field(default_factory=dict)
    rejection_counts: dict[str, int] = field(default_factory=dict)
    checksum_verification: dict[str, str] = field(default_factory=dict)
    failures: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_identifier(self.dataset_id, "dataset_id")
        _validate_identifier(self.dataset_version, "dataset_version")
        _validate_identifier(self.audit_timestamp, "audit_timestamp")
        _validate_boolean("green", self.green)
        _validate_counts(record_count=self.record_count)
        for label, value in self.rejection_counts.items():
            _validate_counts(**{label: value})
        _validate_mapping(self.rejection_counts, "rejection_counts")
        _validate_tuple_members(self.bundle_ids, str, "bundle_ids")
        _validate_mapping(self.validation_statuses, "validation_statuses")
        _validate_mapping(self.checksum_verification, "checksum_verification")
        _validate_tuple_members(self.failures, str, "failures")
        object.__setattr__(self, "validation_statuses", _deep_freeze(self.validation_statuses))
        object.__setattr__(self, "rejection_counts", _deep_freeze(self.rejection_counts))
        object.__setattr__(self, "checksum_verification", _deep_freeze(self.checksum_verification))


@dataclass(frozen=True)
class QualityReport:
    """Immutable quality summary for a dataset release."""

    dataset_id: str
    dataset_version: str
    stage_quality_summaries: dict[str, dict[str, Any]] = field(default_factory=dict)
    rejection_counts: dict[str, int] = field(default_factory=dict)
    synthetic_proportions: dict[str, float] = field(default_factory=dict)
    license_audit: dict[str, Any] = field(default_factory=dict)
    bias_monitoring_summary: dict[str, Any] = field(default_factory=dict)
    contamination_summary: dict[str, Any] = field(default_factory=dict)
    benchmark_linkage_status: dict[str, Any] = field(default_factory=dict)
    green: bool = False

    def __post_init__(self) -> None:
        _validate_identifier(self.dataset_id, "dataset_id")
        _validate_identifier(self.dataset_version, "dataset_version")
        _validate_boolean("green", self.green)
        _validate_proportions(self.synthetic_proportions, "synthetic_proportions")
        mapping_fields = (
            "stage_quality_summaries",
            "license_audit",
            "bias_monitoring_summary",
            "contamination_summary",
            "benchmark_linkage_status",
        )
        for field_name in mapping_fields:
            value = getattr(self, field_name)
            _validate_json_compatible_mapping(value, field_name)
            object.__setattr__(self, field_name, _deep_freeze(value))
        object.__setattr__(self, "rejection_counts", _deep_freeze(self.rejection_counts))
        object.__setattr__(self, "synthetic_proportions", _deep_freeze(self.synthetic_proportions))
