# P01-04B2A Final Review Hold — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Accepted verdict on PR #61:
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT

FD-PV-17:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-17 ACTIVATION CONDITIONS ARE SATISFIED

PR #61:
OPEN / DRAFT / NOT MERGED — HELD

Admissible evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

N-12:
BINDING AND UNDISCHARGED

Windows and macOS obligations:
OPEN

B2B:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-07-31

Required canonical baseline:
`02d0aafb61fa62de414c0e8e5d61187c03b650bd`

Governed pull request:
`PR #61` — exact head `f68f8be8799c0ec67b26c319a4a06789f2ea1a7e`, exact tree
`1caa8f9ae4031ff17ddcd33ffc0a32a4e7cc855e`, 8 commits, 3 files, +3829 / −0

This document is controlling for this package. Prior governance history is
adopted at [`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/) and
is not restated here.

---

## 1. Accepted verdict

A genuinely independent clean-room exact-head review of PR #61 returned:

```text
GOVERNANCE HOLD — PR #61 MUST REMAIN DRAFT
```

The founder accepts that verdict in full. PR #61 remains Draft.

## 2. Accepted blocking findings

Four blocking defects. All four are accepted as stated, none treated as
advisory.

**F1 — large unexpected artifact responses may emit the wrong category.** The
artifact-set guards use pipelines of the form `comm -23 … | grep -q .` under
`set -euo pipefail`. When the `comm` output is large enough that `grep -q` exits
on its first match before draining the pipe, `comm` receives `SIGPIPE` and the
pipeline exit status becomes 141. Under `pipefail` inside an `if` condition that
status reads as false, so the guard does not fire. A response carrying many, or
long, unexpected artifact names can therefore bypass the unexpected-artifact
check and reach a later guard, producing a different category or no category at
all for that condition.

**F2 — B2 tests bypass the real projection and pagination boundary.** The test
harness supplies pre-rendered TSV and ignores the `--paginate` and `--jq`
arguments the workflow actually passes. The `.artifacts[]` projection over
`name`, `size_in_bytes`, `expired` and `id`, and the pagination behaviour, are
therefore never exercised. A regression in the projection or in page handling
would not be detected.

**F3 — dispatch tests do not prove both guard copies or the rejection order.**
The workflow contains two dispatch-guard copies, one per job; the tests execute
one. For malformed SHA inputs the tests do not prove that rejection occurs
*before* `git rev-parse HEAD` is invoked, and the git stub accepts any command,
so a malformed value that fell through to the later HEAD-mismatch branch would
still emit the same category and the test would still pass.

**F4 — archive-cardinality behaviour lacks real execution coverage.** The
archive-cardinality step is asserted structurally only. Neither the passing
six-archive case nor the failing five- and seven-archive cases execute the real
step, so its category emission is unproven.

## 3. Accepted taxonomy mappings — unchanged

The review accepted the following two mappings. They are settled and **must not
be changed** by the authorized correction:

```text
expired expected artifact:
missing_matrix_cell

post-validation archive-count inconsistency:
aggregate_verifier_internal_error
```

## 4. FD-PV-17 — Final Independent-Review Correction Authority

```text
FD-PV-17
RECORDED BUT NOT ACTIVE
```

### Activation conditions — all five required

1. a genuinely independent exact-head review approves **this governance
   package**;
2. a separate founder Ready decision for this governance package;
3. a separate founder merge decision for this governance package;
4. merge into canonical `main`;
5. mechanical verification of the merge SHA, its ordered parents, and the
   resulting canonical main tree.

**No subset activates `FD-PV-17`.** Adoption alone, merge alone, independent
approval plus merge, and adoption plus mechanical verification are each
insufficient. Recording this decision in a Draft pull request activates nothing.

### Authority activated by the complete five-condition gate

Once every condition is satisfied, `FD-PV-17` authorizes exactly:

1. **one** additive ninth commit on the PR #61 branch, required parent
   `f68f8be8799c0ec67b26c319a4a06789f2ea1a7e`, recommended subject
   `fix(mesc): close final portability review findings`;
2. a normal **non-force** push of that commit;
3. the pull-request workflows **automatically triggered** by that push;
4. a **metadata-only** PR #61 body correction, made solely through the
   pull-request metadata endpoint;
5. commissioning a new genuinely independent clean-room exact-head review.

### Exact paths

Primary:

```text
.github/workflows/mesc-b2a-portability.yml
tests/test_mesc_b2a_portability.py
```

Conditional:

```text
tests/_mesc_b2a_portability.py
```

The helper may change **only** if the builder proves that one of the four
blocking defects cannot be closed without it, and that proof must be recorded in
the commit. The expected implementation leaves it byte-unchanged.

### Acts that remain separate

`FD-PV-17` does not authorize, before or after activation: a tenth PR #61
commit or any further commit; a second commit on this governance package;
amendment, rebase, squash, reset, cherry-pick, or force-push; any path outside
those named above; marking either pull request Ready; merging either pull
request; auto-merge; manual workflow rerun or dispatch; producing or accepting
admissible evidence; accepting B2A; discharging binding `N-12`; closing the
Windows or macOS obligations; authorizing B2B; executing the real split;
running B0; training or fine-tuning any model; or deleting any branch.

## 5. Authorized PR #61 body correction

After activation, the metadata-only PR #61 body correction may record: the
accepted `GOVERNANCE HOLD` verdict; that B3 and B4 remain open; that commit 9 is
authorized but not yet executed; the four blocking findings; the two accepted
taxonomy mappings; continued Draft state; and that no Ready, merge, evidence,
B2A acceptance, `N-12` discharge, platform closure, B2B, split, benchmark, or
training is authorized.

The body must be changed **only** through the pull-request metadata endpoint.
Repository file APIs must never be used to edit a pull-request description.

## 6. Standing status

Nothing in this disposition corrects any finding, adopts the infrastructure,
executes any workflow, produces admissible evidence, accepts B2A, discharges
`N-12`, closes the Windows or macOS obligations, or authorizes B2B. P01-04B
remains incomplete and not accepted.
