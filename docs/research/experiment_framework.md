# Reproducible Experiment Framework

- **Status:** Specification (binding on all model experiments from T4 onward; no
  experiment code exists yet — it is built with its first consumer, the T4 landscape run)
- **Date:** 2026-07-10
- **Related:** [reproducibility policy](reproducibility_policy.md) (the binding science
  policy), [release manifests](../releases/reproducibility.md) (published-artifact
  counterpart), [LLM landscape](../models/llm_landscape.md), RQ1–RQ2

An experiment that cannot be re-run is an anecdote (R7). This framework defines what
every MedScale experiment — landscape run, ablation, training run, evaluation — must
produce, wherever it executes.

## 1. The experiment manifest (required, no exceptions)

Every experiment run emits one canonical-JSON manifest:

| Field | Content |
|---|---|
| `experiment_id` | Stable id: `<phase>-<rq>-<slug>-<seed>` (e.g. `t4-rq1-qwen3-8b-2x2-s0`) |
| `rq_refs` | The research question(s) this run tests — **an experiment with no RQ does not run** |
| `configuration` | Full config (decoding params, grammar on/off, shots, adapter hyperparams) + its content hash |
| `dataset` | Name + version + content hash of every dataset/split consumed |
| `model` | Model id + exact revision/SHA + licence tier (from the [registry](../models/model_registry.md)) |
| `code` | Git SHA of the repo at run time; dirty trees are **not permitted** to run |
| `seeds` | All seeds, explicit (P1: never implicit) |
| `metrics` | Deterministic primary metrics only; outputs as committed result artifacts |
| `environment` | Runner class (see §2), Python, lock hash, GPU + peak VRAM for GPU runs |
| `reproduction` | Exact command(s) to re-run from the committed artifacts |

Manifests and result artifacts are committed with the code that produced them
(policy P10). Comparisons: ≥3 seeds, mean ± 95% CI, constraint/prompting deltas split.

## 2. Runners (Colab, local GPU, cloud GPU)

The runner is an environment detail, never a result variable:

- **Any runner is admissible** if the manifest captures the environment and the run
  starts from a clean git SHA + pinned lock.
- GPU nondeterminism is disclosed and bounded by the reported CI (policy P1) — the
  determinism boundary is *replay-exactness of scoring*, byte-exact scorers over saved
  model outputs. Model *outputs* are saved as artifacts so scoring never requires
  re-inference.
- Colab-class is the reference envelope (compute ceiling ~1 GPU-week per plan); a run
  that needs more is flagged and not attempted without operator approval.
- Secrets/API keys never enter manifests; hosted-API comparisons (e.g. DeepSeek-R1)
  record provider + model version + date and are labeled non-replayable-at-source
  (their saved outputs remain replay-scorable).

## 3. Pre-registration discipline

Falsification criteria live in [research_questions.md](research_questions.md) **before**
the run; experiments test them and never redefine them post hoc. A null result is
committed with the same ceremony as a win.

## 4. Storage layout (established at T4, recorded now)

```
experiments/
└── t4-rq1-2x2/
    ├── manifest-<experiment_id>.json
    ├── outputs/          # saved model outputs (scoring inputs)
    ├── results/          # committed metric artifacts
    └── README.md         # what this experiment tests, how to re-run
```

## 5. Relation to release manifests

Experiment manifests are the *upstream* of release manifests: a model release's
evaluation section must reference experiment manifests, and card-lint fails a release
whose numbers lack them. One provenance chain: experiment → result artifact → model
card → published claim.

**Never train without reproducibility** — operationally: no training job starts unless
the manifest fields above are producible for it, and the T5 data-pipeline gate is green.
