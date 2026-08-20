# MESC Backbone Tournament — Repair-2 Readiness Verdict

Status: **TERMINAL VERDICT CANDIDATE — EFFECTIVE ONLY AFTER CANONICAL MERGE AND POST-MERGE VERIFICATION**

Authority: `FD-MESC-BT-READINESS-REPAIR-2`

Base: `53f517e57602b1b721fce6edae71d6f9e64d3bc6` / tree `aff1c0ba76cd9959141c7208d8efb14b37228f16`. Apertus exact AUP blocker is resolved; all four non-empty roster candidates are refreshed/admitted; challenger is `EMPTY`; no non-empty candidate is `BLOCKED`; roster gate passes. R2/R3/R5/R6/R7 boundaries remain preserved.

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
REPORT_VALIDATION_CONTRACT_SHA256 = f02e0217d5cc8120a0047b6a4d71456452d598a4b948331c536e76ca6dc3118e
SCORING_CONTRACT_SHA256 = 8df9d1ef50ca5f56a38f68e85b1fec636b1386d7e94e96f521fb3327e4ef3e5f
PROTOCOL_CONFIG_SHA256 = 9648deca4d7ae607d3d264c44e641d54982e670eb763638594b2d6d004fb7046
PROMPT_PROTOCOL_SHA256 = bc5d85125c942695d8c191920a635c3cea28a68d31e3fe6de1092dd42c8bc92a
REPORT_SCHEMA_SHA256 = 93b8251fd5c7f650bd806aa144c62a7c149720af848a74acbd0127f488384ac9
```

Acceptance items 16–23 are bound by concrete synthetic corpus bytes/count, separate gold keys, prompts, strict parser/normalized schema, deterministic scoring/gates/tie result, normative cross-record report validation, accounting/reproducibility contracts, protocol digest, and report-schema digest.

The specific Repair-2 authorization permits the materialized deterministic-synthetic corpus to be frozen during readiness. This is not execution authority. `FD-MESC-BT-EXEC-1` must re-attest the same corpus and additionally bind PASS R2-provenance and full spec/manifest-conformance audit artifacts before prompt serialization.

If and only if this exact result head passes exact-head CI/CodeQL, fresh independent exact-head review, zero unresolved blocking threads, Ready/post-Ready gates, expected-head merge, and post-merge verification, record:

```text
FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED
REUSABLE = NO
BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```

No model access, inference, generation, tournament execution, training, retrieval, Pilot-01 inspection, PHI/patient/product/telemetry data, challenger addition, or downstream implementation occurred.
