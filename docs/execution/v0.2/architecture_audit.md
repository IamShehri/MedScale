# MedScale v0.2 — Architecture Audit

Stability: public process document.
Scope: repository state after M1/M2/M3/Dataset v1, before M4.
Basis: `uv run ruff/mypy/pytest` green, `tests/test_architecture.py` green.

## 1. Current Package Architecture

### 1.1 Layer map

| Layer | Package / module | Responsibility | Public / internal | Dependencies |
|-------|------------------|----------------|-------------------|--------------|
| 0 — spine | `medscale.__about__` | version constant | internal | none |
| 0 — spine | `medscale._layout` | storage path constants | internal | none |
| 0 — spine | `medscale._runtime` | runtime helpers | internal | none |
| 0 — spine | `medscale.reproducibility` | canonical JSON, content hash, seeding | public spine | none |
| 0 — spine | `medscale.provenance` | provenance types + timestamp validation | public spine | none |
| 1 — knowledge | `medscale.litdb` | corpus, review, screening, sources, store, integrity | public domain | spine |
| 2 — evidence | `medscale.evidence` | claim/evidence model objects | public domain | spine, provenance |
| 2 — evidence | `medscale.evidence_checks` | deterministic verification checks | internal | evidence, spine |
| 2 — evidence | `medscale.evidence_store` | evidence persistence + loaders | internal | evidence, spine |
| 2 — evidence | `medscale.extraction` | record → evidence assembly helpers | internal | evidence, litdb |
| 2 — capability | `medscale.modelkit` | backend interfaces, manifests, recipes, registry | public capability | spine |
| 3 — research | `medscale.research` | index, query, snapshot, stats | public capability | evidence, evidence_store, litdb, spine |
| 3 — artifact | `medscale.dataset` | dataset manifest/schema/split/validate/snapshot | public artifact | spine |
| 4 — benchmark | `medscale.bench` | spec, tasks, scoring, replay, validation | public capability | evidence, evidence_store, modelkit, research, spine |
| 5 — facade | `medscale.workspace` | stable public contract: Workspace, Corpus, Evidence, Benchmark | public frozen | bench, evidence, evidence_checks, litdb, research, spine |
| 6 — transport | `medscale.cli` | argv dispatcher + subcommands | public transport | all public packages |

### 1.2 Ownership boundaries

- `dataset` owns all deterministic dataset artifact rules; no other package may write dataset-specific validation logic.
- `bench` owns benchmark spec/task/scoring/replay rules; `research` provides read-only index/snapshot support.
- `workspace` is the only package allowed to re-export facade objects at the package root.
- `cli` is thin dispatch; it must not own business logic.

## 2. Dependency Direction Review

### 2.1 Observed real edges against policy

Allowed edges observed:
- `dataset -> reproducibility` ✓
- `bench -> dataset` via optional CLI/usage docs, not hard package dependency in `src/` ✓
- `bench -> evidence` ✓
- `bench -> modelkit` ✓
- `CLI -> public packages` ✓

Forbidden edges checked:
- `dataset -> research`: no import edge found ✓
- `dataset -> training`: no training package exists in `src/` ✓
- `bench -> optional backends`: `bench` depends on `modelkit` only; no transformers/llama.cpp/HF imports found ✓
- `evidence -> litdb`: `medscale/evidence/` package does not import `litdb`; the separately hosted `medscale.extraction` module does, but it is not inside the `evidence/` package and was deliberately extracted from `litdb` in a prior refactor ✓
- `core -> CLI`: no core package imports `cli` ✓

### 2.2 Layer-direction summary

Current layer ordering matches the intended foundation → domain → capability → interface flow:
`spine(0) -> knowledge(1) -> evidence(2) -> research(3)/dataset(3) -> bench(4) -> workspace(5) -> cli(6)`

One same-layer allowance exists:
- `evidence` cluster split across `evidence`, `evidence_store`, `evidence_checks`, `extraction` is treated as one conceptual layer by `tests/test_architecture.py`.

## 3. Import Graph Audit

### 3.1 Circular imports

No circular imports detected in the current tree.

### 3.2 Lazy imports

No lazy-import workarounds found. The package uses straightforward top-level imports.

### 3.3 Unnecessary coupling

Notable couplings:
- `workspace.py` imports broad subpackages (`bench`, `evidence`, `evidence_checks`, `litdb`, `research`). This is by design for the facade, but limits future decomposition unless the facade remains as-is through M4.
- `bench/baselines.py` imports `research.index`. Review systems need the joined index; keeping this is acceptable.
- `evidence_store.py` imports `evidence` to reuse `EvidenceObject`. This is acceptable because `evidence_store` is classified as layer 2 same-cluster.

### 3.4 Boundary crossings

The existing `tests/test_architecture.py` enforces:
- no package-root imports from inside `src/`
- downward-only dependency flow
- transport isolation (`cli` only)
- facade isolation (`workspace` only at root)
- evidence-layer purity for files under `src/medscale/evidence/`

Gap:
- `src/medscale/extraction.py` sits in the evidence cluster but is outside `src/medscale/evidence/`; the architecture test’s evidence-purity rule only scans `src/medscale/evidence/*.py`, so an `extraction -> litdb` edge is not currently enforced by automation.

Decision: document the gap; the module was deliberately carved out of `litdb` to fix an earlier inversion, so no code change is warranted before M4.

## 4. ADR Alignment Review

| ADR | Title | Status in repo | Evidence | Notes |
|------|-------|----------------|----------|-------|
| ADR-0023 | Structured Logging | Missing | Future | No `docs/adr/0023-*.md` present. |
| ADR-0024 | Release Automation | Missing | Future | No `docs/adr/0024-*.md` present. |
| ADR-0025 | Coverage Policy | Missing | Future | No `docs/adr/0025-*.md` present. `pyproject.toml` enables pytest-cov in dev, but no enforced minimum gate. |
| ADR-0026 | Collaboration Model | Missing | Future | No `docs/adr/0026-*.md` present. |
| ADR-0027 | Optional Extras | Missing | Future | No `docs/adr/0027-*.md` present. `pyproject.toml` has no optional extras sections. |
| ADR-0028 | FHIR Boundary | Missing | Future | No `docs/adr/0028-*.md` present. No FHIR code exists in `src/`; boundary is currently implicit. |
| ADR-0029 | Benchmark Determinism and Replay Contract | Accepted | Implemented | `bench/spec.py`, `bench/validate.py`, `bench/run.py`, `bench/replay` CLI, M3 READM all encode frozen identities and artifact-first replay. |
| ADR-0030 | Dataset Versioning and Training-Artifact Contract | Accepted | Implemented | `dataset/manifest.py`, `dataset/validate.py`, `dataset/snapshot.py`, `cli/dataset.py`, and sibling `.sha256` policy implemented. |

Finding: ADR coverage for 0023–0028 is absent. For stabilization, record them as documentation debt and create placeholders in M4 or an ADR-epic pass if governance requires a complete registry before release.

## 5. Public API Review

### 5.1 Root exports (`src/medscale/__init__.py`)

Stable public objects:
- `Workspace`, `Corpus`, `Evidence`, `Benchmark`, `Snapshot`, `VerificationEngine`
- `RecordQueryResult`, `EvidenceQueryResult`
- `canonical_json`, `content_hash`, `set_global_seed`
- `__version__`

Observations:
- `Snapshot` is a module-level alias for `ResearchSnapshot` in `workspace.py`. It is stable, but the alias is not declared via `__all__` in `workspace.py`, which reduces visibility during audits. This is recorded as TD-001.

### 5.2 Accidental / unstable exports

No obviously accidental exports were found. `cli` modules are not re-exported at the root. `dataset` public exports are limited to manifest/schema/split/validate functions, matching the approved contract.

### 5.3 Candidates for freeze

- `medscale.workspace` facade objects should be treated as frozen once M4 begins.
- Dataset exports are already marked public-frozen in file-level docstrings.

## 6. Findings summary

| ID | Severity | Finding |
|----|----------|---------|
| A-1 | Medium | `extraction.py` evidence-purity edge is not covered by `test_architecture.py` due to file location outside `evidence/` package. |
| A-2 | Medium | `Snapshot = ResearchSnapshot` alias is not in `workspace.py` `__all__`. |
| A-3 | Low | `workspace.py` is a wide facade import; safe for M4 launch, but a future decomposition target. |
| A-4 | High | ADR registry is incomplete: ADR-0023 through ADR-0028 are missing. |

## 7. Recommendations for M4

- Keep the facade stable through at least M4.
- Do not introduce training-scope imports into `dataset` without a new ADR.
- Add ADR stubs for 0023–0028 only if governance mandates a complete registry before release.
- Preserve the existing `test_architecture.py` layer contract; any new module must be classified before import.
