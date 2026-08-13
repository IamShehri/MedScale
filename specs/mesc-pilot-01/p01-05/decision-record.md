# MESC Pilot-01 — P01-05 Decision Record

Status: **model authority and evidence-source decisions**

Authorization: Entry *** defined — real execution not authorized

---

## Purpose

Record the exact decisions required by P01-05:

1. B0 "without supplied evidence" interpretation
2. B1 definition and evidence channel boundary
3. B1 supplied-evidence contract
4. B1 evidence source determination
5. Model authority reconciliation
6. Implementation delta classification

---

## Decision: B0 "without supplied evidence" interpretation

**Decision:**

Adopt the controlling interpretation unless canonical evidence proves otherwise:

Native benchmark context is part of the immutable PubMedQA task input and is NOT the "supplied evidence" differentiator between B0 and B1.

**Rationale:**

The existing B0 implementation uses the native PubMedQA question and context and performs zero-shot generation with no additional evidence channel. B0 evidence_condition is `"none"`. The "without supplied evidence" phrase therefore differentiates B0 from B1 by the absence of an additional, externally supplied evidence channel, not by the absence of the native benchmark context that is part of the PubMedQA task input.

**Result:**

B0 =
primary Llama model
+
native Pilot-01 question/context
+
no additional evidence channel

No B0 prompt semantics are changed by this decision.

---

## Decision: B1 definition

**Decision:**

Define B1 prospectively as:

**B1 — Llama 3.2 3B with supplied evidence**

**Constraints:**

- same primary base-model family as B0
- same frozen P01-04 split
- same scientific example identities
- same gold-decision isolation
- same deterministic execution discipline
- same abstention policy

B1 differs from B0 ONLY by an explicit additional evidence input channel.

That evidence channel is NOT retrieval. P01-10 remains the retrieval-assisted experiment phase. B1 must not silently become RAG.

---

## Decision: B1 supplied-evidence contract

**Decision:**

A minimal supplied-evidence object suitable for B1 is a versioned private contract conceptually containing:

- `schema_version`
- `evidence_id`
- `example_id`
- `source_document_id`
- `evidence_type`
- `content_reference`
- `content_sha256`
- `provenance`
- `availability`

**Constraints:**

- Do NOT persist copyrighted raw scientific content merely to satisfy this schema.
- The exact contract may use stable references to already-authorized content.
- No fabricated evidence.
- No teacher-generated evidence.
- No LLM-generated gold.
- No retrieval-generated evidence in B1.

---

## Decision: B1 evidence source

**Decision:**

B1 EVIDENCE SOURCE: RATIFIED — MANUAL LABEL-BLIND NATIVE-CONTEXT EVIDENCE CUES

Ratified by founder decision FD-P01-05-B1-EVIDENCE-1
(`specs/mesc-pilot-01/p01-05-b1-evidence-source-ratification/founder-decision.md`).

**Determination:**

Existing canonical Pilot-01 contracts define PubMedQA PQA-L as the primary dataset, with native abstract/context as the task input. The existing B0 loader accepts question and context only, and the gold decision is structurally separate for scoring only.

The ratified B1 supplied-evidence source is manual, label-blind, deterministic evidence-cue annotations over the native PubMedQA context. Every B1 evidence cue resolves to one or more existing ordered context segments belonging to the SAME scientific example/source document (accepted local PilotPubMedQASourceRecord + native ordered context segments + manual evidence-selection annotation). B1 does NOT use an external evidence corpus, retrieval, RAG, a teacher model, or LLM-generated evidence. Evidence records are identity/hash bound (`source_document_id` + context segment index + SHA-256) under the versioned contract `mesc-pilot-01-b1-evidence-cue/1`; raw scientific text remains outside Git.

**Constraints the evidence source must satisfy:**

- no gold `final_decision` enters the prompt
- no test membership information enters the prompt
- no label-derived evidence
- no answer leakage
- no unauthorized full text
- source rights preserved
- evidence identity reproducible
- evidence is available equally under the frozen split
- `long_answer` is NOT a B1 evidence source and remains outside the B1 input condition
- annotation is strictly label-blind; evidence selection only, no rewriting/summarizing/answering
- B1 evidence-cue ledger is INPUT CONDITION DATA, logically separate from any Layer-2 gold claim-support ledger
- no external document, additional PubMed article, guideline, or retrieved document enters B1

**Result:**

B1 EVIDENCE SOURCE: RATIFIED — MANUAL LABEL-BLIND NATIVE-CONTEXT EVIDENCE CUES

B1 IMPLEMENTATION: NOT AUTHORIZED

B1 DEVELOPMENT EVIDENCE PACK: NOT PRODUCED (100 frozen validation examples, domain-separated SHA-256 selection per annotation protocol)

B1 EXECUTION: NOT AUTHORIZED

This does not block B0 documentation entry. It unblocks the B1 evidence-source blocker for future B1 implementation, which remains separately gated and unauthorized by this decision.

---

## Decision: Model authority reconciliation

**Founder constraint:**

Chinese model families are NOT permitted as MESC:

- base models
- teacher models
- embedding models
- rerankers

This includes, at minimum:

- Qwen
- DeepSeek
- Yi
- GLM
- InternLM

**Current execution truth:**

- `meta-llama/Llama-3.2-3B-Instruct`: PERMITTED PRIMARY PILOT TARGET — execution still separately gated
- `meta-llama/Llama-3.2-1B-Instruct`: PERMITTED LOW-MEMORY FALLBACK — substitution separately gated
- `google/medgemma-1.5-4b-it`: PERMITTED FUTURE CLINICAL SPECIALIST / COMPARATOR — separate authorization required
- `BioMistral/BioMistral-7B`: PERMITTED FUTURE BIOMEDICAL SPECIALIST — separate authorization required
- `CohereLabs/aya-expanse-8b`: FUTURE COMPARATOR ONLY — license/non-commercial constraints remain — separate authorization required
- Qwen: NOT PERMITTED FOR MESC EXECUTION
- DeepSeek: NOT PERMITTED FOR MESC EXECUTION
- `BAAI/bge-m3`: NOT PERMITTED AS MESC EMBEDDING / RETRIEVAL / RERANKING MODEL

**Supersession of stale Pilot-01 references:**

The current older Pilot-01 authority contains stale references to:

- `Qwen/Qwen3-4B-Instruct-2507`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`
- `BAAI/bge-m3`

These are HISTORICAL SELECTIONS — SUPERSEDED FOR EXECUTION under the current founder constraint prohibiting Chinese model families for MESC execution.

Do NOT erase historical records. The repository must remain able to explain the historical decision trail.

**Do NOT select replacements for Qwen/DeepSeek/BGE-M3 in this task.**

Future comparator/retrieval replacement selection requires a separate evidence-based decision.

---

## Implementation delta

| surface | current_state | required_P01-05_state | delta | authority_needed |
|---|---|---|---|---|
| B0 orchestration | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| B0 loader | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| B0 CLI | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| transformers runtime | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| B0 tests | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| B1 orchestration | MISSING | PRESENT | IMPLEMENTATION | FD-P01-05-B1-EVIDENCE-1 implementation task |
| B1 evidence contract | PARTIAL | PRESENT | IMPLEMENTATION | P01-05 entry adoption + B1 evidence-source ratification |
| B1 runner wiring | MISSING | PRESENT | IMPLEMENTATION | FD-P01-05-B1-EVIDENCE-1 implementation task |
| B1 tests | MISSING | PRESENT | IMPLEMENTATION | FD-P01-05-B1-EVIDENCE-1 implementation task |
| run manifest | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| baseline report | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| evaluation mapping | PRESENT | PRESENT | NO_DELTA | NONE — already adopted |
| model authority | CONFLICT | RECONCILED | DOCUMENTATION | P01-05 entry adoption |

**Summary:**

- B0 core: PRESENT
- B0 real-execution authority: MISSING / NOT AUTHORIZED
- B1: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES (implementation task FD-P01-05-B1-EVIDENCE-1)
- model-selection authority: CONFLICT requiring this reconciliation — RECONCILED

---

## Provenance / vNext compatibility decision

**Decision:**

Without implementing MESC vNext Stage 1, require future B0/B1 outputs to expose or preserve enough stable identity to map to:

- provenance
- encounter/experiment state
- uncertainty
- evidence reference

**Constraint:**

Do NOT introduce ClinicalObservation runtime types yet. Use an explicit compatibility statement, not speculative code.

---

## Uncertainty / abstention decision

**Decision:**

Preserve explicit states:

- `parsed`
- `unparseable`
- `ambiguous`
- `generation_failed`

Do not silently coerce any of these to a clinical answer. Future B1 must not lower abstention simply because supplied evidence exists. Missing/invalid evidence must fail closed or produce an explicitly defined unavailable state.

---

## Real execution boundary decision

**Decision:**

P01-05 entry adoption does NOT authorize:

- model weight download
- network model access
- real B0 run
- real B1 run
- benchmark-result generation
- publication of results

All real model execution requires a later founder authorization after implementation/qualification acceptance.

---

## Status summary

- P01-04: COMPLETE / CLOSED
- MESC vNext: CANONICALLY RATIFIED
- P01-05 ENTRY CONTRACT: CANONICALLY DEFINED
- B0 IMPLEMENTATION: EXISTING / RECONCILED
- B0 EXECUTION: NOT AUTHORIZED
- B1 EVIDENCE SOURCE: RATIFIED — MANUAL LABEL-BLIND NATIVE-CONTEXT EVIDENCE CUES (FD-P01-05-B1-EVIDENCE-1)
- B1 DEVELOPMENT EVIDENCE PACK: NOT PRODUCED
- B1 IMPLEMENTATION: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES
- B1 DEVELOPMENT EVIDENCE-PACK TOOLING: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES
- B1 EXECUTION: NOT AUTHORIZED
- TEST EVIDENCE PACK: NOT AUTHORIZED
- P01-06: NOT AUTHORIZED
- vNext Stage 1 implementation: NOT AUTHORIZED
