# Repair-2 Acceptance Reconciliation

Status: **NORMATIVE RESULT-PACKAGE RECONCILIATION CANDIDATE**

The specific Repair-2 contract requires a frozen R2-compatible corpus (item 16) and exact corpus count/digest (item 17). This package therefore materializes the corpus during readiness without executing it.

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
SCORING_CONTRACT_SHA256 = d02f84cdc6c6609f795a909a7d4878d9193f47bdcbcb1719f9645ac7e258a63f
PROTOCOL_CONFIG_SHA256 = 01bd6fdfbf5cfb883195c1aac9d05da7dd34f7a507ce8e81db201f591ae265b6
PROMPT_PROTOCOL_SHA256 = b93fbc84ce3742410074727850f7d69dd5df4af0b3d8a56933381f641592bf77
REPORT_SCHEMA_SHA256 = 1f819807b8f785602ba04a0130cc6922c056a5933598a8eddc6af41d765c770c
```

| Acceptance item | Bound artifact |
|---|---|
| 16 | `materialized-corpus.jsonl.gz` + verified decompressed 240-line JSONL, `corpus-specification.json`, `corpus-manifest.json` |
| 17 | count `240`; logical corpus SHA-256 `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd` |
| 18 | `task-prompts.json`, `normalized-output-schema.json`, `parser-contract.json`, `protocol-config.json` |
| 19 | `scoring-contract.json` + `scoring-keys-A.jsonl` … `scoring-keys-F.jsonl` |
| 20 | `scoring-contract.json`, `protocol-config.json`, ADR-0034 |
| 21 | `protocol-freeze.md`, `reproducibility-schema.md`, `report-schema.json` |
| 22 | normalized/parser/reproducibility/report contracts |
| 23 | prompt/protocol `b93fbc84ce3742410074727850f7d69dd5df4af0b3d8a56933381f641592bf77`; report schema `1f819807b8f785602ba04a0130cc6922c056a5933598a8eddc6af41d765c770c` |

Only `payload` is candidate input; gold keys never enter prompts. Parser failures, schema failures, per-item scoring, axis aggregation, role gates, and terminal exact-tie `NO_SELECTION` are deterministic and pre-output.

This closes readiness only. It does not activate model access or `FD-MESC-BT-EXEC-1`.
