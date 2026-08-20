# MESC Backbone Tournament — Reproducibility and Artifact Contract

Status: **FROZEN READINESS CONTRACT — FUTURE EXECUTION ONLY**

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

A future separately authorized run must bind exact MESC commit/tree, exact candidate/model/processor/runtime revisions, hardware/provider identity, protocol/prompt/corpus/schema/validator digests, access evidence, start/end timestamps, and every raw/normalized per-item artifact hash. No executable identity may float.

## Pre-prompt corpus verification

Before reading or serializing any case:

1. verify `materialized-corpus.jsonl.gz` storage SHA-256;
2. decompress and verify logical SHA-256 `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd`;
3. verify exactly 240 canonical JSONL records and 240 unique IDs in canonical order;
4. verify exactly 40 records per axis A–F;
5. deterministically validate every record against `corpus-specification.json` and `corpus-manifest.json`, including archetype assignment, difficulty band, task-template binding, payload integrity, evidence references, expected answer-state rules, and R2 prohibitions;
6. deterministically validate provenance: synthetic/hand-authored only, zero Pilot-01/PHI/patient/clinician/product-telemetry/credentialed-clinical/external-benchmark content, and payload-only model visibility with zero gold leakage;
7. persist two independent audit artifacts — `R2_PROVENANCE_AUDIT=PASS` and `CORPUS_SPEC_CONFORMANCE_AUDIT=PASS` — and bind both SHA-256 values in the activated `FD-MESC-BT-EXEC-1` package.

If either audit fails, stop before model access/prompt serialization.

Read the matching corpus record and serialize **only** `payload` into the frozen task template. Never expose gold-key shards or metadata.

## Per-item and aggregate accounting

Every corpus item contributes exactly one final terminal disposition after the frozen infrastructure-retry policy: completed, or exactly one of `TIMEOUT`, `RUNTIME_FAILURE`, `GENERATION_FAILURE`, `PARSE_FAILURE`, `SCHEMA_FAILURE`, `SAFETY_FAILURE`. Retry attempts do not create extra terminal counts.

For each candidate:

```text
items_attempted = 240
items_completed + errors.total = 240
errors.total = TIMEOUT + RUNTIME_FAILURE + GENERATION_FAILURE + PARSE_FAILURE + SCHEMA_FAILURE + SAFETY_FAILURE
len(exclusions) = errors.total
```

Every failed item ID appears exactly once in `exclusions`, its class matches the typed counter, no completed item is excluded, and all counters are 0..240.

Per-item records preserve raw output separately from normalized output and record candidate/item identity, prompt/raw hashes, parse status, normalized state, scoring components, critical-safety result, latency/tokens/VRAM, retry evidence, and terminal error class.

## Report validation and role selection

Aggregate output must first validate against `MESC-BT-REPORT-V1`, then against `MESC-BT-REPORT-VALIDATION-V1`. The validator must:

- verify exact static and activation-bound digests;
- require unique candidate IDs/revisions and exact admitted revision mapping;
- recompute aggregate scores and both role gates from frozen scoring rules;
- enforce numeric non-negative `peak_vram_mb`/latency for selection;
- require every WINNER to resolve to exactly one reported candidate whose corresponding role gate is PASS;
- recompute the frozen tie order and exact-tie membership;
- reject any contradictory accounting or substituted artifact identity.

No performance/winner claim exists until R5/R7 execution evidence is separately authorized, validator-clean, independently reviewed, and canonically committed.
