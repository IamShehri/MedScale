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
| P01-04B | Split-tooling and contract implementation phase | Completed, adopted and founder-accepted on canonical main `d5a6ac1654cabd33b6a795756d2796bceaf1652a` (PR #83, 2026-08-04); all ten acceptance criteria SATISFIED; tooling acceptance only; real execution not authorized; P01-04C not authorized |
| MESC B0 | Model-execution spine | Adopted |
| MESC B1 | Model-runner / experiment phase | Not evidenced as completed |
| P01-04B2 | Remaining tooling design gate | Design ratified; every authorized increment (B2A, B2B, B2C, B2D), the minimum-deviation correction and the atomic publication boundary implemented, adopted and accepted; execution not authorized |
| P01-04B2A | Deterministic artifact types and canonical serialization | Contracts ratified; implementation adopted (PR #59); portability validation infrastructure adopted on canonical main (PR #61 merge `69f16455...`); evidence-production authority adopted on canonical main (PR #65 merge `e3478da9...`); FD-PV-17 and FD-PV-18 activated and consumed; canonical portability evidence produced by run 30678040133, mechanically verified, and independently reviewed APPROVE WITH NON-BLOCKING NOTES; founder evidence-acceptance decision FD-PV-19 adopted on canonical main (PR #66 merge `1f2d9152...`); founder implementation-acceptance decision FD-B2A-9 issued but not yet adopted on canonical main, with the N-12 discharge and the Windows and macOS closure decisions likewise issued but not yet canonical; execution not authorized; B2A founder-accepted in substance but not yet canonically adopted; B2B not authorized |

P01-04B1 split-tooling naming and MESC B0/B1 model-experiment naming
refer to different workstreams and are not interchangeable.

The per-increment status text in the P01-04B2A row above is a historical
snapshot of that increment's governance position at the time it was written and
is preserved unrewritten. For current status of every P01-04B increment, the
final Current controlling state block in this file controls.

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

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B6 was adopted. It is retained as
historical governance evidence and is not the repository's present controlling
state. The later P01-T03B8 Current controlling state supersedes this block;
P01-T03B9 governs the subsequent FD-PV-18 evidence-production gate.

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

```text
P01-T03B8 — P01-04B2A final independent-review hold gate

--- State at the time this entry was recorded (2026-07-31) ---
The block below is a historical snapshot. It was accurate when written and is
NOT the current state. The later chronological facts and the current
controlling state follow it.

Documentation status:
RECORDED — NOT ADOPTED; FD-PV-17 NOT ACTIVE

Founder disposition:
FINAL REVIEW HOLD ACCEPTED (2026-07-31)

Required canonical baseline:
02d0aafb61fa62de414c0e8e5d61187c03b650bd

Governed Draft pull request:
PR #61 — OPEN / DRAFT / NOT MERGED — HELD

PR #61 exact head:
f68f8be8799c0ec67b26c319a4a06789f2ea1a7e

PR #61 exact tree:
1caa8f9ae4031ff17ddcd33ffc0a32a4e7cc855e

PR #61 scope:
8 COMMITS / 3 FILES / +3829 / -0

Accepted independent exact-head verdict:
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT

Blocking findings:
F1 LARGE UNEXPECTED-ARTIFACT RESPONSES MAY BYPASS THE GUARD THROUGH A
   PIPEFAIL/SIGPIPE PIPELINE RESULT
F2 B2 TESTS BYPASS THE REAL PAGINATED-JSON AND JQ PROJECTION BOUNDARY
F3 DISPATCH TESTS COVER ONE GUARD COPY AND DO NOT PROVE MALFORMED-SHA
   REJECTION PRECEDES GIT REV-PARSE
F4 ARCHIVE-CARDINALITY BEHAVIOUR LACKS REAL EXECUTION COVERAGE

Accepted taxonomy mappings — settled, not to be changed:
EXPIRED EXPECTED ARTIFACT -> missing_matrix_cell
POST-VALIDATION ARCHIVE-COUNT INCONSISTENCY ->
  aggregate_verifier_internal_error

Prospective correction authority:
FD-PV-17 RECORDED BUT NOT ACTIVE — ONE ADDITIVE NINTH PR #61 COMMIT, PARENT
f68f8be8799c0ec67b26c319a4a06789f2ea1a7e

Two primary authorized paths:
.github/workflows/mesc-b2a-portability.yml
tests/test_mesc_b2a_portability.py

Conditional helper path:
tests/_mesc_b2a_portability.py

The helper may change only if the builder proves a blocking defect cannot be
closed without it, with that proof recorded. No tenth commit is authorized.

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
P01-T03B7 ADOPTED (PR #63 merge 02d0aafb...)

Scope:
Record the final independent exact-head review verdict on PR #61 and
prospectively authorize exactly one ninth correction commit under a
five-condition activation gate. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2a-governance-hold/ and is not restated.

--- Later chronological facts (superseding the snapshot above) ---

Governance authorization package:
ADOPTED ON CANONICAL MAIN — PR #64 merged as
63c6e3200c4b8013ec068630a29118df0dfc7a6f (ordered parents
02d0aafb61fa62de414c0e8e5d61187c03b650bd and
0d28c4599f91afb40778226344bb6b3bede56f52; main tree
95d2c59b8e536df2702987440ae524cf4e4e6352)

FD-PV-17:
ACTIVATED — all five activation conditions satisfied and mechanically verified

Commit 9:
CREATED, REVIEWED, AND ADOPTED — 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae,
parent f68f8be8799c0ec67b26c319a4a06789f2ea1a7e, tree
802fe54f976a8c89baffcaf87c99a62cb53250b4, additive and single-parent

Commit 10:
NOT AUTHORIZED / NOT CREATED

FD-PV-17:
CONSUMED

F1 through F4:
CLOSED — verified by an independent clean-room exact-head review

Independent clean-room exact-head review of 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae:
COMPLETED

Accepted verdict:
APPROVE WITH NON-BLOCKING NOTES — EXACT HEAD ELIGIBLE FOR A SEPARATE FOUNDER
READY DECISION
(no blocking findings; nine non-blocking notes, none authorizing a tenth commit)

Founder Ready decision:
EXERCISED — PR #61 transitioned from Draft to Ready

Founder merge decision:
EXERCISED — PR #61 merged 2026-07-31T22:00:34Z

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B8 was adopted. It is retained as
historical governance evidence and is not the repository's present controlling
state. The later P01-T03B9 Current controlling state supersedes this block;
P01-T03B10 governs the subsequent FD-PV-19 evidence-acceptance disposition.

P01-T03B8 documentation:
ADOPTED ON CANONICAL MAIN

FD-PV-17:
ADOPTED, ACTIVATED AND CONSUMED

PR #61:
MERGED AS 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3
(merged head 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae; merge tree
ebbb61b905bde4773d48b40b9f667ceb0d558566; ordered parents
63c6e3200c4b8013ec068630a29118df0dfc7a6f and
7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae; 9 commits; 3 files; +4411 / -0)

Infrastructure adoption:
ACHIEVED ON CANONICAL MAIN

Admissible evidence production:
NOT YET AUTHORIZED — FD-PV-18 RECORDED BUT NOT ACTIVE

Admissible evidence:
NOT PRODUCED

B2A acceptance:
NOT ACHIEVED

N-12:
BINDING AND UNDISCHARGED

Windows/macOS obligations:
OPEN

B2B:
NOT AUTHORIZED

Real split, B0, training, and fine-tuning:
NOT AUTHORIZED

--- Future gated authority ---

FD-PV-18:
RECORDED BUT NOT ACTIVE — see P01-T03B9
```

```text
P01-T03B9 — P01-04B2A canonical portability evidence-production authorization gate

Documentation status:
RECORDED — NOT ADOPTED; FD-PV-18 NOT ACTIVE

Founder disposition:
EVIDENCE-PRODUCTION AUTHORIZATION GATE OPENED (2026-08-01)

Required canonical baseline:
69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3

Adopted infrastructure:
PR #61 — MERGED AS 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3

PR #61 merged head:
7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae

PR #61 merge tree:
ebbb61b905bde4773d48b40b9f667ceb0d558566

PR #61 ordered merge parents:
63c6e3200c4b8013ec068630a29118df0dfc7a6f
7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae

PR #61 merged at:
2026-07-31T22:00:34Z

PR #61 first-parent delta:
3 FILES / +4411 / -0 — .github/workflows/mesc-b2a-portability.yml,
tests/_mesc_b2a_portability.py, tests/test_mesc_b2a_portability.py

Accepted independent exact-head verdict:
APPROVE WITH NON-BLOCKING NOTES — EXACT HEAD ELIGIBLE FOR A SEPARATE FOUNDER
READY DECISION

Blocking findings:
NONE

Non-blocking notes:
NINE — NONE AUTHORIZES OR REQUIRES A TENTH COMMIT

Infrastructure adoption:
ACHIEVED ON CANONICAL MAIN

FD-PV-17:
ACTIVATED AND CONSUMED

Commit 9:
CREATED, REVIEWED, AND ADOPTED

Commit 10:
NOT AUTHORIZED / NOT CREATED

Post-merge automatic runs at 69f16455...:
CI 30668524206 SUCCESS;
CODEQL 30668524193 SUCCESS;
OPTIONAL EXTRAS / BACKENDS 30668524166 SUCCESS
(all event: push, all run_attempt: 1)

MESC B2A Portability post-merge run:
NONE — EXPECTED, NOT A FAILURE. The workflow declares only pull_request and
workflow_dispatch triggers, so a merge push cannot trigger it.

MESC B2A Portability run history:
7 RUNS, ALL event: pull_request, ALL run_attempt: 1;
0 workflow_dispatch RUNS; 0 MANUAL RERUNS

Existing portability artifacts:
NON-ADMISSIBLE PULL-REQUEST INFRASTRUCTURE VALIDATION ONLY;
0 b2a-portability-evidence ARTIFACTS EXIST REPOSITORY-WIDE

Accepted taxonomy mappings — settled, not to be changed:
EXPIRED EXPECTED ARTIFACT -> missing_matrix_cell
POST-VALIDATION ARCHIVE-COUNT INCONSISTENCY ->
  aggregate_verifier_internal_error

Taxonomy:
EXACTLY TWENTY-ONE CATEGORIES — UNCHANGED

Prospective evidence-production authority:
FD-PV-18 RECORDED BUT NOT ACTIVE — EXACTLY ONE workflow_dispatch ATTEMPT
AGAINST .github/workflows/mesc-b2a-portability.yml ON REF main

Required dispatch input:
expected_sha = THE MECHANICALLY VERIFIED CANONICAL-MAIN SHA PRODUCED BY MERGING
THIS PACKAGE. NOT 69f16455... — THAT SHA PREDATES THIS PACKAGE'S MERGE.

Authority consumption:
CONSUMED WHEN GITHUB ACCEPTS THE DISPATCH REQUEST, REGARDLESS OF OUTCOME.
NO RETRY, RERUN, SECOND DISPATCH, OR REPLACEMENT RUN IS AUTHORIZED.

Authorized inspection:
READ-ONLY INSPECTION OF THAT ONE RUN AND OFFLINE VERIFICATION OF ITS SEVEN
ARTIFACTS — SIX CELL ARTIFACTS PLUS b2a-portability-evidence

First independent exact-head review of 617c632f4c67628c9b3fa165aa6712f7b3698079:
COMPLETED — REPORT RETURNED APPROVE WITH NON-BLOCKING NOTES

Founder disposition of that report:
CHANGES REQUIRED — THE CONTRADICTORY CURRENT-CONTROLLING-STATE HEADINGS WERE
RECLASSIFIED AS BLOCKING

Independent exact-head review of the corrected head:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Independent evidence review of the future run:
OUTSTANDING — REQUIRED BEFORE ANY EVIDENCE ACCEPTANCE

Admissible evidence production:
NOT YET AUTHORIZED

Admissible evidence:
NOT PRODUCED

B2A acceptance:
NOT ACHIEVED

Binding N-12:
UNDISCHARGED; WINDOWS AND MACOS OBLIGATIONS OPEN

Downstream status:
B2B NOT AUTHORIZED

Real split, B0, training, and fine-tuning:
NOT AUTHORIZED

Prerequisite:
P01-T03B8 ADOPTED (PR #64 merge 63c6e320...) AND PR #61 ADOPTED
(merge 69f16455...)

Scope:
Record the verified post-merge truth of PR #61 and prospectively authorize
exactly one canonical-main portability evidence-production workflow dispatch
under a five-condition activation gate. Successful evidence production does not
itself accept B2A. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2a-governance-hold/ and
specs/mesc-pilot-01/p01-04b2a-final-review-hold/ and is not restated.

--- Later chronological facts (superseding the entry above) ---

Independent exact-head review of the corrected head:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES; NO BLOCKING FINDINGS

Governance authorization package:
ADOPTED ON CANONICAL MAIN — PR #65 merged as
e3478da94e62ad9af5858a69e28de7e5d5fc04f4 (ordered parents
69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3 and
626a23f01db978d43d51cdbae2c4378d2cf1733f; main tree
e64e57a1c6c94703a7f20ef6598256fa77600b31; merged 2026-08-01T01:19:29Z;
2 commits; 5 files; +909 / -1)

FD-PV-18:
ACTIVATED — all five activation conditions satisfied and mechanically verified

Authorized dispatch:
ACCEPTED — EXACTLY ONE, 2026-08-01T01:30:04Z

FD-PV-18:
CONSUMED

Evidence run:
30678040133 — run number 8, event workflow_dispatch, run_attempt 1,
head_branch main, head_sha e3478da94e62ad9af5858a69e28de7e5d5fc04f4,
actor IamShehri, COMPLETED / SUCCESS

MESC B2A Portability run history:
8 RUNS — 7 event: pull_request, 1 event: workflow_dispatch;
0 RUNS WITH run_attempt > 1

Job topology:
SIX GENERATION JOBS AND ONE AGGREGATE JOB — ALL SUCCESS;
PULL-REQUEST AGGREGATION SKIPPED; DISPATCH AGGREGATION EXECUTED;
EVIDENCE UPLOAD EXECUTED EXACTLY ONCE

Artifacts:
SEVEN — SIX CELL ARTIFACTS PLUS b2a-portability-evidence;
0 DUPLICATE, 0 MISSING, 0 UNEXPECTED, 0 EXPIRED AT INSPECTION AND AT REVIEW

Mechanical evidence verification:
PASSED — CROSS-CELL BYTE IDENTITY ACROSS ALL SIX CELLS;
NB3-A, NB3-B AND NB3-C PASS; CONTENT BOUNDARY PASS

Independent evidence review of the run:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES; NO BLOCKING FINDINGS

Retry, rerun, second dispatch, replacement run:
NOT AUTHORIZED — NONE OCCURRED

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B9 was adopted. It is retained as
historical governance evidence and is not the repository's present controlling
state. The later P01-T03B10 Current controlling state supersedes this block;
P01-T03B11 governs the subsequent FD-B2A-9 implementation-acceptance
disposition.

P01-T03B9 documentation:
ADOPTED ON CANONICAL MAIN

FD-PV-18:
ADOPTED, ACTIVATED AND CONSUMED

PR #65:
MERGED AS e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Admissible evidence:
PRODUCED AND MECHANICALLY VERIFIED AT
e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Founder evidence-acceptance decision:
ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B10

B2A acceptance:
NOT ACHIEVED

N-12:
BINDING AND UNDISCHARGED

Windows/macOS obligations:
OPEN

B2B:
NOT AUTHORIZED

Real split, B0, model access, training, and fine-tuning:
NOT AUTHORIZED

--- Future gated authority ---

FD-PV-19:
RECORDED BUT NOT YET ADOPTED — see P01-T03B10
```

```text
P01-T03B10 — Record the P01-04B2A canonical portability evidence-acceptance decision

Documentation status:
RECORDED — NOT ADOPTED; FD-PV-19 NOT YET ADOPTED ON CANONICAL MAIN

Founder disposition:
CANONICAL PORTABILITY EVIDENCE ACCEPTED (2026-08-01)

Required canonical baseline:
e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Adopted authorization:
PR #65 — MERGED AS e3478da94e62ad9af5858a69e28de7e5d5fc04f4
(merged head 626a23f01db978d43d51cdbae2c4378d2cf1733f; merge tree
e64e57a1c6c94703a7f20ef6598256fa77600b31; ordered parents
69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3 and
626a23f01db978d43d51cdbae2c4378d2cf1733f; merged 2026-08-01T01:19:29Z;
2 commits; 5 files; +909 / -1)

FD-PV-18:
ACTIVATED AND CONSUMED

Authorized dispatch requests:
EXACTLY ONE — ACCEPTED

Retry, rerun, second dispatch, replacement run:
NOT AUTHORIZED

Evidence run:
30678040133 — COMPLETED / SUCCESS
(run number 8; event workflow_dispatch; run_attempt 1; head_branch main;
head_sha e3478da94e62ad9af5858a69e28de7e5d5fc04f4; actor IamShehri;
created 2026-08-01T01:30:04Z)

MESC B2A Portability run history:
8 RUNS — 7 pull_request, 1 workflow_dispatch; 0 RUNS WITH run_attempt > 1

Job topology:
SIX GENERATION JOBS AND ONE AGGREGATE JOB — ALL SUCCESS

Artifacts:
SEVEN — 0 DUPLICATE, 0 MISSING, 0 UNEXPECTED, 0 EXPIRED AT INSPECTION AND
AT REVIEW; ALL BOUND TO RUN 30678040133

Accepted payload identities:
canonical.json 228 BYTES; canonical.jsonl 79 BYTES; manifest.json 308 BYTES —
BYTE-IDENTICAL ACROSS ALL SIX CELLS

Schemas:
MANIFEST mesc-pilot-01-b2a-portability-manifest/1;
EVIDENCE mesc-pilot-01-b2a-portability-evidence/1;
EVIDENCE result: pass;
EVIDENCE canonical_sha e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Mechanical evidence verification:
PASSED — NB3-A PASS; NB3-B PASS; NB3-C PASS; CONTENT BOUNDARY PASS

Independent evidence review:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES

Blocking findings:
NONE

Accepted non-blocking observations:
NB-01 ZIP UNIX PERMISSION METADATA DIFFERS BY PRODUCER (0644 LINUX/MACOS,
0666 WINDOWS) — ARCHIVE METADATA ONLY;
NB-02 BROAD SUBSTRING SCANS PRODUCED FALSE POSITIVES FROM "decomposed" AND
"windows-py3.11" — METHODOLOGY OBSERVATION ONLY.
NEITHER REQUIRES AN EVIDENCE CORRECTION, NEW RUN, RERUN, REPLACEMENT
ARTIFACT, OR IMPLEMENTATION CHANGE.

Founder evidence-acceptance decision:
ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

FD-PV-19:
RECORDED BUT NOT YET ADOPTED

Adoption conditions:
ALL FIVE REQUIRED — INDEPENDENT EXACT-HEAD PACKAGE REVIEW, SEPARATE FOUNDER
READY DECISION, SEPARATE FOUNDER MERGE DECISION, MERGE INTO CANONICAL MAIN,
AND MECHANICAL POST-MERGE VERIFICATION. NO SUBSET ADOPTS FD-PV-19.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Canonical portability evidence:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED UNTIL THIS PACKAGE IS MERGED AND VERIFIED

B2A acceptance:
NOT ACHIEVED

Binding N-12:
UNDISCHARGED; WINDOWS AND MACOS OBLIGATIONS OPEN

Downstream status:
B2B NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split, B0, model access, real dataset access, inference, retrieval,
training, and fine-tuning:
NOT AUTHORIZED

Prerequisite:
P01-T03B9 ADOPTED (PR #65 merge e3478da9...) AND FD-PV-18 CONSUMED

Scope:
Record the founder's acceptance of the canonical portability evidence produced
by the single FD-PV-18-authorized dispatch, together with the immutable run,
artifact, payload and review facts supporting it. Evidence acceptance is not
B2A acceptance. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2a-governance-hold/,
specs/mesc-pilot-01/p01-04b2a-final-review-hold/ and
specs/mesc-pilot-01/p01-04b2a-evidence-production-gate/ and is not restated.

--- Later chronological facts (superseding the entry above) ---

Independent exact-head review of bf26351ff84c7ed6d30f0ad054109309af64b04b:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES; NO BLOCKING FINDINGS;
THREE ACCEPTED NON-BLOCKING NOTES, NONE REQUIRING A SECOND COMMIT

Founder Ready decision:
EXERCISED — PR #66 transitioned from Draft to Ready

Founder merge decision:
EXERCISED — PR #66 merged 2026-08-01T02:37:09Z

Governance package:
ADOPTED ON CANONICAL MAIN — PR #66 merged as
1f2d9152281f3136d212dcf7729063f7b1c64ad1 (ordered parents
e3478da94e62ad9af5858a69e28de7e5d5fc04f4 and
bf26351ff84c7ed6d30f0ad054109309af64b04b; main tree
83de598c69c5ab963f400f9f69d1d0b2a3b0ac81; 1 commit; 5 files; +1056 / -1)

Mechanical post-merge verification:
PASSED — REVIEWED HEAD TO FINAL MERGE ZERO FILE DELTA;
SYNTHETIC MERGE a1e248e9b1c905c00f7e84c78835fc6926bc3e34 TO FINAL MERGE
ZERO FILE DELTA; FIRST-PARENT SCOPE EXACTLY FIVE PATHS

Automatic post-merge runs at 1f2d9152...:
CI 30680367441 SUCCESS;
CODEQL 30680367434 SUCCESS;
OPTIONAL EXTRAS / BACKENDS 30680367448 SUCCESS
(all event: push, all run_attempt: 1)

MESC B2A Portability post-merge run:
NONE — EXPECTED, NOT A FAILURE. The workflow declares only pull_request and
workflow_dispatch triggers, so a merge push cannot trigger it.

MESC B2A Portability run history:
8 RUNS — 7 pull_request, 1 workflow_dispatch; 0 RUNS WITH run_attempt > 1;
RUN 30678040133 REMAINS THE SOLE workflow_dispatch

FD-PV-18:
REMAINS CONSUMED — NOT REVIVED

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B10 was adopted. It is retained as
historical governance evidence and is not the repository's present controlling
state. The later P01-T03B13 Current controlling state supersedes this block;
P01-T03B11 records the intervening FD-B2A-9 implementation-acceptance
disposition and P01-T03B12 the FD-B2B-1 through FD-B2B-10 authorization.

P01-T03B10 documentation:
ADOPTED ON CANONICAL MAIN

PR #66:
MERGED AND MECHANICALLY VERIFIED

FD-PV-19:
ADOPTED ON CANONICAL MAIN AT
1f2d9152281f3136d212dcf7729063f7b1c64ad1

Canonical portability evidence:
FOUNDER-ACCEPTED AND CANONICALLY ADOPTED

FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B11

P01-04B2A:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

N-12:
FOUNDER DISCHARGE DECISION ISSUED;
CANONICALLY BINDING UNTIL THAT PACKAGE IS ADOPTED

Windows/macOS portability obligations:
FOUNDER CLOSURE DECISIONS ISSUED;
CANONICALLY OPEN UNTIL THAT PACKAGE IS ADOPTED

P01-04B:
INCOMPLETE / NOT ACCEPTED

B2B:
NOT AUTHORIZED

Real split, B0, B1, model access, real dataset access, inference, retrieval,
metrics, benchmark execution, training, and fine-tuning:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2A-9:
RECORDED BUT NOT YET ADOPTED — see P01-T03B11
```

```text
P01-T03B11 — Record P01-04B2A implementation acceptance, N-12 discharge and
platform-obligation closure

Documentation status:
RECORDED — NOT ADOPTED; FD-B2A-9 NOT YET ADOPTED ON CANONICAL MAIN

Founder disposition:
P01-04B2A IMPLEMENTATION ACCEPTED (2026-08-01)

Required canonical baseline:
1f2d9152281f3136d212dcf7729063f7b1c64ad1

Adopted predecessor:
PR #66 — MERGED AS 1f2d9152281f3136d212dcf7729063f7b1c64ad1
(merged head bf26351ff84c7ed6d30f0ad054109309af64b04b; merge tree
83de598c69c5ab963f400f9f69d1d0b2a3b0ac81; merged 2026-08-01T02:37:09Z;
1 commit; 5 files; +1056 / -1)

FD-PV-19:
ADOPTED ON CANONICAL MAIN AT
1f2d9152281f3136d212dcf7729063f7b1c64ad1

Contract authority:
PR #55 — MERGE 5c083a0c5f23d0f9837e7543c444633a68524e67;
FOUNDER-RATIFICATION HEAD edc09743a1aa9478c2accbe9debb8fcc5bcbe268;
FD-B2A-1 THROUGH FD-B2A-8 RATIFIED 2026-07-26;
FD-B2A-5 INCLUDES THE PD-B2A-5.1 NON-CIRCULAR FINGERPRINT CLARIFICATION

Accepted implementation:
PR #59 — MERGE 5736b1171f1aa467105d931713f5749fb81acd5b;
MERGED HEAD 7307fcf9085d3d15114984731b49d484523f09eb;
REVIEWED TREE 575fcf124792cd38b546a58a6845ad2ecd317281;
2 COMMITS / 4 FILES / +2559 / -0

Accepted implementation scope:
src/medscale/mesc/_canonical_json_v1.py;
src/medscale/mesc/_split_artifacts_v1.py;
tests/test_mesc_canonical_json_v1.py;
tests/test_mesc_split_artifacts_v1.py

Accepted implementation observations:
IMPLEMENTATION NB-01 UNTYPED StopIteration ON A DELIBERATELY MALFORMED
LOW-LEVEL OBJECT — NON-BLOCKING, NOT CORRECTED;
IMPLEMENTATION NB-02 PRIMITIVE SUBCLASSES ACCEPTED BEFORE THE CANONICAL
SERIALIZATION BOUNDARY REJECTS THEM — NON-BLOCKING, NOT CORRECTED.
NEITHER IS UPGRADED INTO ACCEPTED PUBLIC BEHAVIOUR.

Portability infrastructure:
PR #61 — MERGE 69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3;
REVIEWED HEAD 7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae;
INDEPENDENTLY REVIEWED AND ADOPTED BEFORE FD-PV-18 ACTIVATION;
SIX MATRIX CELLS PRESERVED; EVIDENCE-ONLY; UNMODIFIED AND NOT RERUN

Accepted evidence:
RUN 30678040133 — RUN NUMBER 8; EVENT workflow_dispatch; run_attempt 1;
head_branch main; EVIDENCE CANONICAL SHA
e3478da94e62ad9af5858a69e28de7e5d5fc04f4; COMPLETED / SUCCESS;
6 GENERATION JOBS AND 1 AGGREGATE JOB ALL SUCCESS;
7 ARTIFACTS, 0 DUPLICATE, 0 MISSING, 0 UNEXPECTED, 0 EXPIRED

Accepted payload identities:
canonical.json 228 BYTES; canonical.jsonl 79 BYTES; manifest.json 308 BYTES —
BYTE-IDENTICAL AND HASH-IDENTICAL ACROSS ALL SIX CELLS

Independent evidence review:
COMPLETED — APPROVE WITH NON-BLOCKING NOTES; BLOCKING FINDINGS NONE;
EVIDENCE NB-01 ZIP UNIX PERMISSION METADATA AND EVIDENCE NB-02 SUBSTRING-SCAN
FALSE POSITIVES BOTH ACCEPTED AS NON-BLOCKING

N-12 requirement mapping:
LINUX SATISFIED; WINDOWS SATISFIED; MACOS SATISFIED; PYTHON 3.11 SATISFIED;
PYTHON 3.12 SATISFIED; CROSS-CELL BYTE AND HASH EQUALITY SATISFIED;
INDEPENDENT EVIDENCE REVIEW SATISFIED; FOUNDER EVIDENCE ACCEPTANCE AND
CANONICAL ADOPTION SATISFIED

Founder decision:
FD-B2A-9 — P01-04B2A IMPLEMENTATION ACCEPTANCE DISPOSITION;
DECISION: ACCEPT P01-04B2A IMPLEMENTATION;
N-12 SATISFIED AND DISCHARGED FOR P01-04B2A;
WINDOWS PORTABILITY OBLIGATION SATISFIED AND CLOSED FOR P01-04B2A;
MACOS PORTABILITY OBLIGATION SATISFIED AND CLOSED FOR P01-04B2A

FD-B2A-9:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2A acceptance:
FOUNDER-ACCEPTED IN SUBSTANCE; NOT YET CANONICALLY ADOPTED

N-12:
FOUNDER DISCHARGE DECISION ISSUED;
CANONICALLY BINDING UNTIL THIS PACKAGE IS ADOPTED

Windows/macOS portability obligations:
FOUNDER CLOSURE DECISIONS ISSUED;
CANONICALLY OPEN UNTIL THIS PACKAGE IS ADOPTED

Adoption conditions:
ALL FIVE REQUIRED — INDEPENDENT EXACT-HEAD PACKAGE REVIEW, SEPARATE FOUNDER
READY DECISION, SEPARATE FOUNDER MERGE DECISION, MERGE INTO CANONICAL MAIN,
AND MECHANICAL POST-MERGE VERIFICATION. NO SUBSET ADOPTS FD-B2A-9.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

P01-04B:
INCOMPLETE / NOT ACCEPTED

B2B:
NOT AUTHORIZED

B2C, B2D, and P01-04C through P01-04G:
NOT AUTHORIZED

Real Pilot-01 split, P01-03G or real dataset access, B0/B1 execution, model
access, inference, retrieval, metrics or benchmark execution, training,
fine-tuning, publication, and clinical use:
NOT AUTHORIZED

Prerequisite:
P01-T03B10 ADOPTED (PR #66 merge 1f2d9152...) AND FD-PV-19 ADOPTED

Scope:
Record the founder's acceptance of the P01-04B2A implementation, the discharge
of the binding N-12 sequencing obligation for P01-04B2A, and the closure of the
Windows and macOS portability obligations for P01-04B2A, together with the exact
immutable basis supporting those decisions. B2A acceptance makes a later B2B
authorization decision eligible for consideration and does not itself authorize
B2B. Prior governance history is adopted at specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-governance-hold/,
specs/mesc-pilot-01/p01-04b2a-final-review-hold/,
specs/mesc-pilot-01/p01-04b2a-evidence-production-gate/ and
specs/mesc-pilot-01/p01-04b2a-evidence-acceptance/ and is not restated.
```

```text
P01-T03B12 — Authorize P01-04B2B leakage primitive implementation

Documentation status:
RECORDED ON A NON-CANONICAL DRAFT BRANCH — NOT ADOPTED;
FD-B2B-1 THROUGH FD-B2B-10 NOT ADOPTED ON CANONICAL MAIN

Package revision:
R3 — CLEAN POST-INCIDENT RECONSTRUCTION

Required canonical baseline:
06078180eb7c85da80878f3a86c5fdf3655462c5
(tree 4208ea672a01ac942a1caeee764167d530cc8f1e)

Historical provenance:
PR #68 HEAD a309f0789c48646e36a87181b23673551a23d74d — REVIEWED AND REJECTED
AT ITS EXACT HEAD; NON-CANONICAL; NEVER ADOPTED.
PR #69 HEAD 1c446def4c064b21c2cc60bc894aab3ed8e9ccff — CORRECTED HISTORICAL
PACKAGE; ENTERED MAIN THROUGH THE UNAUTHORIZED DRAFT MERGE
c8e476e42aa7c6f0e433836e278cba8940f0ea26; NEVER VALIDLY REVIEWED OR ADOPTED;
NEITHER SUBSTANTIVELY APPROVED NOR SUBSTANTIVELY REJECTED; MECHANICALLY
CONTAINED THROUGH PR #70.
PR #70 — VALIDLY MERGED AND MECHANICALLY VERIFIED AS
06078180eb7c85da80878f3a86c5fdf3655462c5; RESTORED THE EXACT LAST VALID
CANONICAL TREE.
R3 IS A FRESH RECONSTRUCTION FROM THE PROTECTED CANONICAL MAIN. IT INTRODUCES,
MERGES AND CHERRY-PICKS NO HISTORICAL PACKAGE COMMIT, AND ADDS EXACTLY ONE NEW
SINGLE-PARENT COMMIT ON CANONICAL MAIN WITH FOUR FRESHLY RECONSTRUCTED PACKAGE
BLOBS DISTINCT FROM THE r1 AND r2 BLOBS.
BECAUSE PR #70 PRESERVED RATHER THAN REWROTE INCIDENT HISTORY,
1c446def4c064b21c2cc60bc894aab3ed8e9ccff AND
c8e476e42aa7c6f0e433836e278cba8940f0ea26 REMAIN REACHABLE ANCESTORS OF CANONICAL
MAIN AND THEREFORE OF EVERY BRANCH CREATED FROM IT, INCLUDING R3;
a309f0789c48646e36a87181b23673551a23d74d IS NOT AN ANCESTOR. THAT INHERITED
REACHABILITY IS NOT ADOPTION, APPROVAL, REUSE OR INTRODUCTION BY R3.

Corrections carried forward:
BLOCKING-1 CORRECTED — AUTHORITATIVE CANONICAL score_representation IS A FROZEN
STRING; THE RUNTIME FLOAT IS DERIVED AND EXCLUDED FROM CANONICAL DOCUMENTS,
CANONICAL BYTES, FINGERPRINTS AND FINDING-ID PAYLOAD BYTES; THRESHOLD PASSAGE
USES EXACT INTEGER COMPARISON.
BLOCKING-2 CORRECTED — FINDING_IDENTITY_BYTES IS PINNED TO THE ACCEPTED B2A
CANONICAL SINGLE-OBJECT JSON SERIALIZATION OF AN EXACT SIX-MEMBER IDENTITY
DOCUMENT, INCLUDING THE ACCEPTED TERMINAL LF RULE.

Blocking findings corrected after the independent review of the rejected exact
head 0907b45904e237462fff10f835f15a2dcfa748d6:
B-1 CORRECTED — THE FALSE GRAPH-ANCESTRY CLAIM AND THE IMPOSSIBLE
CLEAN-RECONSTRUCTION ACCEPTANCE CONDITION ARE REPLACED BY CONSTRUCTION-PROVENANCE
LANGUAGE PLUS AN EXPLICIT ACKNOWLEDGEMENT OF INHERITED PR #69 ANCESTRY.
B-2 CORRECTED — token_set_jaccard IS TOTAL; THE UNION-ZERO CASE IS PINNED TO
not_evaluable WITH RUNTIME SCORE null AND NEITHER THRESHOLD PASSED;
jaccard:0/0 IS PROHIBITED AND jaccard:0/1 IS NOT USED FOR THAT CASE.
B-3 CORRECTED — example_ids, source_document_ids AND partitions ARE
UNIQUE-VALUE LISTS; DUPLICATES FAIL CLOSED AND ARE NEVER SILENTLY DEDUPLICATED;
INPUT PERMUTATION IS NON-SEMANTIC AND YIELDS IDENTICAL FINDING_IDENTITY_BYTES.

Blocking finding corrected after the independent review of the superseded exact
head adc01a4ce6919ac7e4de6d915cbe0ffcf6d3cf63:
THAT REVIEW CONFIRMED B-1, B-3 AND THE B-2 UNION-ZERO CORRECTION AS RESOLVED.
BLOCKING-R3-1 CORRECTED — EMPTY-INPUT PRECEDENCE PINNED: EMPTY-INPUT RULES ARE
AUTHORITATIVE EXCEPTIONS EVALUATED BEFORE GENERAL JACCARD FRACTION CONSTRUCTION,
AND A FRACTION IS CONSTRUCTED ONLY WHEN BOTH TOKEN SETS ARE NON-EMPTY;
EXACTLY-ONE-EMPTY REMAINS not_evaluable AS POLICY-DEFINED UNDER SENIOR FD-B2-6
RATHER THAN MATHEMATICALLY UNDEFINED; BOTH-EMPTY REMAINS not_evaluable;
THE ZERO-SCORE GOLDEN VECTOR IS SCOPED TO TWO NON-EMPTY DISJOINT TOKEN SETS WITH
THE LITERAL WITNESS frozenset({"a"}), frozenset({"b"}) -> jaccard:0/1 AND RUNTIME
SCORE 0.0; jaccard:0/1 IS NEVER EMITTED WHEN EITHER TOKEN SET IS EMPTY;
THE EXACTLY-ONE-EMPTY CASE IS NO LONGER CLASSIFIED AS A UNION-ZERO CASE;
REQUIRED TESTS AND ACCEPTANCE CRITERIA ARE MADE MUTUALLY CONSISTENT.

NO PRIOR REVIEW CARRIES FORWARD; THE CORRECTED HEAD REQUIRES A NEW
INDEPENDENT CLEAN-ROOM EXACT-HEAD REVIEW.

Founder decisions issued:
FD-B2B-1 PRIVATE MODULE BOUNDARY;
FD-B2B-2 STRICT INPUT DOMAIN;
FD-B2B-3 EXACT EQUALITY SEMANTICS;
FD-B2B-4 QUESTION NORMALIZATION AND TOKENIZATION;
FD-B2B-5 CANONICAL SCORE, JACCARD AND EMPTY-INPUT SEMANTICS;
FD-B2B-6 CANONICAL FINDING IDENTITY AND ORDERING;
FD-B2B-7 CLASSIFICATION, SUPPRESSION AND REPORT SEMANTICS;
FD-B2B-8 RAW-TEXT AND PROMOTABLE-ARTIFACT BOUNDARY;
FD-B2B-9 DETERMINISTIC ERRORS AND SIDE-EFFECT PROHIBITION;
FD-B2B-10 ACTIVATION AND SEQUENCING

Subordination:
SUBORDINATE TO D1 THROUGH D10, FD-B2-1 THROUGH FD-B2-8, FD-B2A-1 THROUGH
FD-B2A-8, AND THE ACCEPTED P01-04B2A IMPLEMENTATION. AMENDS NONE OF THEM.

Exact future implementation allowlist:
A src/medscale/mesc/_leakage_v1.py;
A tests/test_mesc_leakage_v1.py.
NO OTHER PATH IS AUTHORIZED; THE ALLOWLIST MUST NOT BE EXPANDED DURING
IMPLEMENTATION.

Activation conditions:
ALL FIVE REQUIRED — INDEPENDENT EXACT-HEAD PACKAGE REVIEW, SEPARATE FOUNDER
READY DECISION, SEPARATE FOUNDER MERGE DECISION, MERGE INTO CANONICAL MAIN,
AND MECHANICAL POST-MERGE VERIFICATION.
NO SUBSET ACTIVATES P01-04B2B IMPLEMENTATION AUTHORITY.
A MERGE THAT BYPASSES REVIEW OR THE FOUNDER DECISIONS DOES NOT ADOPT THIS
PACKAGE, REGARDLESS OF THE RESULTING GIT STATE.

Main-branch protection context:
RULESET 20172239 "MedScale canonical main protection v1" IS ACTIVE ON
refs/heads/main WITH NO BYPASS ACTORS. SECURITY CONTEXT ONLY; IT DOES NOT
REPLACE THE GOVERNANCE REVIEW AND FOUNDER-DECISION GATES.

Independent exact-head review of this r3 package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE.
NO EARLIER REVIEW CARRIES OVER.

P01-04B2B authorization package:
PREPARED ON NON-CANONICAL DRAFT BRANCH

FD-B2B-1 through FD-B2B-10:
RECORDED IN DRAFT PACKAGE; NOT ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
INACTIVE

P01-04B2B implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2B acceptance:
NOT ACHIEVED

P01-04B2C / P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real execution and all downstream work:
NOT AUTHORIZED — REAL PILOT-01 SPLIT, REAL OR CANONICAL LEAKAGE AUDIT, FIXTURE
FACADE, CLI, FILESYSTEM PUBLICATION, P01-03G OR REAL DATASET ACCESS, B0/B1
EXECUTION, MODEL ACCESS, INFERENCE, RETRIEVAL, METRICS, BENCHMARK EXECUTION,
TRAINING, FINE-TUNING, PUBLICATION AND CLINICAL USE

Prerequisite:
P01-T03B11 ADOPTED (PR #67 merge bfc4254b...) AND FD-B2A-9 ADOPTED;
CANONICAL INTEGRITY INCIDENT CONTAINED (PR #70 merge 06078180...)

Scope:
Record the founder implementation-authorization decisions FD-B2B-1 through
FD-B2B-10 for the P01-04B2B leakage primitive library as a clean r3
reconstruction from the protected canonical main, together with the exact
future two-path implementation allowlist and the five activation conditions.
This gate implements nothing, executes nothing, and inspects no real or
canonical records. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/ and
specs/mesc-pilot-01/p01-04b2a-acceptance/ and is not restated.
```

```text
P01-T03B13 — Record P01-04B2B implementation acceptance

Documentation status:
RECORDED — NOT ADOPTED; FD-B2B-11 NOT YET ADOPTED ON CANONICAL MAIN

Founder disposition:
P01-04B2B IMPLEMENTATION ACCEPTED (2026-08-02)

Required canonical baseline:
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863
(tree 070b177194094e5ae55d34570a86997fde956302;
ordered parents aeff056cb02fc9f72d2d861cadb84622c5558032 THEN
86cfdca1797cf1be60761284af1cc81e25047f41)

Adopted authorization:
PR #71 — MERGED AS aeff056cb02fc9f72d2d861cadb84622c5558032
(merge tree c265f6ec84de8b7bfcc56b5b569e52ac08ef9a91; merged head
3aa452092a269ab7d62d807bce2339dda8a9533e; merged 2026-08-01T23:45:40Z;
5 files; +2197 / -0); FD-B2B-1 THROUGH FD-B2B-10 AND THE R3 IMPLEMENTATION
CONTRACT. ADOPTED BEFORE THE IMPLEMENTATION COMMIT WAS AUTHORED, SATISFYING
THE FD-B2B-10 ACTIVATION SEQUENCING.

Accepted implementation:
PR #72 — MERGED / CLOSED / NOT DRAFT;
CANONICAL MERGE d91f76e77c4753e556b2ca9c2ee1bfcd5923d863;
REVIEWED AND MERGED HEAD 86cfdca1797cf1be60761284af1cc81e25047f41;
IMPLEMENTATION TREE 070b177194094e5ae55d34570a86997fde956302;
IMPLEMENTATION PARENT aeff056cb02fc9f72d2d861cadb84622c5558032;
1 COMMIT / 2 FILES / +2260 / -0; MERGED 2026-08-02T00:57:57Z

Accepted implementation scope:
src/medscale/mesc/_leakage_v1.py
BLOB 61f2bf4dff7e71f0a7f2be21b425ba8686badf16 (+964);
tests/test_mesc_leakage_v1.py
BLOB a7a77ceee84206c5bfb64b07e64083bb4b0af660 (+1296).
EXACTLY THE TWO AUTHORIZED PATHS; NO THIRD PATH.

Independent implementation review:
COMPLETED AT THE EXACT HEAD 86cfdca1797cf1be60761284af1cc81e25047f41
(TREE 070b177194094e5ae55d34570a86997fde956302) —
APPROVE WITH NON-BLOCKING NOTES; INDEPENDENCE SATISFIED;
BLOCKING FINDINGS NONE

Exact-head checks:
CI RUN 30725954034 — EVENT pull_request; run_attempt 1; COMPLETED / SUCCESS;
quality (py3.11) SUCCESS; quality (py3.12) SUCCESS.
CODEQL RUN 30725954031 — EVENT pull_request; run_attempt 1;
COMPLETED / SUCCESS; analyze (python) SUCCESS.
BOTH quality JOBS COVERED LOCKED DEPENDENCY SYNC, RUFF LINT, RUFF FORMAT,
MYPY STRICT, PYTEST AND medscale check.
NO RERUN, RETRY, REPLACEMENT WORKFLOW OR MANUAL DISPATCH OCCURRED.
NO SEPARATE POST-MERGE CI WORKFLOW IS CLAIMED.

Merge evidence:
READY SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED;
MERGE SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED;
MERGED FROM THE EXACT REVIEWED HEAD;
MERGE TREE IDENTICAL TO THE REVIEWED TREE;
SOURCE BRANCH feat/mesc-p01-04b2b-leakage-primitives RETAINED AT
86cfdca1797cf1be60761284af1cc81e25047f41 — NOT DELETED

Mechanical post-merge verification:
PASSED — PR #72 MERGED FROM THE EXACT REVIEWED HEAD; CANONICAL MAIN EQUALS
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863; BOTH REVIEWED BLOBS PRESENT ON MAIN;
CANONICAL DELTA LIMITED TO THE TWO ACCEPTED PATHS; SOURCE BRANCH NOT DELETED

Contract conformance:
IMPLEMENTATION-CONTRACT §§1–15 MAPPED CRITERION BY CRITERION;
15 OF 15 SECTIONS CONFORM; BLOCKING FINDINGS NONE

Accepted implementation observations:
NB-1 EMPTY IDENTITY ARRAYS REJECTED THROUGH NECESSARY FAIL-CLOSED INFERENCE;
NB-2 THRESHOLD BOUNDARY TESTS ALONE DO NOT DISCRIMINATE INTEGER FROM FLOAT
COMPARISON, THOUGH SOURCE INSPECTION CONFIRMS INTEGER-ONLY THRESHOLD LOGIC;
NB-3 EVIDENCE-REFERENCE LOCAL-PATH CHECK USES AN IMPLEMENTATION-DEFINED
HEURISTIC GROUNDED IN THE SENIOR "NOT LOCAL PATH" REQUIREMENT;
NB-4 CANONICAL FINDING DOCUMENT INCLUDES A SCHEMA MEMBER NOT EXPRESSLY LISTED
IN THE SENIOR LeakageFinding FIELD LIST;
NB-5 detection_methods ALLOWLIST IS NARROWER THAN THE SENIOR GENERIC
ARRAY-OF-STRINGS TYPE;
NB-6 UNICODE COMBINING MARKS ACT AS TOKEN BOUNDARIES, CONSISTENT WITH MAXIMAL
UNICODE ALPHANUMERIC-RUN SEMANTICS.
ALL SIX ARE ACCEPTED NON-BLOCKING IMPLEMENTATION OBSERVATIONS —
NOT CORRECTED, NOT SILENTLY RESOLVED, AND NOT UPGRADED INTO NEW PUBLIC
BEHAVIOUR. NO IMPLEMENTATION CORRECTION IS AUTHORIZED.

Founder decision:
FD-B2B-11 — P01-04B2B IMPLEMENTATION ACCEPTANCE DISPOSITION;
DECISION: ACCEPT P01-04B2B IMPLEMENTATION.
ACCEPTANCE APPLIES ONLY TO THE PRIVATE FIXTURE-ONLY LEAKAGE PRIMITIVE LIBRARY;
IT DOES NOT AUTHORIZE ORCHESTRATION, DATASET SCANNING, RECORD-PAIR DISCOVERY,
REAL EXECUTION OR A REAL LEAKAGE AUDIT; IT DOES NOT AUTHORIZE P01-04B2C OR
P01-04B2D; AND IT DOES NOT COMPLETE OR ACCEPT P01-04B AS A WHOLE.

FD-B2B-11:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE; NOT YET CANONICALLY ADOPTED

Adoption conditions:
ALL FIVE REQUIRED — INDEPENDENT CLEAN-ROOM EXACT-HEAD REVIEW OF THIS
ACCEPTANCE PACKAGE, SEPARATE FOUNDER READY DECISION, SEPARATE FOUNDER MERGE
DECISION, MERGE INTO CANONICAL MAIN, AND MECHANICAL POST-MERGE VERIFICATION.
NO SUBSET ADOPTS FD-B2B-11.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B13 was recorded, before FD-B2B-11
was adopted on canonical main through PR #73. It is retained as historical
governance evidence and is not the repository's present controlling state. The
later P01-T03B14 Current controlling state supersedes this block.

P01-T03B12 documentation:
ADOPTED ON CANONICAL MAIN

PR #71:
MERGED AND MECHANICALLY VERIFIED AS
aeff056cb02fc9f72d2d861cadb84622c5558032

FD-B2B-1 through FD-B2B-10:
ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT

PR #72:
MERGED AND MECHANICALLY VERIFIED AS
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863

P01-04B2B implementation:
COMPLETE ON CANONICAL MAIN — INDEPENDENTLY REVIEWED AT ITS EXACT HEAD WITH NO
BLOCKING FINDING

FD-B2B-11:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B13

P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2C:
NOT AUTHORIZED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split, real or canonical leakage audit, leakage-audit orchestration,
dataset scanning, record-pair discovery, fixture facade, split facade, CLI,
filesystem publication, P01-03G or real dataset access, B0/B1 execution, model
access, inference, retrieval, metrics, benchmark execution, training,
fine-tuning, publication and clinical use:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2B-11:
RECORDED BUT NOT YET ADOPTED — see the five adoption conditions above

P01-04B2C:
UPON VALID ADOPTION OF FD-B2B-11, ELIGIBLE FOR A SEPARATE AUTHORIZATION
DECISION; NOT AUTOMATICALLY AUTHORIZED

Prerequisite:
P01-T03B12 ADOPTED (PR #71 merge aeff056c...) AND FD-B2B-1 THROUGH FD-B2B-10
ADOPTED; P01-04B2B IMPLEMENTATION MERGED AND MECHANICALLY VERIFIED
(PR #72 merge d91f76e7...)

Scope:
Record the founder's acceptance of the P01-04B2B implementation as FD-B2B-11,
together with the exact accepted implementation identity, the independent
exact-head review evidence, the exact-head check evidence, the Ready and merge
evidence, the mechanical post-merge verification, the criterion-by-criterion
contract mapping, and the six accepted non-blocking observations. This gate
implements nothing, corrects nothing, executes nothing, and authorizes no
downstream phase. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-acceptance/ and
specs/mesc-pilot-01/p01-04b2b-authorization/ and is not restated.
```

```text
P01-T03B14 — Authorize P01-04B2C fixture-facade implementation

Documentation status:
RECORDED — NOT ADOPTED; FD-B2C-1 THROUGH FD-B2C-12 NOT YET ADOPTED ON
CANONICAL MAIN

Founder decision:
AUTHORIZE P01-04B2C IMPLEMENTATION SUBJECT TO VALID CANONICAL ADOPTION OF THIS
PACKAGE (2026-08-02)

Required canonical baseline:
3c4d7f153522128533fa9aba26209426b248b4f1
(tree e548aab1342c8783c1b919e707e5036a18e4a80a;
ordered parents d91f76e77c4753e556b2ca9c2ee1bfcd5923d863 THEN
a7b25f1755da2ca62fe516a68ae684b493be6bce;
subject "Merge pull request #73 from IamShehri/docs/mesc-p01-04b2b-acceptance")

Governance state entering this decision:
FD-B2B-11 ADOPTED ON CANONICAL MAIN THROUGH PR #73.
P01-04B2A ACCEPTED. P01-04B2B ACCEPTED.
P01-04B2C ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION BUT NOT YET
AUTHORIZED BEFORE THIS DECISION — ELIGIBILITY WAS NEVER IMPLEMENTATION
AUTHORITY.
P01-04B2D NOT AUTHORIZED. P01-04B INCOMPLETE / NOT ACCEPTED.

Authority chain:
SUBORDINATE TO P01-04A D1-D10, FD-B2-1 THROUGH FD-B2-8, FD-B2A-1 THROUGH
FD-B2A-8, FD-B2A-9, FD-B2B-1 THROUGH FD-B2B-10, FD-B2B-11, AND THE ACCEPTED
B2A AND B2B IMPLEMENTATIONS. ON CONFLICT THE SENIOR AUTHORITY CONTROLS.

Accepted modules the future implementation reuses without forking:
src/medscale/mesc/_split_v1.py (B1);
src/medscale/mesc/_canonical_json_v1.py AND
src/medscale/mesc/_split_artifacts_v1.py (B2A, canonical merge
5736b1171f1aa467105d931713f5749fb81acd5b, final head
7307fcf9085d3d15114984731b49d484523f09eb);
src/medscale/mesc/_leakage_v1.py (B2B, canonical merge
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863, reviewed head
86cfdca1797cf1be60761284af1cc81e25047f41, accepted tree
070b177194094e5ae55d34570a86997fde956302).

Founder decisions issued:
FD-B2C-1 PRIVATE MODULE AND EXACT FUTURE PATH ALLOWLIST;
FD-B2C-2 STATELESS FIXTURE-ONLY FACADE;
FD-B2C-3 EXACT IMMUTABLE REQUEST CONTRACT;
FD-B2C-4 FIXTURE IDENTITY AND HONEST PROOF SEMANTICS;
FD-B2C-5 EXACT B1 INTEGRATION PIPELINE;
FD-B2C-6 B1 COMPATIBILITY MANIFEST;
FD-B2C-7 CANONICAL IN-MEMORY ARTIFACTS;
FD-B2C-8 LEAKAGE INTEGRATION WITHOUT SCANNING;
FD-B2C-9 EXACT IMMUTABLE RESULT CONTRACT;
FD-B2C-10 TYPED ERRORS AND VALIDATION ORDER;
FD-B2C-11 SIDE-EFFECT AND AUTHORITY PROHIBITION;
FD-B2C-12 ACTIVATION AND SEQUENCING.

Exact future implementation allowlist:
src/medscale/mesc/_fixture_split_v1.py;
tests/test_mesc_fixture_split_v1.py.
EXACTLY TWO PATHS; NO THIRD PATH AUTHORIZED. THE FUTURE IMPLEMENTATION MUST
NOT MODIFY __init__.py, split.py, _split_v1.py, _canonical_json_v1.py,
_split_artifacts_v1.py, _leakage_v1.py, ANY CLI, ANY WORKFLOW, ANY DEPENDENCY
OR LOCKFILE, OR ANY GOVERNANCE DOCUMENT.

Honest structural-proof semantics:
fixture_only, non_evidence AND synthetic_identity_proof ARE DECLARED MARKERS
ESTABLISHING INTERNAL IDENTITY CONSISTENCY ONLY. THEY ARE NOT A CRYPTOGRAPHIC
OR REAL-WORLD PROVENANCE ORACLE, AND NO FLAG COMBINATION CAN DETECT A CALLER
REPACKAGING REAL DATA. B2C SAFETY DERIVES FROM STRUCTURE: PRIVATE MODULE, NO
PUBLIC EXPORT, NO CLI, NO PATH INPUT, NO REGISTRY ADAPTER, NO FILESYSTEM
ACCESS, NO REAL-DATA ENTRY POINT, AND SourceDocumentGroupedSplitter.assign
REMAINING FAIL-CLOSED.

Implementation authority:
RECORDED BUT INACTIVE. P01-04B2C IMPLEMENTATION IS NOT AUTHORIZED TO BEGIN.

Activation gate:
ALL FIVE REQUIRED — INDEPENDENT CLEAN-ROOM EXACT-HEAD REVIEW OF THIS
AUTHORIZATION PACKAGE, SEPARATE FOUNDER READY DECISION, SEPARATE FOUNDER MERGE
DECISION, MERGE INTO CANONICAL MAIN, AND MECHANICAL POST-MERGE VERIFICATION.
NO SUBSET ACTIVATES P01-04B2C IMPLEMENTATION AUTHORITY.
UPON VALID ACTIVATION THE AUTHORITY IS ACTIVE FOR ONE BOUNDED IMPLEMENTATION
ONLY AND IS SPENT AFTER ONE IMPLEMENTATION COMMIT SERIES IS ACCEPTED FOR
PUBLICATION. IMPLEMENTATION DOES NOT EQUAL ACCEPTANCE.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B14 was recorded, before FD-B2C-1
through FD-B2C-12 were adopted on canonical main through PR #74 and before the
P01-04B2C implementation was merged through PR #75. It is retained as
historical governance evidence and is not the repository's present controlling
state. The later P01-T03B15 Current controlling state supersedes this block.

P01-T03B13 documentation:
ADOPTED ON CANONICAL MAIN

PR #73:
MERGED AND MECHANICALLY VERIFIED AS
3c4d7f153522128533fa9aba26209426b248b4f1

FD-B2B-11:
ADOPTED ON CANONICAL MAIN

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

FD-B2C-1 through FD-B2C-12:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
RECORDED BUT INACTIVE

P01-04B2C implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, automatic finding discovery, CLI, public export, filesystem
publication, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
publication and clinical use:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2C-1 through FD-B2C-12:
RECORDED BUT NOT YET ADOPTED — see the five activation conditions above

P01-04B2C implementation:
UPON VALID ACTIVATION, AUTHORIZED FOR ONE BOUNDED IMPLEMENTATION WITHIN THE
EXACT TWO-PATH ALLOWLIST; STILL REQUIRES AN INDEPENDENT EXACT-HEAD
IMPLEMENTATION REVIEW, EXACT-HEAD CI AND CODEQL, A SEPARATE READY DECISION, A
SEPARATE MERGE DECISION, POST-MERGE MECHANICAL VERIFICATION, A SEPARATE
IMPLEMENTATION-ACCEPTANCE DISPOSITION, AND CANONICAL ADOPTION OF THAT
DISPOSITION

P01-04B2D:
NOT AUTHORIZED — REMAINS UNAUTHORIZED UNTIL P01-04B2C IS CANONICALLY ACCEPTED.
ITS THREE 1,000-ROW FIXTURES exact-reference-1000-v1,
constraint-stress-1000-v1 AND leakage-positive-v1 MUST NOT BE IMPLEMENTED OR
QUALIFIED DURING B2C

Prerequisite:
P01-T03B13 ADOPTED (PR #73 merge 3c4d7f15...) AND FD-B2B-11 ADOPTED;
P01-04B2A AND P01-04B2B ACCEPTED

Scope:
Record the founder's authorization of the P01-04B2C fixture-only in-memory
facade and integration entry point as FD-B2C-1 through FD-B2C-12, together with
the exact future two-path implementation allowlist, the exact request and
result contracts, the exact fixture and request identity payloads, the exact B1
integration pipeline, the canonical in-memory artifact schemas and ordering,
the non-circular summary and fingerprint construction, the explicit-finding
leakage integration, the typed error categories and validation order, the
side-effect prohibition, and the five-condition activation gate. This gate
implements nothing, executes nothing, accepts nothing, and authorizes no
downstream phase. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/ and
specs/mesc-pilot-01/p01-04b2b-acceptance/ and is not restated.
```

```text
P01-T03B15 — Record P01-04B2C implementation acceptance

Documentation status:
RECORDED — NOT ADOPTED; FD-B2C-ACT-1 AND FD-B2C-13 NOT YET ADOPTED ON CANONICAL
MAIN

Founder decision:
ACCEPT P01-04B2C IMPLEMENTATION (2026-08-02)

Required canonical baseline:
9d4b9ed0bada16455781240bb074ffd852397988
(tree 2fc26581ceb1b09216b2bf51de10fcbece68a62b;
ordered parents fb17439e6c9f0f28b31689c82567cd9c97312085 THEN
17c7478f4e052ac331505d3fcfe4dfde825db898;
subject "Merge pull request #75 from IamShehri/feat/mesc-p01-04b2c-fixture-facade")

Governance state entering this decision:
FD-B2C-1 THROUGH FD-B2C-12 ADOPTED ON CANONICAL MAIN THROUGH PR #74.
P01-04B2C IMPLEMENTATION AUTHORITY ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT.
P01-04B2C IMPLEMENTATION MERGED ON CANONICAL MAIN THROUGH PR #75 AND
INDEPENDENTLY REVIEWED AT ITS EXACT HEAD WITH NO BLOCKING FINDING, BUT NOT YET
FOUNDER-ACCEPTED AND NOT YET CANONICALLY ACCEPTED BEFORE THIS DECISION.
P01-04B2A ACCEPTED. P01-04B2B ACCEPTED.
P01-04B2D NOT AUTHORIZED. P01-04B INCOMPLETE / NOT ACCEPTED.

Authority chain:
SUBORDINATE TO P01-04A D1-D10, FD-B2-1 THROUGH FD-B2-8, FD-B2A-1 THROUGH
FD-B2A-8, FD-B2A-9, FD-B2B-1 THROUGH FD-B2B-10, FD-B2B-11, FD-B2C-1 THROUGH
FD-B2C-12, AND THE ACCEPTED B2A AND B2B IMPLEMENTATIONS. ON CONFLICT THE SENIOR
AUTHORITY CONTROLS.

Founder decisions issued:
FD-B2C-ACT-1 FOUNDER ACTIVATION CONFIRMATION;
FD-B2C-13 P01-04B2C IMPLEMENTATION ACCEPTANCE DISPOSITION.

FD-B2C-ACT-1:
CONFIRMS THAT ALL FIVE FD-B2C-12 ACTIVATION CONDITIONS WERE SATISFIED BEFORE
IMPLEMENTATION COMMIT 17c7478f4e052ac331505d3fcfe4dfde825db898 WAS CREATED —
INDEPENDENT CLEAN-ROOM EXACT-HEAD REVIEW OF THE AUTHORIZATION PACKAGE,
SEPARATE FOUNDER READY DECISION, SEPARATE FOUNDER MERGE DECISION, MERGE INTO
CANONICAL MAIN AS fb17439e6c9f0f28b31689c82567cd9c97312085, AND MECHANICAL
POST-MERGE VERIFICATION. THE ONE BOUNDED AUTHORITY IS NOW SPENT.
IT CONFIRMS SEQUENCING ONLY, CREATES NO NEW IMPLEMENTATION AUTHORITY, DOES NOT
ACCEPT THE IMPLEMENTATION, AND DOES NOT AUTHORIZE P01-04B2D.

Accepted implementation identity:
AUTHORIZATION PR #74, HEAD 89a708587ef28b4e19f6225ce86181715a680805,
TREE c5afa12e85ef4e0c7f9fcbf71c673da211e1ef2a, CANONICAL MERGE
fb17439e6c9f0f28b31689c82567cd9c97312085;
IMPLEMENTATION PR #75, REVIEWED AND MERGED HEAD
17c7478f4e052ac331505d3fcfe4dfde825db898, TREE
2fc26581ceb1b09216b2bf51de10fcbece68a62b, PARENT
fb17439e6c9f0f28b31689c82567cd9c97312085, CANONICAL MERGE
9d4b9ed0bada16455781240bb074ffd852397988;
1 COMMIT / 2 FILES / +2266 / -0.

Accepted paths and blobs:
src/medscale/mesc/_fixture_split_v1.py
blob 6511861b41b2276948a6903292f07c3735317177 (947 additions);
tests/test_mesc_fixture_split_v1.py
blob 5a2c1d5a19afa4ebee63ffacee5c4b9a7aabafd9 (1319 additions).
EXACTLY TWO PATHS; NO THIRD PATH. __init__.py, split.py, _split_v1.py,
_canonical_json_v1.py, _split_artifacts_v1.py AND _leakage_v1.py UNCHANGED.

Evidence:
INDEPENDENT EXACT-HEAD IMPLEMENTATION REVIEW — APPROVE WITH NON-BLOCKING NOTES,
INDEPENDENCE SATISFIED, BLOCKING FINDINGS NONE;
CI RUN 30736118968 AND CODEQL RUN 30736118959 COMPLETED / SUCCESS AT HEAD
17c7478f4e052ac331505d3fcfe4dfde825db898, EVENT pull_request, RUN ATTEMPT 1,
JOBS quality (py3.11), quality (py3.12) AND analyze (python) ALL SUCCESS;
INDEPENDENT VALIDATION AT EXACT HEAD — 145 FOCUSED TESTS PASSED, 1579 PASSED
AND 2 SKIPPED FULL SUITE, RUFF AND RUFF FORMAT PASS, MYPY PASS INCLUDING 175
FILES PROJECT-WIDE, medscale check CLEAN;
MECHANICAL POST-MERGE VERIFICATION — CANONICAL TREE EQUALS THE REVIEWED TREE,
BASE-TO-MERGE DELTA EXACTLY THE TWO PATHS AT +2266 / -0, REVIEWED-HEAD-TO-MERGE
DELTA ZERO CHANGED FILES, BOTH BLOBS PRESENT, SOURCE BRANCH RETAINED.
NO POST-MERGE WORKFLOW RESULT IS CLAIMED AS PART OF THAT VERIFICATION, AND NO
SUBMITTED GITHUB REVIEW, REVIEW DECISION, PR COMMENT OR INLINE REVIEW THREAD IS
CLAIMED; THE OBSERVED PR STATE HAD NONE.

Accepted and discharged observations:
NB-1 THROUGH NB-5 ACCEPTED AS NON-BLOCKING IMPLEMENTATION OBSERVATIONS;
NB-6 DISCHARGED BY FD-B2C-ACT-1 AS A NON-BLOCKING GOVERNANCE OBSERVATION.
NONE IS A DEFERRED OBLIGATION. NO IMPLEMENTATION CORRECTION IS AUTHORIZED. NO
FOLLOW-UP SOURCE COMMIT, TEST COMMIT, CONTRACT AMENDMENT, PUBLIC EXPORT,
BEHAVIORAL EXTENSION OR SCOPE EXPANSION IS AUTHORIZED.

Scope of acceptance:
APPLIES ONLY TO THE EXACT PRIVATE FIXTURE-ONLY, IN-MEMORY P01-04B2C FACADE
MERGED THROUGH PR #75. RECOGNIZES DETERMINISTIC COMPOSITION OF ACCEPTED B1, B2A
AND B2B LAYERS UNDER SYNTHETIC IDENTITY-ONLY FIXTURES. DOES NOT TRANSFORM ANY
GENERATED IN-MEMORY VALUE INTO EVIDENCE, A PUBLISHABLE ARTIFACT, A CANONICAL
REAL SPLIT, A LEAKAGE-AUDIT RESULT OR A CLINICAL/RESEARCH CONCLUSION. ALL
GOLDEN VALUES ARE SYNTHETIC UNIT-FIXTURE IDENTITIES, NOT SCIENTIFIC OR DATASET
EVIDENCE.

Adoption gate:
ALL FIVE REQUIRED — INDEPENDENT CLEAN-ROOM EXACT-HEAD REVIEW OF THIS ACCEPTANCE
PACKAGE, SEPARATE FOUNDER READY DECISION, SEPARATE FOUNDER MERGE DECISION,
MERGE INTO CANONICAL MAIN, AND MECHANICAL POST-MERGE VERIFICATION.
NO SUBSET CANONICALLY ADOPTS FD-B2C-ACT-1 OR FD-B2C-13.
NO SUBSET CANONICALLY ACCEPTS P01-04B2C.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B15 was recorded, before FD-B2C-ACT-1
and FD-B2C-13 were adopted on canonical main through PR #76 and before P01-04B2D
was authorized. It is retained as historical governance evidence and is not the
repository's present controlling state. The later P01-T03B16 Current controlling
state supersedes this block.

P01-T03B14 documentation:
ADOPTED ON CANONICAL MAIN

PR #74:
MERGED AND MECHANICALLY VERIFIED AS
fb17439e6c9f0f28b31689c82567cd9c97312085

FD-B2C-1 through FD-B2C-12:
ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT

PR #75:
MERGED AND MECHANICALLY VERIFIED AS
9d4b9ed0bada16455781240bb074ffd852397988

P01-04B2C implementation:
COMPLETE ON CANONICAL MAIN — INDEPENDENTLY REVIEWED AT ITS EXACT HEAD WITH NO
BLOCKING FINDING

FD-B2C-ACT-1:
FOUNDER CONFIRMATION RECORDED — NOT YET CANONICALLY RECORDED IN THE
REPOSITORY; see P01-T03B15

FD-B2C-13:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B15

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
FOUNDER-ACCEPTED IN SUBSTANCE; NOT YET CANONICALLY ADOPTED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, automatic finding discovery, CLI, public export, filesystem
publication, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
publication and clinical use:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2C-ACT-1 and FD-B2C-13:
RECORDED BUT NOT YET ADOPTED — see the five adoption conditions above

P01-04B2D:
UPON CANONICAL ADOPTION OF FD-B2C-13, ELIGIBLE FOR A SEPARATE AUTHORIZATION
DECISION AND NOTHING MORE; NOT AUTOMATICALLY AUTHORIZED. ELIGIBILITY IS NEVER
IMPLEMENTATION AUTHORITY. ITS THREE 1,000-ROW FIXTURES exact-reference-1000-v1,
constraint-stress-1000-v1 AND leakage-positive-v1 REMAIN NEITHER IMPLEMENTED
NOR QUALIFIED

Prerequisite:
P01-T03B14 ADOPTED (PR #74 merge fb17439e...) AND FD-B2C-1 THROUGH FD-B2C-12
ADOPTED; P01-04B2C IMPLEMENTATION MERGED (PR #75 merge 9d4b9ed0...) AND
INDEPENDENTLY REVIEWED WITH NO BLOCKING FINDING

Scope:
Record the founder's separate implementation-acceptance disposition for the
P01-04B2C fixture-only in-memory facade as FD-B2C-13, and canonically record the
already issued founder activation confirmation as FD-B2C-ACT-1, together with
the exact authorization and implementation identity, the twelve-criterion
decision basis, the independent review, CI, CodeQL, Ready, merge and mechanical
post-merge evidence, the criterion-by-criterion mapping to
implementation-contract.md sections 1 through 16, the dispositions of NB-1
through NB-6, the bounded scope of acceptance, and the five-condition adoption
gate. This gate implements nothing, executes nothing, corrects nothing, and
authorizes no downstream phase. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/,
specs/mesc-pilot-01/p01-04b2b-acceptance/ and
specs/mesc-pilot-01/p01-04b2c-authorization/ and is not restated.
```

```text
P01-T03B16 — Authorize P01-04B2D integrated synthetic qualification

Documentation status:
RECORDED — NOT ADOPTED; FD-B2D-1 THROUGH FD-B2D-14 NOT YET ADOPTED ON CANONICAL
MAIN

Founder decision:
AUTHORIZE ONE BOUNDED P01-04B2D INTEGRATED SYNTHETIC QUALIFICATION
IMPLEMENTATION SUBJECT TO THE ACTIVATION GATE (2026-08-02)

Required canonical baseline:
a0c623aa08354a343fccc1d066a7a6acaa5b8576
(tree 6e766deb531a9d7332942c3a524be0b3de698af3;
ordered parents 9d4b9ed0bada16455781240bb074ffd852397988 THEN
3edcc476cf403bbd4d9c2d5bb05d739b40abe748;
subject "Merge pull request #76 from IamShehri/docs/mesc-p01-04b2c-acceptance")

Chronological completion of P01-T03B15:
P01-04B2C acceptance package: PR #76.
Reviewed package head: 3edcc476cf403bbd4d9c2d5bb05d739b40abe748.
Canonical acceptance merge: a0c623aa08354a343fccc1d066a7a6acaa5b8576.
FD-B2C-ACT-1: CANONICALLY RECORDED.
FD-B2C-13: ADOPTED.
P01-04B2C: ACCEPTED.

Governance state entering this decision:
P01-04B2A, P01-04B2B AND P01-04B2C ACCEPTED. FD-B2C-ACT-1 CANONICALLY RECORDED
AND FD-B2C-13 ADOPTED THROUGH PR #76. THE P01-04B2C IMPLEMENTATION AUTHORITY IS
SPENT. P01-04B2D WAS ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION AND WAS NOT
AUTHORIZED. ELIGIBILITY WAS NEVER IMPLEMENTATION AUTHORITY.

FD-B2-7 conformance:
AN EARLIER DRAFTING ATTEMPT PROPOSED FIXTURE CONTRACTS THAT CONTRADICTED
FOUNDER-RATIFIED FD-B2-7, WHICH specs/mesc-pilot-01/p01-04b2/decision-record.md
DECLARES CONTROLLING ON CONFLICT. THE BUILD WAS STOPPED RATHER THAN SILENTLY
RECONCILED. THE FOUNDER SELECTED PATH 1 — CONFORM P01-04B2D TO RATIFIED FD-B2-7.
FD-B2-7 IS NOT AMENDED, SUPERSEDED OR NARROWED. THE CONFLICTING REQUIREMENTS ARE
WITHDRAWN. CORRECTED CONTROLLING VALUES: exact-reference-1000-v1 HAS 89 GROUPS
SPANNING SIZES 1, 2, 3, 5, 8 AND 13 WITH THE EXACT MATRIX FEASIBLE;
constraint-stress-1000-v1 HAS 500 GROUPS OF SIZE 2 MAKING THE EXACT MATRIX
INFEASIBLE WITH GLOBAL MINIMUM-DEVIATION SCORE 6; leakage-positive-v1 HAS 1000
ROWS AND EXACTLY 999 SOURCE-DOCUMENT GROUPS, BEING EXACTLY ONE HOMOGENEOUS
TWO-EXAMPLE SOURCE-DOCUMENT GROUP WHOSE MEMBERS SHARE A DECISION, REMAIN IN ONE
ACTUAL PARTITION AND NEVER STRADDLE A PARTITION BOUNDARY, PLUS EXACTLY 998
SINGLETON GROUPS AND NO OTHER MULTI-EXAMPLE GROUP, WITH 9 FINDINGS, AT LEAST
THREE SUPPORTED false_positive CLASSIFICATIONS AND AT LEAST ONE unresolved. THE
999-GROUP STRUCTURE IS A FOUNDER-FROZEN FIXTURE REQUIREMENT, NOT AN INFERENCE,
AND IS SUBORDINATE TO AND CONSISTENT WITH FD-B2-7 WITHOUT AMENDING IT.

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B16 was recorded, before FD-B2D-1
through FD-B2D-14 were adopted on canonical main through PR #77, before the
P01-04B2D implementation was merged through PR #78, and before FD-B2D-15 was
issued. It is retained as historical governance evidence and is not the
repository's present controlling state. The later P01-T03B17 Current controlling
state supersedes this block.

P01-T03B15 documentation:
ADOPTED ON CANONICAL MAIN

PR #76:
MERGED AND MECHANICALLY VERIFIED AS
a0c623aa08354a343fccc1d066a7a6acaa5b8576

FD-B2C-ACT-1:
CANONICALLY RECORDED

FD-B2C-13:
ADOPTED ON CANONICAL MAIN

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

P01-04B2C implementation authority:
SPENT

FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B16

P01-04B2D implementation authority:
RECORDED BUT INACTIVE

P01-04B2D implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D qualification:
NOT EXECUTED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, automatic finding discovery, CLI, public export, filesystem
publication, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
adapter creation, publication and clinical use:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2D-1 through FD-B2D-14:
RECORDED BUT NOT YET ADOPTED — see the five activation conditions above

P01-04B2D implementation:
UPON CANONICAL ADOPTION OF FD-B2D-1 THROUGH FD-B2D-14, AUTHORIZED TO BEGIN
EXACTLY ONCE WITHIN THE THREE-PATH ALLOWLIST
tests/_mesc_p01_04b2d_fixtures_v1.py,
tests/test_mesc_p01_04b2d_qualification_v1.py AND
.github/workflows/mesc-p01-04b2d-qualification.yml, AND NOTHING MORE. THE
AUTHORITY IS SPENT AT THAT COMMIT. NO PRODUCTION SOURCE CHANGE, PUBLIC EXPORT,
CLI OR NEW DEPENDENCY IS AUTHORIZED

P01-04B:
REMAINS NOT ACCEPTED WHILE ANY CRITERION IS UNSATISFIED. THE INDIVISIBLE-GROUP
GLOBAL MINIMUM-DEVIATION CRITERION OF FD-B2-7 FIXTURE B IS EXPECTED TO BE
RECORDED UNSATISFIED BECAUSE THE ACCEPTED IMPLEMENTATION FAILS CLOSED WITH THE
TYPED ALLOCATION ERROR RATHER THAN PRODUCING A MINIMUM-DEVIATION ALLOCATION. A
GREEN B2D QUALIFICATION CI DOES NOT EQUAL P01-04B ACCEPTANCE. A SEPARATE FOUNDER
CORRECTION AUTHORIZATION MUST PRECEDE ANY PRODUCTION IMPLEMENTATION OF GLOBALLY
MINIMUM-DEVIATION GROUPED ALLOCATION

Prerequisite:
P01-T03B15 ADOPTED (PR #76 merge a0c623aa...) AND FD-B2C-ACT-1 AND FD-B2C-13
ADOPTED; P01-04B2C ACCEPTED

Scope:
Record the founder's separate prospective authorization for P01-04B2D integrated
synthetic qualification as FD-B2D-1 through FD-B2D-14, together with the exact
three-path future implementation allowlist, the three ratified fixture contracts
conformed to FD-B2-7 without amendment, the shared synthetic identity contract
and non-circular generator-specification proof, the literal-golden requirements,
the six-cell cross-platform qualification workflow, the criterion-by-criterion
P01-04B acceptance-review contract including the expected UNSATISFIED
minimum-deviation criterion, the anti-circularity and fail-closed rules, the
evidence classification, the continuing prohibitions, the five-condition
activation gate and the nine post-implementation gates. This gate implements
nothing, constructs no fixture, invokes no facade, calculates no B2D output
value, executes nothing, and authorizes no downstream phase. Prior governance
history is adopted at specs/mesc-pilot-01/p01-04/,
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/,
specs/mesc-pilot-01/p01-04b2b-acceptance/,
specs/mesc-pilot-01/p01-04b2c-authorization/ and
specs/mesc-pilot-01/p01-04b2c-acceptance/ and is not restated.
```

```text
P01-T03B17 — Record P01-04B2D qualification acceptance
and P01-04B non-acceptance disposition

Documentation status:
RECORDED — NOT ADOPTED

Founder decision:
FD-B2D-15 ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Minimum-deviation capability:
UNSATISFIED

Production correction authority:
NOT GRANTED

P01-04C through P01-04G:
NOT AUTHORIZED

Required canonical baseline:
faf58c3fbfa9a83e7d392630e3ad1f322c616259
(tree 3d27b9c43462ef9880d5fab1ea45b675d5ff55c1;
ordered parents 63cefe04c23726957aa26ac60ca8087ac9ca333a THEN
6e5867829006770ad2ed50f26a9af0c455923594;
subject "Merge pull request #78 from IamShehri/test/mesc-p01-04b2d-qualification";
body "test(mesc): qualify P01-04B2D synthetic suite")

Chronological completion of P01-T03B16:
P01-04B2D authorization package: PR #77.
Reviewed package head: 096f6667251b4783fc9511336301dfaaa4c7f336.
Reviewed package tree: 30b4cb5433a7f8496e62b8a94d879cf34a8ff26a.
Canonical authorization merge: 63cefe04c23726957aa26ac60ca8087ac9ca333a.
Independent exact-head review of that package: COMPLETED, NO BLOCKING FINDING.
FD-B2D-1 THROUGH FD-B2D-14: ADOPTED.
P01-04B2D implementation authority: ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT.

Accepted implementation identity:
PR #78 on branch test/mesc-p01-04b2d-qualification.
Reviewed and merged head: 6e5867829006770ad2ed50f26a9af0c455923594.
Reviewed implementation tree: 3d27b9c43462ef9880d5fab1ea45b675d5ff55c1.
Implementation parent: 63cefe04c23726957aa26ac60ca8087ac9ca333a.
Canonical implementation merge: faf58c3fbfa9a83e7d392630e3ad1f322c616259.
1 commit / 3 files / 3223 additions / 0 deletions, being exactly
.github/workflows/mesc-p01-04b2d-qualification.yml blob
b45811a2e104e61149c766b39d3c1ad832959b69, tests/_mesc_p01_04b2d_fixtures_v1.py
blob f35b4443e79338d2309ca9f4197eee8368ea7069 and
tests/test_mesc_p01_04b2d_qualification_v1.py blob
ad215f717ef1b27bc7adbfb5c68d81e91ccfc6dd. No production module, dependency,
lockfile, public export, CLI or entry point was changed.

Review and workflow basis:
Independent clean-room exact-head implementation review returned APPROVE WITH
NON-BLOCKING NOTES with NO BLOCKING FINDING at head
6e5867829006770ad2ed50f26a9af0c455923594 and tree
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1. All nine non-blocking observations are
carried forward in full and ACCEPTED AS NON-BLOCKING; no correction authorization
is issued and no deferred implementation obligation is created. Pull-request
checks at the exact head: CI run 30780440275 success 2/2, CodeQL run 30780440276
success 1/1, MESC P01-04B2D Qualification run 30780440318 success 6/6. Post-merge
push-triggered runs at faf58c3f...: CI run 30781355622 success 2/2, CodeQL run
30781355591 success 1/1, MESC P01-04B2D Qualification run 30781355599 success
6/6. Mechanical post-merge verification: PASSED. Workflow success is
qualification-harness evidence only and is not scientific, clinical, dataset or
real-split evidence.

Criterion disposition:
Criteria 1 through 10 SATISFIED. Criterion 11 atomic publication and criterion 12
write-path protections are NOT APPLICABLE TO B2D and NOT SATISFIED FOR P01-04B
OVERALL. Criterion 13 date-free promotable artifacts is NOT APPLICABLE TO B2D
OUTPUT PROMOTION, with the date-free canonical-byte invariant SATISFIED for the
synthetic B2D surfaces and establishing no promotability. Recorded separately,
outside the thirteen numbered criteria, the indivisible-group global
minimum-deviation allocation capability of FD-B2-7 Fixture B is UNSATISFIED
because the accepted allocation performs exact-target allocation only and fails
closed with the typed allocation error rather than producing a minimum-deviation
allocation. The typed fail-closed failure is correct detection of a missing
capability and is never conformance to it. NOT APPLICABLE is never converted to
SATISFIED. A GREEN QUALIFICATION WORKFLOW DOES NOT EQUAL P01-04B ACCEPTANCE.

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B17 was recorded, before FD-B2D-15
was adopted on canonical main through PR #79, and before FD-BR-1 and FD-BMD-1
through FD-BMD-14 were issued. It is retained as historical governance evidence
and is not the repository's present controlling state. The later P01-T03B18
Current controlling state supersedes this block.

P01-T03B16 documentation:
ADOPTED ON CANONICAL MAIN

PR #77:
MERGED AND MECHANICALLY VERIFIED AS
63cefe04c23726957aa26ac60ca8087ac9ca333a

FD-B2D-1 through FD-B2D-14:
ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT

PR #78:
MERGED AND MECHANICALLY VERIFIED AS
faf58c3fbfa9a83e7d392630e3ad1f322c616259

P01-04B2D implementation:
COMPLETE ON CANONICAL MAIN — INDEPENDENTLY REVIEWED AT ITS EXACT HEAD WITH NO
BLOCKING FINDING; SIX-CELL QUALIFICATION SUCCEEDED BEFORE AND AFTER MERGE

FD-B2D-15:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B17

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

P01-04B2D:
FOUNDER-ACCEPTED IN SUBSTANCE; NOT YET CANONICALLY ADOPTED

Indivisible-group global minimum-deviation allocation:
UNSATISFIED

Atomic publication:
NOT APPLICABLE TO B2D; NOT SATISFIED FOR P01-04B OVERALL

Write-path protections:
NOT APPLICABLE TO B2D; NOT SATISFIED FOR P01-04B OVERALL

Date-free canonical-byte invariant:
SATISFIED FOR THE SYNTHETIC B2D SURFACES; ESTABLISHES NO PROMOTABILITY

P01-04B acceptance eligibility:
FALSE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Production correction authority:
NOT GRANTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, automatic finding discovery, CLI, public export, filesystem
publication, promotion of any B2D output, P01-03G or real dataset access,
B0/B1 execution, model access, inference, retrieval, metrics, benchmark
execution, training, fine-tuning, adapter creation, publication and clinical
use:
NOT AUTHORIZED

--- Future gated authority ---

FD-B2D-15:
RECORDED BUT NOT YET ADOPTED — canonical adoption requires all five conditions:
a genuinely independent clean-room exact-head review of this acceptance package,
a separate Founder Ready decision, a separate Founder Merge decision, merge into
canonical main, and mechanical post-merge verification. NO SUBSET ADOPTS
FD-B2D-15. NO SUBSET CANONICALLY ACCEPTS P01-04B2D.

Minimum-deviation production correction, atomic-publication implementation and
write-path implementation:
EACH ELIGIBLE FOR A SEPARATE FOUNDER CONSIDERATION WITH ITS OWN AUTHORIZATION,
CONTRACT, INDEPENDENT REVIEW AND ACCEPTANCE DECISION. ELIGIBILITY IS NEVER
AUTHORITY. NONE IS AUTHORIZED BY THIS PACKAGE

P01-04B:
REMAINS CHANGES REQUIRED / NOT ACCEPTED WHILE THE INDIVISIBLE-GROUP GLOBAL
MINIMUM-DEVIATION CRITERION IS UNSATISFIED AND THE ATOMIC-PUBLICATION AND
WRITE-PATH CRITERIA ARE NOT SATISFIED FOR P01-04B OVERALL

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Prerequisite:
P01-T03B16 ADOPTED (PR #77 merge 63cefe04...) AND FD-B2D-1 THROUGH FD-B2D-14
ADOPTED; P01-04B2D IMPLEMENTATION MERGED (PR #78 merge faf58c3f...) AND
MECHANICALLY VERIFIED

Scope:
Record the founder's qualification-acceptance disposition for the exact
P01-04B2D implementation as FD-B2D-15, together with the exact authorization and
implementation identity, the three accepted paths and blobs, the independent
exact-head review verdict and its nine accepted non-blocking observations, the
pull-request and post-merge CI, CodeQL and six-cell qualification evidence, the
mechanical post-merge verification, the three fixture dispositions, the complete
thirteen-criterion mapping, the separately recorded UNSATISFIED minimum-deviation
capability, the P01-04B CHANGES REQUIRED / NOT ACCEPTED decision, the withholding
of production correction authority, the five-condition adoption gate and the
continuing prohibitions. This gate implements nothing, executes nothing, corrects
nothing, promotes nothing, and authorizes no downstream phase. Prior governance
history is adopted at specs/mesc-pilot-01/p01-04/,
specs/mesc-pilot-01/p01-04b2/, specs/mesc-pilot-01/p01-04b2a/,
specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/,
specs/mesc-pilot-01/p01-04b2b-acceptance/,
specs/mesc-pilot-01/p01-04b2c-authorization/,
specs/mesc-pilot-01/p01-04b2c-acceptance/ and
specs/mesc-pilot-01/p01-04b2d-authorization/ and is not restated.
```

```text
P01-T03B18 — Authorize P01-04B minimum-deviation correction

Documentation status:
RECORDED — NOT ADOPTED

FD-BR-1:
ISSUED — NOT YET ADOPTED

FD-BMD-1 through FD-BMD-14:
ISSUED — NOT YET ADOPTED

Minimum-deviation implementation authority:
RECORDED BUT INACTIVE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Atomic publication:
NOT SATISFIED / NOT AUTHORIZED

Write-path protections:
NOT SATISFIED / NOT AUTHORIZED

P01-04C through P01-04G:
NOT AUTHORIZED

Required canonical baseline:
3513d66bc36650363a6368bb4e42901119419802
(tree e08393388f4684b39ef9226a3a90b719ea1ba494;
ordered parents faf58c3fbfa9a83e7d392630e3ad1f322c616259 THEN
c38473d69c996e626510256d6297640bd87405ad;
subject "Merge pull request #79 from IamShehri/docs/mesc-p01-04b2d-acceptance";
body "docs(mesc): record P01-04B2D qualification acceptance")

Chronological completion of P01-T03B17:
P01-04B2D acceptance package: PR #79.
Reviewed package head: c38473d69c996e626510256d6297640bd87405ad.
Canonical acceptance merge: 3513d66bc36650363a6368bb4e42901119419802.
Independent exact-head review of that package: COMPLETED, NO BLOCKING FINDING.
FD-B2D-15: ADOPTED ON CANONICAL MAIN.
P01-04B2D: ACCEPTED.

Recovery architecture recorded as FD-BR-1:
Increment 1 global minimum-deviation grouped allocation correction; increment 2
atomic publication and write-path protection boundary; increment 3 integrated
P01-04B requalification and acceptance disposition. Each increment requires its
own authorization, implementation, independent review, acceptance and canonical
adoption. Atomic publication and write-path protections form one cohesive
filesystem-publication boundary and must not be implemented as independent,
partially operable production surfaces. The allocation correction must be
accepted before publication work may be authorized, and publication-boundary
acceptance must precede final P01-04B requalification. No increment is named
P01-04B2E because P01-04E is an existing official downstream stage.

Prospective implementation authority recorded as FD-BMD-1 through FD-BMD-14:
The correction stays private and library-only, and
SourceDocumentGroupedSplitter.assign remains unconditionally fail-closed. The
accepted exact allocator allocate_indivisible_groups is preserved, not replaced,
and every currently successful exact-feasible request must retain byte-identical
assignments, registries, summaries, hashes and fingerprints. One private typed
SplitAllocationError subclass, raised only at the ranked-boundary crossing, is
the sole fallback trigger; no fallback may depend on parsing an exception
message. One private exact-first/minimum-deviation resolver is authorized. The
objective is the integer sum of squared deviations over the nine cells ordered
yes/train, yes/validation, yes/test, no/train, no/validation, no/test,
maybe/train, maybe/validation, maybe/test, with no floating point, no tolerance
and no heuristic, and the selected result must be a proven global minimum. Ties
break first to the lexicographically smallest nine-cell matrix, then to the
lexicographically smallest partition-code vector using decision order yes, no,
maybe, the existing rank_groups ordering within each decision, and codes
train = 0, validation = 1, test = 2. The search must be a complete deterministic
reachable-state dynamic program, bounded to 1000 examples, 1000 source-document
groups, 3 decisions and 3 partitions, failing closed beyond that boundary.

Required corrected result:
constraint-stress-1000-v1 with 1000 rows, 500 groups of size 2 and target matrix
386,83,83,237,50,51,77,17,16 has an INFEASIBLE exact target, a global minimum
squared-deviation score of 6, exactly 2 minimum-score matrices, selected matrix
386,82,84,238,50,50,76,18,16 and runner-up 386,84,82,236,50,52,78,16,16. It must
then produce a successful deterministic in-memory FixtureSplitResult with frozen
literal goldens. exact-reference-1000-v1 and leakage-positive-v1 must remain
byte-identical, and ALGORITHM_VERSION, SPLIT_SEED and every canonical
serialization, artifact, leakage, fixture-identity and request-identity schema
version must be unchanged.

Future implementation identity:
Branch fix/mesc-p01-04b-minimum-deviation; subject
"fix(mesc): implement P01-04B minimum-deviation allocation"; exactly four paths,
being src/medscale/mesc/_split_v1.py, src/medscale/mesc/_fixture_split_v1.py,
tests/test_mesc_split_v1.py and tests/test_mesc_p01_04b2d_qualification_v1.py.
No fifth path. tests/_mesc_p01_04b2d_fixtures_v1.py,
.github/workflows/mesc-p01-04b2d-qualification.yml, src/medscale/mesc/split.py,
pyproject.toml and uv.lock remain byte-identical, and no workflow edit is
authorized; the existing qualification workflow triggers automatically through
its existing path filters.

Post-correction qualification disposition:
The indivisible-group global minimum-deviation capability becomes SATISFIED,
while atomic publication and write-path protections remain NOT SATISFIED FOR
P01-04B OVERALL, P01-04B acceptance eligibility remains FALSE and P01-04B remains
CHANGES REQUIRED / NOT ACCEPTED. Historical governance documents that truthfully
record the pre-correction UNSATISFIED result are not rewritten, and a successful
correction does not retroactively make those records false.

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B18 was recorded, before FD-BR-1 and
FD-BMD-1 through FD-BMD-14 were adopted on canonical main through PR #80, before
the minimum-deviation implementation was merged through PR #81, and before
FD-BPUB-1 through FD-BPUB-18 were issued. It is retained as historical governance
evidence and is not the repository's present controlling state. The later
P01-T03B19 Current controlling state supersedes this block.

P01-T03B17 documentation:
ADOPTED ON CANONICAL MAIN

PR #79:
MERGED AND MECHANICALLY VERIFIED AS
3513d66bc36650363a6368bb4e42901119419802

FD-B2D-15:
ADOPTED ON CANONICAL MAIN

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

P01-04B2D:
ACCEPTED

FD-BR-1:
FOUNDER DECISION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B18

FD-BMD-1 through FD-BMD-14:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN; see P01-T03B18

Minimum-deviation implementation authority:
RECORDED BUT INACTIVE

Minimum-deviation implementation:
NOT AUTHORIZED TO BEGIN

Indivisible-group global minimum-deviation allocation:
UNSATISFIED

Atomic publication:
NOT SATISFIED FOR P01-04B OVERALL; IMPLEMENTATION NOT AUTHORIZED

Write-path protections:
NOT SATISFIED FOR P01-04B OVERALL; IMPLEMENTATION NOT AUTHORIZED

P01-04B acceptance eligibility:
FALSE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, automatic finding discovery, CLI, public export, filesystem
publication, promotion of any B2D output, P01-03G or real dataset access,
B0/B1 execution, model access, inference, retrieval, metrics, benchmark
execution, training, fine-tuning, adapter creation, publication and clinical
use:
NOT AUTHORIZED

--- Future gated authority ---

FD-BR-1 and FD-BMD-1 through FD-BMD-14:
RECORDED BUT NOT YET ADOPTED — canonical adoption and activation require all
five conditions: a genuinely independent clean-room exact-head review of this
authorization package, a separate Founder Ready decision, a separate Founder
Merge decision, merge into canonical main, and mechanical post-merge
verification. NO SUBSET ACTIVATES IMPLEMENTATION AUTHORITY.

Minimum-deviation implementation:
AFTER ADOPTION ONLY — ONE BRANCH, ONE NORMAL COMMIT, FOUR PATHS, ONE BOUNDED
ATTEMPT. THE AUTHORITY IS SPENT WHEN THE IMPLEMENTATION COMMIT IS CREATED. A
DEFECT AFTER COMMIT REQUIRES STOP, REPORT, NO AMEND, NO SECOND COMMIT AND A
SEPARATE FOUNDER CORRECTION AUTHORIZATION. IMPLEMENTATION MERGE DOES NOT EQUAL
IMPLEMENTATION ACCEPTANCE

Atomic-publication and write-path boundary:
ELIGIBLE FOR A SEPARATE FOUNDER CONSIDERATION ONLY AFTER THE MINIMUM-DEVIATION
IMPLEMENTATION IS SEPARATELY ACCEPTED. ELIGIBILITY IS NEVER AUTHORITY

P01-04B:
REMAINS CHANGES REQUIRED / NOT ACCEPTED UNTIL ALL THREE GAPS ARE CLOSED AND A
SEPARATE INTEGRATED REQUALIFICATION AND ACCEPTANCE DISPOSITION IS ADOPTED

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Prerequisite:
P01-T03B17 ADOPTED (PR #79 merge 3513d66b...) AND FD-B2D-15 ADOPTED;
P01-04B2D ACCEPTED

Scope:
Record the founder's P01-04B recovery architecture as FD-BR-1 and the bounded
prospective minimum-deviation correction authority as FD-BMD-1 through
FD-BMD-14, together with the exact canonical baseline, the accepted B2D
identity, the three remaining P01-04B gaps, the four-path future implementation
allowlist, the exact integer objective, the nine-cell matrix order, both
tie-break rules, the complete deterministic search requirement, the
constraint-stress expected result, the exact-feasible byte non-regression
requirement, the five activation conditions, the one-attempt authority, the
pre-adoption and post-adoption states and the continuing prohibitions. This gate
implements nothing, executes nothing, corrects nothing, promotes nothing, and
authorizes no downstream phase. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04/, specs/mesc-pilot-01/p01-04b2/,
specs/mesc-pilot-01/p01-04b2a/, specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/,
specs/mesc-pilot-01/p01-04b2b-acceptance/,
specs/mesc-pilot-01/p01-04b2c-authorization/,
specs/mesc-pilot-01/p01-04b2c-acceptance/,
specs/mesc-pilot-01/p01-04b2d-authorization/ and
specs/mesc-pilot-01/p01-04b2d-acceptance/ and is not restated.
```

```text
P01-T03B19 — Authorize P01-04B atomic publication and write-path protection
boundary

Documentation status:
RECORDED — NOT ADOPTED

FD-BPUB-1 through FD-BPUB-18:
ISSUED — NOT YET ADOPTED

Publication-boundary implementation authority:
RECORDED BUT INACTIVE

Minimum-deviation capability:
SATISFIED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Atomic publication:
NOT SATISFIED / NOT IMPLEMENTATION-AUTHORIZED

Write-path protections:
NOT SATISFIED / NOT IMPLEMENTATION-AUTHORIZED

P01-04C through P01-04G:
NOT AUTHORIZED

Required canonical baseline:
1e8b78379ee4af0c2870a5388001f528ae977221
(tree 0dba04f0baf8107e5b52e0f5f5f1b7014c818ced;
ordered parents 70bf280fccff4d9f4ecc24839dd9f7597c18e489 THEN
97bec19bca47933bd6f81cf482f668779f9a8298;
subject "Merge pull request #81 from IamShehri/fix/mesc-p01-04b-minimum-deviation";
body "fix(mesc): implement P01-04B minimum-deviation allocation")

Chronological completion of P01-T03B18:
P01-04B minimum-deviation authorization package: PR #80.
Reviewed package head: 823ca6d5a46ac9f6ec317c2f9f320ee7dcc4cf21.
Canonical authorization merge: 70bf280fccff4d9f4ecc24839dd9f7597c18e489.
FD-BR-1: ADOPTED ON CANONICAL MAIN.
FD-BMD-1 through FD-BMD-14: ADOPTED ON CANONICAL MAIN.
Minimum-deviation implementation authority: ACTIVATED, EXERCISED EXACTLY ONCE,
AND SPENT.

Accepted minimum-deviation implementation identity:
PR #81 on branch fix/mesc-p01-04b-minimum-deviation.
Reviewed and merged head: 97bec19bca47933bd6f81cf482f668779f9a8298.
Reviewed implementation tree: 0dba04f0baf8107e5b52e0f5f5f1b7014c818ced.
Implementation parent: 70bf280fccff4d9f4ecc24839dd9f7597c18e489.
Canonical implementation merge: 1e8b78379ee4af0c2870a5388001f528ae977221.
1 commit / 4 files / 1539 additions / 68 deletions, being exactly
src/medscale/mesc/_split_v1.py blob
f755771b68ef80c895f98f529c1b708716458673, src/medscale/mesc/_fixture_split_v1.py
blob 1e73ddf2c9e7def247d5d88d20ae013458528edc, tests/test_mesc_split_v1.py blob
2f38d7a34f6ab785f0a129beb33482850e156d95 and
tests/test_mesc_p01_04b2d_qualification_v1.py blob
ffc776cfbcdf39f8f1ab6072a4609a4ccb6284e6. No path was added or deleted, and no
workflow, dependency, lockfile, public export, CLI or entry point was changed.

Implementation disposition:
Independent clean-room exact-head implementation review: COMPLETED. The reviewed
head was published, opened as a Draft pull request, taken Ready through a
separate founder decision and merged through a separate founder decision.
Mechanical post-merge verification: PERFORMED. Founder acceptance of the
minimum-deviation implementation: GRANTED. The indivisible-group global
minimum-deviation allocation capability is therefore SATISFIED. Implementation
merge is not implementation acceptance, and implementation acceptance is not
P01-04B acceptance. The founder acceptance recorded here is an explicit founder
decision; there is no separate canonically adopted minimum-deviation acceptance
package at this baseline, and none is claimed. Historical governance documents
that truthfully record the pre-correction UNSATISFIED result are not rewritten.

FD-BR-1 recovery position:
Step 1 global minimum-deviation grouped allocation correction: COMPLETE.
Step 2 atomic publication and write-path protection boundary: NEXT — the subject
of this task. Step 3 integrated P01-04B requalification and acceptance
disposition: NOT YET ELIGIBLE.

Prospective implementation authority recorded as FD-BPUB-1 through FD-BPUB-18:
FD-BPUB-1 atomic publication and write-path protection are one cohesive
capability that must never be independently implemented, activated, accepted,
exported or made partially operable. FD-BPUB-2 the future publisher is private,
unexported, library-only, fixture-only, synthetic-only and non-evidence, with no
CLI and no public API; it must not make SourceDocumentGroupedSplitter.assign
executable, and it creates no real split, canonical dataset partition, research
artifact, clinical artifact or admissible evidence. FD-BPUB-3 it consumes only
exact FixtureSplitRequest and FixtureSplitResult instances plus one explicit
absolute publication-parent pathlib.Path and one exact tuple of protected roots,
with no mapping, string, duck-typed object, implicit path, environment default,
URL, file handle, generator, iterator or adapter, and the request/result binding
is completely verified before mutation. FD-BPUB-4 freezes the fail-closed
publication-parent and protected-root rules, full two-way disjointness, direct
one-component child names, and canonical filesystem identity that fails closed
when identity cannot be established. FD-BPUB-5 fixes the final directory name
mesc-p01-04b-split-<split_fingerprint> and the staging directory name
.mesc-p01-04b-split-<split_fingerprint>.staging, derived only from the verified
lowercase 64-hex authoritative split fingerprint, with the literal -split-
component mandatory and no clock, timestamp, PID, hostname, username,
randomness, UUID, retry counter, environment value or caller suffix.

FD-BPUB-6 fixes the exact seven-file inventory: group-registry.jsonl,
example-registry.jsonl, excluded-ledger.json, split-summary-identity-core.json,
split-summary.json and leakage-audit.json bound respectively to
result.group_registry_bytes, result.example_registry_bytes,
result.excluded_ledger_bytes, result.split_summary_identity_core_bytes,
result.split_summary_document_bytes and result.audit_report_bytes, plus exactly
one publication-manifest.json. The leakage audit filename is exactly
leakage-audit.json; a -report infix variant of that filename is prohibited, as
are a compatibility manifest file, request dump, pickle, log, marker, checksum
sidecar, receipt file, lock file, temp file, README and any eighth file.
FD-BPUB-7 fixes the non-circular publication manifest at schema
mesc-pilot-01-fixture-publication-manifest/1 with exactly five top-level members
schema_version, request_id, split_fingerprint, publication_directory_name and
files; publication_directory_name is the final directory basename and never an
absolute path; files holds exactly six records ordered by ascending filename,
each with exactly four members filename, surface, sha256 and byte_size; the six
surface identifiers are exactly group_registry, example_registry,
excluded_ledger, split_summary_identity_core, split_summary_document and
leakage_audit. The manifest describes only the six payload files, carries no
digest or size of itself, and carries no fixture_only, non_evidence, fixture_id,
synthetic_identity_proof, split_hash, execution_evidence_ref, per-record
schema_version, absolute path, protected root, date, time, timestamp, runtime,
host, user or repository metadata and no clinical, research or
evidence-promotion claim. Serialization uses the accepted canonical JSON
serializer with its accepted terminal-LF behaviour preserved, and descriptor
schemas are not inferred from ARTIFACT_SCHEMA_VERSIONS for this manifest: the
exact per-file field is surface, not schema_version.

FD-BPUB-8 requires the complete verified plan — input types, request/result
identity binding, authoritative fingerprint, fingerprint record, artifact
descriptors where present, six exact byte surfaces, six recomputed digests, six
recomputed byte sizes, the six-payload plan, the exact canonical manifest bytes,
filename uniqueness, the exact seven-name inventory, directory names, parent and
protected-root safety, staging absence, final absence and availability of a
supported atomic no-replace rename primitive — to be built and frozen immutably
before the first filesystem mutation, with no planning or canonical-byte
construction after attempt acquisition and no invented descriptor requirement
for byte surfaces the accepted fingerprint record does not describe. FD-BPUB-9
acquires one attempt only through exclusive creation of the deterministic
staging directory as a direct child of the publication parent, writing no
payload file if that creation fails and deriving no alternate staging name.
FD-BPUB-10 writes all seven files exactly once, binary, exclusively, with no
append, truncation, overwrite, temporary sibling, individual-file rename, reopen
for modification or partial rewrite, using no-follow and exclusive facilities
where available and failing closed otherwise. FD-BPUB-11 writes the six payload
files first in exact ascending filename order and publication-manifest.json
last, and staging is never accepted or final merely because the manifest exists
there.

FD-BPUB-12 requires, immediately after every write, a language-level buffer
flush, a supported file synchronization primitive such as os.fsync or a
platform equivalent, close, reopen read-only without following an indirection,
and verification of exact bytes, SHA-256, byte size and regular-file type; the
contract guarantees atomic namespace visibility only and claims no universal
power-loss, storage-controller, filesystem-journal or directory-entry
durability. FD-BPUB-13 requires the complete pre-rename inventory to be
enumerated from the filesystem and verified as exactly seven entries with
exactly the seven expected names, all regular files, with no directory, symlink,
junction, reparse indirection, socket, FIFO, device, missing file, duplicate,
unexpected entry or alternate filename, all seven contents reverified, and the
manifest confirmed to describe exactly the six payload files with matching
request_id, split_fingerprint and publication_directory_name; hard-link
substitution is detected and rejected where the platform exposes reliable
identity or link-count information, and universal hard-link detection is not
claimed where the platform cannot prove it. FD-BPUB-14 publishes through exactly
one same-parent staging-directory-to-final-directory rename with atomic
directory namespace visibility and a destination that must not exist, with no
replace-existing behaviour, merge, copy fallback, cross-device fallback,
recursive move or per-file publication; os.replace is prohibited, a destination
precheck does not provide no-replace semantics, a plain os.rename is authorized
only where that exact primitive guarantees atomic no-replace behaviour for this
directory rename, otherwise a private supported atomic no-replace primitive is
used or the typed unsupported-atomic-rename error is raised before attempt
acquisition, and "precheck, rename and postcheck" is not authorized as a
substitute.

FD-BPUB-15 preserves staging exactly as left after any post-creation failure,
with no deletion, cleanup, retry, resume, repair, alternate name, overwrite or
final rename, and later recovery is outside this authorization. FD-BPUB-16
requires post-rename verification that staging no longer exists, that final
exists under the exact FD-BPUB-5 name as a real directory and not an
indirection, that parent identity matches, that the seven-entry inventory holds,
and that all seven files and the manifest bindings are reread and reverified;
failure raises a typed post-rename verification error and leaves the visible
final directory untouched, with no rollback, cleanup, replacement or repair.
FD-BPUB-17 returns, only after successful post-rename verification, one private
frozen slotted runtime receipt with fields equivalent to exactly
publication_directory (pathlib.Path), request_id (str), split_fingerprint (str),
publication_manifest_sha256 (str) and published_filenames (tuple[str, ...]); the
names final_directory and publication_manifest_bytes must not be used as
substitutes for the selected fields; published_filenames is the exact ascending
seven-file inventory; the receipt is not written, is not canonical evidence, is
not exported, contains no timestamp and no clinical or research claim, does not
promote the fixture result, and is never returned on failure. FD-BPUB-18
authorizes one private base publication error with narrowly typed categories
covering at least invalid input or identity binding, unsafe or protected path,
existing staging or final conflict, unsupported atomic no-replace rename,
exclusive staging creation failure, exclusive file creation or write failure,
content verification failure, inventory verification failure, final rename
failure and post-rename verification failure, preserving accepted upstream typed
exceptions where that gives more precise attribution, with no message parsing
for exception dispatch, and continues the prohibitions on public export, CLI,
environment switch, network, subprocess, clock, randomness, real-data adapter,
evidence-root promotion, repository-root promotion, source-tree publication,
dataset-registry publication, model or weight access, inference, retrieval,
training, fine-tuning, real split execution, real partition membership,
canonical leakage execution, P01-04B acceptance and P01-04C through P01-04G.

Exact activation sequence:
Publication-boundary implementation authority remains inactive until all nine
conditions occur: 1 independent clean-room exact-head documentation review;
2 exact reviewed head pushed; 3 Draft PR opened from that exact head; 4 CI and
CodeQL verified at that exact head; 5 separate Founder Ready decision;
6 separate Founder Merge decision; 7 merge-commit adoption on canonical main;
8 mechanical post-merge verification; 9 separate explicit founder activation of
the implementation gate. The first eight establish canonical adoption and
eligibility only and do not activate implementation. Condition nine remains
separately required. NO SEVEN-CONDITION SUBSTITUTE. NO GROUPED OR IMPLIED
SUBSTITUTE. NO SUBSET ACTIVATES AUTHORITY.

Future implementation identity:
Branch feat/mesc-p01-04b-publication-boundary; subject
"feat(mesc): implement P01-04B publication boundary"; exactly four paths, being
src/medscale/mesc/_fixture_publication_v1.py,
tests/test_mesc_fixture_publication_v1.py,
tests/test_mesc_p01_04b_publication_qualification_v1.py and
.github/workflows/mesc-p01-04b-publication-qualification.yml. No fifth path.
src/medscale/mesc/__init__.py, src/medscale/mesc/split.py,
src/medscale/mesc/_split_v1.py, src/medscale/mesc/_fixture_split_v1.py,
src/medscale/mesc/_canonical_json_v1.py,
src/medscale/mesc/_split_artifacts_v1.py, src/medscale/mesc/_leakage_v1.py,
tests/_mesc_p01_04b2d_fixtures_v1.py, pyproject.toml, uv.lock and every prior
governance package remain byte-identical.

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B19 was recorded, before FD-BPUB-1
through FD-BPUB-18 were adopted on canonical main through PR #82, before the
publication-boundary implementation was merged through PR #83, and before the
founder issued the P01-04B acceptance disposition. It is retained as historical
governance evidence and is not the repository's present controlling state. The
later P01-T03B20 Current controlling state supersedes this block.

P01-T03B18 documentation:
ADOPTED ON CANONICAL MAIN

PR #80:
MERGED AND MECHANICALLY VERIFIED AS
70bf280fccff4d9f4ecc24839dd9f7597c18e489

FD-BR-1:
ADOPTED ON CANONICAL MAIN

FD-BMD-1 through FD-BMD-14:
ADOPTED ON CANONICAL MAIN

PR #81:
MERGED AND MECHANICALLY VERIFIED AS
1e8b78379ee4af0c2870a5388001f528ae977221

Minimum-deviation implementation:
BUILT, INDEPENDENTLY REVIEWED, PUBLISHED, READY, MERGED, MECHANICALLY VERIFIED
AND FOUNDER-ACCEPTED

Minimum-deviation implementation authority:
ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT

MINIMUM-DEVIATION CAPABILITY:
SATISFIED

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

P01-04B2D:
ACCEPTED

FD-BPUB-1 THROUGH FD-BPUB-18:
ISSUED — NOT YET ADOPTED

PUBLICATION-BOUNDARY IMPLEMENTATION AUTHORITY:
RECORDED BUT INACTIVE

ATOMIC PUBLICATION:
NOT YET IMPLEMENTED

WRITE-PATH PROTECTIONS:
NOT YET IMPLEMENTED

P01-04B acceptance eligibility:
FALSE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

REAL EXECUTION:
NOT AUTHORIZED

P01-04C THROUGH P01-04G:
NOT AUTHORIZED

Real split execution, real partition membership, canonical leakage execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, CLI, public export, filesystem publication, promotion of any fixture
output, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
adapter creation, publication and clinical use:
NOT AUTHORIZED

--- Future gated authority ---

FD-BPUB-1 through FD-BPUB-18:
RECORDED BUT NOT YET ADOPTED — canonical adoption requires activation conditions
one through eight, and activation of implementation authority additionally
requires condition nine, the separate explicit founder activation of the
implementation gate. NO SUBSET ACTIVATES IMPLEMENTATION AUTHORITY.

Publication-boundary implementation:
AFTER ADOPTION AND CONDITION NINE ONLY — ONE BRANCH, ONE NORMAL COMMIT, FOUR
PATHS, ONE BOUNDED ATTEMPT. THE AUTHORITY IS SPENT WHEN THE IMPLEMENTATION
COMMIT IS CREATED. A DEFECT AFTER COMMIT REQUIRES STOP, REPORT, NO AMEND, NO
SECOND COMMIT AND A SEPARATE FOUNDER CORRECTION AUTHORIZATION. IMPLEMENTATION
MERGE DOES NOT EQUAL IMPLEMENTATION ACCEPTANCE

Integrated P01-04B requalification and acceptance disposition:
FD-BR-1 STEP 3 — NOT YET ELIGIBLE. IT BECOMES ELIGIBLE FOR A SEPARATE FOUNDER
CONSIDERATION ONLY AFTER THE PUBLICATION BOUNDARY IS SEPARATELY IMPLEMENTED,
INDEPENDENTLY REVIEWED, ADOPTED AND ACCEPTED. ELIGIBILITY IS NEVER AUTHORITY

P01-04B:
REMAINS CHANGES REQUIRED / NOT ACCEPTED UNTIL THE PUBLICATION BOUNDARY IS
CLOSED AND A SEPARATE INTEGRATED REQUALIFICATION AND ACCEPTANCE DISPOSITION IS
ADOPTED

Independent exact-head review of this governance package:
OUTSTANDING — REQUIRED BEFORE READY OR MERGE

Prerequisite:
P01-T03B18 ADOPTED (PR #80 merge 70bf280f...) AND FD-BR-1 AND FD-BMD-1 THROUGH
FD-BMD-14 ADOPTED; MINIMUM-DEVIATION IMPLEMENTATION MERGED (PR #81 merge
1e8b7837...), MECHANICALLY VERIFIED AND FOUNDER-ACCEPTED; MINIMUM-DEVIATION
CAPABILITY SATISFIED

Scope:
Record the founder's bounded prospective authority for the P01-04B atomic
publication and write-path protection boundary as FD-BPUB-1 through FD-BPUB-18,
together with the exact canonical baseline, the PR #80 adoption and PR #81
implementation identity, the founder acceptance of the minimum-deviation
implementation and the resulting SATISFIED capability, the FD-BR-1 recovery
position, the private fixture-only boundary, the exact object and path inputs,
the publication-parent and protected-root rules, the exact directory names with
the mandatory -split- component, the exact seven-file inventory and six byte
bindings, the exact five-member non-circular manifest with four-member
surface-keyed file records, the plan-before-mutation requirement, the
one-attempt acquisition, the exact-once exclusive writes, the manifest-last
ordering, the bounded durability claim, the filesystem-derived inventory, the
atomic no-replace rename requirement, the failure-preservation rule, the
post-rename verification, the exact five-field private receipt, the typed error
taxonomy, the four-path future implementation allowlist, the exact nine-condition
activation sequence and the continuing prohibitions. This gate implements
nothing, executes nothing, publishes nothing, promotes nothing, and authorizes no
downstream phase. Prior governance history is adopted at
specs/mesc-pilot-01/p01-04/, specs/mesc-pilot-01/p01-04b2/,
specs/mesc-pilot-01/p01-04b2a/, specs/mesc-pilot-01/p01-04b2a-acceptance/,
specs/mesc-pilot-01/p01-04b2b-authorization/,
specs/mesc-pilot-01/p01-04b2b-acceptance/,
specs/mesc-pilot-01/p01-04b2c-authorization/,
specs/mesc-pilot-01/p01-04b2c-acceptance/,
specs/mesc-pilot-01/p01-04b2d-authorization/,
specs/mesc-pilot-01/p01-04b2d-acceptance/ and
specs/mesc-pilot-01/p01-04b-min-deviation-authorization/ and is not restated.
```

```text
P01-T03B20 — P01-04B acceptance closeout

Founder acceptance:
ISSUED ON 2026-08-04

Canonical implementation merge:
d5a6ac1654cabd33b6a795756d2796bceaf1652a

Merged PR:
#83

Reviewed correction head:
e78d1fca2d972cdbcdb7ff78bdf09af4cd03966f

Implementation status:
COMPLETED, ADOPTED AND ACCEPTED

Post-merge qualification:
ALL REQUIRED AND OPTIONAL RUNS SUCCESSFUL

Execution status:
NOT AUTHORIZED

Downstream status:
P01-04C NOT AUTHORIZED

Task-identifier note:
This block is numbered P01-T03B20. The identifier P01-T03B7 is already assigned
to the P01-04B2A portability governance-hold resolution gate recorded earlier in
this append-only ledger and adopted through PR #63, so it is not reused here.

Accepted canonical baseline:
d5a6ac1654cabd33b6a795756d2796bceaf1652a
(tree 0037f61ff4fba45fe4e5b2ed126f8bb2567d64b7;
ordered parents 24025f44cc7bdc8fd007616983630d825fc0b233 THEN
e78d1fca2d972cdbcdb7ff78bdf09af4cd03966f;
subject "Merge pull request #83 from IamShehri/feat/mesc-p01-04b-publication-boundary";
body "feat(mesc): implement P01-04B publication boundary";
merge timestamp 2026-08-04T01:41:46Z)

Accepted implementation identity:
Original implementation commit cb73b94b87880f49a220a15a2d4a24412c7d0d0b.
Reviewed correction head e78d1fca2d972cdbcdb7ff78bdf09af4cd03966f.
Adopted through PR #83 as a merge commit.

First-parent scope:
A .github/workflows/mesc-p01-04b-publication-qualification.yml
A src/medscale/mesc/_fixture_publication_v1.py
A tests/test_mesc_fixture_publication_v1.py
A tests/test_mesc_p01_04b_publication_qualification_v1.py
4 files changed, 2707 insertions, 0 deletions. No fifth path.

Accepted post-merge evidence:
CI run 30869536586, run number 260, SUCCESS;
quality (py3.11) SUCCESS; quality (py3.12) SUCCESS.
CodeQL run 30869536582, run number 264, SUCCESS;
analyze (python) SUCCESS.
MESC P01-04B Publication Qualification run 30869536588, run number 3, SUCCESS;
Ubuntu Python 3.11 SUCCESS; Ubuntu Python 3.12 SUCCESS;
Windows Python 3.11 SUCCESS; Windows Python 3.12 SUCCESS;
macOS Python 3.11 SUCCESS; macOS Python 3.12 SUCCESS.
Optional Extras / Backends run 30869536570, run number 85, SUCCESS;
core-without-backends SUCCESS; backends-transformers SUCCESS;
backends-llamacpp SUCCESS.
No workflow was rerun, manually dispatched or cancelled.

Acceptance criterion mapping:
1 public SourceDocumentGroupedSplitter remains fail-closed SATISFIED;
2 separate private FixtureSplitFacade SATISFIED;
3 library-only in-memory execution path SATISFIED;
4 no formal CLI SATISFIED;
5 full 64-hex split_fingerprint authoritative SATISFIED;
6 16-hex split_hash compatibility and display only SATISFIED;
7 FD-B2-6 leakage normalization SATISFIED;
8 three accepted synthetic qualification fixtures SATISFIED;
9 deterministic byte-identical supported-runtime qualification SATISFIED;
10 no real P01-03G membership generated or disclosed SATISFIED.
The three accepted synthetic fixtures are exactly exact-reference-1000-v1,
constraint-stress-1000-v1 and leakage-positive-v1.

Scope:
Record the founder's P01-04B acceptance closeout against the exact canonical
merge baseline, the accepted implementation identity, the first-parent scope and
statistics, the post-merge CI, CodeQL, cross-platform qualification and optional
backend evidence, and the individual mapping of all ten acceptance criteria.
This gate implements nothing, executes nothing, publishes nothing, promotes
nothing and authorizes no downstream phase. It records tooling acceptance only.

--- Current controlling state ---

HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED.

This was the controlling state when P01-T03B20 was recorded, before the P01-04B
acceptance closeout was adopted on canonical main through PR #84 and before the
founder issued the P01-04C synthetic fixture-qualification authorization. It is
retained as historical governance evidence and is not the repository's present
controlling state. The later P01-T03C1 Current controlling state supersedes this
block.

P01-T03B19 documentation:
ADOPTED ON CANONICAL MAIN

FD-BPUB-1 THROUGH FD-BPUB-18:
ADOPTED ON CANONICAL MAIN

PR #82:
MERGED AND MECHANICALLY VERIFIED AS
24025f44cc7bdc8fd007616983630d825fc0b233

PUBLICATION-BOUNDARY IMPLEMENTATION AUTHORITY:
ACTIVATED, EXERCISED EXACTLY ONCE, AND SPENT

Publication-boundary implementation:
BUILT, INDEPENDENTLY REVIEWED, CORRECTED, INDEPENDENTLY REVIEWED, PUBLISHED,
READY, MERGED, MECHANICALLY VERIFIED AND FOUNDER-ACCEPTED

PR #83:
MERGED AND MECHANICALLY VERIFIED AS
d5a6ac1654cabd33b6a795756d2796bceaf1652a

ATOMIC PUBLICATION:
IMPLEMENTED, QUALIFIED AND ACCEPTED

WRITE-PATH PROTECTIONS:
IMPLEMENTED, QUALIFIED AND ACCEPTED

MINIMUM-DEVIATION CAPABILITY:
SATISFIED

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

P01-04B2D:
ACCEPTED

P01-04B acceptance eligibility:
TRUE

P01-04B TOOLING:
ACCEPTED

P01-04B:
ACCEPTED

REAL EXECUTION:
NOT AUTHORIZED

P01-04C:
NOT AUTHORIZED

P01-04D THROUGH P01-04G:
NOT AUTHORIZED

Real split execution, real partition membership, canonical leakage execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, CLI, public export, filesystem publication, promotion of any fixture
output, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
adapter creation, publication and clinical use:
NOT AUTHORIZED

P01-04B acceptance is tooling acceptance only. It is never permission to run
P01-04C, P01-04D or any later stage. No real split exists, no real partition
membership exists, no real labels were processed, no canonical leakage was
executed and no evidence was published. P01-04 overall is not complete and
P01-05 is not unlocked.
```

```text
P01-T03C1 — P01-04C synthetic fixture qualification

HISTORICAL CANDIDATE-BUILD RECORD — SUPERSEDED FOR CURRENT STATUS.
Every field below was true when the candidate was built and is preserved
unrewritten. The later P01-T03C2 block records the current status: the candidate
was independently reviewed, merged through PR #85 and founder-accepted.

Founder authorization:
ISSUED ON 2026-08-04

Prerequisite:
P01-04B COMPLETED, ADOPTED AND ACCEPTED

Qualification status:
BUILT LOCALLY / ACCEPTANCE PENDING

Authorized data:
SYNTHETIC FIXTURES ONLY

Edge-case semantics:
EMPTY EXPECTED FAIL-CLOSED
SINGLE-EXAMPLE EXPECTED SUCCESS
ALL-ONE-LABEL EXPECTED SUCCESS

Real dataset access:
NOT AUTHORIZED

Real partition membership:
NOT AUTHORIZED

P01-04D:
NOT AUTHORIZED

Required canonical baseline:
78cb1004b15c4ff4daa25895e4bbec99c4bb4eae
(tree f01a6b44b85f5e8964e26b3c8940b1de369cc1b8;
ordered parents d5a6ac1654cabd33b6a795756d2796bceaf1652a THEN
e2d4308e4fdc99c206f62cf6b6a78ea6ed14c60b;
subject "Merge pull request #84 from IamShehri/docs/mesc-p01-04b-acceptance-closeout";
body "docs(mesc): record P01-04B acceptance closeout")

Candidate branch:
test/mesc-p01-04c-fixture-qualification

Candidate commit identity:
Recorded outside this block. The candidate is exactly one commit whose parent is
the canonical baseline above, carrying exactly four paths. Its SHA is reported in
the build report and in the independent review request, never written inside the
content it would have to hash.

Exact four-path scope:
A tests/test_mesc_p01_04c_fixture_qualification_v1.py
A specs/mesc-pilot-01/p01-04c-fixture-qualification/qualification-record.md
M specs/mesc-pilot-01/plan.md
M specs/mesc-pilot-01/tasks.md
No fifth path. No source, existing test, workflow, dependency or lockfile change.

Qualification fixtures:
p01-04c-small-20-v1, twenty single-example source documents, decisions yes 8 /
no 7 / maybe 5 assigned by row ordinal 00-07 yes, 08-14 no, 15-19 maybe,
partition totals train 14 / validation 3 / test 3.
p01-04c-single-example-v1, one example, one source document, decision yes,
partition totals train 1 / validation 0 / test 0.
p01-04c-all-one-label-20-v1, twenty single-example source documents, decision
yes for every example, partition totals train 14 / validation 3 / test 3.
Empty input carries zero rows, zero source labels and zero partition totals and
is expected to fail closed with InvalidFixtureRequestError.

Canonical acceptance criteria addressed:
C1 dedicated fixture tests pass for deterministic synthetic small input.
C2 every successful fixture is byte-identical across three fresh runs.
C3 empty, single-example and all-one-label edge cases pass under the ratified
semantics above.
C4 no real dataset partition membership is generated.

Scope:
Record the founder-authorized P01-04C synthetic fixture-qualification candidate
over the accepted and canonically adopted P01-04B tooling. This gate constructs
and executes synthetic fixtures only. It accesses no real dataset, reads or
generates no P01-03G registry membership, generates no real split, executes no
canonical leakage audit, publishes no evidence, and authorizes no downstream
phase. Qualification evidence is never canonical evidence, research evidence or
real split evidence.

--- Historical controlling-state snapshot — SUPERSEDED ---

This was the controlling state when P01-T03C1 was recorded, before the P01-04C
qualification candidate was independently reviewed, published as PR #85, merged
onto canonical main and founder-accepted. Its facts remain truthful for that
point in the chronology and are preserved unrewritten. The later P01-T03C2
Current controlling state supersedes this block for all current status purposes.

P01-T03B20 documentation:
ADOPTED ON CANONICAL MAIN

PR #84:
MERGED AND MECHANICALLY VERIFIED AS
78cb1004b15c4ff4daa25895e4bbec99c4bb4eae

P01-04B:
ACCEPTED AND CANONICALLY ADOPTED

P01-04B TOOLING:
ACCEPTED

P01-04C SYNTHETIC QUALIFICATION AUTHORIZATION:
ISSUED ON 2026-08-04

P01-04C QUALIFICATION CANDIDATE:
BUILT AND EXECUTED LOCALLY

P01-04C independent review:
OUTSTANDING — REQUIRED BEFORE PUBLICATION OR ACCEPTANCE

P01-04C ACCEPTANCE:
NOT ISSUED

CANONICAL ADOPTION OF THE CANDIDATE:
NOT ACHIEVED

REAL DATASET ACCESS:
NOT AUTHORIZED

REAL SPLIT EXECUTION:
NOT AUTHORIZED

REAL PARTITION MEMBERSHIP:
NOT AUTHORIZED

CANONICAL LEAKAGE EXECUTION:
NOT AUTHORIZED

P01-04D:
NOT AUTHORIZED

P01-04E THROUGH P01-04G:
NOT AUTHORIZED

Real split execution, real partition membership, canonical leakage execution,
leakage-audit orchestration, dataset scanning, registry scanning, record-pair
discovery, CLI, public export, filesystem publication, promotion of any fixture
output, P01-03G or real dataset access, B0/B1 execution, model access,
inference, retrieval, metrics, benchmark execution, training, fine-tuning,
adapter creation, publication and clinical use:
NOT AUTHORIZED

A passing synthetic qualification candidate is not P01-04C acceptance. No real
split exists, no real partition membership exists, no real labels were
processed, no canonical leakage was executed and no evidence was published.
P01-04 overall is not complete and P01-05 is not unlocked.
```

```text
P01-T03C2 — P01-04C acceptance closeout

Founder P01-04C acceptance:
ISSUED ON 2026-08-04

Prerequisite:
P01-04C QUALIFICATION CANDIDATE MERGED AND POST-MERGE GREEN

Accepted canonical baseline:
b20dbe0000a129f3019d6f7d2895622ce0560069

Accepted reviewed head:
c9cf1cc58b3ff89c39327c328a10308c0a9dbf4d

Merged PR:
#85

P01-04C:
ACCEPTED

P01-04D:
NOT AUTHORIZED

Real dataset execution:
NOT AUTHORIZED

Accepted canonical baseline detail:
b20dbe0000a129f3019d6f7d2895622ce0560069
(tree 92e78e8020f655316b8b487deb199f444a0ec75f;
ordered parents 78cb1004b15c4ff4daa25895e4bbec99c4bb4eae THEN
c9cf1cc58b3ff89c39327c328a10308c0a9dbf4d;
subject "Merge pull request #85 from IamShehri/test/mesc-p01-04c-fixture-qualification";
body "test(mesc): qualify P01-04C synthetic fixtures")

Closeout branch:
docs/mesc-p01-04c-acceptance-closeout

Closeout commit identity:
Recorded outside this block. The closeout is exactly one commit whose parent is
the accepted canonical baseline above, carrying exactly five documentation
paths. Its SHA is reported in the build report and in the independent review
request, never written inside the content it would have to hash.

Exact five-path scope:
M specs/mesc-pilot-01/p01-04/acceptance.md
M specs/mesc-pilot-01/p01-04/decision-record.md
M specs/mesc-pilot-01/p01-04c-fixture-qualification/qualification-record.md
M specs/mesc-pilot-01/plan.md
M specs/mesc-pilot-01/tasks.md
No sixth path. No source, test, workflow, dependency or lockfile change.

Acceptance basis:
C1 SUPPORTED AND ACCEPTED — all dedicated P01-04C deterministic synthetic
fixture tests pass.
C2 SUPPORTED AND ACCEPTED — all successful fixture artifacts are byte-identical
across three fresh, semantically identical runs.
C3 SUPPORTED AND ACCEPTED — the ratified edge-case semantics pass: empty input
expected deterministic fail-closed, single-example input expected success,
all-one-label input expected success.
C4 SUPPORTED AND ACCEPTED — no real dataset partition membership was generated,
disclosed or accessed.

Accepted fixtures:
p01-04c-small-20-v1
p01-04c-single-example-v1
p01-04c-all-one-label-20-v1
empty-input deterministic fail-closed case

Accepted evidence:
Focused qualification suite 31 passed. Accepted predecessor suites 846 passed,
2 skipped. Canonical pull-request CI SUCCESS. Canonical pull-request CodeQL
SUCCESS. Post-merge CI run 30879121118, run number 264, SUCCESS, with
quality (py3.11) SUCCESS and quality (py3.12) SUCCESS. Post-merge CodeQL run
30879121116, run number 268, SUCCESS, with analyze (python) SUCCESS. Post-merge
Optional Extras / Backends run 30879121117, run number 87, SUCCESS, with
core-without-backends SUCCESS, backends-transformers SUCCESS and
backends-llamacpp SUCCESS.

Non-blocking review notes preserved:
F-01 the exact empty-input sanitized message is accepted implementation text
frozen as a deterministic behavioral surface, rather than a separately ratified
message-contract string. F-02 the builder host encountered a Windows
Application Control console-shim limitation for the medscale check wrapper; the
same exact wrapper succeeded and reported CLEAN in the independent clean-room
review and canonical CI. F-03 the independent Windows host reproduced 54
pre-existing tests/test_mesc_b2a_portability.py failures caused by WSL/bash path
mangling; the same failures reproduced on the canonical parent and the P01-04C
candidate changed no affected path. No source or test was modified to address
these notes.

Scope:
Record the founder's P01-04C acceptance closeout against the exact canonical
merge baseline, the accepted reviewed head, the four-criterion acceptance basis,
the accepted synthetic fixtures and the post-merge evidence. This gate
implements nothing, executes nothing, publishes nothing, promotes nothing and
authorizes no downstream phase. It accepts synthetic fixture qualification only.

--- Historical pre-merge controlling-state snapshot — SUPERSEDED ---

This block was accurate before PR #86 merged, when the P01-04C acceptance
closeout had been built locally but had not yet been adopted on canonical main.
It is preserved as historical truth and no historical field inside it has been
rewritten. The later P01-T03C3 Current controlling state supersedes this block
for all current status purposes.

P01-T03C1 documentation:
ADOPTED ON CANONICAL MAIN

PR #85:
MERGED AND MECHANICALLY VERIFIED AS
b20dbe0000a129f3019d6f7d2895622ce0560069

P01-04B:
ACCEPTED AND CANONICALLY ADOPTED

P01-04C SYNTHETIC QUALIFICATION:
ACCEPTED

P01-04C ACCEPTANCE:
ISSUED ON 2026-08-04

P01-04C CANONICAL ACCEPTANCE BASELINE:
b20dbe0000a129f3019d6f7d2895622ce0560069

P01-04C acceptance closeout:
BUILT LOCALLY / NOT YET CANONICALLY ADOPTED

P01-04D:
NOT AUTHORIZED

P01-04E THROUGH P01-04G:
NOT AUTHORIZED

REAL DATASET ACCESS:
NOT AUTHORIZED

REAL SPLIT EXECUTION:
NOT AUTHORIZED

REAL PARTITION MEMBERSHIP:
NOT AUTHORIZED

CANONICAL LEAKAGE EXECUTION:
NOT AUTHORIZED

P01-03G registry access, dataset scanning, registry scanning, record-pair
discovery, public export, filesystem publication, evidence publication, model
access, inference, retrieval, benchmark execution, training, fine-tuning,
adapter creation and clinical use:
NOT AUTHORIZED

P01-04C acceptance accepts synthetic fixture qualification only. No real split
exists, no real partition membership exists, no real labels were processed, no
canonical leakage was executed and no real evidence was published.
P01-04 overall is not complete.
P01-05 is not unlocked.
```

```text
P01-T03C3 — P01-04C post-merge canonical adoption reconciliation

Founder authorization:
ISSUED ON 2026-08-04

Prerequisite:
PR #86 MERGED AND ALL POST-MERGE CHECKS GREEN

Acceptance-closeout PR:
#86

Accepted closeout head:
c7b55fad1dc9213870608253f8055560b53264c6

Canonical merge commit:
fe2dc1e6fe65d4823655f6d958cf3307629623ec

Canonical merge tree:
b905d696609c9de9488cb10785d9fed8796752f3

P01-04C acceptance closeout:
CANONICALLY ADOPTED

P01-04C:
ACCEPTED AND CANONICALLY CLOSED

Canonical merge identity detail:
fe2dc1e6fe65d4823655f6d958cf3307629623ec
(tree b905d696609c9de9488cb10785d9fed8796752f3;
ordered parents b20dbe0000a129f3019d6f7d2895622ce0560069 THEN
c7b55fad1dc9213870608253f8055560b53264c6;
subject "Merge pull request #86 from IamShehri/docs/mesc-p01-04c-acceptance-closeout";
body "docs(mesc): record P01-04C acceptance closeout")

Reconciliation branch:
docs/mesc-p01-04c-post-merge-truth-reconciliation

Reconciliation commit identity:
Recorded outside this block. The reconciliation is exactly one commit whose
parent is the canonical merge commit above, carrying exactly two documentation
paths. Its SHA is reported in the build report and in the independent review
request, never written inside the content it would have to hash.

Exact two-path scope:
A specs/mesc-pilot-01/p01-04c-fixture-qualification/canonical-adoption-record.md
M specs/mesc-pilot-01/tasks.md
No third path. No source, test, workflow, dependency or lockfile change.

Post-merge evidence:
Post-merge CI run 30914968296, run number 266, SUCCESS, with quality (py3.11)
SUCCESS and quality (py3.12) SUCCESS. Post-merge CodeQL run 30914966999, run
number 270, SUCCESS, with analyze (python) SUCCESS. Post-merge Optional Extras /
Backends run 30914968267, run number 88, SUCCESS, with core-without-backends
SUCCESS, backends-transformers SUCCESS and backends-llamacpp SUCCESS.

Scope:
Reconcile post-merge canonical truth after PR #86 merged. This gate marks the
P01-T03C2 controlling-state block historical, records the canonical adoption of
the P01-04C acceptance closeout, and adds the P01-04C canonical adoption record.
It implements nothing, executes nothing, accesses no dataset, reads no P01-03G
registry, generates no split, creates no partition membership, performs no
leakage analysis, publishes nothing, promotes nothing and authorizes no
downstream phase.

--- Current controlling state ---

P01-T03C2 documentation:
ADOPTED ON CANONICAL MAIN

PR #86:
MERGED AND MECHANICALLY VERIFIED AS
fe2dc1e6fe65d4823655f6d958cf3307629623ec

P01-04B:
ACCEPTED AND CANONICALLY ADOPTED

Founder P01-04C acceptance:
ISSUED ON 2026-08-04

P01-04C SYNTHETIC QUALIFICATION:
ACCEPTED

P01-04C ACCEPTANCE CLOSEOUT:
CANONICALLY ADOPTED THROUGH PR #86

P01-04C CANONICAL MERGE:
fe2dc1e6fe65d4823655f6d958cf3307629623ec

P01-04C:
ACCEPTED AND CANONICALLY CLOSED

P01-04D:
NOT AUTHORIZED

P01-04E THROUGH P01-04G:
NOT AUTHORIZED

REAL DATASET ACCESS:
NOT AUTHORIZED

P01-03G REGISTRY ACCESS:
NOT AUTHORIZED

REAL SPLIT EXECUTION:
NOT AUTHORIZED

REAL PARTITION MEMBERSHIP:
NOT AUTHORIZED

CANONICAL LEAKAGE EXECUTION:
NOT AUTHORIZED

P01-04 OVERALL:
NOT COMPLETE

P01-05:
NOT UNLOCKED

Dataset scanning, registry scanning, record-pair discovery, public export,
filesystem publication, evidence publication, model access, inference,
retrieval, benchmark execution, training, fine-tuning, adapter creation and
clinical use:
NOT AUTHORIZED

P01-04C is closed as a synthetic fixture-qualification gate only. No real split
exists, no real partition membership exists, no real labels were processed, no
canonical leakage was executed and no real evidence was published.
P01-04 overall is not complete.
P01-05 is not unlocked.
Entry into P01-04D remains subject to a separate founder entry decision that has
not been issued.
```
