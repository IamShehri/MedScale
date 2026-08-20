# Repair-2 Acceptance Reconciliation

Status: **NORMATIVE RESULT-PACKAGE RECONCILIATION CANDIDATE**

The specific Repair-2 contract requires a frozen R2-compatible corpus (item 16) and exact corpus count/digest (item 17). The activated Repair-2 founder authorization explicitly permits completing that corpus and creating its digest during this episode after the roster gate passes. This package therefore materializes the deterministic-synthetic corpus during readiness **without executing it**.

This is not execution authority. A future `FD-MESC-BT-EXEC-1` must use the same frozen corpus identity, re-attest its bytes, and bind deterministic R2-provenance and full spec/manifest-conformance audit artifacts before any prompt serialization. It may not substitute another corpus under the same protocol ID.

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

| Acceptance item | Bound artifact |
|---|---|
| 16 | `materialized-corpus.jsonl.gz` + verified decompressed 240-line JSONL, `corpus-specification.json`, `corpus-manifest.json` |
| 17 | count `240`; logical corpus SHA-256 `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd` |
| 18 | `task-prompts.json`, `normalized-output-schema.json`, `parser-contract.json`, `protocol-config.json` |
| 19 | `scoring-contract.json` + `scoring-keys-A.jsonl` … `scoring-keys-F.jsonl` |
| 20 | `scoring-contract.json`, `protocol-config.json`, ADR-0034 |
| 21 | `protocol-freeze.md`, `reproducibility-schema.md`, `report-schema.json`, `report-validation-contract.json` |
| 22 | normalized/parser/reproducibility/report/validator contracts, including exact-binding, accounting, uniqueness, gate-recomputation, and role-selection invariants |
| 23 | prompt/protocol `bc5d85125c942695d8c191920a635c3cea28a68d31e3fe6de1092dd42c8bc92a`; report schema `93b8251fd5c7f650bd806aa144c62a7c149720af848a74acbd0127f488384ac9`; report validator `f02e0217d5cc8120a0047b6a4d71456452d598a4b948331c536e76ca6dc3118e` |

Only `payload` is candidate input; gold keys never enter prompts. Parser failures, schema failures, per-item scoring, axis aggregation, gate recomputation, role selection, and terminal exact-tie `NO_SELECTION` are deterministic and pre-output.

This closes readiness only after canonical merge/post-merge verification. It does not activate model access or `FD-MESC-BT-EXEC-1`.
