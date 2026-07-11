"""Evidence extraction library: INCLUDED records become Evidence Objects.

Stability: **internal** (consumed by the extract CLI and tests; candidates for the
public contract once the extraction workflow stabilizes under real use).

This is the Evidence-layer library half of the extraction workflow — pure functions
only. The interactive transport lives in :mod:`medscale.cli.extract`. Previously these
helpers lived inside ``litdb``, inverting the Knowledge -> Evidence layer direction;
the architecture tests now forbid that.
"""

from __future__ import annotations

from medscale.evidence import EvidenceObject, ExtractionMethod, StudyType
from medscale.litdb.records import LiteratureRecord

__all__ = ["assemble_evidence", "extraction_queue"]


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
