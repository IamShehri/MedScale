# ADR-0029: Benchmark Determinism and Replay Contract

## Status

Accepted

## Context

Benchmarks are scientific claims. A benchmark result is only meaningful if another
researcher can reproduce it years later with the same inputs and the same scorer.
MedScale already has a benchmark runner (`medscale.bench.run`), task model
(`medscale.bench.tasks`), and deterministic scorers (`medscale.bench.scorers`).
What it lacks is an explicit frozen contract for:

- what makes a benchmark run reproducible;
- what fields must match on replay;
- how mismatches fail (loudly or silently).

Without this contract, a "regression" may simply be a dataset drift, a scorer tweak,
or a hand-edited run file. None of those are acceptable in a reproducibility-first
research platform.

## Decision

Adopt a replay contract with these rules:

1. Every benchmark run artifact records five frozen identity fields:
   `spec_id`, `snapshot_id`, `software_version`, `git_sha`, `scorer_version`.

2. A future `bench replay` command recomputes those five identities from the
   current tree and compares them byte-for-byte to the stored artifact.

3. Any mismatch fails with an explicit, actionable message (spec drift, snapshot
   drift, software version drift, repo state drift, scorer drift). Replay never
   silently reuses a stored result.

4. The manifest system records:
   `benchmark_id`, `dataset_id`, `git_sha`, `software_version`, `seed`,
   task versions, scorer versions.
   The manifest is content-addressed; any edit produces a new manifest id.

5. Task definitions become explicit modules under `medscale/bench/tasks/` so their
   version and seed semantics are inspectable and auditable.

6. Replay is artifact-first:
   `medscale bench replay <artifact.json>` reads a single run artifact and
   validates its five frozen identities against the current tree.

## Consequences

- Run artifacts become first-class reproducibility certificates, not just score logs.
- Benchmark publication requires a matching manifest and verified replay.
- Model systems added later plug in through the existing `EvidenceSystem` protocol.
- No new runtime dependencies; replay is stdlib/check-only.

## Alternatives considered

- Silent best-effort replay: rejected; hides drift and produces irreproducible science.
- Human-curated reproducibility notes: rejected; manual notes drift from actual artifacts.
- Versioned datasets only: rejected; code, scorer, and snapshot changes also affect results.

## Implementation

M3 milestone: bench/tasks/ package, manifest files, CLI init/replay, and tests.

## References

- docs/execution/v0.2/adr_implementation_tracker.md
- docs/execution/v0.2/roadmap.md
