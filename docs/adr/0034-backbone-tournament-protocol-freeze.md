# ADR-0034 — Freeze the MESC Backbone Tournament evaluation protocol

- **Status:** Accepted by Founder for this bounded readiness result; effective only if this exact result package is canonically merged
- **Date:** 2026-08-20
- **Decision:** `MESC-BT-PROTOCOL-V1`

## Context

The specific activated authority `FD-MESC-BT-READINESS-REPAIR-2` permits completion of the six-axis synthetic/hand-authored corpus and its deterministic digest during Repair-2 after the roster clears. That specific Repair-2 authority controls over the earlier generic readiness/execution staging language. Materializing these synthetic bytes is readiness evidence only: it grants no weight access, gated-term acceptance, inference, training, retrieval, or tournament execution. R6 requires experiment-defining choices to be frozen before any model output.

## Decision

1. Freeze the exact 240-item deterministic-synthetic corpus (40 items per mandatory axis). Its logical UTF-8 LF JSONL is stored as deterministic gzip `materialized-corpus.jsonl.gz` (`mtime=0`); `corpus-manifest.json` binds storage and decompressed identities.
2. Freeze six separate 40-item gold-key JSONL shards. Only each corpus record's `payload` is model-visible; metadata and gold keys are prohibited from candidate prompts.
3. Freeze `MESC-BT-PROMPTS-V2`, the normalized-output JSON Schema, strict parser/failure mapping, `MESC-BT-SCORING-V1`, `MESC-BT-REPORT-V1`, and `MESC-BT-REPORT-VALIDATION-V1`.
4. Scoring retains all 240 items in denominators; protocol failures score zero. Axis scores are means of 40 items; aggregate weights are 25/20/15/20/10/10. Compact and Flagship/Reasoner gates remain as encoded in `scoring-contract.json`.
5. Tie order is safety → evidence fidelity → medical reasoning → lower peak VRAM → lower median latency. `peak_vram_mb` and `median_latency_ms` must be non-negative numeric values for every candidate participating in role selection. Missing/null peak VRAM is report nonconformance, not an ordering value. A remaining exact tie is terminal `NO_SELECTION / EXACT_TIE_AFTER_ALL_FROZEN_TIE_BREAKERS`.
6. `report-validation-contract.json` is normative for cross-record and arithmetic invariants that JSON Schema cannot express: exact activated bindings, unique candidate identities, terminal error accounting, gate recomputation, winner↔candidate/gate linkage, and exact-tie membership.
7. A future `FD-MESC-BT-EXEC-1` must re-attest the already-frozen corpus bytes and additionally bind two pre-execution PASS artifacts: an R2 provenance audit and a complete corpus-spec/manifest conformance audit. It may not substitute or silently rematerialize a different corpus.
8. Freeze deterministic decoding, limits, timeout/retry semantics, no tools/retrieval/web/function calls, and no candidate-specific semantic prompt optimization as encoded in `protocol-config.json`.

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
REPORT_VALIDATION_CONTRACT_SHA256 = f02e0217d5cc8120a0047b6a4d71456452d598a4b948331c536e76ca6dc3118e
SCORING_CONTRACT_SHA256 = 8df9d1ef50ca5f56a38f68e85b1fec636b1386d7e94e96f521fb3327e4ef3e5f
PROTOCOL_CONFIG_SHA256 = 9648deca4d7ae607d3d264c44e641d54982e670eb763638594b2d6d004fb7046
PROMPT_PROTOCOL_SHA256 = bc5d85125c942695d8c191920a635c3cea28a68d31e3fe6de1092dd42c8bc92a
REPORT_SCHEMA_SHA256 = 93b8251fd5c7f650bd806aa144c62a7c149720af848a74acbd0127f488384ac9
```

## Digest graph

`report-validation-contract.json` is independent of protocol/report hashes. `scoring-contract.json` binds its digest. `protocol-config.json` binds the validator and scoring digests plus `REPORT_SCHEMA_ID`, but intentionally does not embed the report-schema digest, avoiding a hash cycle. `report-schema.json` binds the exact protocol/scoring/validator and other frozen static digests. Its own digest is separately frozen above and must be matched to the exact `FD-MESC-BT-EXEC-1` activation binding by the normative validator.

## Consequences

The corpus, parser, scoring, validation, failure semantics, gates, and terminal tie behavior are fixed before model output. No winner exists. `FD-MESC-BT-EXEC-1` remains separate, inactive, and must additionally bind exact runtime, hardware, access/gating authorization, corpus audit artifacts, run bounds, artifact destinations, review gates, and canonical adoption.
