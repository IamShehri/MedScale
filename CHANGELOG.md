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
