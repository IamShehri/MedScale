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
| P01-04B2A | Deterministic artifact types and canonical serialization | Contracts ratified; implementation adopted (PR #59); portability validation infrastructure adopted on canonical main (PR #61 merge `69f16455...`); evidence-production authority adopted on canonical main (PR #65 merge `e3478da9...`); FD-PV-17 and FD-PV-18 activated and consumed; canonical portability evidence produced by run 30678040133, mechanically verified, and independently reviewed APPROVE WITH NON-BLOCKING NOTES; founder evidence-acceptance decision FD-PV-19 adopted on canonical main (PR #66 merge `1f2d9152...`); founder implementation-acceptance decision FD-B2A-9 issued but not yet adopted on canonical main, with the N-12 discharge and the Windows and macOS closure decisions likewise issued but not yet canonical; execution not authorized; B2A founder-accepted in substance but not yet canonically adopted; B2B not authorized |

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
