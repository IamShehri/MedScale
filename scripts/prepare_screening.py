"""Make the corpus screening-ready (scientific-review items S1 + S2).

One idempotent-by-inspection pass over the committed corpus:

1. fuzzy dedupe (pass 2): auto-merge conflict-free title/year twins; write the merge
   log and the uncertain list; rewrite the corpus;
2. bulk-advance every surviving record IDENTIFIED -> DEDUPED in the screening log
   (single batched, all-or-nothing append);
3. compute per-query/source coverage ratios from the round manifest and write the
   coverage report.

Usage: uv run python scripts/prepare_screening.py --run-id round1
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import medscale._layout as _layout
from medscale.litdb import ScreeningDecision, ScreeningStage, append_decisions
from medscale.litdb.coverage import coverage_for_manifest
from medscale.litdb.dedupe import dedupe_records
from medscale.litdb.store import load_corpus, write_corpus
from medscale.reproducibility import canonical_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="round1")
    parser.add_argument("--root", type=Path, default=Path("data/litdb"))
    args = parser.parse_args()

    corpus_path = _layout.corpus_path(args.root)
    records = load_corpus(corpus_path)
    print(f"loaded corpus: {len(records)} records")

    # 1 — fuzzy dedupe
    result = dedupe_records(records)
    write_corpus(corpus_path, result.records)
    screening_dir = args.root / "screening"
    screening_dir.mkdir(parents=True, exist_ok=True)
    merge_log = screening_dir / "merge_log.jsonl"
    merge_log.write_text(
        "".join(canonical_json(m.to_dict()) + "\n" for m in result.merges),
        encoding="utf-8",
        newline="\n",
    )
    uncertain_path = screening_dir / "uncertain_duplicates.jsonl"
    uncertain_path.write_text(
        "".join(canonical_json(u.to_dict()) + "\n" for u in result.uncertain),
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"dedupe: {len(records)} -> {len(result.records)} records "
        f"({len(result.merges)} merges, {len(result.uncertain)} uncertain groups)"
    )

    # 2 — bulk PRISMA advancement to DEDUPED
    decided_at = datetime.now(UTC).isoformat()
    log_path = screening_dir / "screening_log.jsonl"
    if log_path.exists():
        print("screening log already exists; skipping bulk advancement")
    else:
        append_decisions(
            log_path,
            [
                ScreeningDecision(
                    record_id=record.record_id,
                    to_stage=ScreeningStage.DEDUPED,
                    decided_at=decided_at,
                )
                for record in result.records
            ],
        )
        print(f"screening log: {len(result.records)} records advanced to DEDUPED")

    # 3 — coverage report
    manifest_path = _layout.manifests_dir(args.root) / f"{args.run_id}.json"
    coverage = coverage_for_manifest(args.root, manifest_path)
    report_path = args.root / _layout.REPORTS_DIR / f"{args.run_id}-coverage.json"
    report_path.write_text(
        canonical_json(
            {
                "run_id": args.run_id,
                "note": (
                    "Relevance-ranked sources + result caps make this round a SCOPING "
                    "search; ratios below quantify coverage of each query's matching "
                    "population (scientific review S1)."
                ),
                "coverage": [entry.to_dict() for entry in coverage],
            }
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    worst = min(coverage, key=lambda e: e.coverage_ratio, default=None)
    if worst is not None:
        print(
            f"coverage report: {len(coverage)} entries -> {report_path} "
            f"(lowest: {worst.query_id}/{worst.source_api.value} "
            f"= {worst.coverage_ratio:.4f})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
