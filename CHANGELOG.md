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

## [0.0.0] — 2026-07-09

### Added

- Initial documentation foundation: Strategic Blueprint, Research Vision, research
  questions, paper taxonomy, reproducibility policy, ADR-0003, and archive of the
  superseded working draft. Repository consolidated into a single canonical git repo.
