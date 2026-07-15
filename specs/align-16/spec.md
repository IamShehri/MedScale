# ALIGN-16 — Spec

## Problem

MedScale's model-runtime surface is partially exposed through `medscale.modelkit` and
`medscale.backends`, but the public boundary is ambiguous. The package docstring
declares only `TextGenerator`, `SpanExtractor`, and `ModelRef` as public-frozen
protocols and describes everything else as internal, while the package `__all__` is
wider. Without an explicit governance decision, downstream consumers may rely on
non-stable symbols, and future runtime, promotion, lineage, or registry work may break
the public contract without an accepted migration path.

## Objective

Produce a documentation-only, evidence-bound governance audit that:

* inventories the actual model-related surfaces on canonical `main`;
* classifies each exposed symbol by stability intent;
* determines optional-backend isolation and packaging behavior;
* evaluates whether existing contracts are safe to expose;
* decides whether a new ADR is required before implementation;
* records the minimum future implementation slice without authorizing it.

## Scope

In scope:

* `medscale.modelkit` public surface and internal helpers;
* `medscale.backends` optional adapters and error/configuration contracts;
* `medscale._runtime` and `medscale.workspace` orchestration boundaries;
* `medscale.bench.scorers`, `medscale.bench.run`, `medscale.bench.spec`,
  `medscale.litdb.triage_eval` as evaluation-adjacent surfaces;
* `pyproject.toml` optional extras and packaging metadata;
* `.github/workflows/optional-extras.yml` backend coverage;
* relevant ADRs (`ADR-0006`, `ADR-0015`, `ADR-0020`);
* central alignment registry reconciliation.

Out of scope / non-goals:

```text
No real inference
No model download
No training
No routing implementation
No promotion implementation
No model-lineage implementation
No registry mutation
No export changes
No dependency changes
No ADR creation or acceptance
No push, PR, merge, or release action
No MESC implementation
No Hugging Face publication
No closure of ALIGN-10
```

## Constraints

* Canonical baseline is `3132de8789badead5a6f554a71dbaea559fe2233`.
* Only documentation may change; `src/`, `tests/`, `.github/`, `pyproject.toml`,
  lockfiles, and exports are frozen.
* No background drafting claim may appear; only committed local repository evidence
  is reported.
* `pytest` is not applicable to this Markdown-only audit and must not be treated as a
  publication gate.

## Success criteria

* All model-runtime-facing symbols are inventoried and classified.
* Registry, manifest, recipe, reporting, backend, and evaluation boundaries are
  explicitly documented.
* ADR necessity is stated exactly and backed by accepted authority documents.
* The central alignment registry reflects ALIGN-16 as a complete documentation audit.
* Final report states GO, CONDITIONAL GO, or NO-GO with exact rationale.
* Local documentation commit is clean, atomic, and ready for separate publication
  authorization.
