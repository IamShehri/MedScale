"""Screening CLI: pure formatting/decision helpers, status, and dispatch."""

from __future__ import annotations

from pathlib import Path

from medscale import cli
from medscale.litdb import EvidenceTier, Identifiers, LiteratureRecord
from medscale.litdb.review import ExclusionReason, ReviewDecision, current_reviews
from medscale.litdb.screen_cli import (
    build_event,
    decision_for_key,
    format_record,
)
from medscale.litdb.screen_cli import main as screen_main
from medscale.litdb.store import write_corpus
from medscale.provenance import Provenance, SourceAPI

_TS = "2026-07-10T00:00:00+00:00"


def _record(doi: str, title: str = "A study of grammar-constrained FHIR") -> LiteratureRecord:
    return LiteratureRecord(
        identifiers=Identifiers(doi=doi),
        title=title,
        evidence_tier=EvidenceTier.PEER_REVIEWED,
        provenance=Provenance(SourceAPI.OPENALEX, doi, _TS, "a" * 64),
        year=2025,
        venue="J. Med. AI",
        authors=("A. Author", "B. Author"),
        abstract="We study constrained decoding for FHIR.",
    )


def test_decision_for_key() -> None:
    assert decision_for_key("1") == (ReviewDecision.INCLUDE, False)
    assert decision_for_key("2") == (ReviewDecision.EXCLUDE, True)
    assert decision_for_key("3") == (ReviewDecision.UNCERTAIN, False)
    assert decision_for_key("4") == (ReviewDecision.DUPLICATE_CONFIRMED, False)
    assert decision_for_key("5") is None  # skip
    assert decision_for_key("x") is None


def test_format_record_chrome_is_ascii() -> None:
    """Display chrome must survive cp1252 consoles (only record CONTENT may be Unicode)."""
    record = _record("10.1/ascii", "Plain ascii title")
    text = format_record(record, position=1, remaining=1)
    text.encode("ascii")  # raises if any decorative character is non-ASCII


def test_format_record_shows_key_fields() -> None:
    text = format_record(_record("10.1/x"), position=1, remaining=5)
    assert "grammar-constrained FHIR" in text
    assert "A. Author" in text
    assert "doi=10.1/x" in text
    assert "5 remaining" in text
    assert "[1] Include" in text


def test_build_event_is_attributed() -> None:
    event = build_event(
        "rec1",
        ReviewDecision.EXCLUDE,
        reviewer="alice",
        current=ReviewDecision.PENDING,
        exclusion_reason=ExclusionReason.NOT_MEDICAL_AI,
        notes="off topic",
        now=_TS,
        git_sha="abcdef1",
    )
    assert event.reviewer == "alice"
    assert event.notes == "off topic"
    assert event.exclusion_reason is ExclusionReason.NOT_MEDICAL_AI
    assert event.decided_at == _TS


def _seed_corpus(root: Path) -> None:
    write_corpus(
        root / "corpus" / "records.jsonl",
        [_record("10.1/a"), _record("10.1/b", "Another paper entirely")],
    )


def test_status_command_runs(tmp_path: Path, capsys: object) -> None:
    _seed_corpus(tmp_path)
    rc = cli.main(["screen", "status", "--root", str(tmp_path)])
    assert rc == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "deduplicated : 2" in out
    assert "pending      : 2" in out


def test_unknown_command_errors() -> None:
    assert cli.main(["frobnicate"]) == 2


def test_help_is_zero_with_flag() -> None:
    assert cli.main(["--help"]) == 0


def test_screen_main_status_direct(tmp_path: Path) -> None:
    _seed_corpus(tmp_path)
    assert screen_main(["status", "--root", str(tmp_path)]) == 0


def test_interactive_include_then_status(tmp_path: Path, monkeypatch: object) -> None:
    _seed_corpus(tmp_path)
    # include the first queued record, then quit
    inputs = iter(["1", "", "q"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))  # type: ignore[attr-defined]
    rc = cli.main(["screen", "next", "--root", str(tmp_path), "--reviewer", "tester"])
    assert rc == 0
    reviews = current_reviews(tmp_path / "screening" / "review_log.jsonl")
    assert len(reviews) == 1
    (decision,) = {r.decision for r in reviews.values()}
    assert decision is ReviewDecision.INCLUDE
