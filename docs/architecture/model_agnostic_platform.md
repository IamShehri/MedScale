# The Model-Agnostic AI Platform

- **Status:** Implemented contracts (ADR-0015); backends/training/benchmarks gated
- **Date:** 2026-07-10
- **Related:** [ADR-0015](../adr/0015-model-agnostic-platform.md),
  [model registry](../models/model_registry.md), [LLM landscape](../models/llm_landscape.md),
  [experiment framework](../research/experiment_framework.md)

MedScale is never optimized around a single LLM. `medscale.modelkit` is the contract
surface that makes that structural: models plug into MedScale; MedScale never bends
around a model.

## The plug-in rule

```
            ┌──────────────────────────────────────────────────────┐
            │                  MedScale (fixed)                    │
            │  bench runners · experiment pipelines · recipes ·    │
            │  manifests · reporting · verification spine         │
            └───────────────────────┬──────────────────────────────┘
                                    │ TextGenerator / SpanExtractor
                                    │ (protocols + ModelRef)
        ┌──────────────┬────────────┼────────────┬─────────────────┐
   transformers    llama.cpp    hosted API   OpenMed NER        (future)
    (extra, T4)    (extra, T4)  (extra, T4)  (extra, T3)      any backend
```

- A model that cannot implement the protocol does not enter T4. A backend that cannot
  enforce a requested grammar must **raise** — silent degradation of constrained
  decoding is prohibited by contract and by test.
- `ModelRef` (id + revision + quantization + backend) is the unit of replacement:
  swapping models changes data, not code.
- The registry enforces licence law at construction: `Role.BASE_CANDIDATE` is
  unrepresentable for Tier-2 or encoder models.

## Portability (Colab first, portable everywhere)

Experiments start on Google Colab and must run unchanged on local machines, RunPod,
Kaggle, Lambda Labs, and future clusters:

| Concern | Mechanism |
|---|---|
| Where did this run? | `detect_runner(env)` → colab/kaggle/runpod/cluster/local (Lambda bare VMs classify local; override explicitly) |
| Is the run valid anywhere? | The manifest doesn't care about the runner — it requires clean code SHA, dataset hashes, seeds, RQ refs |
| Are results comparable across runners? | Replay-exact scoring over **saved model outputs**; GPU nondeterminism disclosed and bounded by the reported CI |
| Byte-stability | Canonical JSON + LF everywhere, on every OS |

## What executes when

| Component | State | Gate |
|---|---|---|
| Interfaces, registry, recipes, manifests, reporting | ✅ live, 42 tests | — |
| Benchmark runner consuming `TextGenerator` | ⬜ | T3 |
| Inference backends (extras: `medscale[transformers]`, …) | ⬜ | T4 |
| Training execution from `TrainingRecipe` | ⬜ | T5 |
| Model selection (ADR-0002) | ⬜ | T4 benchmark manifests only |

**Selection is benchmark-driven, structurally:** the only path from "candidate" to
"MESC base" runs through experiment manifests produced by these interfaces on MedScale
tasks. Popularity, marketing, and exam-QA leaderboards have no representation in the
type system — deliberately.
