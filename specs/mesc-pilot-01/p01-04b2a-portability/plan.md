# P01-04B2A Cross-Platform Portability Validation Infrastructure — Plan

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
