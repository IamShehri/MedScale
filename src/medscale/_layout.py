"""Storage layout — the single internal source of truth for on-disk locations.

Stability: **internal**. Every path under a MedScale workspace root is named here and
nowhere else; a future storage-engine change edits this module plus the two store
modules, never the engine. The public API never exposes these values — user code knows
only the opaque workspace root.

The string values are frozen data-compatibility facts: changing one orphans committed
artifacts and breaks snapshot identities. Treat them like the identifier contract
(ADR-0017): changes require an ADR plus a migration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

#: Default workspace root used by CLI entry points.
DEFAULT_ROOT: Final = Path("data/litdb")

# --- knowledge artifacts (hashed into Research Snapshots; values are frozen) ---------
CORPUS: Final = "corpus/records.jsonl"
EVIDENCE: Final = "evidence/objects.jsonl"
SCREENING_LOG: Final = "screening/screening_log.jsonl"
REVIEW_LOG: Final = "screening/review_log.jsonl"
MERGE_LOG: Final = "screening/merge_log.jsonl"
UNCERTAIN_DUPLICATES: Final = "screening/uncertain_duplicates.jsonl"
UNCERTAIN_RESOLUTIONS: Final = "screening/uncertain_resolutions.jsonl"

# --- AI triage artifacts (advisory layer, never touches human logs) -----------------
TRIAGE_LOG: Final = "screening/ai_triage_log.jsonl"
TRIAGE_GOLDSET: Final = "evaluation/triage_goldset.jsonl"
EVALUATION_DIR: Final = "evaluation"

# --- derived / operational locations -------------------------------------------------
RAW_DIR: Final = "raw"
MANIFESTS_DIR: Final = "manifests"
REPORTS_DIR: Final = "reports"
SNAPSHOTS_DIR: Final = "snapshots"
BENCHMARKS_DIR: Final = "benchmarks"
FHIR_REPORTS_DIR: Final = "fhirkit/reports"
REVIEWERS_DIR: Final = "collaboration/reviewers"


def corpus_path(root: Path) -> Path:
    return root / CORPUS


def evidence_path(root: Path) -> Path:
    return root / EVIDENCE


def review_log_path(root: Path) -> Path:
    return root / REVIEW_LOG


def screening_log_path(root: Path) -> Path:
    return root / SCREENING_LOG


def merge_log_path(root: Path) -> Path:
    return root / MERGE_LOG


def uncertain_duplicates_path(root: Path) -> Path:
    return root / UNCERTAIN_DUPLICATES


def uncertain_resolutions_path(root: Path) -> Path:
    return root / UNCERTAIN_RESOLUTIONS


def triage_log_path(root: Path) -> Path:
    return root / TRIAGE_LOG


def triage_goldset_path(root: Path) -> Path:
    return root / TRIAGE_GOLDSET


def evaluation_dir(root: Path) -> Path:
    return root / EVALUATION_DIR


def manifests_dir(root: Path) -> Path:
    return root / MANIFESTS_DIR


def snapshots_dir(root: Path) -> Path:
    return root / SNAPSHOTS_DIR


def benchmarks_dir(root: Path) -> Path:
    return root / BENCHMARKS_DIR


def fhirkit_reports_dir(root: Path) -> Path:
    return root / FHIR_REPORTS_DIR


def reviewers_dir(root: Path) -> Path:
    return root / REVIEWERS_DIR


def collaboration_merges_dir(root: Path) -> Path:
    return root / "collaboration" / "merges"
