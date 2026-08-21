# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **CANDIDATE ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-20

The preflight is complete only if every requirement below is satisfied on one exact canonical input state.

**Execution-order rule:** section letters are acceptance categories, not permission to read frozen Repair-2 content before the one-shot claim. Before the atomic claim in Section F, the worker may inspect Git/repository metadata required to identify the authorization and prove replay state—commit/tree ancestry, repository paths, Git blob IDs, ref targets, protection metadata, and the four authorization-package blob IDs—and may read/parse only **non-Repair-2 episode-governance evidence** required to classify replay/lifecycle state. Permitted content evidence is limited to `activation-receipt.json` / `consumption-receipt.json` reachable from discovered result-lineage commits plus the exact marker-delimited machine-readable PR evidence block defined in F.2 from a structurally selected current-episode preflight-result PR. PR patches, diffs, changed-file contents, review comments, free-form PR prose outside that block, and all frozen Repair-2 content are outside pre-claim authority. The worker MUST NOT read, hash, parse, decompress, or derive values from `task-prompts.json`, corpus bytes, scoring-key bytes, or any other frozen Repair-2 artifact content until the claim is successfully created, re-verified, and the matching `activation-receipt.json` is published by the first permitted fast-forward of the protected `RESULT_REF`. Section A content-byte verification and Sections C–D therefore execute only after Section F.3.

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

No corpus substitution, regeneration, rematerialization, floating ref, omitted frozen contract binding, alternate derivation, or pre-claim frozen-content read is permitted.

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
10. The manifest MUST NOT contain its own file SHA-256. Its exact full-file SHA-256 is computed externally and recorded in the terminal receipt and the preflight result PR evidence block.

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

### F.2 Mutually exclusive replay-state predicates, exhaustive discovery, and claim linearization

The only permitted result-ref and claim-ref prefixes and full ref identities are:

```text
RESULT_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/
RESULT_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
CLAIM_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/
CLAIM_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
PREFLIGHT_RESULT_PR_AUTH_PREFIX = governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/
PREFLIGHT_RESULT_PR_HEAD_REF = governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
```

Each `*_REF_PREFIX` is a literal ref-name prefix, never a glob. A ref is under a prefix iff its full ref name starts with that exact prefix. The only syntactically well-formed descendant under either prefix has exactly two non-empty path segments after the prefix: `<AUTHORIZATION_MERGE_SHA>` MUST be 40 lowercase hexadecimal characters and `<ACTIVATION_RECEIPT_ID>` MUST be 64 lowercase hexadecimal characters. Any malformed descendant => `BLOCKED`. For the **current** `AUTHORIZATION_MERGE_SHA`, the only permitted receipt segment is the uniquely derived current `ACTIVATION_RECEIPT_ID`; any same-authorization sibling with a different receipt ID is unexpected conflicting episode evidence and => `BLOCKED`. Well-formed refs for other authorization SHAs remain historical evidence for those other authorizations and do not by themselves block the current one.

PR enumeration applies **two** deterministic structural classifications:

1. **Current-episode selector.** A PR is selected as the current episode iff all of these structural predicates hold exactly: base repository full name=`TheHalfMoon/MESC`; base ref=`main`; head repository full name=`TheHalfMoon/MESC`; retained `headRefName`=`PREFLIGHT_RESULT_PR_HEAD_REF`. PR state may be open, closed, or merged and is not a selector. Title, labels, reviews, issue linkage, author, and free-form body prose are never selectors. If an authoritative current head OID is exposed, it MUST equal the authoritative `RESULT_REF` target in the same replay snapshot. If the result branch has been deleted and a current head OID is unavailable, retained exact `headRefName` still selects the PR and it remains replay evidence; reconcile its lifecycle through canonical history, permitted non-Repair-2 receipts, and the exact evidence block below.
2. **Current-authorization namespace-conflict detector.** Independently of the current selector, any PR whose head repository is exactly `TheHalfMoon/MESC` and whose retained `headRefName` starts with `PREFLIGHT_RESULT_PR_AUTH_PREFIX` is in the reserved current-authorization result-PR namespace. Such a PR is valid only if it also satisfies the current-episode selector. A different receipt suffix, malformed/non-64-lowercase-hex suffix, extra path segment, wrong base repository/ref, or otherwise non-current structural record under that prefix => `BLOCKED`, even if its branch/ref has since been deleted.

Missing/unreadable required structural fields, inability to classify every PR under both rules, an unreconcilable selected PR, or any reserved-namespace conflict => `BLOCKED`. Only a current-episode selected PR may have its marker-delimited body evidence parsed.

No other governance ref or PR may represent this authorization episode. Before classifying the authorization as `UNUSED`, the worker MUST independently and exhaustively complete all four replay-evidence searches below from authoritative Git hosting data:

1. enumerate every ref whose full name starts with `RESULT_REF_PREFIX`;
2. enumerate every ref whose full name starts with `CLAIM_REF_PREFIX`;
3. traverse the complete canonical commit history reachable from the then-current canonical `main` tip, following every parent edge to repository roots with no shallow boundary or omitted merge parent, and inspect relevant commit/tree metadata and permitted non-Repair-2 episode receipts for this decision/receipt/result evidence; and
4. enumerate the complete PR population in both open and closed/merged states, apply **both** deterministic PR classification rules above to every PR, reject any reserved-namespace conflict, and inspect each current-episode selected PR's structural record plus, if present, only the exact evidence block below.

The only PR-body bytes semantically permitted pre-claim are one marker-delimited canonical JSON object:

```text
<!-- MESC-BT-PREFLIGHT-EVIDENCE-V1:BEGIN -->
<one MESC-BT-PREFLIGHT-CANONICAL-JSON-V1 object>
<!-- MESC-BT-PREFLIGHT-EVIDENCE-V1:END -->
```

A valid current-episode result PR MUST NOT be opened before the activation CAS in F.3.2 has succeeded and been re-read/reconciled. From the first PR publication onward its body MUST contain exactly one valid evidence block; a selected current-episode PR with no block, more than one block, malformed markers, or a stale/incomplete block => `BLOCKED`.

The evidence object MUST contain **exactly these 19 top-level keys**, every time: `evidence_version`, `decision_id`, `authorization_merge_sha`, `activation_receipt_id`, `activation_receipt_preimage`, `claim_ref`, `claim_ref_target`, `result_ref`, `result_ref_target`, `result_ref_activation_commit`, `result_ref_terminal_content_commit`, `terminal_receipt_commit`, `terminal_receipt_sha256`, `preflight_result_manifest_sha256`, `result_ref_cas_protocol`, `result_ref_cas_evidence`, `terminal_result_ref_protection`, `terminal_state`, and `state`. Missing, unknown, or duplicate top-level keys => `BLOCKED`.

Common field rules are exact:

- `evidence_version` = `MESC-BT-PREFLIGHT-EXTERNAL-EVIDENCE-V1`;
- `decision_id` = `FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `authorization_merge_sha` is the exact 40-lowercase-hex current `AUTHORIZATION_MERGE_SHA`;
- `activation_receipt_id` is the exact 64-lowercase-hex current `ACTIVATION_RECEIPT_ID`;
- `activation_receipt_preimage` is exactly the F.1 canonical preimage object with top-level keyset `decision_id`, `authorization_merge_sha`, `authorization_merge_tree`, `authorization_package_files`, `receipt_version`; its `authorization_package_files` array has exactly the four ordered F.1 objects and each object has exactly `path` and `git_blob_sha`; `SHA256(canonical_activation_receipt_preimage_bytes)` MUST equal `activation_receipt_id`;
- `claim_ref` = exact `CLAIM_REF` and `claim_ref_target` = exact `authorization_merge_sha`;
- `result_ref` = exact `RESULT_REF`;
- `result_ref_target` is a 40-lowercase-hex OID equal to the authoritative hosting target observed for `RESULT_REF` in the same replay snapshot;
- `result_ref_activation_commit` is a non-null 40-lowercase-hex OID for the valid activation commit and is the `new_oid` of the first accepted CAS record;
- `result_ref_terminal_content_commit` is either `null` or a 40-lowercase-hex OID; once non-null it MUST identify the valid terminal-content commit and MUST never revert to `null` or change;
- `terminal_receipt_commit` is either `null` or a 40-lowercase-hex OID; once non-null it MUST identify the exact attempted/canonical terminal-receipt commit and MUST never revert to `null` or change;
- `terminal_receipt_sha256` is `null` iff `terminal_receipt_commit` is `null`; otherwise it is the exact 64-lowercase-hex SHA-256 of `RESULT_ROOT/consumption-receipt.json` in that commit;
- `preflight_result_manifest_sha256` is `null` iff the current result-lineage tree has not yet produced `preflight-result-manifest.json`; otherwise it is the exact 64-lowercase-hex full-file SHA-256 of the manifest represented by the current evidence state. If `result_ref_terminal_content_commit` is non-null, this field MUST be non-null and match that terminal-content package;
- `result_ref_cas_protocol` is the exact non-empty NFC string recorded as the selected `RESULT_REF_CAS_PROTOCOL` in the activation receipt;
- `terminal_result_ref_protection` is `null` until a terminal-receipt CAS has been accepted and a terminal protection/freeze observation has been made; when non-null it has exactly `mechanism_identity`, `mechanism_version`, `observed_result_ref_target`, `terminal_frozen`, `no_configured_bypass`, with the first two values non-empty NFC strings, `observed_result_ref_target` a 40-lowercase-hex OID, and the last two values booleans;
- `terminal_state` is exactly `null`, `BLOCKED`, or `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`; and
- `state` is exactly `IN_PROGRESS`, `BLOCKED`, or `CONSUMED`. `UNUSED` and `ISSUED` are impossible in a valid result-PR evidence block because the result PR may exist only after successful activation.

`result_ref_cas_evidence` is a non-empty array containing **every CAS attempt for this episode from the activation update through the current evidence observation**, with no omission. Records are sorted by `sequence` ascending; `sequence` values are contiguous base-10 integers starting at 1. Every record has exactly these keys: `sequence`, `protocol_identity`, `ref_name`, `expected_old_oid`, `new_oid`, `outcome`, `observed_post_target`, `pre_protection`, `post_protection`. `protocol_identity` is the exact `result_ref_cas_protocol`; `ref_name` is the exact `result_ref`; the three OID fields are 40 lowercase hexadecimal; `outcome` is exactly `ACCEPTED` or `REJECTED`. `pre_protection` and `post_protection` each have exactly `mechanism_identity`, `mechanism_version`, `terminal_frozen`, `no_configured_bypass`; mechanism fields are non-empty NFC strings, freeze/bypass fields are booleans, and `no_configured_bypass` MUST be `true` for every record that is accepted as valid protocol evidence.

CAS cross-bindings are mandatory:

1. the first record MUST be `ACCEPTED`, with `expected_old_oid = authorization_merge_sha`, `new_oid = result_ref_activation_commit`, and `observed_post_target = new_oid`;
2. considering only `ACCEPTED` records, every later accepted record MUST have `expected_old_oid` equal to the immediately previous accepted `new_oid`, and every accepted `observed_post_target` MUST equal its `new_oid`;
3. the last array record's `observed_post_target` MUST equal `result_ref_target`;
4. if any record is `REJECTED`, it MUST be the final array record, no later CAS is permitted under this authorization, `state` MUST be `BLOCKED`, and the proposed `new_oid` MUST NOT be treated as an adopted lifecycle target;
5. absent a final rejected attempt, the final accepted `new_oid` MUST equal `result_ref_target`; and
6. every accepted `new_oid` MUST satisfy the F.3 one-parent/result-root lineage rules and its pre/post protection observations MUST reconcile with authoritative hosting evidence.

State-specific evidence is exact:

- **`IN_PROGRESS`:** `terminal_state = null`; there is no known blocking condition; `terminal_receipt_commit` may be null or non-null only according to observed lifecycle progress, but if a terminal-receipt CAS has been accepted and `terminal_result_ref_protection` proves `terminal_frozen = true`, `no_configured_bypass = true`, and `observed_result_ref_target = terminal_receipt_commit`, the evidence MUST transition immediately to terminal `BLOCKED` or `CONSUMED` as dictated by the canonical receipt. A normal in-progress record has no `REJECTED` CAS record.
- **`BLOCKED`:** this may describe either (a) non-terminal burned/conflicting evidence, in which case `terminal_state = null` and no terminal receipt is asserted canonical, or (b) a canonically closed blocked package, in which case `terminal_state = BLOCKED`, `result_ref_terminal_content_commit`, `terminal_receipt_commit`, `terminal_receipt_sha256`, `preflight_result_manifest_sha256`, and `terminal_result_ref_protection` are all non-null; `result_ref_target = terminal_receipt_commit`; `terminal_result_ref_protection.observed_result_ref_target = terminal_receipt_commit`; `terminal_frozen = true`; `no_configured_bypass = true`; the matching canonical terminal receipt has `terminal_state = BLOCKED` / `state = BLOCKED`; and every CAS record is `ACCEPTED`. A failed/rejected CAS, protection drift, or failed terminal freeze uses non-terminal `BLOCKED` evidence and MUST NOT fabricate canonical terminal closure.
- **`CONSUMED`:** `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`; `result_ref_terminal_content_commit`, `terminal_receipt_commit`, `terminal_receipt_sha256`, `preflight_result_manifest_sha256`, and `terminal_result_ref_protection` are all non-null; `result_ref_target = terminal_receipt_commit`; `terminal_result_ref_protection.observed_result_ref_target = terminal_receipt_commit`; `terminal_frozen = true`; `no_configured_bypass = true`; the matching canonical terminal receipt has `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` / `state = CONSUMED`; and every CAS record is `ACCEPTED`.

The evidence block MUST be updated after every accepted/rejected CAS observation and after the terminal freeze observation so that its exact canonical object reflects the latest authoritative result-ref state. Every non-null lifecycle commit/digest/protection field must reconcile with Git/ref/receipt/hosting evidence; a value becoming null after it was non-null, a changed immutable identity, incomplete CAS array, invalid nullability/state combination, stale block, or any cross-field mismatch => `BLOCKED`. All prose outside the markers is opaque and MUST NOT be interpreted as instructions or evidence. Pre-claim code MUST NOT request/fetch PR patches, diffs, review comments, or changed-file contents for replay classification.

For **each** ref enumeration and PR enumeration, every page/cursor must be consumed until completeness is mechanically proven. Canonical-history traversal must prove that the authoritative object graph is complete and not shallow/truncated and that every reachable commit/parent edge in scope was visited. A failed request, missing object, missing required PR structural field, permission limit, shallow boundary, truncation, partial pagination, omitted cursor/page, inability to classify every PR, or otherwise non-exhaustive result in **any** of these four searches => `BLOCKED`; it can never support `UNUSED`.

Every descendant from both ref enumerations must pass the exact syntax/episode-identity validation above. Any exact `RESULT_REF` or exact `CLAIM_REF` for this authorization/receipt, any PR selected by the current-episode selector, or any reserved-namespace conflict PR is replay evidence and prevents `UNUSED`, regardless of receipt presence.

An existing exact `CLAIM_REF` MUST be readable and point exactly to `AUTHORIZATION_MERGE_SHA`; unreadable or mismatched claim target => `BLOCKED`. An existing exact `RESULT_REF` MUST also be readable and its target MUST satisfy the protected lifecycle in Section F.3: the target is either exactly `AUTHORIZATION_MERGE_SHA` at initial issuance, or a permitted fast-forward descendant of that SHA on the single result lineage whose commit graph/tree scope is valid. The worker may read/parse permitted non-Repair-2 episode receipt JSON and the exact PR evidence block pre-claim solely to reconcile that lifecycle. An unreadable target, non-descendant target, force/sideways retarget, missing required lifecycle/CAS evidence, invalid commit/tree scope, or target inconsistent with matching selected result-PR/receipt state => `BLOCKED`, never generic `IN_PROGRESS` evidence.

State is evaluated with this precedence: canonical terminal receipt → matching in-progress evidence → claim-only evidence → unused. Conflicting or ambiguous evidence overrides all normal states and is `BLOCKED`.

| State | Exact evidence predicate | May a new episode start? |
|---|---|---|
| `UNUSED` | both ref-prefix enumerations, complete canonical-history traversal, and complete open+closed/merged PR enumeration/classification under both PR rules are mechanically proven exhaustive; no exact claim ref; no matching activation receipt; no exact `RESULT_REF`; no current-episode selected PR; no terminal receipt; no malformed/unexpected current-authorization descendant or reserved-namespace conflict PR; no conflicting/mismatched historical evidence | YES, by atomic claim only |
| `ISSUED` | the exact protected claim ref exists and points to the authorization merge SHA; **no** activation receipt, exact `RESULT_REF`, selected current-episode result PR, or terminal receipt exists yet | NO |
| `IN_PROGRESS` | the exact protected claim ref exists and at least one matching activation receipt, lifecycle-valid exact `RESULT_REF`, or selected current-episode result PR exists; **no canonical terminal receipt** exists and no blocking/conflicting evidence is present | NO |
| `BLOCKED` | a matching canonical blocked terminal receipt exists, **or** any exact PR evidence block has `state = BLOCKED`, **or** any incomplete ref/history/PR search or PR classification, malformed/unexpected current-authorization descendant, reserved-namespace conflict PR (including same-authorization/different-receipt result PR), claim/result-ref protection violation, deleted/retargeted claim evidence, unreadable or lifecycle-invalid result-ref target, conflicting receipt, mismatched target/state, missing required worker-CAS evidence, or ambiguous state is observed | NO |
| `CONSUMED` | a matching **canonical terminal receipt** records `state = CONSUMED`, matches the final ready manifest, terminal result-ref freeze verification passed, and the exact PR evidence block is state-complete with `state = CONSUMED` | NO |

A terminal receipt is **canonical** only when its containing `TERMINAL_RECEIPT_COMMIT` is the exact frozen `RESULT_REF` target and all F.4 parent/tree/protection checks pass. A candidate receipt that was built but whose final ref update/re-read/freeze failed is not canonical terminal evidence; the episode remains non-reusable through its permanent claim/result history.

`ISSUED` and `IN_PROGRESS` are therefore disjoint. Any state other than proven `UNUSED` => reject reuse.

`PRECLAIM_REPLAY_SNAPSHOT` is canonical JSON under Section B and has exactly these top-level keys: `snapshot_version`, `authorization_merge_sha`, `activation_receipt_id`, `main_tip`, `history_reachable_commit_count`, `history_graph_sha256`, `result_refs`, `claim_refs`, and `selected_prs`. No other top-level key is permitted. `snapshot_version` MUST equal exactly `MESC-BT-PREFLIGHT-REPLAY-SNAPSHOT-V1`.

The snapshot arrays and history digest are deterministic as follows:

1. `result_refs` contains exactly one object `{ "ref_name": <full ref>, "target_oid": <40-lowercase-hex OID> }` for every syntactically valid current-authorization result ref discovered by the exhaustive result-prefix scan. Sort the array by NFC-normalized `ref_name` lexicographically by Unicode code point ascending. Duplicate `ref_name` records are invalid.
2. `claim_refs` uses the identical record shape and identical sort rule for current-authorization claim refs. Duplicate `ref_name` records are invalid.
3. `selected_prs` contains one object for every PR selected by the current-episode selector above, with exactly these keys: `number`, `node_id`, `state`, `base_repository`, `base_ref`, `head_repository`, `head_ref`, `head_oid`, `merge_commit_oid`, `evidence_parse_status`, and `evidence`. `number` is a base-10 integer; `node_id` is an NFC string; `state` is exactly `OPEN`, `CLOSED`, or `MERGED`, with merged taking precedence over closed; repository/ref fields are the exact hosting structural strings; `head_oid` is a 40-lowercase-hex string or `null` only when the hosting API no longer exposes it; `merge_commit_oid` is a 40-lowercase-hex string for merged PRs, otherwise `null`. `evidence_parse_status` is derived by the ordered first-failure procedure below, and `evidence` is the exact parsed state-complete canonical evidence object only when that status is `VALID`; for every other status `evidence = null`. Sort by numeric `number` ascending; if two records somehow have the same number, sort the tie by NFC-normalized `node_id` Unicode-code-point ascending. Duplicate `(number,node_id)` records are invalid.
4. Derive `evidence_parse_status` by evaluating these stages in order and stopping at the first failing stage: (a) if neither marker is present, `ABSENT`; (b) if the count of begin markers or end markers is not exactly one, `MARKER_COUNT_INVALID`; (c) if exactly one of each exists but marker order/framing is invalid, `MARKER_STRUCTURE_INVALID`; (d) if the enclosed bytes cannot parse as exactly one RFC 8259 JSON object with duplicate-member rejection, `JSON_PARSE_INVALID`; (e) if the parsed object does not reproduce byte-for-byte as its Section B canonical serialization, `JSON_NONCANONICAL`; (f) if the exact 19-key evidence schema, types, formats, nullability, state rules, or CAS nested schemas fail, `SCHEMA_INVALID`; (g) if the schema-valid object is stale or disagrees with authoritative Git/ref/receipt/hosting/CAS evidence, `EVIDENCE_INCONSISTENT`; otherwise `VALID`. These are the only permitted status values. Any non-`VALID` status => `BLOCKED`, but the snapshot remains well-defined and serializable with `evidence = null`.
5. Build the history-digest preimage as the Section B canonical JSON object `{"commits":[...]}`. The `commits` array contains exactly one record for every commit reachable from `main_tip`, each with exactly `commit_sha`, `tree_sha`, and `parent_shas`. Sort commit records by lowercase hexadecimal `commit_sha` ascending. Preserve each commit's Git parent order exactly inside `parent_shas`; do not sort that nested array. `history_reachable_commit_count` equals the array length and `history_graph_sha256 = SHA256(canonical_history_preimage_bytes)`.
6. Any malformed/duplicate record, missing required structural field, unavailable complete history record, or inability to reproduce these exact array orders/digest bytes => `BLOCKED`. Evidence parse/schema/content failures use the deterministic `evidence_parse_status` representation above rather than making snapshot serialization undefined.

After the first complete scan, serialize this exact snapshot object. Immediately before claim creation, repeat all four exhaustive searches and require the canonical snapshot bytes to be identical. After successful atomic claim creation, repeat them again **before creating `RESULT_REF`** and require the only permitted semantic delta to be appearance of the exact `CLAIM_REF` at `AUTHORIZATION_MERGE_SHA`; construct the post-claim snapshot using the same schema/order and compare all other fields byte-for-byte. `main_tip`, history digest/count, result refs, sibling claim refs, and selected PR evidence/status must otherwise remain identical. Any pre/post-claim snapshot drift => `BLOCKED`, no `RESULT_REF` creation, and no frozen-content read. The successful claim remains permanent replay evidence, so a drifted episode cannot revert to `UNUSED`.

### F.3 Storage-protected atomic claim and non-self-referential protected result-ref lifecycle before any frozen-content read

Before claim creation, perform only the operations permitted by the execution-order rule and F.2. Failure to prove completeness/integrity of any replay search, snapshot, evidence block, or target => `BLOCKED` before claim creation.

Before creating either episode ref, mechanically verify storage-boundary protection at the Git hosting boundary:

- `CLAIM_REF_PROTECTION = PASS` for every ref whose full name starts with `CLAIM_REF_PREFIX`; and
- `RESULT_REF_PROTECTION = PASS` for every ref whose full name starts with `RESULT_REF_PREFIX`.

`CLAIM_REF_PROTECTION` must be a repository ruleset, server-side hook, or equivalent durable control that:

1. permits the controlled initial claim creation;
2. denies every subsequent claim update, including ordinary fast-forward and force updates;
3. denies claim deletion;
4. has no configured repository/organization bypass actor capable of claim update/deletion after creation; and
5. remains effective from immediately before claim creation through canonical terminal result adoption.

`RESULT_REF_PROTECTION` is the **server-enforced invariant set**. It must be a repository ruleset, server-side hook, or equivalent durable control that:

1. permits controlled initial `RESULT_REF` creation only at `AUTHORIZATION_MERGE_SHA`;
2. before terminal freeze, permits subsequent updates only by the designated preflight principal and only as ordinary fast-forwards;
3. denies force updates, non-fast-forward/sideways retargets, deletion, recreation, and updates by every other principal;
4. requires every accepted new target to remain a descendant of `AUTHORIZATION_MERGE_SHA` on the single episode result lineage;
5. has no configured repository/organization administrative or automation bypass actor capable of violating items 2–4; any provider-internal event that changes a protected ref/policy is treated as observed protection drift and fails closed;
6. remains effective through terminal result construction and canonical adoption; and
7. after the exact terminal receipt commit is published and verified, enters a frozen state denying **all** later update/deletion by every repository/organization actor, with no configured bypass.

`RESULT_REF_CAS_PROTOCOL` is a separate **worker protocol obligation**, not a property attributed to `RESULT_REF_PROTECTION`. Every post-creation `RESULT_REF` update MUST use one atomic compare-and-update operation that supplies all of: full ref name, `expected_old_oid` equal to the immediately re-read 40-hex current target, and `new_oid`. The operation must have server-side atomic semantics: it accepts the update only if the ref still equals `expected_old_oid` and all server protection invariants pass; otherwise it rejects without changing the ref. A normal Git receive-pack ref-update command carrying old OID/new OID/ref, or a hosting API/hook operation with an equivalent explicit old-OID precondition, qualifies. A separate read followed by an unconditional ref PATCH/update does **not** qualify.

For every attempted result-ref update, preserve `RESULT_REF_CAS_EVIDENCE` outside the commit being published, containing at minimum: operation/protocol identity, full ref name, `expected_old_oid`, `new_oid`, accepted/rejected outcome, immediately observed post-operation target, and the exact pre/post server-protection identity/version observations. If the hosting boundary cannot provide an atomic old-OID-precondition operation or the worker cannot preserve/reconcile this evidence, the episode is `BLOCKED` and the update is not valid lifecycle evidence.

Record the exact claim/result server-protection mechanism identities and observed enforcement facts in `activation-receipt.json` and carry them into `consumption-receipt.json`. Record the selected `RESULT_REF_CAS_PROTOCOL` identity in the activation receipt; reconcile externally observed per-update CAS/protection evidence in later result/terminal governance evidence once those updates have occurred. If either server protection cannot be proven, or no qualifying CAS protocol exists, do not create the claim and terminate `BLOCKED` before any frozen-content read.

Then atomically create exactly `CLAIM_REF` with create-only semantics, only if absent, pointing exactly to `AUTHORIZATION_MERGE_SHA`. Immediately perform the F.2 post-claim snapshot revalidation. Creation collision or any unexpected snapshot delta means stop without altering the claim; the authorization is no longer reusable.

Immediately after creation, re-read the claim ref and protections. Any missing/changed claim target or protection drift is `BLOCKED`. Updating, force-updating, retargeting, deleting, or recreating the claim is prohibited. Absence of a terminal receipt never restores `UNUSED` after a claim has existed.

After successful claim creation and post-claim snapshot revalidation, atomically create exactly `RESULT_REF` with create-only semantics at `AUTHORIZATION_MERGE_SHA`. Creation failure because `RESULT_REF` already exists => `BLOCKED` and no frozen content may be read. Immediately re-read `RESULT_REF` and `RESULT_REF_PROTECTION`; any unreadable/mismatched initial target or protection drift => `BLOCKED`.

#### F.3.1 Exact RESULT_REF commit graph and tree scope

```text
RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-result/
```

The only allowed result-root paths are:

- `activation-receipt.json`;
- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- `preflight-result-manifest.json`;
- `execution-authorization-candidate.md` (conditional);
- `consumption-receipt.json` (terminal-receipt commit only).

Every commit ever targeted by `RESULT_REF` after initial creation MUST have **exactly one parent**; merge commits are prohibited. Its single parent MUST equal the immediately preceding valid `RESULT_REF` target/`expected_old_oid`. Every tree delta after `AUTHORIZATION_MERGE_SHA` MUST be confined to `RESULT_ROOT`; any change outside it => `BLOCKED`.

- **Activation commit:** single parent exactly `AUTHORIZATION_MERGE_SHA`; its only tree delta is creation of `RESULT_ROOT/activation-receipt.json`. No other result file may exist yet.
- **Intermediate result commit:** single parent exactly the immediately previous result target; may add/update only the six non-terminal result files listed above (the two audits, inventory, verdict, manifest, conditional candidate). `activation-receipt.json` is immutable after activation. `consumption-receipt.json` must remain absent. The candidate may be deleted only when the blocked-package rebuild rule requires `successor_candidate = null`; no other established result-root path may be deleted.
- **Terminal content commit:** single parent exactly the immediately previous result target; may finalize only the same non-terminal result files; after this commit exists, `activation-receipt.json` and every manifest-bound result artifact are byte-immutable. `consumption-receipt.json` remains absent.
- **Terminal receipt commit:** single parent exactly `TERMINAL_CONTENT_COMMIT`; its only tree delta is addition of `RESULT_ROOT/consumption-receipt.json`; every other path/blob must be byte-identical to the parent.

Every discovered or newly produced result-ref target must be validated against the applicable parent-count, exact-parent, path allowlist, tree-delta, and immutability rules in addition to ordinary ancestry/fast-forward checks. Failure => `BLOCKED`.

#### F.3.2 Protected activation and update sequence

1. Construct `activation-receipt.json` and the activation commit defined above. The receipt records `result_ref_activation_parent = AUTHORIZATION_MERGE_SHA`, the current server-protection identity/version, and selected `RESULT_REF_CAS_PROTOCOL`, but not its own containing commit SHA.
2. After the activation commit SHA is known, immediately re-read `RESULT_REF` and **freshly re-read/revalidate `RESULT_REF_PROTECTION` identity/version**; require target=`AUTHORIZATION_MERGE_SHA` and protection equal the approved pre-claim invariant set. Then invoke CAS with `expected_old_oid = AUTHORIZATION_MERGE_SHA` and `new_oid = <activation commit SHA>`.
3. Preserve CAS evidence, re-read `RESULT_REF`, **freshly re-read/revalidate the same server protection again**, require the exact activation SHA, validate the activation commit graph/tree/receipt bytes, and reconcile CAS evidence. Any target/protection drift => `BLOCKED` and no frozen content access. Only after this entire step passes is frozen Repair-2 content access permitted; the observed SHA is `RESULT_REF_ACTIVATION_COMMIT`.
4. Later intermediate updates repeat the same immediate target read, fresh server-protection observation, atomic old-OID CAS, post-update target/protection re-read, commit/tree validation, and CAS-evidence reconciliation.
5. Construct and publish `TERMINAL_CONTENT_COMMIT` by the same rule. After it is the verified target, its manifest-bound artifacts are immutable.
6. Construct `consumption-receipt.json` binding the already-known activation/content commits, final manifest SHA-256, claim/ref identities, server protections, reconciled CAS evidence through the content commit, and terminal state. Construct `TERMINAL_RECEIPT_COMMIT` as defined in F.3.1; the receipt does not contain its own receipt-commit SHA.
7. Immediately before the final update, freshly re-read target/protection and require target=`TERMINAL_CONTENT_COMMIT`; CAS to `TERMINAL_RECEIPT_COMMIT`; preserve evidence; re-read target/protection; validate exact receipt-commit graph/tree. Then activate and re-read the terminal frozen protection with no configured bypass. Only if all of these checks pass is the terminal receipt canonical. The receipt-commit SHA and final CAS/freeze evidence are external evidence published in the exact PR evidence block, not embedded inside the receipt itself.

Any failed activation/intermediate/terminal update, post-update re-read, protection revalidation, graph/tree validation, CAS reconciliation, or final freeze means the attempted terminal receipt is noncanonical and the episode remains permanently non-reusable through existing claim/result/history evidence. It may remain logically `ISSUED` or `IN_PROGRESS` rather than falsely claiming a completed terminal receipt. A new attempt requires a separately reviewed Founder authorization; terminal closure is never fabricated after a failed publication/freeze.

The activation receipt records `state = IN_PROGRESS` and `content_read_started = false`; the latter is an issuance-time fact, not another replay state.

### F.4 Non-self-referential terminal receipt, terminal result-ref freeze, and immutable adoption verification

A claimed episode that reaches terminal-package construction may close canonically only with `consumption-receipt.json` outside the result-manifest artifact set. It is canonical JSON under Section B and contains exactly:

- `receipt_version = MESC-BT-PREFLIGHT-TERMINAL-RECEIPT-V1`;
- `activation_receipt_id`;
- `activation_receipt_preimage`;
- `claim_ref`;
- `claim_ref_target`;
- `claim_ref_protection` with exact server-protection identity and terminal re-verification facts;
- `result_ref`;
- `result_ref_activation_commit`;
- `result_ref_terminal_content_commit`;
- `result_ref_protection` with exact server-protection identity/version, no-bypass facts, lifecycle evidence, and terminal pre-freeze observation;
- `result_ref_cas_protocol` and reconciled external CAS-evidence identities/records for every accepted lifecycle update through `TERMINAL_CONTENT_COMMIT`;
- `preflight_result_manifest_sha256`;
- `terminal_state`, exactly `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` or `BLOCKED`;
- `state`, exactly `CONSUMED` when `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, otherwise exactly `BLOCKED`.

The receipt MUST NOT contain its own containing `TERMINAL_RECEIPT_COMMIT` SHA. The final CAS/freeze outcome is necessarily external and is valid only through the exact PR evidence block plus authoritative hosting/ref observations.

A terminal receipt becomes canonical only after F.3.2 step 7 succeeds. If any part of final publication/freeze fails, the receipt does not acquire canonical terminal precedence even if its commit object exists. The durable claim/result refs and history still make the episode non-reusable; no synthetic success/blocked terminal receipt may be declared.

A successful canonical package therefore has receipt `state = CONSUMED`; a canonical blocked package has `state = BLOCKED`. Both bind the final manifest and known activation/content commits without self-reference. `CONSUMED` means **the one-shot preflight episode has been consumed**, not that model execution or the successor candidate is authorized.

Canonical merge of the result package is the repository adoption event, but post-merge mechanical verification is not a mutable status note and does not rewrite the terminal receipt. It MUST be bound to one immutable canonical record outside `RESULT_ROOT`:

```text
ADOPTION_RECORD_PATH = specs/mesc-backbone-tournament/execution-preflight-1-adoption/<RESULT_MERGE_SHA>/canonical-adoption-verification.json
```

The record uses Section B canonical JSON, contains no self-digest field, and MUST contain exactly these top-level keys: `record_version`, `decision_id`, `authorization_merge_sha`, `activation_receipt_id`, `result_merge_sha`, `result_merge_tree`, `ordered_parents`, `reviewed_result_head_sha`, `preflight_result_manifest_sha256`, `result_package_artifacts`, `terminal_receipt_commit`, `terminal_receipt_sha256`, `claim_ref`, `claim_ref_target`, `result_ref`, `result_ref_terminal_target`, `terminal_result_ref_protection`, `merge_signature_verification`, `failed_checks`, and `outcome`. Unknown, missing, or duplicate top-level keys => validation failure and PASS is unavailable.

The top-level values are constrained exactly as follows:

- `record_version` = `MESC-BT-PREFLIGHT-CANONICAL-ADOPTION-V1`;
- `decision_id` = `FD-MESC-BT-EXEC-1-PREFLIGHT`;
- `authorization_merge_sha`, `result_merge_sha`, `result_merge_tree`, `reviewed_result_head_sha`, `terminal_receipt_commit`, `claim_ref_target`, and `result_ref_terminal_target` are the exact verified 40-lowercase-hex Git object/target identities for this adoption;
- `activation_receipt_id`, `preflight_result_manifest_sha256`, and `terminal_receipt_sha256` are the exact verified 64-lowercase-hex SHA-256 identities;
- `ordered_parents` is exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]`, preserving that order;
- `claim_ref` and `result_ref` are the exact full refs for this authorization/receipt;
- `result_package_artifacts` is an object whose keyset is exactly the complete final manifest artifact-path set. Each value is an object containing exactly `sha256` and `byte_length`; `sha256` is the exact 64-lowercase-hex full-file digest and `byte_length` is the exact non-negative base-10 integer byte length. Unknown/missing artifact paths or unknown/missing nested keys => validation failure;
- `terminal_result_ref_protection` is an object containing exactly `mechanism_identity`, `mechanism_version`, `observed_result_ref_target`, `terminal_frozen`, and `no_configured_bypass`. The two mechanism fields are the exact non-empty NFC strings observed from the hosting boundary; `observed_result_ref_target` equals `result_ref_terminal_target`; `terminal_frozen` and `no_configured_bypass` MUST both be `true` for a verified PASS;
- `merge_signature_verification` is an object containing exactly `verified`, `reason`, `signature_sha256`, and `payload_sha256`. `verified` is the exact hosting verification boolean; `reason` is the exact non-empty NFC-normalized hosting reason string. Read the authoritative hosting `verification.signature` and `verification.payload` source values, each of which MUST be either a string or `null`. If `verification.signature` is a string, `signature_sha256 = SHA256(UTF8(exact signature text))`; if it is `null`, `signature_sha256 = null`. Apply the identical rule to `verification.payload` / `payload_sha256`. Any other source type, unavailable reason/boolean, or digest that cannot be reproduced is invalid signature evidence. A verified PASS requires `verified = true`, both source values non-null strings, and both digest fields valid 64-lowercase-hex SHA-256 values. If `verified != true` or either source value is null, PASS is unavailable even though the failure record remains deterministically serializable. For the closed `failed_checks` mapping, a well-formed object with `verified = true` but either source value null is specifically invalid signature evidence and MUST trigger `MERGE_SIGNATURE_EVIDENCE_INVALID`; this does not change the null-to-null-digest serialization rule;
- `failed_checks` uses only the closed failure-code set and exact predicate mapping below. It MUST equal the complete set of every code whose predicate fails, with no omissions or extras, serialized as a unique array sorted lexicographically by Unicode code point ascending. It is empty exactly when `outcome = CANONICAL_ADOPTION_VERIFIED` and non-empty exactly when `outcome = CANONICAL_ADOPTION_VERIFICATION_FAILED`; and
- `outcome` is exactly `CANONICAL_ADOPTION_VERIFIED` or `CANONICAL_ADOPTION_VERIFICATION_FAILED`.

The closed `failed_checks` allowlist and predicate mapping are:

| Code | Include iff this predicate fails |
|---|---|
| `ACTIVATION_RECEIPT_ID_MISMATCH` | the record/episode activation receipt ID is not the exact verified authorization receipt ID |
| `AUTHORIZATION_MERGE_SHA_MISMATCH` | the authorization merge SHA does not equal the exact verified authorization merge |
| `CLAIM_REF_MISMATCH` | `claim_ref` is not the exact authorization/receipt claim ref |
| `CLAIM_REF_TARGET_MISMATCH` | the authoritative claim-ref target is unreadable or not the exact authorization merge SHA |
| `DECISION_ID_MISMATCH` | the decision ID is not exactly `FD-MESC-BT-EXEC-1-PREFLIGHT` |
| `MERGE_SIGNATURE_EVIDENCE_INVALID` | the authoritative verification object/reason/signature/payload cannot be represented and rehashed exactly under the null-or-text rule above, **or** authoritative `verification.verified` is exactly `true` while either `verification.signature` or `verification.payload` is `null` |
| `MERGE_SIGNATURE_NOT_VERIFIED` | authoritative hosting `verification.verified` is not exactly `true` or cannot be proven `true` |
| `PREFLIGHT_RESULT_MANIFEST_MISMATCH` | the reviewed/canonical final manifest is unreadable or its exact full-file SHA-256 differs from `preflight_result_manifest_sha256` |
| `RESULT_MERGE_ORDERED_PARENTS_MISMATCH` | the canonical result merge ordered parents are not exactly `[PREMERGE_MAIN_SHA, REVIEWED_RESULT_HEAD_SHA]` |
| `RESULT_MERGE_SHA_MISMATCH` | canonical `main` after result merge is not the exact returned/verified `result_merge_sha` |
| `RESULT_MERGE_TREE_MISMATCH` | the result merge tree is not the exact expected reviewed merge tree |
| `RESULT_PACKAGE_ARTIFACT_MISMATCH` | the final artifact path set, any artifact SHA-256, or any byte length differs from the reviewed final manifest/package |
| `RESULT_REF_MISMATCH` | `result_ref` is not the exact authorization/receipt result ref |
| `RESULT_REF_TERMINAL_TARGET_MISMATCH` | the authoritative frozen result-ref target is unreadable or differs from `result_ref_terminal_target` / terminal receipt commit |
| `REVIEWED_RESULT_HEAD_MISMATCH` | `reviewed_result_head_sha` is not the exact result head that passed the pre-merge exact-head gate |
| `TERMINAL_RECEIPT_COMMIT_MISMATCH` | the terminal receipt commit is unreadable or not the exact reviewed/frozen terminal-receipt commit |
| `TERMINAL_RECEIPT_SHA256_MISMATCH` | the canonical `consumption-receipt.json` bytes are unreadable or hash differently from `terminal_receipt_sha256` |
| `TERMINAL_RESULT_REF_PROTECTION_FAILED` | terminal result-ref protection identity/version/target cannot be revalidated, or `terminal_frozen` / `no_configured_bypass` is not exactly `true` |

If an external predicate cannot be evaluated because required authoritative evidence is missing/unreadable, that predicate fails and its code MUST be included. For signature evidence specifically, the mapping is exhaustive and deterministic: an unreadable/malformed hosting verification object includes both `MERGE_SIGNATURE_EVIDENCE_INVALID` and `MERGE_SIGNATURE_NOT_VERIFIED`; a well-formed hosting verification object with `verified = true` and either authoritative source value `verification.signature = null` or `verification.payload = null` includes `MERGE_SIGNATURE_EVIDENCE_INVALID` but not `MERGE_SIGNATURE_NOT_VERIFIED`; and a well-formed unsigned hosting verification object with `verified = false`, `reason = "unsigned"`, `verification.signature = null`, and `verification.payload = null` includes `MERGE_SIGNATURE_NOT_VERIFIED` but not `MERGE_SIGNATURE_EVIDENCE_INVALID`.

Canonical unsigned signature-evidence fixture under Section B is exactly:

```json
{"payload_sha256":null,"reason":"unsigned","signature_sha256":null,"verified":false}
```

Structural errors in the adoption record itself—unknown/missing/duplicate keys, malformed JSON, or noncanonical serialization—and later adoption-record publication/path/tree-scope errors are validation failures outside this closed self-contained `failed_checks` set; they make PASS unavailable rather than inventing additional failure codes inside the record. Unknown failure codes, a missing required code for a failed predicate, or an extra code for a passing predicate => validation failure and PASS is unavailable.

Unknown, missing, or duplicate keys in `terminal_result_ref_protection` or `merge_signature_verification`, malformed artifact entries, invalid signature null/text representation, a non-deterministic or incorrectly mapped `failed_checks` array, or any value that does not mechanically revalidate => validation failure and PASS is unavailable.

After result-package merge, mechanically re-read the returned merge commit and all bound evidence and construct the exact adoption record. Its publication PR has an **exact create-only tree contract**:

1. substitute `<RESULT_MERGE_SHA>` in `ADOPTION_RECORD_PATH` with the exact `result_merge_sha` value in the record, which MUST also equal the mechanically verified canonical result merge SHA;
2. immediately before opening the adoption-verification PR, and again immediately before merging it, prove that this exact `ADOPTION_RECORD_PATH` is absent from canonical premerge `main`;
3. the adoption-verification PR/head/tree delta MUST contain exactly one changed repository path: `ADOPTION_RECORD_PATH`, with status **added/create-only**;
4. zero other additions, modifications, deletions, renames, copies, replacements, or changes to any pre-existing path are permitted; and
5. a pre-existing target path, path-SHA mismatch, non-create-only status, or any additional tree change => validation failure and PASS is unavailable.

Review that exact one-path create-only head and merge it with expected-head protection. The adoption-record path is outside `RESULT_ROOT`; the PR MUST NOT move `RESULT_REF`, rewrite `consumption-receipt.json`, or mutate any result-package byte.

`CANONICAL_ADOPTION_VERIFIED = PASS` is usable only when the adoption-record file is present on canonical `main`, has `outcome = CANONICAL_ADOPTION_VERIFIED`, and every field revalidates against the canonical result merge, reviewed result head, ordered parents, merge tree/signature evidence, final manifest/artifact digests, claim/result refs, terminal target, and terminal protection. Missing record, noncanonical record PR, missing/unreadable field, digest/signature mismatch, failed revalidation, or `outcome = CANONICAL_ADOPTION_VERIFICATION_FAILED` makes PASS unavailable and keeps the successor candidate inactive/unusable.

Any later execution authorization MUST reference the adoption-record merge SHA/tree and exact `ADOPTION_RECORD_PATH`, canonical Git blob SHA, and full-file SHA-256; it MUST re-read/re-hash/revalidate the record and still require its own separately reviewed Founder authorization. The record is evidence only and cannot create execution authority by itself. Thus a post-merge verification failure can never turn a merged `CONSUMED` preflight receipt into execution authority.

Missing/mismatched server protection, claim, result ref, activation receipt, canonical terminal receipt when terminal closure is asserted, manifest digest, lifecycle/CAS evidence, graph/tree relation, final freeze, adoption record, or state correspondence => the package is not valid for canonical execution authorization.

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

The older `readiness-repair-2-result/execution-authorization-candidate.md` remains immutable historical seed evidence and is superseded only after the V2 result package is canonically merged and the canonical adoption record revalidates to `CANONICAL_ADOPTION_VERIFIED = PASS`. No two candidate records may simultaneously claim current authority.

## H. Terminal state

The preflight may conclude:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

only when Sections A–G pass and every remaining execution blocker is truthfully recorded.

Otherwise a canonically closed terminal package may conclude:

```text
BLOCKED
```

An interrupted/burned episode that cannot canonically close remains non-reusable as `ISSUED` or `IN_PROGRESS`; it must not fabricate a terminal state. Neither a ready, blocked, nor interrupted preflight authorizes model access or execution. Only a separately reviewed and canonically adopted `FD-MESC-BT-EXEC-1` authorization, with a referenced and revalidated canonical adoption record, can do that.