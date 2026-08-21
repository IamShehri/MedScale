# MESC Backbone Tournament — Execution Preflight 1

Status: **FOUNDER-AUTHORIZATION CANDIDATE / NO EXECUTION AUTHORITY**

Date: 2026-08-20

Decision identity: `FD-MESC-BT-EXEC-1-PREFLIGHT`

Canonical Repair-2 identity at proposal time:

```text
MAIN_SHA = 0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3
MAIN_TREE = 60e900daecea1cb9e64db95314bf9358387072b7
REPAIR_2_CANONICAL_MERGE_SHA = 0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3
REPAIR_2_CANONICAL_TREE = 60e900daecea1cb9e64db95314bf9358387072b7
BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE
```

The historical PR number is not an activation predicate. `acceptance.md` requires deterministic Git ancestry against the exact Repair-2 merge SHA/tree above.

## Purpose

This package authorizes only the deterministic pre-execution evidence work required before `FD-MESC-BT-EXEC-1` can be proposed for activation.

It does **not** authorize model access, prompt serialization, inference, generation, or tournament execution.

The episode may produce only:

1. a deterministic R2 provenance audit over the already-frozen 240-item corpus;
2. a deterministic corpus-specification/manifest conformance audit over the same frozen corpus;
3. exact audit and result-package SHA-256 bindings under the serialization rules in `acceptance.md`;
4. a fail-closed execution-binding inventory identifying what is still unbound;
5. a uniquely identified successor candidate, `FD-MESC-BT-EXEC-1-CANDIDATE-V2`, only through the provisional-and-final lifecycle defined in `acceptance.md`;
6. the activation and terminal receipts required to prove one-shot consumption.

The existing `readiness-repair-2-result/execution-authorization-candidate.md` remains immutable historical seed evidence. A successful preflight must **not** edit or duplicate its authority. Instead it may produce the single successor candidate at:

`specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md`

That successor becomes the sole authoritative inactive execution-authorization candidate only after the entire preflight result package is separately reviewed, merged, and post-merge verified. Until then, the historical seed remains the only canonical candidate record and no execution authority exists.

## Frozen inputs

The preflight must consume the exact canonical Repair-2 artifacts without substitution or rematerialization:

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
REPORT_VALIDATION_CONTRACT_SHA256 = c68fcac507e4ebc164632370d2392631b9fec9c388369eb5b8bfa495e5877c1a
SCORING_CONTRACT_SHA256 = a61471d467521b59eb62ee2825d23fa15891bb45a664360aaf2e4ef5882c7d40
PROTOCOL_CONFIG_SHA256 = 097cdd11f5389203cf432760ec316a78b12d157c0676477de69dde707e058203
PROMPT_PROTOCOL_SHA256 = a2a42aef340e27f9396b40810999d5f2c4136af467ce27ee9e3c149e3257c89c
REPORT_SCHEMA_SHA256 = cb3fc506b41cc6236959bb4a89bce249db13c99aeb0c7178ff233f6de44e026d
```

Every frozen binding above is mandatory.

The exact Repair-2 repository object map is:

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

`SYSTEM_PROMPT_SHA256` derives only from the exact `system_prompt` string in the bound `task-prompts.json`. `PROMPT_PROTOCOL_SHA256` derives only from the exact version/system-prompt/prompt-bundle/protocol-config preimage defined in `acceptance.md`. The canonical Repair-2 `corpus-manifest.json` remains authoritative for per-shard SHA-256/count/byte-length values.

## One-shot activation and replay protection

Canonical activation does not itself start the episode. After merge and post-merge verification, `acceptance.md` requires an exact receipt preimage over the canonical authorization merge SHA/tree plus an ordered four-file authorization-package path/blob map.

Before any audit or corpus-content inspection, the worker must prove the episode is `UNUSED` and atomically create the immutable claim ref defined in `acceptance.md`. Any existing claim or `ISSUED`, `IN_PROGRESS`, `BLOCKED`, or `CONSUMED` state rejects reuse. Competing workers must stop; no claim ref may be updated, deleted, or reused.

Every claimed episode terminates with a hash-bound `consumption-receipt.json`: `state = CONSUMED` for `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, or `state = BLOCKED` for a blocked episode.

## Preflight result binding

The four unconditional core outputs are:

- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`.

If `FD-MESC-BT-EXEC-1-CANDIDATE-V2` is provisionally rendered, `execution-authorization-candidate.md` is a conditional fifth bound result artifact. Its exact path, SHA-256, and byte length must be included in the non-circular manifest binding defined in `acceptance.md`. Provisional rendering grants no authority; any later failure removes it and rebuilds the blocked package with `successor_candidate = null`.

The verdict must reference the binding-core SHA-256. `preflight-result-manifest.json` binds all material result artifacts. The terminal `consumption-receipt.json` binds the exact final manifest SHA-256 and is outside the manifest artifact set, so no digest cycle exists.

## Hard boundary

Until a later `FD-MESC-BT-EXEC-1` package is separately canonically adopted:

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
