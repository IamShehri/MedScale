# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Python workspace (T0):** `medscale` package (src-layout), `pyproject.toml`
  (uv/hatchling), reproducibility primitives (`canonical_json`, `content_hash`,
  `set_global_seed`), and a deterministic test suite.
- **Quality gate:** Ruff (lint + format), Mypy (strict), Pytest + coverage; GitHub
  Actions CI on Python 3.11 and 3.12; pre-commit hooks; CodeQL; Dependabot.
- **Community & governance docs:** `README`, `LICENSE` (Apache-2.0), `CONTRIBUTING`,
  `CODE_OF_CONDUCT`, `SECURITY`, `CITATION.cff`, `ROADMAP`, this changelog.
- **Governance:** canonical program rules `docs/governance/rules.md` (R1–R7); ADR
  template (`0000`); `0004-t0-foundation-scope` (single-package decision); documentation
  index, research index, glossary, and developer guide.
- **Repository hygiene:** `.gitattributes` (LF normalization), `.editorconfig`, expanded
  `.gitignore`; issue/PR templates.

### Changed

- ADR-0003 marked **Accepted** with a post-consolidation note.

### Added (architecture — hybrid layering, model registry, deep OpenMed study — 2026-07-10)

- **ADR-0012 Accepted (hybrid architecture)**: non-negotiable Verification &
  Reproducibility **Spine** (cross-cutting) + **seven capability layers** (Knowledge,
  Evidence, AI, Interoperability, Research, Developer, Application). Verification is never
  a peer layer — it is MedScale's defining identity. Operator-refined from the original
  proposal (layered model retained; Knowledge/Evidence kept as distinct layers; ADR-0005
  pillars retained as the cross-layer mission grouping).
- **`docs/models/`**: canonical **model registry** (two axes — licence tier × role;
  ecosystem position map; verified entries: BioMistral Apache-2.0, MedGemma HAI-DEF,
  Bio_ClinicalBERT MIT, PubMedBERT MIT, OpenMed Apache-2.0; MIMIC-III provenance noted)
  and the **model card schema** (`schemas/model_card_schema.md`, machine-checkable, for
  future card-lint CI). `medscale.registry` is *designed* and deferred to Horizon 2 — no
  package created (ADR-0012). Registry moved out of `ai_model_strategy.md` (dedupe).
- **Deep OpenMed study** (`openmed_capability_analysis.md` expanded): capability map +
  architecture lessons + reusable principles + integration opportunities + things to
  avoid, grounded in OpenMed's verified developer surface. Principles absorbed
  (local-first, no runtime phone-home, task-first discoverability, composition over
  pipelines); product not copied.

### Added (release infrastructure design — 2026-07-10)

- **`docs/releases/`** (12 documents): complete publication & artifact lifecycle —
  lifecycle states with immutable releases and visible retraction; per-class versioning
  (SemVer package, no-PATCH `vX.Y` for models/datasets/benchmarks, append-only integer
  schemas); release process with ten checklists (package, HF model/dataset/Space,
  benchmark, paper, updates, deprecation, retraction); GitHub→CI→Releases→HF
  distribution with CI-only publishing; per-artifact licensing matrix (field-level for
  composite datasets); model/dataset card requirements with mandatory verbatim safety
  statements; benchmark publication + leaderboard policy; paper→replication-package
  workflow; release manifest spec; future GitHub Actions design. Documentation only —
  nothing implemented, nothing uploaded.
- **Proposed ADRs 0010** (release architecture; MESC naming — "MedScale-Base" is a
  config reference, never trained base weights) **and 0011** (versioning schemes +
  licensing matrix; closes the long-pending licence ADR debt). Awaiting operator
  approval; not self-ratified.

### Added (T1 ingestion foundation — 2026-07-10)

- **`medscale.litdb` ingestion machinery**: frozen v1 query set as code (Q1–Q10),
  four source adapters (Semantic Scholar, OpenAlex, PubMed, arXiv) behind an injectable
  HTTP layer (CI offline; 404 recorded as NOT_FOUND; 429/transport failures abort
  honestly), verbatim raw archival with SHA-256, byte-stable run manifests, and the
  append-only PRISMA screening log (replay-validated).
- **`data/litdb/` scaffolding** with R3 `LICENSE.md` (per-source terms, verified
  2026-07-10) committed before the first archived byte.
- **Pilot ingestion round 0** (Q2 × 4 sources, cap 3): OpenAlex, arXiv, PubMed archived
  with manifest; Semantic Scholar rate-limited (HTTP 429) after backoff — skipped and
  recorded; full round 1 needs an S2 API key or longer backoff.
- **`docs/architecture/distribution_hf.md`**: Hugging Face (`MedScale` /
  org `MedScaleAI`) recognized as the future distribution layer with publishing gates;
  nothing published before its gate. 22 new offline tests (68 total).

### Added (T1 foundation — 2026-07-10)

- **ADRs 0005–0008 Accepted** with operator refinements (identity: "Open Research
  Intelligence Infrastructure for Medicine"; no hard model dependencies; OpenMed
  boundaries kept ready for future clinical/privacy capabilities; FHIR supports, not
  defines). **ADR-0009 (Evidence Model) Accepted**: evidence objects, verification state
  machine, provenance datatype, deterministic study-design grading.
- **`medscale.provenance`** — Rule R1 as a datatype (SourceAPI, Provenance, NOT_FOUND).
- **`medscale.evidence`** — EvidenceObject with content-derived ids, PICO slots, the
  verification state machine, and the model-cannot-self-verify guard.
- **`medscale.litdb`** — LiteratureRecord (R1 identifier requirement,
  dedupe-by-construction record ids), PRISMA screening state machine (mandatory
  exclusion reasons), SourceAdapter protocol + RawRetrieval envelope (no network code).
- **`docs/execution/search_strategy.md`** — frozen-by-commit query set, PRISMA
  workflow, raw-response archival policy. 38 new deterministic tests (46 total).

### Added (architecture analysis — 2026-07-10)

- **`docs/architecture/`**: evidence-based ecosystem analysis (OpenMed, MedGemma,
  BioMistral, FHIR/EHR-FM, openEHR bridge, OpenEvidence/Medwise), reference architecture
  (adds the verification & reproducibility spine omitted from the proposed 4-layer
  model), AI model strategy, OpenMed integration strategy, interoperability strategy.
- **Proposed ADRs 0005–0008** (awaiting operator approval): research-intelligence scope
  amendment; licence-first two-tier model registry; OpenMed as optional evaluation-time
  adapter; FHIR as single canonical representation with boundary adapters.

## [0.0.0] — 2026-07-09

### Added

- Initial documentation foundation: Strategic Blueprint, Research Vision, research
  questions, paper taxonomy, reproducibility policy, ADR-0003, and archive of the
  superseded working draft. Repository consolidated into a single canonical git repo.
