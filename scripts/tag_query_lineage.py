"""Attach query-lineage tags to every corpus record (one-off, idempotent, verifiable).

Rebuilds record -> query mapping from committed manifests + merge lineage, rewrites the
corpus with ``tags`` populated (record_id is unchanged — tags are not part of identity),
and runs the integrity check afterward. Enables `medscale screen next --query Q2`.

Usage: uv run python scripts/tag_query_lineage.py
"""

from __future__ import annotations

import argparse
import dataclasses
from collections import Counter
from pathlib import Path

from medscale.litdb.integrity import check_litdb, format_report
from medscale.litdb.lineage import build_query_tags
from medscale.litdb.store import load_corpus, write_corpus


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/litdb"))
    args = parser.parse_args()

    corpus_path = args.root / "corpus" / "records.jsonl"
    records = load_corpus(corpus_path)
    tags = build_query_tags(args.root)

    tagged = tuple(
        dataclasses.replace(
            record, tags=tuple(sorted(set(record.tags) | tags.get(record.record_id, set())))
        )
        for record in records
    )
    untagged = [record.record_id for record in tagged if not record.tags]
    per_query = Counter(tag for record in tagged for tag in record.tags)

    write_corpus(corpus_path, tagged)
    tagged_count = len(tagged) - len(untagged)
    print(f"corpus: {len(tagged)} records; tagged: {tagged_count}; untagged: {len(untagged)}")
    print("per-query record counts:", dict(sorted(per_query.items())))
    if untagged:
        print("WARNING untagged record_ids (no archive parse reproduced them):")
        for record_id in untagged[:10]:
            print("  ", record_id)

    report = check_litdb(args.root)
    print(format_report(report))
    return 0 if report.is_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
