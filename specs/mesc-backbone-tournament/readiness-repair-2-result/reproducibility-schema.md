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
SCORING_CONTRACT_SHA256 = d02f84cdc6c6609f795a909a7d4878d9193f47bdcbcb1719f9645ac7e258a63f
PROTOCOL_CONFIG_SHA256 = 01bd6fdfbf5cfb883195c1aac9d05da7dd34f7a507ce8e81db201f591ae265b6
PROMPT_PROTOCOL_SHA256 = b93fbc84ce3742410074727850f7d69dd5df4af0b3d8a56933381f641592bf77
REPORT_SCHEMA_SHA256 = 1f819807b8f785602ba04a0130cc6922c056a5933598a8eddc6af41d765c770c
```

A future separately authorized run must bind exact MESC commit/tree, candidate/model/processor/runtime revisions, hardware/provider identity, protocol/prompt/corpus/schema digests, access evidence, start/end timestamps, and every raw/normalized per-item artifact hash. No executable identity may float.

Before reading cases, verify `materialized-corpus.jsonl.gz` storage SHA-256, decompress it, verify logical SHA-256 `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd`, count exactly 240 canonical JSONL records, and validate IDs/axes. Read the matching record and serialize **only** `payload` into the frozen task template. Never expose gold-key shards or metadata.

Per-item records must preserve raw output separately from normalized output and record candidate/item identity, prompt/raw hashes, parse status, normalized answer state, scoring components, critical-safety result, latency/tokens/VRAM, and error class. Aggregate output must validate against `MESC-BT-REPORT-V1`, including attempted/completed counts, typed errors/exclusions/negative results, six axis scores, aggregate/gates, operational metrics, role outcomes, and all frozen digests.

No performance or winner claim exists until R5/R7 execution evidence is separately authorized and committed.
