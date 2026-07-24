# MESC Pilot-01 — P01-04B2 Plan

Status: **design decisions ratified — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

## Increment dependency DAG

B2A has no B2 implementation predecessor.
B2B requires B2A contract acceptance.
B2C requires B2A and B2B acceptance.
B2D requires B2A, B2B and B2C acceptance.

Each increment still requires:
- separate authorization;
- atomic PR;
- exact-head CI;
- independent Opus review;
- separate merge decision.

Ratification of this package does not authorize B2A.

P01-04B2 decomposes the remaining work into four bounded increments: B2A artifact types/canonical serialization, B2B leakage primitives, B2C fixture-only facade/integration entry point, and B2D integrated qualification and P01-04B acceptance review. Each increment requires separate founder authorization, exact-head CI, and independent Opus review. Ratification of P01-04B2 design decisions does not authorize any B2 increment.

| Increment | Name | Authorization required | Current status |
|---|---|---|---|
| P01-04B2A | Artifact types and canonical serialization | Separate founder authorization | Specification only |
| P01-04B2B | Leakage primitive library | Separate founder authorization | Specification only |
| P01-04B2C | Fixture-only public facade and integration entry point | Separate founder authorization | Specification only |
| P01-04B2D | Integrated synthetic qualification and P01-04B acceptance review | Separate founder authorization | Specification only |

No increment authorizes P01-04C–G.

## Increment details

### P01-04B2A — Artifact types and canonical serialization

**Purpose:** Define stable types and deterministic serialization for all P01-04B output artifacts without implementing them.

**Deliverables:**

- `SplitPolicy` type (stable fields, canonical ordering, serialization)
- `GroupRegistryEntry` type (stable fields, canonical ordering, serialization)
- `ExampleSplitRegistryEntry` type (stable fields, canonical ordering, serialization)
- `SplitSummary` type (stable fields, canonical ordering, serialization)
- `SplitFingerprint` type (stable fields, canonical ordering, serialization)
- `ExcludedOrUnassignedLedger` type (stable fields, canonical ordering, serialization)
- Leakage-related types: `LeakageFinding`, `LeakageAuditReport`
- Fixture-only execution request/result types
- Authorization and path-safety error enumerations

**Exit criteria for this increment:**

- All types have stable field definitions
- All types have canonical serialization rules
- No type contains prohibited fields (raw text, labels, local paths, timestamps)
- Serialization rules are consistent across all types
- No Python implementation is authorized

### P01-04B2B — Leakage primitive library

**Purpose:** Define the leakage-detection primitive library design without implementing real detection.

**Deliverables:**

- `exact_example_identity` function specification
- `exact_source_document_identity` function specification
- `exact_question_equality` function specification
- `normalized_question_equality` function specification (NFKC, case-folded, whitespace-collapsed)
- `token_set_jaccard` function specification (threshold >= 0.90)
- `context_equality` function specification
- Finding identifier generation rules (deterministic, stable across reruns)
- False-positive classification rules
- Suppression prohibition (explicit)

**Exit criteria for this increment:**

- All primitives have input/output contracts
- Normalization rules are unambiguous
- Thresholds and edge cases (empty token sets, Unicode edge cases) are documented
- No raw text is exposed in promotable leakage artifacts
- No Python implementation is authorized

### P01-04B2C — Fixture-only public facade and integration entry point

**Purpose:** Define the separate in-memory fixture-only facade design without implementing it.

**Deliverables:**

- `FixtureSplitFacade` design (separate from the existing private split core)
- `FixtureSplitRequest` structure and validation rules
- No CLI component
- No filesystem input or output path acceptance
- No publication side effects
- Formal P01-04D execution entry point remains separate under separate authorization

**Exit criteria for this increment:**

- Facade accepts only structurally verified in-memory `FixtureSplitRequest`
- No capability or token is required
- No B2 CLI exists
- No arbitrary filesystem input path is accepted
- No arbitrary filesystem output path is accepted
- The fixture facade performs no publication
- Existing `SourceDocumentGroupedSplitter.assign()` remains unconditionally fail-closed
- No Python implementation is authorized

### P01-04B2D — Integrated synthetic qualification and P01-04B acceptance review

**Purpose:** Define the integrated synthetic qualification test strategy using all three fixtures and P01-04B acceptance review process.

**Deliverables:**

- Qualified synthetic fixture suite (`exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`)
- Integration test design (byte-identical output, target counts 700/150/150, label reconciliation, zero group overlaps)
- Split fingerprint reproducibility test design
- P01-04B acceptance review protocol
- Post-acceptance artifact validation rules

**Exit criteria for this increment:**

- All three fixtures are present and validated
- Qualification is byte-identical across supported Python versions and operating systems
- All P01-04B acceptance criteria have a mapped execution path
- No real P01-03G membership is generated during qualification
- P01-04B acceptance can be evaluated independently of implementation

## Relationship to official stage hierarchy

The official P01-04 stage hierarchy remains:

- P01-04A: Specification and Policy Ratification (ratified)
- P01-04B: Split Contracts and Tooling (incomplete)
- P01-04C: Fixture and Dry-Run Qualification (not authorized)
- P01-04D: Formal Split Generation (not authorized)
- P01-04E: Leakage Audit and Finding Resolution (not authorized)
- P01-04F: Freeze and Independent Acceptance (not authorized)
- P01-04G: Repository Promotion and Closeout (not authorized)

B2A–B2D are internal implementation decomposition increments within P01-04B. They do not replace, abbreviate, or skip P01-04C–G.

## Prerequisites

Each increment requires:

1. Founder authorization for that specific increment.
2. Atomic PR with independent Opus review.
3. Each future increment authorization must record the exact then-current canonical main.
4. No real P01-03G registry execution.
5. No automatic authorization of the next increment.

## Stop conditions

Stop without mutation if:

- canonical main SHA does not match the recorded authorization baseline;
- any proposed implementation conflicts with P01-04A decisions D1–D10;
- any document claims execution has started;
- any document claims leakage has been ruled out;
- any document includes source-data redistribution claims beyond canonical rights record;
- an unauthorized path is modified.
