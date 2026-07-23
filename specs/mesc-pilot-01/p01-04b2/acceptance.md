# MESC Pilot-01 — P01-04B2 Acceptance

Status: **design decisions ratified — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

This document defines the documentation-entry-gate acceptance criteria for the
ratified P01-04B2 design decisions. No future implementation is authorized by
completion of this document.

---
## Documentation entry-gate acceptance criteria

The following criteria must be satisfied before the P01-04B2 ratification
documentation is considered complete. These criteria apply to the documentation
package only; they do not authorize implementation.

| Criterion | Requirement | Current status |
|---|---|---|
| All required documents present | README, spec, plan, acceptance, contracts, data-model, research, decision-record, implementation-task, founder-ratification | **SATISFIED — 10 of 10 present** |
| No TODO, FIXME, TBD, placeholder text | Every document scanned and clean | **SATISFIED** |
| No unqualified acceptance claims | No document states P01-04B is accepted, complete, or passed | **SATISFIED** |
| Exact canonical baseline recorded | `ce1272235cb48dbacdb18f20e1ae8db695b01328` recorded consistently | **SATISFIED** |
| Founder-decision gate satisfied | FD-B2-1 through FD-B2-8 ratified on 2026-07-24 | **SATISFIED** |
| B1 described as adopted, private, fixture-only | Consistent across all documents | **SATISFIED** |
| P01-04B overall marked incomplete | Consistent across all documents | **SATISFIED** |
| B2A–B2D marked as proposals requiring separate authorization | Consistent across all documents | **SATISFIED** |
| All pending founder decisions visibly pending | No decision marked accepted without founder ratification | **SATISFIED** |
| Documentation-only path scope | Exactly the authorized P01-04, P01-04B2, and task-registry documentation paths; no source, test, workflow, script, dependency, or lockfile changes | **SATISFIED** |
| Execution prohibitions preserved | No document authorizes split generation, leakage audit, inference, training, or metrics | **SATISFIED** |
| B0/B1 nomenclature distinction | P01-04B1 split tooling is distinct from MESC B0/B1 model work | **SATISFIED** |
| `tasks.md` reconciled | P01-T03B1, P01-T03B2, and P01-T03B3 updated without renumbering | **SATISFIED** |
| No contradiction across documents | P01-04, P01-04B2, and `tasks.md` are internally consistent | **SATISFIED** |
| Implementation gate not opened | P01-04B acceptance is still not met; B2A–B2D remain unimplemented | **SATISFIED** |
| Real execution prohibited | No split, leakage audit, dataset/model access, inference, training, or metrics authorized | **SATISFIED** |

## Documentation entry-gate stop conditions

Do not mark the P01-04B2 ratification documentation complete if:

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

## Future code acceptance criteria

The following criteria reflect the founder-ratified design decisions. They are
proposed requirements for future P01-04B implementation authorization; they are
not accepted, ratified, or implemented.

| Future criterion | Ratified requirement | Status |
|---|---|---|
| Public splitter facade | Deterministic, fixture-only (`FixtureSplitFacade`); refuses real inputs | Proposed |
| Authoritative split identity | 64-hex `split_fingerprint`; 16-hex `split_hash` is compatibility-only | Ratified |
| Canonical JSON/JSONL | UTF-8, no BOM, LF-only, sorted keys, no indentation, byte-identical across Python 3.11/3.12 and OS | Ratified |
| Atomic publication | No-overwrite semantics, atomic finalization, concurrent-writer rejection, same-filesystem requirement | Ratified |
| Leakage primitives | Exact equality; NFKC/case-folded/whitespace-collapsed normalization; token-set Jaccard 0.90/0.95; non-empty positive leakage audit expected | Ratified |
| Fixture suite | Three fixtures: exact-reference-1000-v1, constraint-stress-1000-v1, leakage-positive-v1; byte-identical outputs | Ratified |
| Write-path protections | Atomic no-overwrite rename; workspace-only temp files; no repository or evidence-root writes | Ratified |
| Date-free promotable artifacts | No timestamps in promotable artifacts; provenance in external evidence only | Ratified |
| P01-04B promotion | Requires all future criteria plus separate founder authorization and Opus review | Proposed |

No future implementation criterion authorizes P01-04C–G. Each requires separate founder authorization, exact-head CI, and independent Opus review.

## Relationship to P01-04B1 and B0 spine

P01-04B1 adoption satisfies the private split-core criteria. It does not satisfy the public facade, artifact, leakage, or entry-point criteria.

PR #52 adoption of the MESC B0 deterministic execution spine is a separate workstream. It does not satisfy any P01-04B tooling criterion and does not authorize split generation, leakage audit, or formal execution.
