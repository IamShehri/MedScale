"""PRISMA state machine: legal flow, mandatory exclusion reasons, terminal states."""

from __future__ import annotations

import pytest

from medscale.litdb import ScreeningStage, ScreeningState, advance_stage


def test_full_inclusion_path() -> None:
    s = ScreeningState(ScreeningStage.IDENTIFIED)
    for stage in (
        ScreeningStage.DEDUPED,
        ScreeningStage.SCREENED,
        ScreeningStage.ELIGIBILITY,
        ScreeningStage.INCLUDED,
    ):
        s = advance_stage(s, stage)
    assert s.stage is ScreeningStage.INCLUDED


def test_exclusion_requires_reason() -> None:
    s = ScreeningState(ScreeningStage.SCREENED)
    with pytest.raises(ValueError, match="reason"):
        advance_stage(s, ScreeningStage.EXCLUDED)
    excluded = advance_stage(s, ScreeningStage.EXCLUDED, reason="off-topic to every RQ")
    assert excluded.reason == "off-topic to every RQ"


def test_reason_forbidden_outside_exclusion() -> None:
    with pytest.raises(ValueError, match="only recorded on EXCLUDED"):
        ScreeningState(ScreeningStage.INCLUDED, reason="looks great")


def test_stage_skipping_rejected() -> None:
    s = ScreeningState(ScreeningStage.IDENTIFIED)
    with pytest.raises(ValueError, match="illegal screening transition"):
        advance_stage(s, ScreeningStage.INCLUDED)


def test_included_can_be_excluded_with_reason() -> None:
    s = ScreeningState(ScreeningStage.INCLUDED)
    out = advance_stage(s, ScreeningStage.EXCLUDED, reason="source retracted")
    assert out.stage is ScreeningStage.EXCLUDED


def test_excluded_is_terminal() -> None:
    s = ScreeningState(ScreeningStage.EXCLUDED, reason="no resolvable identifier")
    with pytest.raises(ValueError, match="illegal screening transition"):
        advance_stage(s, ScreeningStage.IDENTIFIED)
