# Search Strategy & Reproducible Ingestion Design (T1)

- **Status:** v1 design — query set is **frozen by commit** before the first ingestion
  run; any later change is a new, versioned search round
- **Date:** 2026-07-10
- **Related:** [paper taxonomy](../research/paper_taxonomy.md) (facets, PRISMA states),
  [research questions](../research/research_questions.md), Rules R1/R5/R7,
  [ADR-0009](../adr/0009-evidence-model.md), `medscale.litdb`

This document is the executable *plan* for populating litdb. It exists so that the
corpus is reproducible: given this file at a given commit plus the archived raw
responses, a third party can reconstruct every screening decision.

## 1. Sources

| Source | Access | Role | Terms note |
|---|---|---|---|
| Semantic Scholar | Graph API (`/graph/v1/paper/search`, `/paper/{id}`) | Primary discovery + citation graph | Public API; polite rate limits |
| OpenAlex | REST (`/works`) | Cross-check + OA metadata + dedupe aid | CC0 metadata |
| PubMed | NCBI E-utilities (`esearch` + `efetch`) | Biomedical authority; PMIDs | NCBI usage policies; metadata field constraints recorded at ingest |
| arXiv | Export API (`/api/query`) | Preprints (constrained decoding, PEFT, eval) | Open |

All four map to `medscale.provenance.SourceAPI`. Adapters implement the
`medscale.litdb.SourceAdapter` protocol and must return `RawRetrieval` envelopes —
**the raw payload is archived and hashed before any parsing.**

## 2. Query set v1 (templates per taxonomy Facet-A domain)

Weighted toward the domains closest to RQ1–RQ5 (taxonomy §9). `<S>` = source-specific
syntax adaptation; queries run per-source with the same concept terms.

| # | Domain (tag) | Concept query (v1) | Bears on |
|---|---|---|---|
| Q1 | `constrained-decoding` | ("constrained decoding" OR "grammar-constrained" OR "structured output" OR GBNF OR "JSON schema" generation) AND (LLM OR "language model") | RQ1 |
| Q2 | `fhir-clinical-modeling` | (FHIR OR "HL7 FHIR") AND ("language model" OR LLM OR generation OR validation) | RQ1, RQ3 |
| Q3 | `clinical-ie` | ("clinical information extraction" OR "note to structured" OR "clinical NER") AND ("language model" OR transformer) | RQ5 |
| Q4 | `eval-methodology` | ("LLM-as-judge" OR "evaluation methodology" OR "benchmark contamination") AND (medical OR clinical) | RQ2, RQ5 |
| Q5 | `peft-efficiency` | (QLoRA OR LoRA OR "parameter-efficient fine-tuning") AND (clinical OR biomedical OR medical) | RQ2 |
| Q6 | `medical-benchmark` | ("medical benchmark" OR "clinical benchmark" OR MedQA OR "clinical evaluation suite") | RQ2 |
| Q7 | `synthetic-clinical-data` | (Synthea OR "synthetic patient" OR "synthetic EHR" OR "synthetic clinical data") | RQ3, RQ6 |
| Q8 | `faithfulness-hallucination` | (hallucination OR faithfulness OR attribution) AND (clinical OR medical) AND ("language model" OR LLM) | RQ5 |
| Q9 | `terminology-ontology` | (SNOMED OR LOINC OR RxNorm OR UMLS) AND ("language model" OR "value set" OR grounding) | RQ7 |
| Q10 | `clinical-llm` | ("clinical language model" OR "medical LLM" OR "biomedical language model") — survey slice | background |

Execution parameters (recorded in every run log): result cap per query per source
(v1: 200), year window (v1: 2019→run date; standards background exempt), language
(English; limitation recorded per reproducibility policy).

## 3. PRISMA workflow (mechanized by `medscale.litdb.screening`)

```
identified ──► deduped ──► screened ──► eligibility ──► included
     │            │            │             │              │ (retraction etc.)
     └────────────┴────────────┴─────────────┴──────────────┴──► excluded (+ mandatory reason)
```

1. **identified** — every raw hit; `RawRetrieval` archived; `LiteratureRecord` created
   with R1 provenance. A lookup that returns nothing is recorded `NOT_FOUND`.
2. **deduped** — pass 1 by construction: identical resolvable identifiers ⇒ identical
   `record_id`. Pass 2 (documented, human-confirmed): fuzzy title+year for cross-id
   duplicates; the merge decision is logged with both provenances retained.
3. **screened** — title/abstract vs inclusion criteria (below).
4. **eligibility** — full-text check; licence and reproducibility signals extracted.
5. **included / excluded** — exclusion always carries a reason (enforced in code).

**Inclusion criteria (from taxonomy §8, operationalized):** bears on ≥1 RQ; provides a
reproducible method/benchmark/dataset **or** essential standards background; retrievable
via resolvable identifier.
**Exclusion reasons (controlled, append-only):** `no-resolvable-identifier`,
`off-topic-all-rqs`, `no-reproducible-artifact-for-design-claim`,
`restricted-license-design-dependency`, `duplicate`, `superseded-version`, `other`
(with note).

## 4. Reproducibility requirements (per run)

- **Frozen inputs:** this file's commit SHA is the query-set version; run logs cite it.
- **Archived outputs:** every raw API response stored verbatim
  (`data/litdb/raw/<source>/<query-id>/<timestamp>.json`) with SHA-256 recorded — the
  hash that `Provenance.raw_response_sha256` carries. A `LICENSE.md` accompanies the
  data directory (R3) before the first byte is committed.
- **Run manifest:** query id, source, timestamp (UTC, tz-aware), result count, cap
  hit (y/n), git SHA — committed with the run.
- **Determinism boundary:** live APIs are inherently non-stationary; reproducibility is
  therefore **replay-exact** (from archives) and **procedure-exact** (from this doc),
  per the reproducibility policy's handling of unavoidable nondeterminism.
- **Targets:** 100–150 included papers (taxonomy §9); PRISMA counts reported at each
  stage in the T1 result artifact.

## 5. Not in this phase

No network adapters are implemented until this document is frozen and the `data/litdb/`
licence scaffolding exists. No LLM screening: title/abstract screening is human
(solo-operator) with logged decisions; any future ML-assisted triage would be a
secondary, labeled aid — never the decision-maker of record (no model-as-judge).
