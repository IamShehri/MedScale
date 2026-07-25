# MESC Pilot-01 — P01-04B2 Entry-Gate Specification

Status: **design decisions founder-ratified — implementation and execution not authorized**
Branch: `docs/mesc-p01-04b2-founder-ratification`
Canonical documentation baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`
P01-04B1 original adoption merge: `2937d735df09851384bfa9a15fb8b1f908c62b6d`

---

## Purpose

P01-04B2 exists solely to define the remaining tooling entry gate between P01-04B1 and P01-04C. It decomposes the remaining P01-04B acceptance criteria into reviewable, non-executing implementation increments, identifies unresolved contract decisions, and preserves every real-execution prohibition.

P01-04B2 does not authorize implementation. It does not authorize execution. It does not authorize P01-04C–G.

## Relationship to P01-04A and P01-04B1

| Layer | Authority | Current status |
|---|---|---|
| Founder authorization | Ratification of split policy, ratios, grouping invariant, leakage taxonomy | **Ratified** (P01-04A) |
| Founder authorization | P01-04B2 design decisions (FD-B2-1 through FD-B2-8) | **Ratified on 2026-07-24** |
| P01-04A specification | `specs/mesc-pilot-01/p01-04/*` | **Ratified** |
| P01-04B1 implementation | Fixture-only deterministic split core | **Adopted** on canonical main (`ce1272235cb48dbacdb18f20e1ae8db695b01328`); original adoption merge `2937d735df09851384bfa9a15fb8b1f908c62b6d` |
| P01-04B2 design | B2 facade, leakage, fixtures, fingerprint, atomic publication | **Design ratified**; implementation not authorized |
| P01-04B overall | Tooling complete and accepted | **Not met** |
| P01-04C–G stages | Separate authorizations each | **Not authorized** |
| Formal split execution | Separate authorization required | **Not authorized** |

## Authority hierarchy

1. Founder ratification of P01-04A policy decisions (D1–D10) is the highest current authority.
2. Founder ratification of P01-04B2 design decisions (FD-B2-1 through FD-B2-8) on 2026-07-24 is binding for design.
3. P01-04B1 adopted code on canonical main `ce1272235cb48dbacdb18f20e1ae8db695b01328` is the highest current implementation authority; it was originally adopted by merge `2937d735df09851384bfa9a15fb8b1f908c62b6d`.
4. No P01-04B2 document authorizes code changes, execution, or promotion of P01-04C–G.

P01-04B2 explicitly defers to P01-04A decision-record.md for all founder policy decisions. If any P01-04B2 proposal conflicts with D1–D10, D1–D10 control. A subordinate implementation-design ratification note in `p01-04/decision-record.md` referencing FD-B2-1 through FD-B2-8 does not amend D1–D10.

## Exact canonical baseline

- Canonical main: `ce1272235cb48dbacdb18f20e1ae8db695b01328`
- Subject: `docs(mesc): reconcile P01-04B state and define B2 gate`
- PR #53 merge: `ce1272235cb48dbacdb18f20e1ae8db695b01328`
- P01-04B1 merge: `2937d735df09851384bfa9a15fb8b1f908c62b6d`
- P01-04B1 reviewed PR head: `34774a8308818d5c3b4875920be34728ddf18f22`

## Current implementation inventory

### Adopted on canonical main (P01-04B1)

The following B1 behavior is present on canonical main at `ce1272235cb48dbacdb18f20e1ae8db695b01328` and was originally adopted by PR #51 merge `2937d735df09851384bfa9a15fb8b1f908c62b6d`.

- `src/medscale/mesc/split.py`:
  - `PilotSplitAssignment` dataclass (frozen, stable fields)
  - `PilotSplitManifest` dataclass (frozen, stable fields)
  - `PilotSplitManifest.computed_split_hash` — 16-hex truncated SHA-256 from canonical payload
  - `PilotSplitManifest._canonical_payload()` — canonical serialization
  - `PilotSplitNotAuthorizedError(NotImplementedError)` — explicitly raised
  - `SourceDocumentGroupedSplitter.assign()` — raises unconditionally; real allocation not implemented
  - `PilotLeakageFinding` dataclass
  - `PilotLeakageAuditReport` dataclass
- `src/medscale/mesc/_split_v1.py`: private deterministic split core (fixture-safe, in-memory only)
- `tests/test_mesc_split.py`: synthetic fixture tests for deterministic split contracts
- `tests/test_mesc_split_v1.py`: synthetic fixture tests for private split core

### Design ratified but not implemented

The following are not present on canonical main and are not authorized for implementation in this task.

- Public deterministic split facade
- Leakage-detection library
- Artifact builders for JSONL outputs
- Split fingerprint artifact construction
- Integration tests exercising 1,000-row synthetic fixture end-to-end
- Any real P01-03G registry execution

## Implementation inventory — detailed

| Component | Location | Adopted | Notes |
|---|---|---|---|
| Data contracts (frozen dataclasses) | `src/medscale/mesc/split.py` | Yes | Stable; do not modify without founder decision |
| Truncated split hash (16 hex) | `PilotSplitManifest.computed_split_hash` | Yes | B1 only; B2 may introduce full fingerprint artifact |
| Private split core | `src/medscale/mesc/_split_v1.py` | Yes | Fixture-safe, in-memory, not public |
| Public splitter facade | Not present | No | Requires separate founder authorization |
| Leakage primitives | Not present | No | Requires separate founder authorization |
| Artifact serialization | Not present | No | Requires separate founder authorization |
| CLI entry point | Not present | No | Deferred beyond B2D; requires separate founder authorization |
| Fail-closed stub | `SourceDocumentGroupedSplitter.assign()` | Yes | Raises `PilotSplitNotAuthorizedError` |

## Prohibited activities

P01-04B2 does not authorize and does not reference:

- real split generation against P01-03G registry
- leakage audit execution
- reading the external `source-records.jsonl`
- accessing validation/test partition content
- modifying `src/**` or `tests/**`
- downloading datasets or models
- running inference or training
- executing formal metrics
- authorizing P01-04C–G
- authorizing P01-05 or later
- claiming leakage is ruled out
- claiming P01-04B is accepted

## Document index

| File | Purpose |
|------|---------|
| `README.md` | This document |
| `spec.md` | Problem definition and scope boundaries |
| `plan.md` | B2A–B2D decomposition |
| `acceptance.md` | Documentation entry-gate acceptance criteria |
| `contracts.md` | Founder-ratified design type contracts without Python implementation |
| `data-model.md` | Entity relationships and data flow |
| `research.md` | Design evidence and gap analysis |
| `decision-record.md` | Ratified design decisions (FD-B2-1 through FD-B2-8) and historical proposed decisions (PD-1 through PD-8) |
| `founder-ratification.md` | Canonical founder-authorization record for FD-B2-1 through FD-B2-8 |
| `implementation-task.md` | Future implementation brief (not authorized) |
