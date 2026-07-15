# ALIGN-16 — Research Evidence

## Methodology

Inspection proceeded file-by-file from the canonical repository state and from the
exact commands requested by the audit charter. No production, test, workflow,
dependency, export, or facade code was changed. All inferred conclusions are grounded
in the inspected source, tests, packaging metadata, workflow definitions, or accepted
ADRs.

The audit distinguishes:

* **canonical evidence** — files present on `origin/main` at baseline
  `3132de8789badead5a6f554a71dbaea559fe2233`;
* **candidate future contracts** — clearly labeled concepts that are planned,
  referenced in ADRs, or assumed in architecture documents but not yet implemented;
* **nonexistent concepts** — explicitly recorded with `Does not exist on canonical main.`
  to avoid placeholder assumptions.

## Inspected production files

### Core orchestration surfaces

- `src/medscale/__init__.py`
- `src/medscale/_runtime.py`
- `src/medscale/workspace.py`

Findings:
- `_runtime.py` and `workspace.py` are internal orchestration.
- `medscale.__init__.__all__` exports only spine/core objects: `Benchmark`, `Corpus`,
  `Evidence`, `EvidenceQueryResult`, `RecordQueryResult`, `Snapshot`, `VerificationEngine`,
  `Workspace`, `__version__`, `canonical_json`, `content_hash`, `set_global_seed`.
- `workspace.__all__` does not expose `medscale.modelkit` or `medscale.backends`
  symbols.
- `Benchmark.run(...)` accepts `EvidenceSystem`; its parameter type is evaluation-facing,
  not model-execution-facing.

### Modelkit package

- `src/medscale/modelkit/__init__.py`
- `src/medscale/modelkit/interfaces.py`
- `src/medscale/modelkit/manifests.py`
- `src/medscale/modelkit/recipes.py`
- `src/medscale/modelkit/registry.py`
- `src/medscale/modelkit/reporting.py`

Findings:
- `modelkit.__init__.py` exports a wider surface than its docstring describes.
- The docstring states only `TextGenerator`, `SpanExtractor`, and `ModelRef` are
  public-frozen protocols and says everything else is internal, but `__all__` includes
  registry, manifest, recipe, runner, reporting, and helper symbols.
- This mismatch is classified as:
  `D. a mixed surface requiring symbol-by-symbol classification`.
- No change to `__all__` was made.
- Two optional backend adapters currently implement the `TextGenerator` protocol shape as
  deterministic contract-test adapters:
  * `TransformersTextGenerator`
  * `LlamaCppTextGenerator`
- They return synthetic `GenerationResult` values and do not load model weights or perform
  real Transformers or llama.cpp inference.
- `recipes` and `manifests` are dependency-free schema/helpers modules; they do not
  import ML frameworks.

### Backend package

- `src/medscale/backends/__init__.py`
- `src/medscale/backends/common.py`
- `src/medscale/backends/transformers/__init__.py`
- `src/medscale/backends/transformers/backend.py`
- `src/medscale/backends/transformers/validation.py`
- `src/medscale/backends/llamacpp/__init__.py`
- `src/medscale/backends/llamacpp/backend.py`
- `src/medscale/backends/llamacpp/validation.py`

Findings:
- Backends import safely from core because:
  * `backends.__init__` only re-exports contracts from `common`;
  * backend subpackage `__init__` files do not unconditionally import optional ML deps;
  * constructors and validators raise explicit `BackendMissingDependencyError`.
- Optional extras are:
  * `backends-transformers`
  * `backends-llamacpp`
- No aggregate `backends` extra exists.
- `backends-llamacpp` is gated with `sys_platform != 'win32'`, so `pip install medscale[backends-llamacpp]`
  silently installs nothing on Windows.

### Bench / evaluation surface

- `src/medscale/bench/scorers.py`
- `src/medscale/bench/run.py`
- `src/medscale/bench/spec.py`
- `src/medscale/litdb/triage_eval.py`

Findings:
- `bench.scorers` owns deterministic benchmark metrics; it makes no ML/embedding/LLM
  assumptions.
- `Benchmark.run(...)` still accepts only `EvidenceSystem`; no `TextGenerator`,
  `SpanExtractor`, or `ModelRef` acceptance path exists on benchmark task output.
- `BenchmarkRunArtifact` is the ALIGN-15 canonical evaluation output surface.
- `modelkit.reporting` vs `bench.scorers` ownership is unresolved.

### Lineage module (literature database)

- `src/medscale/litdb/lineage.py`
- `tests/test_litdb_lineage.py`

Findings:
- `litdb.lineage` is literature-record merge lineage; it is not a model lineage module.
- No model adoption, promotion, training, checkpoint, adapter, deployment, or
  infrastructure lineage concepts are present.

## Inspected tests

- `tests/test_modelkit_backends.py`
- `tests/test_modelkit_interfaces.py`
- `tests/test_modelkit_manifests.py`
- `tests/test_modelkit_recipes.py`
- `tests/test_modelkit_registry.py`
- `tests/test_modelkit_reporting.py`
- `tests/test_litdb_lineage.py`

Findings:
- `tests/test_modelkit_backends.py` uses the correct path `tests/test_modelkit_backends.py`.
- Backend tests validate:
  * core/package import safety;
  * actionable missing-dependency errors with install hints;
  * backend module boundaries (`cli`, `research`, `dataset` are not imported);
  * deterministic contract adapters without real inference or model downloads.
- `tests/test_modelkit_manifests.py` validates canonical-JSON/LF round-trip, no-RQ guard,
  dirty-tree guard, JSON config validation, seeds validation, and injectable runner detection.
- `tests/test_modelkit_recipes.py` validates deterministic `recipe_id`, QLoRA base-quantization
  requirement, and hyperparameter validation.
- `tests/test_modelkit_registry.py` validates Tier-1 generative BASE_CANDIDATE invariants,
  duplicate-ID guard, entry lookup, and extraction-baseline type enforcement.
- `tests/test_modelkit_reporting.py` reports deterministic arithmetic for mean ± 95% CI.
- `tests/test_litdb_lineage.py` covers literature-record merge lineage only.

## Packaging and optional extras

File inspected: `pyproject.toml`

Findings:
- Core `dependencies = []`.
- Optional extras:
  * `backends-transformers = ["transformers>=4.44"]`
  * `backends-llamacpp = ["llama-cpp-python>=0.3.21; sys_platform != 'win32'"]`
- No aggregate `backends` extra exists.
- Backend subpackage files are included in the `src/medscale` wheel.
- Version ranges are bounded but loose; reproducibility depends on the lockfile.
- llama.cpp installation risk is platform-dependent; Windows is explicitly excluded by
  packaging metadata.
- These states mean:
  * `Installed dependency` ≠ `Packaged module` ≠ `Available backend` ≠ `Loaded model`
    ≠ `Executed inference`.

## Workflow evidence

File inspected: `.github/workflows/optional-extras.yml`

Findings:
- Trigger events: push to `main`; PR changes under `src/medscale/backends/**`,
  `pyproject.toml`, or `tests/test_modelkit_backends.py`.
- Jobs:
  * `backends-transformers`: installs `medscale[backends-transformers]` and runs
    `tests/test_modelkit_backends.py -q --no-header`.
  * `backends-llamacpp`: installs `medscale[backends-llamacpp]` and runs
    `tests/test_modelkit_backends.py -k 'llamacpp or llamacpp_skip' -q --no-header`.
  * `core-without-backends`: installs core only and runs `import medscale.backends`,
    ruff, and mypy.
- No workflow step downloads model weights.
- No workflow step performs real inference.
- CI proves:
  * core import safety,
  * optional-dependency installation,
  * backend contract/shape tests.

Classification:

```text
Core compatibility evidence
Optional-dependency installation evidence
Backend protocol/contract evidence
Not real inference evidence
```

## Optional extras behavior

- `backends-transformers`:
  * installing makes `transformers` available;
  * tests still exercise contract adapters, not real model inference.
- `backends-llamacpp`:
  * installing makes `llama-cpp-python` available on non-Windows;
  * tests still exercise contract adapters.
- Core-only install:
  * `import medscale.backends` succeeds;
  * backend subpackages prevent optional dependency import until constructors are invoked.

## ADR authority documents inspected

- `docs/adr/0006-model-access-strategy.md`
- `docs/adr/0015-model-agnostic-platform.md`
- `docs/adr/0020-public-api-stability.md`
- `docs/models/model_registry.md`
- `docs/architecture/model_agnostic_platform.md`
- `docs/architecture/ai_model_strategy.md`

Key evidence:
- ADR-0015 accepts `TextGenerator`, `SpanExtractor`, `ModelRef`, manifest/recipe/reporting
  module existence, and optional-backend isolation.
- ADR-0015 explicitly gates inference backends at T4 and training execution at T5;
  model downloads are not in scope.
- ADR-0020 public-frozen list includes `TextGenerator`, `SpanExtractor`, `ModelRef`,
  benchmark output types, and spine primitives; the wider `modelkit.__all__` is not
  explicitly listed.
- ADR-0006 governs licence tiers and registry structure as documentation/code twin;
  it does not authorize promotion or mutable runtime registry semantics.
- The first real backend may force contract revision per accepted ADR language.

## Risks and gaps

- Wider `modelkit.__all__` public surface is unexplained by accepted ADRs.
- Reporting ownership overlaps `bench.scorers` and future `BenchmarkRunArtifact` fields.
- No accepted ADR governs promotion, lineage, training execution, checkpoint identity,
  adapter artifact semantics, deployment, or infrastructure contract boundaries.
- Zero model-lineage, promotion, training-run, checkpoint, adapter-artifact,
  deployment-record, or infrastructure-spec contracts exist on canonical main.
