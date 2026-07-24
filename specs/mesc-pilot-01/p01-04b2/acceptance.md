# MESC Pilot-01 — P01-04B2 Acceptance

Status: **design decisions founder-ratified — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

This document defines the documentation-entry-gate acceptance criteria for the
founder-ratified P01-04B2 design requirements. The design requirements are
founder-ratified; they are not implementation-accepted, implemented, or
execution-authorized. No future implementation is authorized by completion of
this document.

## Documentation entry-gate acceptance criteria

The following criteria must be satisfied before the P01-04B2 ratification
documentation is considered complete. These criteria apply to the documentation
package only; they do not authorize implementation.

| Criterion | Requirement | Status |
|---|---|---|
| All required documents present | README, spec, plan, acceptance, contracts, data-model, research, decision-record, implementation-task, founder-ratification | **SATISFIED — 10 of 10 present** |
| No unfinished-work markers or placeholder text | Every document scanned and clean | **SATISFIED** |
| No unqualified acceptance claims | No document states P01-04B is accepted, complete, or passed | **SATISFIED** |
| Exact canonical baseline recorded | `ce1272235cb48dbacdb18f20e1ae8db695b01328` recorded consistently | **SATISFIED** |
| Founder-decision gate satisfied | FD-B2-1 through FD-B2-8 ratified on 2026-07-24 | **SATISFIED** |
| B1 described as adopted, private, fixture-only | Consistent across all documents | **SATISFIED** |
| P01-04B overall marked incomplete | Consistent across all documents | **SATISFIED** |
| B2A–B2D marked as design-ratified but unauthorized | Consistent across all documents | **SATISFIED** |
| Historic proposals labelled and superseded | PD-1 through PD-8 labelled historical where retained | **SATISFIED** |
| Change-path scope | Exactly authorized documentation paths; no source, test, workflow, script, dependency, or lockfile changes | **SATISFIED** |
| Execution prohibitions preserved | No document authorizes split generation, leakage audit, inference, training, or metrics | **SATISFIED** |
| B0/B1 nomenclature distinction | P01-04B1 split tooling is distinct from MESC B0/B1 model work | **SATISFIED** |
| `tasks.md` reconciled | P01-T03B1, P01-T03B2, and P01-T03B3 updated without renumbering | **SATISFIED** |
| No contradiction across documents | P01-04, P01-04B2, and `tasks.md` are internally consistent | **SATISFIED** |
| Implementation gate not opened | P01-04B acceptance is still not met; B2A–B2D remain unimplemented | **SATISFIED** |
| Real execution prohibited | No split, leakage audit, dataset/model access, inference, training, or metrics authorized | **SATISFIED** |

## Documentation entry-gate stop conditions

Do not mark the P01-04B2 ratification documentation complete if:

- any required document is missing;
- any document contains unfinished-work markers, placeholder text, or merge-conflict markers;
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
proposed requirements for future P01-04B implementation authorization; the
design requirements are founder-ratified and are not implementation-accepted,
implemented, or execution-authorized.

| Future criterion | Ratified requirement | Status |
|---|---|---|
| Public splitter facade | In-memory `FixtureSplitFacade`; refuses real inputs; separate from existing fail-closed splitter | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Authoritative split identity | 64-hex `split_fingerprint`; 16-hex `split_hash` is compatibility-only | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Canonical JSON/JSONL | UTF-8, no BOM, LF-only, sorted keys, no indentation, byte-identical across Python 3.11/3.12 and OS | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Atomic publication | No-overwrite semantics, atomic finalization, concurrent-writer rejection; applies to separately authorized artifact-publication components, not filesystem output behavior of `FixtureSplitFacade` | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Leakage primitives | Exact equality; NFKC/case-folded/whitespace-collapsed normalization; token-set Jaccard 0.90/0.95; non-empty positive leakage audit expected | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Fixture suite | Three fixtures: `exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`; byte-identical outputs | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Write-path protections | Atomic no-overwrite rename; workspace-only temp files; no repository or evidence-root writes | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| Date-free promotable artifacts | No timestamps in promotable artifacts; provenance in external evidence only | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |
| P01-04B promotion | Requires all future criteria plus separate founder authorization and Opus review | DESIGN RATIFIED — IMPLEMENTATION NOT AUTHORIZED |

No future implementation criterion authorizes P01-04C–G. Each requires separate founder authorization, exact-head CI, and independent Opus review.

## Relationship to P01-04B1 and B0 spine

P01-04B1 adoption satisfies the private split-core criteria. It does not satisfy the public facade, artifact, leakage, or entry-point criteria.

PR #52 adoption of the MESC B0 deterministic execution spine is a separate workstream. It does not satisfy any P01-04B tooling criterion and does not authorize split generation, leakage audit, or formal execution.
