# ALIGN-16 — Model Runtime and Governance Boundary Audit

## Task identity

Repository audit of MedScale’s model runtime, backend, registry, recipe, manifest,
reporting, promotion, lineage, training-artifact, and infrastructure surfaces to
determine the stable contract boundary, classify public exposure, and decide whether
implementation may proceed.

## Canonical baseline

```text
Repository: IamShehri/MedScale
Canonical branch: main
Expected origin/main:
3132de8789badead5a6f554a71dbaea559fe2233
```

## Status

```text
Planning/audit: complete
Runtime implementation: not authorized
ADR: required before implementation
Audit decision: CONDITIONAL GO
```

A viable dependency-safe contract boundary exists, but the current `modelkit`
public surface, registry exposure, reporting ownership, and missing promotion/lineage
contracts require a dedicated ADR before any implementation.

## Document index

- `README.md` — this file.
- `research.md` — inspected production files, tests, packaging, workflows, and
  authority documents.
- `spec.md` — problem statement, objective, scope, non-goals, constraints, and
  success criteria.
- `plan.md` — stages and decision gates.
- `audit-task.md` — completed audit task.
- `contracts.md` — existing, experimental, internal, and nonexistent contracts.
- `data-model.md` — domain concept inventory.
- `decision-record.md` — selected boundary, rejected alternatives, and ADR requirement.
- `acceptance.md` — claims mapped to repository evidence and next founder gate.

## Authorization boundary

Authorized:

* read-only repository inspection;
* creation of one clean documentation branch and worktree;
* documentation-only ALIGN-16 Spec Kit artifacts;
* narrow reconciliation of the central alignment registry;
* one local atomic documentation commit;
* mechanical documentation verification;
* a final read-only report.

Not authorized:

* production source changes;
* test changes;
* package facade or export changes;
* model downloads;
* inference;
* fine-tuning or training;
* GPU execution;
* network or cloud execution;
* external APIs;
* mutable model registries;
* provider configuration;
* routing implementation;
* promotion implementation;
* persistence implementation;
* workflow or dependency changes;
* lockfile changes;
* ADR creation or acceptance;
* push;
* pull-request creation;
* merge;
* branch deletion;
* tag or release;
* MESC implementation;
* Hugging Face publication;
* closure of ALIGN-10.
