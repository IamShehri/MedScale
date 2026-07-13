# MedScale v0.2 Final Release Audit

Stability: public release artifact.
Date: 2026-07-13
Auditor: Hermes / manual evidence review + local verification

## 1. Executive Summary

MedScale v0.2 is **internally consistent** and **reproducible by construction**. All core quality gates pass on the current tree:

- `uv run ruff check .` PASS
- `uv run mypy src tests` PASS
- `uv run pytest -q --no-header` PASS (340 passed, 2 skipped)

The codebase is small, deterministic, and dependency-bounded. Architecture boundaries are enforced by build-failing tests. The evidence corpus, dataset artifacts, benchmark contracts, FHIR boundary, and reviewer collaboration layer are all local-only and content-addressed where appropriate.

The repo is **not yet ready for `v0.2.0` tagging** without about a dozen minor documentation, tracker, and release-workflow fixes. None of these are architectural redesigns. They are release-readiness hygiene items that should be resolved in the tag candidate, not in v0.3.

**Recommendation: GO WITH MINOR FIXES**

---

## 2. Milestone Completion Status

| Milestone | Implementation | Tests | Docs | Status |
|---|---|---|---|---|
| M1 Release Engineering | ✅ | ✅ | ✅ | Complete |
| M2 Evidence Infrastructure | ✅ | ✅ | ✅ | Complete |
| M3 Benchmark Framework | ✅ | ✅ | ✅ | Complete |
| Dataset v1 + S0 | ✅ | ✅ | ✅ | Complete |
| M4 Optional Modelkit Backends | ✅ | ✅ | ✅ | Complete |
| M5 FHIR Boundary | ✅ | ✅ | ✅ | Complete |
| M6 Collaboration Workflow | ✅ | ✅ | ✅ | Complete |

Total test count: **340 passed**, **2 skipped** (pre-existing optional-extras skips when `transformers` is installed; `llama-cpp` runtime absent, tests skip gracefully).

Verified commands:
```bash
uv run ruff check .
uv run mypy src tests
uv run pytest -q --no-header
uv run pytest tests/test_architecture.py -q --no-header
```

---

## 3. ADR Status

| ADR | Document | Implementation | Tests | Docs | Verdict |
|---|---|---|---|---|---|
| ADR-0023 Structured Logging | Missing | Partial / implicit | Partial | Partial | Gap |
| ADR-0024 Release Automation | Missing | Partial | Partial | Partial | Gap |
| ADR-0025 Coverage Policy | Missing | Partial | Partial | Partial | Gap |
| ADR-0026 Collaboration Model | Missing | Implemented | 9 tests | M6 README | Implemented but undocumented |
| ADR-0027 Optional Extras | Missing | Implemented | Covered | M4 README | Implemented but undocumented |
| ADR-0028 FHIR Boundary | Missing | Implemented | 13 tests | M5 README | Implemented but undocumented |
| ADR-0029 Benchmark Determinism | ✅ | ✅ | ✅ | M3 README | Implemented |
| ADR-0030 Dataset Versioning | ✅ | ✅ | ✅ | dataset_v1.md | Implemented |

### Gap details

**ADR-0023 — Structured Logging**
- No `docs/adr/0023-*.md`.
- No structured logging framework in `src/medscale`; CLI uses `print` statements.
- Current state: logging is human-readable only; no JSON/structured events.

**ADR-0024 — Release Automation**
- No `docs/adr/0024-*.md`.
- Release process is documented in `docs/releases/release_process.md` and `docs/releases/ci_cd.md`, but no GitHub Actions release workflow exists under `.github/workflows/`.
- No `release-package.yml`, no tag-triggered GitHub Release automation, no PyPI trusted-publishing workflow.

**ADR-0025 — Coverage Policy**
- No `docs/adr/0025-*.md`.
- `pytest --cov` is available in CI, but no minimum coverage threshold is enforced in `pyproject.toml` or CI.
- `docs/execution/v0.2/release_readiness.md` explicitly lists coverage ≥90% as open.

**ADR-0026/0027/0028**
- Implementations and tests exist.
- Formal ADR documents are absent. The `docs/execution/v0.2/adr_implementation_tracker.md` currently marks them as "planned" or omits them from the registry.
- This is a documentation debt item, not a missing feature.

### Governance rule applied
Per task constraints: do not redesign ADR structure, do not invent ADR content. The gaps are recorded above; no placeholder ADRs were written.

---

## 4. Architecture Findings

### 4.1 Layer ordering

Current enforced layers from `tests/test_architecture.py`:

| Layer | Modules |
|---|---|
| 0 — spine | `__about__`, `_layout`, `_runtime`, `reproducibility`, `provenance` |
| 1 — knowledge | `litdb` |
| 2 — evidence/capability | `evidence`, `evidence_store`, `evidence_checks`, `extraction`, `modelkit`, `backends`, `fhirkit`, `collaboration` |
| 3 — research/artifact | `research`, `dataset` |
| 4 — benchmark | `bench` |
| 5 — facade | `workspace` |
| 6 — transport | `cli` |

Adjacency check: `cli` (6) imports `fhirkit` (2). Same-layer imports are allowed only within spine (0) and evidence cluster (2). `cli -> fhirkit` is a downward edge and is allowed.

### 4.2 Forbidden dependency check

| Forbidden edge | Present? | Status |
|---|---|---|
| `dataset -> research` | No | ✅ |
| `evidence -> litdb` | No (evidence package only; `extraction` is outside `evidence/`) | ⚠️ Not enforced by automation (see A-1 below) |
| `bench -> optional backends` | No | ✅ |
| `fhirkit -> cli` | No | ✅ |
| `backends -> cli/research/dataset/fhirkit` | No | ✅ |
| engine -> cli` | No | ✅ |
| `collaboration -> dataset/research/backends/fhirkit` | No | ✅ |

### 4.3 Open findings

| ID | Severity | Finding |
|---|---|---|
| A-1 | Medium | `src/medscale/extraction.py` sits outside `src/medscale/evidence/`; the architecture test’s evidence-purity rule only scans `src/medscale/evidence/*.py`, so an `extraction -> litdb` edge is not enforced by automation. Documented in `architecture_audit.md`. No code change required; no automated regression possible without moving files or widening the rule. |
| A-2 | Low | `src/medscale/workspace.py` exports `Snapshot = ResearchSnapshot` without declaring it in `workspace.py`’s `__all__`. Documented as TD-001 in `technical_debt.md`. |
| A-3 | Low | Network code (`urllib`) is confined to `src/medscale/litdb/adapters.py`; core paths never contact the network. Acceptable isolation. |

---

## 5. Reproducibility Findings

### 5.1 Benchmark

- `BenchmarkSpec.spec_id` is a content hash of spec metadata.
- Run artifacts record 5 frozen identities: `spec_id`, `snapshot_id`, `software_version`, `git_sha`, `scorer_version`.
- Replay reads those identities and fails loudly on any mismatch.
- CI includes `medscale bench validate` via `medscale check`.
- Test coverage: `tests/test_bench_replay.py` covers artifact missing + malformed JSON paths. The replay mismatch logic itself is exercised indirectly through `tests/test_bench_engine.py` and `tests/test_bench_tasks.py`.
- Verdict: **reproducible**, with minor test-coverage depth gap.

### 5.2 Dataset

- Deterministic splits using content-hash primitive with fixed seed 42.
- Sibling `.sha256` checksums for every artifact.
- Schema versioned (`schema.json` says `version: 1`).
- No uncontrolled random splitting, no hidden timestamps in split assignment.
- Freeze policy enforced by `validate.py`; rejects mismatched hashes, missing metadata, path traversal.
- Verdict: **reproducible and immutable after freeze**.

### 5.3 Collaboration

- Append-only JSONL reviewer logs with previous-event hash chain.
- Deterministic merge by lexicographic timestamp ordering.
- Merge manifest includes source hashes, conflict list, counts, and manifest hash.
- Conflicts are surfaced, never auto-resolved.
- Verdict: **reproducible and auditable**.

### 5.4 FHIR

- `ValidationReport` is a frozen dataclass with deterministic `canonical_json` serialization.
- Storage is content-addressed by `report_hash(report)`.
- Validator execution is optional and local; missing validator returns `UnavailableValidatorError` with install guidance.
- No network dependency; no hidden timestamps in deterministic paths.
- Verdict: **deterministic and local-only**.

### 5.5 Cross-cutting

- `canonical_json`, `content_hash`, and `set_global_seed` are available from the spine and reused by all artifact-producing modules.
- `_layout` centralizes all path constants; no hardcoded layout strings in engine code (enforced by `test_storage_layout_lives_in_exactly_one_module`).
- `_runtime` centralizes `utc_now()` and `git_sha()`; the adapter layer still calls `datetime.now(UTC)` directly for transport metadata, which is acceptable.

---

## 6. CI Status

### 6.1 Workflows present

| Workflow | Purpose |
|---|---|
| `.github/workflows/ci.yml` | Quality gate: ruff, mypy, pytest, litdb integrity |
| `.github/workflows/optional-extras.yml` | Isolated backends testing: transformers, llama.cpp, core-only import safety |
| `.github/workflows/codeql.yml` | Security scanning |

### 6.2 Missing workflows

| Expected workflow | Status |
|---|---|
| Tag-only release workflow | Missing |
| PyPI trusted-publishing workflow | Missing |
| Coverage threshold enforcement | Missing from CI config |

### 6.3 CI isolation verification

- `optional-extras.yml` runs backends tests only when backends files change, on their own jobs, with explicit extra install.
- `core-without-backends` job verifies `import medscale.backends` succeeds on core-only install.
- No automatic publish is configured.
- Tag-only release is *documented* in `docs/releases/ci_cd.md` but not yet implemented in workflow YAML.

### 6.4 Observed CI gap

The `ci.yml` matrix uses `uv sync --frozen`, which requires `uv.lock` to be present and up to date. The lockfile exists and CI passes locally. No evidence of lockfile staleness in recent commits.

---

## 7. Documentation Status

### 7.1 v0.2 execution docs present

| Document | Status |
|---|---|
| `docs/execution/v0.2/adr_implementation_tracker.md` | Outdated: ADR-0026 marked "planned"; ADR-0027/0028/0023/0024/0025 absent |
| `docs/execution/v0.2/architecture_audit.md` | Current; M4-era but still valid |
| `docs/execution/v0.2/dataset_v1.md` | Aligned with ADR-0030 |
| `docs/execution/v0.2/M2-evidence-infrastructure.md` | Current |
| `docs/execution/v0.2/M3-README.md` | Current |
| `docs/execution/v0.2/M4-README.md` | Current |
| `docs/execution/v0.2/M5-README.md` | Current |
| `docs/execution/v0.2/M6-README.md` | Current |
| `docs/execution/v0.2/milestone_tracker.md` | Outdated: M6 marked "in progress" |
| `docs/execution/v0.2/release_readiness.md` | Mixed state; many checkboxes still open |
| `docs/execution/v0.2/technical_debt.md` | Current; TD-001 through TD-004 |

### 7.2 Top-level docs

| Document | Status |
|---|---|
| `README.md` | Outdated: status badge says "Foundation (T0)"; M4/M5/M6 not reflected |
| `RELEASES.md` | Outdated: only v0.1.0 recorded |
| `CHANGELOG.md` | Outdated: `[Unreleased]` section is empty; no v0.2 entries |
| `CITATION.cff` | Outdated: version `0.1.0`, date `2026-07-10` |
| `src/medscale/__about__.py` | Outdated: `__version__ = "0.1.0"` |
| `ROADMAP.md` | Not inspected in detail for v0.2 accuracy |

### 7.3 Archive state

`docs/archive/DATASET_V1_PLAN.superseded.md` exists; source-of-truth attribution is preserved.

---

## 8. Release Blockers

### 8.1 Hard blockers (must fix before tagging v0.2.0)

| # | Blocker | Evidence |
|---|---|---|
| R-1 | `__about__.py` version is `0.1.0` | `src/medscale/__about__.py:1` |
| R-2 | `CITATION.cff` version/date still v0.1.0 | `CITATION.cff` |
| R-3 | `RELEASES.md` has no v0.2.0 section | `RELEASES.md` |
| R-4 | Milestone tracker marks M6 "in progress" | `docs/execution/v0.2/milestone_tracker.md` |
| R-5 | ADR tracker does not list ADR-0026/0027/0028 as implemented | `docs/execution/v0.2/adr_implementation_tracker.md` |
| R-6 | No release workflow YAML exists | `.github/workflows/` listing |

### 8.2 Minor fixes (GO WITH MINOR FIXES window)

| # | Gap | Evidence |
|---|---|---|
| R-7 | `README.md` status badge says T0 / Foundation, not v0.2 final | `README.md` |
| R-8 | `CHANGELOG.md` `[Unreleased]` is empty | `CHANGELOG.md` |
| R-9 | `release_readiness.md` has unchecked items that are now satisfied | `docs/execution/v0.2/release_readiness.md` |
| R-10 | ADR-0023/0024/0025 formal registry entries absent | `docs/adr/` listing |
| R-11 | No explicit coverage threshold in `pyproject.toml` or CI | `pyproject.toml`, `.github/workflows/ci.yml` |

---

## 9. Recommendation

### GO WITH MINOR FIXES

MedScale v0.2 satisfies the core mission: it is deterministic, architecture-bounded, tested, and documented at the implementation level. The six hard blockers are all release-hygiene items (version strings, release workflow, tracker state), not defects or redesigns.

**Path to GO:**

1. **Version/tracker sync** — bump `__about__.py`, `CITATION.cff`, `RELEASES.md`, `CHANGELOG.md`; update `milestone_tracker.md` and `adr_implementation_tracker.md`.
2. **Release workflow** — add a minimal tag-only release workflow (`.github/workflows/release.yml`) that triggers on `v*` tags, runs quality gates, builds wheel+sdists, and creates a GitHub Release without automatic publish. This aligns `docs/releases/ci_cd.md` with reality.
3. **ADR registry pass** — add or align tracker entries for ADR-0026/0027/0028 as implemented; document 0023/0024/0025 as post-v0.2 technical-debt items rather than leaving them as silent absences.
4. **Readme/status pass** — update status badge and high-level README so it reflects v0.2 final, not T0.
5. **Coverage threshold** — add `fail_under` to `pytest-cov` config in `pyproject.toml` or CI; even 80% would close R-11.
6. **Release checklist** — execute `docs/execution/v0.2/RELEASE_CHECKLIST.md` and record evidence for each item.

No code changes are required. No new features. No architecture changes. No v0.3 work.

After these fixes, re-run the three canonical verification commands, cut the tag, and publish the GitHub Release.
