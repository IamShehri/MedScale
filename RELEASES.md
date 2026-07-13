# MedScale v0.2.0 Release Notes

**Release date:** 2026-07-13  **Tag:** `v0.2.0`  **Commit:** `[current HEAD]`  **Python:** 3.11, 3.12  **Quality gates:** ruff PASS · mypy PASS · pytest 340/340 PASS

## Highlights

- Complete v0.2 milestone set: M1 release engineering, M2 evidence infrastructure, M3 benchmark framework, Dataset v1, S0 stabilization, M4 optional backends, M5 FHIR boundary, and M6 collaboration workflow.
- Deterministic, content-addressed, local-first research intelligence platform with architecture-enforced boundaries.
- Optional backends (`transformers`, `llama.cpp`) fully isolated behind extras and CI jobs.
- FHIR boundary frozen to deterministic `ValidationReport` contracts with optional local validator.
- Multi-reviewer collaboration workflow with append-only logs, deterministic merge, conflict visibility, and PRISMA replay.

## New capabilities

### Release engineering
- Structured logging, release workflow, coverage enforcement, storage hygiene checks.
- Architecture enforcement tests prevent package boundary decay.

### Evidence infrastructure
- `medscale.evidence` subpackage with frozen models, grading, protocol, and backward-compatible shim.
- Evidence store and checks packages isolated from `litdb`.

### Benchmarks
- Deterministic benchmark spec, task contract, frozen scorers, and artifact-first replay.
- Five frozen run identities: `spec_id`, `snapshot_id`, `software_version`, `git_sha`, `scorer_version`.

### Dataset v1
- Deterministic manifest, schema, and seed-42 content-hash split.
- Sibling `.sha256` checksums and metadata/license enforcement.

### FHIR boundary
- `medscale.fhirkit` package with `ValidationReport`, deterministic serialization, content-addressed storage.
- Optional local validator boundary with explicit install guidance on missing dependency.

### Collaboration workflow
- Reviewer-scoped append-only JSONL logs with hash chaining.
- Deterministic merge by timestamp ordering with conflict visibility.
- PRISMA reproducibility from merged reviewer logs.

## Quality

- 340 deterministic tests.
- ruff, mypy strict, pytest + coverage green.
- Optional extras CI isolated; no accidental publish.
- Architecture tests enforce downward-only dependency flow.

## Known limitations

- No release workflow YAML yet; tag-only automation planned.
- ADR-0023, ADR-0024, ADR-0025 formal registry entries deferred.
- No minimum coverage threshold enforced in CI.
- `Snapshot` alias not declared in `workspace.py` `__all__` (TD-001).
- Adapter layer still uses `urllib` for live retrieval; core paths remain offline-only.

## Recommended git tag

```
v0.2.0
```

## Recommended commit message

```
chore(release): v0.2.0 tag candidate
```
