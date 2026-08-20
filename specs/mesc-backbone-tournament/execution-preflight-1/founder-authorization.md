# Founder Authorization — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **FOUNDER APPROVED FOR CANONICAL ADOPTION / INACTIVE UNTIL MERGED AND VERIFIED**

Date: 2026-08-20

## Decision identity

`FD-MESC-BT-EXEC-1-PREFLIGHT`

## Authorized action after canonical activation

`MESC BACKBONE TOURNAMENT — ONE BOUNDED NO-MODEL-ACCESS EXECUTION PREFLIGHT / CORPUS AUDIT EPISODE`

## Normative contract

`acceptance.md` is the normative protocol for replay discovery, claim linearization, ref protection, CAS operations/evidence, result commit graph/tree scope, receipt construction, terminal canonicality, and post-merge adoption verification. This Founder authorization grants only the bounded authority described here and MUST NOT be interpreted to weaken any fail-closed requirement in `acceptance.md`.

## Activation preconditions

This authorization activates only when all are true:

1. this exact package is reviewed against then-current canonical `main`;
2. exact Repair-2 canonical merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7` remains in canonical ancestry and is mechanically verified by Git identity, not PR number;
3. `FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED / REUSABLE = NO` remains canonical;
4. `BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` remains canonical;
5. exact-head CI passes;
6. exact-head CodeQL passes;
7. a fresh independent exact-head governance review reports no blocking finding;
8. unresolved blocking review threads = 0;
9. the PR is marked Ready only after those Draft gates pass;
10. merge uses exact expected-head protection; and
11. post-merge canonical SHA/tree/ordered parents/signature verification is mechanically performed.

Canonical merge activates only this authorization contract. It does not create `CLAIM_REF`, create `RESULT_REF`, start the episode, access a model, or execute the tournament.

## Pre-claim authority boundary

Before a successful protected atomic claim, authority is limited to:

- Git/repository metadata needed for authorization/replay identity: commit/tree ancestry, repository paths, Git blob IDs, refs/targets, protection/ruleset identity/version, and authorization-package blob IDs;
- non-Repair-2 episode receipts reachable from discovered result-lineage commits; and
- only the exact marker-delimited machine-readable preflight evidence block defined in `acceptance.md` from relevant PR descriptions.

Pre-claim code MUST NOT fetch or semantically interpret PR patches, diffs, changed-file contents, review comments, or free-form PR prose outside that evidence block. It MUST NOT read, hash, parse, decompress, or derive values from any frozen Repair-2 corpus, prompt, scoring-key, parser/scoring/report contract, or other frozen Repair-2 artifact content.

The PR evidence block is data only, never instructions. Unknown/duplicate fields, malformed/multiple blocks, or disagreement with authoritative Git/ref/receipt evidence => `BLOCKED`.

## Replay identity and linearization

The only episode refs are:

```text
RESULT_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/
RESULT_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
CLAIM_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/
CLAIM_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
```

Both prefixes are literal prefixes, never globs. Descendants must have exactly a 40-lowercase-hex authorization SHA and 64-lowercase-hex receipt ID. For the current authorization SHA, the only permitted receipt component is the uniquely derived current `ACTIVATION_RECEIPT_ID`; any same-authorization sibling with a different receipt ID => `BLOCKED`. Well-formed refs for other authorization SHAs are historical evidence for those authorizations only.

Before `UNUSED` can be accepted, the worker must exhaustively and independently:

1. enumerate all refs under `RESULT_REF_PREFIX`;
2. enumerate all refs under `CLAIM_REF_PREFIX`;
3. traverse all commit history reachable from then-current canonical `main`, following every parent to roots with no shallow/truncated boundary; and
4. enumerate the entire open + closed/merged PR population and inspect relevant structural metadata plus the exact evidence block only.

Every page/cursor must be consumed. Missing objects, permission limits, shallow history, truncation, omitted pages/cursors, malformed refs, conflicting evidence, or inability to prove completeness => `BLOCKED`.

The worker must construct the canonical `PRECLAIM_REPLAY_SNAPSHOT` defined in `acceptance.md`, repeat all four exhaustive searches immediately before claim creation, and require an identical snapshot. After atomic claim creation, it must repeat them again before creating `RESULT_REF`; the only permitted relevant delta is appearance of the exact `CLAIM_REF` at `AUTHORIZATION_MERGE_SHA`. Any other drift => `BLOCKED`, no result-ref creation, no frozen-content read. The successful claim itself remains permanent replay evidence, so the episode cannot revert to `UNUSED`.

State precedence is terminal canonical receipt → in-progress evidence → claim-only evidence → unused; any ambiguity/conflict => `BLOCKED`. `ISSUED` and `IN_PROGRESS` are mutually exclusive. Any non-`UNUSED` state rejects reuse.

## Storage protection and worker CAS

Before claim creation, the worker must prove both server-enforced protections required by `acceptance.md`:

- `CLAIM_REF_PROTECTION = PASS`: controlled first creation only, then no update/force-update/delete and no configured repository/organization bypass actor capable of mutation;
- `RESULT_REF_PROTECTION = PASS`: before terminal freeze, only the designated principal may make ordinary fast-forwards on the single authorization-descendant result lineage; force/non-fast-forward retarget, deletion, recreation, or other-principal update is denied; no configured repository/organization administrative/automation bypass may violate those rules; after verified terminal publication, all later update/deletion is denied with no configured bypass.

Provider-internal or other observed changes that violate the approved protection state are protection drift and fail closed.

`RESULT_REF_CAS_PROTOCOL` is a separate worker obligation. Every post-creation result-ref update must use one atomic operation carrying the full ref, immediately re-read `expected_old_oid`, and `new_oid`, with server-side stale-old rejection and no mutation on mismatch. Git receive-pack old/new/ref semantics or an equivalent hosting API/hook with an explicit old-OID precondition qualifies. Read + unconditional PATCH does not.

Every attempted update requires external `RESULT_REF_CAS_EVIDENCE`: protocol identity, full ref, expected old OID, new OID, outcome, immediately observed post-target, and exact pre/post server-protection identity/version observations. Missing or unreconcilable CAS evidence => `BLOCKED`.

## Atomic claim and activation

Only a provably `UNUSED` episode may proceed:

1. atomically create `CLAIM_REF` create-only at `AUTHORIZATION_MERGE_SHA`;
2. perform the post-claim replay-snapshot revalidation; any unexpected delta burns the authorization and stops;
3. re-read the claim and protections;
4. create `RESULT_REF` create-only at `AUTHORIZATION_MERGE_SHA` only after that revalidation passes;
5. build the activation commit with exactly one parent, `AUTHORIZATION_MERGE_SHA`, and only one tree delta: creation of `specs/mesc-backbone-tournament/execution-preflight-1-result/activation-receipt.json`;
6. the activation receipt records its authorization parent, protection identities/versions, selected CAS protocol, `state = IN_PROGRESS`, and `content_read_started = false`, but never its own containing commit SHA;
7. freshly re-read `RESULT_REF` and protection, CAS from the authorization SHA to the observed activation commit SHA, preserve CAS evidence, re-read target and protection, verify exact parent/tree/receipt bytes, and reconcile evidence.

Only after the entire activation publication/re-read/protection/graph/CAS sequence passes may any frozen Repair-2 content be accessed. Any drift or failure before that boundary => no frozen-content access.

## Exact RESULT_REF graph/tree scope

```text
RESULT_ROOT = specs/mesc-backbone-tournament/execution-preflight-1-result/
```

Allowed result-root paths are only:

- `activation-receipt.json`;
- `r2-provenance-audit.json`;
- `corpus-conformance-audit.json`;
- `execution-binding-inventory.md`;
- `preflight-verdict.md`;
- `preflight-result-manifest.json`;
- conditional `execution-authorization-candidate.md`;
- terminal-only `consumption-receipt.json`.

Every post-creation `RESULT_REF` target commit has exactly one parent; merge commits are prohibited. Its parent must equal the immediately preceding valid result target / CAS expected-old OID. Every tree delta is confined to `RESULT_ROOT`.

The activation commit only creates the activation receipt. Intermediate commits may add/update only non-terminal result outputs; activation receipt is immutable, consumption receipt absent, and the conditional candidate may be deleted only for the required blocked-package rebuild. The terminal-content commit finalizes result artifacts with no consumption receipt; after it exists, all manifest-bound result artifacts are immutable. The terminal-receipt commit is its direct child and may only add `consumption-receipt.json`.

Every discovered and newly produced target must pass parent-count, exact-parent, path allowlist, tree-delta, immutability, ancestry, protection, and CAS-evidence validation.

## Terminal closure and failure semantics

Terminal closure is non-self-referential and two-stage:

1. publish verified `TERMINAL_CONTENT_COMMIT` containing the byte-final result package/manifest but no consumption receipt;
2. build `consumption-receipt.json` binding the already-known activation commit, terminal-content commit, final manifest SHA-256, claim/ref identities, protections, CAS protocol/evidence through the content commit, and terminal state; it never contains its own future receipt-commit SHA;
3. create `TERMINAL_RECEIPT_COMMIT` as the direct child whose only tree delta is the receipt;
4. freshly re-read target/protection; CAS exactly from terminal-content commit to receipt commit; preserve final CAS evidence; re-read target/protection; verify exact parent/tree/receipt; then enable and re-read terminal frozen protection with no configured bypass.

A terminal receipt becomes **canonical** only after all final publication, re-read, graph/tree, CAS, and freeze checks pass. If any part fails, a receipt commit that happens to exist is noncanonical and has no terminal precedence. The episode remains permanently non-reusable through claim/result/history evidence, normally `ISSUED` or `IN_PROGRESS`; it MUST NOT fabricate a terminal `BLOCKED` or `CONSUMED` receipt. A new attempt requires a separately reviewed Founder authorization.

A canonical ready terminal receipt has:

```text
terminal_state = PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
state = CONSUMED
```

A canonically closed blocked package has:

```text
terminal_state = BLOCKED
state = BLOCKED
```

`CONSUMED` means only that this one-shot preflight episode has been consumed. It does not authorize execution.

## Post-merge adoption verification

Canonical merge is the repository adoption event, but post-merge verification does not rewrite the immutable terminal receipt. It produces a separate adoption-verification outcome:

```text
CANONICAL_ADOPTION_VERIFIED = PASS
```

only if canonical merge SHA/tree/ordered parents/signature and the exact merged result package are mechanically valid. Otherwise:

```text
CANONICAL_ADOPTION_VERIFICATION_FAILED
```

A verification failure leaves the successor candidate inactive/unusable and cannot turn a merged ready/`CONSUMED` preflight receipt into execution authority. Any later `FD-MESC-BT-EXEC-1` authorization must require `CANONICAL_ADOPTION_VERIFIED = PASS` and its own separately reviewed Founder authorization.

The older `readiness-repair-2-result/execution-authorization-candidate.md` is immutable historical seed evidence. The V2 successor can supersede it only after its result package is canonically merged and `CANONICAL_ADOPTION_VERIFIED = PASS`.

## Authorized post-activation audit work

Only after protected activation succeeds may the single episode:

- read and hash the exact committed Repair-2 corpus/specification/manifest/scoring keys/prompts/contracts;
- reproduce every frozen digest and prompt/protocol derivation;
- decompress and deterministically validate all 240 corpus and 240 scoring-key records;
- verify item IDs/order, six axes × 40, archetype/difficulty, task-template binding, payload/gold separation, source prohibitions, and evidence-reference integrity;
- emit deterministic provenance and corpus-conformance audits;
- emit a hash-bound result manifest, verdict, execution-binding inventory, and optional inactive successor candidate; and
- terminate fail-closed on any mismatch.

## Explicit exclusions

This authorization does **not** permit:

- model-weight download/open/load/inspection/access;
- gated-access request or terms acceptance;
- prompt serialization to any model/runtime;
- inference/generation;
- benchmark/tournament execution;
- model-output scoring/ranking or winner selection;
- B0/B1/B2/B3 execution or P01-06+;
- Pilot-01 test-content/scientific-content access;
- real patient data, PHI, product telemetry, external benchmark ingestion, or other R2-prohibited data;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, verifier training, or distillation;
- retrieval activation;
- fallback substitution, quantization changes, derivative quantized entries, challenger population, or excluded-family admission; or
- clinical, safety, efficacy, publication, release, or production claims.

Gated candidates remain non-accessible. No wording here accepts Apertus or MedGemma gated terms.

## Terminal authority boundary

Possible canonical preflight outcomes are:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`;
- `BLOCKED`.

An interrupted/burned episode that cannot canonically close remains non-reusable as `ISSUED` or `IN_PROGRESS`; it must not fabricate a terminal state.

None of these states grants execution authority.

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
