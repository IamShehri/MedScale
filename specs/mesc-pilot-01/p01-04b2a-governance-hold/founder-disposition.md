# P01-04B2A Governance Hold — Founder Disposition

```text
Status:
FOUNDER DISPOSITION RECORDED

Authority-record gap (B1):
ACKNOWLEDGED — NOT RETROACTIVELY CURED

FD-PV-16:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-16 ACTIVATION CONDITIONS ARE SATISFIED

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
`3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9`

Governed pull request:
`PR #61`, exact head `2260fa540c440ce3584535f30e74323381568b98`, exact tree
`eb5cd1757f89bca2b42e1e9c61d3fcd1270a5e94`

---

## 1. Disposition of the authority-record gap (B1)

### What actually happened

This section records the governance failure plainly. It does not reconstruct
records that never existed.

1. Separate founder decisions authorizing PR #61 commit 6 and commit 7 were
   issued **outside** the canonical repository record, immediately before the
   corresponding builder actions.
2. Those decisions were **not durably persisted** anywhere a later reader can
   reach: not in `specs/**`, not in the pull-request description, not in a
   review, not in an issue, not in any adopted record on canonical main.
3. The independent reviewer therefore **could not reconstruct them** from
   canonical evidence, and correctly refused to infer them.
4. **Commit messages are not independent authority records.** A commit message
   is authored by the same party performing the action it describes. It is
   evidence of intent, never evidence of authorization.
5. The absence of durable authority evidence at the time of execution is a
   **governance defect**, not a documentation inconvenience. The adopted
   `FD-PV-15` record lists "a fourth implementation correction commit" among the
   acts that remain a separate founder act; commits 6 and 7 are the fourth and
   fifth implementation-side commits on that branch, and no repository-native
   record authorizes them.

### What this disposition is not

This disposition does **not** rewrite history, does **not** pretend the missing
records existed, does **not** backdate any decision, and is **not** retroactive
evidence that the original recordkeeping process was compliant. It was not.

### The disposition

1. The founder **acknowledges** the historical authority-record gap surrounding
   PR #61 commits 6 and 7.
2. The founder accepts that those commits **exist** in PR #61 but do **not, by
   themselves, prove prior authority**.
3. The founder **ratifies their continued presence for review purposes only**,
   so that the independent reviewer of the final head evaluates the actual code
   rather than a reconstructed branch. Ratification of presence is not
   ratification of the process that produced them, and is not acceptance of
   their content.
4. **Ready and merge are prohibited** for PR #61 until every current blocking
   finding is corrected and a new genuinely independent exact-head review
   approves the final head.
5. This disposition creates no precedent. It is confined to these two commits.
6. **All future implementation authority must be recorded canonically before
   execution.** A decision that exists only in a conversation is not an
   authorization for the purposes of this project.

### Exact commits covered

```text
Commit 6:
605536737a22db5a3abfe4243a1c528623a46ba5
fix(mesc): cap artifact transport and reject unexpected artifacts

Commit 7:
2260fa540c440ce3584535f30e74323381568b98
test(mesc): exercise transport pipeline failures
```

No other commit is covered by this disposition.

---

## 2. Preventive control decision

Recorded prospectively and controlling from adoption:

1. Canonical `main` must **not** receive direct file mutations through content
   APIs or through ref movement during governed work.
2. Normal changes enter canonical `main` **only** through reviewed pull
   requests.
3. **Force updates to canonical `main` are prohibited**, except under a
   separately recorded emergency-recovery decision that names the exact
   before-and-after SHAs and the reason.
4. Tooling must verify the **target branch** and the **action type** before any
   mutation, and must refuse a write whose target is a protected branch.
5. Pull-request body updates must use the **pull-request metadata endpoint**.
   Repository file APIs must never be used to edit a pull-request description.
6. Adoption of branch protection or a repository ruleset on `main` is
   **recommended as a separate operational action**. This record does not change
   any repository setting.

---

## 3. FD-PV-16 — Final Governance-Hold Correction Authority

```text
FD-PV-16
RECORDED BUT NOT ACTIVE
```

### Activation conditions — all five required

`FD-PV-16` becomes operative only after **all five** of the following:

1. a genuinely independent exact-head approval of **this governance pull
   request**;
2. a separate founder Ready-transition decision for this governance pull
   request;
3. a separate founder merge decision for this governance pull request;
4. merge of this governance pull request into canonical `main`;
5. mechanical verification of its canonical merge SHA, its ordered parents, and
   the resulting canonical main tree.

**No subset activates `FD-PV-16`.** Adoption alone is insufficient. Merge alone
is insufficient. Independent approval plus merge, without both separate founder
decisions and the mechanical verification, is insufficient. Recording this
decision in a Draft pull request activates nothing.

### Authority activated by the complete five-condition gate

Once every activation condition is satisfied, `FD-PV-16` authorizes exactly:

1. **one** additive correction commit on the PR #61 branch, with required parent
   `2260fa540c440ce3584535f30e74323381568b98` and recommended subject
   `fix(mesc): close portability governance-hold findings`;
2. a normal **non-force** push of that commit;
3. the pull-request workflows **automatically triggered** by that push;
4. a PR #61 body update reflecting the final exact head, made through the
   pull-request metadata endpoint;
5. commissioning a new genuinely independent clean-room exact-head review of the
   resulting head.

No further founder authorization is required for those five acts once
`FD-PV-16` is activated.

### Exact future implementation paths

```text
.github/workflows/mesc-b2a-portability.yml
tests/test_mesc_b2a_portability.py
```

`tests/_mesc_b2a_portability.py` may be modified **only** if the future
independent correction analysis proves a helper change is strictly necessary,
and that necessity must be stated in the commit record. Otherwise it must remain
byte-identical.

### Acts that remain separate

`FD-PV-16` does not authorize, before or after activation:

- a ninth PR #61 commit, or any commit beyond the single authorized one;
- amendment, rebase, squash, reset, cherry-pick, or force-push;
- any path outside the paths named above;
- marking PR #61 Ready, or merging PR #61;
- marking this governance package Ready, or merging it;
- enabling auto-merge on either pull request;
- manually rerunning or dispatching any workflow;
- producing or accepting admissible portability evidence;
- accepting B2A;
- discharging binding `N-12`;
- closing the Windows or macOS obligations;
- authorizing B2B;
- deleting any branch;
- changing any repository setting, including branch protection.

Ready and merge for PR #61 remain separate founder acts, available only after a
successful independent review of the final head.

---

## 4. Standing status

Nothing in this disposition adopts the portability infrastructure, executes any
workflow, produces admissible evidence, accepts B2A, discharges `N-12`, closes
the Windows or macOS obligations, or authorizes B2B. P01-04B remains incomplete
and not accepted.
