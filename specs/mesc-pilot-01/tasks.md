# MESC Pilot-01 — Tasks

Status: **foundation task registry**
Authorization: Foundation authorized; execution not authorized
Freeze date: 2026-07-17

---

## Task registry

```text
P01-T01 — Complete foundation contracts
Status: COMPLETED
Prerequisites: frozen model selection, dataset selection, architecture registration
Outputs: deterministic contracts, split contracts, manifest contracts, evaluation metrics, smoke fixture, architecture tests
Acceptance: typing clean, lint clean, full Pytest passes, Mypy passes, staging empty
Stop conditions: prohibited imports, weakened enforcement, changed semantics, stale counts accepted without evidence
```

```text
P01-T02 — Verify model metadata and revisions
Status: COMPLETED
Prerequisites: P01-01 complete
Outputs: model metadata record; revision pin list; license matrix
Acceptance: all metadata recorded; no weights downloaded
Stop conditions: gated-access requirements ignored; model identity unresolved
```

```text
P01-T03 — Verify dataset license and source rights
Status: COMPLETED
Prerequisites: P01-01 complete
Outputs: license review record; rights summary; immutable revision assignment
Acceptance: license and rights documented; revision strategy defined
Stop conditions: license unresolved; full-text rights asserted without evidence
```

```text
P01-T03A — P01-04 split and leakage specification
Status: DOCUMENTATION STAGE ONLY — EXECUTION NOT AUTHORIZED
Prerequisites: P01-03G promotion merged and verified; separate founder authorization
Outputs: `specs/mesc-pilot-01/p01-04/*` specification and policy documents
Acceptance: all eight required documents present; founder policy decisions reflected; no execution claims present
Stop conditions: execution claims introduced; source-data redistribution claims asserted beyond canonical rights record; paths exceed `specs/mesc-pilot-01/p01-04/**`
```

```text
P01-T03B1 — Implement fixture-only deterministic split core

Implementation status:
COMPLETED AND ADOPTED

Execution status:
NOT AUTHORIZED

Reviewed head:
34774a8308818d5c3b4875920be34728ddf18f22

Merge:
2937d735df09851384bfa9a15fb8b1f908c62b6d

Boundary:
Private in-memory synthetic-fixture primitives only.
No public splitter activation and no real partition generation.
```

```text
P01-T03B2 — Define remaining P01-04B tooling entry gate

Documentation status:
COMPLETED AND ADOPTED

Adoption merge:
ce1272235cb48dbacdb18f20e1ae8db695b01328

Implementation status:
NOT AUTHORIZED

Execution status:
NOT AUTHORIZED
```

```text
P01-T03B3 — Ratify P01-04B2 design decisions

Founder authorization:
ISSUED ON 2026-07-24

Canonical adoption:
PENDING MERGE OF THIS DOCUMENTATION PR

Implementation status:
NOT AUTHORIZED

Execution status:
NOT AUTHORIZED

Scope:
FD-B2-1 through FD-B2-8 only.
```

```text
P01-T04 — Acquire PQA-L
Status: PLANNING AUTHORIZED / EXECUTION NOT AUTHORIZED
Prerequisites: P01-03 planning complete; separate acquisition authorization
Outputs: acquisition authorization record; artifact allowlist; storage boundary confirmation; acquisition manifest; downloaded Parquet artifacts
Acceptance: immutable revision; reproducible content hash; fail-closed checks pass
Stop conditions: revision drift; acquisition outside authorized environment; raw content inside Git tracking
```

```text
P01-T05 — Transform records
Status: PLANNING AUTHORIZED / EXECUTION NOT AUTHORIZED
Prerequisites: P01-04 complete; separate transformation authorization
Outputs: transformed PilotPubMedQASourceRecord set; validation report; schema versioning record
Acceptance: deterministic transformation; unique IDs; reproducible hashes; unavailable fields marked not_annotated
Stop conditions: schema revision uncontrolled; full-text contamination; annotation fields fabricated without authorization
```

```text
P01-T06 — Freeze source-document-grouped split
Status: NOT AUTHORIZED
Prerequisites: P01-05 complete
Outputs: frozen split manifest; leakage audit report
Acceptance: deterministic split; leakage findings reported; split hash reproducible
Stop conditions: randomness introduced; leakage suppressed
```

```text
P01-T07 — Run leakage audit
Status: NOT AUTHORIZED
Prerequisites: P01-06 complete
Outputs: leakage audit report; normalization record
Acceptance: exact/normalized/near-duplicate findings reported; cross-split overlap detected
Stop conditions: findings redacted; false negatives accepted
```

```text
P01-T08 — Create reviewed grounding subset protocol
Status: NOT AUTHORIZED
Prerequisites: P01-07 complete
Outputs: manual review protocol; 100-example gold subset; annotation interface
Acceptance: gold subset reviewed; claim-support metrics gated behind gold data
Stop conditions: LLM judge substituted for manual review; insufficient coverage
```

```text
P01-T09 — Implement B0/B1 runner

MESC B0 implementation:
Deterministic execution spine adopted at merge
ce1272235cb48dbacdb18f20e1ae8db695b01328.

MESC B1 model-runner implementation:
Not complete unless separately evidenced and authorized.

Real B0/B1 execution:
Not authorized.

Status: NOT AUTHORIZED
Prerequisites: P01-08 complete
Outputs: deterministic runner; run manifest schema; missing-metric policy
Acceptance: no unauthorized weight access; abstention behavior preserved
Stop conditions: executable without authorization; scientific identity mutated
```

## Nomenclature note

| Name | Workstream | Status |
|---|---|---|
| P01-04B1 | Split-tooling subphase | Adopted |
| MESC B0 | Model-execution spine | Adopted |
| MESC B1 | Model-runner / experiment phase | Not evidenced as completed |
| P01-04B2 | Remaining tooling entry gate | Specification in preparation |

P01-04B1 split-tooling naming and MESC B0/B1 model-experiment naming
refer to different workstreams and are not interchangeable.

```text
P01-T10 — Perform Colab feasibility test
Status: NOT AUTHORIZED
Prerequisites: P01-09 complete
Outputs: feasibility report; memory usage record; fallback decision
Acceptance: fallback explicit; no persistent adapter; no published weights
Stop conditions: OOM/Colab disconnection ignored; unauthorized fallback substitution
```

```text
P01-T11 — Execute B0/B1
Status: NOT AUTHORIZED
Prerequisites: P01-10 complete
Outputs: B0/B1 evaluation reports; Layer 1 metrics; abstention report
Acceptance: Layer 1 metrics deterministic; Layer 2 metrics gated; no clinical/production claims
Stop conditions: execution without authorization; results presented as foundation claim
```

```text
P01-T12 — Authorize QLoRA
Status: NOT AUTHORIZED
Prerequisites: P01-11 complete
Outputs: authorization record; adapter metadata policy; training boundary
Acceptance: explicit authorization recorded; no adapter created without authorization record
Stop conditions: adapter accepted as default artifact; training boundary ignored
```

```text
P01-T13 — Execute B2/B3
Status: NOT AUTHORIZED
Prerequisites: P01-12 complete
Outputs: B2/B3 evaluation reports; adapter manifest; Layer 2 metrics
Acceptance: Layer 2 metrics gated behind gold subset; adapter metadata non-public
Stop conditions: Layer 2 metrics reported without gold subset
```

```text
P01-T14 — Run comparator study
Status: NOT AUTHORIZED
Prerequisites: P01-13 complete
Outputs: comparator result schema; external baseline report; clinical boundary record
Acceptance: clinical use excluded; external baselines recorded only
Stop conditions: clinical specialist used for downstream diagnosis; external baseline treated as production model
```

```text
P01-T15 — Add BGE-M3 retrieval
Status: NOT AUTHORIZED
Prerequisites: P01-14 complete
Outputs: retrieval configuration; evidence coverage metrics; deterministic reranker behavior
Acceptance: retrieval optional; gold-subject gating preserved; deterministic behavior
Stop conditions: retrieval forced into foundation baseline; retrieval evidence treated as gold
```

```text
P01-T16 — Validate Evidence Judge
Status: NOT AUTHORIZED
Prerequisites: P01-15 complete
Outputs: Evidence Judge validation report; SciFact result schema; judge bias log
Acceptance: auxiliary dataset only; PubMedQA gold labels preserved; judge bias documented
Stop conditions: judge replaces manual review; SciFact treated as primary benchmark
```

```text
P01-T17 — Produce research evidence package
Status: NOT AUTHORIZED
Prerequisites: P01-16 complete
Outputs: reproducibility record; paper evidence package; public-facing claims
Acceptance: claims match executed work; reproducibility preserved; clinical and production claims absent
Stop conditions: claims exceed executed phases; full article text outside documented rights
```

---

## Status definitions

- COMPLETED: work executed and verified.
- IN PROGRESS: work started but not verified complete.
- AUTHORIZED: work may begin under explicit authorization.
- NOT AUTHORIZED: work may not begin without explicit authorization.
- BLOCKED: prerequisite unsatisfied or rights/access unresolved.
- DEFERRED: explicit decision to postpone with documented rationale.
