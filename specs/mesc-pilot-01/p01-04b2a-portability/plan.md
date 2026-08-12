# P01-04B2A Cross-Platform Portability Validation Infrastructure — Plan

```text
Status:
CONTRACTS FOUNDER RATIFIED;
REMEDIATION AUTHORITY RECORDED BY FD-PV-11 THROUGH FD-PV-15 BUT NOT ACTIVE

Contracts:
FOUNDER RATIFIED

Historical initial implementation:
OCCURRED BEFORE CANONICAL AUTHORIZATION

Current remediation authority:
RECORDED BUT NOT ACTIVE

Activation:
OPERATIVE ONLY AFTER ALL FIVE FD-PV-15 ACTIVATION CONDITIONS ARE SATISFIED

Infrastructure adoption:
NOT ACHIEVED

Execution:
NOT AUTHORIZED

Admissible evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED

B2B:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

Canonical planning baseline:
`0884971f68619be8f25c3b905a3dcad7c5212101`

Founder ratification:
`FD-PV-1` through `FD-PV-10` ratified on 2026-07-27; see
`founder-ratification.md`.

---

## Controlled sequence

Each step is a hard boundary. No step may begin before the previous step has
produced its recorded outcome.

| # | Step | Actor | Gate |
|---|---|---|---|
| 1 | Cross-platform validation-infrastructure documentation gate | Builder | This package. No code. No self-authorization. |
| 2 | Founder decision on the proposed infrastructure contracts | Founder | **Completed 2026-07-27.** PD-PV-1 through PD-PV-10 adopted as FD-PV-1 through FD-PV-10, with the FD-PV-6 numeric limits selected. |
| 3 | Separate B2A implementation authorization | Founder | Explicit, naming a canonical baseline. |
| 4 | Atomic B2A implementation PR | Builder | Limited to the four already-ratified B2A implementation and test paths. |
| 5 | Exact-head Linux CI and independent Opus review | CI / Opus | Linux evidence only; partial by construction. |
| 6 | Separate merge decision for B2A code | Founder / ChatGPT | Merged only as `IMPLEMENTED BUT NOT ACCEPTED`. |
| 7 | Separate validation-infrastructure implementation authorization | Founder | Explicit and distinct from step 3. |
| 8 | Validation-infrastructure PR | Builder | Based on a canonical main that already contains the B2A implementation. Limited to the three proposed paths. |
| 9 | Six-cell cross-platform portability run | CI | All six cells must succeed. |
| 10 | Aggregate byte and hash comparison | CI | Fail-closed verifier. |
| 11 | Independent Opus review of infrastructure and evidence | Opus | Read-only. |
| 12 | Merge decision for the validation infrastructure | Founder / ChatGPT | Separate act. |
| 13 | Canonical-main `workflow_dispatch` evidence run | CI on main | The only evidence admissible for acceptance. |
| 14 | Independent review of canonical-main evidence | Opus | Read-only. |
| 15 | Separate founder/ChatGPT B2A acceptance decision | Founder | The act that changes B2A from implemented to accepted. |
| 16 | Only then may B2B authorization be considered | Founder | Consideration, not automatic grant. |

## Why the design is frozen before the code exists

This plan deliberately does **not** require workflow infrastructure to be
implemented before B2A code exists. The ordering is:

1. the infrastructure **design** is frozen first, so its contracts are decided
   while they are still cheap to change;
2. B2A code may then be implemented and merged **without acceptance**, because
   merging code is not accepting it;
3. the workflow implementation follows once the private B2A implementation
   exists on canonical main, since the workflow's only purpose is to exercise
   that implementation across platforms;
4. cross-platform evidence is required **before acceptance**, not before code
   authorship.

Requiring the workflow first would mean writing a workflow with nothing to
exercise. Requiring acceptance before evidence would violate N-12.

## Explicit prohibitions

The following are prohibited throughout this sequence:

- **Parallel B2B work.** No B2B documentation, implementation or review may
  begin at any point in this sequence.
- **Combined pull requests.** B2A implementation and validation-infrastructure
  implementation must never be combined into one pull request.
- **Infrastructure before code.** The infrastructure implementation must not be
  authored before the B2A implementation is available on canonical main for it
  to exercise.
- **Accepting B2A on Linux-only evidence.** Linux Python 3.11 and 3.12 evidence
  is partial and can never discharge N-12 alone.
- **Treating pull-request evidence as canonical-main evidence.** Evidence from a
  `pull_request` run may not substitute for a canonical-main
  `workflow_dispatch` run without a reviewed tree-equivalence argument and a
  separate acceptance decision.
- **Starting B2B because a workflow passed.** A green workflow is not an
  acceptance decision and does not unblock B2B.

## Stop conditions

Stop without mutation if:

- canonical main has moved from the baseline recorded in the relevant
  authorization;
- any proposal conflicts with D1–D10, FD-B2-1 through FD-B2-8, FD-B2A-1 through
  FD-B2A-8, or binding N-12;
- an unauthorized path would be modified;
- `.github/workflows/ci.yml` would be modified;
- secrets, write permissions, OIDC, dataset access, model access, or network
  fetches beyond the locked dependency environment would be introduced;
- any document would claim authority the founder has not recorded.

## Historical chronology — status before FD-PV-11

This section preserves the status this document carried before founder decisions
`FD-PV-11` through `FD-PV-15` were recorded. It is retained as history. It is
**not** the current status, and it was **not** wrong when written: it accurately
described the period it covers.

```text
Status:
FOUNDER-RATIFIED CONTRACTS — IMPLEMENTATION NOT AUTHORIZED

Infrastructure implementation:
NOT AUTHORIZED

B2A implementation:
NOT AUTHORIZED

Execution:
NOT AUTHORIZED

Evidence production:
NOT AUTHORIZED

B2A acceptance:
NOT ACHIEVED
```

Between the ratification of `FD-PV-1` through `FD-PV-10` on 2026-07-27 and the
adoption of this record, **no canonical infrastructure-implementation
authorization existed**. The implementation work now present in Draft PR #61 was
created during that period. `FD-PV-11` records that fact. It does not convert it
into retroactive authorization.

---

## Remediation sequence (FD-PV-15)

Each step is a hard boundary. No step may begin before the previous step has
completed and been verified. This sequence is authorized prospectively and is
not executed by the record that authorizes it.

1. Complete the full activation gate for this governance package. All five
   conditions are required, in order, and none may be inferred from another:
   1. a genuinely independent exact-head approval of PR #62;
   2. a separate founder Ready-transition decision for PR #62;
   3. a separate founder merge decision for PR #62;
   4. merge of PR #62 into canonical main;
   5. mechanical verification of the canonical merge SHA and the resulting main
      tree.

   Only after all five have occurred may step 2 begin. Merge alone, without the
   other four, activates nothing.
2. Synchronize the new canonical main into
   `feat/mesc-b2a-portability-infrastructure` with a normal non-force merge
   commit. Preserve both existing commit identities. No rebase, amend, squash,
   reset, cherry-pick, or force-push.
3. Correction A — bind the canonical SHA into the evidence envelope
   (`FD-PV-14`).
4. Correction B — bounded artifact handling, corrected limit axes and timing,
   removal of the invented per-file limit, and real safe-extraction regression
   tests (`FD-PV-12`, `FD-PV-13`).
5. Verify exact-head workflows pass.
6. Obtain a genuinely independent exact-head review from a reviewer that did not
   author the work.
7. Obtain a separate founder Ready-transition decision.

### What activation authorizes

Step 1 is the complete five-condition activation gate; every one of its five
conditions must be satisfied before anything below it is authorized. Step 2 and
steps 3 through 5 — the non-force synchronization merge commit, Correction A,
Correction B, the normal push, and the automatically triggered validation those
pushes cause — become authorized **together** by `FD-PV-15` once it activates,
and need no further founder decision.

Their strict ordering above remains binding: no step may begin before the
previous step has completed and been verified.

Step 6, independent exact-head review, remains a **mandatory gate** and is not
satisfied by any earlier step.

Step 7, the PR #61 Ready transition, remains a **separate founder decision**.

Outside `FD-PV-15` entirely, and requiring separate founder decisions where
applicable: PR #61 merge, manual workflow rerun, manual workflow dispatch,
admissible evidence production, evidence acceptance, B2A acceptance, discharge
of binding `N-12`, closure of the Windows or macOS obligations, B2B, and branch
deletion.

## Additional stop conditions for remediation

Stop without mutation if:

- any one of the five `FD-PV-15` activation conditions is not yet satisfied,
  including this governance package not yet being adopted on canonical main and
  the canonical merge SHA and resulting main tree not yet being mechanically
  verified;
- either existing PR #61 commit identity would change;
- a fourth or later correction commit would be required;
- any path outside the three implementation paths would be modified;
- a permission beyond `contents: read` and `actions: read` would be required;
- any of the four `FD-PV-6` byte values would change;
- the twenty-one-category failure taxonomy would be renamed, merged, or
  extended;
- a new evidence schema version would be created.
