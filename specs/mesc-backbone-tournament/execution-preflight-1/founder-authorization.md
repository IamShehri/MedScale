# Founder Authorization — FD-MESC-BT-EXEC-1-PREFLIGHT

Status: **FOUNDER APPROVED FOR CANONICAL ADOPTION / INACTIVE UNTIL MERGED AND VERIFIED**

Date: 2026-08-20

## Decision identity

`FD-MESC-BT-EXEC-1-PREFLIGHT`

## Authorized action after canonical activation

`MESC BACKBONE TOURNAMENT — ONE BOUNDED NO-MODEL-ACCESS EXECUTION PREFLIGHT / CORPUS AUDIT EPISODE`

## Activation preconditions

This authorization activates only when all are true:

1. this exact package is reviewed against then-current canonical `main`;
2. exact Repair-2 canonical merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7` remains in canonical ancestry and is mechanically verified by Git identity, not PR number;
3. `FD-MESC-BT-READINESS-REPAIR-2 = CONSUMED / REUSABLE = NO` remains canonical;
4. `BACKBONE_TOURNAMENT_READINESS = READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` remains canonical;
5. exact-head CI passes;
6. exact-head CodeQL passes;
7. a fresh independent exact-head governance review reports no unresolved blocking findings;
8. all review threads are resolved or explicitly dispositioned with evidence;
9. the package is marked Ready only after those gates pass;
10. merge uses exact expected-head protection;
11. post-merge canonical main/tree/ordered parents/signature are mechanically verified.

Canonical merge activates only this authorization contract. It does not itself start or claim the one-shot episode.

## Authority if activated

Before the one-shot claim succeeds, authority is limited to Git/repository metadata needed to identify this canonical authorization and prove replay/claim state: commit/tree ancestry, repository paths, Git blob IDs, result-PR metadata, claim-ref metadata, claim-protection metadata, and the four authorization-package blob IDs. **No frozen Repair-2 artifact content may be read, hashed, parsed, decompressed, or used for a derived digest before the protected atomic claim and matching activation receipt are established exactly as required by `acceptance.md`.**

Only after that protected claim and activation receipt exist may the single episode:

- read the exact committed Repair-2 corpus, corpus specification, manifest, scoring keys, prompts, parser/scoring/report contracts, and their Git-object contents;
- verify all frozen byte-level SHA-256 and prompt/protocol derivations;
- decompress the exact committed corpus locally and compute deterministic byte lengths and SHA-256 values;
- run deterministic local validation over all 240 committed corpus records and all 240 scoring-key records;
- verify exact item-ID membership/order, six 40-item axes, archetype/difficulty assignment, task-template bindings, answer-state/scoring-key compatibility, evidence-reference integrity, payload/gold separation, and frozen R2 source prohibitions;
- generate deterministic `R2_PROVENANCE_AUDIT` and `CORPUS_SPEC_MANIFEST_CONFORMANCE_AUDIT` artifacts under the exact canonical serialization rule in `acceptance.md`;
- generate a fully hash-bound preflight result manifest, verdict, execution-binding inventory, activation receipt, and terminal receipt;
- record negative audit findings as first-class evidence and terminate `BLOCKED` on any mismatch;
- inspect public, ungated candidate/runtime metadata read-only only when needed to inventory remaining execution bindings;
- record exact hardware/provider/runtime facts only when they are actually observed and independently identifiable;
- propose, but not activate, a candidate subset of at least two previously admitted candidates.

### Successor-candidate lifecycle

After Sections A–D of `acceptance.md` PASS and the execution-binding inventory is complete and truthful for the provisional ready path, the episode may render exactly one provisional `FD-MESC-BT-EXEC-1-CANDIDATE-V2` at:

`specs/mesc-backbone-tournament/execution-preflight-1-result/execution-authorization-candidate.md`

That provisional file exists solely to compute the Section E manifest binding. It grants no authority and is not yet a valid output. It becomes a valid inactive preflight output only if all acceptance sections pass and the terminal state is `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`.

If any later acceptance, claim, receipt, binding, review, or package check fails, the provisional successor must be removed, `successor_candidate` must be set to `null`, and the blocked manifest/verdict package must be rebuilt with fresh hashes.

The existing `readiness-repair-2-result/execution-authorization-candidate.md` is immutable historical seed evidence. It is superseded only if the V2 successor is later canonically merged and post-merge verified; until then it remains the only canonical candidate record.

## Explicit exclusions

This authorization does **not** permit:

- downloading, opening, loading, inspecting, or accessing model weights;
- requesting or accepting gated model access;
- accepting gated-access terms or model-access agreements;
- serializing any tournament prompt to any model endpoint/runtime;
- inference or generation;
- benchmark/tournament execution;
- scoring or ranking model outputs;
- selecting a Compact or Flagship/Reasoner winner;
- B0/B1/B2/B3 execution or P01-06+;
- Pilot-01 test-content access or scientific-content inspection;
- real patient data, PHI, product telemetry, or other R2-prohibited data;
- external benchmark ingestion;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, verifier training, or distillation;
- retrieval activation;
- fallback substitution;
- quantization changes or derivative quantized entries;
- challenger population;
- excluded model-family admission;
- clinical, safety, efficacy, publication, release, or production claims.

## Fail-closed rules

Any mismatch in committed corpus/storage/logical/scoring-key identity, any missing frozen protocol-contract binding, any non-canonical item ID, any prohibited source indication, any gold leakage into model-visible payload, any unresolved evidence-reference mismatch, any duplicate JSON member name in a canonicalized preflight object, any result-package hash mismatch, any pre-claim frozen-content read, any missing/mismatched claim or receipt, any missing or bypassable storage-boundary claim protection, any deleted/retargeted/updated claim after creation, any conflicting replay-state evidence, or any inability to reproduce a required audit deterministically => `BLOCKED`.

Gated candidates remain non-accessible during this episode. No wording in this authorization constitutes acceptance of Apertus or MedGemma gated terms.

## Atomic single-use claim, receipt, protection, and consumption rule

This decision is single-use and replay-resistant. `acceptance.md` is normative for the exact receipt preimage, claim-ref namespace, storage-boundary protection requirements, canonical JSON encoding, state predicates, and terminal receipt shape.

State evaluation uses this exact precedence: canonical terminal receipt → matching in-progress evidence → protected claim-only evidence → unused. Conflicting or ambiguous evidence is `BLOCKED`.

| State | Exact predicate | New episode allowed? |
|---|---|---|
| `UNUSED` | no claim ref, activation receipt, result branch/PR, terminal receipt, or conflicting evidence for this authorization/receipt | YES, only by successful protected atomic claim |
| `ISSUED` | exact protected claim exists at the exact authorization merge SHA, with no activation receipt, result branch/PR, or terminal receipt | NO |
| `IN_PROGRESS` | exact protected claim exists and matching activation-receipt/result-branch/result-PR evidence exists, with no canonical terminal receipt | NO |
| `BLOCKED` | canonical blocked terminal receipt, or any protection violation, deleted/changed claim evidence, conflicting receipt, mismatched target, or ambiguous state | NO |
| `CONSUMED` | canonical consumed terminal receipt matches the final ready manifest | NO |

`ISSUED` and `IN_PROGRESS` are mutually exclusive. A terminal receipt supersedes both. Any state other than proven `UNUSED` rejects reuse.

Before any frozen Repair-2 content read:

1. derive `ACTIVATION_RECEIPT_ID` only from canonical authorization Git metadata and the exact ordered four-file authorization-package blob IDs specified in `acceptance.md`;
2. search canonical history and all open/closed preflight-result PR metadata for the decision, receipt, claim, and prior episode evidence;
3. require proven `UNUSED`;
4. mechanically prove storage-boundary protection for `refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/**` using a repository ruleset, server-side hook, or equivalent durable control that permits the controlled initial creation but denies every subsequent update, force update, and deletion, gives the preflight worker no relevant bypass, and remains effective through canonical terminal adoption;
5. if that protection cannot be proven, terminate `BLOCKED` before reading frozen content and do not create the claim;
6. atomically create the exact claim ref with create-only semantics, pointing exactly to the canonical authorization merge SHA;
7. immediately re-read and verify the claim target and protection; any drift is `BLOCKED`;
8. only the successful claimant may create the unique result branch and publish the matching `activation-receipt.json`, recording the claim target and exact protection identity/enforcement facts;
9. only after that activation receipt is published may any frozen Repair-2 content be read, hashed, parsed, decompressed, or used for derived digest verification.

Competing workers observing an existing claim must stop. Claim refs are permanent governance evidence. Updating, force-updating, retargeting, deleting, or recreating a claim is prohibited. If a claim is ever observed changed or deleted after creation, that episode is permanently non-`UNUSED`; durable `BLOCKED` evidence must be preserved and the authorization cannot be restarted.

Every claimed terminal episode, successful or blocked, must preserve the activation identity and publish `consumption-receipt.json` bound to the exact final result-manifest SHA-256 and terminal re-verification of claim protection:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` => receipt `state = CONSUMED`;
- `BLOCKED` => receipt `state = BLOCKED`.

Canonical merge of the result package is the durable terminal-state transition. A claimed episode that cannot publish a terminal package is still burned and non-reusable. Any later attempt requires a new separately reviewed Founder authorization.

Terminal outcomes are only:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION`, or
- `BLOCKED`.

Even `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` grants no execution authority.

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
PROMPT_SERIALIZATION_TO_MODEL = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
