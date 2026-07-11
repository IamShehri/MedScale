"""Referential integrity: orphan detection, merge lineage, real-corpus cleanliness."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from medscale.litdb.integrity import Merge, check_litdb, check_references, main

_ROOT = Path(__file__).resolve().parents[1] / "data" / "litdb"


def test_clean_when_all_refs_resolve() -> None:
    report = check_references(
        {"a", "b", "c"},
        review_ref_ids={"a"},
        screening_ref_ids={"a", "b"},
        merges=(Merge("a", ("x", "y")),),  # sources x,y correctly absent from corpus
    )
    assert report.is_clean
    assert report.corpus_size == 3


def test_orphaned_review_ref_detected() -> None:
    report = check_references(
        {"a"}, review_ref_ids={"a", "ghost"}, screening_ref_ids=set(), merges=()
    )
    assert not report.is_clean
    (issue,) = report.issues
    assert issue.kind == "orphaned_review_ref"
    assert issue.record_id == "ghost"


def test_orphaned_screening_ref_detected() -> None:
    report = check_references({"a"}, review_ref_ids=set(), screening_ref_ids={"gone"}, merges=())
    assert [i.kind for i in report.issues] == ["orphaned_screening_ref"]


def test_broken_merge_lineage_detected() -> None:
    report = check_references(
        {"other"},
        review_ref_ids=set(),
        screening_ref_ids=set(),
        merges=(Merge("missing_merged", ("s1",)),),
    )
    assert any(i.kind == "broken_merge_lineage" for i in report.issues)


def test_resurrected_merged_source_detected() -> None:
    # a merged-away source id must not still be in the corpus
    report = check_references(
        {"merged", "s1"},
        review_ref_ids=set(),
        screening_ref_ids=set(),
        merges=(Merge("merged", ("s1",)),),
    )
    assert any(i.kind == "resurrected_merged_source" for i in report.issues)


def test_the_documented_hazard() -> None:
    """A decision keyed to a merged-away id is exactly what the check catches."""
    corpus = {"merged"}  # after dedupe: only the merged record survives
    report = check_references(
        corpus,
        review_ref_ids={"old_source"},  # decision made before dedupe, now orphaned
        screening_ref_ids=set(),
        merges=(Merge("merged", ("old_source", "other_source")),),
    )
    assert not report.is_clean
    assert any(
        i.record_id == "old_source" and i.kind == "orphaned_review_ref" for i in report.issues
    )


@pytest.mark.skipif(not (_ROOT / "corpus" / "records.jsonl").exists(), reason="no corpus")
def test_real_litdb_is_clean() -> None:
    report = check_litdb(_ROOT)
    assert report.corpus_size == 1346
    assert report.merges == 40
    assert report.is_clean, [i.to_dict() for i in report.issues]


@pytest.mark.skipif(not (_ROOT / "corpus" / "records.jsonl").exists(), reason="no corpus")
def test_cli_check_exit_code_clean() -> None:
    assert main(["--root", str(_ROOT)]) == 0


def test_cli_check_nonzero_on_dirty(tmp_path: Path) -> None:
    (tmp_path / "corpus").mkdir()
    (tmp_path / "corpus" / "records.jsonl").write_text("", encoding="utf-8")
    (tmp_path / "screening").mkdir()
    (tmp_path / "screening" / "review_log.jsonl").write_text(
        json.dumps({"record_id": "ghost"}) + "\n", encoding="utf-8"
    )
    assert main(["--root", str(tmp_path)]) == 1  # orphan => non-zero for CI gating
