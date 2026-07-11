"""Referential integrity for the litdb corpus and its append-only logs.

The corpus and the screening/review logs are coupled by ``record_id``. Because fuzzy
dedupe mints a *new* ``record_id`` and removes the merged sources, a decision recorded
against a since-merged id would be orphaned — a silent reproducibility break. This
module makes that guarantee *checkable*: every id referenced by a log must resolve to a
live corpus record, merged records must be present, and merged-away sources must be
absent. It is the enforcement mechanism behind ADR-0017.

Pure core (``check_references``) + an I/O wrapper (``check_litdb``) + a CLI entry.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import medscale._layout as _layout
from medscale.litdb.store import load_corpus

__all__ = [
    "IntegrityIssue",
    "IntegrityReport",
    "Merge",
    "check_litdb",
    "check_references",
]

_REVIEW_LOG: Final = _layout.REVIEW_LOG
_SCREENING_LOG: Final = _layout.SCREENING_LOG
_MERGE_LOG: Final = _layout.MERGE_LOG
_CORPUS: Final = _layout.CORPUS
_EVIDENCE: Final = _layout.EVIDENCE


@dataclass(frozen=True)
class IntegrityIssue:
    kind: str
    record_id: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "record_id": self.record_id, "detail": self.detail}


@dataclass(frozen=True)
class Merge:
    merged_record_id: str
    source_record_ids: tuple[str, ...]


@dataclass(frozen=True)
class IntegrityReport:
    corpus_size: int
    review_refs: int
    screening_refs: int
    merges: int
    issues: tuple[IntegrityIssue, ...]
    evidence_refs: int = 0

    @property
    def is_clean(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "corpus_size": self.corpus_size,
            "review_refs": self.review_refs,
            "screening_refs": self.screening_refs,
            "merges": self.merges,
            "evidence_refs": self.evidence_refs,
            "clean": self.is_clean,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def check_references(
    corpus_ids: set[str],
    *,
    review_ref_ids: set[str],
    screening_ref_ids: set[str],
    merges: Iterable[Merge],
    evidence_source_ids: set[str] | None = None,
) -> IntegrityReport:
    """Pure integrity check over id sets. Deterministic issue ordering."""
    issues: list[IntegrityIssue] = []
    merges = tuple(merges)
    evidence_source_ids = evidence_source_ids or set()

    for ref in sorted(evidence_source_ids - corpus_ids):
        issues.append(
            IntegrityIssue(
                "orphaned_evidence_ref",
                ref,
                "evidence object references a source record not in the corpus",
            )
        )

    for ref in sorted(review_ref_ids - corpus_ids):
        issues.append(
            IntegrityIssue(
                "orphaned_review_ref", ref, "review decision references a record not in the corpus"
            )
        )
    for ref in sorted(screening_ref_ids - corpus_ids):
        issues.append(
            IntegrityIssue(
                "orphaned_screening_ref",
                ref,
                "screening decision references a record not in the corpus",
            )
        )
    for merge in merges:
        if merge.merged_record_id not in corpus_ids:
            issues.append(
                IntegrityIssue(
                    "broken_merge_lineage",
                    merge.merged_record_id,
                    "merged record is missing from the corpus",
                )
            )
        for source in merge.source_record_ids:
            if source in corpus_ids:
                issues.append(
                    IntegrityIssue(
                        "resurrected_merged_source",
                        source,
                        "a merged-away source record is still present in the corpus",
                    )
                )

    return IntegrityReport(
        corpus_size=len(corpus_ids),
        review_refs=len(review_ref_ids),
        screening_refs=len(screening_ref_ids),
        merges=len(merges),
        issues=tuple(issues),
        evidence_refs=len(evidence_source_ids),
    )


def _referenced_ids(path: Path, key: str) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(str(json.loads(line)[key]))
    return ids


def _load_merges(path: Path) -> tuple[Merge, ...]:
    if not path.exists():
        return ()
    merges: list[Merge] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        merges.append(Merge(str(data["merged_record_id"]), tuple(data["source_record_ids"])))
    return tuple(merges)


def check_litdb(root: Path) -> IntegrityReport:
    """Run the integrity check over a ``data/litdb`` directory."""
    corpus_ids = {record.record_id for record in load_corpus(root / _CORPUS)}
    evidence_sources: set[str] = set()
    evidence_path = root / _EVIDENCE
    if evidence_path.exists():
        for line in evidence_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                source = json.loads(line).get("source_record_id")
                if source:
                    evidence_sources.add(str(source))
    return check_references(
        corpus_ids,
        review_ref_ids=_referenced_ids(root / _REVIEW_LOG, "record_id"),
        screening_ref_ids=_referenced_ids(root / _SCREENING_LOG, "record_id"),
        merges=_load_merges(root / _MERGE_LOG),
        evidence_source_ids=evidence_sources,
    )


def format_report(report: IntegrityReport) -> str:
    lines = [
        "MedScale litdb integrity",
        f"  corpus records  : {report.corpus_size}",
        f"  review refs     : {report.review_refs}",
        f"  screening refs  : {report.screening_refs}",
        f"  merges          : {report.merges}",
        f"  evidence refs   : {report.evidence_refs}",
        f"  status          : {'CLEAN' if report.is_clean else 'ISSUES FOUND'}",
    ]
    for issue in report.issues:
        lines.append(f"    ! {issue.kind}: {issue.record_id} — {issue.detail}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(0)
