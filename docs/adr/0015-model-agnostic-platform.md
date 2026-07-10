# ADR-0015 — The Model-Agnostic AI Platform (`medscale.modelkit`)

- **Status:** Accepted (2026-07-10; created and approved by operator directive: "Do not
  optimize MedScale around a single open LLM… Every supported model must plug into the
  same interface so models can be replaced without changing MedScale")
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Amends:** ADR-0006 compliance clause ("the registry lives as a documentation table…
  until T4 needs it in structured form") — the structured registry is pulled forward by
  this directive; the documentation table remains the human narrative, the code is the
  enforceable twin
- **Related:** [ADR-0006](0006-model-access-strategy.md) (tiers),
  [ADR-0012](0012-layered-architecture-model.md) (AI Infrastructure layer),
  [experiment framework](../research/experiment_framework.md),
  [LLM landscape](../models/llm_landscape.md)

## Context

MedScale's thesis has always been that models are replaceable and the verification
spine is not — but until now that replaceability was prose. Without a code-level
contract, the first inference backend written for one model would quietly become the
platform's shape, and "model-agnostic" would die by default. The operator has directed
that the infrastructure be built first, with model selection driven only by benchmark
results on MedScale tasks.

## Decision

1. **`medscale.modelkit` is the AI-Infrastructure layer's contract surface**, five
   modules, all pure and dependency-free:
   - `interfaces` — `TextGenerator` / `SpanExtractor` protocols, `ModelRef`
     (id + revision + quantization + backend = identity), typed request/result
     envelopes. **Grammar is a request field**: a backend that cannot enforce it must
     raise, never silently ignore it.
   - `registry` — the machine-readable registry; the ADR-0006 invariant is now a
     constructor error: a Tier-2 or non-generative model *cannot be represented* as an
     adapter-base candidate.
   - `recipes` — content-addressed LoRA/QLoRA recipe schemas (`recipe_id` =
     content hash). Schemas only.
   - `manifests` — deterministic experiment manifests (canonical JSON, LF), runner
     detection/recording for Colab, Kaggle, RunPod, Lambda, local, cluster. No RQ →
     the manifest does not construct; dirty tree → does not construct.
   - `reporting` — the single implementation of mean ± 95% CI (Student-t) over seeds;
     single-seed numbers report without a CI rather than a dressed-up one.
2. **Portability policy:** the runner is a recorded environment detail, never a result
   variable. Replay-exactness lives in scoring over saved outputs; any machine that can
   produce a valid manifest is an admissible runner.
3. **What remains gated (unchanged by this ADR):** inference backends (optional extras
   at T4 — transformers/llama.cpp/hosted-API adapters implementing `TextGenerator`);
   training execution (T5); benchmark tasks and runners (T3, which will consume these
   interfaces); model downloads (nothing in modelkit fetches weights).
4. **Selection discipline restated as code contract:** T4 selection (reserved ADR-0002)
   is decided by benchmark manifests produced through these interfaces — never by
   popularity, never by leaderboard scores on non-MedScale tasks.

## Consequences

**Positive:** replaceability becomes structural — swapping a model changes a `ModelRef`;
the licence-tier rule is enforced at object construction; every future experiment is
manifest-shaped from birth; T3/T4/T5 inherit interfaces instead of inventing them.

**Negative / costs:** interfaces designed before their heaviest consumers (T4 backends)
may need revision — accepted: they encode only what the framework spec already requires,
and they are cheap to version now, expensive to retrofit later. 42 new tests carry the
contracts.

## Alternatives considered

- **Wait for T4 and let the first backend define the interface.** Rejected: that is
  precisely how platforms become single-model-shaped.
- **Adopt an existing abstraction layer (LangChain/LlamaIndex).** Rejected: heavy
  dependencies, unstable APIs, and none treats grammar-constraint, licence tiers, or
  deterministic manifests as first-class — the parts MedScale exists for.
- **Registry as JSON data file now.** Deferred: code-as-data keeps mypy/tests on every
  row; a JSON export lands when card-lint CI needs one (releases/ci_cd design).

## Compliance

Backends must implement these protocols to enter T4; PRs adding a backend as a hard
dependency fail review (optional extras only). The docs table and `REGISTRY` must stay
consistent — a drift test may be added when the table format stabilizes.
