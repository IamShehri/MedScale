# MESC Pilot-01 — P01-05 Baseline Runner Entry Contract

Status: **entry contract defined — execution not authorized**

Purpose: qualify and complete deterministic B0/B1 runner contracts before real baseline execution

---

## Purpose

P01-05 exists to define and canonically adopt the entry contract for the B0/B1
baseline runner phase. It records the prospective contracts, evidence semantics,
model authority reconciliation, and implementation delta required before any
real baseline execution may be authorized.

P01-05 is a documentation and governance phase only. It does not authorize:

- model weight download
- network model access
- real B0 run
- real B1 run
- benchmark-result generation
- publication of results

---

## Relationship to P01-04

P01-05 depends on P01-04 (frozen split and leakage audit) being complete. As of
this entry-contract adoption, P01-04 is canonically ratified and closed. P01-05
does not itself produce split artifacts or leakage-audit findings.

---

## Relationship to MESC vNext

MESC vNext is the canonically ratified target architecture. P01-05 remains a
bounded text-first Pilot-01 experiment phase. It MUST be compatible with the
ratified MESC vNext architecture, but it does NOT implement vNext multimodal
stages.

- MESC vNext: RATIFIED TARGET ARCHITECTURE
- P01-05: TEXT-FIRST BASELINE EXPERIMENT PHASE
- Multimodal implementation: NOT AUTHORIZED
- ClinicalObservation implementation: NOT AUTHORIZED
- Audio/video/image implementation: NOT AUTHORIZED

P01-05 outputs should preserve enough provenance, uncertainty, identity, and
state boundaries that future vNext layers can wrap or consume them without
changing their scientific meaning.

---

## Phase boundaries

**In scope:**

- B0 definition reconciliation
- B1 prospective definition
- B1 supplied-evidence contract definition
- B1 evidence-source determination
- Model authority reconciliation
- Implementation delta classification
- Provenance / vNext compatibility statement
- Uncertainty / abstention preservation

**Out of scope:**

- real inference
- model download
- training
- QLoRA
- retrieval
- Evidence Judge
- specialist routing
- multimodal inputs
- clinical use
- production use
- P01-06
- P01-07
- vNext implementation

---

## Authorization status

P01-05 entry contract: CANONICALLY DEFINED

B0 implementation: EXISTING / RECONCILED

B1 implementation: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES

B1 development evidence-pack tooling: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES

B1 development evidence pack: NOT PRODUCED

B0 execution: NOT AUTHORIZED

B1 execution: NOT AUTHORIZED

P01-06: NOT AUTHORIZED

vNext Stage 1 implementation: NOT AUTHORIZED

---

## Document index

- `spec.md` — P01-05 specification
- `plan.md` — P01-05 plan
- `data-model.md` — deterministic prospective contracts
- `execution-protocol.md` — execution boundary and protocol
- `decision-record.md` — model authority and evidence-source decisions
- `acceptance.md` — acceptance criteria
