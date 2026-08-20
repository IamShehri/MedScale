# MESC Backbone Tournament — Readiness Repair-2 Result

Status: **RESULT CANDIDATE — EFFECTIVE ONLY AFTER CANONICAL MERGE AND POST-MERGE VERIFICATION**

Authority: `FD-MESC-BT-READINESS-REPAIR-2`

Episode base: `53f517e57602b1b721fce6edae71d6f9e64d3bc6` / tree `aff1c0ba76cd9959141c7208d8efb14b37228f16`.

Repair-2 resolved the Apertus v1.5 AUP blocker with exact public artifact binding (`53794` bytes; SHA-256 `424b0a0d24ee1369f9a8614d9e4c7eb0fc3ee8a9ad7ece39baea3a83f0d4ba76`; authoritative/computed Git blob `8ddd8e25b6672340dd4f921ba623578571a65526`). All four non-empty candidates were refreshed and remain `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`; challenger remains `EMPTY`.

## Frozen readiness artifacts

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

The exact materialized corpus contains 240 deterministic-synthetic records, 40 per axis. `materialized-corpus.jsonl.gz` deterministically decompresses to the bound logical JSONL. Under the specific Repair-2 authorization these bytes are frozen during readiness but are **not executed**. Gold keys remain in `scoring-keys-A.jsonl` … `scoring-keys-F.jsonl`; prompts serialize only `payload`.

Machine-readable `normalized-output-schema.json`, `parser-contract.json`, `scoring-contract.json`, `protocol-config.json`, `report-schema.json`, and `report-validation-contract.json` close parser/scoring/tie/report-integrity ambiguities. The validator adds exact artifact bindings, distinct candidate IDs/revisions, error accounting, gate recomputation, winner linkage, and exact-tie membership. Remaining exact ties yield `NO_SELECTION`.

A later execution authorization must re-attest these same corpus bytes and bind PASS R2-provenance plus full corpus-spec/manifest-conformance audit artifacts before model access or prompt serialization.

## Non-authority

No model was downloaded, opened, loaded, queried, ranked, trained, or used for retrieval. No gated access or terms were requested/accepted. `FD-MESC-BT-EXEC-1` remains inactive.
