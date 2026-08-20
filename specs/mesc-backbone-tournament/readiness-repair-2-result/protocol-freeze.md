# MESC Backbone Tournament — Protocol Freeze

Status: **FROZEN DESIGN CANDIDATE — NO EXECUTION AUTHORITY**

Protocol ID: `MESC-BT-PROTOCOL-V1`

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

## Corpus and prompt projection

The verified decompressed corpus has exactly 240 deterministic-synthetic JSONL records, 40 per axis. Only the `payload` object is serialized into `{{ITEM_PAYLOAD}}`. Gold-key shards and corpus metadata are never prompt input.

## Parsing

`parser-contract.json` is normative: one UTF-8 JSON object only; duplicate keys, Markdown fences, invalid JSON, oversize output, or trailing non-whitespace are `PARSE_FAILURE`; normalized-schema or cross-item evidence violations are `SCHEMA_FAILURE`; no semantic repair or semantic retry occurs.

## Scoring and gates

`scoring-contract.json` is normative. Each item scores 0–100 from exact state/answer/evidence/control comparisons; protocol failures score zero and remain in denominators. Each axis is the arithmetic mean of 40 items (decimal half-up, 2dp); the aggregate uses weights 25/20/15/20/10/10. Compact/Flagship gates and critical-safety semantics are frozen there.

Tie order: safety → evidence fidelity → medical reasoning → lower peak VRAM → lower median latency. Remaining exact tie => `NO_SELECTION / EXACT_TIE_AFTER_ALL_FROZEN_TIE_BREAKERS`. No additional post-output tie-breaker.

## Equal treatment

Single-turn; input 8192; output 1024; no tools/retrieval/web/function calls; greedy decoding; temperature 0; top-p 1; seed 0 where accepted; timeout 180s; one identical infrastructure retry; zero semantic/parse/schema retries; no candidate-specific semantic optimization; hidden reasoning is not scored. Exact details are canonical in `protocol-config.json`.

## Boundary

No corpus item has been executed. `BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED`.
