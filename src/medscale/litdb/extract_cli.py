"""Evidence extraction CLI: `medscale extract` — INCLUDED records become Evidence Objects.

The pipeline stage after screening: for each record the human reviewer INCLUDED, the
operator extracts one or more atomic claims (with optional PICO/effect structure). Each
object is immediately rule-verified (source reference + provenance anchor) and persisted
content-addressed. No model participates; extraction_method is HUMAN by construction.

Pure helpers (queue computation, object assembly) are testable without a terminal; the
interactive loop is a thin shell, same pattern as `medscale screen`.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from medscale.evidence import EvidenceObject, ExtractionMethod, StudyType
from medscale.evidence_checks import archived_payload_hashes, rule_verify_source
from medscale.evidence_store import load_evidence, write_evidence
from medscale.litdb.records import LiteratureRecord
from medscale.litdb.review import ReviewDecision, current_reviews
from medscale.litdb.store import load_corpus

_DEFAULT_ROOT: Final = Path("data/litdb")
_CORPUS: Final = "corpus/records.jsonl"
_REVIEW_LOG: Final = "screening/review_log.jsonl"
_EVIDENCE: Final = "evidence/objects.jsonl"

_STUDY_TYPES: Final[tuple[StudyType, ...]] = tuple(StudyType)


def extraction_queue(
    corpus: tuple[LiteratureRecord, ...],
    included_ids: frozenset[str],
    extracted_source_ids: frozenset[str],
) -> tuple[LiteratureRecord, ...]:
    """INCLUDED records with no evidence object yet, in stable record_id order."""
    return tuple(
        record
        for record in sorted(corpus, key=lambda r: r.record_id)
        if record.record_id in included_ids and record.record_id not in extracted_source_ids
    )


def assemble_evidence(
    record: LiteratureRecord,
    *,
    claim: str,
    study_type: StudyType,
    created_at: str,
    population: str | None = None,
    intervention: str | None = None,
    comparator: str | None = None,
    outcome: str | None = None,
    effect_measure: str | None = None,
    effect_value: str | None = None,
) -> EvidenceObject:
    """Build a HUMAN-extracted evidence object bound to its source record's provenance."""
    return EvidenceObject(
        claim=claim,
        study_type=study_type,
        provenance=record.provenance,
        created_at=created_at,
        source_record_id=record.record_id,
        population=population,
        intervention=intervention,
        comparator=comparator,
        outcome=outcome,
        effect_measure=effect_measure,
        effect_value=effect_value,
        extraction_method=ExtractionMethod.HUMAN,
    )


def _prompt_study_type() -> StudyType | None:
    print("  study type:")
    for index, study_type in enumerate(_STUDY_TYPES, start=1):
        print(f"    [{index}] {study_type.value}")
    raw = input("  study type > ").strip()
    if not raw.isdigit() or not (1 <= int(raw) <= len(_STUDY_TYPES)):
        print("  invalid; extraction skipped")
        return None
    return _STUDY_TYPES[int(raw) - 1]


def _optional(prompt: str) -> str | None:
    value = input(f"  {prompt} (optional) > ").strip()
    return value or None


def _show_record(record: LiteratureRecord, position: int, total: int) -> None:
    print(f"\n--- extract {position}/{total} " + "-" * 50)
    print(f"title    : {record.title}")
    print(f"year     : {record.year or '?'}    venue: {record.venue or '(none)'}")
    print(f"record_id: {record.record_id}")
    print(f"abstract : {(record.abstract or '(no abstract)')[:1200]}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="medscale extract", description=__doc__)
    parser.add_argument("--root", type=Path, default=_DEFAULT_ROOT)
    parser.add_argument("--limit", type=int, default=None, help="max records this session")
    args = parser.parse_args(argv)

    corpus = load_corpus(args.root / _CORPUS)
    reviews = current_reviews(args.root / _REVIEW_LOG)
    included = frozenset(
        record_id
        for record_id, review in reviews.items()
        if review.decision is ReviewDecision.INCLUDE
    )
    if not included:
        print("no INCLUDED records yet - screening comes first (`medscale screen next`).")
        return 0
    evidence_path = args.root / _EVIDENCE
    existing = load_evidence(evidence_path)
    extracted_sources = frozenset(obj.source_record_id for obj in existing if obj.source_record_id)
    queue = extraction_queue(corpus, included, extracted_sources)
    if not queue:
        print(f"extraction queue empty: all {len(included)} INCLUDED records have evidence.")
        return 0

    corpus_ids = frozenset(record.record_id for record in corpus)
    known_hashes = archived_payload_hashes(args.root)
    collected: list[EvidenceObject] = list(existing)
    done = 0
    for position, record in enumerate(queue, start=1):
        if args.limit is not None and done >= args.limit:
            print(f"\nreached --limit {args.limit}; resume with `medscale extract`.")
            break
        _show_record(record, position, len(queue))
        while True:
            claim = input("  claim ([enter]=next record, q=quit) > ").strip()
            if claim.lower() == "q":
                write_evidence(evidence_path, collected)
                print(f"quit - {done} extraction(s) saved to {evidence_path}")
                return 0
            if not claim:
                break
            study_type = _prompt_study_type()
            if study_type is None:
                continue
            obj = assemble_evidence(
                record,
                claim=claim,
                study_type=study_type,
                created_at=datetime.now(UTC).isoformat(),
                population=_optional("population"),
                intervention=_optional("intervention"),
                comparator=_optional("comparator"),
                outcome=_optional("outcome"),
                effect_measure=_optional("effect measure"),
                effect_value=_optional("effect value"),
            )
            verified, results = rule_verify_source(obj, corpus_ids, known_hashes)
            for result in results:
                marker = "ok" if result.passed else "FAIL"
                print(f"    [{marker}] {result.check}: {result.reason}")
            collected.append(verified)
            done += 1
            print(f"    recorded: {verified.verification.value}  ({verified.evidence_id[:12]}...)")
    count = write_evidence(evidence_path, collected)
    print(f"\n{done} extraction(s) this session; evidence store now {count} objects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
