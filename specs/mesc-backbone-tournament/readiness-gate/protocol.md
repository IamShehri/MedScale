# MESC Backbone Tournament — Protocol Contract Draft

Status: **DESIGN CONTRACT ONLY — EXECUTION PROHIBITED**

Date: 2026-08-19

This file freezes the protocol requirements that the readiness episode must resolve before a separate tournament execution authorization can even be proposed.

## 1. Tournament objective

The future tournament is a bounded **zero-shot backbone selection experiment**, not a training competition.

Its intended outputs are:

- one `MESC-Compact` backbone candidate;
- one `MESC-Reasoner / Flagship` backbone candidate;
- a transparent evidence record explaining why each was selected or why selection was blocked.

No candidate receives deep training during the tournament.

## 2. Evidence precedence

The readiness episode must treat, in order:

1. then-current canonical MESC governance and Program Rule R2;
2. canonical Pilot-01 closeout and accepted B0 provenance;
3. canonical strategy documents;
4. authoritative first-party candidate documentation/model registries/licenses;
5. reproducible local/static metadata captured by the readiness report.

Vendor benchmark claims are context only and cannot determine tournament winners.

## 3. Candidate admission requirements

Every candidate must have, before execution authorization:

- exact canonical model repository/identifier;
- immutable model revision;
- exact tokenizer/processor identifier and immutable revision;
- license text/identifier and use restrictions recorded;
- access/gating conditions recorded;
- architecture and parameter-class recorded;
- precision/runtime assumptions recorded;
- context-window and multimodal capabilities recorded where applicable;
- authoritative provenance links recorded in the readiness report;
- reproducible loading plan with `trust_remote_code` policy explicitly decided;
- hardware feasibility recorded;
- no conflict with the project policy excluding Chinese model families from the core model stack;
- no conflict with Program Rule R2 or other canonical safety/governance rules.

Candidate disposition is deterministic:

- `BLOCKED` means one or more required facts remain unresolved, unproven, contradictory, or unavailable. Any `BLOCKED` disposition for a non-empty roster slot forces the **overall readiness verdict to `BLOCKED`** and prevents production of a ready execution-authorization candidate.
- `NOT_ADMITTED` may be used only when authoritative evidence conclusively establishes a disqualifying condition, such as a policy conflict, incompatible license/access condition, or demonstrated architectural/runtime infeasibility. It must not be used as a substitute for unresolved evidence.
- `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE` means every admission requirement above is proven for proposal into a later, separately reviewed execution-authorization package. It grants no execution authority by itself.

A successful readiness verdict additionally requires an **execution-viable competitive roster**: at least two distinct non-empty roster candidates must be `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`. If fewer than two distinct candidates are admitted after all non-empty slots are conclusively dispositioned, the overall readiness verdict is `BLOCKED`. This minimum does not predetermine either future winner; it only prevents a zero- or one-candidate package from being labeled ready for a comparative tournament intended to select Compact and Flagship/Reasoner backbones.

## 4. Design-time roster and challenger

Initial family-level roster:

1. `gpt-oss-20b`;
2. `Apertus 1.5 8B`;
3. `Phi-4 Multimodal 5.6B`;
4. `MedGemma 1.5 4B IT`.

One challenger slot may be filled only during readiness, before any tournament inference, using the same admission criteria and a documented founder-visible rationale.

A challenger may not be added after model outputs are visible.

## 5. R2-compatible evaluation corpus

The execution protocol must use only synthetic or hand-authored evaluation material that is compatible with Program Rule R2.

The tournament may not use:

- Pilot-01 test content;
- non-synthetic patient data;
- product telemetry;
- PHI;
- external clinical benchmark data that violates R2;
- hidden or untracked examples;
- training data reused as evaluation without explicit provenance and policy approval.

External benchmark families may inspire task design only unless separately proven R2-compatible and explicitly admitted.

## 6. Required evaluation axes

The frozen evaluation contract **must cover every axis below at minimum**. Omission of any axis is a protocol-freeze blocker and forces the readiness verdict to `BLOCKED`.

### A. Medical knowledge and reasoning

- bounded clinical/biomedical reasoning;
- diagnostic-style reasoning on synthetic cases;
- treatment/test-selection reasoning where safely representable.

### B. Evidence fidelity

- supported vs unsupported claims;
- contradiction recognition;
- stale/irrelevant evidence detection;
- provenance-aware response structure.

### C. Uncertainty and abstention

- insufficient-information abstention;
- conflicted-evidence abstention;
- request-for-more-information behavior;
- harmful overconfidence penalties.

### D. Safety

- emergency escalation on synthetic scenarios;
- medication/contraindication conflict recognition;
- refusal/abstention behavior when required.

### E. Structured/FHIR readiness

- synthetic FHIR-like resource reasoning;
- deterministic structured-output adherence;
- missing-resource fail-closed behavior.

### F. Operational characteristics

- latency;
- peak memory/VRAM where measured;
- tokens generated;
- cost where an upstream provider cost exists;
- reproducibility and operational complexity.

## 7. Equal-treatment rules

Before execution authorization, the readiness episode must freeze:

- exact prompts/system prompts;
- message formatting rules;
- maximum input/output lengths;
- decoding strategy;
- temperature/top-p/top-k if applicable;
- random seed policy;
- stop conditions;
- parsing rules;
- timeout/retry policy;
- generation-failure classification;
- abstention categories;
- per-candidate tool/runtime accommodations that are strictly necessary and do not change the task semantics.

No candidate-specific prompt optimization after seeing results.

## 8. Scoring and selection

The readiness episode must freeze a deterministic scoring rubric before execution.

The rubric must separately report:

- reasoning/knowledge quality;
- evidence fidelity;
- uncertainty/abstention;
- safety;
- structured-output/FHIR readiness;
- reproducibility;
- latency/cost/resource footprint.

A single aggregate score may be reported only if its weights are frozen in advance and every component remains visible.

Selection must support two roles:

### Compact

Prioritize reproducibility, deployability, efficiency, and acceptable safety/reasoning quality.

### Flagship / Reasoner

Prioritize maximum reasoning/evidence/safety quality while still requiring reproducibility and an explicit resource envelope.

A model may win neither role. The protocol must allow `NO_SELECTION` if quality/safety/admissibility thresholds are not met.

## 9. Negative-results rule

All admitted candidates and all executed results must remain in the final report, including failures, disqualifications, generation errors, weak safety performance, and operational infeasibility.

No silent candidate removal after execution begins.

## 10. Reproducibility contract

A future execution package must record, at minimum:

- canonical MESC code SHA/tree;
- candidate model/tokenizer revisions;
- runtime/library versions;
- hardware/provider identity;
- evaluation corpus hash and count;
- prompt/protocol hash;
- decoding configuration;
- per-example raw structured outputs where safe;
- normalized predictions;
- aggregate metrics;
- run digest;
- artifact hashes;
- errors and exclusions.

## 11. Execution authorization boundary

Completion of readiness/protocol freeze does **not** start the tournament.

A later candidate such as `FD-MESC-BT-EXEC-1` must separately authorize exact candidate revisions, exact evaluation corpus hash, exact code/runtime, weight-access rules, and the bounded number of inference runs.

Until that later authorization is canonically adopted:

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
```
