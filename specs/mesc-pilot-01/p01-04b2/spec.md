# MESC Pilot-01 — P01-04B2 Specification

Status: **design decisions ratified — implementation and execution not authorized**

---

## Problem statement

P01-04B1 adopted a fixture-only deterministic split core. The adopted behavior satisfies only part of the P01-04B acceptance criteria enumerated in `specs/mesc-pilot-01/p01-04/acceptance.md`.

The remaining work required for P01-04B acceptance includes:

1. A public, deterministic in-memory splitter facade that can be tested with synthetic fixtures while remaining impossible to invoke accidentally against canonical real inputs.
2. Typed artifact builders for canonical JSONL serialization of split registries.
3. Split fingerprint construction and verification (distinct from the 16-hex truncated hash B1 already provides).
4. Leakage-detection primitives (exact identity, normalized equality, token-set Jaccard near-duplicate).
5. A fixture-only integration entry point with write-path and overwrite protections.
6. Complete synthetic acceptance tests demonstrating the above.

This document defines the ratified design for the remaining P01-04B tooling entry gate between P01-04B1 and P01-04C. The design decisions are resolved by founding owner ratification; implementation and execution remain unauthorized.

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

## Scope boundaries

P01-04B2 covers:

- Public facade and safety boundary design for deterministic split allocation
- Artifact type definitions and canonical serialization rules
- Leakage-detection primitive specifications (library design, not execution)
- Fixture-only entry point design (CLI boundary proposal only)
- Split fingerprint artifact schema and verification rules
- Synthetic 1,000-row fixture strategy

P01-04B2 does not cover:

- P01-04C fixture qualification
- P01-04D formal split generation against P01-03G registry
- P01-04E leakage audit execution
- P01-04F freeze and acceptance
- P01-04G repository promotion
- P01-04B1 pure split core (already adopted)
- Any modification to `src/medscale/mesc/split.py` data contracts (`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, `PilotLeakageAuditReport`)
- Any modification to P01-04A decisions D1–D10

## Required future behavior (proposed, not authorized)

### 1. Public splitter facade

The future tooling must provide a public deterministic in-memory splitter facade that:

- accepts synthetic fixture rows only;
- refuses canonical real inputs without explicit authorization;
- produces byte-identical outputs on repeated runs with identical inputs;
- raises a distinct error on any real-registry invocation attempt;
- never writes to disk unless explicitly authorized.

The facade must be testable without any real dataset, model, or registry access.

### 2. Typed artifact builders

Future artifact builders must produce:

- `group-registry.jsonl` — one JSON object per source-document group
- `example-split-registry.jsonl` — one JSON object per example
- `split-summary.json` — aggregate counts and label distributions
- `split-fingerprint.json` — full 64-hex SHA-256 fingerprint of canonical payload
- `excluded-or-unassigned-ledger.json` — any unassigned examples

All artifacts must use canonical JSON serialization with deterministic byte output.

### 3. Canonical serialization

All JSONL outputs must use:

- sorted keys (recursive);
- UTF-8 encoding;
- no BOM;
- LF-only line endings;
- object ordering: `(assigned_split, group_id)` for group registry; `(assigned_split, row_ordinal)` for example registry;
- `ensure_ascii=False`;
- `allow_nan=False`;
- separators: `(",", ":")`;
- no indentation;
- terminal newline policy: LF at end of each line;
|- identical output on repeated runs with identical inputs across supported runtimes.

### 4. Split fingerprint construction and verification

Future tooling must distinguish:

- `split_hash` (16-hex truncated SHA-256): already implemented in B1 for in-memory manifest integrity;
- `split-fingerprint.json` (full 64-hex SHA-256): proposed new artifact covering the complete canonical split payload including all assignment rows, group structure, and schema version.

The split fingerprint must be recomputable from the promoted artifacts alone and must equal the value recorded in `split-summary.json`.

### 5. Leakage-detection primitives

Future leakage-detection primitives must provide:

- exact-example cross-partition check (byte-identical `example_id` in multiple partitions);
- source-document cross-partition check (byte-identical `source_document_id` in multiple partitions);
- exact-question equality (byte-identical question text);
- normalized-question equality (NFKC, case-folded, whitespace-collapsed);
- token-set Jaccard near-duplicate detection (threshold >= 0.90);
- deterministic finding identifiers (stable across reruns);
- no suppression of findings;
- no leakage of raw question, context, or answer text into promotable artifacts.

### 6. Fixture-only integration entry point

The future fixture-only entry point must:

- accept only synthetic fixture inputs (injected rows or fixture file path);
- reject canonical P01-03G registry paths;
- reject external evidence-root destinations;
- require no real execution authorization;
- produce deterministic outputs writeable only to a designated workspace;
- support exit-code classes consistent with MedScale CLI governance.

### 7. Write-path and overwrite protections

Future write-path controls must:

- require unique temporary names for all in-progress writes;
- enforce no-overwrite semantics on completed artifacts;
- use atomic rename for finalization;
- reject concurrent writer attempts;
- preserve invalidated candidates without modification;
- cleanup failed writes from the workspace only, never from the evidence root or repository.

## Safe-publication constraints

No P01-04B2 artifact or interface may expose:

- question text
- context text
- long-answer text
- per-example answer labels
- local paths
- usernames
- hostnames
- runtime timestamps (beyond ISO date in ratified fields)
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
