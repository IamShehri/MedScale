# MESC Pilot-01 — P01-04B2 Specification

Status: **design decisions founder-ratified — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

## Problem statement

P01-04B1 adopted a fixture-only deterministic split core. The adopted behavior satisfies only part of the P01-04B acceptance criteria enumerated in `specs/mesc-pilot-01/p01-04/acceptance.md`.

The remaining work required for P01-04B acceptance includes:

1. A public deterministic in-memory splitter facade that can be tested with synthetic fixtures while remaining impossible to invoke accidentally against canonical real inputs.
2. Typed artifact builders for canonical JSONL serialization of split registries.
3. Split fingerprint construction and verification (distinct from the 16-hex truncated hash B1 already provides).
4. Leakage-detection primitives (exact identity, normalized equality, token-set Jaccard near-duplicate).
5. A fixture-only integration entry point.
6. Complete synthetic acceptance tests demonstrating the above.

This document defines the founder-ratified design for the remaining P01-04B tooling entry gate between P01-04B1 and P01-04C. The design decisions are resolved by the founder; implementation and execution remain unauthorized.

## Scope boundaries

P01-04B2 covers:

- Public facade and safety boundary design for deterministic split allocation
- Artifact type definitions and canonical serialization rules
- Leakage-detection primitive specifications (library design, not execution)
- Split fingerprint artifact schema and verification rules
- Synthetic fixture suite (`exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`)

P01-04B2 does not cover:

- P01-04C fixture qualification
- P01-04D formal split generation against P01-03G registry
- P01-04E leakage audit execution
- P01-04F freeze and acceptance
- P01-04G repository promotion
- P01-04B1 pure split core (already adopted)
- Any modification to `src/medscale/mesc/split.py` data contracts (`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, `PilotLeakageAuditReport`)
- Any modification to P01-04A decisions D1–D10

## Ratified design requirements

The following requirements are founder-ratified. They do not authorize implementation.

### B2C — Fixture-only public facade and integration entry point

B2C is library-only and in-memory.

The facade:

- accepts only a structurally verified in-memory `FixtureSplitRequest`;
- raises a distinct error on any real-registry invocation attempt;
- produces deterministic output in memory only;
- performs no publication;
- accepts no arbitrary filesystem input path;
- accepts no arbitrary filesystem output path;
- requires no capability token or external authorization;
- performs no write-path, overwrite, or concurrency handling.

The facade is separate from the existing `SourceDocumentGroupedSplitter.assign()` fail-closed stub.

The future formal P01-04D executor is a separate private entry point under separate authorization.

B2 does not add a CLI. CLI work is deferred beyond B2D and requires separate founder authorization.

### B2D — Integrated synthetic qualification

Qualification uses exactly three fixtures:

- `exact-reference-1000-v1`
- `constraint-stress-1000-v1`
- `leakage-positive-v1`

No document may reduce qualification to one generic 1,000-row fixture.

### B2 identity and fingerprint

Full 64-hex `split_fingerprint` is the sole authoritative identity. The 16-hex `split_hash` is B1 compatibility/display-only.

### Promotable artifact constraints

No date or timestamp field is permitted in a fingerprinted promotable split artifact.

No Python-version-pinning limitation applies. Canonical JSON/JSONL is stable across Python 3.11/3.12 and supported operating systems.

Atomic publication, no-overwrite and concurrency controls apply to separately authorized artifact-publication components. They are not filesystem output behavior of `FixtureSplitFacade`.

### Leakage policy

Exact and normalized leakage rules follow FD-B2-6. Empty normalized questions are not automatically classified clean. Suppression is prohibited. A positive qualification fixture produces non-empty expected findings.

## Safe-publication constraints

No P01-04B2 artifact or interface may expose:

- question text
- context text
- long-answer text
- per-example answer labels
- local paths
- usernames
- hostnames
- runtime timestamps
- command logs
- workspace locations

This list is bounded by the D9 public-repository policy and the canonical rights-and-provenance record.

## Single-writer and concurrency risk

The current B0 report writer has a documented single-writer limitation. P01-04B2 tooling must not introduce additional concurrency assumptions. Write-path controls must explicitly reject concurrent access rather than silently serialize it.

## Why real data remains prohibited

Real P01-03G registry execution under P01-04B2 is prohibited because:

- P01-04B2 is a documentation and entry-gate task only.
- Real execution requires P01-04D authorization, which requires P01-04B and P01-04C acceptance first.
- P01-04B is incomplete; P01-04B2 does not complete it.
- No founder authorization for P01-04D exists.
- Accidental invocation against canonical inputs must remain architecturally impossible until P01-04D authorization is explicitly granted.
