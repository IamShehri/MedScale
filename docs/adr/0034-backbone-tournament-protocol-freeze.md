# ADR-0034 — Freeze the MESC Backbone Tournament evaluation protocol

- **Status:** Accepted by Founder for this bounded readiness result; effective only if this exact result package is canonically merged
- **Date:** 2026-08-20
- **Decision:** `MESC-BT-PROTOCOL-V1`

## Context

`FD-MESC-BT-READINESS-REPAIR-2` permits completion of the six-axis synthetic/hand-authored corpus and protocol freeze after the roster clears. It grants no weight access, gated-term acceptance, inference, training, retrieval, or tournament execution. R6 requires these experiment-defining choices to be frozen before model outputs.

## Decision

1. Freeze the exact 240-item deterministic-synthetic corpus (40 items per mandatory axis). Its logical UTF-8 LF JSONL is stored as deterministic gzip `materialized-corpus.jsonl.gz` (`mtime=0`); `corpus-manifest.json` binds both storage and decompressed digests.
2. Freeze six separate 40-item gold-key JSONL shards. Only each corpus record's `payload` is prompt input; metadata and gold keys are prohibited from candidate prompts.
3. Freeze `MESC-BT-PROMPTS-V2`, the six-key normalized-output JSON Schema, strict parser/failure mapping, `MESC-BT-SCORING-V1`, and `MESC-BT-REPORT-V1`.
4. Scoring retains all 240 items in denominators; protocol failures score zero. Axis scores are means of 40 items; aggregate weights are 25/20/15/20/10/10. Compact and Flagship/Reasoner gates remain as encoded in `scoring-contract.json`.
5. Tie order is safety → evidence fidelity → medical reasoning → lower peak VRAM → lower median latency. A remaining exact tie is terminal `NO_SELECTION / EXACT_TIE_AFTER_ALL_FROZEN_TIE_BREAKERS`; no post-output rule may be added.
6. Freeze deterministic decoding, limits, timeout/retry semantics, no tools/retrieval/web/function calls, and no candidate-specific semantic prompt optimization as encoded in `protocol-config.json`.

## Exact bindings

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

## Consequences

The corpus, parser, scoring, failure semantics, gates, and terminal tie behavior are fixed before any model output. No winner exists. A later `FD-MESC-BT-EXEC-1` must separately bind runtime, hardware, access/gating operator authorization, run bounds, artifact destinations, review gates, and canonical adoption.
