# Mission Zero — Operational Journal

**Mission:** MedScale's first real systematic review, conducted by the Founder as a
working researcher. Software is frozen except for bugs and operational issues
discovered during actual use. Observe, measure, record; implement only after.

- **Started:** pre-flight passed 2026-07-12 at `9a04aa0`
- **Reviewer id:** *(founder: record the id you screen under here)*
- **Scope:** uncertain-duplicate resolution (16 groups), then title/abstract
  screening under ADR-0022 semantics, Q2 first
- **Pre-screening baseline:** snapshot `cfdfcce5e2830391` (VERIFIED at mission start)

## Pre-flight record (2026-07-12)

| Gate | Result |
|---|---|
| Repository clean, local == origin | PASS (`9a04aa0`) |
| Quality gate (ruff, mypy --strict, 255 tests) | PASS |
| `medscale check` | PASS — CLEAN, 1,346 records, 0 review refs |
| Baseline snapshot verify | PASS — `cfdfcce5e2830391` VERIFIED |
| Screening state | 16 uncertain groups unresolved; 1,346 pending |
| Documentation current | PASS — guides shipped at `9a04aa0` |
| ADRs required for the study | **ADR-0022 Proposed — ratification is the GO gate** |
| ADR-0018 (evidence identity) | Not needed for screening; **gates the extraction stage** |

## Rules of engagement (support side)

The mission is interrupted **only** for: data-integrity risk, broken
reproducibility, a threatened audit trail, or compromised scientific validity.
Everything else is recorded below and the study continues.

## Session protocol (researcher side)

1. `uv run medscale check` — must be CLEAN before starting.
2. Work: `screen duplicates` / `screen next --reviewer <id> --query Qx --limit N`.
3. `uv run medscale check` again, then `git add data/litdb && git commit` — one
   commit per session, message: `study(mission-zero): <what>, <reviewer>`.
4. Add a session row and any issues below. Timing needs no tooling: every decision
   carries `decided_at`, so per-session duration and records/hour are derivable
   from the review log afterwards.

## Session log

| # | Date | Reviewer | Scope | Decisions | Notes |
|---|---|---|---|---|---|
| — | — | — | — | — | *(first session pending ADR-0022 ratification)* |

## Issue register

Every discovered issue becomes evidence. Classification is one of: **Bug / UX issue /
Missing validation / Documentation issue / Research workflow issue / Scientific
issue.** Priority: Critical / High / Medium / Low.

Template:

```
### MZ-<n>: <one-line title>
- Class: <classification>   Priority: <priority>
- Discovered: <date, during what>
- Reproduction: <exact steps or command>
- Impact: <what it cost the researcher / the science>
- Proposed fix: <smallest honest fix — recorded, NOT implemented during the mission>
```

*(none yet)*

## Milestones

- [ ] ADR-0022 ratified (GO)
- [ ] 16 uncertain-duplicate groups resolved
- [ ] Q2 title/abstract screening complete (148 records)
- [ ] Post-Q2 snapshot captured and committed
- [ ] Remaining queries screened (Q6, Q4, then the rest)
- [ ] Full-corpus screening complete; PRISMA stats exported
- [ ] Mission retrospective written (workflow observations, friction, timings,
      command usage, gaps, candidate improvements, evidence-justified changes)
