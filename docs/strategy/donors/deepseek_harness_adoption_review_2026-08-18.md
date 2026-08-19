# DeepSeek Harness Adoption Review for MESC

Date: 2026-08-18
Status: STRATEGIC DONOR REVIEW — NO RUNTIME ADOPTION AUTHORIZED

## Source

Repository: `deepseek-ai/deepseek-harness`

Reviewed live upstream state:

- upstream default branch: `master`
- reviewed recent head: `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`
- release represented by that head: `dsh@0.1.0-rc.7`
- upstream status: developer preview; compatibility-breaking changes are explicitly expected
- upstream license: MIT

## Decision

DeepSeek Harness is **not** a MESC model/backbone candidate.

It is accepted as a **high-value architectural donor/reference** for the future MESC Capability Realization Layer (MCRL), agent/tool runtime, provenance, verification, and policy seams.

This review does not authorize:

- DeepSeek model use;
- importing DeepSeek Harness as a runtime dependency;
- copying upstream code into MESC;
- MCRL implementation;
- tool execution against real clinical systems;
- retrieval activation;
- P01-06 or later Pilot-01 stages.

Any code adoption requires its own bounded implementation and license/provenance gate.

## Why it matters to MESC

DeepSeek Harness is a real agent harness rather than a prompt-only control scheme. Its architecture makes model adapters, tools, session logging, the agent loop, sandboxing, approval policy, persistence, credentials, and telemetry composable and replaceable.

Several of its architectural invariants map directly onto the MESC trust problem.

## Concepts to adopt or independently reproduce

### 1. Event-sourced, append-only clinical execution ledger

Upstream treats durable session events as the source of truth for replay, persistence, transcripts, telemetry, fork/resume, and model history.

MESC adaptation:

`MCRL ClinicalEventLog`

Potential event families:

- `clinical/input-admitted`
- `evidence/observed`
- `evidence/selected`
- `claim/proposed`
- `claim/verified`
- `claim/refuted`
- `uncertainty/updated`
- `abstention/triggered`
- `tool/call`
- `tool/result`
- `calculation/verified`
- `safety/escalation`
- `modality/observation`
- `modality/disagreement`
- `goal/change`

A medical decision should be reconstructable from durable events rather than from mutable hidden application state.

### 2. `Model-visible means logged` invariant

Upstream states that anything reaching a model request must be reconstructable from the session log.

MESC should strengthen this into:

> Any evidence, patient-state fact, tool result, image/audio observation, guideline excerpt, or derived clinical constraint that can influence a MESC model request must have a reconstructable provenance-bearing event.

This is a candidate core MESC invariant.

### 3. Guarded tool execution pipeline

Upstream separates tool execution into:

1. pre-execution hooks/policy;
2. monotonic guards;
3. optional approval;
4. execution wrappers such as timeout/retry/metrics;
5. tool body;
6. post-execution policy;
7. result normalization/finalization;
8. one frozen authoritative model-visible result.

MESC adaptation:

`ClinicalToolPipeline`

Required properties should include:

- patient/resource scope check;
- tool identity and schema pinning;
- data provenance;
- read/write distinction;
- monotonic safety guards;
- explicit approval for high-risk actions;
- fail-closed behavior when approval is unavailable;
- timeout/retry policies that preserve diagnosis of prior failure;
- result schema validation;
- unit and range validation for clinical calculations;
- immutable authoritative outcome event;
- no silent transformation after verification.

### 4. Monotonic guards

Upstream places monotonic guards after pre-execution policy and allows them to deny/abstain while protecting identity.

MESC should use monotonic medical guards for constraints that later plugins cannot weaken, for example:

- forbidden patient scope;
- missing authorization;
- unsupported clinical action;
- medication contraindication gate;
- unsafe unit/range ambiguity;
- missing required identity/provenance;
- disallowed write operation;
- test-partition scientific-content boundary during research execution.

### 5. Versioned durable goals with compare-and-set semantics

Upstream goals have stable IDs, revisions, phases (`active`, `paused`, `blocked`, `complete`), durable block reasons, round caps, and compare-and-set mutations.

MESC adaptation:

`ClinicalObjective`

Candidate fields:

- stable objective ID;
- revision;
- objective text/type;
- allowed evidence scope;
- allowed tool scope;
- current phase;
- block reason code/message;
- time horizon;
- required verification coverage;
- maximum reasoning/tool rounds;
- current uncertainty state.

This can prevent stale or concurrent agent state from silently changing the clinical objective.

### 6. Capability seams

Upstream formalizes swappable capabilities using service definition, provider, and consumer roles.

MESC should use explicit seams for:

- LLM backbone;
- evidence retrieval;
- FHIR/EHR access;
- terminology service;
- medication knowledge;
- clinical calculator;
- guideline evidence;
- AMGE visual experts;
- audio/biosignal experts;
- verifier;
- sandbox;
- persistence;
- human approval.

No provider should be privileged solely because it was implemented first.

### 7. Turn/step distinction and durable tool-call adjacency

Upstream distinguishes a model request step from a multi-step turn and durably logs tool calls/results.

MESC should preserve a similar distinction so a single clinical objective may contain multiple evidence/tool cycles while still producing one auditable decision episode.

### 8. Replaceable model adapters

Upstream places model adapters behind a replaceable LLM seam.

This strongly supports the MESC Backbone Tournament architecture: MCRL should not be coupled to Llama, Apertus, gpt-oss, Phi, MedGemma, or any other specific backbone.

### 9. Sandbox and approval as first-class policy services

Upstream places sandbox and approval policy in the composable base runtime rather than burying them inside individual tools.

MESC should do the same for future clinical tool execution, particularly where actions may affect files, external systems, EHR resources, or research evidence boundaries.

### 10. Fork/resume/replay as provenance features

Upstream derives fork, resume, transcripts, and replay from the durable event stream.

MESC can use this pattern for:

- reproducible case replay;
- reviewer reproduction;
- counterfactual evidence branches;
- verifier re-runs;
- model-backbone A/B comparisons from the same admitted evidence state;
- scientific audit trails.

## What not to adopt blindly

### Do not adopt DeepSeek as a model dependency

The harness architecture is useful independently of DeepSeek model choice. The existing MESC core-model restriction remains unchanged.

### Do not import the entire Harness runtime by default

The upstream system is a broad TypeScript/Cordis agent platform and is in developer preview. MESC should not acquire a large runtime dependency merely to reuse architectural ideas.

Default strategy:

1. extract invariants and seams;
2. specify MESC-native interfaces;
3. implement the minimum medical-native runtime necessary;
4. only consider direct library reuse where it is smaller, stable, and clearly superior to independent implementation.

### Do not inherit generic-agent semantics where clinical semantics are stricter

MESC needs stronger contracts for:

- evidence provenance;
- temporal patient state;
- medication safety;
- unit normalization;
- modality disagreement;
- uncertainty calibration;
- abstention;
- emergency escalation;
- clinician/human review;
- research split boundaries;
- FHIR resource identity.

### Do not treat generic completion as clinical correctness

A completed agent goal must not imply a verified clinical conclusion. MESC completion should remain separate from evidence sufficiency, verification coverage, calibration, and safety state.

## Relationship to J-Space

J-Space remains useful as a conceptual donor for selective active state, checkpoint/recovery, verification discipline, and capability-realization thinking.

DeepSeek Harness is the stronger donor for **runtime architecture** because it provides explicit event sourcing, tool pipelines, model seams, policy hooks, sandboxing, durable goals, and replayable execution.

Recommended relationship:

- J-Space → conceptual inference-control inspiration;
- DeepSeek Harness → runtime architecture/reference implementation;
- MCRL → independent medical-native system with stricter clinical invariants.

## Proposed MCRL architecture after this review

```text
Patient / Research Input
        │
        ▼
Admission + Identity Gate
        │
        ▼
MCRL Clinical Event Log
        │
        ├── Clinical Objective (revisioned)
        ├── Patient-State Ledger
        ├── Evidence Ledger
        ├── Uncertainty / Abstention Controller
        ├── Contradiction Register
        ├── Verification Coverage
        └── Modality Agreement State
        │
        ▼
Backbone Adapter Seam
        │
        ▼
MESC Generator / Reasoner
        │
        ├── Clinical Tool Pipeline
        │     ├── pre-policy
        │     ├── monotonic guards
        │     ├── approval
        │     ├── execution
        │     ├── verification
        │     └── frozen result event
        │
        └── MESC Verifier
              │
              ▼
        Verified / Uncertain / Abstain / Escalate
```

## Recommendation

Classification: `HIGH_VALUE_ARCHITECTURAL_DONOR`

Priority: `HIGH` for post-Pilot MCRL specification.

Direct runtime dependency: `NOT_APPROVED`.

DeepSeek backbone inclusion: `NOT_APPROVED`.

Next safe action after Pilot-01: produce a bounded MCRL interface/invariant specification that compares J-Space concepts, DeepSeek Harness runtime patterns, and MESC-specific clinical requirements before any implementation.
