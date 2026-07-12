# Research Journal Template

*Copy the block below into [journal.md](journal.md) at the end of every session.
Two minutes, honestly filled, beats ten minutes of polish. `decided_at` timestamps
in the review log back up your duration figures — record wall-clock anyway (the log
can't see your breaks).*

```markdown
## Session <n> — <YYYY-MM-DD>

- Reviewer: <id>
- Duration: <start>–<end> (~<minutes> min, minus <breaks> min breaks)
- Scope: <duplicates | Qx screening | extraction | benchmark>

### Counts
- Records reviewed: <n>   (include: <n>, exclude: <n>, maybe: <n>, duplicate: <n>, skip: <n>)
- Duplicate groups resolved: <n> of 16
- Corrections (amend): <n>
- Evidence objects extracted: <n>  (verified: <n>, unverified: <n>)

### Issues encountered
<!-- one MZ block per issue; "none" is a fine and common answer -->
### MZ-<n>: <one-line title>
- Class: Bug | UX | Missing validation | Documentation | Research workflow | Scientific
- Priority: Critical | High | Medium | Low
- Reproduction: <exact command / situation>
- Impact: <what it cost>
- Proposed fix: <smallest honest fix - recorded, not implemented>

### Observations
<!-- what the tooling/workflow felt like today; what PRISMA-relevant patterns you noticed -->

### Ideas
<!-- improvements that occurred to you; they go here and NOWHERE else during the mission -->

### Questions
<!-- open scientific or process questions to resolve before/at retrospective -->

### Next session goal
<!-- one line, concrete: "finish Q2 (23 remaining)" -->
```

**Milestone sessions** (duplicates done, a query finished, extraction start/end)
additionally record: the snapshot id captured, and the commit hash of the session.
