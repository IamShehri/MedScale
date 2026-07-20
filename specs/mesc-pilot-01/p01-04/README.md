# MESC Pilot-01 — P01-04A Specification and Policy Ratification

Status: **specification and policy only — no execution authorized**
Branch: `docs/mesc-p01-04a-spec-policy`
Ratification review baseline: cd0f72b0ee9720f06d95dfa01862a4f403c31b16

---

## Purpose

P01-04A exists solely to record the canonical specification, scientific policy, artifact contracts, acceptance criteria, and execution-safety protocol for the future split-and-leakage-audit phase (P01-04). Nothing in this package authorizes execution.

## Authority hierarchy

| Layer | Authority | Current status |
|-------|-----------|----------------|
| Founder authorization | Ratification of split policy, ratios, grouping invariant, leakage taxonomy | **Ratified** |
| P01-04A specification | This package | **Ratified** |
| P01-04 execution | Separate authorization required | **Not authorized** |
| P01-04B tooling implementation | Separate authorization required | **Not authorized** |
| P01-04C–G stages | Separate authorizations each | **Not authorized** |
| P01-05 and later | Separate authorization | **Not authorized** |

## Stage status

P01-04A was ratified for specification and policy only on 2026-07-20.
No code execution, split generation, leakage audit, or partition membership
has been authorized. Review reference: `P01-04A-final-ratification-review-20260720-707195f1`.

## Package contents

| File | Purpose |
|------|---------|
| `README.md` | This document |
| `plan.md` | Stage decomposition and gate definitions |
| `spec.md` | Scientific objectives, invariants, and exclusion rules |
| `decision-record.md` | Ratified founder policy decisions |
| `acceptance.md` | Per-stage acceptance criteria |
| `execution-protocol.md` | Future execution-safety controls |
| `artifact-contracts.md` | Stable artifact schema inventory |
| `data-model.md` | Canonical data structures for split and audit outputs |

## Relationship to P01-03G

P01-04A depends on P01-03G. The ordered example registry (`specs/mesc-pilot-01/p01-03g/ordered-example-id-registry.jsonl`) and the source-document registry (`specs/mesc-pilot-01/p01-03g/source-document-id-registry.jsonl`) are the authoritative inputs for any future formal split generation. Those records must not be modified under P01-04A.

## Execution prohibition

P01-04A does not authorize and does not reference:

- split generation
- group assignment
- partition membership calculation
- seed execution against the real dataset
- leakage auditing
- real split registry creation
- test-set disclosure
- P01-04B or any later P01-04 stage
- P01-05 or any later Pilot-01 phase
- benchmark or model evaluation
