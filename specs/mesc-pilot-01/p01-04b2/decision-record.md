# MESC Pilot-01 — P01-04B2 Decision Record

Status: **specification and entry-gate proposal only — implementation and execution not authorized**

This document records **proposed** decisions for P01-04B2 tooling. No decision in this document is accepted, ratified, or implemented. Ratified decisions remain in `specs/mesc-pilot-01/p01-04/decision-record.md` (D1–D10).

All unresolved items must be reviewed and resolved by the founder before any implementation authorization.

---

## Ratified decisions (P01-04A — not repeated here)

D1–D10 remain ratified policy as recorded in `specs/mesc-pilot-01/p01-04/decision-record.md`. They are not re-ratified here. Any P01-04B2 proposal that conflicts with D1–D10 is subordinate to D1–D10.

## Implementation status

| Decision area | Status |
|---|---|
| D1–D10 ratified policy | Ratified (P01-04A); unchanged |
| P01-04B1 pure split core | Implemented and adopted on canonical main (`2937d73`) |
| Public splitter facade | Not implemented; proposed in B2C |
| Leakage-detection library | Not implemented; proposed in B2B |
| Artifact builders | Not implemented; proposed in B2A |
| Split fingerprint artifact (64-hex) | B1 provides 16-hex truncated hash; proposed extension in B2A |
| CLI entry point | Not implemented; proposed in B2C |
| Real split execution | Not authorized |
| Leakage audit execution | Not authorized |
| P01-04C–G stages | Not authorized |

## Proposed decisions pending founder ratification

### PD-1 — Public splitter semantics

**Proposed decision:** `SourceDocumentGroupedSplitter.assign()` in its future authorized form must accept only synthetic fixture rows and must refuse canonical real inputs.

**Alternatives considered:**

1. Explicit fixture-only request type injected at call time
2. Injected source rows with no disk access
3. Authorization capability/token required at instantiation
4. Private implementation with guarded public facade

**Recommended path:** Private implementation with guarded public facade (option 4), using explicit fixture-only request type (option 1) for integration entry point.

**Status:** PENDING FOUNDER DECISION

### PD-2 — Split-hash identity

**Proposed decision:** Distinguish two hash values with different authority:

- `split_fingerprint` (64 lowercase hexadecimal characters; full SHA-256 over the defined canonical split bundle) is the **sole authoritative split identity** for every formal artifact and all cross-generation verification. The canonical bundle must bind all assignment rows, source-document group structure, `split_seed`, `algorithm_version`, and `schema_version`.
- `split_hash` (16 lowercase hexadecimal characters; truncated SHA-256) is a **compatibility and display value only**, retained for B1 `PilotSplitManifest.computed_split_hash`. It is never authoritative, must never identify a promotable artifact, and must never be used for cross-generation equality.

The 16-hex compatibility value must never be silently treated as equivalent to the full 64-hex fingerprint.

**Status:** PENDING FOUNDER DECISION

### PD-3 — Date fields and reproducibility

**Proposed decision:**

- `ratified_at`: ISO date only, injected at authorization time, excluded from fingerprint payloads.
- `generated_at`: ISO date only, NOT populated by runtime timestamp generation in deterministic artifacts.
- No runtime timestamps in any deterministic artifact.
- Date fields excluded from fingerprint payloads to ensure reproducibility across time zones and clock drift.

**Status:** PENDING FOUNDER DECISION

### PD-4 — Canonical JSONL

**Proposed decision:**

- sorted keys (recursive);
- UTF-8;
- no BOM;
- LF-only line endings;
- terminal newline at end of each line;
- `ensure_ascii=False`;
- `allow_nan=False`;
- separators: `(",", ":")`;
- no indentation;
- identical output on repeated runs with identical inputs and identical Python version.

**Status:** PENDING FOUNDER DECISION

### PD-5 — Atomic publication and concurrency

**Proposed decision:**

- unique temporary names for all in-progress writes;
- no-overwrite semantics on completed artifacts;
- atomic rename for finalization;
- concurrent writer rejection (explicit error, not silent serialization);
- invalidated candidate preservation (never overwritten or deleted);
- cleanup of failed writes from workspace only, never from evidence root or repository.

**Status:** PENDING FOUNDER DECISION

### PD-6 — Leakage normalization

**Proposed decision:**

- exact-example: byte-equality on `example_id`
- exact-source-document: byte-equality on `source_document_id`
- exact-question: byte-equality on question text
- normalized-question: NFKC normalization, case folding, whitespace collapse
- token-set Jaccard: tokenization on whitespace/punctuation boundary, Jaccard >= 0.90 threshold
- empty token sets: classified as non-leakage with explicit evidence
- finding identifiers: deterministic, stable across reruns
- **suppression is prohibited.** Every finding must carry an explicit `classification` of `unresolved`, `false_positive`, or `confirmed_leakage`. A finding remains `unresolved` unless it is classified as `false_positive` with supporting evidence or as `confirmed_leakage`. The `suppressed` flag must always be `false`. Setting `suppressed=true`, silently dropping a finding, or omitting a finding without classification is a hard stop condition that halts the audit.

**Status:** PENDING FOUNDER DECISION

### PD-7 — Fixture identity

**Proposed decision:**

- synthetic 1,000-row fixture generated from synthetic identities only;
- reproduces label totals 552/338/110;
- targets 700/150/150;
- contains no P01-03G membership;
- cannot be confused with formal dataset evidence;
- produces byte-identical repeated outputs.

**Status:** PENDING FOUNDER DECISION

### PD-8 — Entry-point and CLI boundary

**Proposed decision:**

- fixture-only entry point accepts only synthetic fixture inputs;
- rejects canonical P01-03G registry paths;
- rejects external source-record files;
- rejects evidence-root destinations;
- requires no real execution authorization;
- defines exit-code classes consistent with MedScale CLI governance.

**Status:** PENDING FOUNDER DECISION

---

## Boundary violations to avoid

The following are explicitly prohibited in any implementation authorized under P01-04B2:

- modifying `src/medscale/mesc/split.py` data contracts (`PilotSplitAssignment`, `PilotSplitManifest`, `PilotLeakageFinding`, `PilotLeakageAuditReport`) without founder decision;
- adding a public `assign()` that silently fabricates assignments without authorization;
- exposing raw question, context, or answer text in any promotable artifact;
- generating real P01-03G registry membership;
- authorizing P01-04C–G implicitly;
- modifying P01-04A decisions D1–D10;
- using runtime timestamps in deterministic artifacts;
- claiming leakage is ruled out.

---

## Implementation status is not execution authorization

Completion of P01-04B2 documentation does not authorize implementation. Completion of P01-04B2 implementation does not authorize execution. Execution authorization requires explicit founder authorization for each stage (P01-04B, P01-04C, P01-04D, etc.).
