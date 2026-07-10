# ADR-0007 — OpenMed as an Optional Evaluation-Time Adapter

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [OpenMed integration strategy](../architecture/openmed_integration_strategy.md),
  [ecosystem analysis §1](../architecture/ecosystem_analysis.md#1-openmed), Rules R2/R3,
  RQ5

## Context

OpenMed (github.com/maziyarpanahi/openmed; huggingface.co/OpenMed) is a mature
(4.4k stars, v1.8.0 July 2026), Apache-2.0, local-first clinical NLP ecosystem: 1,511+
encoder models for medical NER and PII de-identification. Its licence passes R3 cleanly.
Its capabilities overlap MedScale in exactly one place: deterministic entity spans, which
the T-EXTRACT hallucination metric (RQ5) and benchmark baselines need. Its de-identification
capability is *not* needed by MedScale (synthetic-only, R2 — there is no PHI to remove),
and its application surface (REST, Docker, mobile, browser) is product scope MedScale
must not absorb.

## Decision (proposed)

1. **Role: (C) optional adapter + (D) reference architecture.** Not a dependency, not an
   external service, not a core integration.
2. **Integration point:** an optional extras group (`medscale[openmed]`) providing a thin
   adapter behind a MedScale-owned `SpanExtractor` protocol, used only in T3/T7 for
   (a) span-alignment tooling assists and (b) encoder-NER baselines on T-EXTRACT.
3. **Reproducibility conditions:** model ids pinned by revision + SHA; spans precomputed
   and committed as artifacts; benchmark scoring runs offline and green with OpenMed
   absent; any OpenMed-assisted score is a labeled *secondary* metric — primary metrics
   remain model-free (no model-as-judge).
4. **Explicit non-goals:** no de-identification features in MedScale; no OpenMed runtime
   service; no OpenMed output as ground truth.

## Consequences

**Positive:** RQ5 tooling and a strong, cheap, non-LLM baseline for Papers 2–3 at near-zero
platform cost; a worked example of "integration over reinvention."

**Negative / costs:** one more pinned external artifact to track (mitigated: evaluation-time
only, cached); risk of scope-pull toward clinical NLP features (mitigated by the
non-goals list, which is part of this decision).

## Alternatives considered

- **(A) Core dependency.** Rejected: couples the platform to a fast-moving product repo
  for an evaluation-time need.
- **(B) External service.** Rejected: network at benchmark time breaks determinism and
  offline reproducibility.
- **Build our own medical NER.** Rejected: reinventing an excellent Apache-2.0 project
  (architecture rule 7).
- **Ignore OpenMed.** Rejected: T-EXTRACT baselines and span tooling would be rebuilt
  poorly from scratch at T3.

## Compliance

No code until T3. When implemented: extras group in `pyproject.toml`, pinned revisions
recorded in the benchmark spec, offline-cache test in CI proving the no-OpenMed path.
