# P01-04B Minimum-Deviation Correction — Founder Authorization

```text
Status:
FOUNDER AUTHORIZATION RECORDED

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

Founder:
Abdulaziz M. Alshehri

Decision date:
2026-08-03

Required canonical baseline:
`3513d66bc36650363a6368bb4e42901119419802`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`implementation-contract.md`](implementation-contract.md) or
[`acceptance.md`](acceptance.md), this document controls.

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
and is not restated here. Those packages are immutable historical authorities
and are not modified by this one.

---

## 1. Exact canonical baseline

```text
Repository:
IamShehri/MedScale

Required canonical main:
3513d66bc36650363a6368bb4e42901119419802

Required canonical tree:
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

This package is bound to that exact baseline and is not rebased onto a later
`main`.

## 2. Canonical state entering this decision

```text
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

Indivisible-group global minimum-deviation capability:
UNSATISFIED

Atomic publication:
NOT SATISFIED FOR P01-04B OVERALL

Write-path protections:
NOT SATISFIED FOR P01-04B OVERALL

P01-04B acceptance eligibility:
FALSE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Production correction authority:
NOT GRANTED BEFORE THIS PACKAGE IS CANONICALLY ADOPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

The accepted B2D qualification correctly detected the missing capability. Its
typed failure was never conformance to that capability, and nothing in this
package retroactively converts that historical result.

## 3. Accepted B2D identity

The correction is authorized against, and must preserve, this exact accepted
implementation:

```text
Authorization PR:
#77 — MERGED / CLOSED / NOT DRAFT
reviewed head 096f6667251b4783fc9511336301dfaaa4c7f336
reviewed tree 30b4cb5433a7f8496e62b8a94d879cf34a8ff26a
canonical merge 63cefe04c23726957aa26ac60ca8087ac9ca333a
adopted authority FD-B2D-1 through FD-B2D-14

Implementation PR:
#78 — MERGED / CLOSED / NOT DRAFT
branch test/mesc-p01-04b2d-qualification
reviewed and merged head 6e5867829006770ad2ed50f26a9af0c455923594
reviewed tree 3d27b9c43462ef9880d5fab1ea45b675d5ff55c1
canonical merge faf58c3fbfa9a83e7d392630e3ad1f322c616259
1 commit / 3 files / 3223 additions / 0 deletions

Acceptance PR:
#79 — MERGED / CLOSED / NOT DRAFT
branch docs/mesc-p01-04b2d-acceptance
reviewed head c38473d69c996e626510256d6297640bd87405ad
canonical merge 3513d66bc36650363a6368bb4e42901119419802
5 files / 2188 additions / 0 deletions
adopted authority FD-B2D-15
```

Accepted B2D implementation blobs, which this correction must not invalidate:

```text
.github/workflows/mesc-p01-04b2d-qualification.yml
blob b45811a2e104e61149c766b39d3c1ad832959b69

tests/_mesc_p01_04b2d_fixtures_v1.py
blob f35b4443e79338d2309ca9f4197eee8368ea7069

tests/test_mesc_p01_04b2d_qualification_v1.py
blob ad215f717ef1b27bc7adbfb5c68d81e91ccfc6dd
```

## 4. The three remaining P01-04B gaps

```text
Gap 1 — indivisible-group global minimum-deviation allocation
UNSATISFIED. The accepted allocator performs exact-target allocation only and
fails closed at a ranked boundary crossing. No global minimum-deviation
fallback exists.

Gap 2 — atomic publication
NOT SATISFIED FOR P01-04B OVERALL. No filesystem publication component exists.

Gap 3 — write-path protections
NOT SATISFIED FOR P01-04B OVERALL. No write path exists to protect.
```

This package addresses **Gap 1 only**, and only prospectively.

## 5. FD-BR-1 — P01-04B recovery architecture

```text
FD-BR-1 — P01-04B RECOVERY ARCHITECTURE

Founder:
Abdulaziz M. Alshehri

Decision date:
2026-08-03

Selected recovery sequence:

1. Global minimum-deviation grouped allocation correction
2. Atomic publication and write-path protection boundary
3. Integrated P01-04B requalification and acceptance disposition

The three increments require separate authorization,
implementation, independent review, acceptance and canonical adoption.

Atomic publication and write-path protections form one cohesive
filesystem-publication boundary and must not be implemented as
independent, partially operable production surfaces.

The allocation correction must be accepted before publication work
may be authorized.

The allocation correction does not authorize publication.

Publication-boundary acceptance must precede final P01-04B
requalification.

No recovery increment is named P01-04B2E because P01-04E is an
existing official downstream stage.

P01-04C through P01-04G remain unauthorized.
```

Increment 1 is the only increment this package authorizes, and it is authorized
only prospectively, subject to §20.

## 6. FD-BMD-1 — Private correction boundary

```text
FD-BMD-1 — PRIVATE CORRECTION BOUNDARY

The correction remains private and library-only.

SourceDocumentGroupedSplitter.assign():
REMAINS UNCONDITIONALLY FAIL-CLOSED

No public export
No CLI
No filesystem input
No filesystem output
No real-data adapter
No registry adapter
No formal executor
```

`SourceDocumentGroupedSplitter.assign` must continue to raise
`PilotSplitNotAuthorizedError` on every call, with no conditional path, no flag,
no environment switch and no argument value that permits execution. Formal
dataset membership remains separately authorized work that this package does not
grant.

## 7. FD-BMD-2 — Preserve the accepted exact allocator

```text
FD-BMD-2 — PRESERVE THE ACCEPTED EXACT ALLOCATOR

allocate_indivisible_groups:
REMAINS THE ACCEPTED EXACT-TARGET ALLOCATOR

Its supported exact-feasible behaviour must not be replaced,
weakened or silently reinterpreted.

Every currently successful exact-feasible request must retain
byte-identical assignments, registries, summaries, hashes and
fingerprints.
```

The minimum-deviation correction is an **additional private capability**, not a
rewrite of accepted exact behaviour. `allocate_indivisible_groups` keeps its
name, signature, exact-target semantics, validation order, error semantics and
returned ordering.

The accepted returned ordering, which the registries and every canonical byte
surface depend on, is:

```text
partition order   train, validation, test
then decision order   yes, no, maybe
then partition_key
then source_document_id
then min(row_ordinals)
```

## 8. FD-BMD-3 — Typed fallback trigger

```text
FD-BMD-3 — TYPED FALLBACK TRIGGER

One private typed subclass of SplitAllocationError is permitted,
representing an exact ranked-boundary allocation failure.

Required properties:
subclass of SplitAllocationError
private
deterministic
message stable
not publicly exported
```

The facade may invoke the minimum-deviation resolver **only** after the accepted
exact allocator raises this specific typed boundary failure.

The resolver must **not** be invoked for:

```text
malformed input
duplicate identity
inconsistent dataset identity
invalid target keys
negative totals
label/partition grand-total mismatch
observed/expected label-total mismatch
internal invariant failure
unknown exception
```

```text
NO FALLBACK MAY DEPEND ON PARSING AN EXCEPTION MESSAGE.
```

The accepted allocator raises `SplitAllocationError` at four distinct sites. Only
one is a ranked-boundary crossing, and only that one may carry the new subclass:

```text
AUTHORIZED TRIGGER
the ranked-boundary crossing raise —
"group ... of size N would cross the <decision>/<partition> boundary
 with R places remaining"

NOT A TRIGGER
the observed/expected label-total mismatch raise
the "allocation did not exhaust targets" raise
the controlled-rounding "no valid controlled-rounding matrix exists" raise
```

Discrimination must be by exception **class**, never by message text, message
prefix, regular expression, string containment or argument inspection.

## 9. FD-BMD-4 — Private resolver

```text
FD-BMD-4 — PRIVATE RESOLVER
```

One private function is authorized, provisionally named:

```python
allocate_indivisible_groups_with_minimum_deviation(
    examples: Sequence[LabeledExample],
    targets: Sequence[LabelTarget],
) -> tuple[GroupAssignment, ...]
```

The exact final private name may vary only if the implementation report explains
why, but its behaviour and boundary must remain identical.

It must:

```text
try the accepted exact allocation first
return its exact result unchanged when successful
invoke the global resolver only for the authorized typed boundary failure
return the globally selected assignment
raise a typed SplitAllocationError subclass if no partition-total-feasible
  assignment exists
```

The returned tuple must carry the same `GroupAssignment` type and the same final
ordering defined in §7, so that every downstream registry, summary, hash and
fingerprint is constructed from a canonically ordered sequence.

## 10. FD-BMD-5 — Global constraints

```text
FD-BMD-5 — GLOBAL CONSTRAINTS

The resolver must assign every ranked source-document group exactly once
to exactly one of:
train
validation
test

It must enforce:
all groups indivisible
zero cross-partition group overlap
all examples assigned exactly once
exact label row totals
exact overall partition totals
no excluded examples
no duplicated examples
no omitted groups
```

A cell may deviate from its target **only** because indivisible-group constraints
make the exact target matrix unavailable. Deviation is never a convenience, a
tolerance, a rounding allowance or a performance shortcut.

Note the asymmetry that makes this correction coherent: label **row** totals and
overall **partition** totals remain exact; only the nine interior cells may
deviate, and only minimally.

## 11. FD-BMD-6 — Objective

```text
FD-BMD-6 — OBJECTIVE
```

The nine actual matrix cells use this exact order:

```text
yes/train
yes/validation
yes/test
no/train
no/validation
no/test
maybe/train
maybe/validation
maybe/test
```

The corresponding target cells are the accepted `LabelTarget` values.

The objective is exactly:

```text
sum((actual_cell - target_cell) ** 2 for all nine cells)
```

Requirements:

```text
integer arithmetic only
no binary floating point
no approximate comparison
no tolerance
no heuristic objective
no weighted objective
no normalized objective
```

The selected result must be a **proven global minimum** over all assignments
satisfying FD-BMD-5. A search that merely fails to find a better answer is not a
proof; the implementation must establish that no better answer can exist.

## 12. FD-BMD-7 — Matrix tie-break

```text
FD-BMD-7 — MATRIX TIE-BREAK

When more than one feasible matrix has the same minimum score, select the
lexicographically smallest nine-cell actual matrix in the exact order
defined by FD-BMD-6.
```

For `constraint-stress-1000-v1` this selects:

```text
386,82,84,238,50,50,76,18,16
```

over:

```text
386,84,82,236,50,52,78,16,16
```

Both have score `6`. The two vectors first differ at index 1
(`yes/validation`), where `82 < 84`.

## 13. FD-BMD-8 — Assignment tie-break

```text
FD-BMD-8 — ASSIGNMENT TIE-BREAK

If multiple group assignments produce the selected matrix, choose the
lexicographically smallest partition-code vector.

Canonical vector order:

decision order:
yes, no, maybe

within each decision:
the existing rank_groups ordering

partition codes:
train = 0
validation = 1
test = 2
```

```text
No dictionary insertion order, set order, filesystem order, process
scheduling, platform behavior or random source may affect the selected
assignment.
```

The existing `rank_groups` ordering is the accepted deterministic rank:

```text
partition_key
then source_document_id
then min(row_ordinals)
```

where `partition_key` is the accepted SHA-256 over the ratified D6 payload of
`algorithm_version`, `seed`, `source_document_id` and `stratum`.

## 14. FD-BMD-9 — Complete deterministic search

```text
FD-BMD-9 — COMPLETE DETERMINISTIC SEARCH

The implementation must prove global optimality through a complete
deterministic reachable-state algorithm.

Required architecture:
dynamic programming over reachable integer count states
per-decision reachable matrices
global combination enforcing exact partition totals
canonical predecessor and tie-break retention

Prohibited:
greedy approximation presented as global
random search
beam search
local search
external solver dependency
platform-native optimizer
subprocess
network operation
3**group_count brute-force enumeration
floating-point optimization
```

The implementation may optimize memory or predecessor storage, but must preserve
the exact complete state set and tie-break semantics.

The correction is bounded to at most:

```text
1000 examples
1000 source-document groups
3 decisions
3 partitions
```

Inputs beyond that correction boundary fail closed using a private typed
allocation error. The bound is a governance boundary, not a performance
heuristic: an input outside it is refused, never approximated.

## 15. FD-BMD-10 — Constraint-stress required result

```text
FD-BMD-10 — CONSTRAINT-STRESS REQUIRED RESULT

fixture:
constraint-stress-1000-v1

rows:
1000

groups:
500

group size:
2

target matrix:
386,83,83,237,50,51,77,17,16

exact target:
INFEASIBLE

global minimum squared-deviation score:
6

number of minimum-score matrices:
2

selected matrix:
386,82,84,238,50,50,76,18,16

runner-up:
386,84,82,236,50,52,78,16,16
```

After implementation, the fixture must produce a successful deterministic
in-memory `FixtureSplitResult`.

The implementation test must freeze literal values for:

```text
request identity
split_hash
split_fingerprint
all six canonical byte-surface SHA-256 values
all six canonical byte sizes
partition counts
group counts
actual label matrix
target label matrix
per-cell deviations
minimum score
selected matrix
runner-up matrix
```

The six canonical byte surfaces are:

```text
group_registry_bytes
example_registry_bytes
excluded_ledger_bytes
split_summary_identity_core_bytes
split_summary_document_bytes
audit_report_bytes
```

```text
Literal goldens must not be regenerated automatically, updated by a flag,
or approved from the result under test.
```

Infeasibility of the exact target is mechanical, not asserted: every group has
size 2 and no group may cross a partition or a decision stratum, so every
realized cell must be even, while the ratified target contains six odd-valued
cells (`yes/validation 83`, `yes/test 83`, `no/train 237`, `no/test 51`,
`maybe/train 77`, `maybe/validation 17`) comprising five distinct odd values
because 83 occurs twice.

## 16. FD-BMD-11 — Exact-feasible non-regression

```text
FD-BMD-11 — EXACT-FEASIBLE NON-REGRESSION

The following accepted fixtures must remain byte-identical:
exact-reference-1000-v1
leakage-positive-v1
```

Required unchanged values include:

```text
fixture SHA-256
request ID
split_hash
split_fingerprint
every canonical byte surface
every canonical byte-surface digest
every canonical byte size
partition counts
label matrix
group counts
ordered leakage finding IDs
audit classifications
```

The correction **completes** the existing ratified split-algorithm version. It
must not bump or silently change:

```text
ALGORITHM_VERSION
SPLIT_SEED
canonical serialization versions
artifact schema versions
leakage schema versions
fixture identity schema
request identity schema
```

The constraint-stress result has no prior successful artifact identity, so
freezing its first successful result creates no identity conflict.

## 17. FD-BMD-12 — Facade integration

```text
FD-BMD-12 — FACADE INTEGRATION

FixtureSplitFacade.run() may change only to use the authorized
exact-first/minimum-deviation allocation path.

It must remain:
private
unexported
stateless
in-memory
fixture-only
non-evidence
without path inputs
without path outputs
without I/O
without environment reads
without network
without subprocess
without publication
```

```text
No result field may be added, removed or renamed.
No B2A, B2B or B2C artifact schema may change.
```

The twelve-field `FixtureSplitResult` is frozen exactly as accepted:

```text
request_id
split_manifest
group_registry_bytes
example_registry_bytes
excluded_ledger_bytes
split_summary_identity_core
split_summary_identity_core_bytes
split_summary_document_bytes
split_fingerprint_record
audit_report
audit_report_bytes
execution_evidence_ref
```

The accepted twelve-step validation order is controlling and unchanged. In
particular, fixture-identity verification and request-identity verification must
continue to execute **before** allocation, so that reaching any allocation
outcome still proves both identity digests are the real ones.

The actual matrix and score may be independently derived and recorded by the
qualification suite without changing the frozen twelve-field
`FixtureSplitResult`.

## 18. FD-BMD-13 — Qualification disposition after correction

```text
FD-BMD-13 — QUALIFICATION DISPOSITION AFTER CORRECTION

The revised B2D qualification must report:

Indivisible-group global minimum-deviation capability:
SATISFIED

Atomic publication:
NOT SATISFIED FOR P01-04B OVERALL

Write-path protections:
NOT SATISFIED FOR P01-04B OVERALL

P01-04B acceptance eligibility:
FALSE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED
```

The correction must remove the obsolete expected typed-failure assertion for
`constraint-stress-1000-v1` and replace it with the successful literal-golden
qualification.

```text
It must not rewrite historical governance documents that truthfully record
the pre-correction UNSATISFIED result.

A successful correction does not retroactively make those historical
records false.

No aggregate may treat NOT APPLICABLE TO THIS CORRECTION as satisfaction of
the two remaining P01-04B requirements.
```

Satisfying Gap 1 does not satisfy Gap 2 or Gap 3, and does not make P01-04B
eligible for acceptance.

## 19. FD-BMD-14 — Activation and bounded implementation

```text
FD-BMD-14 — ACTIVATION AND BOUNDED IMPLEMENTATION

The future implementation authority activates only after all five:

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

After activation, exactly the following is authorized:

```text
one implementation branch
one normal implementation commit
four changed paths
one bounded implementation attempt
```

Future branch:

```text
fix/mesc-p01-04b-minimum-deviation
```

Future subject:

```text
fix(mesc): implement P01-04B minimum-deviation allocation
```

Exact future implementation paths:

```text
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_fixture_split_v1.py
tests/test_mesc_split_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
```

```text
NO FIFTH PATH.
```

In particular, `tests/_mesc_p01_04b2d_fixtures_v1.py`,
`.github/workflows/mesc-p01-04b2d-qualification.yml`, `src/medscale/mesc/split.py`,
`pyproject.toml` and `uv.lock` are **not** in the allowlist and must remain
byte-identical.

The implementation authority is **spent** when the implementation commit is
created.

A defect after commit requires:

```text
STOP
REPORT
NO AMEND
NO SECOND COMMIT
SEPARATE FOUNDER CORRECTION AUTHORIZATION
```

```text
IMPLEMENTATION MERGE DOES NOT EQUAL IMPLEMENTATION ACCEPTANCE.
```

After implementation merge and mechanical verification, a separate
implementation-acceptance disposition and canonical adoption are required. Only
after that acceptance may the atomic-publication/write-path-protection
authorization package be considered.

## 20. Pre-adoption state

While this package is local, Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified:

```text
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

Local commit creation activates nothing. Draft creation activates nothing.
Review approval alone, Ready alone, merge alone, review plus merge, and merge
without mechanical verification are each insufficient.

## 21. Post-adoption state

Only after all five activation conditions of §19 pass:

```text
FD-BR-1:
ADOPTED ON CANONICAL MAIN

FD-BMD-1 THROUGH FD-BMD-14:
ADOPTED ON CANONICAL MAIN

MINIMUM-DEVIATION IMPLEMENTATION AUTHORITY:
ACTIVE FOR ONE BOUNDED FOUR-PATH ATTEMPT

MINIMUM-DEVIATION IMPLEMENTATION:
AUTHORIZED TO BEGIN EXACTLY ONCE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

ATOMIC PUBLICATION / WRITE-PATH IMPLEMENTATION:
NOT AUTHORIZED

P01-04C THROUGH P01-04G:
NOT AUTHORIZED
```

P01-04B remains not accepted in **both** states. Adoption of this package
activates one bounded implementation attempt and nothing else.

## 22. Continuing prohibitions

Before and after canonical adoption, this package does not authorize:

```text
source or test changes outside the exact four-path allowlist
workflow changes
dependency changes
lockfile changes
public export
CLI
filesystem publication
atomic publisher implementation
write-path implementation
real registry access
real source-record access
real split generation
real partition membership
real or canonical leakage audit
record-pair discovery
dataset or model download
model access
inference
retrieval
metrics
benchmark execution
training
fine-tuning
adapter creation
publication
clinical use
P01-04C through P01-04G
P01-05 or later
modification of any prior governance package
a second commit on this package
amendment, rebase, squash, reset, cherry-pick or force-push
marking this package's pull request Ready
merging this package
auto-merge
deleting any branch
any workflow dispatch, rerun or cancellation
```

The later publication boundary is eligible for consideration only after the
minimum-deviation implementation is separately accepted.

```text
ELIGIBILITY IS NOT AUTHORITY.
```

## 23. Non-execution record

Building this package performed no execution of any kind:

```text
no fixture constructed
no facade invoked
no split executed
no leakage audit executed
no allocation performed
no digest, request identifier, split hash or fingerprint calculated
no workflow dispatched, rerun or cancelled
no real dataset, registry or source-record access
no model access, inference, retrieval or metrics
no training, fine-tuning or adapter creation
no publication and no clinical use
no repository setting changed
```

Every value recorded here was read from the repository at the exact baseline or
queried read-only from the hosting service.
