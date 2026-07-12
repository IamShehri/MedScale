"""AI Triage CLI: `medscale screen triage`.

Advisory prioritization layer only. Does not modify human review logs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Final

import medscale._layout as _layout
from medscale.cli import _common
from medscale.litdb.ai_triage import (
    AI_TRIAGE_SIGNALS,
    AIRecommendation,
    append_recommendations,
    build_recommendation,
    detect_deterministic_flags,
    detect_ontology_signals,
    load_triage_log,
    pending_for_triage,
    score_triage,
)
from medscale.litdb.store import load_corpus
from medscale.litdb.review import current_reviews

_DEFAULT_ROOT: Final = _layout.DEFAULT_ROOT


def _priority_label(priority_score: float) -> str:
    if priority_score >= 0.7:
        return "HIGH"
    if priority_score >= 0.45:
        return "MEDIUM"
    if priority_score >= 0.25:
        return "LOW"
    return "LOW"


def _print_recommendation(recommendation: AIRecommendation, record_title: str) -> None:
    priority_score = recommendation.priority_score
    print("--------------------------------")
    print("Title:")
    print(record_title)
    print()
    print("Priority:")
    print(_priority_label(priority_score))
    print()
    print("Signals:")
    signals = recommendation.ontology_signals or ["(none)"]
    print("\n".join(f"  {signal}" for signal in signals))
    print()
    print("Reason:")
    print(recommendation.reasoning)
    print()
    print("AI recommendation:")
    print(recommendation.recommendation)
    print()
    print("Confidence:")
    print(f"{recommendation.confidence:.2f}")
    print("--------------------------------")


def _run_status(root: Path) -> int:
    corpus = load_corpus(_layout.corpus_path(root))
    reviews = current_reviews(_layout.review_log_path(root))
    pending = pending_for_triage(corpus, reviews, query=None, limit=None)
    triage_recommendations = load_triage_log(_layout.triage_log_path(root))
    high = sum(1 for r in triage_recommendations.values() if r.priority_score >= 0.7 and r.relevance_score >= 0.55)
    medium = sum(1 for r in triage_recommendations.values() if 0.45 <= r.priority_score < 0.7 and 0.35 <= r.relevance_score < 0.55)
    total_triaged = len(triage_recommendations)
    print("MedScale AI Triage status")
    print(f"  corpus        : {len(corpus)} records")
    print(f"  pending       : {len(pending)} records awaiting human review")
    print(f"  triaged       : {total_triaged} records")
    print(f"  high priority : {high}")
    print(f"  medium priority: {medium}")
    return 0


def _run_recommend(root: Path, query: str | None, limit: int | None) -> int:
    corpus = load_corpus(_layout.corpus_path(root))
    reviews = current_reviews(_layout.review_log_path(root))
    pending = pending_for_triage(corpus, reviews, query=query, limit=limit)
    if not pending:
        print("no pending records for triage.")
        return 0
    triage_log_path = _layout.triage_log_path(root)
    existing = load_triage_log(triage_log_path)
    recommendations: list[AIRecommendation] = []
    by_id = {record.record.record_id: record for record in pending}
    for triage_record in pending:
        text = f"{triage_record.record.title or ''} {triage_record.record.abstract or ''}"
        ontology_signals = detect_ontology_signals(text)
        deterministic_flags = detect_deterministic_flags(triage_record.record)
        updated = TriageRecord(
            record=triage_record.record,
            deterministic_flags=tuple(deterministic_flags),
            ontology_signals=tuple(ontology_signals),
        )
        priority_score, relevance_score = score_triage(updated)
        updated = TriageRecord(
            record=updated.record,
            deterministic_flags=updated.deterministic_flags,
            ontology_signals=updated.ontology_signals,
            priority_score=priority_score,
            relevance_score=relevance_score,
        )
        recommendation = build_recommendation(
            updated, model=None, provider=None
        )
        recommendations.append(recommendation)
    if recommendations:
        append_recommendations(triage_log_path, recommendations)
    for recommendation in recommendations:
        record = by_id[recommendation.record_id].record
        _print_recommendation(recommendation, record.title or "(untitled)")
    print(f"\n{len(recommendations)} recommendation(s) written to triage log.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="medscale screen triage",
        description="AI-assisted triage prioritization: advisory queue for human reviewers.",
    )
    parser.add_argument(
        "command",
        choices=["status", "recommend"],
        help="status: triage counts; recommend: generate recommendations for pending records",
    )
    parser.add_argument(
        "--root", type=Path, default=_DEFAULT_ROOT, help="workspace root (default: data/litdb)"
    )
    parser.add_argument(
        "--query", default=None, help="only records retrieved by this query id (e.g. Q2)"
    )
    parser.add_argument("--limit", type=int, default=None, help="max records this run")
    args = parser.parse_args(argv)

    guard = _common.require_corpus(args.root)
    if guard is not None:
        return guard

    if args.command == "status":
        return _run_status(args.root)
    return _run_recommend(args.root, args.query, args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
