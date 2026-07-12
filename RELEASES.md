# MedScale v0.1.0 Release Notes

**Release date:** 2026-07-12  
**Tag:** `v0.1.0`  
**Commit:** `30983d6`  
**Python:** 3.11, 3.12  
**Quality gates:** ruff PASS · mypy PASS · pytest 277/277 PASS

## Highlights

- First stable release of the MedScale research-intelligence foundation.
- Deterministic literature database (`medscale.litdb`) with content-addressed corpus storage and append-only screening audit trail.
- Advisory AI triage module (`medscale.litdb.ai_triage`) with runtime-validated typing, deterministic scoring, and goldset-ready evaluation helpers.
- Frozen screening decision semantics (ADR-0022) and mission-zero operations manual.
- Strict quality gate integration: ruff, mypy strict, pytest + coverage, CI on Python 3.11 and 3.12.

## New capabilities

### Reproducibility spine
- Content-addressed record identity (`LiteratureRecord.record_id`).
- Deterministic snapshot capture and verification (`medscale snapshot --verify`).
- Canonical JSON serialization and content hashing.
- Internal `_layout` and `_runtime` modules eliminate path and timestamp drift.

### Literature database (`medscale.litdb`)
- `LiteratureRecord` schema with identifier normalization, provenance, and `EvidenceTier`.
- `ReviewDecision` state machine with mandatory exclusion taxonomy.
- Append-only `review_log.jsonl` and `triage_log.jsonl` audit logs.
- Atomic evidence writes via temp-file + replace.
- CLI commands: `screen`, `screen amend`, `snapshot`, `stats`, `check`.

### AI triage
- `AIRecommendation` dataclass with `to_dict` / `from_dict` round-trip under strict mypy.
- `pending_for_triage` advisory screen that never excludes automatically.
- Deterministic recommendation flags: confidence, evidence tier, priority, recommendation literal.
- Evaluation helpers (`compute_metrics`, `write_goldset`) with `collections.abc.Mapping` contracts.
- Separate triage audit log to avoid collision with screening/review logs.

### Screening semantics
- ADR-0022 accepted: `INCLUDE` = passed title/abstract; `EXCLUDE` = stage-terminal with taxonomy; `UNCERTAIN` = revisit marker; `DUPLICATE_CONFIRMED` = pre-screening dedupe bucket.
- Eligibility is a distinct future stage; existing events remain valid under future extensions.

### Researcher documentation
- `docs/guides/research_quickstart.md`: fifteen-minute path to first screening decisions.
- `docs/guides/first_systematic_review.md`: complete PRISMA-mapped workflow.
- `docs/guides/troubleshooting.md`: symptom-first operator guidance.

## Architecture

- Verified layering: Verification & Reproducibility Spine + seven capability layers.
- Public API frozen per ADR-0020; stability tiers and deprecation policy documented.
- Six build-failing architecture enforcement tests (`tests/test_architecture.py`).
- No EventBus, CQRS, repo pattern, or unnecessary abstraction layers.
- Package uses `src/medscale` layout with hatchling build backend.

## AI Triage

- Advisory-only: no automatic exclusion, no model API calls in v0.1.
- Model/provider fields are optional string metadata for future backend integration.
- Evidence tracking via `evidence_tier` and `confidence` fields.
- Goldset pipeline ready for offline evaluation against operator-labeled decisions.
- Reproducibility: deterministic flags, no runtime randomness, content-addressed inputs.
- Future-ready: `modelkit.interfaces` protocols defined; backends gated to v0.2+.

## litdb

- JSONL corpus with byte-stable identifiers and manifest integrity.
- Source adapter protocol implemented (network code deferred).
- PRISMA screening state machine with append-only replay validation.
- Format version marker in all persisted artifacts (`"format": 1`).
- Interrupt-safe CLI with saved-state messages and atomic writes.

## Quality

- ruff configuration: E, F, I, N, UP, B, A, C4, SIM, PTH, RUF.
- mypy strict mode with `warn_unused_configs`, `warn_redundant_casts`, `warn_unreachable`.
- pytest with strict markers and config; coverage branch tracking enabled.
- CodeQL, Dependabot, pre-commit hooks active in CI.
- 277 deterministic tests on Python 3.11/3.12.

## Testing

- Unit tests: `tests/test_*.py` covering evidence engine, research engine, bench engine, CLI UX, format versioning, architecture rules, ai_triage, litdb modules.
- Architecture tests: layer boundaries, no root imports, downward-only dependencies, transport isolation.
- Operator-safety tests: interrupt handling, friendly failures, append-only corrections.
- No mocked network code; source adapters are protocol-only in v0.1.

## Documentation

- README with status, repository map, quickstart, and quality-gate instructions.
- ADR registry with 23 records (0000–0022); numbering and cross-references audited.
- ROADMAP with T0–T7 phase mapping and horizon classification.
- CHANGELOG following Keep a Changelog with `[Unreleased]` and `[0.1.0]` sections.
- CITATION.cff with version, date-released, and Apache-2.0 license.
- SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md present.
- Release infrastructure design documented in `docs/releases/` (12 documents); implementation deferred to v0.2.

## Known limitations

- No PyPI publish workflow yet; first distribution via GitHub Releases only.
- ADR-0010, ADR-0011, ADR-0013, ADR-0014 remain Proposed; not self-ratified.
- Repository authority concentrated on a single maintainer account (ADR-0019 proposed, not accepted).
- No runtime dependencies; all medical model inference, FHIR validation toolkit, and benchmark execution are deferred.
- `_layout` paths are local constants; multi-user collaboration semantics not designed.
- Logging is human-only (print statements); structured observability deferred.
- No authentication or authorization layer; single-operator use only.
- Coverage reporting in CI does not enforce minimum thresholds.
- `uv.lock` size is present but acceptable; no distribution size optimization performed.

## Roadmap to v0.2

1. Accept or formalize ADR-0019 governance/succession plan.
2. Implement GitHub Release + PyPI publish workflow from `docs/releases/ci_cd.md`.
3. Add structured logging across CLI and litdb engines.
4. Make `AIRecommendation.model/provider` first-class `ModelRef` from `modelkit.interfaces`.
5. Execute first reproducible benchmark parity score against deterministic scorers.
6. Introduce optional file-backed ACL stub before multi-user deployment.
7. Automate dataset licence validation in CI for `data/` changes.
8. Expand triage tests: malformed JSONL, corrupted logs, schema evolution, Windows file locking.

## Recommended git tag

```
v0.1.0
```

## Recommended commit message

```
chore(release): v0.1.0 freeze prep
```
