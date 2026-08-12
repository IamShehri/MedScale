# P01-04B2D Acceptance — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Decision:
ACCEPT THE EXACT P01-04B2D IMPLEMENTATION, QUALIFICATION HARNESS,
AND BOUNDED SYNTHETIC QUALIFICATION EVIDENCE

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

Real split generation, real or canonical leakage-audit execution,
real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-03

Required canonical baseline:
`faf58c3fbfa9a83e7d392630e3ad1f322c616259`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`decision-basis.md`](decision-basis.md) or
[`acceptance.md`](acceptance.md), this document controls.

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
and is not restated here. Those packages are immutable historical authorities
and are not modified by this one.

---

## 1. FD-B2D-15 — Qualification acceptance and P01-04B non-acceptance

```text
FD-B2D-15 — P01-04B2D QUALIFICATION ACCEPTANCE
AND P01-04B NON-ACCEPTANCE DISPOSITION

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-03

Decision:
ACCEPT THE EXACT P01-04B2D IMPLEMENTATION,
QUALIFICATION HARNESS, AND BOUNDED SYNTHETIC
QUALIFICATION EVIDENCE.

P01-04B2D:
ACCEPTED IN SUBSTANCE;
NOT YET CANONICALLY ADOPTED.

Indivisible-group global minimum-deviation allocation:
UNSATISFIED.

Atomic publication:
NOT SATISFIED FOR P01-04B OVERALL.

Write-path protections:
NOT SATISFIED FOR P01-04B OVERALL.

Date-free canonical-byte invariant:
SATISFIED FOR THE SYNTHETIC B2D SURFACES;
DOES NOT ESTABLISH PROMOTABILITY.

P01-04B acceptance eligibility:
FALSE.

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED.

Production correction authority:
NOT GRANTED.

P01-04C through P01-04G:
NOT AUTHORIZED.
```

Acceptance is bounded to the exact implementation identity recorded in §3 and to
the contract adopted through the authorization package. It extends to no other
commit, tree, blob, path or behaviour, and to no later change.

No `UNSATISFIED`, `NOT SATISFIED` or `NOT APPLICABLE` result recorded anywhere in
this package is weakened, reinterpreted, aggregated away or silently overridden
by this decision.

## 2. Decision basis

The acceptance rests on all thirteen of the following, each evidenced in
[`decision-basis.md`](decision-basis.md):

```text
 1. FD-B2D-1 through FD-B2D-14 were validly adopted before implementation
 2. the five FD-B2D-14 activation conditions were satisfied before the
    implementation commit was created
 3. the implementation stayed within the exact three-path allowlist
 4. no production module, dependency, lockfile, public export, CLI or
    entry point was changed
 5. the implementation conformed to implementation-contract.md sections 1-16
 6. the complete required fixture, literal-golden-vector and criterion suite
    was present
 7. an independent clean-room exact-head implementation review found no
    blocking finding
 8. exact-head CI and CodeQL passed
 9. the exact-head six-cell qualification workflow passed in all six cells
10. Ready was separately founder-authorized and executed
11. merge was separately founder-authorized and executed
12. the canonical merge preserved the reviewed tree, paths and blobs
13. mechanical post-merge verification passed, and the post-merge
    push-triggered CI, CodeQL and six-cell qualification runs passed
```

No criterion is waived, substituted or inferred from merge alone. A merge event
by itself evidences criteria 11 and 12 only, and never criteria 1 through 10 or
criterion 13.

## 3. Exact accepted implementation identity

```text
Authorization package:
PR #77 — MERGED / CLOSED / NOT DRAFT

Authorization reviewed head:
096f6667251b4783fc9511336301dfaaa4c7f336

Authorization reviewed tree:
30b4cb5433a7f8496e62b8a94d879cf34a8ff26a

Authorization canonical merge:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Adopted authority:
FD-B2D-1 through FD-B2D-14
```

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

Exactly three paths, identified by path and blob rather than by restated source:

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

No fourth path exists in the accepted change. `src/`, `docs/`, `specs/`,
`pyproject.toml`, `uv.lock`, every pre-existing test and every pre-existing
workflow are byte-identical to their pre-implementation state.

`tests/_mesc_p01_04b2d_fixtures_v1.py` remains a non-promotable, non-package
test helper. It is not importable from `medscale`, is referenced by no
production file, and is not made promotable by this acceptance.

## 4. Exact qualification and workflow basis

```text
Independent clean-room exact-head implementation review:
APPROVE WITH NON-BLOCKING NOTES

Blocking findings:
NONE

Reviewed head:
6e5867829006770ad2ed50f26a9af0c455923594

Reviewed tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1
```

Pull-request-triggered checks at the exact reviewed head:

```text
CI run 30780440275                          completed / success
  quality (py3.11)                          completed / success
  quality (py3.12)                          completed / success

CodeQL run 30780440276                      completed / success
  analyze (python)                          completed / success

MESC P01-04B2D Qualification run 30780440318  completed / success
  qualification (ubuntu-latest py3.11)      completed / success
  qualification (ubuntu-latest py3.12)      completed / success
  qualification (windows-latest py3.11)     completed / success
  qualification (windows-latest py3.12)     completed / success
  qualification (macos-latest py3.11)       completed / success
  qualification (macos-latest py3.12)       completed / success
```

Post-merge push-triggered runs at the canonical merge commit:

```text
CI run 30781355622                          SUCCESS — 2/2 jobs
CodeQL run 30781355591                      SUCCESS — 1/1 job
MESC P01-04B2D Qualification run 30781355599  SUCCESS — 6/6 jobs
```

Success in all six operating-system and runtime cells against a single set of
committed literal golden vectors, with no operating-system-specific expected
value anywhere in the suite, is the cross-runtime byte-identity evidence this
acceptance rests on.

```text
Workflow success is qualification-harness evidence only.

It is not scientific evidence, not clinical evidence, not dataset evidence,
not a real split, and not a real or canonical leakage audit.
```

## 5. Accepted non-blocking observations

The independent clean-room exact-head implementation review returned
`APPROVE WITH NON-BLOCKING NOTES` with **no blocking finding**. All nine
observations are carried forward here in full and disposed of. None is deferred,
and none creates authority to change the accepted implementation.

### NB-1 — criterion-4 test reads repository source from disk

```text
Observed behavior:
test_criterion_04_no_b2_cli_exists resolves src/medscale/cli/*.py relative to
the test file and reads those files from disk. Against an installed
distribution rather than a source checkout the glob would be empty and the
criterion would pass vacuously.

Scope:
One criterion test in tests/test_mesc_p01_04b2d_qualification_v1.py.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
Every authorized qualification cell checks the repository out before running,
so the glob is never empty in the governed execution path. The read is
explicit, deterministic and identical on every runner, and no golden value
depends on it. The reviewer separately confirmed by source inspection that no
CLI module references the fixture facade.

Correction authorized:
NO.
```

### NB-2 — duplicated file read in the same criterion test

```text
Observed behavior:
The same criterion-4 test calls read_text once per operand of a boolean or,
reading each file twice.

Scope:
One expression in one criterion test.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
Cosmetic. The assertion, its failure behavior and its result are unaffected.

Correction authorized:
NO.
```

### NB-3 — workflow omits a runtime uv-version assertion

```text
Observed behavior:
The qualification workflow pins the uv version explicitly through the setup
action input but, unlike the baseline portability workflow, contains no
separate step asserting the resolved uv version at run time.

Scope:
.github/workflows/mesc-p01-04b2d-qualification.yml.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
FD-B2D-8 and implementation-contract.md section 9 require an explicit pinned
uv version, which the workflow supplies, together with a SHA-pinned checkout
action, a SHA-pinned setup action, persist-credentials disabled and a locked
sync. The reviewer verified both action pins resolve to the claimed releases
and are byte-identical to the accepted baseline convention. The absent step is
a strengthening of that convention, not a required element of it.

Correction authorized:
NO.
```

### NB-4 — date-free probes are raw substrings

```text
Observed behavior:
The criterion-13 date-free assertion scans canonical byte surfaces for raw
substrings such as date and command. Such a probe would also match an
innocuous longer word that happens to contain the substring.

Scope:
One criterion test asserting the date-free canonical-byte invariant.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
The assertion is conservative in the safe direction: it can only over-report,
never under-report, a forbidden runtime token. No canonical B2D surface
contains such a word, and the invariant it protects holds. The observation
concerns probe precision, not an incorrect byte surface.

Correction authorized:
NO.
```

### NB-5 — context surfaces tokenized through the question token-set helper

```text
Observed behavior:
The approximate-context-overlap scenario tokenizes its context surfaces
through the accepted question token-set helper. The declared detection-method
tuple names the two underlying primitives rather than the composed helper that
is actually invoked.

Scope:
One leakage scenario in the qualification suite.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
The accepted B2B surface exposes no context-specific token-set helper;
context_token_set exists only as an allowlisted shared-surface marker. The
composed helper is exactly the tokenizer applied to the normalized string, so
the computation is the ratified one, and the declared detection-method tuple
remains truthful because it names both primitives the composition uses. The
scenario produced the exact frozen intersection, union, score representation
and threshold result.

Correction authorized:
NO.
```

### NB-6 — typed-failure assertion freezes a production message string

```text
Observed behavior:
The constraint-stress assertion freezes the verbatim boundary-crossing message
emitted by the accepted allocation function, including its grammatical
imperfection, rather than asserting only the error type and structured
semantics.

Scope:
One frozen literal in the qualification suite.

Founder disposition:
ACCEPTED — NON-BLOCKING.

Why non-blocking:
FD-B2D-11 requires the qualification to fail closed on any drift, so freezing
the exact message is a stronger assertion than the contract's minimum, not a
weaker one. The accepted B1 layer is frozen and cannot be reworded without a
separate founder decision. Stable semantics are additionally asserted
independently of the message text through the frozen crossing rank, the
frozen placed-example count and the frozen boundary identity.

Correction authorized:
NO.
```

### NB-7 — local full-suite deviation traceable to shell resolution

```text
Observed behavior:
When the reviewer ran the project-wide suite from a shell where the resolved
bash executable was a subsystem stub unable to resolve native paths, 54 tests
in the pre-existing B2A portability test module failed. Re-running the same
tree with a conforming bash first on the search path produced 1734 passed and
2 skipped.

Scope:
Local developer environment. A pre-existing test module untouched by this
implementation.

Founder disposition:
ACCEPTED — NON-BLOCKING; ENVIRONMENTAL, NOT AN IMPLEMENTATION OBSERVATION.

Why non-blocking:
The accepted change modifies no source, no pre-existing test and no
pre-existing workflow, so it cannot affect that module. The authorized CI and
qualification cells passed. The reviewer isolated the cause mechanically.

Correction authorized:
NO.
```

### NB-8 — local type-check deviation under an extras-installed tree

```text
Observed behavior:
Running the type checker over a tree synchronized with all optional extras
fails inside a third-party stub that uses syntax newer than the configured
target version. The locked synchronization the canonical gate and CI use
passes cleanly over 177 source files.

Scope:
Local developer environment. Pre-existing project configuration.

Founder disposition:
ACCEPTED — NON-BLOCKING; ENVIRONMENTAL, NOT AN IMPLEMENTATION OBSERVATION.

Why non-blocking:
The accepted change adds no dependency and modifies neither the project
metadata nor the lockfile. The gate CI executes passed.

Correction authorized:
NO.
```

### NB-9 — helper import mutates the interpreter search path

```text
Observed behavior:
The qualification module inserts the test directory onto the interpreter
search path at import time so the non-package fixture helper can be imported,
which mutates that path for the whole session.

Scope:
Three lines at the top of tests/test_mesc_p01_04b2d_qualification_v1.py.

Founder disposition:
ACCEPTED — NON-BLOCKING; ESTABLISHED HOUSE PATTERN.

Why non-blocking:
It reproduces the accepted B2A portability precedent exactly. FD-B2D-1
requires the helper to be a non-package, non-promotable test-only module,
which is precisely what makes this import form necessary. Linting and
formatting gates pass, and the pattern is recorded for completeness rather
than as drift.

Correction authorized:
NO.
```

### Effect of accepting these observations

```text
All independent-review non-blocking notes:
ACCEPTED AS NON-BLOCKING

Correction authorization:
NOT ISSUED

Deferred implementation obligation:
NONE CREATED BY THIS PACKAGE
```

No follow-up source commit, test commit, workflow commit, contract amendment,
public export, behavioural extension or scope expansion is authorized by
accepting these notes. None of NB-1 through NB-9 is a deferred obligation, a
conditional acceptance, a remediation commitment or a scheduled follow-up.

## 6. Fixture disposition

### `exact-reference-1000-v1`

```text
Rows:                              1000
Source-document groups:            89
Partition totals:                  700 / 150 / 150
Label totals:                      552 / 338 / 110
Exact ratified matrix:             REPRODUCED
Indivisible group placement:       CONFORMING
Cross-platform deterministic literals: SATISFIED
```

### `constraint-stress-1000-v1`

```text
Rows:                              1000
Groups:                            500
Group size:                        2
Exact target:                      PROVABLY INFEASIBLE
Global minimum squared-deviation score: 6
Number of score-6 matrices:        2
Lexicographic selected matrix:     386,82,84,238,50,50,76,18,16
Runner-up:                         386,84,82,236,50,52,78,16,16
Current production minimum-deviation fallback: ABSENT
Accepted facade behavior:          TYPED FAIL-CLOSED
Minimum-deviation production capability: UNSATISFIED
```

```text
The typed fail-closed allocation failure is the correct detection and
classification of a missing capability.

It is NOT implementation conformance to the required global
minimum-deviation allocation, and it must never be recorded as such.
```

### `leakage-positive-v1`

```text
Rows:                              1000
Source-document groups:            999
Two-example groups:                1
Singleton groups:                  998
Findings:                          9
false_positive:                    3
unresolved:                        6
leaked:                            true
suppressed:                        0
```

Preserved semantic boundary:

```text
The exact-example self-identity and exact-source-document same-group
scenarios are same-partition synthetic controls.

They do not establish cross-partition leakage, duplicate split membership,
source-document overlap, real leakage, or canonical leakage evidence.
```

## 7. Thirteen-criterion disposition

```text
 1. SourceDocumentGroupedSplitter.assign remains unconditionally fail-closed
    SATISFIED

 2. FixtureSplitFacade exists as the separate fixture-only facade
    SATISFIED

 3. Qualification is library-only and in-memory
    SATISFIED

 4. No B2 CLI exists
    SATISFIED

 5. 64-hex split_fingerprint is authoritative
    SATISFIED

 6. 16-hex split_hash is compatibility/display only
    SATISFIED

 7. Leakage normalization follows FD-B2-6
    SATISFIED

 8. Exactly the three named fixtures form the suite
    SATISFIED

 9. Stable synthetic inputs produce byte-identical results
    SATISFIED

10. No real P01-03G membership is generated or disclosed
    SATISFIED

11. Atomic publication
    NOT APPLICABLE TO B2D
    NOT SATISFIED FOR P01-04B OVERALL

12. Write-path protections
    NOT APPLICABLE TO B2D
    NOT SATISFIED FOR P01-04B OVERALL

13. Date-free promotable artifacts
    NOT APPLICABLE TO B2D OUTPUT PROMOTION
    DATE-FREE CANONICAL-BYTE INVARIANT SATISFIED
    DOES NOT ESTABLISH PROMOTABILITY
```

Recorded separately, outside the thirteen numbered criteria:

```text
Indivisible-group global minimum-deviation allocation (FD-B2-7 Fixture B):
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

NOT APPLICABLE IS NEVER CONVERTED TO SATISFIED, NEVER COUNTS TOWARD
P01-04B ACCEPTANCE, AND RECORDS ONLY THAT B2D CANNOT QUALIFY THE CRITERION.
```

Criterion 13's disposition class remains `NOT APPLICABLE`. The satisfied
date-free canonical-byte invariant is a separate bounded result about the
synthetic B2D byte surfaces and does not convert that class, does not make any
B2D output promotable, and does not satisfy repository promotion or publication
acceptance.

## 8. P01-04B decision

```text
P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

Reason:
The indivisible-group global minimum-deviation allocation capability required
by FD-B2-7 Fixture B is UNSATISFIED, and the atomic-publication and
write-path-protection criteria are NOT SATISFIED FOR P01-04B OVERALL.

Production correction authority:
NOT GRANTED.
```

Accepting the qualification harness and its bounded synthetic evidence accepts
what the harness proved. It does not accept the capability the harness proved to
be missing. A production implementation of globally minimum-deviation grouped
allocation, an atomic-publication component or a write-path-protection component
each requires its own separate founder authorization, its own contract, its own
independent review and its own acceptance decision.

Such later, separately governed decisions are **eligible for founder
consideration**. This package authorizes none of them.

## 9. Adoption conditions — all five required

```text
1. genuinely independent clean-room exact-head review of this acceptance package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset canonically adopts FD-B2D-15.

No subset canonically accepts P01-04B2D.
```

Local commit creation activates nothing. Draft creation activates nothing.
Review approval alone, Ready alone, merge alone, review plus merge, and merge
without mechanical verification are each insufficient.

## 10. Classification before canonical adoption

While this package is local, Draft, Ready-but-unmerged, or
merged-but-not-mechanically-verified:

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

P01-04B2D must not be described as canonically accepted merely because this
local package exists.

## 11. Classification after canonical adoption

Only after all five adoption conditions of §9 pass:

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

P01-04B2D acceptance closes the B2 qualification sub-phase only. It does not
complete P01-04B, does not create eligibility for P01-04C, and does not convert
any unsatisfied or inapplicable criterion.

## 12. Continuing prohibitions

Before and after canonical adoption, FD-B2D-15 does not authorize:

```text
minimum-deviation production correction
atomic-publication implementation
write-path implementation
correction, amendment or extension of the accepted implementation
modification of any accepted B1, B2A, B2B or B2C module
modification of any prior governance package
real dataset or registry access
real source-record access
real split generation
real partition membership
real or canonical leakage audit
leakage-audit orchestration over a collection
generic record-pair discovery or automatic finding discovery
dataset download
model download
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
CLI, filesystem publication or public package export
promotion of any B2D output or fixture helper
P01-04B whole-phase acceptance
P01-04C through P01-04G
P01-05 or later
a second commit on this package
amendment, rebase, squash, reset, cherry-pick or force-push
marking this package's pull request Ready
merging this package
auto-merge
deleting any branch
any workflow dispatch, rerun or cancellation
```

## 13. Downstream separation and standing status

```text
P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

P01-05 or later:
NOT AUTHORIZED
```

B2D acceptance is separated from P01-04B acceptance by an explicit unsatisfied
criterion, and P01-04B acceptance is separated from any downstream phase by its
own separate founder decision. No chain of eligibility substitutes for either.

The bounded P01-04B2D implementation authority was exercised exactly once and is
spent. It does not authorize a second attempt, a correction series or a
follow-up expansion. No execution authority of any kind is created by this
disposition.
