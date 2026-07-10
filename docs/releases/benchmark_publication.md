# Benchmark Publication

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10
- **Related:** [Blueprint §8](../vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md),
  [reproducibility policy](../research/reproducibility_policy.md)

MedScale-Bench is the crown artifact; its publication rules are correspondingly the
strictest. A benchmark is released as **one versioned unit**: specification + data +
scorers + baseline results.

## The unit of release

| Component | Requirement |
|---|---|
| Specification | Task definitions, metric formulae, split policy, failure taxonomy — a document, versioned with the release |
| Data | Passes the [dataset checklist](release_process.md); split content hashes published |
| Scorers | Deterministic, unit-tested, byte-identical re-runs demonstrated in CI; **no LLM-as-judge in any primary metric** — ever |
| Baselines | At least: unconstrained base, grammar-constrained base (the 2×2 anchors), and any cheap non-LLM baseline (e.g. encoder-NER for T-EXTRACT). Why: a benchmark shipped without baselines invites leaderboard gaming and cannot demonstrate its own headroom |

## Scoring reproducibility

`score(model_outputs, bench_version, seed) → results` must be a pure function of its
arguments. Published scores carry: bench version, model + version, seeds (≥3), mean ±
95% CI, constraint/prompting deltas split, scorer version, environment manifest. A
score whose manifest is missing any element is not a score (R7).

## Immutable versions

- Task or metric definition changes ⇒ **MAJOR** bump ⇒ a new leaderboard; old scores
  are never mixed with new ones (stated in the release notes in bold).
- Additive tasks ⇒ MINOR; existing task scores remain valid.
- Scorer bug fixes that change any score ⇒ MAJOR (a "fix" that moves numbers is a
  definition change), with a re-scored baseline table and an erratum note.

## Leaderboard policy

- **v0 (T3–T7):** results table in the repo, maintained by the operator; every row
  requires a submitted manifest and reproducible outputs.
- **v1 (H2):** held-out test administration — submissions run against a private test
  split; public dev split for development. Why deferred: a held-out administration
  needs infrastructure and community volume that do not exist yet; pretending
  otherwise would produce a decorative leaderboard.
- Integrity firewall (Vision §7): MedScale/Afia results appear under exactly the same
  rules and manifests as anyone else's; unflattering results are published identically.

## Acceptance criteria for hosting external results

Manifest complete · outputs reproducible from released model + bench version · licence
of the evaluated model recorded · no test-split tuning attestation · deterministic
primary metrics only.

## Publication workflow

1. Bench spec frozen (versioned doc) →
2. Data + scorers green through checklists →
3. Baselines run, manifests committed →
4. GitHub Release `medscale-bench-vX.Y` →
5. HF dataset mirror + (later) `benchmark-viewer` Space →
6. Paper 2 cites the released version.
