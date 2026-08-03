# P01-04B2D Acceptance

```text
Package status:
RECORDED — NOT ADOPTED

FD-B2D-15:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

Indivisible-group global minimum-deviation allocation:
UNSATISFIED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Production correction authority:
NOT GRANTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

## Purpose

This package records one founder decision, **FD-B2D-15**, after the exact
P01-04B2D implementation was independently reviewed at its exact head, passed
exact-head CI, CodeQL and the six-cell qualification workflow, was canonically
merged, and passed mechanical post-merge verification.

FD-B2D-15 does two things at once, and both must be read together:

```text
It ACCEPTS the exact P01-04B2D implementation, the qualification harness,
and its bounded synthetic qualification evidence.

It records that P01-04B is CHANGES REQUIRED / NOT ACCEPTED, because the
capability the harness was built to test is UNSATISFIED.
```

Accepting a harness that correctly detects a missing capability is not
accepting the capability. That separation is the substance of this package.

This is documentation-only governance work. It implements nothing, executes
nothing, corrects nothing and authorizes no downstream phase.

## Canonical baseline

```text
Required canonical main:
faf58c3fbfa9a83e7d392630e3ad1f322c616259

Required tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1

Ordered parent 1:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Ordered parent 2:
6e5867829006770ad2ed50f26a9af0c455923594

Merge subject:
Merge pull request #78 from IamShehri/test/mesc-p01-04b2d-qualification

Merge body:
test(mesc): qualify P01-04B2D synthetic suite
```

## Authorization identity

```text
Authorization PR:
#77 — MERGED / CLOSED / NOT DRAFT

Authorization reviewed head:
096f6667251b4783fc9511336301dfaaa4c7f336

Authorization reviewed tree:
30b4cb5433a7f8496e62b8a94d879cf34a8ff26a

Authorization canonical merge:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Adopted authority:
FD-B2D-1 through FD-B2D-14
```

## Accepted implementation identity

```text
Implementation PR:
#78 — MERGED / CLOSED / NOT DRAFT

Implementation branch:
test/mesc-p01-04b2d-qualification

Reviewed and merged head:
6e5867829006770ad2ed50f26a9af0c455923594

Reviewed implementation tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1

Implementation parent:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Canonical implementation merge:
faf58c3fbfa9a83e7d392630e3ad1f322c616259

Commit count:
1

Changed files:
3

Statistics:
3223 additions
0 deletions
```

```text
.github/workflows/mesc-p01-04b2d-qualification.yml
99 additions / 0 deletions
blob b45811a2e104e61149c766b39d3c1ad832959b69

tests/_mesc_p01_04b2d_fixtures_v1.py
1022 additions / 0 deletions
blob f35b4443e79338d2309ca9f4197eee8368ea7069

tests/test_mesc_p01_04b2d_qualification_v1.py
2102 additions / 0 deletions
blob ad215f717ef1b27bc7adbfb5c68d81e91ccfc6dd
```

Acceptance is bounded to exactly this identity and to no later change. No
production module, dependency, lockfile, public export, CLI or entry point was
touched.

## Review and workflow summary

```text
Independent clean-room exact-head implementation review:
APPROVE WITH NON-BLOCKING NOTES

Blocking findings:
NONE

Non-blocking observations:
9 — all carried forward and ACCEPTED AS NON-BLOCKING

Correction authorization:
NOT ISSUED
```

Pull-request-triggered checks at the reviewed head:

```text
CI run 30780440275                            completed / success — 2/2 jobs
CodeQL run 30780440276                        completed / success — 1/1 job
MESC P01-04B2D Qualification run 30780440318  completed / success — 6/6 jobs
```

Post-merge push-triggered runs at the canonical merge:

```text
CI run 30781355622                            SUCCESS — 2/2 jobs
CodeQL run 30781355591                        SUCCESS — 1/1 job
MESC P01-04B2D Qualification run 30781355599  SUCCESS — 6/6 jobs
```

Six qualification cells, each completed / success:

```text
qualification (ubuntu-latest py3.11)
qualification (ubuntu-latest py3.12)
qualification (windows-latest py3.11)
qualification (windows-latest py3.12)
qualification (macos-latest py3.11)
qualification (macos-latest py3.12)
```

```text
Workflow success is qualification-harness evidence only. It is not
scientific, clinical, dataset or real-split evidence.
```

## Fixture disposition summary

```text
exact-reference-1000-v1
1000 rows / 89 groups / 700-150-150 / 552-338-110
exact ratified matrix REPRODUCED
indivisible group placement CONFORMING
cross-platform deterministic literals SATISFIED

constraint-stress-1000-v1
1000 rows / 500 groups / group size 2
exact target PROVABLY INFEASIBLE
minimum squared-deviation score 6 / exactly 2 score-6 matrices
selected 386,82,84,238,50,50,76,18,16
runner-up 386,84,82,236,50,52,78,16,16
production minimum-deviation fallback ABSENT
accepted facade behavior TYPED FAIL-CLOSED
minimum-deviation production capability UNSATISFIED

leakage-positive-v1
1000 rows / 999 groups / 1 two-example group / 998 singletons
9 findings / 3 false_positive / 6 unresolved / leaked true / 0 suppressed
```

```text
The exact-example self-identity and exact-source-document same-group
scenarios are same-partition synthetic controls.

They do not establish cross-partition leakage, duplicate split membership,
source-document overlap, real leakage, or canonical leakage evidence.
```

The typed fail-closed allocation failure is correct detection of a missing
capability. It is never implementation conformance to that capability.

## Criterion summary

```text
criteria 1 through 10                SATISFIED
criterion 11 atomic publication      NOT APPLICABLE TO B2D;
                                     NOT SATISFIED FOR P01-04B OVERALL
criterion 12 write-path protections  NOT APPLICABLE TO B2D;
                                     NOT SATISFIED FOR P01-04B OVERALL
criterion 13 date-free promotable    NOT APPLICABLE TO B2D OUTPUT PROMOTION;
             artifacts               DATE-FREE CANONICAL-BYTE INVARIANT SATISFIED;
                                     DOES NOT ESTABLISH PROMOTABILITY

indivisible-group global minimum-deviation allocation
                                     UNSATISFIED
```

```text
P01-04B acceptance eligibility:
FALSE

P01-04B acceptance recommendation:
CHANGES REQUIRED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

```text
A GREEN QUALIFICATION WORKFLOW DOES NOT EQUAL P01-04B ACCEPTANCE.

NOT APPLICABLE IS NEVER CONVERTED TO SATISFIED.
```

## Document index

```text
README.md                — this overview
founder-disposition.md   — controlling
decision-basis.md        — immutable evidence ledger
acceptance.md            — this package's documentation gate
```

- [`README.md`](README.md)
- [`founder-disposition.md`](founder-disposition.md) — **controlling**
- [`decision-basis.md`](decision-basis.md)
- [`acceptance.md`](acceptance.md)

On any conflict, [`founder-disposition.md`](founder-disposition.md) controls.

Prior governance history is adopted at
[`../p01-04/`](../p01-04/),
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/),
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/),
[`../p01-04b2c-authorization/`](../p01-04b2c-authorization/),
[`../p01-04b2c-acceptance/`](../p01-04b2c-acceptance/)
and
[`../p01-04b2d-authorization/`](../p01-04b2d-authorization/)
and is not restated here.

## Adoption boundary

Canonical adoption requires all five conditions:

```text
1. genuinely independent clean-room exact-head review of this acceptance package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset adopts FD-B2D-15.
No subset canonically accepts P01-04B2D.
```

Draft creation, independent review, Ready, merge, or merge without mechanical
verification is individually insufficient.

### Classification before canonical adoption

```text
FD-B2D-15:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D:
FOUNDER-ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

### Classification after canonical adoption

```text
FD-B2D-15:
ADOPTED ON CANONICAL MAIN

P01-04B2D:
ACCEPTED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

## Continuing separation

```text
B2D acceptance is separated from P01-04B acceptance by an explicit
UNSATISFIED criterion.

P01-04B acceptance is separated from every downstream phase by its own
separate founder decision.
```

A later, separately governed correction decision or remaining-tooling decision
is eligible for founder consideration. Eligibility is never authority.

## What this package does not do

```text
does not authorize a minimum-deviation production correction
does not authorize an atomic-publication or write-path implementation
does not authorize any change to the accepted implementation
does not modify any prior governance package
does not accept P01-04B
does not make any B2D output or the fixture helper promotable
does not authorize real dataset, registry or source-record access
does not authorize real split generation or real partition membership
does not authorize a real or canonical leakage audit
does not authorize record-pair discovery or automatic finding discovery
does not authorize dataset or model download, model access, inference,
  retrieval, metrics, benchmark execution, training, fine-tuning or
  adapter creation
does not authorize publication or clinical use
does not authorize P01-04C through P01-04G, or P01-05 or later
does not dispatch, rerun or cancel any workflow
```
