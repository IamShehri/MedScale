# Daily Research Checklist

*One page. Every session. In order.*

## Before starting

- [ ] `git status` — clean (last session was committed and pushed)
- [ ] `uv run medscale check` — CLEAN (else: [incident response](incident_response.md), do not screen)
- [ ] `uv run medscale screen status` — note the queue; unresolved duplicate groups come first
- [ ] Note wall-clock start time
- [ ] Any corrections queued from last session? `screen amend` them now

## During screening

- [ ] `--reviewer <your-id>` on every command — never `operator`
- [ ] `--limit 25`–`50` per block; stand up between blocks
- [ ] In doubt at abstract level → `3` (maybe), not a reluctant EXCLUDE
- [ ] EXCLUDE reason = the *primary* reason, honestly
- [ ] Anything surprising → one-line MZ-issue in the journal immediately, then continue
- [ ] Never fix, tweak, or hand-edit anything — record and move on

## Before committing

- [ ] `uv run medscale check` — CLEAN
- [ ] `uv run medscale screen status` — numbers match what you think you did
- [ ] `git diff --stat` — only `data/litdb/**` and the mission journal changed
- [ ] Milestone completed (duplicates done / query finished)? → `uv run medscale snapshot`

## End of session

- [ ] Journal entry written ([template](journal_template.md)) — duration, counts, issues
- [ ] `git add data/litdb docs/execution/mission_zero && git commit -m "study(mission-zero): <scope>, <n> decisions (<id>)"`
- [ ] `git push`
- [ ] Next session's goal written down while it's obvious

## Never forget

- Nothing under `data/litdb` is ever edited by hand. Ever.
- One reviewer id. One machine. One writer.
- Ctrl+C is always safe — recorded work is already on disk.
- Mistakes are corrected with `amend`, visible forever, and that is correct.
- An unpushed session exists on one disk.
