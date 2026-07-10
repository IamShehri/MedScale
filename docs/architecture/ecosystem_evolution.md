# Ecosystem Evolution — The Linux-Style Long View

- **Status:** Horizon-3 vision (documented, deliberately not implemented; extraction is
  gated, below)
- **Date:** 2026-07-10
- **Related:** [ADR-0004](../adr/0004-t0-foundation-scope.md) (single package — still
  binding), [ADR-0012](../adr/0012-layered-architecture-model.md) (capability layers),
  Founder's Permanent Directive (2026-07-10)

MedScale should eventually be an *ecosystem* of independently valuable systems — the way
Linux is not a kernel but a world. This document records that ambition **and the gates
that keep it from prematurely fragmenting a solo-maintained platform.** Today, one
repository and one Python package (`medscale`) is correct (ADR-0004); ecosystems are
*extracted from* working monoliths, not designed in advance — Linux itself began as one
tree.

## Future systems → where they live today

| Future system (directive) | Lives today as | Graduation phase |
|---|---|---|
| `medscale-core` | `medscale.reproducibility` + `medscale.provenance` (namespace consolidation: [ADR-0014](../adr/0014-core-namespace.md), Proposed) | H2+ |
| `medscale-verification` | The spine as it grows code: validators (T2), deterministic scorers (T3) | H2+ |
| `medscale-evidence` | `medscale.evidence` (ADR-0009) | H2+ |
| `medscale-litdb` | `medscale.litdb` (T1) | H2+ |
| `medscale-modelkit` / `medscale-registry` | `medscale.modelkit` (ADR-0015; registry inside) | H2+ |
| `medscale-fhir` | `medscale.fhirkit` (T2, not started) | H2+ |
| `medscale-bench` | `medscale.bench` (T3, not started) | H2+ — likely the **first** worth extracting (external labs run benchmarks without wanting the rest) |
| `medscale-training` | Recipes exist (`modelkit.recipes`); execution gated (T5) | H3 |
| `medscale-runtime` / `medscale-sdk` / `medscale-hub` | Do not exist; runtime/serving and a hosted hub are H3 platform questions | H3 — each needs its own ADR |
| `medscale-agents` | Explicitly gated (ADR-0005: validator-gated, H2+) | H3 |

## Graduation gates (all must hold before any extraction)

1. **External consumers exist** who want the piece without the whole.
2. **The API has been stable** across ≥2 release cycles.
3. **Independent release cadence is actually needed** (not aesthetically pleasing).
4. **Maintainer capacity exists** — every extracted package is its own CI, versioning,
   and issue tracker; a solo maintainer multiplying repos is how ecosystems die young.
5. **A dedicated ADR** records the split, the dependency direction (extracted packages
   never depend on applications — ADR-0003's rule generalized), and the migration path.

Until then: the subpackage boundaries inside `medscale` *are* the future package
boundaries — kept clean now (minimal coupling, no cross-layer imports except through
the spine) precisely so extraction later is `git mv`, not surgery.

## Interface roadmap (model-agnostic platform growth)

The directive names ten model interfaces. Protocols are added **with their first
consumer**, never ahead (empty abstractions rot):

| Interface | Status | First consumer |
|---|---|---|
| Text generation (+ grammar-constrained as a request field) | ✅ `TextGenerator` | T3/T4 |
| Extraction (spans) | ✅ `SpanExtractor` | T3 baselines (RQ5) |
| Structured output | Covered by grammar-constrained generation (a schema *is* a grammar) — no separate protocol unless evidence demands one | — |
| Classification | ⬜ | T1/H2 screening-assist experiments (secondary, never decider of record) |
| Embedding | ⬜ | H2 retrieval (registry role exists) |
| Evaluation | ⬜ deliberately **never** an LLM-judge primary metric; a protocol only if secondary labeled scores need one | H2 |
| Function calling / Reasoning / Summarization | ⬜ | H2+ agents & synthesis, ADR-gated |

## Registry schema evolution

`ModelEntry` v1 records *verifiable static facts* (licence, tier, kind, roles, params).
The directive's measurement fields — benchmark history, evaluation reports,
hallucination metrics, verification metrics, FHIR capability — become honest only when
T3/T4 produce manifests to link. Planned v2 (at T4, append-only): `context_length`,
`supported_features`, `benchmark_results: tuple[manifest ref, ...]`. **No field is added
before real data can fill it** — a registry with empty capability columns is marketing,
not measurement. Models are evaluated, never trusted.
