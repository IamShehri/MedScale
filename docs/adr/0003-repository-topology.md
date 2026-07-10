# ADR-0003 — Repository Topology and the MedScale ⇄ Afia Boundary

- **Status:** Accepted (2026-07-10)
- **Date:** 2026-07-09
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** ADR-0000 (template, lands in T0), ADR-0001 (grammar engine, T2), ADR-0002 (base model, T4)

> Note on numbering: this ADR is authored *before* the T0 scaffold that creates the
> canonical `0000-template.md`. The number `0003` is reserved deliberately so that
> repository topology — a program-level, expensive-to-reverse decision (Rule R6) —
> sits above the technical ADRs (grammar engine, base model) that depend on it. When
> T0 lands, this file is reformatted to conform to `0000-template.md` without changing
> its decision content.

## Context

MedScale (MESC) is a FHIR-native clinical reasoning system — QLoRA adapters over an
open base model + grammar-constrained decoding against FHIR StructureDefinitions + a
validation layer. It is intended to become an open-source healthcare-AI research
platform and the research foundation that powers the Afia product.

Two products, one workspace:

- **MedScale** — research engine: FHIR intelligence, benchmarks, datasets, models,
  scientific publications.
- **Afia** — product layer: a healthcare operating system with Studio, AI Lab, and
  clinical workflows.

The required dependency direction is strict and one-way: **Afia consumes MedScale;
MedScale must never depend on Afia.**

### Live state at time of writing (verified, not assumed)

- `medscale/` exists inside the Afia workspace as a freshly `git init`'d repository:
  **no commits, no remote.**
- The parent Afia repo reports `medscale/` as **untracked (`?? medscale/`)** and it is
  **not** listed in the parent `.gitignore`.
- The parent workspace pins Python **3.12** (`/.python-version`); MESC requires Python
  **3.11** (project stack decision).

The untracked-embedded-repo state is a concrete hazard. A `git add -A` (or an IDE
"stage all") executed at the Afia root will embed `medscale/` as a **gitlink** pointing
at a repo with no remote and no commits — the classic path to silently unpushable,
losable work and confused tooling. This must be resolved as part of the decision, not
left to chance.

## Decision

1. **MedScale is a standalone git repository with its own remote and release
   lifecycle.** It owns its `pyproject.toml`, CI, `docs/`, Python environment
   (3.11, pinned locally in `medscale/.python-version`), versioning, and licence.

2. **Physical nesting is permitted; logical coupling is not.** `medscale/` may live
   inside the Afia workspace for convenience, but the Afia repository must treat it as
   opaque and external:
   - The parent Afia `.gitignore` **must** ignore `medscale/` so Afia never embeds it
     as a gitlink or tracks its contents. *(This resolves the live footgun above.)*
   - Alternatively, if the operator later wants Afia to pin an exact MedScale source
     revision, MedScale is registered as a **git submodule** — never as an untracked
     embedded repo. The default chosen here is the `.gitignore` route, because it best
     expresses logical independence.

3. **All MedScale tooling runs from the `medscale/` root.** `uv`, `ruff`, `mypy`,
   `pytest`, and CI resolve configuration and the Python interpreter from
   `medscale/`, never from the Afia workspace root. MedScale never reads Afia's
   `.python-version`, `package.json`, `Cargo.toml`, or `docs/`.

4. **Dependency direction is mechanically enforced, not merely stated.** MedScale
   source may not import from, path-reference, or otherwise depend on any Afia code or
   configuration. A CI guard (candidate for the T0 scaffold) fails the build if MedScale
   references any path outside its own root (e.g. `../afia-ui`, `../apps`, `../services`).

5. **Afia consumes MedScale only through published, versioned artifacts** — a Python
   package (e.g. `medscale` / `fhirkit`), released model weights, and released FHIR
   schemas/grammars — **not** by importing MedScale source across the workspace. The
   consumption contract is versioned; Afia pins a MedScale release, MedScale never
   pins Afia.

6. **The PHI boundary is one-way and absolute.** MedScale is synthetic-data-only
   (Rule R2). No real patient data, product telemetry, or clinical content from Afia
   may ever flow into MedScale training, evaluation, or benchmark data. The consumption
   edge is *outbound only*: models and schemas flow MedScale → Afia; data never flows
   Afia → MedScale.

## Consequences

**Positive**
- Clean, testable dependency direction; the research engine can be open-sourced and
  released independently of the product.
- No interpreter/toolchain cross-contamination between the 3.12 Afia workspace and the
  3.11 MedScale repo.
- The embedded-repo hazard is closed explicitly.
- Benchmarks and model cards retain scientific independence from product pressure
  (see `docs/research/reproducibility_policy.md`).

**Negative / costs**
- Two release lifecycles to maintain solo.
- The consumption contract (package + weights + schemas) must be defined and versioned
  before Afia can depend on MedScale in earnest; until then, the boundary is a
  documented intention, not yet a shipped interface.
- A CI import-direction guard must be built and maintained.

**Enforcement checklist (tracked into T0)**
- [ ] Add `medscale/` (or `/medscale/`) to the parent Afia `.gitignore`.
- [ ] `medscale/.python-version` pins `3.11`.
- [ ] MedScale CI checks out and runs only from `medscale/`.
- [ ] CI guard: fail on any upward path reference or Afia import from MedScale source.
- [ ] MedScale licence file present and permits derivative + commercial use (so Afia
      may consume it).

## Alternatives considered

- **MedScale as an Afia monorepo package.** Rejected: couples release lifecycles,
  forces a shared toolchain (Node/Rust/3.12), and makes "MedScale must not depend on
  Afia" a convention rather than a boundary. Contradicts the operator's stated topology.
- **Untracked embedded repo (the current accidental state).** Rejected: the gitlink
  footgun, no expressed independence, high risk of lost work.
- **Git submodule from day one.** Deferred, not rejected: viable once Afia needs to pin
  an exact MedScale source revision. Until a consumption contract exists, `.gitignore`
  isolation is simpler and equally correct.

## Compliance

This ADR is governed by Rule R6 (decisions costing >1 day to reverse require an ADR;
propose, wait for approval, then implement).

**Accepted 2026-07-10.** The decision is now realized: MedScale is a standalone git
repository (`github.com/IamShehri/MedScale`) with its own remote, committed history, and a
Python 3.11 baseline; T0 scaffolding has proceeded under
[ADR-0004](0004-t0-foundation-scope.md). The "Live state at time of writing" section above
is retained as a historical record. One enforcement item remains **outstanding on the Afia
side** (not actionable from this repository): add `/medscale/` to the parent Afia
`.gitignore` and retire the now-empty nested `Afia-remote/medscale/` repository.
