# MESC Pilot-01 — P01-04A Specification and Policy Ratification

Status: **specification and policy only — no execution authorized**
Branch: `docs/mesc-p01-04a-spec-policy`
Ratification review baseline: cd0f72b0ee9720f06d95dfa01862a4f403c31b16

---

## Current maintenance context

This historical P01-04A ratification package is currently maintained as part
of the broader P01-04 governance record.

Current maintenance branch:
`docs/mesc-p01-04b2-founder-ratification`

Current canonical documentation baseline:
`ce1272235cb48dbacdb18f20e1ae8db695b01328`

These current-maintenance references do not replace, amend, or reinterpret the
original P01-04A ratification branch or review baseline.

## Purpose

P01-04A exists solely to record the canonical specification, scientific policy, artifact contracts, acceptance criteria, and execution-safety protocol for the future split-and-leakage-audit phase (P01-04). Nothing in this package authorizes execution.

## Authority hierarchy

| Layer | Authority | Current status |
|---|---|---|
| Founder authorization | Ratification of split policy, ratios, grouping invariant, leakage taxonomy | **Ratified** |
| P01-04A specification | This package | **Ratified** |
| P01-04B1 implementation | Fixture-only deterministic split core | **Adopted**; original adoption merge `2937d735df09851384bfa9a15fb8b1f908c62b6d`; current canonical main `ce1272235cb48dbacdb18f20e1ae8db695b01328`; private, in-memory, fixture-only; execution authority: none |
| P01-04B2 design | Founder-ratified entry gate (FD-B2-1–FD-B2-8) | **Design ratified on 2026-07-24**; implementation not authorized; execution not authorized |
| P01-04B overall | Incomplete; B2A–B2D not started | **Not met** |
| P01-04C–G stages | Separate authorizations each | **Not authorized** |
| P01-05 and later | Separate authorization | **Not authorized** |
| Formal split execution | Separate authorization required | **Not authorized** |

## Stage status

P01-04A was ratified for specification and policy only on 2026-07-20.
No code execution, split generation, leakage audit, or partition membership
has been authorized. Review reference: `P01-04A-final-ratification-review-20260720-707195f1`.

## P01-04B1 — Fixture-only deterministic split core (adopted)

PR #51 adopted the fixture-only deterministic split core on canonical main.
The adopted behavior is private, in-memory, and synthetic-fixture-safe.
It does not authorize real split generation or public splitter activation.

- Reviewed PR head: `34774a8308818d5c3b4875920be34728ddf18f22`
- Merge commit: `2937d735df09851384bfa9a15fb8b1f908c62b6d`

Adopted behavior includes canonical full-SHA-256 example-ID derivation,
identity-only extraction from source-record envelopes, fail-closed label joins,
exact constrained apportionment, deterministic SHA-256 source-document ranking,
indivisible group allocation, canonical JSON-byte primitives, and synthetic fixture tests.

P01-04B1 intentionally does not provide filesystem entry points,
make `SourceDocumentGroupedSplitter.assign()` publicly executable,
create formal split artifacts, generate or disclose real partition membership,
implement leakage auditing, or authorize P01-04C–G.

## MESC B0 deterministic execution spine (adopted separately)

PR #52 adopted the deterministic B0 execution spine on canonical main.
This is a separate workstream from P01-04B1 split-tooling nomenclature.
It does not authorize model or dataset download, real inference, training,
formal metrics, partition generation, validation/test access, or clinical claims.

- Reviewed PR head: `23841257f7b189628abe47d0b709775275de341a`
- Merge commit: `3edf328f583f13fcd9d566e5080ec3cce83ae178`

## Nomenclature boundary

| Name | Workstream | Status |
|---|---|---|
| P01-04B1 | Split-tooling subphase (pure deterministic split core) | Adopted |
| MESC B0 | Model-execution spine | Adopted |
| MESC B1 | Model-runner / experiment phase | Not evidenced as completed |
| P01-04B2 | Remaining tooling design gate | Design ratified; implementation and execution not authorized |

P01-04B1 and MESC B0/B1 are different workstreams and are not interchangeable.
P01-04B1 does not authorize model execution.
MESC B0/B1 adoption does not authorize split generation.

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
