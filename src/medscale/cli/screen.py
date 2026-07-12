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
from pathlib import Path
from typing import Final

import medscale._layout as _layout
from medscale.__about__ import __version__
from medscale._runtime import git_sha as _runtime_git_sha
from medscale._runtime import utc_now
from medscale.cli import _common
from medscale.cli import ai_triage as ai_triage_cli
from medscale.evidence_store import load_evidence
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
from medscale.litdb.uncertain import (
    GroupResolution,
    append_resolution,
    duplicate_hints,
    load_groups,
    load_resolutions,
    unresolved_groups,
)

_DEFAULT_ROOT: Final = _layout.DEFAULT_ROOT
_REVIEW_LOG: Final = _layout.REVIEW_LOG
_CORPUS: Final = _layout.CORPUS
_UNCERTAIN: Final = _layout.UNCERTAIN_DUPLICATES
_RESOLUTIONS: Final = _layout.UNCERTAIN_RESOLUTIONS

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


def format_record(
    record: LiteratureRecord,
    *,
    position: int,
    remaining: int,
    duplicate_hint: str | None = None,
) -> str:
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
    if duplicate_hint:
        lines.insert(1, f"!! {duplicate_hint}")
    return "\n".join(lines)


def _git_sha() -> str:
    return _runtime_git_sha()


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
        decided_at=now or utc_now(),
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
    unresolved = len(
        unresolved_groups(load_groups(root / _UNCERTAIN), load_resolutions(root / _RESOLUTIONS))
    )
    return "\n".join(
        [
            "MedScale screening status",
            f"  uncertain-duplicate groups unresolved: {unresolved}"
            + ("  <- resolve first: medscale screen duplicates" if unresolved else ""),
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
    hints = duplicate_hints(
        load_groups(root / _UNCERTAIN), load_resolutions(root / _RESOLUTIONS), by_id
    )
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
        print(
            "\n"
            + format_record(
                record,
                position=position,
                remaining=len(queue) - position + 1,
                duplicate_hint=hints.get(record_id),
            )
        )
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


def _format_group_member(index: int, record: LiteratureRecord) -> str:
    ids = record.identifiers
    id_text = "  ".join(
        f"{name}={value}"
        for name, value in (
            ("doi", ids.doi),
            ("pmid", ids.pmid),
            ("arxiv", ids.arxiv_id),
            ("s2", ids.s2_corpus_id),
        )
        if value
    )
    abstract = (record.abstract or "(no abstract)")[:220]
    return "\n".join(
        [
            f"  [{index}] {record.title}",
            f"      year={record.year or '?'}  venue={record.venue or '(none)'}  "
            f"source={record.provenance.source_api.value}  tier={record.evidence_tier.value}",
            f"      {id_text}",
            f"      {abstract}",
        ]
    )


def _run_duplicates(root: Path, reviewer: str) -> int:
    """Resolve uncertain duplicate groups BEFORE screening proceeds blind (ADR-0017-safe:
    extras are excluded via review events; the corpus is never rewritten)."""
    corpus = load_corpus(root / _CORPUS)
    by_id = {record.record_id: record for record in corpus}
    groups = unresolved_groups(
        load_groups(root / _UNCERTAIN), load_resolutions(root / _RESOLUTIONS)
    )
    if not groups:
        print("no unresolved uncertain-duplicate groups. Screening can proceed.")
        return 0
    reviews = current_reviews(root / _REVIEW_LOG)
    for group_number, group in enumerate(groups, start=1):
        members = [by_id[rid] for rid in group.record_ids if rid in by_id]
        print(f"\n=== group {group_number}/{len(groups)}  ({group.reason}) " + "=" * 20)
        for index, member in enumerate(members, start=1):
            print(_format_group_member(index, member))
        print(
            f"\n[1..{len(members)}] keep that member, mark the others duplicates"
            "   [d] all distinct   [s] skip   [q] quit"
        )
        choice = input("> ").strip().lower()
        if choice == "q":
            print("quit - progress saved.")
            break
        if choice == "s":
            continue
        now = utc_now()
        if choice == "d":
            append_resolution(
                root / _RESOLUTIONS,
                GroupResolution(
                    key=group.key, resolution="distinct", reviewer=reviewer, decided_at=now
                ),
            )
            print("  recorded: all distinct")
            continue
        if not choice.isdigit() or not (1 <= int(choice) <= len(members)):
            print("  unrecognized; skipped.")
            continue
        kept = members[int(choice) - 1]
        events = [
            build_event(
                member.record_id,
                ReviewDecision.DUPLICATE_CONFIRMED,
                reviewer=reviewer,
                current=(
                    reviews[member.record_id].decision
                    if member.record_id in reviews
                    else ReviewDecision.PENDING
                ),
                exclusion_reason=ExclusionReason.DUPLICATE,
                notes=f"duplicate of {kept.record_id} (uncertain group {group.key[:12]})",
                now=now,
            )
            for member in members
            if member.record_id != kept.record_id
        ]
        append_events(root / _REVIEW_LOG, events)
        for event in events:
            reviews[event.record_id] = RecordReview(
                ReviewDecision.DUPLICATE_CONFIRMED, ExclusionReason.DUPLICATE
            )
        append_resolution(
            root / _RESOLUTIONS,
            GroupResolution(
                key=group.key,
                resolution="duplicates",
                reviewer=reviewer,
                decided_at=now,
                kept_record_id=kept.record_id,
            ),
        )
        print(f"  recorded: kept {kept.record_id[:12]}, {len(events)} marked duplicate")
    remaining = len(
        unresolved_groups(load_groups(root / _UNCERTAIN), load_resolutions(root / _RESOLUTIONS))
    )
    print(f"\nunresolved groups remaining: {remaining}")
    return 0


def _run_amend(root: Path, reviewer: str, record_prefix: str) -> int:
    """Correct one earlier decision: append a new event, never rewrite history."""
    corpus = load_corpus(root / _CORPUS)
    matches = [r for r in corpus if r.record_id.startswith(record_prefix)]
    if not matches:
        return _common.fail(
            f"no record starts with {record_prefix!r}",
            hint="record ids are shown during screening and in the review log",
        )
    if len(matches) > 1:
        return _common.fail(
            f"{record_prefix!r} is ambiguous ({len(matches)} records match)",
            hint="give more characters of the record id",
        )
    record = matches[0]
    reviews = current_reviews(root / _REVIEW_LOG)
    current = reviews.get(record.record_id)
    current_decision = current.decision if current else ReviewDecision.PENDING
    print(format_record(record, position=1, remaining=1))
    print(f"\ncurrent decision: {current_decision.value}")
    evidence_count = sum(
        1
        for obj in load_evidence(_layout.evidence_path(root))
        if obj.source_record_id == record.record_id
    )
    if evidence_count:
        print(
            f"!! {evidence_count} Evidence Object(s) already cite this record - "
            "moving it away from INCLUDE leaves them citing a non-included source. "
            "Review the evidence store after amending."
        )
    choice = input("new decision > ").strip().lower()
    action = decision_for_key(choice)
    if action is None:
        print("unrecognized key; nothing changed.")
        return 0
    decision, needs_reason = action
    reason: ExclusionReason | None = None
    if decision is ReviewDecision.DUPLICATE_CONFIRMED:
        reason = ExclusionReason.DUPLICATE
    elif needs_reason:
        reason = _prompt_exclusion_reason()
        if reason is None:
            return 0
    notes = input("  why the correction? (recorded in the audit trail) > ").strip()
    event = build_event(
        record.record_id,
        decision,
        reviewer=reviewer,
        current=current_decision,
        exclusion_reason=reason,
        notes=notes,
    )
    append_events(root / _REVIEW_LOG, (event,))
    print(f"  recorded: {current_decision.value} -> {decision.value}")
    return 0


_EXAMPLES: Final = """\
examples:
  medscale screen status                         where the review stands
  medscale screen duplicates --reviewer alice    resolve uncertain duplicates (do this first)
  medscale screen next --reviewer alice --query Q2 --limit 25
  medscale screen amend --record 3e7155a2 --reviewer alice   correct an earlier decision
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="medscale screen",
        description="Screen literature records and keep a complete, append-only audit "
        "trail. Every decision is attributed to a reviewer and can be corrected later "
        "with `amend` - history is never rewritten.",
        epilog=_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=["next", "status", "resume", "duplicates", "amend", "triage"],
        help="next/resume: screen pending records; status: counts; "
        "duplicates: resolve uncertain groups; amend: correct one earlier decision; "
        "triage: AI-assisted prioritization (advisory only)",
    )
    parser.add_argument(
        "--root", type=Path, default=_DEFAULT_ROOT, help="workspace root (default: data/litdb)"
    )
    parser.add_argument(
        "--reviewer", default="operator", help="reviewer id recorded in the audit trail"
    )
    parser.add_argument("--limit", type=int, default=None, help="max records this session")
    parser.add_argument(
        "--query", default=None, help="only records retrieved by this query id (e.g. Q2)"
    )
    parser.add_argument("--record", default=None, help="record id (or unique prefix) for `amend`")
    args = parser.parse_args(argv)

    guard = _common.require_corpus(args.root)
    if guard is not None:
        return guard

    try:
        if args.command == "status":
            print(_status_text(args.root))
            return 0
        if args.command == "duplicates":
            return _run_duplicates(args.root, args.reviewer)
        if args.command == "amend":
            if not args.record:
                return _common.fail(
                    "amend needs --record <record id or prefix>",
                    hint="example: medscale screen amend --record 3e7155a2",
                )
            return _run_amend(args.root, args.reviewer, args.record)
        if args.command == "triage":
            return ai_triage_cli.main(argv[1:] if argv else None)
        # 'next' and 'resume' are the same operation: pick up the pending queue.
        return _run_interactive(args.root, args.reviewer, args.limit, args.query)
    except (KeyboardInterrupt, EOFError):
        # Decisions are appended one-by-one, so an interrupt loses nothing.
        print("\nsession interrupted - every recorded decision is already saved.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
