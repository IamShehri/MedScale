# MESC Pilot-01 — P01-04B2A Authorization Gate

Status:
**FOUNDER-RATIFIED CONTRACT GATE — ADOPTED ON CANONICAL MAIN**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Acceptance:
**B2A NOT ACCEPTED**

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

Canonical adoption:
`5c083a0c5f23d0f9837e7543c444633a68524e67`

Adoption PR:
`#55`

Reviewed PR head:
`edc09743a1aa9478c2accbe9debb8fcc5bcbe268`

Founder decision date:
`2026-07-26`

Canonical founder record:
`founder-ratification.md`

---
## Purpose

This package defines the exact implementation boundary for P01-04B2A —
Deterministic Artifact Types and Canonical Serialization. It records the
artifact contracts, identifies future implementation and test paths, and
carries the B2A-specific founder decisions.

## Package state after adoption

The proposal documents in this package — `spec.md`, `contracts.md`,
`decision-record.md`, `plan.md`, `acceptance.md` and `implementation-task.md` —
preserve their reviewed pre-ratification wording. Their pending-decision
markers describe the state at the reviewed head and are retained as a
historical record; they are not the current authority.

The additive `founder-ratification.md` record is controlling for authority.
Under it:

- PD-B2A-1 through PD-B2A-8 were adopted as FD-B2A-1 through FD-B2A-8 on
  2026-07-26;
- FD-B2A-5 incorporates the clarification and validation sequence recorded
  under the historical proposal label PD-B2A-5.1;
- ratification freezes the contract decisions only;
- implementation remains separately unauthorized.

PR #54 ratified the P01-04B2 *design* package; PR #55 adopted this B2A contract
gate. Neither authorizes B2A implementation or execution. Merging or recording
this documentation does not authorize implementation.

## Authority hierarchy

| Layer | Authority | Current status |
|---|---|---|
| Founder authorization | Ratification of split policy, ratios, grouping invariant, leakage taxonomy | **Ratified** (P01-04A) |
| P01-04A specification | `specs/mesc-pilot-01/p01-04/*` | **Ratified** |
| P01-04B1 implementation | Fixture-only deterministic split core | **Adopted**; private, in-memory, fixture-only; execution authority: none |
| P01-04B2 design | Founder-ratified entry gate (FD-B2-1 through FD-B2-8) | **Design ratified**; implementation not authorized; execution not authorized |
| P01-04B2A contracts | Deterministic artifact types and canonical serialization (FD-B2A-1 through FD-B2A-8) | **Founder-ratified 2026-07-26**; adopted on canonical main (`5c083a0c5f23d0f9837e7543c444633a68524e67`); implementation not authorized; execution not authorized; **B2A not accepted** |
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

## N-12 binding sequencing consequences

The founder-ratified N-12 decision recorded in `founder-ratification.md` binds
the following:

- Linux evidence on Python 3.11 and Python 3.12 is partial evidence only.
- B2A cannot be accepted while the Windows and macOS portability evidence
  remains open.
- Validation-infrastructure or workflow changes require separate founder
  authorization; this package authorizes none.
- B2B remains blocked until B2A acceptance.
- Merging or recording this documentation does not authorize implementation.

Until that evidence is produced and independently reviewed, B2A remains not
accepted, the portability obligation remains open, and no artifact may be
promoted on the claim of completed cross-platform determinism.

## Cross-platform portability validation gate

The validation-gate design for the cross-platform portability evidence
infrastructure required by N-12 was merged through PR #57.

Canonical adoption:
`30f79b183a4fff6a08e30e1e43f5da549ce20c1a`

Final merged PR head:
`b76420913c80bd54fd31e63ccffd5ed43a36a854`

Source branch:
`docs/mesc-p01-04b2a-portability-gate` — deleted after verified post-merge cleanup.

Post-merge verification on canonical main:
- CI `30233225446` — success
- CodeQL `30233225421` — success
- Optional Extras / Backends `30233225422` — success

Those runs are standard Linux quality and security gates; they are not the
six-cell golden-vector portability evidence required for B2A acceptance.

Current state:

- portability infrastructure gate designed, founder-ratified, and adopted on
  canonical main through PR #57, with FD-PV-1 through FD-PV-10 recorded on
  2026-07-27 and FD-PV-6 numeric limits selected;
- canonical adoption is `30f79b183a4fff6a08e30e1e43f5da549ce20c1a`;
- infrastructure implementation remains **not authorized**;
- portability evidence was **not produced**;
- the standard Linux workflows are quality/security gates only;
- Windows and macOS portability evidence remains **open**;
- B2A remains **not accepted**;
- B2B remains **not authorized**.

The gate design is at `../p01-04b2a-portability/`. It does not alter FD-B2A-1
through FD-B2A-8, does not authorize implementation or execution, and does not
produce or claim any portability evidence.

## Document index

| File | Purpose |
|---|---|
| `README.md` | This document |
| `founder-ratification.md` | Canonical additive founder-authority record for FD-B2A-1 through FD-B2A-8 and N-12 |
| `spec.md` | Functional scope, non-goals, deterministic behavior, security/provenance boundaries |
| `contracts.md` | Canonical value domain, serialization contracts, artifact descriptors, identity model, error taxonomy |
| `decision-record.md` | Historical PD-B2A-1 through PD-B2A-8 proposals as reviewed before ratification |
| `plan.md` | Documentation gate, founder decision, implementation authorization, exact-head CI, Opus review, merge decision |
| `acceptance.md` | Documentation-gate acceptance, future implementation acceptance, execution prohibitions |
| `implementation-task.md` | Future implementation and test brief; not executable without explicit founder authorization |
