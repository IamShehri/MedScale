# ADR Implementation Tracker

## M1 Relevant ADRs
- ADR-0004: Foundation scope (single-package).
- ADR-0010: Release architecture (`docs/adr/0010-release-architecture.md`).
- ADR-0012: Layered architecture.
- ADR-0013: Language strategy (Python only).

## M2 Relevant ADRs
- ADR-0009: Evidence model (`docs/adr/0009-evidence-model.md`).
- ADR-0018: Evidence identity decoupling.

## M3 Relevant ADRs
- ADR-0022: Screening decision semantics.

## Dataset v1 Relevant ADRs
- ADR-0017: Identifier stability contract.
- ADR-0030: Dataset versioning and training-artifact contract.

## M4 Relevant ADRs
- ADR-0027: Optional extras (`docs/execution/v0.2/M4-README.md`).
  - `backends-transformers` and `backends-llamacpp` extras defined in `pyproject.toml`.
  - CI isolation in `.github/workflows/optional-extras.yml`.

## M5 Relevant ADRs
- ADR-0008: FHIR as canonical clinical representation (`docs/adr/0008-interoperability-fhir-canonical.md`).
- ADR-0028: FHIR boundary determinism and optional validator integration (`docs/execution/v0.2/M5-README.md`).
  - Deterministic `ValidationReport` schema.
  - Content-addressed storage.
  - Optional validator boundary with explicit local execution.

## M6 Relevant ADRs
- ADR-0026: Collaboration model (`docs/execution/v0.2/M6-README.md`).
  - Reviewer-scoped append-only JSONL logs.
  - Deterministic merge with conflict visibility.
  - PRISMA reproducibility via merged redirects.
  - Audit preservation and replay integrity.

## Post-v0.2 ADRs
- ADR-0023 Structured Logging: formal record deferred to v0.3 governance pass.
- ADR-0024 Release Automation: documented in `docs/releases/ci_cd.md`; implementation blocked until `.github/workflows/release.yml` exists.
- ADR-0025 Coverage Policy: formal threshold deferred to post-v0.2 quality-gate pass.
