"""Dataset release manifest, audit report, and quality report contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
