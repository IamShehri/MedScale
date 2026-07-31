# P01-04B2A Evidence Production Gate — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Accepted verdict on PR #61 exact head 7c1522eb...:
APPROVE WITH NON-BLOCKING NOTES — EXACT HEAD ELIGIBLE FOR A SEPARATE FOUNDER
READY DECISION

PR #61:
MERGED / CLOSED

Infrastructure adoption:
ACHIEVED ON CANONICAL MAIN

FD-PV-17:
ACTIVATED AND CONSUMED

FD-PV-18:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-18 ACTIVATION CONDITIONS ARE SATISFIED

Admissible evidence production:
NOT YET AUTHORIZED

Admissible evidence:
NOT PRODUCED

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
2026-08-01

Required canonical baseline:
`69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3`

This document is controlling for this package. Prior governance history is
adopted at [`../p01-04b2a-governance-hold/`](../p01-04b2a-governance-hold/) and
[`../p01-04b2a-final-review-hold/`](../p01-04b2a-final-review-hold/) and is not
restated here.

---

## 1. Verified post-merge truth

The merge object was verified mechanically from immutable Git objects, not from
a helper summary.

```text
Merge SHA:
69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3

Tree:
ebbb61b905bde4773d48b40b9f667ceb0d558566

Ordered parent 1:
63c6e3200c4b8013ec068630a29118df0dfc7a6f

Ordered parent 2:
7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae

Subject:
ci(mesc): add B2A portability infrastructure (#61)

Merged at:
2026-07-31T22:00:34Z
```

First-parent delta against `63c6e320...`:

```text
A .github/workflows/mesc-b2a-portability.yml   +493
A tests/_mesc_b2a_portability.py              +1068
A tests/test_mesc_b2a_portability.py          +2850

3 files changed, 4411 insertions(+), 0 deletions(-)
```

Pull-request final state:

```text
PR #61:
MERGED / CLOSED / NOT DRAFT

Merged head:
7c1522ebfd5376fa237f9ff40a5856b8ed03f1ae

Commits:
9 — all nine are ancestors of the merge

Commit 10:
NOT AUTHORIZED / NOT CREATED

Branch feat/mesc-b2a-portability-infrastructure:
still 7c1522eb... — no force-push, no branch movement
```

Canonical `main` points at the merge SHA. Nothing on the branch moved after the
merge.

## 2. Post-merge Actions truth

The merge triggered three `push`-event runs on `main`, all attempt 1, all
successful:

```text
CI                          30668524206   push   attempt 1   success
CodeQL                      30668524193   push   attempt 1   success
Optional Extras / Backends  30668524166   push   attempt 1   success
```

`.github/workflows/mesc-b2a-portability.yml` declares only `pull_request` and
`workflow_dispatch` triggers. The merge therefore **correctly** produced no
portability run. That absence is expected behaviour and is **not** a failure.

```text
MESC B2A Portability runs, all time:
7 runs — every one event: pull_request, every one run_attempt: 1

workflow_dispatch runs:
0

Manual reruns:
0

b2a-portability-evidence artifacts, repository-wide:
0
```

Every existing portability run is non-admissible pull-request infrastructure
validation on the feature branch. No run has ever executed against canonical
`main`, and no evidence envelope artifact has ever been produced. The CI and
CodeQL runs are recorded separately above and are **not** portability evidence.

## 3. What adoption did and did not achieve

Adoption places the six-cell portability workflow, its private harness, and its
test suite on canonical `main`. It does **not** produce portability evidence.

```text
Infrastructure adoption:      ACHIEVED
Admissible evidence:          NOT PRODUCED
B2A acceptance:               NOT ACHIEVED
N-12:                         BINDING AND UNDISCHARGED
Windows and macOS obligations: OPEN
B2B:                          NOT AUTHORIZED
P01-04B:                      INCOMPLETE / NOT ACCEPTED
```

No existing pull-request artifact satisfies the canonical-main obligation, and
none may be downloaded, cited, or interpreted as admissible evidence.

## 4. FD-PV-18 — Canonical Portability Evidence Production Authority

```text
FD-PV-18
RECORDED BUT NOT ACTIVE
```

### Activation conditions — all five required

1. a genuinely independent clean-room exact-head review approves **this
   governance package**;
2. a separate founder Ready decision for this governance package's pull
   request;
3. a separate founder merge decision for that pull request;
4. merge into canonical `main`;
5. mechanical verification of the resulting merge SHA, its ordered parents, its
   tree, its path scope, and the final canonical-main identity.

**No subset activates `FD-PV-18`.** Draft creation activates nothing. Review
approval alone, Ready alone, merge alone, review plus merge, and merge without
mechanical verification are each insufficient.

### Authority activated by the complete five-condition gate

Once every condition is satisfied, `FD-PV-18` authorizes exactly:

1. **one** attempt to dispatch `.github/workflows/mesc-b2a-portability.yml` on
   ref `main` through the `workflow_dispatch` event;
2. the six matrix cells and the one aggregate-verification job that workflow
   defines;
3. upload of the single canonical evidence envelope by that run's own
   dispatch-gated upload step;
4. read-only inspection of that exact run, its jobs, steps, logs, metadata, and
   artifacts;
5. download and offline verification of the **seven** exact artifacts from that
   one run — the six portability cell artifacts and `b2a-portability-evidence`.

### Required dispatch input

```text
expected_sha = the mechanically verified canonical-main SHA produced by merging
               this governance package
```

That SHA does not exist yet and must not be guessed. It is **not**
`69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3`, because merging this package will
create a newer canonical-main commit. The value must be read from canonical
`main` after the merge and verified mechanically before it is used.

### Consumption

The authority is **consumed the moment GitHub accepts the dispatch request**,
whether the workflow then succeeds, fails, is cancelled, or times out.

No retry, no rerun, no second dispatch, and no replacement run is authorized. A
failed, cancelled, timed-out, or malformed run requires a **new** founder
decision.

### Acts that remain separate

`FD-PV-18` does not authorize, before or after activation: a second dispatch or
any rerun; any dispatch against a ref other than `main`; any `expected_sha`
other than the mechanically verified activated canonical-main SHA; a second
commit on this governance package; amendment, rebase, squash, reset,
cherry-pick, or force-push; any path outside those named in
[`acceptance.md`](acceptance.md); marking this package's pull request Ready;
merging it; auto-merge; accepting the produced evidence; accepting B2A;
discharging binding `N-12`; closing the Windows or macOS obligations;
authorizing B2B; completing P01-04B acceptance; executing the real Pilot-01
split; running B0; accessing model weights or the real dataset; running
inference, retrieval, training, or fine-tuning; publication; clinical use; or
deleting any branch.

## 5. Evidence does not equal acceptance

```text
Successful evidence production does not itself accept B2A.
```

After a successful dispatch the required sequence is, in order:

1. mechanical run and artifact verification;
2. a genuinely independent clean-room evidence review;
3. a separate founder evidence-acceptance decision;
4. only then, and only if every governing criterion is satisfied — B2A
   acceptance, the binding `N-12` disposition, closure of the Windows and macOS
   obligations, and consideration of B2B authorization.

`FD-PV-18` authorizes step 1 only. It authorizes none of steps 2 through 4, and
producing evidence creates no entitlement to any of them.

## 6. Standing status

Nothing in this disposition dispatches a workflow, produces admissible evidence,
accepts evidence, accepts B2A, discharges `N-12`, closes the Windows or macOS
obligations, or authorizes B2B. P01-04B remains incomplete and not accepted.
