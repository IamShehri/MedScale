# Mission Zero Operations Manual

*The official operating manual for MedScale's first real systematic review.
Approved 2026-07-12; ADR-0022 (screening semantics) Accepted as the GO gate.
Software is frozen for the mission except bugs and operational issues found in use.*

| Document | Use it when |
|---|---|
| [Protocol](protocol.md) | The rules of the whole study — read once, consult on doubt |
| [Daily Checklist](daily_checklist.md) | Every session, start to finish (one page) |
| [Incident Response](incident_response.md) | Something looks wrong |
| [Journal](journal.md) | The living record: sessions, issues, milestones |
| [Journal Template](journal_template.md) | Copy-paste block for each session entry |
| [Completion Criteria](completion_criteria.md) | "Are we done?" — objective answer |
| [Success Metrics](success_metrics.md) | What is measured and how |
| [Lessons Learned Framework](lessons_learned.md) | The retrospective, after the mission |

**The five commitments** (everything else elaborates these):

1. Nothing under `data/litdb` is ever edited by hand.
2. One reviewer id, one writer, one machine.
3. `medscale check` opens and closes every session; a session ends with a commit.
4. Corrections are `amend` events; mistakes stay visible next to their fixes.
5. Every friction becomes an MZ-issue in the journal; nothing gets "fixed quickly"
   during the mission.
