# ALIGN-17 — ModelKit Public Surface and Runtime Governance ADR Task

## Task identity

```text
Task: ALIGN-17
Type: ADR-only governance
Decision: Accepted
Implementation: Blocked
```

## Problem

The documented public-frozen protocol surface of `medscale.modelkit` is narrower than the current `medscale.modelkit.__all__`. The wider facade exports registry, manifest, recipe, runner, and reporting symbols without per-symbol compatibility classification. `DatasetRef` is public only through the recipes submodule. Reporting ownership is unresolved across `modelkit.reporting`, `bench.scorers`, and `BenchmarkRunArtifact`. Scientific identity semantics for `ModelRef` are inconsistent for hosted and open-weight models. ALIGN-16 recorded these items as a conditional GO pending an accepted ADR.

## Required decisions

ADR-0033 resolves:

1. exact stable facade allowlist;
2. provisional/governance-public facade symbols;
3. compatibility-carried internal helpers;
4. `DatasetRef` submodule status;
5. immutable registry-governance semantics;
6. `ModelRef` revision, quantization, backend, and digest policy;
7. recipe and manifest compatibility category;
8. reporting ownership;
9. migration protections;
10. runtime exclusions and deferred ADRs.

## Exact documentation allowlist

```text
docs/adr/0033-modelkit-public-surface-and-runtime-governance.md
specs/align-17/README.md
specs/align-17/adr-task.md
specs/align-17/acceptance.md
specs/public-repository-alignment/plan.md
specs/public-repository-alignment/spec.md
specs/public-repository-alignment/tasks.md
```

## Explicit exclusions

```text
src/
tests/
.github/
pyproject.toml
lockfiles
```

Implementation and release actions are excluded.

## Required verification

For this documentation-only package:

- full semantic review;
- `git diff --check`;
- exact path-scope gate;
- prohibited-path scan;
- clean staging state;
- comparison against canonical baseline.

```text
pytest: NOT APPLICABLE
```

Reason:

```text
No Python source, test, workflow, dependency, export, or executable behavior is changed.
```

## Future implementation gate

An accepted ADR does not define or authorize an implementation allowlist.

Any later implementation requires a separately scoped task, an exact allowlist, and separate founder authorization.
