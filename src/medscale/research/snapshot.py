"""Research Snapshots: the exact state of MedScale knowledge at time T, citable.

A paper says "generated from snapshot ``a1b2c3...``" and any lab, in any year, can
``verify`` that a repository tree matches it — every knowledge artifact is hashed
(file bytes), the frozen query set is content-hashed, and the snapshot id is itself a
content hash of the whole description. Verification recomputes everything; a mismatch
names the artifact that drifted. Future surface: ``GET /snapshots``.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import medscale._layout as _layout
from medscale.litdb.queries import QUERY_SET
from medscale.provenance import validate_timestamp
from medscale.reproducibility import canonical_json, content_hash

__all__ = [
    "ResearchSnapshot",
    "capture_snapshot",
    "load_snapshot",
    "verify_snapshot",
    "write_snapshot",
]

_GIT_SHA: Final = re.compile(r"^[0-9a-f]{7,40}$")

#: Every knowledge artifact a snapshot pins: (key, path relative to the litdb root).
_ARTIFACTS: Final[tuple[tuple[str, str], ...]] = (
    ("corpus", _layout.CORPUS),
    ("evidence", _layout.EVIDENCE),
    ("screening_log", _layout.SCREENING_LOG),
    ("review_log", _layout.REVIEW_LOG),
    ("merge_log", _layout.MERGE_LOG),
    ("uncertain_resolutions", _layout.UNCERTAIN_RESOLUTIONS),
)


def _file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _query_set_hash() -> str:
    return content_hash(
        [
            {
                "query_id": spec.query_id,
                "domain_tag": spec.domain_tag,
                "concept_query": spec.concept_query,
                "rq_refs": list(spec.rq_refs),
            }
            for spec in QUERY_SET
        ]
    )


@dataclass(frozen=True)
class ResearchSnapshot:
    """A content-addressed description of one knowledge state."""

    created_at: str
    git_sha: str
    software_version: str
    query_set_sha256: str
    artifact_hashes: dict[str, str | None]

    def __post_init__(self) -> None:
        validate_timestamp(self.created_at, "created_at")
        if not _GIT_SHA.match(self.git_sha):
            raise ValueError(f"git_sha must be 7-40 hex chars, got {self.git_sha!r}")
        missing = {key for key, _ in _ARTIFACTS} - set(self.artifact_hashes)
        if missing:
            raise ValueError(f"artifact_hashes missing keys: {sorted(missing)}")

    @property
    def snapshot_id(self) -> str:
        """Identity of the *knowledge state* (not of when/who captured it)."""
        return content_hash(
            {
                "query_set_sha256": self.query_set_sha256,
                "artifact_hashes": self.artifact_hashes,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": 1,
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "git_sha": self.git_sha,
            "software_version": self.software_version,
            "query_set_sha256": self.query_set_sha256,
            "artifact_hashes": self.artifact_hashes,
        }


def capture_snapshot(
    root: Path, *, git_sha: str, software_version: str, created_at: str
) -> ResearchSnapshot:
    """Hash every knowledge artifact under ``root`` into a snapshot (pure given a tree)."""
    return ResearchSnapshot(
        created_at=created_at,
        git_sha=git_sha,
        software_version=software_version,
        query_set_sha256=_query_set_hash(),
        artifact_hashes={key: _file_sha256(root / rel) for key, rel in _ARTIFACTS},
    )


def write_snapshot(root: Path, snapshot: ResearchSnapshot) -> Path:
    target = _layout.snapshots_dir(root) / f"{snapshot.snapshot_id[:16]}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_json(snapshot.to_dict()) + "\n", encoding="utf-8", newline="\n")
    return target


def load_snapshot(path: Path) -> ResearchSnapshot:
    data = json.loads(path.read_text(encoding="utf-8"))
    snapshot = ResearchSnapshot(
        created_at=data["created_at"],
        git_sha=data["git_sha"],
        software_version=data["software_version"],
        query_set_sha256=data["query_set_sha256"],
        artifact_hashes=dict(data["artifact_hashes"]),
    )
    stored_id = data.get("snapshot_id")
    if stored_id is not None and stored_id != snapshot.snapshot_id:
        raise ValueError(
            f"snapshot file id {stored_id[:12]}... does not match recomputed identity "
            f"{snapshot.snapshot_id[:12]}... (file tampered or hand-edited)"
        )
    return snapshot


def verify_snapshot(root: Path, snapshot: ResearchSnapshot) -> tuple[str, ...]:
    """Recompute every hash against the tree; return mismatch descriptions (empty = verified)."""
    mismatches: list[str] = []
    if _query_set_hash() != snapshot.query_set_sha256:
        mismatches.append("query_set: frozen query set differs from snapshot")
    for key, rel in _ARTIFACTS:
        actual = _file_sha256(root / rel)
        expected = snapshot.artifact_hashes.get(key)
        if actual != expected:
            mismatches.append(
                f"{key}: expected {(expected or 'absent')[:12]}, found {(actual or 'absent')[:12]}"
            )
    return tuple(mismatches)
