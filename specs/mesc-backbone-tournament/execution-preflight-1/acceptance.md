# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **CANDIDATE ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-20

The preflight is complete only if every requirement below is satisfied on one exact canonical input state.

## A. Canonical ancestry and complete input identity

1. canonical authorization base SHA is recorded and contains PR #130 in ancestry;
2. canonical authorization base tree is recorded;
3. every frozen Repair-2 artifact consumed by the audit is identified by repository path and Git blob SHA;
4. **all** frozen Repair-2 bindings listed in the preflight README are mandatory and must be reproduced; none is optional or conditionally applicable. Exact verification includes:
   - `corpus-specification.json` bytes against `CORPUS_SPEC_SHA256`;
   - `materialized-corpus.jsonl.gz` bytes against `MATERIALIZED_CORPUS_GZIP_SHA256`;
   - decompressed logical corpus bytes against `MATERIALIZED_CORPUS_SHA256` and exact count 240;
   - `corpus-manifest.json` bytes against `CORPUS_MANIFEST_SHA256`;
   - every scoring-key shard by path/Git blob/manifest SHA-256/count/byte length and their frozen logical concatenation against `SCORING_KEYS_SHA256`;
   - `task-prompts.json` exact bytes against `TASK_PROMPT_BUNDLE_SHA256`;
   - the exact system-prompt string according to the frozen derivation against `SYSTEM_PROMPT_SHA256`;
   - `normalized-output-schema.json` exact bytes against `NORMALIZED_OUTPUT_SCHEMA_SHA256`;
   - `parser-contract.json` exact bytes against `PARSER_CONTRACT_SHA256`;
   - `report-validation-contract.json` exact bytes against `REPORT_VALIDATION_CONTRACT_SHA256`;
   - `scoring-contract.json` exact bytes against `SCORING_CONTRACT_SHA256`;
   - `protocol-config.json` exact bytes against `PROTOCOL_CONFIG_SHA256`;
   - the frozen composite prompt/protocol derivation against `PROMPT_PROTOCOL_SHA256`;
   - `report-schema.json` exact bytes against `REPORT_SCHEMA_SHA256`;
5. no corpus substitution, regeneration, rematerialization, floating ref, or omitted frozen contract binding is permitted.

Any missing path, blob identity, digest reproduction, or derivation proof => `BLOCKED`.

## B. Canonical audit serialization and SHA-256 rule

Both audit JSON artifacts use exactly the same serialization rule.

1. The audit object MUST NOT contain any field that stores its own file SHA-256.
2. The audit file is the exact hash preimage. It is serialized as one RFC 8259 JSON object using:
   - UTF-8 encoding without BOM;
   - Unicode strings normalized to NFC before serialization;
   - object keys sorted lexicographically by Unicode code point at every object level;
   - array order preserved exactly as defined by the audit contract;
   - separators exactly `,` and `:` with no insignificant whitespace;
   - JSON escaping only as required by RFC 8259; non-ASCII Unicode is encoded directly as UTF-8, not `\u`-escaped unless required by JSON syntax;
   - booleans as `true`/`false`, null as `null`;
   - audit numeric values restricted to base-10 integers, with no leading plus sign, no leading zeros except `0`, and no floating-point values;
   - **no trailing newline** and no bytes before or after the JSON object.
3. `SHA256(file_bytes)` over the complete audit file bytes is the artifact SHA-256.
4. The resulting audit SHA-256 is published only in `preflight-result-manifest.json`; it is never inserted back into the audit file.
5. The exact canonicalization rule identifier is `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` and must be recorded in each audit.

Any serializer that cannot reproduce these exact bytes => `BLOCKED`.

## C. R2 provenance audit

`r2-provenance-audit.json` may report `result = PASS` only if all are true:

1. exactly 240 model-visible synthetic/hand-authored payload records are present;
2. Pilot-01 content is absent;
3. real patient/clinician records, PHI, product telemetry, credentialed clinical data, and external benchmark examples are absent;
4. every payload is self-contained synthetic/hand-authored material under the frozen R2 policy;
5. model-visible payload contains no gold answer/scoring-key fields;
6. every evidence reference used by a scoring key resolves to evidence present in that item's payload;
7. the artifact records deterministic input identities, check counts, explicit failure records, canonicalization rule ID, and result.

Any unresolved provenance ambiguity or prohibited-source indication => `BLOCKED`.

## D. Corpus specification / manifest conformance audit

`corpus-conformance-audit.json` may report `result = PASS` only if all are true:

1. decompressed logical corpus SHA-256 equals `48fba9119f0170eb40775c75f12916e277cb3953abe22357e0b22497dadbbebd`;
2. compressed storage SHA-256 equals `667cd68e5ccc9356321eb5857c6e9203e1320ec33d866ccf514411c211ceb632`;
3. logical corpus count is exactly 240;
4. canonical item IDs are exactly `BT-A-001..040` through `BT-F-001..040`, each once, in frozen order;
5. each axis has exactly 40 records;
6. archetype assignment and difficulty bands match `corpus-specification.json`;
7. each item uses the frozen task-template binding for its axis;
8. expected answer-state/scoring-key fields conform to the frozen schemas/contracts;
9. logical scoring-key count is exactly 240 and its SHA-256 equals `bb3524bc8dd1f05bad433c664ac3c48a5110939ac78b5ffa2ad8853f944c6318`;
10. each manifest shard count/hash/byte-length binding is reproduced;
11. no duplicate, missing, extra, reordered, or malformed item is accepted;
12. the artifact records deterministic input identities, check counts, explicit failure records, canonicalization rule ID, and result.

Any mismatch => `BLOCKED`.

## E. Complete preflight result-package binding without digest cycles

The four unconditional core outputs are:

1. `r2-provenance-audit.json`;
2. `corpus-conformance-audit.json`;
3. `execution-binding-inventory.md`;
4. `preflight-verdict.md`.

If a successor is produced, `execution-authorization-candidate.md` is a conditional fifth bound result artifact. The result package must also contain `preflight-result-manifest.json`.

To avoid a verdict/manifest digest cycle while binding the successor bytes, construct the binding in this exact order:

1. Compute the exact SHA-256 of the two audit files under Section B.
2. Compute `SHA256(file_bytes)` for `execution-binding-inventory.md`, whose file bytes MUST be UTF-8 without BOM, LF line endings, and exactly one final LF.
3. Determine the successor-candidate binding before constructing the manifest core:
   - if Sections A–D pass and the execution-binding inventory is complete and truthful for a provisional `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` path, render exactly one `FD-MESC-BT-EXEC-1-CANDIDATE-V2` at `execution-authorization-candidate.md` under the preflight result directory, encoded as UTF-8 without BOM, LF line endings, and exactly one final LF; compute its exact full-file SHA-256 and byte length;
   - otherwise no successor-candidate file may be present and the binding value is `null`;
   - provisional rendering grants no authority and is valid only as an input to the result-package binding.
4. Construct `manifest_binding_core` as canonical JSON under `MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` containing exactly:
   - `manifest_id = MESC-BT-PREFLIGHT-RESULT-MANIFEST-V1`;
   - exact authorization decision ID;
   - exact canonical authorization merge SHA and tree;
   - exact Repair-2 frozen input digest map;
   - the three already-known artifact paths and SHA-256 values for both audits and the execution-binding inventory;
   - `verdict_path = preflight-verdict.md`;
   - `successor_candidate = null` when no successor exists, otherwise an object containing exactly `id = FD-MESC-BT-EXEC-1-CANDIDATE-V2`, its exact result-relative path, exact SHA-256, and exact byte length.
5. `MANIFEST_BINDING_CORE_SHA256 = SHA256(canonical_manifest_binding_core_bytes)`.
6. Generate `preflight-verdict.md` in UTF-8 without BOM, LF endings, exactly one final LF, and require it to contain the exact `MANIFEST_BINDING_CORE_SHA256`, manifest ID, authorization merge SHA/tree, and terminal preflight state.
7. Compute the exact full-file SHA-256 of `preflight-verdict.md`.
8. Generate `preflight-result-manifest.json` as canonical JSON under Section B. It must contain the complete `manifest_binding_core` object, its SHA-256, and an `artifacts` map containing the exact path, SHA-256, and byte length of all four unconditional core outputs plus the successor candidate when `successor_candidate` is non-null.
9. If any later binding, receipt, or acceptance check forces terminal `BLOCKED` after provisional candidate rendering, remove the successor-candidate file, set `successor_candidate = null`, and rebuild the binding core, verdict, and manifest from the resulting blocked package; stale hashes are invalid.
10. The manifest MUST NOT contain its own file SHA-256. Its exact full-file SHA-256 is computed externally and published in `consumption-receipt.json` and in the preflight result PR description.

A present-but-unbound successor candidate, missing/mismatched core hash, output hash, byte length, path, or verdict reference => `BLOCKED`.

## F. One-shot activation receipt, durable consumption, and replay rejection

The authorization episode requires a receipt before any audit begins.

1. After this authorization PR is canonically merged and post-merge verified, derive `ACTIVATION_RECEIPT_ID` as SHA-256 of canonical JSON under Section B containing exactly:
   - `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`;
   - canonical authorization merge SHA;
   - canonical authorization merge tree;
   - the four authorization-package repository paths and their Git blob SHAs;
   - `receipt_version = MESC-BT-PREFLIGHT-RECEIPT-V1`.
2. Before starting the episode, search canonical history and open/closed preflight-result PRs for this decision ID and receipt ID. If a canonical `consumption-receipt.json` already records this receipt as `CONSUMED`, or a different receipt is associated with the same authorization merge SHA/tree, replay is rejected => `BLOCKED`.
3. The result branch must contain `activation-receipt.json` before audit-result publication. It must exactly reproduce the receipt preimage, `ACTIVATION_RECEIPT_ID`, and `state = ISSUED`. Missing or mismatched receipt => `BLOCKED`.
4. A successful result package must include `consumption-receipt.json` containing the same receipt ID/preimage, `state = CONSUMED`, and the exact SHA-256 of `preflight-result-manifest.json`.
5. Canonical merge of the result package is the durable consumed-state transition. After that merge, any attempt to reuse `FD-MESC-BT-EXEC-1-PREFLIGHT` or the same receipt is rejected fail-closed.
6. A failed/blocked episode must still preserve its receipt and negative evidence; it may not silently restart under the same authorization. A new attempt requires a new separately reviewed founder authorization.

## G. Remaining execution-binding inventory and single successor candidate

The result must explicitly report the status of every `FD-MESC-BT-EXEC-1` mandatory pre-activation binding:

- exact canonical code SHA/tree;
- selected candidate subset (`>=2` distinct) — may remain `UNBOUND` in preflight;
- tokenizer/processor/custom-code revisions;
- exact hardware/provider/runtime/precision identity — may remain `UNBOUND` in preflight;
- peak-VRAM and latency measurement capability;
- gated-access authorization status;
- bounded run attempts and artifact destinations;
- audit artifact SHA-256 values;
- exact report-validation/report-schema bindings;
- later exact-head CI/review/merge gates.

An `UNBOUND` execution item must remain explicitly blocking for execution; it does not make a successful corpus audit false.

If Sections A–D pass and the inventory is complete and truthful for the ready path, the result may provisionally render exactly one successor inactive candidate for Section E binding:

```text
CANDIDATE_ID = FD-MESC-BT-EXEC-1-CANDIDATE-V2
AUTHORITATIVE_PATH = specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md
```

The successor is a valid preflight output only if its exact bytes are bound by Section E and Sections E–F also pass. A `BLOCKED` terminal package must not retain the successor candidate; it must use `successor_candidate = null` and preserve the blocked evidence instead.

The older `readiness-repair-2-result/execution-authorization-candidate.md` remains immutable historical seed evidence and is superseded **only after** the V2 result package is canonically merged and post-merge verified. No two candidate records may simultaneously claim current authority.

## H. Terminal state

The preflight may conclude:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

only when Sections A–G pass and every remaining execution blocker is truthfully recorded.

Otherwise:

```text
BLOCKED
```

Neither terminal state authorizes model access or execution. Only a separately reviewed and canonically adopted `FD-MESC-BT-EXEC-1` authorization can do that.
