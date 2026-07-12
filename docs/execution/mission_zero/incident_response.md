# Incident Response Guide

*Symptom → recognize → act. "STOP" means no further research writes until resolved;
"CONTINUE" means journal it and keep working. Every incident gets an MZ-issue in the
[journal](journal.md) — class, reproduction, impact — no matter how it ends.*

## Failed integrity check (`medscale check` exits 1)

- **Recognize:** violations listed, `status: DIRTY`.
- **Act:** **STOP.** Do not screen, extract, or commit. `git status` + `git diff
  data/litdb` — identify what changed outside the CLIs. If the working tree drifted
  from the last good commit: `git checkout -- data/litdb`, re-run `check`, then
  re-enter any lost decisions through the CLI (your last commit bounds the loss to
  one session). If the *committed* state is dirty, stop entirely and investigate
  with support before anything else is written.
- **Resume when:** CLEAN again. **Document:** MZ-issue (Bug or Missing validation),
  including what `git diff` showed.

## Snapshot mismatch (`snapshot --verify` says MISMATCH)

- **Recognize:** read the drift lines — they name the changed artifacts.
- **Act:** if work legitimately happened since capture (review_log drifted after a
  screening session): **CONTINUE** — that is a snapshot doing its job; capture a new
  milestone snapshot if one is due. If *nothing* should have changed since capture:
  treat as a failed integrity check (STOP, `git diff`).
- **Document:** only the alarming case needs an MZ-issue.

## Duplicate discovered late (mid-screening, past the duplicates stage)

- **Recognize:** the record on screen is the same work as one you already decided.
- **Act:** **CONTINUE** — press `4` (Duplicate); in the notes, paste the record_id
  of the copy you are keeping. No group machinery is needed after the fact; the
  event carries the linkage.
- **Document:** MZ-issue (Research workflow) only if it happens repeatedly — that
  would mean the dedupe pass has a systematic hole.

## Accidental exclusion (or any wrong decision)

- **Recognize:** you realize a record was mis-decided — seconds or sessions later.
- **Act:** **CONTINUE.** `uv run medscale screen amend --record <prefix> --reviewer
  <id>` with an honest note. If amend warns about citing evidence, re-examine those
  objects the same session.
- **Document:** no MZ-issue needed — corrections are normal science. Journal the
  count (it is a metric).

## Interrupted extraction (crash, Ctrl+C, closed terminal)

- **Recognize:** session ended without the summary line.
- **Act:** **CONTINUE.** Nothing is lost — every object was written when it said
  `recorded:`. Run `medscale check`, then `medscale extract` again; the queue
  resumes. 
- **Document:** journal the unplanned interruption (metric); MZ-issue only if
  anything actually failed to persist (that would be a Critical bug).

## Git conflict

- **Recognize:** `git pull`/`push` reports divergence or merge conflict touching
  `data/litdb`.
- **Act:** **STOP for data files.** Never hand-merge a JSONL log — that is a manual
  repository edit. This should be impossible under the one-machine rule, so first
  ask *why* there are two writers. Recovery: keep the pushed (remote) state as
  truth, re-enter the unpushed session's decisions through the CLI. Conflicts in
  docs (journal) may be merged normally.
- **Document:** MZ-issue (Research workflow, High) — the one-machine rule failed;
  say how.

## Corrupted workspace (unreadable files, parse errors, sync artifacts)

- **Recognize:** tracebacks mentioning JSON parsing, `medscale check` crashing
  (not failing — crashing), OneDrive "conflicted copy" files appearing under
  `data/litdb`.
- **Act:** **STOP.** Delete nothing. `git status` to see damage extent; restore
  tracked files from the last commit (`git checkout -- data/litdb`); delete
  untracked conflicted-copy litter only after confirming the restored tree is
  CLEAN. Re-enter the bounded lost work via CLI.
- **Document:** MZ-issue (Bug, Critical if the CLIs caused it; Research workflow
  if sync did). If sync did it: move the working clone out of OneDrive before the
  next session.

## Missing provenance (extraction verification FAIL)

- **Recognize:** `[FAIL] provenance_anchor: ...` (or `source_reference`) during
  extract; object recorded as `unverified`.
- **Act:** **CONTINUE.** Do not retry-until-green, do not work around. The object
  stays honestly unverified; that is the verification system telling the truth.
- **Document:** MZ-issue (Scientific): which record, which check, what the archive
  actually contains. A pattern here is major mission evidence.

## Benchmark failure

- **Recognize:** `bench validate` exits 1 (snapshot no longer verifies, or gold no
  longer resolves), or a run errors, or a rerun's `results_id` differs.
- **Act:** validate-failure after new decisions is **expected drift** — the
  benchmark is pinned to an older knowledge state; CONTINUE screening, and re-pin
  or defer the benchmark to a fresh snapshot at the milestone. A **rerun producing
  a different `results_id` is a STOP** for all benchmark work: that is a
  reproducibility break, the exact thing the mission exists to catch.
- **Document:** MZ-issue; Critical if reproducibility broke.

## Anything not on this page

Default posture: if data integrity, reproducibility, the audit trail, or scientific
validity could be at risk — STOP and ask support. Otherwise journal it and keep
going. When unsure which case you're in, that uncertainty itself is the answer: STOP.
