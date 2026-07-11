"""medscale.modelkit — the model-agnostic AI-infrastructure layer (ADR-0015).

Stability: **public-frozen protocols** (``TextGenerator``, ``SpanExtractor``,
``ModelRef``) — backends must implement these to exist; everything else internal.

MedScale is never optimized around a single LLM. This package defines the contracts
every model must satisfy to participate — so models can be replaced without changing
MedScale:

- **interfaces**: ``TextGenerator`` / ``SpanExtractor`` protocols and the typed
  request/result envelopes (grammar-constrained generation is a first-class request
  field, not a backend detail);
- **registry**: the machine-readable, licence-first model registry (two tiers x roles);
- **recipes**: typed, content-addressed LoRA/QLoRA training recipes (schemas only —
  training *execution* is gated at T5);
- **manifests**: deterministic experiment manifests + runner portability
  (Colab, Kaggle, RunPod, Lambda, local, cluster);
- **reporting**: honest metric summaries (mean ± 95% CI over seeds).

No ML dependency lives here; inference backends plug in later as optional extras and
must implement these protocols to exist at all.
"""

from __future__ import annotations

from medscale.modelkit.interfaces import (
    FinishReason,
    GenerationRequest,
    GenerationResult,
    ModelRef,
    Span,
    SpanExtractor,
    TextGenerator,
)
from medscale.modelkit.manifests import (
    DatasetSnapshot,
    ExperimentManifest,
    RunnerClass,
    RunnerEnv,
    detect_runner,
    read_manifest,
    write_manifest,
)
from medscale.modelkit.recipes import AdapterMethod, TrainingRecipe
from medscale.modelkit.registry import (
    REGISTRY,
    ModelEntry,
    ModelKind,
    Role,
    eligible_bases,
    extraction_baselines,
    get_entry,
    validate_registry,
)
from medscale.modelkit.reporting import MetricSummary, summarize_metric

__all__ = [
    "REGISTRY",
    "AdapterMethod",
    "DatasetSnapshot",
    "ExperimentManifest",
    "FinishReason",
    "GenerationRequest",
    "GenerationResult",
    "MetricSummary",
    "ModelEntry",
    "ModelKind",
    "ModelRef",
    "Role",
    "RunnerClass",
    "RunnerEnv",
    "Span",
    "SpanExtractor",
    "TextGenerator",
    "TrainingRecipe",
    "detect_runner",
    "eligible_bases",
    "extraction_baselines",
    "get_entry",
    "read_manifest",
    "summarize_metric",
    "validate_registry",
    "write_manifest",
]
