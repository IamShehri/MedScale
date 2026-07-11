"""Uncertain duplicate groups: loading, resolution state, and screening hints.

Dedupe pass 2 refuses to auto-merge ambiguous title matches; those groups need a human
verdict *before* screening proceeds blind. Resolution is PRISMA-standard and
ADR-0017-safe: extra copies are **excluded via attributed review events**
(``DUPLICATE_CONFIRMED``) — the corpus is never rewritten and no record_id changes, so
the ordering invariant is never at risk. "Distinct" verdicts are recorded in an
append-only resolutions log so a group is asked exactly once.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from medscale.litdb.records import LiteratureRecord
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json, content_hash

__all__ = [
    "GroupResolution",
    "UncertainGroup",
    "append_resolution",
    "duplicate_hints",
    "group_key",
    "load_groups",
    "load_resolutions",
    "unresolved_groups",
]


def group_key(record_ids: tuple[str, ...]) -> str:
    """Order-independent, content-derived identity of a group."""
    return content_hash({"record_ids": sorted(record_ids)})


@dataclass(frozen=True)
class UncertainGroup:
    record_ids: tuple[str, ...]
    normalized_title: str
    reason: str

    @property
    def key(self) -> str:
        return group_key(self.record_ids)


@dataclass(frozen=True)
class GroupResolution:
    """One human verdict on a group. ``kept_record_id`` is set iff duplicates confirmed."""

    key: str
    resolution: str  # "distinct" | "duplicates"
    reviewer: str
    decided_at: str
    kept_record_id: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        if self.resolution not in ("distinct", "duplicates"):
            raise ValueError(
                f"resolution must be 'distinct' or 'duplicates', got {self.resolution!r}"
            )
        if (self.resolution == "duplicates") != (self.kept_record_id is not None):
            raise ValueError("kept_record_id is required iff resolution == 'duplicates'")
        if not self.reviewer.strip():
            raise ValueError("reviewer must be non-empty")
        validate_timestamp(self.decided_at, "decided_at")

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "key": self.key,
            "resolution": self.resolution,
            "reviewer": self.reviewer,
            "decided_at": self.decided_at,
            "kept_record_id": self.kept_record_id,
            "notes": self.notes,
        }


def load_groups(path: Path) -> tuple[UncertainGroup, ...]:
    if not path.exists():
        return ()
    return tuple(
        UncertainGroup(
            record_ids=tuple(data["record_ids"]),
            normalized_title=str(data["normalized_title"]),
            reason=str(data["reason"]),
        )
        for data in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    )


def load_resolutions(path: Path) -> dict[str, GroupResolution]:
    """Latest resolution per group key (append-only log; last event wins)."""
    if not path.exists():
        return {}
    resolutions: dict[str, GroupResolution] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        resolution = GroupResolution(
            key=str(data["key"]),
            resolution=str(data["resolution"]),
            reviewer=str(data["reviewer"]),
            decided_at=str(data["decided_at"]),
            kept_record_id=data.get("kept_record_id"),
            notes=str(data.get("notes", "")),
        )
        resolutions[resolution.key] = resolution
    return resolutions


def append_resolution(path: Path, resolution: GroupResolution) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(resolution.to_dict()) + "\n")


def unresolved_groups(
    groups: tuple[UncertainGroup, ...], resolutions: dict[str, GroupResolution]
) -> tuple[UncertainGroup, ...]:
    return tuple(group for group in groups if group.key not in resolutions)


def duplicate_hints(
    groups: tuple[UncertainGroup, ...],
    resolutions: dict[str, GroupResolution],
    by_id: dict[str, LiteratureRecord],
) -> dict[str, str]:
    """record_id -> warning line for the screening display (unresolved groups only)."""
    hints: dict[str, str] = {}
    for group in unresolved_groups(groups, resolutions):
        for record_id in group.record_ids:
            others = [rid for rid in group.record_ids if rid != record_id]
            titles = "; ".join(
                (by_id[rid].title[:60] if rid in by_id else rid[:12]) for rid in others
            )
            hints[record_id] = (
                f"POSSIBLE DUPLICATE ({group.reason}) of: {titles} "
                "- resolve via `medscale screen duplicates`"
            )
    return hints
