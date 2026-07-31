# MESC Pilot-01 — Tasks

Status: **foundation task registry**
Authorization: Foundation *** execution not authorized
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
FOUNDER RATIFIED ON 2026-07-24

Canonical adoption:
1a9169f7229bb72eba6772448724c54ec71937c5

Adoption PR:
#54

Adopted:
2026-07-25

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

---

## Nomenclature note

| Name | Workstream | Status |
|---|---|---|
| P01-04B1 | Split-tooling subphase | Adopted |
| MESC B0 | Model-execution spine | Adopted |
| MESC B1 | Model-runner / experiment phase | Not evidenced as completed |
| P01-04B2 | Remaining tooling design gate | Design ratified; implementation not authorized except for the separately authorized P01-04B2A increment below; execution not authorized |
| P01-04B2A | Deterministic artifact types and canonical serialization | Contracts ratified; implementation adopted (PR #59); portability remediation executed on Draft PR #61 and now under GOVERNANCE HOLD (four blocking findings, FD-PV-16 correction authority recorded but not active); infrastructure not adopted; execution not authorized; B2A not accepted |

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


```text
P01-T03B4 — P01-04B2A contract authorization gate

Documentation status:
COMPLETED AND ADOPTED

Founder authorization:
FD-B2A-1 THROUGH FD-B2A-8 RATIFIED ON 2026-07-26

Canonical adoption:
5c083a0c5f23d0f9837e7543c444633a68524e67

Adoption PR:
#55

Reviewed PR head:
edc09743a1aa9478c2accbe9debb8fcc5bcbe268

Implementation status:
IMPLEMENTED BUT NOT ACCEPTED
(implementation completed and adopted on canonical main;
this gate did not itself authorize implementation)

Implementation adoption PR:
#59

Canonical implementation merge:
5736b1171f1aa467105d931713f5749fb81acd5b

Final merged PR head:
7307fcf9085d3d15114984731b49d484523f09eb

Execution status:
NOT AUTHORIZED

Acceptance status:
B2A NOT ACCEPTED

Portability status:
WINDOWS AND MACOS EVIDENCE OPEN

Downstream status:
B2B NOT AUTHORIZED

Scope:
FD-B2A-1 through FD-B2A-8, including the FD-B2A-5
non-circular fingerprint clarification and binding N-12 sequencing decision.
```

```text
P01-T03B5 — P01-04B2A cross-platform validation-infrastructure gate

Documentation status:
COMPLETED AND ADOPTED

Founder authorization:
FD-PV-1 THROUGH FD-PV-10 RATIFIED ON 2026-07-27

Reviewed PR head:
c555144b480b2334aeaaab0864cad59efe0a1e46

Canonical adoption:
30f79b183a4fff6a08e30e1e43f5da549ce20c1a

Adoption PR:
#57 — MERGED

Final merged PR head:
b76420913c80bd54fd31e63ccffd5ed43a36a854

Founder-ratified reviewed head:
c555144b480b2334aeaaab0864cad59efe0a1e46

Post-merge verification:
CI 30233225446 SUCCESS;
CODEQL 30233225421 SUCCESS;
OPTIONAL EXTRAS / BACKENDS 30233225422 SUCCESS

Source branch:
docs/mesc-p01-04b2a-portability-gate
DELETED AFTER VERIFIED POST-MERGE CLEANUP

FD-PV-6 numeric limits:
1048576 BYTES COMPRESSED AND 4194304 BYTES EXTRACTED PER ARTIFACT;
6291456 BYTES COMPRESSED AND 25165824 BYTES EXTRACTED ACROSS SIX ARTIFACTS

Infrastructure implementation:
HISTORICAL DRAFT WORK CREATED BEFORE CANONICAL AUTHORIZATION (PR #61);
REMEDIATION AUTHORITY RECORDED 2026-07-30 BY FD-PV-11 THROUGH FD-PV-15 BUT NOT
ACTIVE UNTIL ALL FIVE FD-PV-15 ACTIVATION CONDITIONS ARE SATISFIED;
NOT RETROACTIVELY AUTHORIZED; NOT ADOPTED

Infrastructure adoption:
NOT ACHIEVED

B2A implementation:
ADOPTED THROUGH PR #59
(canonical implementation merge 5736b1171f1aa467105d931713f5749fb81acd5b;
not authorized by this portability gate)

Execution:
NOT AUTHORIZED

Evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

Portability status:
PORTABILITY EVIDENCE NOT PRODUCED;
STANDARD LINUX QUALITY GATES SUCCESSFUL;
WINDOWS AND MACOS PORTABILITY EVIDENCE OPEN

Prerequisite:
P01-T03B4 COMPLETED AND ADOPTED

Downstream status:
B2B NOT AUTHORIZED

Scope:
Design and founder-decision gate for deterministic six-cell
cross-platform golden-vector evidence infrastructure.
```

```text
P01-T03B6 — P01-04B2A portability remediation authorization gate

--- State at the time this entry was recorded (2026-07-30) ---
The block below is a historical snapshot. It was accurate when written and is
NOT the current state. The later chronological facts and the current
controlling state follow it.

Documentation status:
RECORDED — NOT ADOPTED; REMEDIATION AUTHORITY NOT ACTIVE

Founder authorization:
FD-PV-11 THROUGH FD-PV-15 RECORDED ON 2026-07-30

Required canonical baseline:
f71c6abf2b2f905f605951605efd6c8ab016523e

Affected Draft pull request:
PR #61 — OPEN / DRAFT / NOT MERGED

Exact reviewed head:
8e484739ba72f4a3be357bd5934b305fd9e7cf41

Exact reviewed tree:
a6bfb21cb2bfa34964ce68190e53f5f809661002

Accepted determination:
AUTHORITY GAP — PR #61 MUST REMAIN DRAFT UNTIL MISSING DECISIONS ARE CANONICALIZED

Historical initial implementation:
OCCURRED BEFORE CANONICAL AUTHORIZATION; NOT RETROACTIVELY AUTHORIZED

Current remediation authority:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-15 ACTIVATION CONDITIONS ARE SATISFIED

Independent clean-room review of pre-remediation exact head:
COMPLETED — AUTHORITY GAP VERDICT ACCEPTED

Independent clean-room review of b9c523138917e22c31d31ded857aeecb8aef55e4:
COMPLETED — CHANGES REQUIRED

Independent clean-room review of a78ccf4dff2c6dc1df8b76ea9cb9ff395b001e53:
COMPLETED — CHANGES REQUIRED

Post-correction independent exact-head review:
OUTSTANDING — REQUIRED BEFORE PR #62 READY OR MERGE

Post-remediation independent exact-head review of PR #61:
OUTSTANDING — REQUIRED BEFORE PR #61 READY OR MERGE

Infrastructure adoption:
NOT ACHIEVED

Execution:
NOT AUTHORIZED

Admissible evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

Downstream status:
B2B NOT AUTHORIZED

Prerequisite:
P01-T03B5 COMPLETED AND ADOPTED

Scope:
Canonicalize the missing portability implementation decisions, preserve the
historical record that PR #61 predates authorization, and authorize a bounded
remediation sequence prospectively: one non-force synchronization merge commit
plus exactly two additive correction commits — three commits in the activated
remediation sequence. The synchronization merge commit is synchronization only
and is not a correction commit; exactly two correction commits, Correction A
then Correction B, are authorized, and no third correction commit is authorized.

--- Later chronological facts (superseding the snapshot above) ---

Governance authorization package:
ADOPTED ON CANONICAL MAIN — PR #62 merged as
3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9 (main tree
f8c80688c1a31ef06cedad4ce44cc13546a92919)

FD-PV-15:
ACTIVATED — all five activation conditions satisfied and mechanically verified

PR #61 remediation:
EXECUTED — one non-force synchronization merge commit plus Correction A and
Correction B, followed by two separately authorized additional commits

Independent clean-room exact-head review of PR #61:
COMPLETED

Accepted verdict:
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT

Resolution pull request:
PR #63 OPENED — see P01-T03B7

--- Current controlling state ---

P01-T03B6 documentation:
ADOPTED ON CANONICAL MAIN

FD-PV-11 through FD-PV-15:
ADOPTED AND CONTROLLING

PR #61:
OPEN / DRAFT / NOT MERGED — HELD by the four blocking findings recorded in
P01-T03B7. NOT accepted, NOT Ready, NOT merged, NOT adopted.

PR #63:
OPEN / DRAFT / NOT MERGED — not adopted

--- Future gated authority ---

FD-PV-16:
RECORDED BUT NOT ACTIVE — see P01-T03B7
```

```text
P01-T03B7 — P01-04B2A portability governance-hold resolution gate

Documentation status:
RECORDED — NOT ADOPTED; FD-PV-16 NOT ACTIVE

Founder disposition:
AUTHORITY-RECORD GAP ACKNOWLEDGED, NOT RETROACTIVELY CURED (2026-07-31)

Required canonical baseline:
3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9

Governed Draft pull request:
PR #61 — OPEN / DRAFT / NOT MERGED — HELD

PR #61 exact head:
2260fa540c440ce3584535f30e74323381568b98

PR #61 exact tree:
eb5cd1757f89bca2b42e1e9c61d3fcd1270a5e94

Accepted independent exact-head verdict:
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT

Blocking findings:
B1 MISSING RECOVERABLE AUTHORIZATION FOR COMMITS 6 AND 7
B2 EXPIRED UNEXPECTED SEVENTH ARTIFACT IS ACCEPTED
B3 WORKFLOW FAILURES BYPASS THE RATIFIED TAXONOMY
B4 CORRECTION B TEST-QUALITY REQUIREMENTS REMAIN UNSATISFIED

Non-blocking findings:
N1 CONSUMER-FAILURE TEST DOES NOT EXERCISE BROKEN-PIPE BEHAVIOUR
N2 ACCIDENTAL CANONICAL-MAIN INCIDENT REQUIRES A DURABLE GOVERNANCE RECORD

Canonical-main incident d2c5ecc96b093613bc9b5863720715dba6395227:
CONTAINED TECHNICALLY; NON-FAST-FORWARD REWIND RECORDED;
NOT AN ANCESTOR OF MAIN OR PR #61; NOT A PR #61 IMPLEMENTATION BLOCKER

Preventive controls:
DIRECT MAIN MUTATION AND FORCE UPDATE PROHIBITED DURING GOVERNED WORK;
PR BODIES VIA THE PULL-REQUEST METADATA ENDPOINT ONLY;
BRANCH PROTECTION RECOMMENDED AS A SEPARATE OPERATIONAL ACTION

Prospective correction authority:
FD-PV-16 RECORDED BUT NOT ACTIVE — ONE ADDITIVE PR #61 COMMIT, PARENT
2260fa540c440ce3584535f30e74323381568b98

Two primary authorized paths:
.github/workflows/mesc-b2a-portability.yml
tests/test_mesc_b2a_portability.py

Conditional helper path:
tests/_mesc_b2a_portability.py

The helper may change only upon strictly proven necessity under FD-PV-16, with
that necessity explicitly recorded. This clarification does not broaden
authority.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Independent exact-head review of the corrected PR #61 head:
OUTSTANDING — REQUIRED BEFORE PR #61 READY OR MERGE

Infrastructure adoption:
NOT ACHIEVED

Execution:
NOT AUTHORIZED

Admissible evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

Binding N-12:
UNDISCHARGED; WINDOWS AND MACOS OBLIGATIONS OPEN

Downstream status:
B2B NOT AUTHORIZED

Prerequisite:
P01-T03B6 RECORDED AND ADOPTED (PR #62 merge 3a0fd67c...)

Scope:
Dispose of the historical authority-record gap for PR #61 commits 6 and 7,
record the accidental canonical-main ref incident and its containment, adopt
preventive controls, and prospectively authorize exactly one additive PR #61
correction commit under a five-condition activation gate.
```
