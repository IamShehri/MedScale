# P01-04B Minimum-Deviation Correction Authorization

```text
Package status:
RECORDED — NOT ADOPTED

FD-BR-1:
FOUNDER DECISION ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

FD-BMD-1 THROUGH FD-BMD-14:
FOUNDER DECISIONS ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

MINIMUM-DEVIATION IMPLEMENTATION AUTHORITY:
RECORDED BUT INACTIVE

MINIMUM-DEVIATION IMPLEMENTATION:
NOT AUTHORIZED TO BEGIN

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

ATOMIC PUBLICATION / WRITE-PATH IMPLEMENTATION:
NOT AUTHORIZED

P01-04C THROUGH P01-04G:
NOT AUTHORIZED
```

## Purpose

This package records the founder's recovery architecture for P01-04B as
**FD-BR-1**, and prospectively authorizes one tightly bounded future
implementation of the missing indivisible-group global minimum-deviation
allocation capability as **FD-BMD-1 through FD-BMD-14**.

```text
This package does not implement the correction.
It implements nothing, executes nothing and corrects nothing.
```

The accepted P01-04B2D qualification did its job: it detected a missing
production capability and failed closed. That typed failure was never conformance
to the capability. This package is the governed response to that finding.

## Canonical baseline

```text
Required canonical main:
3513d66bc36650363a6368bb4e42901119419802

Required tree:
e08393388f4684b39ef9226a3a90b719ea1ba494

Ordered parent 1:
faf58c3fbfa9a83e7d392630e3ad1f322c616259

Ordered parent 2:
c38473d69c996e626510256d6297640bd87405ad

Merge subject:
Merge pull request #79 from IamShehri/docs/mesc-p01-04b2d-acceptance

Merge body:
docs(mesc): record P01-04B2D qualification acceptance
```

## Current accepted B2D identity

```text
Authorization PR #77   head 096f6667…  tree 30b4cb54…  merge 63cefe04…
Implementation PR #78  head 6e586782…  tree 3d27b9c4…  merge faf58c3f…
Acceptance PR #79      head c38473d6…                  merge 3513d66b…

FD-B2D-1 through FD-B2D-15:  ADOPTED ON CANONICAL MAIN
P01-04B2A / B2B / B2C / B2D: ACCEPTED
```

Accepted implementation blobs, which this correction must not invalidate:

```text
.github/workflows/mesc-p01-04b2d-qualification.yml  b45811a2…
tests/_mesc_p01_04b2d_fixtures_v1.py                f35b4443…
tests/test_mesc_p01_04b2d_qualification_v1.py       ad215f71…
```

## The three remaining P01-04B gaps

```text
1. indivisible-group global minimum-deviation allocation   UNSATISFIED
2. atomic publication          NOT SATISFIED FOR P01-04B OVERALL
3. write-path protections      NOT SATISFIED FOR P01-04B OVERALL
```

This package addresses **gap 1 only**, and only prospectively.

## FD-BR-1 summary

```text
Recovery sequence:

1. Global minimum-deviation grouped allocation correction
2. Atomic publication and write-path protection boundary
3. Integrated P01-04B requalification and acceptance disposition
```

Each increment requires its own authorization, implementation, independent
review, acceptance and canonical adoption. Atomic publication and write-path
protections form one cohesive filesystem-publication boundary and must not be
implemented as independent, partially operable production surfaces. The
allocation correction must be accepted before publication work may be authorized,
and publication-boundary acceptance must precede final P01-04B requalification.

No increment is named `P01-04B2E`, because `P01-04E` is an existing official
downstream stage and the collision would be misleading.

## FD-BMD decision summary

```text
FD-BMD-1   private, library-only correction; public splitter stays fail-closed
FD-BMD-2   the accepted exact allocator is preserved, not replaced
FD-BMD-3   one private typed SplitAllocationError subclass is the only trigger
FD-BMD-4   one private exact-first / minimum-deviation resolver
FD-BMD-5   global constraints: indivisible groups, exact row and partition totals
FD-BMD-6   integer sum-of-squared-deviations objective, proven global minimum
FD-BMD-7   matrix tie-break: lexicographically smallest nine-cell vector
FD-BMD-8   assignment tie-break: lexicographically smallest partition-code vector
FD-BMD-9   complete deterministic reachable-state search; bounded to 1000/1000/3/3
FD-BMD-10  constraint-stress must succeed with score 6 and the selected matrix
FD-BMD-11  exact-reference and leakage-positive stay byte-identical
FD-BMD-12  facade integration only at the allocation call site
FD-BMD-13  capability becomes SATISFIED; P01-04B stays NOT ACCEPTED
FD-BMD-14  five activation conditions; one bounded four-path attempt
```

## Future implementation scope

```text
branch:
fix/mesc-p01-04b-minimum-deviation

subject:
fix(mesc): implement P01-04B minimum-deviation allocation

exactly four paths:
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_fixture_split_v1.py
tests/test_mesc_split_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py

no fifth path
```

Explicitly excluded and required to stay byte-identical:

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml
src/medscale/mesc/split.py
pyproject.toml
uv.lock
every prior governance package
```

The existing qualification workflow runs automatically through its existing path
filters; no workflow edit is authorized.

## Algorithm summary

```text
Try the accepted exact allocator first.
Return its result unchanged when it succeeds.

Only when it raises the private typed ranked-boundary failure,
resolve globally:

objective       sum((actual_cell - target_cell) ** 2) over nine cells
arithmetic      integers only — no float, no tolerance, no heuristic
constraints     indivisible groups; exact label row totals;
                exact overall partition totals; every example placed once
search          complete deterministic reachable-state dynamic programming
matrix order    yes/train, yes/validation, yes/test,
                no/train, no/validation, no/test,
                maybe/train, maybe/validation, maybe/test
matrix tie      lexicographically smallest nine-cell vector
assignment tie  lexicographically smallest partition-code vector
                (train = 0, validation = 1, test = 2)
bound           1000 examples / 1000 groups / 3 decisions / 3 partitions
```

Required constraint-stress outcome:

```text
target      386,83,83,237,50,51,77,17,16   exact target INFEASIBLE
minimum squared-deviation score            6
minimum-score matrices                     2
selected    386,82,84,238,50,50,76,18,16
runner-up   386,84,82,236,50,52,78,16,16
```

## Activation boundary

Canonical adoption and activation require all five conditions:

```text
1. genuinely independent clean-room exact-head review of this
   authorization package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
NO SUBSET ACTIVATES IMPLEMENTATION AUTHORITY.
```

Draft creation, independent review, Ready, merge, or merge without mechanical
verification is individually insufficient. The implementation authority is spent
when the single implementation commit is created, and implementation merge does
not equal implementation acceptance.

## Document index

```text
README.md                  — this overview
founder-authorization.md   — controlling
implementation-contract.md — future criterion-by-criterion contract
acceptance.md              — this package's documentation gate
```

- [`README.md`](README.md)
- [`founder-authorization.md`](founder-authorization.md) — **controlling**
- [`implementation-contract.md`](implementation-contract.md)
- [`acceptance.md`](acceptance.md)

On any conflict, [`founder-authorization.md`](founder-authorization.md) controls.

Prior governance history is adopted at
[`../p01-04/`](../p01-04/),
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/),
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/),
[`../p01-04b2c-authorization/`](../p01-04b2c-authorization/),
[`../p01-04b2c-acceptance/`](../p01-04b2c-acceptance/),
[`../p01-04b2d-authorization/`](../p01-04b2d-authorization/)
and
[`../p01-04b2d-acceptance/`](../p01-04b2d-acceptance/)
and is not restated here.

## Continuing prohibitions

```text
source or test changes outside the four-path future allowlist
workflow changes                   dependency or lockfile changes
public export                      CLI
filesystem publication             atomic publisher implementation
write-path implementation          real registry access
real source-record access          real split generation
real partition membership          real or canonical leakage audit
record-pair discovery              dataset or model download
model access                       inference
retrieval                          metrics
benchmark execution                training
fine-tuning                        adapter creation
publication                        clinical use
P01-04C through P01-04G            P01-05 or later
```

## What this package does not do

```text
does not implement the correction
does not activate implementation authority before adoption
does not replace or weaken the accepted exact allocator
does not make SourceDocumentGroupedSplitter.assign executable
does not change any artifact, serialization or leakage schema
does not change ALGORITHM_VERSION or SPLIT_SEED
does not modify any prior governance package
does not accept P01-04B
does not authorize atomic publication or write-path implementation
does not authorize a workflow edit or a fifth implementation path
does not authorize real dataset, registry or source-record access
does not authorize real split generation or real partition membership
does not authorize a real or canonical leakage audit
does not authorize dataset or model download, model access, inference,
  retrieval, metrics, benchmark execution, training, fine-tuning or
  adapter creation
does not authorize publication or clinical use
does not authorize P01-04C through P01-04G, or P01-05 or later
does not dispatch, rerun or cancel any workflow
```

A later, separately governed correction or remaining-tooling decision is eligible
for founder consideration.

```text
ELIGIBILITY IS NEVER AUTHORITY.
```
