# FD-MESC-BT-EXEC-1 — Execution Authorization Candidate

Status: **DRAFT / INACTIVE / NOT AUTHORIZED**

A future execution package may reference the frozen Repair-2 artifacts below but cannot inherit authority from them.

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

## Mandatory pre-activation bindings

Before activation it must bind all of the following, fail-closed:

1. exact canonical MESC commit/tree;
2. the selected subset (>=2 distinct) of the four admitted candidate IDs with their exact immutable revisions, plus tokenizer/processor/custom-code revisions;
3. exact hardware/provider/runtime/precision state and non-negative numeric peak-VRAM/latency measurement capability required by the frozen tie policy;
4. explicit Founder authorization for any gated-access request or terms acceptance;
5. bounded run attempts, artifact destinations, and exact raw/normalized evidence identities;
6. the already-frozen corpus storage/logical/count/spec/manifest identities above — **no corpus substitution or rematerialization**;
7. a deterministic **R2 provenance audit artifact** with `RESULT=PASS` and its SHA-256, proving the frozen source/prohibition and payload/gold-separation constraints;
8. a deterministic **corpus specification/manifest conformance audit artifact** with `RESULT=PASS` and its SHA-256, proving all 240 IDs/order/axes/archetypes/difficulty bands/answer-state rules/task-template bindings/payload integrity/R2 constraints;
9. `MESC-BT-REPORT-VALIDATION-V1` and the exact report-schema digest above, including canonical report `item_id` membership against the same 240-item corpus;
10. exact-head CI/CodeQL, fresh independent review, zero unresolved blocking threads, Ready/post-Ready gates, expected-head merge protection, and post-merge verification.

Both corpus audits must PASS **before any candidate prompt serialization or model access**. Infrastructure retries are attempt-level evidence only; every corpus item has one terminal disposition.

Current state:

```text
FD-MESC-BT-EXEC-1 = INACTIVE_CANDIDATE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
