# P01-04B2D Acceptance — Decision Basis

```text
Status:
IMMUTABLE EVIDENCE LEDGER

Package status:
RECORDED — NOT ADOPTED
```

This document records the evidence on which
[`founder-disposition.md`](founder-disposition.md) rests. It creates no
authority. On any conflict, [`founder-disposition.md`](founder-disposition.md)
controls.

Evidence is separated by kind so no class is mistaken for another:

```text
§1 - §6    repository evidence
§7 - §8    GitHub workflow evidence
§9         independent-review evidence
§10        founder decision
§11 - §12  mechanical verification
§13 - §16  bounded qualification results and the safety boundary
```

```text
Workflow success is qualification-harness evidence only. It is not scientific
evidence, not clinical evidence, not dataset evidence, not a real split, and
not a real or canonical leakage audit.
```

---

## 1. Authorization identity — repository evidence

```text
Authorization package:
PR #77 — docs(mesc): authorize P01-04B2D qualification
MERGED / CLOSED / NOT DRAFT

Head branch:
docs/mesc-p01-04b2d-authorization-r4

Authorization reviewed head:
096f6667251b4783fc9511336301dfaaa4c7f336

Authorization reviewed tree:
30b4cb5433a7f8496e62b8a94d879cf34a8ff26a

Canonical authorization merge:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Merged at:
2026-08-02T12:23:40Z

Files / statistics:
5 files, 3614 additions, 0 deletions

Adopted authority:
FD-B2D-1 through FD-B2D-14
```

The adopted authority is recorded at
[`../p01-04b2d-authorization/founder-authorization.md`](../p01-04b2d-authorization/founder-authorization.md)
and its exact requirements at
[`../p01-04b2d-authorization/implementation-contract.md`](../p01-04b2d-authorization/implementation-contract.md).

## 2. Activation sequencing — repository evidence

All five FD-B2D-14 activation conditions were satisfied before implementation
commit `6e5867829006770ad2ed50f26a9af0c455923594` was created:

```text
1. independent clean-room exact-head review of the authorization package
   — SATISFIED
2. separate Founder Ready decision
   — SATISFIED (PR #77 marked ready 2026-08-02T12:14:30Z)
3. separate Founder Merge decision
   — SATISFIED (PR #77 merged 2026-08-02T12:23:40Z)
4. merge into canonical main
   — SATISFIED (63cefe04c23726957aa26ac60ca8087ac9ca333a)
5. mechanical post-merge verification
   — SATISFIED
```

The implementation commit's single parent is exactly that canonical
authorization merge, so implementation authority was ACTIVE when the commit was
created. That authority is now SPENT.

## 3. Implementation commit, tree and parent — repository evidence

```text
Implementation branch:
test/mesc-p01-04b2d-qualification

Reviewed and merged head:
6e5867829006770ad2ed50f26a9af0c455923594

Implementation tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1

Implementation parent:
63cefe04c23726957aa26ac60ca8087ac9ca333a

Parent count:
1 — normal commit, not a merge

Commit count above the authorization baseline:
1

Commit subject:
test(mesc): qualify P01-04B2D synthetic suite

Commit message:
one line; no body, no trailer, no Co-Authored-By
```

## 4. Pull request and merge identity — repository evidence

```text
Implementation PR:
#78 — test(mesc): qualify P01-04B2D synthetic suite
MERGED / CLOSED / NOT DRAFT

Base branch:
main

Head oid:
6e5867829006770ad2ed50f26a9af0c455923594

Opened:
2026-08-03T02:54:44Z

Marked ready for review:
2026-08-03T03:13:15Z

Merged:
2026-08-03T03:15:12Z

Canonical implementation merge:
faf58c3fbfa9a83e7d392630e3ad1f322c616259

Merge tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1

Ordered parents:
63cefe04c23726957aa26ac60ca8087ac9ca333a
6e5867829006770ad2ed50f26a9af0c455923594

Merge subject:
Merge pull request #78 from IamShehri/test/mesc-p01-04b2d-qualification

Merge body:
test(mesc): qualify P01-04B2D synthetic suite

Files / statistics:
3 files, 3223 additions, 0 deletions
```

## 5. Path and blob identity — repository evidence

Exactly three added paths, identified by path and blob rather than by restated
source:

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

```text
Status of all three paths:
ADDED

Modified existing paths:
0

Deleted paths:
0

Renames / copies / binary files:
0
```

The three blobs present at the canonical merge commit are byte-identical to the
three blobs at the reviewed head.

## 6. Diff statistics and protected-path integrity — repository evidence

```text
Total files changed:
3

Total additions:
3223

Total deletions:
0
```

Protected subtrees compared between the authorization baseline
`63cefe04c23726957aa26ac60ca8087ac9ca333a` and the canonical merge
`faf58c3fbfa9a83e7d392630e3ad1f322c616259`:

```text
src            IDENTICAL — 4dc56e6b3af5dd3a7cbce7fdc66e00ebe583a813
specs          IDENTICAL — 5e1ef9c8203bd938f47f9b3116a0f4cbddc0684e
docs           IDENTICAL — 62141aafd60f69e2200fe8d63d626eb224de373d
pyproject.toml IDENTICAL — 2dcbf8e137946663eec9740bcad4545f79fc8bf4
uv.lock        IDENTICAL — 4dacb7898c69fc640bb50c60fb90c8b225f16c1d
```

The `tests` and `.github` subtrees differ only by the added qualification files.
No pre-existing test and no pre-existing workflow was modified. No dependency,
no public export, no CLI and no entry point was introduced.

`tests/_mesc_p01_04b2d_fixtures_v1.py` is referenced by no production file. Its
only repository references are the qualification workflow's path filters and the
authorization documents.

## 7. Pull-request-triggered checks — GitHub workflow evidence

All checks below ran against the exact reviewed head
`6e5867829006770ad2ed50f26a9af0c455923594`.

```text
CI
run id 30780440275   run number 248   event pull_request
completed / success
  quality (py3.11)                        completed / success
  quality (py3.12)                        completed / success
  jobs: 2/2 success

CodeQL
run id 30780440276   run number 251   event pull_request
completed / success
  analyze (python)                        completed / success
  jobs: 1/1 success

MESC P01-04B2D Qualification
run id 30780440318   run number 1     event pull_request
completed / success
  qualification (ubuntu-latest py3.11)    completed / success
  qualification (ubuntu-latest py3.12)    completed / success
  qualification (windows-latest py3.11)   completed / success
  qualification (windows-latest py3.12)   completed / success
  qualification (macos-latest py3.11)     completed / success
  qualification (macos-latest py3.12)     completed / success
  jobs: 6/6 success
```

Every cell executed the single dedicated qualification module against the same
committed literal golden vectors. No operating-system-specific expected value
exists in the suite, so success in all six cells is the cross-runtime
byte-identity evidence.

## 8. Post-merge push-triggered runs — GitHub workflow evidence

All runs below were triggered by the push of the canonical merge commit
`faf58c3fbfa9a83e7d392630e3ad1f322c616259` to `main`. The run identifiers were
queried from the repository, not assumed.

```text
CI
run id 30781355622   run number 249   event push   branch main
SUCCESS — 2/2 jobs
  quality (py3.11)                        completed / success
  quality (py3.12)                        completed / success

CodeQL
run id 30781355591   run number 252   event push   branch main
SUCCESS — 1/1 job
  analyze (python)                        completed / success

MESC P01-04B2D Qualification
run id 30781355599   run number 2     event push   branch main
SUCCESS — 6/6 jobs
  qualification (ubuntu-latest py3.11)    completed / success
  qualification (ubuntu-latest py3.12)    completed / success
  qualification (windows-latest py3.11)   completed / success
  qualification (windows-latest py3.12)   completed / success
  qualification (macos-latest py3.11)     completed / success
  qualification (macos-latest py3.12)     completed / success
```

One further pre-existing workflow ran on the same push and is recorded for
completeness of the observation, not as a required gate:

```text
Optional Extras / Backends
run id 30781355633   run number 80    event push   branch main
completed / success
```

```text
No workflow was dispatched, rerun or cancelled while building this package.
Existing results were inspected read-only.
```

## 9. Independent-review evidence

```text
Review type:
independent clean-room exact-head implementation review

Verdict:
APPROVE WITH NON-BLOCKING NOTES

Blocking findings:
NONE

Reviewed head:
6e5867829006770ad2ed50f26a9af0c455923594

Reviewed tree:
3d27b9c43462ef9880d5fab1ea45b675d5ff55c1

Review method:
fresh detached worktree at the exact head; read-only throughout;
zero repository mutation
```

The review is a governance-process review conducted in a separate session and
role, not a GitHub pull-request review submission; PR #78 carries no GitHub
review record, and none is claimed here.

Independently reproduced by the review, without reusing the implementation as
its own oracle:

```text
commit, tree, parent, subject and full message
three paths, three blobs and the exact statistics
zero protected-path drift
the complete exact-reference group-size arithmetic and size histogram
the complete constraint-stress feasible lattice, minimum score and both optima
the D6 ranks of the frozen pair, the frozen crossing group and every
  frozen scenario document
every literal golden value in full, not by prefix
the fail-closed behaviour of the goldens under deliberate mutation
both pinned action SHAs against their claimed releases
the eleven workflow path filters, parsed with correct YAML semantics
```

Nine non-blocking observations were returned. Each is carried forward in full,
with its founder disposition, in
[`founder-disposition.md`](founder-disposition.md) §5:

```text
NB-1  criterion-4 test reads repository source from disk
NB-2  duplicated file read in the same criterion test
NB-3  workflow omits a runtime uv-version assertion
NB-4  date-free probes are raw substrings
NB-5  context surfaces tokenized through the question token-set helper
NB-6  typed-failure assertion freezes a production message string
NB-7  local full-suite deviation traceable to shell resolution
NB-8  local type-check deviation under an extras-installed tree
NB-9  helper import mutates the interpreter search path
```

```text
All independent-review non-blocking notes:
ACCEPTED AS NON-BLOCKING

Correction authorization:
NOT ISSUED

Deferred implementation obligation:
NONE CREATED BY THIS PACKAGE
```

## 10. Founder Ready and Merge decisions

```text
Founder:
Abdulaziz Alshehri

Ready decision:
SEPARATE AND EXPLICIT — PR #78 marked ready for review 2026-08-03T03:13:15Z,
after the independent exact-head review returned no blocking finding

Merge decision:
SEPARATE AND EXPLICIT — PR #78 merged 2026-08-03T03:15:12Z

Acceptance decision:
FD-B2D-15, recorded 2026-08-03, in this package
```

Ready, merge and acceptance are three distinct decisions. None implies another.
The merge placed the reviewed implementation on canonical main; it did not
accept it. Acceptance is made by FD-B2D-15 and is not canonically adopted until
the five conditions of [`acceptance.md`](acceptance.md) §1 pass.

## 11. Canonical merge identity — mechanical verification

```text
Canonical main:
faf58c3fbfa9a83e7d392630e3ad1f322c616259

Tree:
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

## 12. Mechanical post-merge verification

Performed against the canonical merge commit before this package was written:

```text
origin/main equals faf58c3fbfa9a83e7d392630e3ad1f322c616259    VERIFIED
merge tree equals the reviewed implementation tree             VERIFIED
ordered parents are exactly 63cefe04... then 6e586782...       VERIFIED
second parent is exactly the reviewed head                     VERIFIED
commits introduced over the authorization baseline: 2
  (the reviewed implementation commit and the merge commit)    VERIFIED
diff baseline to merge: 3 added paths, 3223 additions,
  0 deletions, 0 modifications                                 VERIFIED
all three blobs at the merge match the reviewed blobs          VERIFIED
src, specs, docs, pyproject.toml and uv.lock unchanged         VERIFIED
post-merge CI, CodeQL and six-cell qualification all success   VERIFIED
```

```text
Mechanical post-merge verification:
PASSED
```

## 13. Fixture arithmetic and result classifications

### `exact-reference-1000-v1`

```text
rows                                1000
source-document groups              89
group counts by decision            yes 45 / no 31 / maybe 13
group sizes present                 1, 2, 3, 5, 8, 13
partition totals                    700 / 150 / 150
label totals                        552 / 338 / 110
exact ratified matrix               REPRODUCED
indivisible group placement         CONFORMING
groups crossing a partition         0
groups crossing a decision stratum  0
excluded records                    0
leakage findings                    0 — clean report
cross-platform deterministic literals  SATISFIED
```

Reproduced ratified matrix:

```text
              train  validation  test  total
yes             386          83    83    552
no              237          50    51    338
maybe            77          17    16    110
total           700         150   150   1000
```

### `constraint-stress-1000-v1`

```text
rows                                1000
groups                              500
group size                          2 for every group
group counts by decision            yes 276 / no 169 / maybe 55
exact target                        PROVABLY INFEASIBLE
odd cells in the ratified target    6 cells / 5 distinct odd values
global minimum squared-deviation score  6
number of score-6 matrices          2
lexicographic selected matrix       386,82,84,238,50,50,76,18,16
runner-up                           386,84,82,236,50,52,78,16,16
current production fallback         ABSENT
accepted facade behaviour           TYPED FAIL-CLOSED
minimum-deviation capability        UNSATISFIED
```

Infeasibility is mechanical, not asserted: every group has size 2 and no group
may cross a partition or a decision stratum, so every realized cell must be
even, while the ratified target contains six odd-valued cells. The count is six
cells; five is the number of distinct odd values, because 83 occurs twice.

```text
The typed fail-closed allocation failure is correct detection and
classification of a missing capability.

It is NOT implementation conformance to the required global
minimum-deviation allocation.
```

### `leakage-positive-v1`

```text
rows                                1000
source-document groups              999
two-example groups                  1 — homogeneous by decision
singleton groups                    998
other multi-example groups          0
pair partition                      wholly inside one actual partition
findings                            9
false_positive                      3
unresolved                          6
confirmed_leakage                   0
leaked                              true
suppressed                          0
```

```text
The exact-example self-identity and exact-source-document same-group
scenarios are same-partition synthetic controls.

They do not establish cross-partition leakage, duplicate split membership,
source-document overlap, real leakage, or canonical leakage evidence.
```

No raw synthetic question or context text reaches any canonical byte surface.
Raw synthetic surfaces exist only inside the non-promotable test helper.

## 14. Thirteen-criterion mapping

```text
 1  public splitter remains unconditionally fail-closed        SATISFIED
 2  FixtureSplitFacade is the separate fixture-only facade     SATISFIED
 3  qualification is library-only and in-memory                SATISFIED
 4  no B2 CLI exists                                           SATISFIED
 5  64-hex split_fingerprint is authoritative                  SATISFIED
 6  16-hex split_hash is compatibility/display only            SATISFIED
 7  leakage normalization follows FD-B2-6                      SATISFIED
 8  exactly the three named fixtures form the suite            SATISFIED
 9  stable synthetic inputs produce byte-identical results     SATISFIED
10  no real P01-03G membership is generated or disclosed       SATISFIED
11  atomic publication                                         NOT APPLICABLE TO B2D
                                                               NOT SATISFIED FOR
                                                               P01-04B OVERALL
12  write-path protections                                     NOT APPLICABLE TO B2D
                                                               NOT SATISFIED FOR
                                                               P01-04B OVERALL
13  date-free promotable artifacts                             NOT APPLICABLE TO B2D
                                                               OUTPUT PROMOTION;
                                                               DATE-FREE CANONICAL-BYTE
                                                               INVARIANT SATISFIED;
                                                               DOES NOT ESTABLISH
                                                               PROMOTABILITY
```

Each criterion is proved by a dedicated test or test group in the accepted
qualification module, with an exact assertion and a clear failure message, and
each is mapped to its proving test symbol inside that module.

## 15. Minimum-deviation capability gap

```text
Indivisible-group global minimum-deviation allocation (FD-B2-7 Fixture B):
UNSATISFIED

Cause:
the accepted allocation performs exact-target allocation only and fails closed
at a boundary crossing; it implements no global minimum-deviation fallback

Production correction made in B2D:
NONE

Production correction authorized by this package:
NONE
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

NOT APPLICABLE IS NEVER CONVERTED TO SATISFIED AND NEVER COUNTS
TOWARD P01-04B ACCEPTANCE.
```

## 16. Non-execution and safety boundary

Building this package performed no execution of any kind:

```text
no B2D fixture constructed
no facade invoked
no B2D digest, request identifier, split hash, fingerprint or finding
  identifier calculated
no workflow dispatched, rerun or cancelled
no real dataset, registry or source-record access
no real split generation or real partition membership
no real or canonical leakage audit
no record-pair discovery
no dataset or model download, model access, inference or retrieval
no metrics, benchmark execution, training, fine-tuning or adapter creation
no publication and no clinical use
no repository setting changed
```

Every value in this ledger was read from the repository or queried read-only
from the hosting service. Every quantity attributed to the qualification suite
is a bounded synthetic qualification result.

```text
All B2D inputs and outputs are synthetic, fixture-only, non-evidence,
non-clinical, non-promotable as a real split and non-promotable as a real
leakage audit.
```

## 17. Ledger integrity

This ledger is immutable once committed. A later correction requires a separate
founder decision and its own package; it must never be applied by editing this
document. No entry here creates authority, and no entry may be read as
authorizing implementation, correction, execution or any downstream phase.
