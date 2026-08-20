# Repair-2 Acceptance Reconciliation

Status: **NORMATIVE RESULT-PACKAGE RECONCILIATION CANDIDATE**

This document reconciles items 16–23 of the canonically adopted `FD-MESC-BT-READINESS-REPAIR-2` acceptance contract without expanding readiness authority into model execution or weight access.

## Readiness corpus versus execution materialization

The term `corpus` has two distinct artifact layers that must not be conflated:

1. **Readiness corpus specification** — the frozen, pre-output 240-slot evaluation manifest that fixes all item identities, six-axis allocation, archetypes, difficulty bands, target answer-state rules, R2 provenance constraints, task-template binding, and materialization rules. This is the corpus artifact required and hashable at readiness.
2. **Execution materialized corpus** — the later concrete synthetic/hand-authored `ITEM_PAYLOAD` content for those already-frozen slots. Its byte digest cannot exist until those payloads are materialized, committed, R2-audited, and separately authorized for execution. It remains a mandatory blocker for `FD-MESC-BT-EXEC-1`.

The readiness artifact is canonical compact sorted-key JSON at:

`specs/mesc-backbone-tournament/readiness-repair-2-result/corpus-specification.json`

```text
READINESS_CORPUS_SPEC_ID = MESC-BT-CORPUS-SPEC-V1
READINESS_CORPUS_ITEM_COUNT = 240
READINESS_CORPUS_SPEC_SHA256 = 73a236db0fe4a7ab9064d87b70d8dac98b3a7f1bf15132ac239f2393072d65c3
MATERIALIZED_CORPUS_SHA256 = REQUIRED_LATER_FOR_EXECUTION
```

The specification deterministically expands to 40 slots per axis: eight frozen archetypes times five frozen difficulty bands. Item IDs are fixed as `BT-{axis_letter}-{001..040}`. It cannot be altered after model outputs without superseding governance.

## Frozen prompt artifacts

Canonical compact sorted-key JSON:

`specs/mesc-backbone-tournament/readiness-repair-2-result/task-prompts.json`

```text
PROMPT_BUNDLE_ID = MESC-BT-PROMPTS-V1
TASK_TEMPLATE_COUNT = 6
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
TASK_PROMPT_BUNDLE_SHA256 = fb0b24fbc55f81e3fc3b828fe9b7c291df883e82c8f9362f2cf2d8afeedca777
```

There is one exact task template per mandatory axis. All use the same `{{ITEM_PAYLOAD}}` placeholder and normalized answer envelope. Candidate-native templates may encode identical semantics only.

The frozen protocol configuration remains:

```text
PROTOCOL_ID = MESC-BT-PROTOCOL-V1
PROTOCOL_CONFIG_SHA256 = 30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa
```

The prompt/protocol combined digest is SHA-256 over compact sorted-key JSON containing exactly `version`, `system_prompt_sha256`, `prompt_bundle_sha256`, and `protocol_config_sha256`:

```text
PROMPT_PROTOCOL_DIGEST_ID = MESC-BT-PROMPT-PROTOCOL-DIGEST-V1
PROMPT_PROTOCOL_SHA256 = 0928585636fc3ea2e3b1066ac0cf19a30b38bb69ffad6a1b240247bb2f566ef1
```

## Frozen report schema

Canonical compact sorted-key JSON Schema:

`specs/mesc-backbone-tournament/readiness-repair-2-result/report-schema.json`

```text
REPORT_SCHEMA_ID = MESC-BT-REPORT-V1
REPORT_SCHEMA_SHA256 = 64962cd417e5b0816ec1a3078a506f9a5509367ed573168f9c152151035a80d1
```

The schema binds the canonical code/tree identity, protocol/prompt/corpus hashes, all six axis scores, aggregate score, safety failures, role-gate outcomes, operational metrics, negative results, role results, and artifact-manifest digest. A later report must also bind the separately materialized corpus digest and exact count 240.

## Acceptance mapping

| Acceptance item | Repair-2 result artifact |
|---|---|
| 16 — frozen R2-compatible corpus across six axes | `corpus-specification.json` plus `protocol-freeze.md` |
| 17 — exact corpus count and deterministic corpus digest | count `240`; readiness corpus-spec digest `73a236...d65c3` |
| 18 — frozen system/task prompts and execution semantics | `task-prompts.json` plus `protocol-freeze.md` |
| 19 — metrics/weights | `protocol-freeze.md` |
| 20 — role thresholds/tie-break/resource/NO_SELECTION | `protocol-freeze.md` and ADR-0034 |
| 21 — latency/token/cost/memory accounting | `protocol-freeze.md` and `reproducibility-schema.md` |
| 22 — reproducibility/raw/normalized/error/exclusion/report/artifact schemas | `reproducibility-schema.md` plus `report-schema.json` |
| 23 — prompt/protocol and report-schema digests | `092858...66ef1` and `64962c...a80d1` |

## Fail-closed boundary

The readiness corpus-spec digest is **not** represented as the digest of future case bytes. `FD-MESC-BT-EXEC-1` remains inactive until the exact materialized 240-item JSONL corpus is committed, independently R2-audited, and its own SHA-256 is bound with exact runtime/hardware/access state. No model may be loaded or queried merely because the readiness specification is complete.
