# ADR-0009 — The MedScale Evidence Model

- **Status:** Accepted (2026-07-10; created and approved by operator directive as the
  precondition for T1)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [ADR-0005](0005-research-intelligence-scope.md) (pillar 2),
  [paper taxonomy](../research/paper_taxonomy.md), Rules R1/R5/R7,
  [reproducibility policy](../research/reproducibility_policy.md)

## Context

MedScale's second pillar is *verified evidence infrastructure*. Retrieving documents is
not enough: the platform must represent **validated evidence objects** — claims bound to
sources, with machine-checkable provenance and an explicit verification state. This
abstraction must serve litdb today and, later, the knowledge graph (an edge is a claim),
benchmarks, AI reasoning, and research agents — so it must be defined once, before T1
builds on it.

Design forces, inherited from the program's identity:

1. **A claim is not evidence.** Evidence = claim + source + provenance + verification
   state. An unverified claim is representable but visibly unverified.
2. **Determinism (R5/R7).** Evidence objects must be content-addressable: equal content
   ⇒ identical id, computed with the T0 primitives (`canonical_json`/`content_hash`).
3. **Citation integrity (R1).** Provenance records a resolvable identifier,
   `verified_at`, `source_api`, and the SHA-256 of the raw API response. `NOT_FOUND`
   is recordable, never backfilled.
4. **No model self-verification.** Model-extracted claims can never reach a verified
   state without a human or deterministic-rule check. (The no-LLM-as-judge invariant,
   applied to evidence.)
5. **No invented authority.** Evidence *grading* is either mechanically derived from
   study design by a declared, versioned rubric — or explicitly human, labeled as such.
   MedScale never emits an opaque "confidence score."

## Decision

### 1. Evidence Object schema (v1 — `schema_version = "1"`)

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | derived | `content_hash` over the identity fields (below) — never stored, always recomputable |
| `claim` | str, required | One atomic, natural-language assertion |
| `study_type` | enum | systematic_review · meta_analysis · randomized_controlled_trial · cohort · case_control · cross_sectional · case_report · preclinical · in_silico · other |
| `population` / `intervention` / `comparator` / `outcome` | str? | PICO slots; optional per-slot |
| `effect_measure` / `effect_value` | str? | e.g. "relative risk" / "0.82 (95% CI 0.71–0.95)" — strings in v1, structured later by evidence |
| `provenance` | Provenance, required | see §3 |
| `source_record_id` | str? | FK to the litdb `LiteratureRecord.record_id` |
| `grading_scheme` / `evidence_level` | str / str | see §4 |
| `extraction_method` | enum | human · rule · model |
| `verification` | enum | see §2 |
| `created_at` | str, required | explicit timezone-aware ISO-8601 (never implicit `now()` — determinism) |
| `schema_version` | str | `"1"`; schema evolution is append-only |

**Identity fields** (what `evidence_id` hashes): claim, study_type, the four PICO slots,
effect fields, `provenance.source_api`, `provenance.identifier`, `schema_version`.
Verification state and timestamps are *excluded* — an evidence object keeps its identity
as it moves through verification.

### 2. Verification state machine

```
UNVERIFIED ──► SOURCE_VERIFIED ──► EXTRACTION_VERIFIED
                    │    ▲               │
                    ▼    │               ▼
                 DISPUTED ◄──────────────┘
                    │
                    ▼
                RETRACTED        (RETRACTED is terminal; also reachable
                                  from SOURCE_VERIFIED / EXTRACTION_VERIFIED)
```

- **UNVERIFIED** — drafted; provenance not yet R1-complete.
- **SOURCE_VERIFIED** — the source exists and resolves: R1-complete provenance attached.
- **EXTRACTION_VERIFIED** — the structured fields were checked against the source by a
  **human or deterministic rule**. Guard: an object with `extraction_method = model`
  cannot enter this state without that independent check (force 4).
- **DISPUTED** — contradicted or under challenge; may return to EXTRACTION_VERIFIED
  through re-verification.
- **RETRACTED** — source retracted; terminal.

Illegal transitions raise; state changes produce new immutable objects.

### 3. Provenance model (shared with litdb)

`Provenance` = (`source_api` ∈ {semantic_scholar, openalex, pubmed, arxiv},
`identifier`, `verified_at` tz-aware ISO-8601, `raw_response_sha256`,
`status` ∈ {found, not_found}). This is Rule R1 as a datatype: every claim's source
chain is auditable down to the hash of the raw API response, and a failed lookup is a
recorded fact.

### 4. Evidence grading

v1 ships exactly one scheme: **`medscale-study-design-v1`** — a deterministic, versioned
mapping from study design to level (1 = systematic review/meta-analysis, 2 = RCT,
3 = cohort/case-control, 4 = cross-sectional/case report, 5 = preclinical/in-silico/other).
It grades *design*, not quality of execution — a deliberately mechanical floor.
Established frameworks (GRADE, Oxford CEBM) can be added later as additional declared
schemes with `derived_by = human`; MedScale never averages or blends schemes into a
single opaque score.

### 5. Relationship to litdb and beyond

- **litdb (T1):** `LiteratureRecord` = the bibliographic *source* (identifiers, tier,
  screening state). `EvidenceObject` = a *claim extracted from* a source
  (`source_record_id` FK). Records answer "what did we screen?"; evidence objects answer
  "what does it assert, and how checked is it?"
- **Knowledge graph (H2, gated):** a KG edge is an evidence object wearing graph
  clothes — no edge without an evidence object behind it.
- **Benchmarks / reasoning / agents:** any system claim ("supported by [source]") must
  cite an evidence object whose verification state backs the strength of the assertion.

## Consequences

**Positive:** one abstraction serves five future consumers; verification is visible and
enforceable; ids are reproducible; R1 becomes a datatype instead of a policy paragraph.

**Negative / costs:** v1's string-typed effect fields defer structured effect-size
modeling; single-source evidence objects defer multi-source synthesis (a future
`EvidenceSynthesis` composite, H2) — both deliberate simplifications, extendable
append-only via `schema_version`.

## Alternatives considered

- **Documents-only litdb (no evidence layer).** Rejected: repeats the retrieval-not-
  verification pattern of the closed products MedScale differentiates against.
- **Full EBM ontology now (GRADE profiles, structured effect sizes, synthesis).**
  Rejected: premature; no corpus exists yet to justify the complexity.
- **Numeric confidence scores.** Rejected: opaque authority; violates the
  no-invented-judgment principle.

## Compliance

Implemented in T1 as `medscale/evidence.py` + `medscale/provenance.py` with
deterministic tests (id stability, transition legality, the model-cannot-self-verify
guard). Schema changes are append-only and require an ADR referencing this one.
