# ALIGN-15 — Evaluation Engine Boundary Audit Plan

## Audit stages

### Stage 1 — Canonical verification
- Verify `origin/main` matches expected SHA `99b024aaf6831ad15296cb85210b8ae7f8df6998`.
- Verify ALIGN-13, ALIGN-14 implementation, and ALIGN-14 governance commits are ancestors.
- Confirm no unexpected main advancement.

### Stage 2 — Surface discovery
- Enumerate all production modules, tests, facades, CLI commands, packaging exposure, and ADR/docs references that contain evaluation-adjacent code.
- Search for `EvaluationReport`, `EvaluationResult`, `evaluation`, `evaluator`, `pipeline`, `execution`, `metric`, `benchmark`, `uncertainty`, `report bundle`.
- Map each hit to its actual owner module and exposure level.

### Stage 3 — Dependency and import analysis
- For each evaluation-adjacent module, document:
  - canonical owner;
  - inbound imports;
  - outbound imports;
  - dependencies on evidence, dataset, benchmark, model execution, network, scheduler, cloud, GPU;
  - optional runtime dependencies;
  - wheel exposure;
  - public export status.

### Stage 4 — Symbol classification
- Produce explicit matrix classifying every evaluation-adjacent symbol as public, experimental, or internal.
- Identify any duplicate or competing contract roots.
- Determine the stable public surface, if any.

### Stage 5 — Phase 3 naming resolution
- Audit the actual relationship between execution, result, and report concepts.
- Answer: Is `BenchmarkRunArtifact` the result, the report, or both? Is there a missing `EvaluationReport`? Should execution remain internal?

### Stage 6 — Minimum slice definition
- Identify the smallest dependency-complete future slice:
  - production allowlist;
  - test allowlist;
  - protected files;
  - explicit exclusions;
  - dependency graph;
  - facade impact;
  - clean-wheel impact;
  - serialization impact;
  - compatibility risk.

### Stage 7 — ADR determination
- Decide: ADR REQUIRED, ADR NOT REQUIRED, or INSUFFICIENT EVIDENCE.
- If required, list the exact decisions the future ADR must settle.

### Stage 8 — Registry reconciliation
- Update `specs/public-repository-alignment/tasks.md`:
  - ALIGN-13: mark completed with PR #10 evidence.
  - ALIGN-14: mark completed with PRs #11, #12, #13 evidence.
  - ALIGN-15: add as Evaluation Engine Boundary Audit with accurate final status.
- Update `specs/public-repository-alignment/plan.md`:
  - Replace obsolete baseline SHA with current `origin/main`.
  - Mark Phase 2 complete.
  - Record ALIGN-13 and ALIGN-14 complete.
  - Identify Phase 3 evaluation audit as current governed phase.
  - Preserve implementation blocking until audit and any required ADR are approved.
- Review `specs/public-repository-alignment/spec.md`:
  - Correct only stale baseline SHA or obsolete current-state assumptions.

### Stage 9 — ALIGN-15 Spec Kit package creation
Create the following documentation files under `specs/align-15/`:
- `README.md` — task identity, planning status, authorization boundary
- `research.md` — repository evidence and file inventory
- `spec.md` — problem, objective, scope, non-goals, success criteria
- `plan.md` — audit stages and decision gates
- `audit-task.md` — completed planning/audit task definition
- `contracts.md` — existing and candidate contract boundaries
- `data-model.md` — evaluation domain map
- `decision-record.md` — alternatives, boundary, ADR requirement, deferrals
- `acceptance.md` — audit claims mapped to evidence, next founder gate

### Stage 10 — Local commit and verification
- Stage only documentation files under `specs/`.
- Commit with message: `docs(align-15): audit evaluation engine boundary`.
- Run verification:
  - `git diff --check`
  - `git status --short`
  - `git diff --name-only | grep -E '^(src|tests|\.github|pyproject\.toml|uv\.lock|poetry\.lock)'` (must produce no output)
- Do not push. Do not open a PR. Do not create tags or releases.

## Future PR sequence

1. **ALIGN-15 docs PR** — this audit; blocks nothing except future evaluation implementation planning.
2. **[Future]** ADR-only PR — if ADR is required, this opens after ALIGN-15 is merged.
3. **[Future]** Evaluation capability PR — requires separate founder authorization after ADR is accepted and merged.

## Decision gates

| Gate | Owner | Blocking |
|---|---|---|
| Canonical main verified | auditor | Yes |
| Surface discovery complete | auditor | Yes |
| Symbol classification complete | auditor | Yes |
| Minimum slice defined | auditor | Yes |
- ADR requirement decided | auditor | Yes |
| Registry reconciled | auditor | Yes |
- Spec Kit package complete | auditor | Yes |
- Documentation-only scope verified | auditor | Yes |
- Local atomic commit created | auditor | Yes |
- Publication authorization | founder | Yes |
