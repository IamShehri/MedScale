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

Before the one-shot claim succeeds, authority is limited to Git/repository metadata needed to identify this canonical authorization and prove replay/claim state: commit/tree ancestry, repository paths, Git blob IDs, result-PR metadata, claim-ref metadata, result-ref metadata, claim/result-ref protection metadata, and the four authorization-package blob IDs. **No frozen Repair-2 artifact content may be read, hashed, parsed, decompressed, or used for a derived digest before the protected atomic claim and matching activation receipt are established exactly as required by `acceptance.md`.**

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

Any mismatch in committed corpus/storage/logical/scoring-key identity, any missing frozen protocol-contract binding, any non-canonical item ID, any prohibited source indication, any gold leakage into model-visible payload, any unresolved evidence-reference mismatch, any duplicate JSON member name in a canonicalized preflight object, any result-package hash mismatch, any pre-claim frozen-content read, any missing/mismatched claim or receipt, any failed/incomplete result-ref or claim-ref enumeration, any failed/incomplete canonical-history traversal or open/closed result-PR enumeration, any unexpected result or claim ref, any missing or bypassable storage-boundary claim/result-ref protection, any deleted/retargeted/updated claim after creation, any unreadable or lifecycle-invalid result-ref target, any unauthorized/force/non-fast-forward result-ref update or deletion, any self-referential commit-SHA binding, any invalid terminal content/receipt parent relation, any conflicting replay-state evidence, or any inability to reproduce a required audit deterministically => `BLOCKED`.

Gated candidates remain non-accessible during this episode. No wording in this authorization constitutes acceptance of Apertus or MedGemma gated terms.

## Atomic single-use claim, receipt, protection, and consumption rule

This decision is single-use and replay-resistant. `acceptance.md` is normative for the exact receipt preimage, claim-ref prefix, result-ref prefix, complete canonical-history/PR discovery requirements, storage-boundary protection requirements, canonical JSON encoding, state predicates, non-self-referential result-ref lifecycle, and terminal receipt shape.

The only permitted result-ref and claim-ref identities are derived exactly as:

```text
RESULT_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/
RESULT_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-result/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
CLAIM_REF_PREFIX = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/
CLAIM_REF = refs/heads/governance/fd-mesc-bt-exec-1-preflight-claim/<AUTHORIZATION_MERGE_SHA>/<ACTIVATION_RECEIPT_ID>
```

Each prefix is a literal ref-name prefix, never a glob. A ref is under a prefix iff its full ref name starts with that exact prefix. The only well-formed descendant has exactly two non-empty path segments after the prefix: `<AUTHORIZATION_MERGE_SHA>` must be 40 lowercase hexadecimal characters and `<ACTIVATION_RECEIPT_ID>` must be 64 lowercase hexadecimal characters. Any other descendant under either prefix is `BLOCKED`.

Before `UNUSED` may be accepted, all replay-evidence discovery must be independently exhaustive and mechanically complete:

1. enumerate every ref whose full name starts with `RESULT_REF_PREFIX`;
2. enumerate every ref whose full name starts with `CLAIM_REF_PREFIX`;
3. traverse every commit reachable from then-current canonical `main`, following every parent edge to repository roots with no shallow/truncated boundary; and
4. enumerate the entire open and closed/merged PR population and inspect every preflight-result PR metadata record relevant to this authorization/receipt.

Every page/cursor must be consumed for each paginated ref/PR enumeration, and canonical-history traversal must prove the authoritative object graph is complete. Any failed request, missing object, permission limit, shallow boundary, truncation, partial pagination, omitted cursor/page, or otherwise non-exhaustive search => `BLOCKED`. Every discovered ref descendant must pass exact shape validation.

Any exact `RESULT_REF` or exact `CLAIM_REF` is replay evidence even without a PR or receipt. Existing exact refs are integrity-checked, not merely counted: `CLAIM_REF` must be readable and point exactly to `AUTHORIZATION_MERGE_SHA`; `RESULT_REF` must be readable and either point exactly to that SHA at initial issuance or to a lifecycle-valid permitted fast-forward descendant on the single episode result lineage. Unreadable, non-descendant, force/sideways-retargeted, or state-inconsistent result-ref targets => `BLOCKED`.

State evaluation uses this exact precedence: canonical terminal receipt → matching in-progress evidence → protected claim-only evidence → unused. Conflicting or ambiguous evidence is `BLOCKED`.

| State | Exact predicate | New episode allowed? |
|---|---|---|
| `UNUSED` | both ref scans, complete canonical-history traversal, and complete open+closed/merged PR enumeration are proven exhaustive; no exact claim ref, activation receipt, exact result ref, result PR, terminal receipt, malformed/unexpected descendant, or conflicting evidence for this authorization/receipt | YES, only by successful protected atomic claim |
| `ISSUED` | exact protected claim exists at the exact authorization merge SHA, with no activation receipt, exact result ref, result PR, or terminal receipt | NO |
| `IN_PROGRESS` | exact protected claim exists and matching activation-receipt/lifecycle-valid exact-result-ref/result-PR evidence exists, with no canonical terminal receipt | NO |
| `BLOCKED` | canonical blocked terminal receipt, incomplete ref/history/PR discovery, malformed/unexpected descendant under either prefix, claim/result-ref protection violation, deleted/changed claim evidence, unreadable or lifecycle-invalid result-ref target, conflicting receipt, mismatched target/state, or ambiguous state | NO |
| `CONSUMED` | canonical consumed terminal receipt matches the final ready manifest | NO |

`ISSUED` and `IN_PROGRESS` are mutually exclusive. Publishing the matching activation receipt or advancing/observing a lifecycle-valid exact result ref makes the logical replay state `IN_PROGRESS`. A terminal receipt supersedes both. Any state other than proven `UNUSED` rejects reuse.

Before any frozen Repair-2 content read:

1. derive `ACTIVATION_RECEIPT_ID` only from canonical authorization Git metadata and the exact ordered four-file authorization-package blob IDs specified in `acceptance.md`;
2. complete both exhaustive ref-prefix scans, the complete canonical-history traversal, and the complete open+closed/merged PR enumeration, consuming all pages/cursors and proving no shallow/truncated history; validate every descendant shape and every existing exact claim/result-ref target;
3. if any discovery is incomplete or fails, or exposes any malformed/unexpected descendant or integrity-invalid target/state, terminate `BLOCKED` before claim creation;
4. require proven `UNUSED`;
5. mechanically prove storage-boundary `CLAIM_REF_PROTECTION = PASS` and `RESULT_REF_PROTECTION = PASS` as defined in `acceptance.md`; claim protection permits controlled first creation but denies all later claim updates/deletion, while result-ref protection permits only designated-principal expected-old-target ordinary fast-forwards on the single authorization-descendant result lineage, denies force/non-fast-forward updates and deletion/recreation, and freezes all updates after the terminal receipt commit;
6. if either protection cannot be proven, terminate `BLOCKED` before reading frozen content and do not create the claim;
7. atomically create exactly `CLAIM_REF` with create-only semantics, pointing exactly to the canonical authorization merge SHA;
8. immediately re-read and verify the claim target and both protections; any drift is `BLOCKED` and the episode remains permanently non-reusable once the claim has existed;
9. only the successful claimant may atomically create exactly `RESULT_REF` with create-only semantics at the authorization merge SHA, then re-read that exact initial target;
10. construct the matching activation receipt and activation commit with **single parent exactly `AUTHORIZATION_MERGE_SHA`**. The receipt records `result_ref_activation_parent = AUTHORIZATION_MERGE_SHA` but does not and must not contain the SHA of the commit that contains it;
11. after the activation commit exists and its SHA is known, atomically fast-forward `RESULT_REF` from exactly the authorization merge SHA to it using expected-old-target semantics; re-read the ref, require that exact observed commit SHA, verify its single parent and receipt bytes, and define that external identity as `RESULT_REF_ACTIVATION_COMMIT`;
12. only after that protected activation fast-forward is re-read and structurally verified may any frozen Repair-2 content be read, hashed, parsed, decompressed, or used for derived digest verification;
13. later result commits may advance `RESULT_REF` only by the same controlled expected-old-target ordinary-fast-forward rule;
14. terminal closure is two commits: first create and publish `TERMINAL_CONTENT_COMMIT` containing the byte-final result package and manifest but no terminal receipt; then create `TERMINAL_RECEIPT_COMMIT` as its direct child adding only `consumption-receipt.json`, whose contents bind the already-known activation commit SHA, terminal-content commit SHA, final manifest SHA-256, claim/ref identities, protections, and state but do not contain the receipt commit's own SHA;
15. fast-forward `RESULT_REF` from exactly `TERMINAL_CONTENT_COMMIT` to the externally observed `TERMINAL_RECEIPT_COMMIT`, re-read and verify the parent/tree relation, then freeze the result ref against all later update/delete.

Competing workers observing an existing claim or exact result ref must stop. Claim refs are permanent immutable governance evidence. Result refs are permanent single-lineage governance evidence: only the lifecycle fast-forwards above are permitted before terminal freeze. Any claim deletion/change, result-ref force/non-fast-forward retarget/deletion/recreation, protection bypass/drift, self-referential SHA requirement, or irreconcilable target makes the episode permanently non-`UNUSED`; durable `BLOCKED` evidence must be preserved when possible and the authorization cannot be restarted.

A claimed episode that reaches terminal-package construction must preserve the activation identity and publish `consumption-receipt.json` bound to the exact final result-manifest SHA-256 and the already-known `TERMINAL_CONTENT_COMMIT`. The receipt binds exact `result_ref`, exact `result_ref_activation_commit`, exact `result_ref_terminal_content_commit`, and terminal protection re-verification. `TERMINAL_RECEIPT_COMMIT` is verified externally as the direct child of that content commit whose only tree delta is the receipt, and its SHA is recorded in the result PR description rather than inside its own receipt:

- `PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION` => receipt `state = CONSUMED`;
- `BLOCKED` => receipt `state = BLOCKED`.

Canonical merge of the result package is the durable terminal-state transition. A claimed episode that cannot reach terminal receipt closure is still burned and non-reusable; the existence/history of its claim or result evidence is sufficient to prevent `UNUSED`. Any later attempt requires a new separately reviewed Founder authorization.

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
