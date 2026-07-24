# MESC Pilot-01 — P01-04B2 Decision Record

Status: **design decisions founder-ratified — implementation and execution not authorized**

Historical proposals:
PD-1 through PD-8, non-normative and superseded where inconsistent

Normative resolutions:
FD-B2-1 through FD-B2-8

Authoritative normative record:
founder-ratification.md

---

## PD-1 — Public splitter semantics (historical)

Historical proposal context.

Matching normative resolution: FD-B2-1.

FD-B2-1 controls on conflict. Ratified resolution summary:

Existing `SourceDocumentGroupedSplitter.assign()` remains unconditionally fail-closed. B2 uses a separate `FixtureSplitFacade` that accepts only a structurally verified in-memory `FixtureSplitRequest`. No capability/token is required. No B2 CLI exists. No arbitrary filesystem input path is accepted. No arbitrary filesystem output path is accepted. The fixture facade performs no publication. Formal P01-04D execution remains a separate entry point under separate authorization.

---

## PD-2 — Split-hash identity (historical)

Historical proposal context.

Matching normative resolution: FD-B2-2.

FD-B2-2 controls on conflict. Ratified resolution summary:

Full 64-hex `split_fingerprint` is the sole authoritative identity. The 16-hex `split_hash` is compatibility/display-only. No outstanding contract decision remains.

---

## PD-3 — Date fields and reproducibility (historical)

Historical proposal context.

Matching normative resolution: FD-B2-3.

FD-B2-3 controls on conflict. Ratified resolution summary:

Promotable fingerprinted artifacts contain no date or timestamp fields. Provenance dates belong outside deterministic promotable bytes.

---

## PD-4 — Canonical JSONL (historical)

Historical proposal context.

Matching normative resolution: FD-B2-4.

FD-B2-4 controls on conflict. Ratified resolution summary:

Canonical JSON/JSONL is stable across Python 3.11/3.12 and supported operating systems. No single-Python-version limitation applies.

---

## PD-5 — Atomic publication and concurrency (historical)

Historical proposal context.

Matching normative resolution: FD-B2-5.

FD-B2-5 controls on conflict. Ratified resolution summary:

Atomic publication, no-overwrite and concurrency controls apply to separately authorized artifact-publication components. They must not be misrepresented as filesystem output behavior of `FixtureSplitFacade`.

---

## PD-6 — Leakage normalization and classification (historical)

Historical proposal context.

Matching normative resolution: FD-B2-6.

FD-B2-6 controls on conflict. Ratified resolution summary:

Exact and normalized leakage rules match founder ratification. Empty normalized questions are not automatically classified clean. Suppression is prohibited. A positive qualification fixture produces non-empty expected findings.

---

## PD-7 — Fixture identity (historical)

Historical proposal context.

Matching normative resolution: FD-B2-7.

FD-B2-7 controls on conflict. Ratified resolution summary:

Qualification uses exactly `exact-reference-1000-v1`, `constraint-stress-1000-v1`, and `leakage-positive-v1`. No document may reduce this to one generic 1,000-row fixture.

---

## PD-8 — Entry-point and CLI boundary (historical)

Historical proposal context.

Matching normative resolution: FD-B2-8.

FD-B2-8 controls on conflict. Ratified resolution summary:

B2 is library-only and in-memory. CLI is deferred beyond B2D and requires separate founder authorization.

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

## Ratification does not imply authorization

Completion of P01-04B2 documentation does not authorize implementation.
Completion of P01-04B2 implementation does not authorize execution.
Execution authorization requires explicit founder authorization for each stage
(P01-04B, P01-04C, P01-04D, etc.).

Founder Abdulaziz M. Alshehri ratified FD-B2-1 through FD-B2-8 on 2026-07-24.
Repository adoption occurs when the P01-04B2 documentation PR referring to this ratification is merged.
Any future amendment requires a new founder decision and independent review.
