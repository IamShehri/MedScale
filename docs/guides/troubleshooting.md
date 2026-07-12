# Troubleshooting

*Symptoms first. Every entry: what you see -> what it means -> what to do.*

## `error: workspace root not found: ...`

You are not in the repository root, or `--root` has a typo. All commands default to
`data/litdb` **relative to the current directory**. `cd` to the repo root or pass
the correct `--root`. (The CLI refuses to guess: a wrong path must never come back
as a plausible-looking empty corpus.)

## `error: no corpus at ...`

The directory exists but has never been ingested into. If you expected the shipped
corpus, you are pointing at the wrong directory; the real one is `data/litdb` in
the repository.

## `medscale check` prints violations and exits 1

Something references something that does not exist (e.g. a review event for an
unknown record id). This should never happen through the CLIs. Most likely causes,
in order: a hand-edited file under `data/litdb` (restore it: `git checkout --
data/litdb/<file>`), a partially synced tree (see OneDrive below), or a genuinely
interrupted write. `git diff data/litdb` shows you exactly what changed; the last
committed state is always recoverable.

## `snapshot --verify` says MISMATCH

The tree is not in the state the snapshot names. Read the lines below the verdict -
they name the drifted artifacts:

- `review_log: expected absent, found <hash>` after a screening session is
  **normal** - the knowledge state legitimately moved on. Capture a new snapshot.
- A mismatch when *nothing should have changed* means the tree was modified outside
  the CLIs. Treat it like a failed `check`: `git diff data/litdb`.

A snapshot is an identity, not a backup: verification tells you *whether* the state
matches, git tells you *what* changed.

## Screening session crashed / Ctrl+C / terminal closed

Nothing is lost, ever:

- `screen`: every decision was appended the moment you made it.
- `extract`: every object was written the moment it said `recorded:`.

Run `medscale check`, then just start the command again - both queues resume from
what is already decided.

## I made a wrong screening decision

```bash
uv run medscale screen amend --record <id-prefix> --reviewer <you>
```

The record id is shown on every screening card and in the review log. A prefix is
enough if it is unique. The correction is appended to the audit trail alongside the
original - both remain visible, which is correct for a systematic review. If
evidence was already extracted from the record, `amend` warns you: re-examine those
objects afterwards.

## Garbled characters (é, ", ×) in titles or abstracts on Windows

Cosmetic only. Windows consoles often use the cp1252 encoding; unrenderable
characters degrade to `?` instead of crashing the session, and **the stored data is
untouched** - records are UTF-8 on disk regardless of what your console can
display. For pretty output: `chcp 65001` or use Windows Terminal.

## `git_sha` recorded as `0000000`

You ran a command outside a git checkout, so decisions could not be pinned to a
commit. The decision is still valid and recorded. Work from the repository root of
a real clone to get proper commit pinning.

## OneDrive / Dropbox / iCloud warnings

Do not keep your **working** clone inside a cloud-sync folder if you can avoid it:
sync services can produce conflicted copies of files the CLIs are appending to.
GitHub is the off-machine backup - commit and push after every session. If you must
work inside a synced folder, run `medscale check` at the start of every session and
before every commit.

## `medscale stats` shows `identified: null`

Correct behavior, not a bug: total-identified counts belong to ingestion manifests
(per round, per source), not to the screening log, and the stats document refuses
to fake a number it cannot derive. Get identification counts from
`data/litdb/manifests/`.

## `queue empty - every record has a decision`

You finished (that scope, at least). If you used `--query`, other queries may still
have pending records: `medscale screen status` shows the global picture.

## `no records tagged 'Qx'`

The query id has a typo (valid ids are Q1-Q10, case-sensitive), or you are pointing
at a corpus that was never lineage-tagged.

## Something else

`medscale <command> --help` for every command's options and examples;
[Quick Start](research_quickstart.md) for the happy path;
[First Systematic Review](first_systematic_review.md) for stage-by-stage detail.
If the tooling did something this page does not explain, that is a bug in the page:
record it.
