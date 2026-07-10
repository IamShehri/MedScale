# Paper Taxonomy

- **Status:** Foundational (governs how the literature database is organized)
- **Date:** 2026-07-09
- **Related:** T1 (literature database), `docs/research/search_strategy.md` (T1),
  `docs/research/research_questions.md`

This document defines the **classification scheme** for the MedScale literature database
(litdb, T1). It is the schema by which papers are screened, tagged, and extracted — not a
list of papers. It maps directly onto the litdb tables so that every included paper is
placed on the same set of axes.

> **Rule R1 (no fabricated citations).** This file contains **no** concrete paper titles,
> authors, years, or identifiers. Every actual paper enters via a live API response
> (Semantic Scholar / OpenAlex / PubMed / arXiv) with a resolvable DOI, arXiv id, PMID,
> or S2 corpusId, plus `verified_at` and `source_api`. An API returning nothing is
> recorded as `NOT_FOUND`, never backfilled from memory.

---

## 1. How the taxonomy binds to litdb

The litdb `extraction` table records, per included paper: `task`, `datasets_used`,
`method_family`, `base_model`, `key_metric`, `metric_value`, `code_available`, `license`.
The facets below are the controlled vocabularies those free-ish fields draw from, plus
`tags` for topic domains and `screening(stage, reason)` for PRISMA state. Keeping the
vocabulary fixed here is what makes the corpus queryable and reproducible.

## 2. Facet A — Topic domain (`tags`)

A paper may carry more than one domain tag.

- `fhir-clinical-modeling` — FHIR, HL7, clinical data standards, interoperability.
- `constrained-decoding` — grammar/JSON-schema/regex-constrained generation, structured
  output, GBNF, finite-state / CFG decoding.
- `clinical-llm` — medical/clinical language models (open or closed).
- `clinical-ie` — information extraction from clinical text to structured schemas.
- `medical-benchmark` — evaluation suites and leaderboards for medical/clinical AI.
- `eval-methodology` — metric design, LLM-as-judge critiques, contamination, reporting.
- `peft-efficiency` — QLoRA/LoRA/PEFT, quantization, low-resource fine-tuning.
- `terminology-ontology` — LOINC, RxNorm, SNOMED CT, UMLS, value-set grounding.
- `synthetic-clinical-data` — Synthea and other synthetic EHR/clinical data generation.
- `faithfulness-hallucination` — grounding, attribution, hallucination measurement.
- `safety-governance` — clinical AI safety, regulation, model/dataset documentation.

## 3. Facet B — Contribution type (single value)

- `method` — a new technique or model.
- `benchmark` — a dataset+metric evaluation artifact.
- `dataset` — a data resource.
- `system` — an applied/engineering system.
- `survey` — a review or survey.
- `negative-result` — a paper whose primary contribution is a null/refutation.
- `position` — argument/opinion/framework without primary empirical results.

## 4. Facet C — Method family (`extraction.method_family`)

Controlled vocabulary; extend only by appending (never renaming).

- `constrained-decoding`
- `sft-instruction-tuning`
- `peft-qlora`
- `rag-retrieval`
- `prompting-fewshot`
- `pretraining-continued`
- `rule-symbolic` (validators, grammars, ontology reasoning)
- `alignment-rlhf-dpo` (tracked for completeness; out of scope for MESC v0)
- `other` (must be accompanied by a `screening.reason` note explaining why nothing fits)

## 5. Facet D — Evidence tier

Records how much weight a finding can bear; independent of relevance.

- `peer-reviewed` — venue-reviewed publication.
- `preprint` — arXiv/medRxiv/bioRxiv, not yet peer-reviewed.
- `benchmark-report` — technical report / model card with reproducible numbers.
- `grey` — blog, docs, standard text (e.g. an HL7 spec page); citable for facts, not for
  performance claims.

## 6. Facet E — Reproducibility signals (from `extraction`)

- `code_available` — yes/no + URL.
- `data_available` — yes/no + licence (ties to Rule R3 thinking for third-party data).
- `license` — SPDX id where determinable; blocks derivative/commercial use assessment.
- `weights_available` — for models: open weights? derivative + commercial use permitted?

## 7. Facet F — Relevance to research questions

Each included paper is tagged with the RQ(s) it bears on (`RQ1`–`RQ7`), so the corpus can
be sliced by open question. A paper relevant to no RQ is a candidate for exclusion at the
eligibility stage unless it establishes essential background.

## 8. PRISMA screening state (`screening.stage`, `screening.reason`)

Every record moves through explicit stages; every exclusion records a reason.

1. `identified` — returned by a source query (raw).
2. `deduped` — survived dedupe (DOI first, then fuzzy title+year).
3. `screened` — title/abstract screened.
4. `eligibility` — full-text eligibility assessed.
5. `included` — in the working corpus.
6. `excluded` — with a mandatory `reason`.

### Inclusion criteria (working; finalized in `search_strategy.md`, T1)
- Bears on at least one RQ (Facet F), **and**
- Provides either a reproducible method/benchmark/dataset or essential standards
  background, **and**
- Is retrievable with a resolvable identifier (Rule R1).

### Exclusion criteria
- No resolvable identifier → cannot be verified → excluded (recorded `NOT_FOUND`).
- Off-topic to every RQ and not required as background.
- Performance claim with no reproducible artifact when the row is being used to support
  a MedScale design decision (grey-tier facts are still citable for non-performance
  statements).
- Restricted data/model that cannot inform a permissive, commercial-use platform (may
  still be recorded for landscape awareness, tagged accordingly, but not used as a
  design dependency).

## 9. Target corpus

100–150 included papers across the domains in Facet A, weighted toward `constrained-decoding`,
`fhir-clinical-modeling`, `clinical-ie`, `eval-methodology`, and `peft-efficiency` — the
domains closest to RQ1–RQ5. Exact per-source query strings and the final PRISMA thresholds
live in `docs/research/search_strategy.md` (T1).

## 10. Change control

Vocabularies are **append-only**: add new tags/families/tiers, never rename or delete
existing ones (renames break the audit trail and past extractions). Structural changes to
the taxonomy itself require an ADR.
