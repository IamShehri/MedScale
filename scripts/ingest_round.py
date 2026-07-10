"""Run one ingestion round of the frozen query set (search_strategy, ADR-governed).

Reproducible by construction: the run is parameterized only by (run_id, cap), executes
the frozen QUERY_SET at the current git SHA, archives every raw payload verbatim,
writes the round manifest, parses everything into the deduplicated corpus, and emits a
PRISMA-count report. Politeness: spaced requests; Semantic Scholar aborts for the round
after two consecutive rate-limit failures (recorded, never silent).

Usage:  uv run --with truststore python scripts/ingest_round.py --run-id round1 --cap 50
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from medscale.litdb import (
    QUERY_SET,
    ArxivAdapter,
    LiteratureRecord,
    OpenAlexAdapter,
    PubMedAdapter,
    RetrievalError,
    RunManifest,
    SemanticScholarAdapter,
    archive_retrieval,
    parse_pubmed_esearch_ids,
    parse_records,
    write_manifest,
)
from medscale.litdb.ingest import ArchiveEntry
from medscale.litdb.store import write_corpus
from medscale.reproducibility import canonical_json

_SLEEP_SECONDS = 1.5
_S2_BACKOFF_SECONDS = 30
_S2_MAX_CONSECUTIVE_FAILURES = 2
_S2_REQUEST_LIMIT = 100  # Semantic Scholar per-request maximum


def _git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="round1")
    parser.add_argument("--cap", type=int, default=50, help="results per query per source")
    parser.add_argument("--root", type=Path, default=Path("data/litdb"))
    args = parser.parse_args()

    sha = _git_sha()
    entries: list[ArchiveEntry] = []
    records: list[LiteratureRecord] = []
    skipped_items: list[str] = []
    failures: list[str] = []
    identified = 0

    def archive_and_parse(
        query_id: str, run_id: str, retrieval_query: str, adapter: object
    ) -> None:
        nonlocal identified
        assert isinstance(adapter, OpenAlexAdapter | ArxivAdapter | SemanticScholarAdapter)
        (retrieval,) = adapter.search(retrieval_query, limit=args.cap)
        entries.append(archive_retrieval(args.root, run_id, query_id, retrieval))
        outcome = parse_records(retrieval)
        identified += len(outcome.records) + len(outcome.skipped)
        records.extend(outcome.records)
        skipped_items.extend(outcome.skipped)

    # --- OpenAlex + arXiv: straightforward search-and-archive per query
    for adapter in (OpenAlexAdapter(), ArxivAdapter()):
        name = adapter.api.value
        for spec in QUERY_SET:
            try:
                archive_and_parse(spec.query_id, args.run_id, spec.concept_query, adapter)
                print(f"{name} {spec.query_id}: ok")
            except RetrievalError as exc:
                failures.append(f"{name} {spec.query_id}: {exc}")
                print(f"{name} {spec.query_id}: FAILED ({exc})", file=sys.stderr)
            time.sleep(_SLEEP_SECONDS)

    # --- PubMed: esearch (ids) then one esummary batch per query
    pubmed = PubMedAdapter()
    for spec in QUERY_SET:
        try:
            (esearch,) = pubmed.search(spec.concept_query, limit=args.cap)
            entries.append(archive_retrieval(args.root, args.run_id, spec.query_id, esearch))
            pmids = parse_pubmed_esearch_ids(esearch)
            identified += 0  # ids counted when esummary records parse
            if pmids:
                time.sleep(_SLEEP_SECONDS)
                summary = pubmed.fetch_by_identifier(",".join(pmids))
                entries.append(
                    archive_retrieval(args.root, f"{args.run_id}-esummary", spec.query_id, summary)
                )
                outcome = parse_records(summary)
                identified += len(outcome.records) + len(outcome.skipped)
                records.extend(outcome.records)
                skipped_items.extend(outcome.skipped)
            print(f"pubmed {spec.query_id}: {len(pmids)} ids")
        except RetrievalError as exc:
            failures.append(f"pubmed {spec.query_id}: {exc}")
            print(f"pubmed {spec.query_id}: FAILED ({exc})", file=sys.stderr)
        time.sleep(_SLEEP_SECONDS)

    # --- Semantic Scholar: attempt with backoff; abort round after repeated 429s
    s2 = SemanticScholarAdapter()
    consecutive = 0
    for spec in QUERY_SET:
        if consecutive >= _S2_MAX_CONSECUTIVE_FAILURES:
            failures.append(f"semantic_scholar {spec.query_id}: skipped (rate-limit regime)")
            continue
        try:
            (retrieval,) = s2.search(spec.concept_query, limit=min(args.cap, _S2_REQUEST_LIMIT))
            entries.append(archive_retrieval(args.root, args.run_id, spec.query_id, retrieval))
            outcome = parse_records(retrieval)
            identified += len(outcome.records) + len(outcome.skipped)
            records.extend(outcome.records)
            skipped_items.extend(outcome.skipped)
            consecutive = 0
            print(f"semantic_scholar {spec.query_id}: ok")
        except RetrievalError:
            time.sleep(_S2_BACKOFF_SECONDS)
            try:
                (retrieval,) = s2.search(spec.concept_query, limit=min(args.cap, _S2_REQUEST_LIMIT))
                entries.append(archive_retrieval(args.root, args.run_id, spec.query_id, retrieval))
                outcome = parse_records(retrieval)
                identified += len(outcome.records) + len(outcome.skipped)
                records.extend(outcome.records)
                skipped_items.extend(outcome.skipped)
                consecutive = 0
                print(f"semantic_scholar {spec.query_id}: ok (after backoff)")
            except RetrievalError as exc:
                consecutive += 1
                failures.append(f"semantic_scholar {spec.query_id}: {exc}")
                print(f"semantic_scholar {spec.query_id}: FAILED after backoff", file=sys.stderr)
        time.sleep(_SLEEP_SECONDS)

    # --- Manifest, corpus, report
    manifest = RunManifest(run_id=args.run_id, search_strategy_git_sha=sha, entries=tuple(entries))
    manifest_path = write_manifest(args.root, manifest)
    corpus_path = args.root / "corpus" / "records.jsonl"
    deduped = write_corpus(corpus_path, records)

    report = {
        "run_id": args.run_id,
        "cap": args.cap,
        "git_sha": sha,
        "archived_payloads": len(entries),
        "prisma": {
            "identified_raw_items": identified,
            "parsed_records": len(records),
            "parser_skipped": len(skipped_items),
            "deduped_unique_records": deduped,
        },
        "failures": failures,
        "skipped_item_reasons": skipped_items,
    }
    report_path = args.root / "reports" / f"{args.run_id}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(canonical_json(report) + "\n", encoding="utf-8", newline="\n")

    print(
        f"\nround complete: {len(entries)} payloads archived, {identified} items identified, "
        f"{len(records)} parsed, {deduped} unique records -> {corpus_path}"
    )
    print(f"manifest: {manifest_path}\nreport:   {report_path}")
    print(f"failures: {len(failures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
