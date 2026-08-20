# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **CANDIDATE ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-20

The preflight is complete only if every requirement below is satisfied on one exact canonical input state.

**Execution-order rule:** section letters are acceptance categories, not permission to read content before the one-shot claim. Before the atomic claim in Section F, the worker may inspect only Git/repository metadata required to identify the authorization and prove replay state: commit/tree ancestry, repository paths, Git blob IDs, PR/result metadata, claim/protection metadata, and the four authorization-package blob IDs. It MUST NOT read, hash, parse, decompress, or derive values from `task-prompts.json`, corpus bytes, scoring-key bytes, or any other frozen Repair-2 artifact content until the claim is successfully created, re-verified, and the matching `activation-receipt.json` is published on the unique result branch. Section A content-byte verification and Sections C–D therefore execute only after Section F.3.

## A. Canonical ancestry and complete input identity

The Repair-2 canonical Git identity is fixed as:

```text
REPAIR_2_CANONICAL_MERGE_SHA = 0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3
REPAIR_2_CANONICAL_TREE = 60e900daecea1cb9e64db95314bf9358387072b7
```

The PR number is historical metadata only and is not an ancestry predicate. Pre-claim metadata inspection must mechanically prove that `REPAIR_2_CANONICAL_MERGE_SHA` is an ancestor of the canonical authorization merge and that the commit has exactly `REPAIR_2_CANONICAL_TREE`.

Every frozen Repair-2 file input used by this preflight is additionally bound to its repository path and Git blob SHA in that exact canonical tree. This path/blob identity check is Git metadata and may be performed pre-claim; reading or hashing the blob contents may not.

| Repository path | Git blob SHA |
|---|---|
| `specs/mesc-backbone-tournament/readiness-repair-2-result/corpus-specification.json` | `d067a9939f8862fb5a36713fba5f5d24c4a9ef20` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/materialized-corpus.jsonl.gz` | `cfd8ec3dac6a9a1f9f638eb73b21d52f07edfc4c` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/corpus-manifest.json` | `801cfc6a591baa1d70621236cbc55e8c761c1c65` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-A.jsonl` | `9f164e31bbafe8ee0479d34831e1a0506523a603` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-B.jsonl` | `3811ab1b39147fdede5dbb29b7a758e68fabef3e` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-C.jsonl` | `cbca882762707c84fa2afd960a2d7772e8934aed` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-D.jsonl` | `fef60fa940a070a2f48da07d1a07755acb86f6e1` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-E.jsonl` | `1db506fdb0b2dba74df599603d0615ee1a797e30` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-keys-F.jsonl` | `5747c4493f26ad6aa8e2b76919e86220a2c603e4` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/task-prompts.json` | `9a2edb0843e31e04c56320e93334d06471b9e69e` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/normalized-output-schema.json` | `2af7feab3bda5403c7c37a86a0b4535bbffcc2cb` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/parser-contract.json` | `7ed89a551b208854443e6e4aa4796fa30559fd2d` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/report-validation-contract.json` | `4200d144986648a5c7ac4a198d32b001367fdc4f` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/scoring-contract.json` | `a31a9e9977327c1ab269267771d717a20b270186` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/protocol-config.json` | `28bc86a263c1a5f4edc7e0edb2106f0120d207f2` |
| `specs/mesc-backbone-tournament/readiness-repair-2-result/report-schema.json` | `6310e7ba0914e95bbf5a50d38637007c8b30299c` |

All entries above are mandatory. `corpus-manifest.json` remains the immutable canonical source for the six scoring-key shard SHA-256/count/byte-length bindings; this table adds Git-object identity and does not replace that manifest.

**Only after successful Section F.3 claim + activation-receipt publication**, exact frozen content verification must include:

- `corpus-specification.json` bytes against `CORPUS_SPEC_SHA256`;
- `materialized-corpus.jsonl.gz` bytes against `MATERIALIZED_CORPUS_GZIP_SHA256`;
- decompressed logical corpus bytes against `MATERIALIZED_CORPUS_SHA256` and exact count 240;
- `corpus-manifest.json` bytes against `CORPUS_MANIFEST_SHA256`;
- every scoring-key shard by path/Git blob/manifest SHA-256/count/byte length and their frozen logical concatenation against `SCORING_KEYS_SHA256`;
- `task-prompts.json` exact bytes against `TASK_PROMPT_BUNDLE_SHA256`;
- `normalized-output-schema.json` exact bytes against `NORMALIZED_OUTPUT_SCHEMA_SHA256`;
- `parser-contract.json` exact bytes against `PARSER_CONTRACT_SHA256`;
- `report-validation-contract.json` exact bytes against `REPORT_VALIDATION_CONTRACT_SHA256`;
- `scoring-contract.json` exact bytes against `SCORING_CONTRACT_SHA256`;
- `protocol-config.json` exact bytes against `PROTOCOL_CONFIG_SHA256`;
- `report-schema.json` exact bytes against `REPORT_SCHEMA_SHA256`.

The two derived prompt bindings are also mandatory **post-claim only** and have exact source/preimage rules:

1. `SYSTEM_PROMPT_SHA256` is `SHA256(UTF8(task-prompts.json["system_prompt"]))`, where `task-prompts.json` is the exact blob above and JSON parsing rejects duplicate member names.
2. `PROMPT_PROTOCOL_SHA256` is SHA-256 of the no-newline canonical JSON bytes for exactly:

```json
{"prompt_bundle_sha256":"54d9da5cf3dad58c0bf9fb28761c15d8f82568013895b8467f1cb7d532c314b7","protocol_config_sha256":"097cdd11f5389203cf432760ec316a78b12d157c0676477de69dde707e058203","system_prompt_sha256":"02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867","version":"MESC-BT-PROMPT-PROTOCOL-DIGEST-V1"}
```

The resulting digest must equal `a2a42aef340e27f9396b40810999d5f2c4136af467ce27ee9e3c149e3257c89c`.

No corpus substitution, regeneration, rematerialization, floating ref, omitted frozen contract binding, alternate derivation, or pre-claim content read is permitted.

Any missing path, blob identity, digest reproduction, derivation proof, or execution-order violation => `BLOCKED`.

## B. Canonical JSON serialization and SHA-256 rule

`MESC-BT-PREFLIGHT-CANONICAL-JSON-V1` applies to both audit files and every preflight canonical JSON preimage or artifact that invokes this section, including activation/terminal receipts and result-manifest objects.

Before canonicalization, every parsed JSON object MUST reject duplicate member names at every nesting level. Duplicate member names are invalid; no first-wins, last-wins, merge, or parser-dependent behavior is permitted. Detection of any duplicate member name => `BLOCKED` before serialization or SHA-256 computation.

Canonical serialization is one RFC 8259 JSON object using:

- UTF-8 encoding without BOM;
- Unicode strings normalized to NFC before serialization;
- object keys sorted lexicographically by Unicode code point at every object level;
- array order preserved exactly as defined by the applicable contract;
- separators exactly `,` and `:` with no insignificant whitespace;
- JSON escaping only as required by RFC 8259; non-ASCII Unicode is encoded directly as UTF-8, not `\u`-escaped unless required by JSON syntax;
- booleans as `true`/`false`, null as `null`;
- numeric values restricted to base-10 integers, with no leading plus sign, no leading zeros except `0`, and no floating-point values;
- no trailing newline and no bytes before or after the JSON object.

For an audit artifact:

1. the audit object MUST NOT contain any field storing its own file SHA-256;
2. the complete canonical audit file bytes are the hash preimage;
3. `SHA256(file_bytes)` is the audit artifact SHA-256;
4. the digest is published only in `preflight-result-manifest.json`, never inserted back into the audit file;
5. each audit records `canonicalization_rule_id = MESC-BT-PREFLIGHT-CANONICAL-JSON-V1`.

Any parser or serializer that cannot enforce or reproduce these exact bytes => `BLOCKED`.

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
3. After Sections A–D PASS and the execution-binding inventory is complete and truthful for the provisional ready path, the episode may provisionally render exactly one `FD-MESC-BT-EXEC-1-CANDIDATE-V2` solely as a Section E hash input. Render it at `execution-authorization-candidate.md` under the preflight result directory, UTF-8 without BOM, LF line endings, exactly one final LF, then compute its exact full-file SHA-256 and byte length. Provisional rendering grants no authority and is not yet a valid preflight output. If those prerequisites are not met, no successor file may be present and the binding value is `null`.
4. Construct `manifest_binding_core` as canonical JSON under Section B containing exactly:
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
8. Generate `preflight-result-manifest.json` as canonical JSON under Section B. It must contain the complete `manifest_binding_core` object, its SHA-256, and an `artifacts` map containing exact path, SHA-256, and byte length for all four unconditional core outputs plus the successor candidate when `successor_candidate` is non-null.
9. If any Section E, F, G, receipt, claim, or later acceptance check forces terminal `BLOCKED`, remove any provisionally rendered successor, set `successor_candidate = null`, and rebuild the binding core, verdict, and manifest from the blocked package; stale hashes are invalid.
10. The manifest MUST NOT contain its own file SHA-256. Its exact full-file SHA-256 is computed externally and recorded in the terminal receipt and the preflight result PR description.

A present-but-unbound successor candidate, missing/mismatched core hash, output hash, byte length, path, or verdict reference => `BLOCKED`.

## F. Atomic one-shot claim, activation receipt, durable terminal receipt, and replay rejection

The authorization episode is single-use. Exactly one worker may transition it from `UNUSED`; any observed non-`UNUSED` state rejects reuse.

### F.1 Exact activation receipt preimage

After this authorization package is canonically merged and post-merge verified, derive `ACTIVATION_RECEIPT_ID` using only canonical authorization Git metadata; this derivation requires no Repair-2 content read. It is SHA-256 of canonical JSON under Section B containing exactly these keys:

- `decision_id = FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `authorization_merge_sha = <canonical authorization merge SHA>`;
- `authorization_merge_tree = <canonical authorization merge tree>`;
- `authorization_package_files = <ordered array below>`;
- `receipt_version = MESC-BT-PREFLIGHT-RECEIPT-V1`.

`authorization_package_files` contains exactly four objects, in this exact array order, with each `git_blob_sha` read from the canonical authorization merge tree:

1. `{"path":"specs/mesc-backbone-tournament/execution-preflight-1/README.md","git_blob_sha":"<40-hex blob SHA>"}`
2. `{"path":"specs/mesc-backbone-tournament/execution-preflight-1/acceptance.md","git_blob_sha":"<40-hex blob SHA>"}`
3. `{"path":"specs/mesc-backbone-tournament/execution-preflight-1/founder-authorization.md","git_blob_sha":"<40-hex blob SHA>"}`
4. `{"path":"specs/mesc-backbone-tournament/execution-preflight-1/plan.md","git_blob_sha":"<40-hex blob SHA>"}`

No other path belongs to the activation-receipt preimage. Missing, reordered, duplicated, extra, or mismatched path/blob entries => `BLOCKED`.

### F.2 Mutually exclusive replay-state predicates

State is evaluated with this precedence: canonical terminal receipt → matching in-progress evidence → claim-only evidence → unused. Conflicting or ambiguous evidence overrides all normal states and is `BLOCKED`.

| State | Exact evidence predicate | May a new episode start? |
|---|---|---|
| `UNUSED` | no claim ref; no matching activation receipt; no result branch or open/closed result PR for this authorization/receipt; no terminal receipt; no conflicting/mismatched historical evidence | YES, by atomic claim only |
| `ISSUED` | the exact protected claim ref exists and points to the authorization merge SHA; **no** activation receipt, result branch/PR, or terminal receipt exists yet | NO |
| `IN_PROGRESS` | the exact protected claim ref exists and at least one matching activation receipt, result branch, or result PR exists; **no canonical terminal receipt** exists | NO |
| `BLOCKED` | a matching canonical terminal receipt records `state = BLOCKED`, **or** any claim-protection violation, deleted/retargeted claim evidence, conflicting receipt, mismatched claim target, or ambiguous state is observed | NO |
| `CONSUMED` | a matching canonical terminal receipt records `state = CONSUMED` and matches the final ready manifest | NO |

`ISSUED` and `IN_PROGRESS` are therefore disjoint: publication/creation of any matching activation-receipt/result evidence moves the logical state from claim-only `ISSUED` to `IN_PROGRESS`. A terminal receipt supersedes both. Any state other than proven `UNUSED` => reject reuse.

### F.3 Storage-protected atomic claim before any frozen-content read

Before claim creation, perform only the metadata operations permitted by the execution-order rule: verify canonical authorization/Repair-2 commit/tree ancestry, the expected path→blob IDs, derive `ACTIVATION_RECEIPT_ID` from the four authorization-package blob IDs, and search canonical history/open/closed result PR metadata for replay evidence. Do **not** read any Repair-2 blob contents.

Before creating the claim, mechanically verify `CLAIM_REF_PROTECTION = PASS` at the Git hosting/storage boundary for this exact namespace:

```text
refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/**
```

The protection must be a repository ruleset, server-side hook, or equivalent durable control that is already effective and that, for this claim namespace:

1. permits the controlled initial ref creation required by this episode;
2. denies every subsequent ref update, including ordinary fast-forward updates and force updates;
3. denies ref deletion;
4. gives the preflight worker no bypass capable of update/deletion after creation;
5. remains effective from immediately before claim creation through canonical terminal result adoption.

Record the exact protection mechanism identity and observed enforcement facts in `activation-receipt.json` and carry them into `consumption-receipt.json`. If no such durable storage-boundary protection can be proven, do not create a claim and terminate `BLOCKED` before any frozen-content read.

Then atomically create exactly one claim ref:

```text
refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
```

The claim ref MUST use create-only semantics, only if absent, and MUST point exactly to `AUTHORIZATION_MERGE_SHA`. Creation failure because the ref already exists means another worker/episode already claimed the authorization: stop immediately without changing the ref or starting audit work.

Immediately after creation, re-read the claim ref and protection control. Any missing/changed target or protection drift is `BLOCKED`. Updating, force-updating, retargeting, deleting, or recreating the claim is prohibited. If a claim is ever observed deleted or changed after creation, the episode can never be classified `UNUSED`; the observing worker must preserve durable `BLOCKED` evidence in its result package/terminal receipt and stop.

After successful claim creation and re-verification, create the unique result branch and publish `activation-receipt.json` **before any Repair-2 frozen-content read/hash/parse/decompression**. It must reproduce the receipt preimage and `ACTIVATION_RECEIPT_ID`, record the exact `claim_ref` and target, record the verified claim-protection mechanism identity/enforcement facts, and record `state = ISSUED`. Only after this receipt is published may Section A content verification and Sections C–D begin; from the first such content operation onward the logical state is `IN_PROGRESS`.

### F.4 Terminal receipt for both outcomes

Every claimed episode must terminate with `consumption-receipt.json` outside the result-manifest artifact set. It is canonical JSON under Section B and contains exactly:

- `receipt_version = MESC-BT-PREFLIGHT-TERMINAL-RECEIPT-V1`;
- `activation_receipt_id`;
- `activation_receipt_preimage`;
- `claim_ref`;
- `claim_ref_target`;
- `claim_ref_protection` containing the exact protection mechanism identity and terminal re-verification facts;
- `preflight_result_manifest_sha256`;
- `terminal_state`, exactly `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` or `BLOCKED`;
- `state`, exactly `CONSUMED` when `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, otherwise exactly `BLOCKED`.

A successful package therefore records `state = CONSUMED`; a blocked package records `state = BLOCKED`. Both bind the exact final manifest SHA-256 and matching activation identity. The terminal receipt is not included in the manifest hash set, avoiding a digest cycle.

Canonical merge of the result package is the durable terminal-state transition. The protected claim ref remains permanent in either outcome. A claimed episode that cannot publish a terminal result remains burned/non-reusable; any later evidence of the claim or its activation receipt prevents `UNUSED`. It requires a new separately reviewed Founder authorization rather than a restart.

Missing/mismatched protection, claim, activation receipt, terminal receipt, manifest digest, or state correspondence => `BLOCKED`.

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

The successor-candidate lifecycle is exactly:

1. provisional rendering is allowed only under Section E after Sections A–D PASS and inventory readiness checks;
2. provisional bytes exist only to compute the Section E manifest binding and grant no authority;
3. `FD-MESC-BT-EXEC-1-CANDIDATE-V2` becomes a valid preflight output only if Sections A–G all pass and the terminal package is `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`;
4. any later failure requires removal of the provisional file, `successor_candidate = null`, and deterministic rebuild of the blocked binding package.

The only permitted successor identity/path is:

```text
CANDIDATE_ID = FD-MESC-BT-EXEC-1-CANDIDATE-V2
AUTHORITATIVE_PATH = specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md
```

The older `readiness-repair-2-result/execution-authorization-candidate.md` remains immutable historical seed evidence and is superseded only after the V2 result package is canonically merged and post-merge verified. No two candidate records may simultaneously claim current authority.

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
