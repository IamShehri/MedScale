"""Benchmark validation: a benchmark that cannot prove its substrate does not run.

Checks (each failure is a named issue, never an exception mid-list):

1. the referenced Research Snapshot exists on disk and **verifies against the tree**
   (gold standards cannot move under a benchmark);
2. every evidence id referenced by any task input or gold resolves in the evidence
   store of that tree;
3. every referenced evidence object meets the spec's ``min_verification`` state;
4. task types are implemented (reserved extension points rejected);
5. structural sanity (duplicate task ids are rejected at write time; re-checked here).
"""

from __future__ import annotations

import json
from pathlib import Path

import medscale._layout as _layout
from medscale.bench.spec import IMPLEMENTED_TASK_TYPES, BenchmarkSpec
from medscale.bench.tasks import TaskItem
from medscale.evidence import VerificationState
from medscale.evidence_store import load_evidence
from medscale.research.snapshot import ResearchSnapshot, load_snapshot, verify_snapshot

__all__ = ["find_snapshot", "validate_benchmark"]

_ORDER: dict[VerificationState, int] = {
    VerificationState.UNVERIFIED: 0,
    VerificationState.DISPUTED: 0,
    VerificationState.RETRACTED: 0,
    VerificationState.SOURCE_VERIFIED: 1,
    VerificationState.EXTRACTION_VERIFIED: 2,
}


def find_snapshot(root: Path, snapshot_id: str) -> ResearchSnapshot | None:
    snapshots_dir = _layout.snapshots_dir(root)
    if not snapshots_dir.exists():
        return None
    for path in sorted(snapshots_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("snapshot_id") == snapshot_id:
            return load_snapshot(path)
    return None


def validate_benchmark(
    root: Path, spec: BenchmarkSpec, items: tuple[TaskItem, ...]
) -> tuple[str, ...]:
    """Return every validity issue (empty tuple = the benchmark is scientifically runnable)."""
    issues: list[str] = []

    snapshot = find_snapshot(root, spec.snapshot_id)
    if snapshot is None:
        issues.append(f"snapshot {spec.snapshot_id[:12]}... not found under snapshots/")
    else:
        for mismatch in verify_snapshot(root, snapshot):
            issues.append(f"snapshot drift: {mismatch}")

    evidence = {obj.evidence_id: obj for obj in load_evidence(_layout.evidence_path(root))}
    minimum = _ORDER[spec.min_verification]

    task_ids: set[str] = set()
    for item in items:
        if item.task_id in task_ids:
            issues.append(f"{item.task_id}: duplicate task_id")
        task_ids.add(item.task_id)
        if item.task_type not in IMPLEMENTED_TASK_TYPES:
            issues.append(f"{item.task_id}: reserved task type {item.task_type.value}")
        if item.task_type not in spec.task_types:
            issues.append(f"{item.task_id}: task type not declared by the spec")
        for evidence_id in sorted(item.gold.all_ids | set(item.input_evidence_ids)):
            obj = evidence.get(evidence_id)
            if obj is None:
                issues.append(f"{item.task_id}: evidence {evidence_id[:12]}... not in store")
            elif _ORDER[obj.verification] < minimum:
                issues.append(
                    f"{item.task_id}: evidence {evidence_id[:12]}... is "
                    f"{obj.verification.value}, below required {spec.min_verification.value}"
                )
    return tuple(issues)
