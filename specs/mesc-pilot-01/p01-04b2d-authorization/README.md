# P01-04B2D Authorization

```text
Current status:
FOUNDER AUTHORIZATION ISSUED — NOT ADOPTED

FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

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
real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Recording this package in a pull request authorizes nothing. Implementation
authority activates only through the five conditions in
[Activation gate](#activation-gate).

## Purpose

This package is the separate founder **authorization** for P01-04B2D —
integrated synthetic qualification of the accepted B1, B2A, B2B and B2C layers
against the three ratified synthetic fixtures, together with a criterion-by-
criterion P01-04B acceptance review.

It is documentation only. It implements nothing, executes nothing, constructs no
fixture, invokes no facade, and calculates no B2D hash, identifier or
fingerprint. B2C acceptance made B2D *eligible* for this decision; eligibility
was never authority, and this authorization is itself inactive until adopted.

## Canonical baseline

```text
origin/main:
a0c623aa08354a343fccc1d066a7a6acaa5b8576

Tree:
6e766deb531a9d7332942c3a524be0b3de698af3

Ordered parent 1:
9d4b9ed0bada16455781240bb074ffd852397988

Ordered parent 2:
3edcc476cf403bbd4d9c2d5bb05d739b40abe748

Subject:
Merge pull request #76 from IamShehri/docs/mesc-p01-04b2c-acceptance
docs(mesc): record P01-04B2C implementation acceptance
```

## Prerequisite acceptance chain

```text
P01-04B2A:   ACCEPTED
P01-04B2B:   ACCEPTED
P01-04B2C:   ACCEPTED

FD-B2C-ACT-1:  CANONICALLY RECORDED
FD-B2C-13:     ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:  SPENT
P01-04B2D:   ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION — NOT AUTHORIZED
P01-04B:     INCOMPLETE / NOT ACCEPTED
```

## FD-B2-7 conformance

An earlier drafting attempt proposed fixture contracts that contradicted
founder-ratified FD-B2-7, which `p01-04b2/decision-record.md` declares
controlling on conflict. The build was stopped rather than silently reconciled.

```text
Selected resolution:
PATH 1 — CONFORM P01-04B2D TO RATIFIED FD-B2-7

FD-B2-7 amended:      NO
FD-B2-7 superseded:   NO
Conflicting requirements:  WITHDRAWN
```

| Conflict | Withdrawn proposal | Ratified requirement | Resolution |
|---|---|---|---|
| A | 1000 singleton groups in the reference fixture | multi-example groups mandatory; sizes must include 1, 2, 3, 5, 8, 13 | FD-B2D-4: **89 groups**, all six sizes present |
| B | constraint-stress proves exact targets with zero deviation | group sizes intentionally make exact targets infeasible; minimum deviation recorded | FD-B2D-5: **500 groups of size 2**, matrix provably infeasible |
| C | all findings `unresolved` | at least one supported `false_positive`, at least one `unresolved` | FD-B2D-6: **9 findings**, 3 false positives, 6 unresolved |
| D | five scenarios omitting three ratified cases | deterministic cases for all nine comparison behaviours | FD-B2D-6: all **9 scenarios** covered by same-partition controls |

## Decision index

| Decision | Subject |
|---|---|
| FD-B2D-1 | Qualification-only surface and exact three-path allowlist |
| FD-B2D-2 | Exact fixture set — the three ratified names only |
| FD-B2D-3 | Shared synthetic identity contract and generator-spec proof |
| FD-B2D-4 | `exact-reference-1000-v1` |
| FD-B2D-5 | `constraint-stress-1000-v1` |
| FD-B2D-6 | `leakage-positive-v1` |
| FD-B2D-7 | Literal qualification vectors |
| FD-B2D-8 | Cross-platform six-cell qualification workflow |
| FD-B2D-9 | P01-04B acceptance-criteria mapping — 13 unique criteria |
| FD-B2D-10 | Oracle independence and anti-circularity |
| FD-B2D-11 | Fail-closed and golden-change policy |
| FD-B2D-12 | Evidence classification |
| FD-B2D-13 | Prohibitions and downstream non-authority |
| FD-B2D-14 | Activation and one bounded implementation |

## Future exact three-path implementation allowlist

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml

exact path count:  3
production source changes authorized:  0
new dependencies authorized:  0
public export or CLI authorized:  NONE
existing workflow modification authorized:  NONE
```

```text
Future branch:
test/mesc-p01-04b2d-qualification

Future commit subject:
test(mesc): qualify P01-04B2D synthetic suite
```

## The three exact fixtures

```text
exact-reference-1000-v1
constraint-stress-1000-v1
leakage-positive-v1
```

No generic `fixture-1000-v1` alias. No fourth qualification fixture. Derived
negative mutations inside tests are never qualification fixtures.

| Fixture | Rows | Groups | Structure | Exact ratified matrix |
|---|---|---|---|---|
| `exact-reference-1000-v1` | 1000 | **89** | sizes 1, 2, 3, 5, 8, 13 | FEASIBLE |
| `constraint-stress-1000-v1` | 1000 | **500** | every group size 2 | **INFEASIBLE** |
| `leakage-positive-v1` | 1000 | **999** | 998 singletons + 1 homogeneous pair | FEASIBLE |

```text
constraint-stress global minimum-deviation score:  6
constraint-stress score-6 matrices:                2

leakage-positive source-document groups:           999
leakage-positive two-example groups:               1
leakage-positive singleton groups:                 998
leakage-positive findings:                         9
leakage-positive leaked:                           true
```

### Constraint-stress infeasibility and tie-break

The ratified target matrix contains exactly **six** odd-valued cells, comprising
**five** distinct odd values because `83` occurs twice:

```text
yes / validation    = 83
yes / test          = 83
no / train          = 237
no / test           = 51
maybe / train       = 77
maybe / validation  = 17
```

Every constraint-stress group has size 2, so every realized label-by-partition
cell must be even. The six odd target cells therefore make the exact ratified
matrix infeasible.

Exactly **two** feasible matrices attain the minimum squared-deviation score of
`6`. Both are founder-frozen:

```text
Matrix A — lexicographic winner (selected)

              train  validation  test  total
yes             386          82    84    552
no              238          50    50    338
maybe            76          18    16    110
total           700         150   150   1000

flattened vector:  386,82,84,238,50,50,76,18,16
```

```text
Matrix B — score-6 runner-up

              train  validation  test  total
yes             386          84    82    552
no              236          50    52    338
maybe            78          16    16    110
total           700         150   150   1000

flattened vector:  386,84,82,236,50,52,78,16,16
```

```text
Exactly two feasible matrices have minimum squared-deviation score 6.

Under the controlling lexicographic order:

label order:
yes, no, maybe

partition order:
train, validation, test

Matrix A is smaller than Matrix B and is therefore the uniquely selected
qualification oracle result.
```

The `leakage-positive-v1` structure — 999 source-document groups, exactly one
homogeneous two-example group whose members share a decision and one actual
partition and which never straddles a partition boundary, and exactly 998
singleton groups with no other multi-example group — is a **founder-frozen
requirement**, not a derived or inferred value. It is subordinate to and
consistent with FD-B2-7 and **does not amend FD-B2-7**.

### Same-partition synthetic control boundary

```text
The exact-example self-identity scenario and the exact-source-document
same-group scenario are same-partition synthetic controls.

They qualify primitive behavior, finding construction, canonical identity,
classification and evidence-reference enforcement only.

They are not cross-partition leakage findings, do not establish duplicate
partition membership, do not establish source-document overlap, and do not
constitute a real or canonical leakage audit.
```

FD-B2D-6 requires this distinction to be explicit in all four authorization
documents: `README.md`, `acceptance.md`, `founder-authorization.md` and
`implementation-contract.md`.

## Cross-platform workflow summary

```text
path:  .github/workflows/mesc-p01-04b2d-qualification.yml
name:  MESC P01-04B2D Qualification

triggers:      pull_request, push to main
permissions:   contents: read
fail-fast:     false

matrix:
  ubuntu-latest   Python 3.11
  ubuntu-latest   Python 3.12
  windows-latest  Python 3.11
  windows-latest  Python 3.12
  macos-latest    Python 3.11
  macos-latest    Python 3.12
```

No `workflow_dispatch`, no schedule, no secrets, no artifact upload, no write
permission. Every cell compares against the same committed literal goldens. No
OS-specific expected value is permitted.

## Review and capability summary

The acceptance mapping covers **13 unique criteria**:

```text
The mapping contains:
- the ten P01-04B tooling-acceptance criteria; and
- three additional non-duplicative future-code criteria from
  p01-04b2/acceptance.md.
```

The ten tooling rows alone do not represent every canonical criterion.

| # | Criterion | Status |
|---|---|---|
| 1–10 | P01-04B tooling-acceptance criteria | expected SATISFIED |
| 11 | atomic publication | NOT APPLICABLE to B2D; **NOT SATISFIED** for P01-04B overall |
| 12 | write-path protections | NOT APPLICABLE to B2D; **NOT SATISFIED** for P01-04B overall |
| 13 | date-free promotable artifacts | NOT APPLICABLE to B2D output promotion; date-free byte invariant testable |
| — | indivisible-group minimum-deviation allocation | **UNSATISFIED** |

`FixtureSplitFacade` performs no filesystem publication and accepts no
filesystem path, so criteria 11 and 12 cannot be qualified by B2D — and their
inapplicability to B2D is not qualification of a future write or publication
path. Criterion 13 is bounded: the harness must assert that every canonical byte
surface is free of dates, timestamps, local paths, usernames, hostnames, runtime
durations, workflow IDs, command logs and workspace locations, but a successful
assertion does not make any B2D output promotable.

No aggregate acceptance algorithm may treat the suite as accepting P01-04B while
any criterion is `UNSATISFIED` or `BLOCKED`. `NOT APPLICABLE` never converts to
`SATISFIED`.

The B2D harness is expected to be **green** while recording one **UNSATISFIED**
P01-04B criterion:

```text
constraint-stress minimum-deviation allocation:
UNSATISFIED BY CURRENT ACCEPTED IMPLEMENTATION
```

The accepted `allocate_indivisible_groups` performs exact-target allocation only
and raises `SplitAllocationError` at a boundary crossing. It does not implement
the FD-B2-7 Fixture B global minimum-deviation fallback. The qualification test
asserts that exact typed failure.

```text
B2D qualification harness:
PASS — EXPECTED BLOCKING CAPABILITY GAP DETECTED

P01-04B acceptance eligibility:  FALSE
P01-04B acceptance recommendation:  CHANGES REQUIRED

GREEN B2D QUALIFICATION CI
DOES NOT EQUAL P01-04B ACCEPTANCE.
```

No production correction is authorized in B2D. A separate founder correction
authorization must precede any production implementation of globally
minimum-deviation grouped allocation.

## Activation gate

Implementation authority activates only after all five conditions:

```text
1. genuinely independent clean-room exact-head review
   of this authorization package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset activates authority.
```

Local commit activates nothing. Draft creation activates nothing. Review alone,
Ready alone, merge alone, and merge without mechanical verification are each
insufficient.

## Post-implementation gates

Even after the future implementation is built:

```text
1. independent clean-room exact-head implementation review
2. exact-head standard CI and CodeQL success
3. all six dedicated B2D workflow cells successful
4. separate Founder Ready decision
5. separate Founder Merge decision
6. canonical merge with expected-head lock
7. mechanical post-merge verification
8. separate founder qualification-and-P01-04B acceptance disposition
9. independent review and canonical adoption of that acceptance disposition
```

```text
No implementation merge automatically accepts B2D or P01-04B.
No B2D acceptance automatically authorizes P01-04C.
```

## Classification before canonical adoption

While this package is local, Draft, Ready-but-unmerged, or merged-but-not-
mechanically-verified:

```text
FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:  RECORDED BUT INACTIVE
P01-04B2D implementation:            NOT AUTHORIZED TO BEGIN
P01-04B2D qualification:             NOT EXECUTED
P01-04B:                             INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G:             NOT AUTHORIZED
```

## Classification after canonical adoption

Only after all five activation conditions pass:

```text
FD-B2D-1 through FD-B2D-14:
ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
ACTIVE FOR ONE BOUNDED IMPLEMENTATION ONLY

P01-04B2D implementation:
AUTHORIZED TO BEGIN
NOT YET IMPLEMENTED
NOT YET QUALIFIED
NOT ACCEPTED

P01-04B:                    INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G:    NOT AUTHORIZED
```

This is a future conditional state and is never current while this package
remains unadopted.

## Continuing prohibitions

Before and after canonical adoption, FD-B2D-1 through FD-B2D-14 do not
authorize:

```text
real P01-03G access               real source-records.jsonl access
real ordered registry access      real split generation
real partition membership         real leakage scanning
generic record-pair discovery     real leakage findings
dataset download                  model download
model access                      inference
retrieval                         metrics
benchmark execution               training
fine-tuning                       adapter creation
publication                       clinical use

P01-04C through P01-04G implementation or execution
P01-05 or later
P01-04B whole-phase acceptance
production correction of the minimum-deviation gap
modification of D1-D10 or FD-B2-1 through FD-B2-8
modification of accepted B2A, B2B or B2C behaviour
CLI, public API or filesystem-facing product capability
```

## Document index

```text
README.md
  this overview

founder-authorization.md — controlling
  FD-B2D-1 through FD-B2D-14 in full

implementation-contract.md
  the exact future implementation contract

acceptance.md
  authorization-package acceptance criteria
```

[`founder-authorization.md`](founder-authorization.md) **controls on conflict**
with [`README.md`](README.md),
[`implementation-contract.md`](implementation-contract.md) or
[`acceptance.md`](acceptance.md).

Prior governance history is adopted at
[`../p01-04/`](../p01-04/),
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/),
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/),
[`../p01-04b2c-authorization/`](../p01-04b2c-authorization/)
and
[`../p01-04b2c-acceptance/`](../p01-04b2c-acceptance/).
Those packages are immutable historical authorities and are not modified here.
