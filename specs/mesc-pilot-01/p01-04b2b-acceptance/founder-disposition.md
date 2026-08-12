# P01-04B2B Acceptance — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Decision:
ACCEPT P01-04B2B IMPLEMENTATION

FD-B2B-11:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2C:
NOT AUTHORIZED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split, real or canonical leakage audit, real-data access,
model access, inference, retrieval, metrics, benchmark execution,
training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Required canonical baseline:
`d91f76e77c4753e556b2ca9c2ee1bfcd5923d863`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`decision-basis.md`](decision-basis.md) or
[`acceptance.md`](acceptance.md), this document controls.

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/)
and
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/)
and is not restated here.

---

## 1. FD-B2B-11 — P01-04B2B Implementation Acceptance Disposition

```text
FD-B2B-11 — P01-04B2B Implementation Acceptance Disposition

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Decision:
ACCEPT P01-04B2B IMPLEMENTATION

Accepted implementation:
The private, fixture-only P01-04B2B leakage primitive library introduced
through PR #72 at the reviewed head 86cfdca1797cf1be60761284af1cc81e25047f41
and canonically merged as d91f76e77c4753e556b2ca9c2ee1bfcd5923d863, under the
FD-B2B-1 through FD-B2B-10 authorization and the r3 implementation contract
adopted through PR #71 at aeff056cb02fc9f72d2d861cadb84622c5558032.

P01-04B2B:
ACCEPTED
```

## 2. Decision basis

The acceptance rests on all nine of the following, each evidenced in
[`decision-basis.md`](decision-basis.md):

```text
1. the authorization was validly adopted
2. the implementation stayed within the exact two-path allowlist
3. the implementation conformed to the adopted contract
4. the required synthetic and golden-vector tests were present and passing
5. an independent exact-head implementation review found no blocking finding
6. Ready was separately founder-authorized and executed
7. merge was separately founder-authorized and executed
8. the canonical merge preserved the reviewed head and the reviewed blobs
9. mechanical post-merge verification passed
```

No criterion is waived, inferred or substituted. Each is satisfied on the exact
identity recorded in §3.

## 3. Exact implementation accepted

```text
Authorization package:
PR #71 — MERGED / CLOSED / NOT DRAFT
canonical merge aeff056cb02fc9f72d2d861cadb84622c5558032
FD-B2B-1 through FD-B2B-10 and the r3 implementation contract

Implementation:
PR #72 — MERGED / CLOSED / NOT DRAFT
canonical merge d91f76e77c4753e556b2ca9c2ee1bfcd5923d863
reviewed and merged head 86cfdca1797cf1be60761284af1cc81e25047f41
implementation tree 070b177194094e5ae55d34570a86997fde956302
implementation parent aeff056cb02fc9f72d2d861cadb84622c5558032
1 commit / 2 files / +2260 / -0
```

Exactly two paths:

```text
src/medscale/mesc/_leakage_v1.py
blob 61f2bf4dff7e71f0a7f2be21b425ba8686badf16          +964

tests/test_mesc_leakage_v1.py
blob a7a77ceee84206c5bfb64b07e64083bb4b0af660         +1296
```

The acceptance is bounded to this exact implementation identity. It does not
extend to any later, amended or unmerged implementation, to any public surface,
or to any execution entry point — none of which exists in this increment.

## 4. Scope of acceptance

```text
Acceptance applies only to the private fixture-only leakage primitive library.

Acceptance does not authorize orchestration, dataset scanning,
record-pair discovery, real execution or a real leakage audit.

Acceptance does not authorize P01-04B2C or P01-04B2D.

Acceptance does not complete or accept P01-04B as a whole.
```

The accepted module is private (`src/medscale/mesc/_leakage_v1.py`), exports no
public façade, adds no CLI surface, adds no dependency, performs no filesystem,
network, subprocess, clock, locale or environment access, and is exercised only
by synthetic in-memory fixtures committed in
`tests/test_mesc_leakage_v1.py`. Accepting it grants no authority that the
adopted contract withheld.

## 5. Accepted non-blocking observations

The independent implementation review returned `APPROVE WITH NON-BLOCKING
NOTES` with **no blocking finding**. Its six observations are carried forward
verbatim in substance and are classified as:

```text
ACCEPTED NON-BLOCKING IMPLEMENTATION OBSERVATIONS
NOT CORRECTED
NOT SILENTLY RESOLVED
NOT UPGRADED INTO NEW PUBLIC BEHAVIOUR
```

```text
NB-1:
Empty identity arrays are rejected through necessary fail-closed inference;
founder clarification had been recommended.

Disposition:
ACCEPTED — NON-BLOCKING. The contract does not expressly state a minimum
arity for the identity arrays. Rejecting an empty array is the fail-closed
reading, is consistent with the identity document's purpose, and is retained
as accepted behaviour without amending the contract.
```

```text
NB-2:
The threshold boundary tests alone do not discriminate integer comparison from
a hypothetical float comparison, although source inspection confirms
integer-only threshold logic.

Disposition:
ACCEPTED — NON-BLOCKING. The reviewed source performs threshold passage by
exact integer comparison as §3 requires. The observation concerns the
discriminating power of the committed tests, not the behaviour of the
accepted implementation.
```

```text
NB-3:
The evidence-reference local-path check uses an implementation-defined
heuristic grounded in the senior "not local path" requirement.

Disposition:
ACCEPTED — NON-BLOCKING. The contract requires that a local path never serve
as a stable supporting-evidence reference but does not specify a detection
method. The chosen heuristic fails closed and is retained as accepted
behaviour.
```

```text
NB-4:
The canonical finding document includes a schema member not expressly listed
in the senior LeakageFinding field list.

Disposition:
ACCEPTED — NON-BLOCKING. The member is a schema identifier in the finding's
canonical document. It does not alter the exact six-member finding-ID identity
document of §6.1, and therefore does not alter FINDING_IDENTITY_BYTES or any
finding_id.
```

```text
NB-5:
The detection_methods allowlist is narrower than the senior generic
array-of-strings type.

Disposition:
ACCEPTED — NON-BLOCKING. Narrowing a permitted type to a closed allowlist is
fail-closed and admits no value the contract permitted to carry meaning. It is
retained as accepted behaviour.
```

```text
NB-6:
Unicode combining marks act as token boundaries, consistent with maximal
Unicode alphanumeric-run semantics.

Disposition:
ACCEPTED — NON-BLOCKING. This is the direct consequence of the §2 rule that
tokens are maximal consecutive Unicode alphanumeric runs, applied after NFKC
normalization. It is conforming behaviour, not a defect.
```

**No implementation correction is authorized by this package.** No follow-up
commit, patch, contract amendment, test addition or behavioural change is
authorized by recording these observations, and none of them is to be treated
as a deferred obligation against the accepted implementation identity.

## 6. Adoption conditions — all five required

`FD-B2B-11` is **issued but not yet canonical**. Adoption requires:

1. a genuinely independent clean-room exact-head review of **this acceptance
   package**;
2. a separate founder Ready decision;
3. a separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification.

```text
No subset adopts FD-B2B-11.
```

Local commit creation adopts nothing. Draft creation adopts nothing. Review
approval alone, Ready alone, merge alone, review plus merge, and merge without
mechanical verification are each insufficient.

## 7. Classification before canonical adoption

While this package remains local, Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified:

```text
FD-B2B-11:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B2C:
NOT AUTHORIZED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

B2B is **not** canonically accepted merely because this decision appears in a
local branch or a Draft pull request.

## 8. Classification after canonical adoption

Only after all five adoption conditions pass:

```text
FD-B2B-11:
ADOPTED ON CANONICAL MAIN

P01-04B2B:
ACCEPTED

P01-04B2C:
ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION;
NOT AUTOMATICALLY AUTHORIZED

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

## 9. Continuing prohibitions

Before and after canonical adoption, `FD-B2B-11` does not authorize:

```text
P01-04B2C or P01-04B2D
P01-04C through P01-04G
P01-04B whole-phase acceptance
leakage-audit orchestration
dataset scanning or registry scanning
record-pair enumeration or automatic finding discovery
fixture facade, split facade, CLI or filesystem publication
the real Pilot-01 split
a real or canonical leakage audit
P01-03G or real dataset access
B0 or B1 execution
model access
inference
retrieval
metrics or benchmark execution
training or fine-tuning
publication
clinical use
any workflow dispatch, rerun or cancellation
any correction, amendment or extension of the accepted implementation
any expansion of the accepted two-path implementation scope
modification of any prior governance package
any implementation, test, workflow, dependency or configuration change
a second commit on this package
amendment, rebase, squash, reset, cherry-pick or force-push
marking this package's pull request Ready
merging this package
auto-merge
deleting any branch
```

## 10. Standing status

P01-04B remains incomplete and not accepted. P01-04B2C and P01-04B2D remain
unauthorized. No execution authority of any kind is created by this
disposition.
