"""M6 — Collaboration workflow tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.litdb.collaboration import (
    REVIEWERS_DIR,
    ReviewerIdentity,
    ReviewerLog,
    load_reviewer_events,
    load_reviewer_identity,
    merge_reviewer_logs,
    merge_summary,
    prisma_from_merged,
    reviewer_log_path,
    validate_merge_references,
    validate_reviewer_log,
    write_reviewer_identity,
)
from medscale.litdb.review import (
    ExclusionReason,
    ReviewDecision,
    make_event,
)

_TS = "2026-07-13T00:00:00+00:00"
_SHA = "1234567"
_VERSION = "medscale-v0.2"


def _event_dict(
    *,
    record_id: str = "rec1",
    previous_decision: ReviewDecision = ReviewDecision.PENDING,
    new_decision: ReviewDecision = ReviewDecision.INCLUDE,
    reviewer: str = "reviewer_a",
    exclusion_reason: ExclusionReason | None = None,
    notes: str = "",
) -> dict[str, object]:
    return make_event(
        record_id,
        new_decision,
        reviewer=reviewer,
        decided_at=_TS,
        software_version=_VERSION,
        git_sha=_SHA,
        current=previous_decision,
        exclusion_reason=exclusion_reason,
        notes=notes,
    ).to_dict()


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    return tmp_path / "workspace"


def test_reviewer_identity_deterministic(root: Path) -> None:
    expected_dict = {"reviewer_id": "alice", "metadata": {}}
    identity = ReviewerIdentity(reviewer_id="alice", metadata={})
    assert identity.to_dict() == expected_dict
    assert identity == ReviewerIdentity(reviewer_id="alice", metadata={})


def test_reviewer_log_requires_reviewer_id() -> None:
    with pytest.raises(ValueError):
        ReviewerLog(reviewer_id=" ", record_ids=(), decisions=(), created_at=_TS)


def test_validate_reviewer_log_missing_path(root: Path) -> None:
    report = validate_reviewer_log(root / REVIEWERS_DIR / "reviewer_a.jsonl")
    assert report.reviewer_id == "reviewer_a"
    assert report.event_count == 0
    assert report.is_clean


def test_reviewer_log_append_order_preserved(root: Path) -> None:
    path = root / REVIEWERS_DIR / "reviewer_a.jsonl"
    first = _event_dict(
        record_id="rec1",
        previous_decision=ReviewDecision.PENDING,
        new_decision=ReviewDecision.INCLUDE,
    )
    second = _event_dict(
        record_id="rec1",
        previous_decision=ReviewDecision.INCLUDE,
        new_decision=ReviewDecision.EXCLUDE,
        exclusion_reason=ExclusionReason.NOT_RELEVANT,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(first, sort_keys=True) + "\n" + json.dumps(second, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    events = load_reviewer_events(path)
    assert [event.new_decision for event in events] == [
        ReviewDecision.INCLUDE,
        ReviewDecision.EXCLUDE,
    ]


def test_validate_reviewer_log_detects_invalid_event(root: Path) -> None:
    path = reviewer_log_path(root, "reviewer_a")
    invalid_payload = json.dumps({"record_id": "rec1", "git_sha": "abc123"}, sort_keys=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(invalid_payload + "\n", encoding="utf-8")

    report = validate_reviewer_log(path)
    assert not report.is_clean
    assert any("invalid review event" in issue for issue in report.issues)


def test_merge_deterministic_order_and_conflict_visibility(root: Path) -> None:
    reviewer_a = reviewer_log_path(root, "reviewer_a")
    reviewer_b = reviewer_log_path(root, "reviewer_b")
    reviewer_a.parent.mkdir(parents=True, exist_ok=True)
    reviewer_b.parent.mkdir(parents=True, exist_ok=True)

    reviewer_a.write_text(
        "\n".join(
            json.dumps(
                _event_dict(
                    record_id=record_id,
                    previous_decision=ReviewDecision.PENDING,
                    new_decision=new_decision,
                    exclusion_reason=(
                        ExclusionReason.NOT_RELEVANT
                        if new_decision is ReviewDecision.EXCLUDE
                        else None
                    ),
                ),
                sort_keys=True,
            )
            for record_id, new_decision in [
                ("rec1", ReviewDecision.INCLUDE),
                ("rec2", ReviewDecision.EXCLUDE),
                ("rec3", ReviewDecision.INCLUDE),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    reviewer_b.write_text(
        "\n".join(
            json.dumps(
                _event_dict(
                    record_id=record_id,
                    previous_decision=ReviewDecision.PENDING,
                    new_decision=new_decision,
                    exclusion_reason=(
                        ExclusionReason.NOT_RELEVANT
                        if new_decision is ReviewDecision.EXCLUDE
                        else None
                    ),
                ),
                sort_keys=True,
            )
            for record_id, new_decision in [
                ("rec1", ReviewDecision.EXCLUDE),
                ("rec2", ReviewDecision.INCLUDE),
                ("rec3", ReviewDecision.INCLUDE),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    merged = merge_reviewer_logs(root, "reviewer_a", "reviewer_b")
    assert [c.record_id for c in merged.manifest.conflicts] == ["rec1", "rec2"]
    assert merged.manifest.conflicts[0].decision_a is ReviewDecision.INCLUDE
    assert merged.manifest.conflicts[0].decision_b is ReviewDecision.EXCLUDE
    assert merged.manifest.conflict_count == len(merged.manifest.conflicts)
    summary = merge_summary(merged)
    assert summary["include"] == 4


def test_two_reviewer_merge_reproduces_prisma_counts(root: Path) -> None:
    reviewer_a = reviewer_log_path(root, "reviewer_a")
    reviewer_b = reviewer_log_path(root, "reviewer_b")
    reviewer_a.parent.mkdir(parents=True, exist_ok=True)
    reviewer_b.parent.mkdir(parents=True, exist_ok=True)
    for reviewer_path, reviewer in ((reviewer_a, "reviewer_a"), (reviewer_b, "reviewer_b")):
        reviewer_path.write_text(
            "\n".join(
                json.dumps(
                    _event_dict(
                        record_id=record_id,
                        previous_decision=ReviewDecision.PENDING,
                        new_decision=ReviewDecision.INCLUDE,
                        reviewer=reviewer,
                    ),
                    sort_keys=True,
                )
                for record_id in ("rec1", "rec2", "rec3")
            )
            + "\n",
            encoding="utf-8",
        )

    merged_first = merge_reviewer_logs(root, "reviewer_a", "reviewer_b")
    merged_second = merge_reviewer_logs(root, "reviewer_a", "reviewer_b")
    prisma_first = prisma_from_merged(merged_first)
    prisma_second = prisma_from_merged(merged_second)
    assert prisma_first == prisma_second
    assert prisma_first["included"] == 3
    assert prisma_first["excluded"] == 0
    assert merged_first.manifest.manifest_hash == merged_second.manifest.manifest_hash


def test_merge_references_detects_missing_logs(root: Path) -> None:
    merged = merge_reviewer_logs(root, "missing_a", "missing_b")
    valid, issues = validate_merge_references(merged, root)
    assert not valid
    assert any("missing reviewer log" in issue for issue in issues)


def test_identity_emits_event_written_reviewer_id() -> None:
    root_dir = Path.cwd()
    identity = ReviewerIdentity(reviewer_id="alice", metadata={"role": "primary"})
    path = write_reviewer_identity(root_dir, identity)
    loaded = load_reviewer_identity(path)
    assert loaded == identity
