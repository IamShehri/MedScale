# MESC Pilot-01 — P01-04B2A Authorization Gate

Status:
**PROPOSED AUTHORIZATION GATE — FOUNDER DECISION PENDING**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Purpose

This package proposes the exact implementation boundary for **P01-04B2A —
Deterministic Artifact Types and Canonical Serialization**. It freezes artifact
contracts, identifies future implementation and test paths, records the
remaining B2A-specific founder decisions, and requests founder authorization.
It does not grant that authorization and it does not authorize any further
increment.

PR #54 ratified the P01-04B2 *design* package; it did not authorize B2A
implementation or execution. Merge of this documentation PR must not be
interpreted as implementation authorization unless the founder decision record
in this package explicitly grants it.

## Authority hierarchy

| Layer | Authority | Current status |
|---|---|---|
| Founder authorization | Ratification of split policy, ratios, grouping invariant, leakage taxonomy | **Ratified** (P01-04A) |
| P01-04A specification | `specs/mesc-pilot-01/p01-04/*` | **Ratified** |
| P01-04B1 implementation | Fixture-only deterministic split core | **Adopted**; private, in-memory, fixture-only; execution authority: none |
| P01-04B2 design | Founder-ratified entry gate (FD-B2-1 through FD-B2-8) | **Design ratified**; implementation not authorized; execution not authorized |
| P01-04B2A design | Deterministic artifact types and canonical serialization | **Proposed**; founder decision pending; implementation not authorized |
| P01-04B overall | Tooling complete and accepted | **Not met** |
| P01-04B2B–B2D | Separately proposed increments | **Not authorized** |
| P01-04C–G stages | Separate authorizations each | **Not authorized** |
| Formal split execution | Separate authorization required | **Not authorized** |

## B2A boundary

P01-04B2A may later implement only:

1. private immutable artifact-contract types;
2. canonical in-memory JSON serialization;
3. canonical in-memory JSONL serialization;
4. SHA-256 artifact descriptors;
5. non-circular authoritative split-fingerprint construction;
6. validation and typed fail-closed errors;
7. synthetic unit and golden-vector tests.

P01-04B2A must not implement:

- leakage detection or classification;
- fixture facade or public splitter activation;
- CLI or filesystem publication;
- atomic rename/write behavior;
- real P01-03G loading or partition generation;
- dataset, model, inference, training, or metrics access.

No new public export is permitted in B2A. Public exposure, fixture
integration, and execution entry points belong to later separately authorized
increments.

## Relationship to B1 and B2B–D

B2A may reference B1 identities without changing B1 serialization or behavior.
B2B requires separate authorization after B2A acceptance. B2C requires
separate authorization after B2A and B2B acceptance. B2D requires separate
authorization after B2A, B2B, and B2C acceptance.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| `spec.md` | Functional scope, non-goals, deterministic behavior, security/provenance boundaries |
| `contracts.md` | Proposed canonical value domain, serialization contracts, artifact descriptors, identity model, error taxonomy |
| `decision-record.md` | Proposed PD-B2A-1 through PD-B2A-8 pending founder decision |
| `plan.md` | Documentation gate, founder decision, implementation authorization, exact-head CI, Opus review, merge decision |
| `acceptance.md` | Documentation-gate acceptance, future implementation acceptance, execution prohibitions |
| `implementation-task.md` | Future implementation and test brief; not executable without explicit founder authorization |
