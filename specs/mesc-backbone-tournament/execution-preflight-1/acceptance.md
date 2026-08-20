# Acceptance — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **CANDIDATE ACCEPTANCE CONTRACT — NO EXECUTION AUTHORITY**

Date: 2026-08-20

The preflight is complete only if every requirement below is satisfied on one exact canonical input state.

**Execution-order rule:** section letters are acceptance categories, not permission to read frozen Repair-2 content before the one-shot claim. Before the atomic claim in Section F, the worker may inspect Git/repository metadata required to identify the authorization and prove replay state—commit/tree ancestry, repository paths, Git blob IDs, ref targets, protection metadata, and the four authorization-package blob IDs—and may read/parse only **non-Repair-2 episode-governance evidence** required to classify replay/lifecycle state, such as `activation-receipt.json` / `consumption-receipt.json` reachable from discovered result-lineage commits and relevant preflight-result PR description/status fields. Such pre-claim episode evidence must itself contain no frozen Repair-2 corpus/prompt/scoring-key/contract content. The worker MUST NOT read, hash, parse, decompress, or derive values from `task-prompts.json`, corpus bytes, scoring-key bytes, or any other frozen Repair-2 artifact content until the claim is successfully created, re-verified, and the matching `activation-receipt.json` is published by the first permitted fast-forward of the protected `RESULT_REF`. Section A content-byte verification and Sections C–D therefore execute only after Section F.3.

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

### F.2 Mutually exclusive replay-state predicates and exhaustive discovery

The only permitted result-ref and claim-ref prefixes and full ref identities are:

```text
RESULT_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/
RESULT_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
CLAIM_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/
CLAIM_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
```

Each `*_REF_PREFIX` is a literal ref-name prefix, never a glob. A ref is under a prefix iff its full ref name starts with that exact prefix. The only well-formed descendant under either prefix has exactly two non-empty path segments after the prefix: `<AUTHORIZATION_MERGE_SHA>` MUST be 40 lowercase hexadecimal characters and `<ACTIVATION_RECEIPT_ID>` MUST be 64 lowercase hexadecimal characters. Any other descendant ref under either prefix => `BLOCKED`.

No other governance ref may represent this authorization episode. Before classifying the authorization as `UNUSED`, the worker MUST independently and exhaustively complete all four replay-evidence searches below from authoritative Git hosting data:

1. enumerate every ref whose full name starts with `RESULT_REF_PREFIX`;
2. enumerate every ref whose full name starts with `CLAIM_REF_PREFIX`;
3. traverse the complete canonical commit history reachable from the then-current canonical `main` tip, following every parent edge to repository roots with no shallow boundary or omitted merge parent, and inspect relevant commit/tree metadata **and non-Repair-2 episode receipts** for this decision/receipt/result evidence; and
4. enumerate the complete PR population in both open and closed/merged states and inspect every preflight-result PR metadata/description record relevant to this decision/receipt/result identity.

For **each** ref enumeration and PR enumeration, every page/cursor must be consumed until completeness is mechanically proven. Canonical-history traversal must prove that the authoritative object graph is complete and not shallow/truncated and that every reachable commit/parent edge in scope was visited. A failed request, missing object, permission limit, shallow boundary, truncation, partial pagination, omitted cursor/page, or otherwise non-exhaustive result in **any** of these four searches => `BLOCKED`; it can never support `UNUSED`.

Every descendant from both ref enumerations must pass the exact shape validation above; any malformed or unexpected descendant => `BLOCKED`. Any exact `RESULT_REF` or exact `CLAIM_REF` for this authorization/receipt is replay evidence and prevents `UNUSED`, regardless of PR or receipt presence.

An existing exact `CLAIM_REF` MUST be readable and point exactly to `AUTHORIZATION_MERGE_SHA`; unreadable or mismatched claim target => `BLOCKED`. An existing exact `RESULT_REF` MUST also be readable and its target MUST satisfy the protected lifecycle in Section F.3: the target is either exactly `AUTHORIZATION_MERGE_SHA` at initial issuance, or a permitted fast-forward descendant of that SHA on the single result lineage. The worker may read/parse non-Repair-2 episode receipt JSON and relevant PR description/status evidence pre-claim solely to reconcile that lifecycle. An unreadable target, non-descendant target, force/sideways retarget, missing required lifecycle evidence, or target inconsistent with the matching result-PR/receipt state => `BLOCKED`, never generic `IN_PROGRESS` evidence.

State is evaluated with this precedence: canonical terminal receipt → matching in-progress evidence → claim-only evidence → unused. Conflicting or ambiguous evidence overrides all normal states and is `BLOCKED`.

| State | Exact evidence predicate | May a new episode start? |
|---|---|---|
| `UNUSED` | both ref-prefix enumerations, complete canonical-history traversal, and complete open+closed/merged PR enumeration are mechanically proven exhaustive; no exact claim ref; no matching activation receipt; no exact `RESULT_REF`; no result PR for this authorization/receipt; no terminal receipt; no malformed/unexpected descendant under either prefix; no conflicting/mismatched historical evidence | YES, by atomic claim only |
| `ISSUED` | the exact protected claim ref exists and points to the authorization merge SHA; **no** activation receipt, exact `RESULT_REF`, result PR, or terminal receipt exists yet | NO |
| `IN_PROGRESS` | the exact protected claim ref exists and at least one matching activation receipt, lifecycle-valid exact `RESULT_REF`, or result PR exists; **no canonical terminal receipt** exists | NO |
| `BLOCKED` | a matching canonical terminal receipt records `state = BLOCKED`, **or** any incomplete ref/history/PR search, malformed or unexpected descendant under either prefix, claim/result-ref protection violation, deleted/retargeted claim evidence, unreadable or lifecycle-invalid result-ref target, conflicting receipt, mismatched claim target, mismatched result-ref target/state, missing required worker-CAS evidence, or ambiguous state is observed | NO |
| `CONSUMED` | a matching canonical terminal receipt records `state = CONSUMED` and matches the final ready manifest | NO |

`ISSUED` and `IN_PROGRESS` are therefore disjoint: publication/creation of any matching activation-receipt/result-ref/result-PR evidence moves the logical state from claim-only `ISSUED` to `IN_PROGRESS`. A terminal receipt supersedes both. Any state other than proven `UNUSED` => reject reuse.

### F.3 Storage-protected atomic claim and non-self-referential protected result-ref lifecycle before any frozen-content read

Before claim creation, perform only the operations permitted by the execution-order rule: verify canonical authorization/Repair-2 commit/tree ancestry and expected path→blob IDs; derive `ACTIVATION_RECEIPT_ID` from the four authorization-package blob IDs; complete both authoritative ref-prefix enumerations; complete the full canonical-history traversal; complete the full open+closed/merged PR enumeration; read/parse only the non-Repair-2 episode-governance receipts and PR description/status evidence necessary to reconcile discovered lifecycle state; validate every discovered ref shape and every existing exact claim/result-ref target against this contract; and classify replay state. Do **not** read any frozen Repair-2 blob contents. Failure to prove completeness or integrity of any replay search/target => `BLOCKED` before claim creation.

Before creating either episode ref, mechanically verify storage-boundary protection at the Git hosting boundary:

- `CLAIM_REF_PROTECTION = PASS` for every ref whose full name starts with `CLAIM_REF_PREFIX`; and
- `RESULT_REF_PROTECTION = PASS` for every ref whose full name starts with `RESULT_REF_PREFIX`.

`CLAIM_REF_PROTECTION` must be a repository ruleset, server-side hook, or equivalent durable control that:

1. permits the controlled initial claim creation;
2. denies every subsequent claim update, including ordinary fast-forward and force updates;
3. denies claim deletion;
4. gives the preflight worker no bypass capable of claim update/deletion after creation; and
5. remains effective from immediately before claim creation through canonical terminal result adoption.

`RESULT_REF_PROTECTION` is the **server-enforced invariant set**. It must be a repository ruleset, server-side hook, or equivalent durable control that:

1. permits controlled initial `RESULT_REF` creation only at `AUTHORIZATION_MERGE_SHA`;
2. permits subsequent updates only by the designated preflight principal and only as ordinary fast-forwards;
3. denies force updates, non-fast-forward/sideways retargets, deletion, recreation, and updates by any other principal;
4. requires every accepted new target to remain a descendant of `AUTHORIZATION_MERGE_SHA` on the single episode result lineage;
5. remains effective through terminal result construction and canonical adoption; and
6. after the exact terminal receipt commit is published and verified, enters a frozen state that denies every further update and deletion.

`RESULT_REF_CAS_PROTOCOL` is a separate **worker protocol obligation**, not a property attributed to `RESULT_REF_PROTECTION`. Every post-creation `RESULT_REF` update MUST use one atomic compare-and-update operation that supplies all of: full ref name, `expected_old_oid` equal to the immediately re-read 40-hex current target, and `new_oid`. The operation must have server-side atomic semantics: it accepts the update only if the ref still equals `expected_old_oid` and all server protection invariants pass; otherwise it rejects without changing the ref. A normal Git receive-pack ref-update command carrying old OID/new OID/ref, or a hosting API/hook operation with an equivalent explicit old-OID precondition, qualifies. A separate read followed by an unconditional ref PATCH/update does **not** qualify.

For every attempted result-ref update, preserve `RESULT_REF_CAS_EVIDENCE` outside the commit being published, containing at minimum: operation/protocol identity, full ref name, `expected_old_oid`, `new_oid`, accepted/rejected outcome, and the immediately observed post-operation target. This may be authoritative hosting/receive-pack audit evidence and may later be copied into result-package governance evidence; it is not required to be embedded in the commit whose SHA is being established. If the hosting boundary cannot provide an atomic old-OID-precondition operation or the worker cannot preserve/reconcile this evidence, the episode is `BLOCKED` and the update must not be treated as valid lifecycle evidence.

Record the exact claim/result **server-protection** mechanism identities and observed enforcement facts in `activation-receipt.json` and carry them into `consumption-receipt.json`. Record the selected `RESULT_REF_CAS_PROTOCOL` identity in the activation receipt; record/reconcile the externally observed per-update `RESULT_REF_CAS_EVIDENCE` in later result/terminal governance evidence once those updates have occurred. If either server protection cannot be proven, or no qualifying CAS protocol exists, do not create the claim and terminate `BLOCKED` before any frozen-content read.

Then atomically create exactly `CLAIM_REF`. The claim ref MUST use create-only semantics, only if absent, and MUST point exactly to `AUTHORIZATION_MERGE_SHA`. Creation failure because the ref already exists means another worker/episode already claimed the authorization: stop immediately without changing the ref or starting audit work.

Immediately after creation, re-read the claim ref and both protection controls. Any missing/changed claim target or protection drift is `BLOCKED`. Updating, force-updating, retargeting, deleting, or recreating the claim is prohibited. If a claim is ever observed deleted or changed after creation, the episode can never be classified `UNUSED`; the observing worker must preserve durable `BLOCKED` evidence if possible and stop. Absence of a terminal receipt never restores `UNUSED` after a claim has existed.

After successful claim creation and re-verification, atomically create exactly `RESULT_REF` with create-only semantics at `AUTHORIZATION_MERGE_SHA`. Creation failure because `RESULT_REF` already exists => `BLOCKED` and no frozen content may be read. Immediately re-read `RESULT_REF` and `RESULT_REF_PROTECTION`; any unreadable/mismatched initial target or protection drift => `BLOCKED`.

The only permitted `RESULT_REF` update sequence is then:

1. Construct `activation-receipt.json` and an activation commit whose **single parent is exactly `AUTHORIZATION_MERGE_SHA`**. The receipt may record `result_ref_activation_parent = AUTHORIZATION_MERGE_SHA` and the selected `RESULT_REF_CAS_PROTOCOL`, but it MUST NOT contain the SHA of the activation commit that contains it. The activation commit may add only the episode bootstrap/result metadata required to publish that receipt and must not contain any frozen Repair-2 content read or derived-content result.
2. After the activation commit object exists and its SHA is therefore known, immediately re-read `RESULT_REF`, require exactly `AUTHORIZATION_MERGE_SHA`, then invoke `RESULT_REF_CAS_PROTOCOL` with `expected_old_oid = AUTHORIZATION_MERGE_SHA` and `new_oid = <activation commit SHA>`. Preserve the external `RESULT_REF_CAS_EVIDENCE`.
3. Re-read `RESULT_REF`; require it to equal the exact observed activation commit SHA; inspect that commit and require its single parent to equal `AUTHORIZATION_MERGE_SHA` and its tree to contain the exact expected activation-receipt bytes; reconcile the CAS evidence's observed target. Only after this succeeds is activation receipt publication complete and frozen Repair-2 content access permitted. The observed activation commit SHA is thereafter `RESULT_REF_ACTIVATION_COMMIT` and may be recorded in later artifacts because it is no longer self-referential.
4. Later episode result commits may advance `RESULT_REF` only by the same immediately-re-read + atomic old-OID-precondition CAS protocol, ordinary-fast-forward rule, server protections, and externally preserved CAS evidence on that single lineage.
5. When result artifacts are byte-final for a terminal outcome, construct `TERMINAL_CONTENT_COMMIT` on the current result lineage. It contains the final result package and final `preflight-result-manifest.json` but **does not contain `consumption-receipt.json`**. After the commit object exists, its SHA is known; immediately re-read the current ref, then CAS from exactly that observed old OID to `TERMINAL_CONTENT_COMMIT`, preserve CAS evidence, and re-read/reconcile the exact target.
6. Construct `consumption-receipt.json` binding the already-known `RESULT_REF_ACTIVATION_COMMIT`, `TERMINAL_CONTENT_COMMIT`, final manifest SHA-256, claim/ref identities, server protections, reconciled lifecycle/CAS evidence, and terminal state. Then construct `TERMINAL_RECEIPT_COMMIT` as the direct child of `TERMINAL_CONTENT_COMMIT`; relative to its parent it may add only `consumption-receipt.json` and may not alter any bound result artifact. The receipt MUST NOT contain the SHA of `TERMINAL_RECEIPT_COMMIT` itself.
7. After `TERMINAL_RECEIPT_COMMIT` exists and its SHA is known, immediately re-read and require `RESULT_REF = TERMINAL_CONTENT_COMMIT`; invoke the qualifying CAS operation with `expected_old_oid = TERMINAL_CONTENT_COMMIT` and `new_oid = TERMINAL_RECEIPT_COMMIT`; preserve/reconcile CAS evidence; re-read and inspect the exact commit/parent/tree relation; then freeze `RESULT_REF` against every later update/delete through and after canonical result adoption. The observed receipt-commit SHA is external terminal-ref evidence and is recorded in the result PR description, not inside its own receipt.

Any skipped immediate re-read, missing/invalid atomic old-OID precondition, missing/unreconciled CAS evidence, unexpected updater, force/non-fast-forward update, deletion/recreation, unreadable target, ancestry break, self-referential commit-SHA field, receipt/content mutation outside the permitted closure steps, or observed target that cannot be reconciled with this exact sequence => `BLOCKED` and permanently prevents `UNUSED`.

The activation receipt must reproduce the receipt preimage and `ACTIVATION_RECEIPT_ID`, record the exact `claim_ref` and target, record `result_ref = RESULT_REF`, `result_ref_activation_parent = AUTHORIZATION_MERGE_SHA`, both verified server-protection mechanism identities/enforcement facts, the selected `result_ref_cas_protocol`, `state = IN_PROGRESS`, and `content_read_started = false`. It MUST NOT record its containing activation commit SHA or the outcome evidence for the update that publishes itself. The receipt-state field is the replay state after receipt publication; it is therefore `IN_PROGRESS`, not `ISSUED`. Only after the protected activation CAS fast-forward is re-read, structurally verified, and reconciled with external CAS evidence may Section A content verification and Sections C–D begin. `content_read_started = false` records the issuance-time fact and is not a separate replay state.

### F.4 Non-self-referential terminal receipt and terminal result-ref freeze

A claimed episode that reaches terminal-package construction must close with `consumption-receipt.json` outside the result-manifest artifact set. It is canonical JSON under Section B and contains exactly:

- `receipt_version = MESC-BT-PREFLIGHT-TERMINAL-RECEIPT-V1`;
- `activation_receipt_id`;
- `activation_receipt_preimage`;
- `claim_ref`;
- `claim_ref_target`;
- `claim_ref_protection` containing the exact server-protection mechanism identity and terminal re-verification facts;
- `result_ref`;
- `result_ref_activation_commit`, equal to the already-observed activation commit SHA;
- `result_ref_terminal_content_commit`, equal to the already-observed `TERMINAL_CONTENT_COMMIT` SHA;
- `result_ref_protection` containing the exact server-protection mechanism identity, permitted-lifecycle evidence, and terminal re-verification facts required before freeze;
- `result_ref_cas_protocol` and reconciled external CAS-evidence identities/records for every accepted lifecycle update through `TERMINAL_CONTENT_COMMIT`;
- `preflight_result_manifest_sha256`;
- `terminal_state`, exactly `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` or `BLOCKED`;
- `state`, exactly `CONSUMED` when `terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, otherwise exactly `BLOCKED`.

The terminal receipt MUST NOT contain `TERMINAL_RECEIPT_COMMIT` or any other field whose value would be the SHA of the commit containing that receipt. CAS outcome evidence for the final update that publishes `TERMINAL_RECEIPT_COMMIT` is necessarily external and is recorded/reconciled in the result PR description and hosting audit evidence after that commit exists.

Terminal closure is mechanically verified in this order:

1. before creating the receipt, re-read `CLAIM_REF`, `RESULT_REF`, and both server protections; `CLAIM_REF` must still point exactly to `AUTHORIZATION_MERGE_SHA`, while `RESULT_REF` must point exactly to the already-created `TERMINAL_CONTENT_COMMIT` and that commit must be a permitted descendant on the single episode lineage; reconcile all prior CAS evidence;
2. create the canonical receipt binding that already-known content commit and final manifest SHA-256;
3. create `TERMINAL_RECEIPT_COMMIT` as a direct child of `TERMINAL_CONTENT_COMMIT`, with the tree delta limited exactly to adding `consumption-receipt.json` and no changes to any bound result artifact;
4. immediately re-read `RESULT_REF`, require exactly `TERMINAL_CONTENT_COMMIT`, then invoke the qualifying atomic CAS operation with expected old OID equal to `TERMINAL_CONTENT_COMMIT` and new OID equal to the observed receipt-commit SHA;
5. preserve final external CAS evidence; re-read `RESULT_REF`, require the exact observed receipt-commit SHA, require that commit's single parent to equal `result_ref_terminal_content_commit`, re-verify the receipt bytes and all bound result artifacts, reconcile the final CAS evidence, then activate the terminal frozen server protection that denies all further result-ref update/delete; and
6. record the external observed `TERMINAL_RECEIPT_COMMIT` SHA, final CAS evidence identity/record, and final manifest SHA-256 in the result PR description for independent verification.

A successful package therefore records `state = CONSUMED`; a blocked package records `state = BLOCKED`. Both bind the exact final manifest SHA-256 and matching activation identity without any commit-SHA self-reference. The terminal receipt is not included in the manifest hash set.

Canonical merge of the result package is the durable terminal-state transition. The protected claim ref remains permanent in either outcome, and the frozen `RESULT_REF` remains permanent at the externally observed `TERMINAL_RECEIPT_COMMIT`. A claimed episode that cannot reach terminal receipt closure remains burned/non-reusable: the permanent claim, any result ref, activation receipt, PR evidence, or historical evidence prevents `UNUSED`. It requires a new separately reviewed Founder authorization rather than a restart; a terminal receipt is not required to prove that such an interrupted claimed episode is non-reusable.

Missing/mismatched server protection, claim, result ref, activation receipt, terminal receipt when terminal closure was reached, manifest digest, lifecycle/CAS evidence, parent/tree closure relation, or state correspondence => `BLOCKED`.

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