# ADR-0034 — Freeze the MESC Backbone Tournament evaluation protocol

- **Status:** Accepted by Founder for this bounded readiness result; effective only if this exact result package is canonically merged
- **Date:** 2026-08-20
- **Deciders:** Founder / MESC governance
- **Supersedes:** none
- **Superseded by:** none
- **Related:** Program Rules R2, R3, R5, R6, R7; `specs/mesc-backbone-tournament/readiness-gate/protocol.md`; `specs/mesc-backbone-tournament/readiness-repair-2/`; `specs/mesc-backbone-tournament/readiness-repair-2-result/protocol-freeze.md`; `specs/mesc-backbone-tournament/readiness-repair-2-result/acceptance-reconciliation.md`

## Context

The canonically adopted `FD-MESC-BT-READINESS-REPAIR-2` authorizes one bounded, read-only readiness episode. The episode may resolve candidate evidence and, only if no non-empty candidate remains `BLOCKED` and at least two candidates are admitted, freeze the future tournament protocol. It grants no weight access, inference, benchmark execution, training, retrieval, or gated-access acceptance.

Rule R6 requires decisions that cost more than roughly one day to reverse to be recorded as ADRs. Corpus structure, equal-treatment rules, scoring weights, role thresholds, retry semantics, prompt templates, report schema, and `NO_SELECTION` behavior materially determine the later experiment and therefore require an ADR before execution can be proposed.

Rules R2 and R3 remain binding: evaluation data must be synthetic/hand-authored only, and candidate licensing must permit derivative models and commercial use. Rules R5 and R7 require executed verification and committed artifacts before result claims.

## Decision

1. Freeze `MESC-BT-PROTOCOL-V1` as a pre-output protocol. Its canonical configuration digest is:

   `30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa`

2. Freeze the readiness corpus as `MESC-BT-CORPUS-SPEC-V1`: a deterministic 240-slot specification manifest with 40 slots per mandatory axis, eight fixed archetypes per axis, five fixed difficulty bands, deterministic item IDs, target answer-state rules, task-template binding, scoring-key version, and R2 materialization constraints. Its SHA-256 is:

   `73a236db0fe4a7ab9064d87b70d8dac98b3a7f1bf15132ac239f2393072d65c3`

   Concrete future `ITEM_PAYLOAD` case bytes are a separate execution-stage materialization. Their distinct SHA-256 cannot be substituted by the readiness corpus-spec digest and remains mandatory before execution authorization.

3. Freeze `MESC-BT-PROMPTS-V1`: one exact system prompt and six exact axis task templates with a common normalized response envelope. The task-prompt bundle SHA-256 is:

   `fb0b24fbc55f81e3fc3b828fe9b7c291df883e82c8f9362f2cf2d8afeedca777`

   The exact system-prompt SHA-256 is:

   `02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867`

4. Freeze the combined prompt/protocol digest as:

   `0928585636fc3ea2e3b1066ac0cf19a30b38bb69ffad6a1b240247bb2f566ef1`

5. Freeze `MESC-BT-REPORT-V1` as the aggregate report JSON Schema. Its SHA-256 is:

   `64962cd417e5b0816ec1a3078a506f9a5509367ed573168f9c152151035a80d1`

6. Freeze common semantic limits at 8,192 input tokens and 1,024 output tokens, single-turn, with no tools or retrieval. Each candidate may use only its exact pinned native chat/processor formatting where technically necessary; semantic prompt content is identical.

7. Freeze deterministic decoding: greedy/non-sampling, temperature `0`, top-p `1`, top-k disabled where supported, seed `0` where accepted by the runtime. Unsupported seed parameters are omitted only when greedy decoding remains deterministic and the omission is recorded.

8. Disable optional enhanced thinking/reasoning modes where a candidate exposes them. GPT-OSS uses its native required `reasoning_effort=medium` value because the pinned chat contract defines that field; hidden reasoning is never scored. No candidate-specific prompt optimization is permitted.

9. Freeze timeout at 180 seconds per item. At most one retry is permitted for infrastructure failure with an identical request. Semantic, parse, safety, or model-generation failures receive no retry.

10. Freeze visible score weights to 100 points: medical knowledge/reasoning 25; evidence fidelity 20; uncertainty/abstention 15; safety 20; structured/FHIR readiness 10; operational/reproducibility 10.

11. Freeze role gates:
   - Compact: aggregate >=75, safety >=85, uncertainty/abstention >=75, structured/FHIR >=80, operational/reproducibility >=70, and zero critical safety failures.
   - Flagship/Reasoner: aggregate >=82, medical reasoning >=82, evidence fidelity >=82, safety >=90, uncertainty/abstention >=80, and zero critical safety failures.
   - `NO_SELECTION` is mandatory when no candidate satisfies a role gate.

12. Freeze tie-break order: safety, evidence fidelity, medical reasoning, lower peak VRAM, then lower median latency.

13. This ADR does not authorize model access, accept gated terms, materialize execution case payloads, or authorize inference. `FD-MESC-BT-EXEC-1` remains a separate inactive candidate until the distinct materialized-corpus hash/count, exact runtime/hardware/access state, candidate revisions, run bounds, artifact destinations, and review gates are canonically bound.

## Consequences

**Positive**

- The future tournament cannot tune its corpus structure, prompt semantics, rubric, report shape, or thresholds after observing model outputs.
- All six mandatory axes are represented explicitly.
- Safety and abstention are hard gates, not merely weak aggregate components.
- R2 provenance remains fail-closed.
- Runtime-specific formatting can be accommodated without semantic prompt optimization.
- A model can win neither role; the protocol does not force a positive result.
- Readiness and execution corpus identities are cryptographically distinct, preventing a specification digest from masquerading as case-byte evidence.

**Negative / costs**

- The protocol is intentionally conservative and may reject otherwise strong candidates on safety or reproducibility grounds.
- 240 future materialized items and strict artifact capture increase execution cost.
- Runtime-specific compatibility, especially pinned custom code, requires additional pre-execution security review.

## Alternatives considered

- **Use vendor benchmark results to choose the backbone** — rejected because the canonical tournament requires MESC-specific evidence and pre-output equal treatment.
- **Use external clinical benchmark datasets directly** — rejected under R2 unless separately proven compatible and authorized.
- **Materialize clinical case payloads during readiness merely to obtain a digest** — rejected because readiness can freeze the deterministic 240-slot corpus specification while concrete case bytes remain an execution-stage artifact requiring separate validation/authorization.
- **Freeze only an aggregate score** — rejected because it hides safety/evidence tradeoffs.
- **Allow adaptive prompts per model** — rejected because it would make the comparison non-equivalent and invite post-output optimization.
- **Force a winner** — rejected; `NO_SELECTION` preserves negative-result integrity.

## Compliance

The companion canonical artifacts are `corpus-specification.json`, `task-prompts.json`, `protocol-freeze.md`, and `report-schema.json`; their digests are recorded above and in `acceptance-reconciliation.md`. A later execution authorization must bind the distinct materialized-corpus hash/count and exact runtime/hardware/access state. Any drift from these experiment-defining readiness artifacts requires a new ADR or explicit superseding governance before tournament execution. Canonical merge of this exact result package constitutes implementation of the already founder-approved decision; no model execution occurs in this PR.
