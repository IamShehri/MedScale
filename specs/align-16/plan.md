# ALIGN-16 — Plan

## Goal

Document the model-runtime governance boundary without implementing it.

## Stages

1. **Surface discovery**
   * list all model-runtime-relevant modules, exports, facades, helpers, tests, workflows,
     and ADRs;
   * do not invent nonexistent modules.

2. **Packaging and extras inspection**
   * inspect `pyproject.toml`;
   * record core dependencies, optional extras, platform markers, shipped modules,
     import safety, lockfile bounds, and Windows behavior.

3. **Workflow evidence classification**
   * inspect `.github/workflows/optional-extras.yml`;
   * classify each job as core compatibility, optional-dependency installation, backend
     contract/contract-test evidence, or real inference evidence.

4. **Symbol-by-symbol classification**
   * classify every `modelkit` and `backend` symbol separately;
   * do not classify a function as public merely because it appears in `__all__`.

5. **Registry analysis**
   * determine whether `REGISTRY` is immutable fact registry, runtime registry,
     promotion store, or deployment registry;
   * assess query helpers and validate-public status.

6. **Recipe and manifest analysis**
   * confirm schema-only vs execution behavior;
   * confirm content-addressed identity, runner detection purity, and environment-metadata
     treatment.

7. **Reporting/evaluation ownership analysis**
   * compare `modelkit.reporting` against `bench.scorers` and `BenchmarkRunArtifact`;
   * flag overlaps.

8. **Promotion and lineage discovery**
   * record actual concepts vs nonexistent concepts;
   * do not insert placeholder contracts.

9. **ADR authority review**
   * map decisions to accepted ADRs;
   * state exactly whether an ADR is required.

10. **Future guarded sequence**
    * record exact sequence under separate authorization gates;
    * do not imply ADR acceptance authorizes implementation.

## Decision gates

| Gate | Required outcome |
|------|------------------|
| Canonical main | `3132de8789badead5a6f554a71dbaea559fe2233` |
| Worktree/branch | clean `docs/align-16-model-runtime-governance-audit-v2` baseline |
| Documentation scope | all changes under `specs/` only |
| Verification | `git diff --check` PASS; prohibited-path gate emits no output |
| Audit decision | `CONDITIONAL GO` with `ADR REQUIRED BEFORE IMPLEMENTATION` |
| Registry state | `ALIGN-10` pending; `ALIGN-13`–`ALIGN-15` done; `Phase 4` current |
| Commit | one atomic documentation commit; no push |

## Future sequence

```text
ALIGN-16 audit merge
→ separately authorized ADR-only task
→ ADR review and acceptance
→ separately authorized exact implementation allowlist
→ implementation PR
```

An accepted ADR does not automatically authorize implementation. Future implementation
remains blocked until a separate founder authorization issues an exact allowlist.
