# Mission Zero Protocol

*Operational instructions for the entire study. Written in the imperative because
they are orders — including to future-you at the end of a long screening session.*

## Preparation (once, already done at `d2c1b6b`)

- Pre-flight passed: gates green, `medscale check` CLEAN, baseline
  `cfdfcce5e2830391` VERIFIED, ADR-0022 Accepted.
- Choose your reviewer id and write it in [journal.md](journal.md). It never changes.
- Work from exactly one clone on exactly one machine for the duration. If that
  clone lives under OneDrive, run `medscale check` at session start *and* end
  without exception (it is your sync-corruption tripwire).

## Daily workflow

The mission's order of work is fixed:

1. **Uncertain duplicates** — all 16 groups, before any screening.
2. **Title/abstract screening** — Q2 (148), then Q6 (143), then Q4, then the rest,
   under ADR-0022 semantics (INCLUDE = passes title/abstract, nothing more).
3. **Evidence extraction** — *gated*: begins only after Q2+Q6 screening is complete
   **and** ADR-0018 is decided. Not before, no exceptions.
4. **Benchmark** — only from mission-extracted evidence, at the end.

## Beginning of session

```bash
git status                 # must be clean (previous session was committed)
uv run medscale check      # must print CLEAN - if not: incident_response.md
uv run medscale screen status
```

Note the wall-clock start time in your journal draft.

## During the session

- Always `--reviewer <your-id>`. Never screen as `operator`.
- Use `--limit` (25–50 is a sensible screening block). Decision fatigue is a
  scientific-validity threat, not a productivity statistic.
- Don't agonize at the abstract level: `3` (maybe) is cheap and comes back;
  a wrong EXCLUDE is the only decision that silently costs the study.
- The moment anything surprises you — error, confusing prompt, wrong count, "I
  wish it did X" — put an MZ-issue in the journal *right then*, one line is
  enough; polish later. Then continue. Do not fix anything.

## End of session

```bash
uv run medscale check      # CLEAN again
uv run medscale screen status
git diff --stat            # only data/litdb and the journal should have changed
```

Fill a session entry from [journal_template.md](journal_template.md), then commit.

## Commit policy

- **One commit per session**, containing the session's `data/litdb` changes and the
  journal entry together (the decisions and their context travel as one unit).
- Message: `study(mission-zero): <scope>, <n> decisions (<reviewer>)`
  e.g. `study(mission-zero): Q2 screening, 25 decisions (az)`.
- Push after every commit. An unpushed session exists on one disk.
- Never commit with a failing `medscale check`.

## Snapshot policy

Snapshots mark citable milestones, not sessions. Capture (`uv run medscale
snapshot`) and commit the snapshot file when:

1. the 16 duplicate groups are fully resolved;
2. each query's screening completes (post-Q2, post-Q6, ...);
3. extraction campaigns start and end;
4. a benchmark is about to be specified (the spec binds to this snapshot).

The pre-screening baseline `cfdfcce5e2830391` is permanent history — it will (and
should) MISMATCH from now on. Verify the *latest* milestone snapshot when you want
assurance, e.g. after a sync scare.

## Reviewer identity policy

One id, chosen before the first decision, recorded in the journal, used for every
`--reviewer` flag for the whole mission. If a second reviewer ever joins, that is a
new ADR *and* the D2 (multi-writer) trigger — stop and plan; do not just start
screening from a second machine.

## Interruption policy

- Ctrl+C, crashes, closed terminals: **safe at any moment.** Decisions and
  evidence objects persist as they are recorded. Rerun the same command; the queue
  resumes where it left off. Log an unplanned interruption in the journal (it is a
  metric).
- Support (Claude) interrupts the mission only for: data-integrity risk, broken
  reproducibility, threatened audit trail, compromised scientific validity.
  Everything else is journal evidence.

## Correction policy

- Wrong decision → `uv run medscale screen amend --record <id-prefix> --reviewer
  <your-id>`, with an honest note; the original stays in the log next to the fix.
- Batch your corrections at session start rather than context-switching mid-queue,
  unless the mistake blocks what you're doing now.
- If `amend` warns the record already has evidence citing it: finish the amend,
  then re-examine those evidence objects the same session and journal the outcome.
- Corrections are counted (correction rate is a mission metric) but never
  penalized: an audit trail with zero corrections over 1,346 human decisions would
  itself be suspicious.

## Evidence extraction policy

- **Gate:** Q2+Q6 screening complete and ADR-0018 decided. Both, before the first
  `medscale extract` against real INCLUDEs.
- Extract atomic, quotable claims; use PICO fields where the abstract supports
  them; per ADR-0022 §7 all mission evidence is abstract-anchored — extract
  conservatively and never present it as synthesis-grade.
- A `FAIL` on a verification check is *information, not an error to work around*:
  the object stays honestly unverified, gets an MZ-issue, and you move on.
- Extraction sessions are shorter than screening sessions (claims demand more
  judgment). `--limit 5` to start.

## Benchmark policy

- One real benchmark, built at the end from mission evidence, bound to a fresh
  committed snapshot, gold set annotated by the reviewer id that extracted.
- Before it may be cited anywhere: `bench validate` passes; `gold-oracle` scores
  1.0 and `empty` scores 0.0; the run is executed **twice** and the `results_id`
  is byte-identical both times. Reproducibility is demonstrated, not assumed.
- Benchmark creation is a library task; it is performed with support, and the
  creating script is committed alongside the spec.
