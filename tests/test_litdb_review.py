"""Human review layer: decisions, audit trail, append-only, PRISMA, resume."""

from __future__ import annotations

from pathlib import Path

import pytest

from medscale.litdb.review import (
    ExclusionReason,
    RecordReview,
    ReviewDecision,
    ReviewEvent,
    append_events,
    current_reviews,
    make_event,
    pending_queue,
    prisma_summary,
    replay_reviews,
    stage_for_decision,
)
from medscale.litdb.screening import ScreeningStage

_TS = "2026-07-10T00:00:00+00:00"
_SHA = "a3e0869"


def _event(record_id: str, decision: ReviewDecision, **kw: object) -> ReviewEvent:
    return make_event(
        record_id,
        decision,
        reviewer="operator",
        decided_at=_TS,
        software_version="0.0.0",
        git_sha=_SHA,
        **kw,  # type: ignore[arg-type]
    )


# --- decision -> stage mapping (state transitions) -------------------------------
def test_decision_stage_mapping() -> None:
    assert stage_for_decision(ReviewDecision.PENDING) is ScreeningStage.DEDUPED
    assert stage_for_decision(ReviewDecision.UNCERTAIN) is ScreeningStage.DEDUPED
    assert stage_for_decision(ReviewDecision.INCLUDE) is ScreeningStage.SCREENED
    assert stage_for_decision(ReviewDecision.EXCLUDE) is ScreeningStage.EXCLUDED
    assert stage_for_decision(ReviewDecision.DUPLICATE_CONFIRMED) is ScreeningStage.EXCLUDED


def test_event_records_prev_and_new_stage() -> None:
    event = _event("r1", ReviewDecision.INCLUDE, current=ReviewDecision.UNCERTAIN)
    d = event.to_dict()
    assert d["previous_decision"] == "uncertain" and d["previous_stage"] == "deduped"
    assert d["new_decision"] == "include" and d["new_stage"] == "screened"
    assert d["reviewer"] == "operator" and d["git_sha"] == _SHA and d["software_version"] == "0.0.0"


# --- invalid decisions / exclusion validation ------------------------------------
def test_exclude_requires_reason() -> None:
    with pytest.raises(ValueError, match="requires an exclusion_reason"):
        _event("r1", ReviewDecision.EXCLUDE)


def test_reason_forbidden_on_include() -> None:
    with pytest.raises(ValueError, match="only valid for EXCLUDE"):
        _event("r1", ReviewDecision.INCLUDE, exclusion_reason=ExclusionReason.NOT_RELEVANT)


def test_duplicate_confirmed_forces_duplicate_reason() -> None:
    with pytest.raises(ValueError, match="exclusion_reason=DUPLICATE"):
        _event("r1", ReviewDecision.DUPLICATE_CONFIRMED, exclusion_reason=ExclusionReason.OTHER)
    ok = _event(
        "r1", ReviewDecision.DUPLICATE_CONFIRMED, exclusion_reason=ExclusionReason.DUPLICATE
    )
    assert ok.new_decision is ReviewDecision.DUPLICATE_CONFIRMED


def test_pending_cannot_be_applied() -> None:
    with pytest.raises(ValueError, match="PENDING is the default"):
        _event("r1", ReviewDecision.PENDING)


def test_bad_git_sha_rejected() -> None:
    with pytest.raises(ValueError, match="git_sha"):
        make_event(
            "r1",
            ReviewDecision.INCLUDE,
            reviewer="op",
            decided_at=_TS,
            software_version="0.0.0",
            git_sha="nope",
        )


def test_empty_reviewer_rejected() -> None:
    with pytest.raises(ValueError, match="reviewer"):
        make_event(
            "r1",
            ReviewDecision.INCLUDE,
            reviewer="  ",
            decided_at=_TS,
            software_version="0.0.0",
            git_sha=_SHA,
        )


def test_naive_timestamp_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        make_event(
            "r1",
            ReviewDecision.INCLUDE,
            reviewer="op",
            decided_at="2026-07-10T00:00:00",
            software_version="0.0.0",
            git_sha=_SHA,
        )


# --- append-only + replay --------------------------------------------------------
def test_append_and_replay(tmp_path: Path) -> None:
    log = tmp_path / "review_log.jsonl"
    append_events(log, (_event("r1", ReviewDecision.INCLUDE),))
    append_events(
        log,
        (_event("r2", ReviewDecision.EXCLUDE, exclusion_reason=ExclusionReason.NOT_MEDICAL_AI),),
    )
    reviews = current_reviews(log)
    assert reviews["r1"] == RecordReview(ReviewDecision.INCLUDE)
    assert reviews["r2"].decision is ReviewDecision.EXCLUDE
    assert reviews["r2"].exclusion_reason is ExclusionReason.NOT_MEDICAL_AI


def test_correction_is_a_new_event_latest_wins(tmp_path: Path) -> None:
    log = tmp_path / "review_log.jsonl"
    append_events(log, (_event("r1", ReviewDecision.INCLUDE),))
    # corrected later to EXCLUDE - history preserved, latest wins
    append_events(
        log,
        (
            _event(
                "r1",
                ReviewDecision.EXCLUDE,
                current=ReviewDecision.INCLUDE,
                exclusion_reason=ExclusionReason.WRONG_OUTCOME,
            ),
        ),
    )
    assert len(log.read_text(encoding="utf-8").splitlines()) == 2  # nothing rewritten
    assert current_reviews(log)["r1"].decision is ReviewDecision.EXCLUDE


def test_append_is_lf_and_canonical(tmp_path: Path) -> None:
    log = tmp_path / "review_log.jsonl"
    append_events(log, (_event("r1", ReviewDecision.INCLUDE),))
    assert b"\r\n" not in log.read_bytes()


# --- resume behaviour (pending queue) --------------------------------------------
def test_pending_queue_never_seen_then_uncertain(tmp_path: Path) -> None:
    ids = ["a", "b", "c", "d"]
    log = tmp_path / "review_log.jsonl"
    append_events(
        log,
        (
            _event("a", ReviewDecision.INCLUDE),
            _event("b", ReviewDecision.UNCERTAIN),
        ),
    )
    reviews = current_reviews(log)
    # c, d never seen (first); b uncertain (revisit, last); a decided (gone)
    assert pending_queue(ids, reviews) == ("c", "d", "b")


def test_empty_log_all_pending() -> None:
    assert pending_queue(["a", "b"], {}) == ("a", "b")


# --- PRISMA calculations ---------------------------------------------------------
def test_prisma_summary_counts() -> None:
    ids = [f"r{i}" for i in range(6)]
    reviews = {
        "r0": RecordReview(ReviewDecision.INCLUDE),
        "r1": RecordReview(ReviewDecision.INCLUDE),
        "r2": RecordReview(ReviewDecision.EXCLUDE, ExclusionReason.NOT_RELEVANT),
        "r3": RecordReview(ReviewDecision.DUPLICATE_CONFIRMED, ExclusionReason.DUPLICATE),
        "r4": RecordReview(ReviewDecision.UNCERTAIN),
        # r5 unseen -> pending
    }
    summary = prisma_summary(ids, reviews, identified=1462)
    assert summary.identified == 1462
    assert summary.deduplicated == 6
    assert summary.included == 2
    assert summary.excluded == 2
    assert summary.uncertain == 1
    assert summary.pending == 1
    assert summary.screened == 4  # included + excluded (records decided)
    assert summary.exclusion_breakdown == {"duplicate": 1, "not_relevant": 1}


def test_prisma_reproducible_from_log(tmp_path: Path) -> None:
    log = tmp_path / "review_log.jsonl"
    append_events(
        log,
        (
            _event("a", ReviewDecision.INCLUDE),
            _event("b", ReviewDecision.EXCLUDE, exclusion_reason=ExclusionReason.OTHER),
        ),
    )
    reviews = replay_reviews(log.read_text(encoding="utf-8").splitlines())
    summary = prisma_summary(["a", "b", "c"], reviews)
    assert (summary.included, summary.excluded, summary.pending) == (1, 1, 1)
