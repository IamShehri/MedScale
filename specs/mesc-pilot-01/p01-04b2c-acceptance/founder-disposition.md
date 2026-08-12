# P01-04B2C Acceptance — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Decision:
ACCEPT P01-04B2C IMPLEMENTATION

FD-B2C-ACT-1:
FOUNDER CONFIRMATION RECORDED —
NOT YET CANONICALLY RECORDED IN THE REPOSITORY

FD-B2C-13:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split generation, real or canonical leakage-audit execution,
real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Required canonical baseline:
`9d4b9ed0bada16455781240bb074ffd852397988`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`decision-basis.md`](decision-basis.md) or
[`acceptance.md`](acceptance.md), this document controls.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/),
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/)
and
[`../p01-04b2c-authorization/`](../p01-04b2c-authorization/)
and is not restated here. Those packages are immutable historical authorities
and are not modified by this one.

---

## 1. FD-B2C-ACT-1 — Founder Activation Confirmation

```text
FD-B2C-ACT-1 — FOUNDER ACTIVATION CONFIRMATION

Founder:
Abdulaziz Alshehri

Confirmation date:
2026-08-02

Authorization package head:
89a708587ef28b4e19f6225ce86181715a680805

Authorization package tree:
c5afa12e85ef4e0c7f9fcbf71c673da211e1ef2a

Canonical authorization merge:
fb17439e6c9f0f28b31689c82567cd9c97312085

Before implementation commit
17c7478f4e052ac331505d3fcfe4dfde825db898
was created, all five FD-B2C-12 activation conditions were satisfied:

1. independent clean-room exact-head review of the authorization package
   — SATISFIED
2. separate Founder Ready decision
   — SATISFIED
3. separate Founder Merge decision
   — SATISFIED
4. merge into canonical main
   — SATISFIED
5. mechanical post-merge verification
   — SATISFIED

Therefore P01-04B2C implementation authority was ACTIVE before implementation.

The one bounded implementation authority is now SPENT.
```

FD-B2C-ACT-1 is historical sequencing evidence. Explicitly:

```text
FD-B2C-ACT-1:
confirms sequencing only
creates no new implementation authority
does not accept the implementation
does not authorize P01-04B2D
```

The acceptance of the implementation is made by FD-B2C-13 below, not by this
confirmation. The sequencing evidence is recorded in
[`decision-basis.md`](decision-basis.md) §2.

## 2. FD-B2C-13 — P01-04B2C Implementation Acceptance Disposition

```text
FD-B2C-13 — P01-04B2C Implementation Acceptance Disposition

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Decision:
ACCEPT P01-04B2C IMPLEMENTATION

Accepted implementation:
The private, fixture-only, in-memory P01-04B2C split facade introduced through
PR #75 at the reviewed head 17c7478f4e052ac331505d3fcfe4dfde825db898 and
canonically merged as 9d4b9ed0bada16455781240bb074ffd852397988, under the
FD-B2C-1 through FD-B2C-12 authorization adopted through PR #74 at
89a708587ef28b4e19f6225ce86181715a680805 and canonically merged as
fb17439e6c9f0f28b31689c82567cd9c97312085.

P01-04B2C:
ACCEPTED
```

Acceptance is bounded to the exact implementation identity recorded in §4 and
to the contract adopted through the authorization package. It extends to no
other commit, tree, blob, path or behaviour.

## 3. Decision basis

The acceptance rests on all twelve of the following, each evidenced in
[`decision-basis.md`](decision-basis.md):

```text
 1. FD-B2C-1 through FD-B2C-12 were validly adopted before implementation
 2. FD-B2C-ACT-1 confirms the five activation conditions were satisfied
 3. the implementation stayed within the exact two-path allowlist
 4. no accepted B1, B2A or B2B module was modified
 5. the implementation conformed to implementation-contract.md sections 1-16
 6. the complete required synthetic and literal-golden-vector suite was present
 7. an independent exact-head implementation review found no blocking finding
 8. exact-head CI and CodeQL passed
 9. Ready was separately founder-authorized and executed
10. merge was separately founder-authorized and executed
11. canonical merge preserved the reviewed tree, paths and blobs
12. mechanical post-merge verification passed
```

No criterion is waived, substituted or inferred from merge alone. A merge event
by itself evidences criteria 10 and 11 only, and never criteria 1 through 9 or
criterion 12.

## 4. Exact implementation accepted

```text
Authorization package:
PR #74 — MERGED / CLOSED / NOT DRAFT

Authorization package head:
89a708587ef28b4e19f6225ce86181715a680805

Authorization package tree:
c5afa12e85ef4e0c7f9fcbf71c673da211e1ef2a

Canonical authorization merge:
fb17439e6c9f0f28b31689c82567cd9c97312085

Adopted authority:
FD-B2C-1 through FD-B2C-12
```

```text
Implementation PR:
#75 — MERGED / CLOSED / NOT DRAFT

Reviewed and merged head:
17c7478f4e052ac331505d3fcfe4dfde825db898

Implementation tree:
2fc26581ceb1b09216b2bf51de10fcbece68a62b

Implementation parent:
fb17439e6c9f0f28b31689c82567cd9c97312085

Canonical implementation merge:
9d4b9ed0bada16455781240bb074ffd852397988

Commit count:
1

Files:
2

Statistics:
2266 additions
0 deletions
```

Exactly two paths, identified by path and blob rather than by restated source:

```text
src/medscale/mesc/_fixture_split_v1.py
blob 6511861b41b2276948a6903292f07c3735317177
947 additions
0 deletions

tests/test_mesc_fixture_split_v1.py
blob 5a2c1d5a19afa4ebee63ffacee5c4b9a7aabafd9
1319 additions
0 deletions
```

No third path exists in the accepted change. The accepted modules
`src/medscale/mesc/__init__.py`, `src/medscale/mesc/split.py`,
`src/medscale/mesc/_split_v1.py`,
`src/medscale/mesc/_canonical_json_v1.py`,
`src/medscale/mesc/_split_artifacts_v1.py` and
`src/medscale/mesc/_leakage_v1.py` are byte-identical to their pre-implementation
state.

## 5. Scope of acceptance

```text
Acceptance applies only to the exact private fixture-only, in-memory P01-04B2C
facade implementation merged through PR #75.

Acceptance recognizes deterministic composition of accepted B1, B2A and B2B
layers under synthetic identity-only fixtures.

Acceptance does not transform any generated in-memory value into evidence, a
publishable artifact, a canonical real split, a leakage-audit result or a
clinical/research conclusion.
```

Every identity value verified during review — fixture digests, request
identifiers, group identifiers, the 16-hex compatibility hash and the 64-hex
authoritative fingerprint — is a **synthetic unit-fixture identity**. None is
scientific evidence, dataset evidence, or a real split artifact.

The declared `fixture_only`, `non_evidence` and `synthetic_identity_proof`
markers remain declared markers establishing internal identity consistency only.
Acceptance does not convert them into a cryptographic or real-world provenance
oracle, and no flag combination detects a caller repackaging real data. B2C
safety continues to derive from structure: a private unexported module, no CLI,
no path input, no registry adapter, no filesystem access, no real-data entry
point, and `SourceDocumentGroupedSplitter.assign` remaining unconditionally
fail-closed.

## 6. Accepted and discharged non-blocking observations

The independent exact-head implementation review returned
`APPROVE WITH NON-BLOCKING NOTES` with **no blocking finding**. All six
observations are carried forward here in full and disposed of. None is deferred,
and none creates authority to change the accepted implementation.

### NB-1

```text
Observation:
The sixth facade error class is correctly implemented but omitted from two
error-matrix tests.

Disposition:
ACCEPTED — NON-BLOCKING.

The implementation contains the required class and stable code. The observation
concerns completeness of two parameterized test matrices, not absence or
incorrect behavior of the error class.
```

### NB-2

```text
Observation:
B2C-specific invariant-failure arms are not directly exercised, although the
successful pipeline executes the invariants and required tampering failures are
covered through accepted B2A verification paths.

Disposition:
ACCEPTED — NON-BLOCKING.

Source inspection established the invariant checks. The observation concerns
direct branch coverage and creates no authority to add tests or alter behavior.
```

### NB-3

```text
Observation:
One label-total reconciliation check is derivationally weaker than the wording
of the governing invariant.

Disposition:
ACCEPTED — NON-BLOCKING.

The reviewed composed pipeline, complete-domain construction and remaining
cross-object reconciliation preserve the required fail-closed result. No
behavioral correction is authorized.
```

### NB-4

```text
Observation:
The final-summary fingerprint-presence check is implemented as an exact
byte-substring check rather than parsing the canonical document and comparing a
field.

Disposition:
ACCEPTED — NON-BLOCKING.

The final summary is produced by the accepted canonical serializer from the
newly constructed authoritative fingerprint and is checked before return. The
observation does not establish an incorrect byte surface or fingerprint.
```

### NB-5

```text
Observation:
Several implemented request-validation rules are not represented by an
individual dedicated committed test.

Disposition:
ACCEPTED — NON-BLOCKING.

Independent source inspection confirmed the required rules and the complete
focused and project-wide suites passed. This observation creates no
test-addition authority.
```

### NB-6

```text
Observation:
The pre-activation governance snapshot remained in repository text and did not
itself prove that implementation authority had activated before implementation.

Disposition:
DISCHARGED BY FD-B2C-ACT-1 — NON-BLOCKING GOVERNANCE OBSERVATION.

The founder activation confirmation records the exact sequencing evidence.
This was not an implementation defect and requires no source or test change.
```

### Effect of accepting these observations

```text
No implementation correction is authorized by this package.

No follow-up source commit, test commit, contract amendment, public export,
behavioral extension or scope expansion is authorized by accepting these notes.

NB-1 through NB-5 are accepted non-blocking implementation observations.

NB-6 is a discharged non-blocking governance observation through
FD-B2C-ACT-1.
```

None of NB-1 through NB-6 is a deferred obligation, a conditional acceptance, a
remediation commitment or a scheduled follow-up.

## 7. Adoption conditions — all five required

```text
1. genuinely independent clean-room exact-head review of this acceptance package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset canonically adopts FD-B2C-ACT-1 or FD-B2C-13.

No subset canonically accepts P01-04B2C.
```

Local commit creation activates nothing. Draft creation activates nothing.
Review approval alone, Ready alone, merge alone, review plus merge, and merge
without mechanical verification are each insufficient.

## 8. Classification before canonical adoption

While this package is local, Draft, Ready-but-unmerged, or merged-but-not-
mechanically-verified:

```text
FD-B2C-ACT-1:
FOUNDER CONFIRMATION RECORDED —
NOT YET CANONICALLY RECORDED IN THE REPOSITORY

FD-B2C-13:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

P01-04B2C must not be described as canonically accepted merely because this
local package exists.

## 9. Classification after canonical adoption

Only after all five adoption conditions of §7 pass:

```text
FD-B2C-ACT-1:
CANONICALLY RECORDED

FD-B2C-13:
ADOPTED ON CANONICAL MAIN

P01-04B2C:
ACCEPTED

P01-04B2D:
ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION;
NOT AUTOMATICALLY AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

B2C acceptance creates only eligibility to consider a separate B2D authorization
package. Eligibility is never implementation authority.

## 10. Continuing prohibitions

Before and after canonical adoption, FD-B2C-ACT-1 and FD-B2C-13 do not
authorize:

```text
P01-04B2D implementation
B2D qualification
exact-reference-1000-v1
constraint-stress-1000-v1
leakage-positive-v1
real split generation
real or canonical leakage-audit execution
leakage-audit orchestration over a collection
dataset or registry scanning
record-pair enumeration or automatic finding discovery
P01-03G or real-data access
CLI or filesystem publication
public package export
model access
inference
retrieval
metrics or benchmark execution
training
fine-tuning
publication
clinical use
P01-04C through P01-04G
P01-04B whole-phase acceptance
correction, amendment or extension of the accepted implementation
modification of any accepted B1, B2A or B2B module
modification of any prior governance package
a second commit on this package
amendment, rebase, squash, reset, cherry-pick or force-push
marking this package's pull request Ready
merging this package
auto-merge
deleting any branch
any workflow dispatch, rerun or cancellation
```

## 11. Standing status

P01-04B remains incomplete and not accepted. P01-04B2D remains unauthorized. No
execution authority of any kind is created by this disposition. The bounded
P01-04B2C implementation authority was exercised exactly once and is spent; it
does not authorize a second attempt, a correction series, or a follow-up
expansion.
