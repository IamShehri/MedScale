# OpenMed Integration Strategy

- **Status:** Strategy (implements no code; governed by [ADR-0007](../adr/0007-openmed-adapter.md), Proposed)
- **Date:** 2026-07-10
- **Related:** [ecosystem analysis §1](ecosystem_analysis.md#1-openmed), Rules R2/R3,
  [RQ5](../research/research_questions.md)

## Position in one sentence

OpenMed is an **optional, evaluation-time adapter and a reference architecture** — never a
core dependency, never a runtime service MedScale requires.

## What we can reuse

1. **NER models as deterministic span tooling (RQ5).** The T-EXTRACT hallucination metric
   needs entity spans aligned between source note and generated bundle. OpenMed's
   Apache-2.0 encoder NER models (110M–1B) are local, deterministic per fixed weights, and
   domain-tuned — a credible *assist* for building span-alignment fixtures and a
   *baseline family* to report against. Usage rule: **pinned model revision + SHA, spans
   cached as committed artifacts** so benchmark scoring never requires a live model
   (Principle 2, reproducibility policy). The primary scorer itself stays
   model-free; any OpenMed-assisted variant is labeled secondary.
2. **Extraction baselines for MedScale-Bench.** Reporting "encoder-NER pipeline vs
   grammar-constrained LLM" on T-EXTRACT strengthens Paper 2/3 (a strong, cheap,
   non-LLM baseline is exactly what honest benchmarks lack).
3. **Reference architecture (read, don't import).** Three patterns worth emulating:
   local-first inference as a privacy stance; a curated HF model registry with pinned
   revisions; multi-backend serving kept *out* of the core library.

## What we should avoid

- **De-identification as a MedScale feature.** MedScale is synthetic-only (R2); it has no
  PHI to de-identify. Shipping de-id invites exactly the real-data workflows the PHI
  boundary forbids. If Afia needs de-id, Afia integrates OpenMed directly — downstream,
  not through MedScale.
- **The application surface.** REST API, Docker service, mobile SDKs, browser inference —
  505 open issues of product surface MedScale must not inherit.
- **Hard dependency.** `medscale` must install, test, and benchmark green with OpenMed
  entirely absent.
- **Treating OpenMed output as ground truth.** NER predictions are model output; ground
  truth in MedScale is validator output and hand-verified fixtures, never another model's
  guess (no model-as-judge in primary metrics).

## Integration shape (when T3/T7 arrive — not now)

```
medscale.bench (T3)
  └── baselines/            # optional extras group: `medscale[openmed]`
        openmed_ner.py      # thin adapter: text -> [(span, label, score)]
                            # pinned model id + revision + SHA; offline cache
```

- Adapter interface owned by MedScale (`SpanExtractor` protocol), so OpenMed is one
  pluggable implementation, not a coupling point (avoids vendor lock-in, Rule 6/7 of the
  architecture rules).
- No network at benchmark time: spans are precomputed into committed artifacts.

## How it fits the mission

OpenMed covers the *clinical-NLP-over-real-text* layer of the healthcare stack so
MedScale doesn't have to. MedScale's unique value — verification, grammar, deterministic
benchmarks — stays undiluted, and an excellent open project is integrated rather than
reinvented.
