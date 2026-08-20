# MESC Backbone Tournament — Execution Preflight 1

Status: **FOUNDER-AUTHORIZATION CANDIDATE / NO EXECUTION AUTHORITY**

Date: 2026-08-20

Decision identity: `FD-MESC-BT-EXEC-1-PREFLIGHT`

Canonical base at proposal time:

```text
MAIN_SHA = 0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3
MAIN_TREE = 60e900daecea1cb9e64db95314bf9358387072b7
PR_130 = MERGED / CANONICAL
BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE
```

## Purpose

This package authorizes only the deterministic pre-execution evidence work required before `FD-MESC-BT-EXEC-1` can be proposed for activation.

It does **not** authorize model access, prompt serialization, inference, generation, or tournament execution.

The episode may produce only:

1. a deterministic R2 provenance audit over the already-frozen 240-item corpus;
2. a deterministic corpus-specification/manifest conformance audit over the same frozen corpus;
3. exact audit artifact SHA-256 bindings;
4. a fail-closed execution-binding inventory identifying what is still unbound;
5. an inactive `FD-MESC-BT-EXEC-1` activation candidate only if all preflight acceptance criteria pass.

## Frozen inputs

The preflight must consume the exact canonical Repair-2 artifacts without substitution or rematerialization:

```text
CORPUS_SPEC_SHA256 = 49f554d57e29da4b1d04223d43f1630731e5f8c9b72e7a1e15f959e38c00643b
MATERIALIZED_CORPUS_ITEM_COUNT = 240
MATERIALIZED_CORPUS_SHA256 = 48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd
MATERIALIZED_CORPUS_GZIP_SHA256 = 667cd68e5ccc9356321eb5857c6e9203e1320ec33d866ccf514411c211ceb632
CORPUS_MANIFEST_SHA256 = 201fa1351923a72097ff7e467b6dce2eb8bd0cfa1e88c73157788f77dd89e745
SCORING_KEYS_SHA256 = bb3524bc8dd1f05bad433c664ac3c48a5110939ac78b5ffa2ad8853f944c6318
TASK_PROMPT_BUNDLE_SHA256 = 54d9da5cf3dad58c0bf9fb28761c15d8f82568013895b8467f1cb7d532c314b7
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
NORMALIZED_OUTPUT_SCHEMA_SHA256 = 3e0a1523af45a61db77e3287a3333361fa26411f521321bbef0804dec7a63ed4
PARSER_CONTRACT_SHA256 = 9905096b491ddc3bce2b5d668c1f8726f638dde9dba383ac1bb755f1b6b42071
REPORT_VALIDATION_CONTRACT_SHA256 = c68fcac507e4ebc164632370d2392631b9fec9c388369eb5b8bfa495e5877c1a
SCORING_CONTRACT_SHA256 = a61471d467521b59eb62ee2825d23fa15891bb45a664360aaf2e4ef5882c7d40
PROTOCOL_CONFIG_SHA256 = 097cdd11f5389203cf432760ec316a78b12d157c0676477de69dde707e058203
PROMPT_PROTOCOL_SHA256 = a2a42aef340e27f9396b40810999d5f2c4136af467ce27ee9e3c149e3257c89c
REPORT_SCHEMA_SHA256 = cb3fc506b41cc6236959bb4a89bce249db13c99aeb0c7178ff233f6de44e026d
```

## Hard boundary

Until a later `FD-MESC-BT-EXEC-1` package is separately canonically adopted:

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
