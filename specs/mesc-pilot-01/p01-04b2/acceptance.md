# MESC Pilot-01 — P01-04B2 Acceptance

Status: **specification and entry-gate proposal only — implementation and execution not authorized**

This document defines documentation-entry-gate acceptance separately from any future code acceptance. No future implementation is authorized by completion of this document.

---

## Documentation entry-gate acceptance criteria

The following criteria must be satisfied before P01-04B2 documentation is considered complete. These criteria apply to the documentation package only; they do not authorize implementation.

| Criterion | Requirement | Current status |
|---|---|---|
| All required documents present | README, spec, plan, acceptance, contracts, data-model, research, decision-record, implementation-task | **SATISFIED — 9 of 9 present** |
| No TODO, FIXME, TBD, placeholder text | Every document scanned and clean | **SATISFIED** |
| No unqualified acceptance claims | No document states P01-04B is accepted, complete, or passed | **SATISFIED** |
| Exact canonical baseline recorded | `3edf328f583f13fcd9d566e5080ec3cce83ae178` recorded consistently | **SATISFIED** |
| B1 described as adopted, private, fixture-only | Consistent across all documents | **SATISFIED** |
| P01-04B overall marked incomplete | Consistent across all documents | **SATISFIED** |
| B2A–B2D marked as proposals requiring separate authorization | Consistent across all documents | **SATISFIED** |
| All pending founder decisions visibly pending | No decision marked accepted without founder ratification | **SATISFIED** |
| Documentation-only path scope | Exactly the authorized P01-04, P01-04B2, and task-registry documentation paths; no source, test, workflow, script, dependency, or lockfile changes | **SATISFIED** |
| Execution prohibitions preserved | No document authorizes split generation, leakage audit, inference, training, or metrics | **SATISFIED** |
| B0/B1 nomenclature distinction | P01-04B1 split tooling is distinct from MESC B0/B1 model work | **SATISFIED** |
| `tasks.md` reconciled | P01-T03B1, P01-T03B2, and P01-T09 updated without renumbering | **SATISFIED** |
| No contradiction across documents | P01-04, P01-04B2, and `tasks.md` are internally consistent | **SATISFIED** |

## Documentation entry-gate stop conditions

Do not mark P01-04B2 documentation complete if:

- any required document is missing;
- any document contains TODO, FIXME, TBD, placeholder, or conflict-marker text;
- any document claims P01-04B is accepted, complete, or passed;
- any document claims execution is authorized;
- any document claims leakage is ruled out;
- any document modifies P01-04A decisions D1–D10 without explicit founder action;
- any contradiction exists between P01-04 documents and P01-04B2 documents;
- any authorized path outside the following authorized documentation scope is modified:
  - `specs/mesc-pilot-01/p01-04/**`
  - `specs/mesc-pilot-01/p01-04b2/**`
  - `specs/mesc-pilot-01/tasks.md`

## Future code acceptance criteria (proposed, not ratified)

The following criteria are proposed for future P01-04B implementation acceptance. They are not accepted, ratified, or implemented.

| Future criterion | Proposed requirement | Status |
|---|---|---|
| Public splitter facade | Deterministic, fixture-only, refuses real inputs | Proposed |
| Artifact builders | Produce canonical JSONL with deterministic output | Proposed |
| Split fingerprint (64-hex) | Computable from promoted artifacts alone | Proposed |
| Leakage primitives | Exact, normalized, Jaccard; no raw text exposure | Proposed |
| Fixture-only entry point | No real registry access, no evidence-root writes | Proposed |
| Write-path protections | Atomic rename, no-overwrite, concurrent-writer rejection | Proposed |
| Synthetic 1,000-row qualification | Byte-identical output, target counts 700/150/150 | Proposed |
| P01-04B promotion | Requires all future criteria plus independent Opus review | Proposed |

No future criterion authorizes P01-04C–G. Each future criterion requires separate founder authorization and independent Opus review.

## Relationship to P01-04B1 and B0 spine

P01-04B1 adoption satisfies the private split-core criteria. It does not satisfy the public facade, artifact, leakage, or entry-point criteria.

PR #52 adoption of the MESC B0 deterministic execution spine is a separate workstream. It does not satisfy any P01-04B tooling criterion and does not authorize split generation, leakage audit, or formal execution.
