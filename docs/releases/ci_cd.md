# Release CI/CD — Future Automation Design

- **Status:** Design only (no workflow implemented beyond the existing quality gate;
  ADR-0010, Proposed)
- **Date:** 2026-07-10

**Current state (implemented):** `ci.yml` — quality gate on push/PR, Python 3.11/3.12
matrix, `uv sync --frozen`, ruff + format + mypy strict + pytest with coverage;
`codeql.yml` — code scanning. Everything below is future design, GitHub Actions only,
built **when its first consumer release exists** — automation without an artifact to
release is speculative implementation.

## Design principles

1. **CI is the only publisher.** PyPI via trusted publishing (OIDC); HF via an org
   token stored as a repo secret, used only in release workflows. No local uploads.
2. **Human gate at the edge.** Distribution jobs run in a GitHub *environment*
   (`release`) requiring operator approval — automation executes, the operator decides.
3. **Validation before distribution, always.** A release job that cannot verify a
   manifest does not upload.

## Planned workflows (in adoption order)

| Workflow | Trigger | Jobs | Build when |
|---|---|---|---|
| `release-package.yml` | Tag `v*` | Quality gate → build wheel/sdist → install-smoke-test → manifest validation → GitHub Release → [approval] → PyPI | First PyPI release (v0.2) |
| `validate-docs.yml` | PR touching `docs/` | Internal-link check; ADR header lint (Status/Date/Deciders); archive-banner check for `docs/archive/` | With litdb v1 docs churn |
| `validate-data.yml` | PR touching `data/` | R3 licence-file presence; manifest hash re-verification; screening-log replay (legality of the whole log) | End of T1 |
| `release-dataset.yml` | Tag `*-v*` (dataset) | Dataset checklist automation: schema check → licence check → content hash → card lint → GitHub Release → [approval] → HF mirror | litdb v1 export |
| `release-model.yml` | Tag `mesc-*` | Manifest + card lint (mandatory statements present, verbatim) → eval-artifact presence check → GitHub Release → [approval] → HF mirror | MESC-v0 (T6/T7) |
| `validate-reproducibility.yml` | Manual / pre-release | Re-run headline scores from the replication package on a clean runner; byte-compare result artifacts | First paper submission |

## Validation jobs — what "lint" means here

- **Card lint:** mandatory sections present; the two verbatim statements
  ([model_cards.md §2](model_cards.md)) byte-exact; version/tag/licence fields
  consistent with the manifest.
- **Licence validation:** every `data/` dir has `LICENSE.md`; SPDX ids from the
  allowed set; composite datasets have field tables.
- **Manifest validation:** required fields present; `git_sha` matches the tag;
  dataset hashes resolve to known releases.

## Non-goals

No CD to any runtime (MedScale ships artifacts, not services); no auto-merge; no
scheduled retraining; no HF sync outside tagged releases. The pipeline's job is to make
the *approved* path effortless and every other path impossible.
