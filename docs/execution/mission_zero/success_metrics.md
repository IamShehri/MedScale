# Success Metrics

*Two kinds of numbers. **Hard metrics** have targets and failing them means the
mission (or the platform) failed. **Baseline metrics** have no targets — Mission
Zero exists to establish them; whatever they turn out to be is the finding.*

## Hard metrics (targets)

| Metric | Target | Measured by |
|---|---|---|
| Integrity failures at session boundaries | **0** | `medscale check` results recorded per session |
| Manual edits under `data/litdb` | **0** | git history audit vs journal at mission end |
| Data-loss events (work reported recorded, later absent) | **0** | MZ-issues |
| Milestone snapshot verification | **100%** | `snapshot --verify` per milestone + fresh-clone check |
| Benchmark rerun reproducibility | byte-identical `results_id` | two runs, diff |
| Evidence verification success | **≥ 90%** `source_verified`, every miss explained | `medscale stats` (`evidence.by_verification`) + MZ-issues |
| Issues documented vs discovered | **100%** | journal discipline (self-audited at retrospective) |

## Baseline metrics (no target — measure and report)

| Metric | Definition | Measured by |
|---|---|---|
| Records/hour | decisions ÷ active screening time | journal wall-clock, cross-checked against `decided_at` deltas in the review log |
| Median decision time | median gap between consecutive `decided_at` within a block | review log timestamps |
| First-pass UNCERTAIN rate | `3`-decisions ÷ first-pass decisions | review log |
| Skip rate | skips ÷ records shown | journal counts |
| Correction rate | amend events ÷ total decisions | review log (events with a prior decision) |
| Exclusion profile | breakdown by taxonomy reason | `medscale stats` (`screening.exclusion_reasons`) |
| Evidence extraction rate | objects/hour; claims per included record | journal + evidence store |
| Unplanned interruptions | sessions ended other than by choice | journal |
| Issues per 100 decisions | MZ-issues ÷ decisions × 100, by class | journal |

## Measurement notes

- The audit trail is the instrument: `decided_at`, reviewer, prior decision, and
  reason are already on every event — most metrics are a small script over
  `review_log.jsonl` at retrospective time. Do not build tooling during the
  mission; the data is being collected by design.
- Wall-clock in the journal catches what timestamps cannot (breaks, reading time
  before the first decision).
- Report baseline metrics as distributions where it matters (median + spread for
  decision time), not just means — one agonizing record shouldn't hide in an
  average.
