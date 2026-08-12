# MESC Pilot-01 — P01-05 Plan

Status: **baseline runner entry contract**

Authorization: Entry *** defined — real execution not authorized

---

## Phase overview

P01-05 is the documentation and governance phase that defines the B0/B1 baseline runner entry contract after P01-04 completion and MESC vNext architecture ratification.

It does not execute inference. It does not download model weights. It does not implement B1. It does not modify B0 implementation. It does not start P01-06. It does not start MESC vNext implementation stages.

---

## Phase sequence context

Within the broader Pilot-01 plan:

```text
P01-01 — Foundation contracts — COMPLETED
P01-02 — Dataset identity, rights, and immutable revision lock — COMPLETED
P01-03 — Dataset transformation and validation — PLANNING AUTHORIZED / EXECUTION NOT AUTHORIZED
P01-04 — Frozen split and leakage audit — CANONICALLY RATIFIED / CLOSED
P01-05 — B0/B1 baseline runner — ENTRY CONTRACT DEFINED / EXECUTION NOT AUTHORIZED
P01-06 — Colab feasibility smoke run — NOT AUTHORIZED
P01-07 — First QLoRA run — NOT AUTHORIZED
P01-08 — B2/B3 evaluation — NOT AUTHORIZED
P01-09 — Clinical and external comparators — NOT AUTHORIZED
P01-10 — Retrieval-assisted experiments — NOT AUTHORIZED
P01-11 — Evidence Judge validation — NOT AUTHORIZED
P01-12 — Paper evidence package — NOT AUTHORIZED
```

---

## P01-05 activities

1. Reconcile existing B0 implementation truth.
2. Reconcile B0 "without supplied evidence" semantics.
3. Define B1 prospectively and unambiguously.
4. Define the B1 supplied-evidence object contract.
5. Determine B1 evidence source from existing canonical contracts.
6. Reconcile model authority so stale references are explicitly superseded.
7. Classify the implementation delta.
8. Record provenance / vNext compatibility statement.
9. Preserve uncertainty / abstention semantics.

---

## P01-05 inputs

- Frozen P01-04 split and leakage audit (canonically ratified)
- MESC vNext architecture (canonically ratified)
- Existing B0 implementation (`_b0.py`, `_pilot_loader.py`, `mesc_eval.py`, validation surfaces)
- Existing Pilot-01 spec, plan, tasks, model-selection, model-landscape
- Founder constraint prohibiting Chinese model families for MESC execution

---

## P01-05 outputs

- `specs/mesc-pilot-01/p01-05/README.md`
- `specs/mesc-pilot-01/p01-05/spec.md`
- `specs/mesc-pilot-01/p01-05/plan.md`
- `specs/mesc-pilot-01/p01-05/data-model.md`
- `specs/mesc-pilot-01/p01-05/execution-protocol.md`
- `specs/mesc-pilot-01/p01-05/decision-record.md`
- `specs/mesc-pilot-01/p01-05/acceptance.md`

plus controlling supersession annotations on existing Pilot-01 documents where necessary.

---

## P01-05 acceptance criteria

See `acceptance.md`.

---

## Stop conditions

- Any real model execution or weight download attempted.
- B1 evidence source fabricated rather than canonically determined.
- Retrieval smuggled into B1.
- Model authority reconciliation erases historical records instead of superseding them.
- P01-06 or later phase authorized.
- Any source, test, or script code changed.

---

## Authorization status

P01-05 entry contract: CANONICALLY DEFINED

B0 implementation: EXISTING / RECONCILED

B0 execution: NOT AUTHORIZED

B1 implementation: NOT AUTHORIZED

B1 execution: NOT AUTHORIZED

P01-06: NOT AUTHORIZED

vNext Stage 1 implementation: NOT AUTHORIZED
