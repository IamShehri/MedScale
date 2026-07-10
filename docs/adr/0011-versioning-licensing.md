# ADR-0011 — Artifact Versioning Schemes and the Licensing Matrix

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none (completes the licence decision left as a "working assumption"
  in Vision §8; the Apache-2.0 LICENSE file has been in force since T0)
- **Superseded by:** none
- **Related:** [ADR-0006](0006-model-access-strategy.md) (model tiers),
  [ADR-0009](0009-evidence-model.md) (schema versioning),
  [releases/versioning.md](../releases/versioning.md),
  [releases/licensing.md](../releases/licensing.md)

## Context

Five artifact classes with different mutation semantics need version schemes that make
*content change visible in citations*; and the platform invariant (everything shipped
permits derivatives + commercial use) needs a per-artifact licensing matrix rather than
a single repo licence, because datasets inherit composite upstream terms (CC0 OpenAlex
fields, ODC-BY Semantic Scholar fields, non-redistributable PubMed abstracts) and model
weights inherit base-model terms (Tier-1 clean vs Tier-2 passthrough).

## Decision (proposed)

1. **Versioning schemes** as specified in [releases/versioning.md](../releases/versioning.md):
   SemVer for the package (0.x rules; 1.0.0 gated on MESC-v0 + Bench v0 + litdb v1);
   `vX.Y` without PATCH for models/datasets/benchmarks (any content change ≥ MINOR;
   comparability-breaking change = MAJOR; benchmark MAJOR = new leaderboard);
   append-only integers for schemas (per ADR-0009); prefixed git tags
   (`<artifact>-vX.Y`) for non-package artifacts in the single repo.
2. **Licensing matrix** as specified in [releases/licensing.md](../releases/licensing.md):
   Apache-2.0 repo-wide (code + docs); Apache-2.0 for MedScale-authored adapter weights
   over Tier-1 bases only; CC-BY-4.0 for published synthetic datasets; field-level
   composite licensing for litdb exports (CC0 pass-through, ODC-BY attribution,
   exclusion of non-redistributable fields); permissive-only runtime dependencies;
   Apache-2.0-compatibility test for anything vendored.
3. **Tier-2 derivatives** (e.g. MedGemma) remain unreleased absent a dedicated
   Accepted ADR (restates ADR-0006 at the release boundary).
4. **Citation:** CITATION.cff maintained per release; artifact cards carry citation
   blocks; papers cite exact artifact versions, never "latest".

## Consequences

**Positive:** versions become claims about immutable content; licence questions get
answered once, at the matrix, instead of per-release under time pressure; the
long-pending "licence ADR" debt is closed.

**Negative / costs:** no-PATCH versioning makes even small data corrections visible
version bumps (intended — silence is the failure mode); field-level dataset licensing
demands per-field provenance discipline (already required by R1/R3, so the marginal
cost is documentation).

## Alternatives considered

- **CalVer for datasets.** Rejected: dates say *when*, not *whether comparability
  broke* — the property citations need.
- **Single CC licence for all data.** Rejected: upstream terms are heterogeneous;
  blanket licensing would either over-claim (relicensing CC0/ODC-BY sources wrongly)
  or under-claim (restricting wholly-synthetic data needlessly).
- **Dual-licensing docs (CC-BY) vs code (Apache-2.0).** Rejected for now: one repo,
  one licence is simpler and sufficient; standalone published documents (preprints)
  handle their own terms at publication.

## Compliance

On acceptance, [releases/versioning.md](../releases/versioning.md) and
[releases/licensing.md](../releases/licensing.md) become binding; release validation
(ci_cd design) enforces SPDX ids and manifest version fields mechanically.
