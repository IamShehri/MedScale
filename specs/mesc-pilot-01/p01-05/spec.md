# MESC Pilot-01 — P01-05 Specification

Status: **baseline runner entry contract**

Authorization: Entry contract defined — real execution not authorized

---

## P01-05 purpose

P01-05 qualifies and completes the deterministic B0/B1 runner contracts before real baseline execution may be authorized.

It does this by:

1. Reconciling the existing B0 implementation truth rather than duplicating it.
2. Defining B1 prospectively and unambiguously.
3. Defining a minimal supplied-evidence object contract suitable for B1.
4. Determining, from existing canonical Pilot-01 contracts, what evidence may legally and scientifically be supplied to B1.
5. Reconciling current model authority so that stale Pilot-01 references are explicitly superseded.
6. Recording the exact implementation delta.

---

## B0 — existing implementation

B0 is the simplest baseline: one approved student model, zero-shot, no retrieved evidence, no fine-tuning, no teacher, no Evidence Judge, no specialist board, no reranker or embedding model, and no model-family combination.

Canonical definition:

**B0 — Llama 3.2 3B without supplied evidence**

Existing B0 implementation truth (read-only reconciliation):

- uses the native PubMedQA question
- uses the native PubMedQA context
- performs zero-shot generation
- uses no retrieval
- uses no teacher
- uses no Evidence Judge
- uses no specialist board
- uses no embedding model
- uses no reranker
- performs no fine-tuning

### B0 "without supplied evidence" interpretation

The controlling interpretation for this phase, unless canonical evidence proves otherwise, is:

Native benchmark context is part of the immutable PubMedQA task input and is NOT the "supplied evidence" differentiator between B0 and B1.

Therefore:

B0 =
primary Llama model
+
native Pilot-01 question/context
+
no additional evidence channel

This interpretation preserves the existing B0 prompt semantics and does not change B0 code.

---

## B1 — prospective definition

Canonical definition:

**B1 — Llama 3.2 3B with supplied evidence**

B1 must use:

- the same primary base-model family as B0
- the same frozen P01-04 split
- the same scientific example identities
- the same gold-decision isolation
- the same deterministic execution discipline
- the same abstention policy

B1 differs from B0 ONLY by an explicit additional evidence input channel.

That evidence channel is NOT retrieval. P01-10 remains the retrieval-assisted experiment phase. B1 must not silently become RAG.

---

## B1 supplied-evidence contract

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

Do NOT persist copyrighted raw scientific content merely to satisfy this schema. The exact contract may use stable references to already-authorized content.

No fabricated evidence. No teacher-generated evidence. No LLM-generated gold. No retrieval-generated evidence in B1.

---

## B1 evidence source

Determine from existing canonical Pilot-01 contracts what evidence may legally and scientifically be supplied to B1 without introducing retrieval or leaking gold labels.

The decision must satisfy:

- no gold `final_decision` enters the prompt
- no test membership information enters the prompt
- no label-derived evidence
- no answer leakage
- no unauthorized full text
- source rights preserved
- evidence identity reproducible
- evidence is available equally under the frozen split

If no currently canonical evidence source satisfies this, the phase records:

B1 EVIDENCE SOURCE: UNRESOLVED

and:

B1 IMPLEMENTATION: BLOCKED PENDING EVIDENCE-SOURCE RATIFICATION

Do NOT fabricate a source merely to unblock B1.

**Current determination for this entry contract:**

Existing canonical Pilot-01 contracts define PubMedQA PQA-L as the primary dataset, with native abstract/context as the task input. The existing B0 loader (`_pilot_loader.py`) accepts question and context only, and the gold decision is structurally separate for scoring only. No separate, rights-cleared, non-gold, non-retrieval evidence channel is currently defined in the canonical Pilot-01 package.

Therefore:

B1 EVIDENCE SOURCE: UNRESOLVED

B1 IMPLEMENTATION: BLOCKED PENDING EVIDENCE-SOURCE RATIFICATION

This does not block B0 documentation entry. It blocks B1 runner wiring until a canonical evidence source is separately ratified.

---

## Model authority reconciliation

Current founder constraint:

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

The current older Pilot-01 authority contains stale references to:

- `Qwen/Qwen3-4B-Instruct-2507`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`
- `BAAI/bge-m3`

Reconcile this canonically. Do NOT erase historical records. Add a controlling current-authority supersession.

Required current execution truth:

- `meta-llama/Llama-3.2-3B-Instruct`: PERMITTED PRIMARY PILOT TARGET — execution still separately gated
- `meta-llama/Llama-3.2-1B-Instruct`: PERMITTED LOW-MEMORY FALLBACK — substitution separately gated
- `google/medgemma-1.5-4b-it`: PERMITTED FUTURE CLINICAL SPECIALIST / COMPARATOR — separate authorization required
- `BioMistral/BioMistral-7B`: PERMITTED FUTURE BIOMEDICAL SPECIALIST — separate authorization required
- `CohereLabs/aya-expanse-8b`: FUTURE COMPARATOR ONLY — license/non-commercial constraints remain — separate authorization required

- Qwen: NOT PERMITTED FOR MESC EXECUTION
- DeepSeek: NOT PERMITTED FOR MESC EXECUTION
- `BAAI/bge-m3`: NOT PERMITTED AS MESC EMBEDDING / RETRIEVAL / RERANKING MODEL

Do NOT select replacements for Qwen/DeepSeek/BGE-M3 in this task. Future comparator/retrieval replacement selection requires a separate evidence-based decision.

---

## Existing B0 implementation truth

Do a bounded read-only inspection of the existing B0 implementation.

At minimum inspect:

- `src/medscale/mesc/_b0.py`
- `src/medscale/mesc/_pilot_loader.py`
- `src/medscale/cli/mesc_eval.py`
- backends / validation surfaces used by B0
- B0-focused tests

Record exact current blob identities.

Canonical truth must recognize:

- MESC B0 implementation: ALREADY ADOPTED
- B0 real execution: NOT AUTHORIZED

B0 implementation must NOT be rebuilt merely because P01-05 documentation did not yet exist.

---

## Implementation delta

See `decision-record.md` for the full reconciliation table.

Expected likely result (not forced):

- B0 core: PRESENT
- B0 real-execution authority: MISSING / NOT AUTHORIZED
- B1: PARTIAL or MISSING
- B1 evidence-source authority: must be explicitly determined
- model-selection authority: CONFLICT requiring this reconciliation

---

## Provenance / vNext compatibility

Without implementing MESC vNext Stage 1, require future B0/B1 outputs to expose or preserve enough stable identity to map to:

- provenance
- encounter/experiment state
- uncertainty
- evidence reference

Do NOT introduce ClinicalObservation runtime types yet. Use an explicit compatibility statement, not speculative code.

---

## Uncertainty / abstention

Preserve explicit states:

- `parsed`
- `unparseable`
- `ambiguous`
- `generation_failed`

Do not silently coerce any of these to a clinical answer. Future B1 must not lower abstention simply because supplied evidence exists. Missing/invalid evidence must fail closed or produce an explicitly defined unavailable state.

---

## Real execution boundary

P01-05 entry adoption does NOT authorize:

- model weight download
- network model access
- real B0 run
- real B1 run
- benchmark-result generation
- publication of results

All real model execution requires a later founder authorization after implementation/qualification acceptance.

---

## Exclusions

- Clinical use is excluded.
- Production use is excluded.
- No experimental result claims are made in this entry contract.
- Do not modify frozen model selections.
- Do not execute inference, retrieval, baselines, or training without separate authorization.
- P01-06 and later phases remain NOT AUTHORIZED.
