# Public Repository Alignment — Specification

## Goal
Make `https://github.com/IamShehri/MedScale` the canonical truthful source for MedScale's
current state, capabilities, and quality evidence. This spec covers alignment, packaging,
distribution, and open-source readiness only. It does not add architecture, models,
datasets, or training execution.

## Non-goals
- No additional architecture layers.
- No model downloads, inference, fine-tuning, GPU execution, external APIs, or dataset mutation.
- No tags, releases, or pushes until founder approval after this audit.

## Scope
1. Public truth alignment — README, ROADMAP, CHANGELOG, RELEASES, CITATION.cff, pyproject.toml, docs index.
2. MESC positioning — clarify MedScale Evaluation, Sandbox, and Contracts tier experimentally where present.
3. Release/version strategy — SemVer, artifact naming, provenance, changelog discipline.
4. API stability classification — public / experimental / internal for all M17–M18 contracts.
5. Executable golden path — one deterministic end-to-end flow with a smoke command + example output.
6. Documentation publishing — hosted docs readiness and link hygiene.
7. Package distribution — TestPyPI / PyPI wheel/sdist readiness, provenance, checksums.
8. CI and supply-chain hardening — reproducible CI, action pinning, coverage enforcement, provenance attestation.
9. Contributor readiness — templates, onboarding, succession risk, good-first-issue candidates.

## Success criteria
- The public repository gains a truthful internal alignment plan without changing public capability claims or release metadata.
- Spec Kit artifacts explicitly record verified local versus `origin/main` state, quality baseline, and civic release boundaries.
- Future PRs are sequenced with explicit public-truth freeze points and a release gate.
- One deterministic golden-path example is identified as a release prerequisite, but not executed in this PR.

## Constraints
- Additive-only changes relative to v0.2.0 baseline public API.
- No breaking changes to existing v0.2.0 public surface.
- No hidden compute assumptions, no scheduler, no cloud integration, no execution layer beyond validation and contracts.

## Phase skip rules
- A planned hygiene or formatting phase may be recorded `Not Applicable` when a verified audit finds zero tracked behavior-preserving candidates.
- A no-op empty PR must not be created merely to satisfy sequence numbering.
- Functional, contract, API, schema, CLI, or architectural changes must move into separately scoped capability PRs.
- Skipping a non-applicable phase requires recorded evidence and an explicit sequencing amendment before the next governed capability PR is opened.

## Assumptions
- Public origin is `https://github.com/IamShehri/MedScale` on `main`.
- Local working tree contains uncommitted M17/M18/MESC/HuggingFace work relative to `origin/main`.
- Current `origin/main` is `0f9a2d3b68546e5475946a582be1496d8ac40ad3`, and includes merged PRs #5, #4, and #6.
