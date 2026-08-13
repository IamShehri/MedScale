# MESC Pilot-01 — P01-05 Execution Protocol

Status: **prospective execution boundary**

Authorization: Entry *** defined — real execution not authorized

---

## Purpose

Record the execution boundary and protocol for B0/B1 runner phases.

This document defines what P01-05 entry adoption does and does not authorize. It does not authorize real execution. It records the deterministic discipline that any later authorized execution must follow.

---

## What P01-05 entry adoption authorizes

- Definition of the B0/B1 baseline runner entry contract
- Reconciliation of existing B0 implementation truth
- Prospective definition of B1
- Definition of the B1 supplied-evidence contract
- Determination of B1 evidence source status
- Model authority reconciliation
- Implementation delta classification
- Provenance / vNext compatibility statement
- Documentation of uncertainty / abstention preservation

---

## What P01-05 entry adoption does NOT authorize

- model weight download
- network model access
- real B0 run
- real B1 run
- benchmark-result generation
- publication of results
- P01-06
- P01-07
- vNext Stage 1 implementation

---

## Deterministic execution discipline

Any later authorized B0/B1 execution must follow the same deterministic discipline already adopted for B0:

- greedy, deterministic generation
- immutable model and tokenizer revisions
- local-files-only execution
- no network or model download in the default runner path
- explicit runtime manifest capture
- deterministic run digest
- gold-decision isolation for scoring only
- explicit abstention states

---

## B0 execution path

The existing B0 execution path is already adopted in `src/medscale/mesc/_b0.py` and `src/medscale/cli/mesc_eval.py`.

The runner is dependency-injected with a generator, so the full pipeline is exercised with a deterministic fake and never touches a real model, the network, or training.

Real B0 execution still requires a separately gated authorization.

---

## B1 execution path

The B1 evidence source is canonically ratified and the B1 runner wiring is implemented and qualified with synthetic fixtures. Real B1 execution remains NOT AUTHORIZED.

B1 must use:

- the same primary base-model family as B0
- the same frozen P01-04 split
- the same scientific example identities
- the same gold-decision isolation
- the same deterministic execution discipline
- the same abstention policy

B1 differs from B0 ONLY by an explicit additional evidence input channel.

That evidence channel is NOT retrieval. P01-10 remains the retrieval-assisted experiment phase.

---

## Evidence handling protocol

For B1, the supplied-evidence object must be validated before any prompt construction.

Missing or invalid evidence must fail closed or produce an explicitly defined unavailable state. B1 must not silently fall back to B0 behavior when evidence is missing unless that fallback is explicitly defined and authorized.

The supplied evidence must not:

- contain gold final_decision
- leak test membership information
- derive from labels
- leak answers
- include unauthorized full text

---

## Run manifest protocol

Every run must record a reproducible runtime manifest capturing:

- code commit
- Python version
- library versions
- model revision
- tokenizer revision
- device
- dtype
- quantization
- seed
- prompt template version
- evidence condition

The canonical run digest must exclude hostnames, absolute paths, and wall-clock/elapsed time.

---

## Report protocol

Reports must be written deterministically and must refuse to overwrite existing results.

Missing metrics must report `not_applicable` where appropriate. No experimental result may be claimed without execution authority.

---

## Abstention protocol

Parse states must be preserved explicitly:

- `parsed`
- `unparseable`
- `ambiguous`
- `generation_failed`

No parse state may be silently coerced to a clinical answer. Future B1 must not lower abstention simply because supplied evidence exists.

---

## Execution gating

Real execution requires:

1. P01-05 entry contract adopted
2. B1 evidence source ratified, if B1 execution is intended
3. Primary model gated access reviewed
4. Separate founder authorization for real execution

No execution may proceed without all required gates satisfied.
