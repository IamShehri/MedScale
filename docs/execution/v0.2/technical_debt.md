# MedScale v0.2 — Technical Debt Register

Stability: **public process document**.
This register is append-only.  Each item gets an ID, severity, and
rationale.  Resolution requires a follow-on ADR or milestone doc update.

## How to read this register

| Severity | Meaning |
|----------|---------|
| Critical | Breaks invariants, blocks M4, or hides architectural debt |
| High | Causes maintenance risk, documentation drift, or hidden test gaps |
| Medium | Cleanup that improves determinism or readability |
| Low | Style, naming, or minor documentation hygiene |

## Register

### TD-001
Severity: High
Category: dead exports / API drift
Location: `src/medscale/__init__.py`, `src/medscale/workspace.py`
Rationale:
The public root exports a snapshot alias `Snapshot = ResearchSnapshot`.
That alias is not exported explicitly in `workspace.py`’s module `__all__`
and is implemented as a module-level assignment instead of an explicit
re-export.  Future maintainers can miss this contract during import-graph
audits.

Proposed resolution:
- Add a frozen alias export helper path in `workspace.py` if the alias
  must remain, or
- Document `Snapshot` as an accepted backward-compatibility alias and
  mark it as frozen in ADR-0020 / release readiness.

### TD-002
Severity: Medium
Category: implicit runtime timestamp
Location: `src/medscale/workspace.py` `Workspace.snapshot()`
Rationale:
Snapshot capture uses `utc_now()` inside the public library.  That
preserves historical behavior, but it also means capture time is not an
explicit CLI input.  Dataset v1 explicitly forbids implicit timestamps;
this root primitive should stay aligned.

Proposed resolution:
Keep for M1/M2/M3 compatibility.  Document as legacy behavior; defer
to M4 if a CLI-side explicit timestamp policy is introduced globally.

### TD-003
Severity: High
Category: documentation inconsistency
Location: `docs/execution/v0.2/dataset_v1.md`
Rationale:
The doc showed two paths for license metadata:
`metadata/licenses.json` and `metadata/license.json`.
The approved architecture uses `metadata/license.json` only.

Resolution: FIXED — unified to `metadata/license.json` and aligned checksum/training-scope language with ADR-0030.

### TD-004
Severity: High
Category: dead doc / outdated plan
Location: `docs/execution/v0.2/DATASET_V1_PLAN.md`
Rationale:
The plan mixed historical context from an earlier draft, including removed training-scope language.

Resolution: FIXED — superseded plan moved to `docs/archive/DATASET_V1_PLAN.superseded.md`; current approved contract lives in `docs/execution/v0.2/dataset_v1.md`, `docs/execution/v0.2/DATASET_V1_PLAN.md` was no longer the source of truth after implementation.

### TD-009
Severity: Medium
Category: missing architecture test
Resolution: FIXED — added `test_dataset_does_not_import_research` and `test_cli_imports_are_not_imported_by_engine_modules` to `tests/test_architecture.py`.

## Priority order

1. TD-001
2. TD-007
3. TD-002 / TD-005 / TD-006 / TD-008
