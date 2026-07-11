"""Uncertain-duplicate groups: loading, resolution log, hints, CLI resolution flow."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale import cli
from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.review import ReviewDecision, current_reviews
from medscale.litdb.store import write_corpus
from medscale.litdb.uncertain import (
    GroupResolution,
    UncertainGroup,
    append_resolution,
    duplicate_hints,
    group_key,
    load_groups,
    load_resolutions,
    unresolved_groups,
)
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(doi: str, title: str) -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title=title,
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, doi, _TS, "a" * 64),
        year=2025,
        abstract="An abstract.",
    )


def test_group_key_is_order_independent() -> None:
    assert group_key(("a", "b")) == group_key(("b", "a"))
    assert group_key(("a", "b")) != group_key(("a", "c"))


def test_resolution_validation() -> None:
    with pytest.raises(ValueError, match="kept_record_id is required iff"):
        GroupResolution(key="k", resolution="duplicates", reviewer="op", decided_at=_TS)
    with pytest.raises(ValueError, match="kept_record_id is required iff"):
        GroupResolution(
            key="k", resolution="distinct", reviewer="op", decided_at=_TS, kept_record_id="x"
        )
    with pytest.raises(ValueError, match="resolution must be"):
        GroupResolution(key="k", resolution="maybe", reviewer="op", decided_at=_TS)


def test_load_append_unresolved_roundtrip(tmp_path: Path) -> None:
    groups_path = tmp_path / "uncertain_duplicates.jsonl"
    groups_path.write_text(
        json.dumps({"record_ids": ["r1", "r2"], "normalized_title": "t", "reason": "x"}) + "\n",
        encoding="utf-8",
    )
    groups = load_groups(groups_path)
    assert len(groups) == 1 and groups[0].record_ids == ("r1", "r2")

    resolutions_path = tmp_path / "uncertain_resolutions.jsonl"
    assert unresolved_groups(groups, load_resolutions(resolutions_path)) == groups
    append_resolution(
        resolutions_path,
        GroupResolution(key=groups[0].key, resolution="distinct", reviewer="op", decided_at=_TS),
    )
    assert unresolved_groups(groups, load_resolutions(resolutions_path)) == ()


def test_duplicate_hints_only_for_unresolved() -> None:
    a, b = (
        _record("10.1/a", "Same title of paper here"),
        _record("10.1/b", "Same title of paper here"),
    )
    group = UncertainGroup((a.record_id, b.record_id), "same title of paper here", "conflict")
    by_id = {a.record_id: a, b.record_id: b}
    hints = duplicate_hints((group,), {}, by_id)
    assert a.record_id in hints and b.record_id in hints
    assert "POSSIBLE DUPLICATE" in hints[a.record_id]
    resolved = {group.key: GroupResolution(group.key, "distinct", "op", _TS)}
    assert duplicate_hints((group,), resolved, by_id) == {}


def _seed(root: Path) -> tuple[LiteratureRecord, LiteratureRecord]:
    a = _record("10.1/a", "A very specific duplicate candidate title")
    b = _record("10.1/b", "A very specific duplicate candidate title")
    write_corpus(root / "corpus" / "records.jsonl", [a, b])
    screening = root / "screening"
    screening.mkdir(parents=True, exist_ok=True)
    (screening / "uncertain_duplicates.jsonl").write_text(
        json.dumps(
            {
                "record_ids": [a.record_id, b.record_id],
                "normalized_title": "a very specific duplicate candidate title",
                "reason": "conflicting identifiers of the same type",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return a, b


def test_cli_duplicates_keep_one(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    a, b = _seed(tmp_path)
    answers = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    rc = cli.main(["screen", "duplicates", "--root", str(tmp_path), "--reviewer", "tester"])
    assert rc == 0
    reviews = current_reviews(tmp_path / "screening" / "review_log.jsonl")
    assert set(reviews) == {b.record_id}  # kept member has no review event
    assert reviews[b.record_id].decision is ReviewDecision.DUPLICATE_CONFIRMED
    resolutions = load_resolutions(tmp_path / "screening" / "uncertain_resolutions.jsonl")
    (resolution,) = resolutions.values()
    assert resolution.kept_record_id == a.record_id
    # second run: nothing left to resolve
    rc = cli.main(["screen", "duplicates", "--root", str(tmp_path)])
    assert rc == 0


def test_cli_duplicates_all_distinct(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed(tmp_path)
    answers = iter(["d"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    assert cli.main(["screen", "duplicates", "--root", str(tmp_path)]) == 0
    assert not (tmp_path / "screening" / "review_log.jsonl").exists()  # no review events
    resolutions = load_resolutions(tmp_path / "screening" / "uncertain_resolutions.jsonl")
    (resolution,) = resolutions.values()
    assert resolution.resolution == "distinct"


def test_screening_display_carries_hint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _seed(tmp_path)
    answers = iter(["q"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    cli.main(["screen", "next", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert "POSSIBLE DUPLICATE" in out
