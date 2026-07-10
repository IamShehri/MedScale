# ADR-0004 — T0 Foundation Scope: one package, not a monorepo

- **Status:** Accepted
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [ADR-0003](0003-repository-topology.md) (topology), Rules
  [R4](../governance/rules.md#r4--one-ticket-per-session), R6;
  [Strategic Blueprint §7](../vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md);
  [Research Vision](../vision/MEDSCALE_RESEARCH_VISION.md)

## Context

With the repository consolidated, version-controlled, and pushed to GitHub, and with
ADR-0003 (topology) accepted, T0 — the engineering foundation — is authorized to begin.

A founding-engineer charter proposed structuring the repo as eight packages
(`medscale`, `fhirkit`, `bench`, `data`, `train`, `eval`, `common`) and scaffolding
training/evaluation/benchmark code up front.

Three constraints pull against that:

1. **The Blueprint itself** (§7.2) specifies "a single, cohesive Python package
   (`medscale` / `fhirkit`)" as the consumable surface.
2. **Scope discipline** is the program's stated survival strategy: the Research Vision
   warns that "adding breadth now is how solo projects die," Rule R4 mandates one ticket
   at a time, and the pre-freeze audit flagged "an unfocused collection of tools" as a
   top scope risk.
3. **The charter's own principles**: avoid overengineering, avoid premature abstraction,
   build foundations not research, prefer the simpler option.

Eight top-level packages, seven of which would be empty at T0, is premature abstraction:
it creates interfaces before there is behavior to justify them, multiplies packaging and
CI surface, and signals breadth the program has explicitly disowned.

## Decision

1. **MedScale is one Python package, `medscale`, in `src/` layout.** Subpackages are
   added *inside* it only when a phase produces code to hold (e.g. `medscale.fhirkit` at
   T2, `medscale.bench` at T3). No empty top-level packages are created ahead of need.

2. **Toolchain:** uv (env + lock), hatchling (build), Ruff (lint + format), Mypy
   (`strict`), Pytest + coverage. Python `>=3.11` (3.11 is the pinned baseline per
   ADR-0003; CI also runs 3.12). `uv.lock` is committed.

3. **The public API is what `medscale/__init__.py` exports** and ships `py.typed`, so
   downstream consumers (Afia) receive types. At v0 the surface is reproducibility
   primitives only.

4. **The quality gate** (ruff + ruff-format + mypy-strict + pytest) must pass locally
   (pre-commit) and in CI before any merge. Verification is a run, not a claim (R5).

## Consequences

**Positive**

- Minimal, honest surface; no dead scaffolding. Simpler to maintain solo.
- Consistent with the Blueprint's stated package design and with scope discipline.
- Strict typing + `py.typed` make the eventual Afia consumption contract type-safe.

**Negative / costs**

- Contributors expecting a monorepo must add subpackages inside `medscale/` instead of at
  the top level; documented in the developer guide.
- If a subpackage later needs an independent release cadence, it can be extracted then —
  a reversible, evidence-driven change, not a speculative one now.

## Alternatives considered

- **Eight-package monorepo now.** Rejected: premature abstraction; contradicts Blueprint
  §7.2, Rule R4, and the audit's scope-risk finding; produces empty packages.
- **Single module (no package).** Rejected: MedScale is meant to be installed and consumed
  by Afia; it needs to be a real, typed, versioned package from the start.

## Compliance

Enforced by the CI quality gate and the committed `pyproject.toml`. Extracting or adding
top-level packages is a decision >1 day to reverse and requires a new ADR (R6).
