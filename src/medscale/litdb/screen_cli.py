"""Operator-first screening CLI: `medscale screen {next|status|resume}`.

The scientific decisions are the operator's; this is only the surface that presents a
record and records the choice. All logic that can be tested without a terminal lives in
pure functions here (``format_record``, ``decision_for_key``, ``build_event``); the
interactive loop is a thin wrapper that reads a keypress and appends one event.

Human screening -> evidence corpus -> benchmark -> models. Never the reverse; no model
in this loop.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from medscale import __version__
from medscale.litdb.dedupe import normalize_title
from medscale.litdb.records import LiteratureRecord
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
)
from medscale.litdb.store import load_corpus

_DEFAULT_ROOT: Final = Path("data/litdb")
_REVIEW_LOG: Final = "screening/review_log.jsonl"
_CORPUS: Final = "corpus/records.jsonl"

#: Keypress -> (decision, needs an exclusion reason?)
_KEY_ACTIONS: Final[dict[str, tuple[ReviewDecision, bool]]] = {
    "1": (ReviewDecision.INCLUDE, False),
    "2": (ReviewDecision.EXCLUDE, True),
    "3": (ReviewDecision.UNCERTAIN, False),
    "4": (ReviewDecision.DUPLICATE_CONFIRMED, False),  # reason fixed to DUPLICATE
}
_EXCLUSION_KEYS: Final[tuple[ExclusionReason, ...]] = tuple(ExclusionReason)


def decision_for_key(key: str) -> tuple[ReviewDecision, bool] | None:
    """Map a menu key to a decision. ``5`` (skip) and unknown keys return None."""
    return _KEY_ACTIONS.get(key)


def format_record(record: LiteratureRecord, *, position: int, remaining: int) -> str:
    """Render a record for screening — everything the operator needs, nothing more."""
    ids = record.identifiers
    id_parts = [
        f"{name}={value}"
        for name, value in (
            ("doi", ids.doi),
            ("pmid", ids.pmid),
            ("arxiv", ids.arxiv_id),
            ("s2", ids.s2_corpus_id),
        )
        if value
    ]
    authors = ", ".join(record.authors[:6]) + (" et al." if len(record.authors) > 6 else "")
    abstract = record.abstract or "(no abstract)"
    if len(abstract) > 1500:
        abstract = abstract[:1500] + " ..."
    # Chrome stays ASCII: Windows consoles default to cp1252 and must never crash here.
    lines = [
        f"--- record {position} | {remaining} remaining " + "-" * 40,
        f"title    : {record.title}",
        f"authors  : {authors or '(none listed)'}",
        f"year     : {record.year or '?'}    venue: {record.venue or '(none)'}",
        f"tier     : {record.evidence_tier.value}   source: {record.provenance.source_api.value}",
        f"queries  : {', '.join(record.tags) or '(untagged)'}",
        f"ids      : {'  '.join(id_parts)}",
        f"record_id: {record.record_id}",
        "",
        f"abstract : {abstract}",
        "",
        "[1] Include   [2] Exclude   [3] Maybe   [4] Duplicate   [5] Skip   [q] Quit",
    ]
    return "\n".join(lines)


def _git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "0000000"  # detached/no-git: still a valid 7-hex placeholder


def build_event(
    record_id: str,
    decision: ReviewDecision,
    *,
    reviewer: str,
    current: ReviewDecision,
    exclusion_reason: ExclusionReason | None,
    notes: str,
    now: str | None = None,
    git_sha: str | None = None,
) -> ReviewEvent:
    """Assemble a fully-attributed review event (pure; time/git injectable for tests)."""
    return make_event(
        record_id,
        decision,
        reviewer=reviewer,
        decided_at=now or datetime.now(UTC).isoformat(),
        software_version=__version__,
        git_sha=git_sha or _git_sha(),
        current=current,
        exclusion_reason=exclusion_reason,
        notes=notes,
    )


def _status_text(root: Path) -> str:
    corpus = load_corpus(root / _CORPUS)
    ids = [record.record_id for record in corpus]
    reviews = current_reviews(root / _REVIEW_LOG)
    summary = prisma_summary(ids, reviews)
    pending = len(pending_queue(ids, reviews))
    breakdown = "  ".join(f"{k}={v}" for k, v in summary.exclusion_breakdown.items()) or "(none)"
    return "\n".join(
        [
            "MedScale screening status",
            f"  deduplicated : {summary.deduplicated}",
            f"  screened     : {summary.screened}",
            f"  included     : {summary.included}",
            f"  excluded     : {summary.excluded}",
            f"  uncertain    : {summary.uncertain}",
            f"  pending      : {summary.pending}",
            f"  queue        : {pending} awaiting a decision",
            f"  exclusions   : {breakdown}",
        ]
    )


def _prompt_exclusion_reason() -> ExclusionReason | None:
    print("  exclusion reason:")
    for index, reason in enumerate(_EXCLUSION_KEYS, start=1):
        print(f"    [{index}] {reason.value}")
    raw = input("  reason > ").strip()
    if not raw.isdigit() or not (1 <= int(raw) <= len(_EXCLUSION_KEYS)):
        print("  invalid reason; decision skipped")
        return None
    return _EXCLUSION_KEYS[int(raw) - 1]


def _run_interactive(root: Path, reviewer: str, limit: int | None, query: str | None) -> int:
    corpus = load_corpus(root / _CORPUS)
    if query is not None:
        corpus = tuple(record for record in corpus if query in record.tags)
        if not corpus:
            print(f"no records tagged {query!r} - run scripts/tag_query_lineage.py or check the id")
            return 1
    ids_in_order = [
        record.record_id for record in sorted(corpus, key=lambda r: normalize_title(r.title))
    ]
    by_id = {record.record_id: record for record in corpus}
    reviews = current_reviews(root / _REVIEW_LOG)
    queue = pending_queue(ids_in_order, reviews)
    if not queue:
        print("queue empty - every record has a decision. Nothing to screen.")
        return 0
    done = 0
    for position, record_id in enumerate(queue, start=1):
        if limit is not None and done >= limit:
            print(f"\nreached --limit {limit}; stopping. Resume with `medscale screen next`.")
            break
        record = by_id[record_id]
        print("\n" + format_record(record, position=position, remaining=len(queue) - position + 1))
        choice = input("> ").strip().lower()
        if choice == "q":
            print("quit - progress saved.")
            break
        if choice == "5":
            continue
        action = decision_for_key(choice)
        if action is None:
            print("unrecognized key; skipped.")
            continue
        decision, needs_reason = action
        reason: ExclusionReason | None = None
        if decision is ReviewDecision.DUPLICATE_CONFIRMED:
            reason = ExclusionReason.DUPLICATE
        elif needs_reason:
            reason = _prompt_exclusion_reason()
            if reason is None:
                continue
        notes = input("  notes (optional) > ").strip()
        current = reviews.get(record_id)
        event = build_event(
            record_id,
            decision,
            reviewer=reviewer,
            current=current.decision if current else ReviewDecision.PENDING,
            exclusion_reason=reason,
            notes=notes,
        )
        append_events(root / _REVIEW_LOG, (event,))
        reviews[record_id] = RecordReview(decision, reason)
        done += 1
        print(f"  recorded: {decision.value}")
    print(f"\n{done} decision(s) this session.")
    print(_status_text(root))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale screen", description=__doc__)
    parser.add_argument(
        "command",
        choices=["next", "status", "resume"],
        help="next/resume screen records; status prints counts",
    )
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    parser.add_argument(
        "--reviewer", default="operator", help="reviewer id recorded in the audit trail"
    )
    parser.add_argument("--limit", type=int, default=None, help="max records this session")
    parser.add_argument(
        "--query", default=None, help="only records retrieved by this query id (e.g. Q2)"
    )
    args = parser.parse_args(argv)

    if args.command == "status":
        print(_status_text(args.root))
        return 0
    # 'next' and 'resume' are the same operation: pick up the pending queue.
    return _run_interactive(args.root, args.reviewer, args.limit, args.query)


if __name__ == "__main__":
    raise SystemExit(main())
