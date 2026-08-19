# MESC Backbone Tournament Readiness Gate — Acceptance Contract

Status: **DRAFT / INACTIVE**

Date: 2026-08-19

## Package adoption criteria

This package is eligible for canonical adoption only if all are true:

- it is based on then-current verified canonical `main`;
- the separate Pilot-01 closeout disposition is proven adopted by the merged PR #125 / merge commit `c0a9acfc678149736bd9054f7fadae1c31b488a1`;
- that closeout merge mechanically verifies to tree `71f36f2e49932f82a6ee733833b93306ab5f1f41`, ordered parents `f69a1b2f1c050aad6fe77eb6273016c764c109f5` then `1e52fa581af8f7894e2cfe3dbd1b07683ae0de72`, and GitHub verification `verified=true / reason=valid`;
- then-current canonical `main` is equal to or a descendant of `c0a9acfc678149736bd9054f7fadae1c31b488a1`;
- changes are docs/governance only;
- it preserves canonical Pilot-01 closeout and accepted B0 provenance;
- it grants no tournament/model execution authority;
- it preserves Program Rule R2;
- it preserves the current excluded-model-family policy;
- it preserves no-rerun/no-test/no-training/no-retrieval boundaries;
- the design-time roster matches canonical strategy or any deviation is explicitly justified without admitting a new candidate;
- exact-head CI passes;
- exact-head CodeQL passes;
- fresh independent exact-head review reports no unresolved blocking findings;
- all review threads are resolved or explicitly dispositioned with evidence;
- the founder separately exercises Ready;
- the founder separately exercises Merge;
- merge uses an exact expected-head guard or equivalent fail-closed protection;
- post-merge canonical main/tree/ordered parents are mechanically verified;
- after package merge, canonical `main` still contains the verified Pilot-01 closeout merge in its ancestry.

The Pilot-01 closeout prerequisite is fail-closed. Historical or proposed status text is insufficient by itself; the objective merge identity, tree, ordered parents, signature verification, and canonical ancestry above must be mechanically observable.

## Readiness episode required outputs after adoption

The authorized episode must produce a deterministic package containing:

1. exact canonical main/tree inspected;
2. controlling governance inventory;
3. candidate family-to-exact-ID resolution;
4. immutable model/tokenizer/processor revision pins or explicit blockers;
5. authoritative license/access evidence and deterministic admissibility disposition per candidate, using `BLOCKED` for unresolved evidence and `NOT_ADMITTED` only for conclusively proven disqualification;
6. hardware/runtime feasibility evidence;
7. challenger-slot disposition;
8. frozen R2-compatible evaluation-corpus specification and provenance rules that explicitly cover **all six required protocol axes**: medical knowledge/reasoning, evidence fidelity, uncertainty/abstention, safety, structured/FHIR readiness, and operational characteristics;
9. frozen prompt/decoding/parser/error/abstention contract;
10. frozen metrics and selection thresholds for Compact and Flagship roles;
11. reproducibility/artifact schema;
12. execution-viable roster proof showing at least two distinct non-empty candidates are `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
13. readiness conclusion:
   - `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`, or
   - `BLOCKED`;
14. a separate founder execution-disposition/authorization candidate that remains inactive.

Any `BLOCKED` disposition for a non-empty roster slot forces item 13 to be `BLOCKED`; it cannot be bypassed by excluding that candidate. An intentionally empty optional challenger slot is not a blocker. Fewer than two distinct admitted candidates also forces item 13 to be `BLOCKED`, even if all remaining non-empty candidates are conclusively `NOT_ADMITTED`.

## Required execution-candidate fields

A later execution authorization candidate must, at minimum, bind:

- exact admitted candidate IDs and immutable revisions;
- exact tokenizer/processor revisions;
- exact MESC code SHA/tree;
- exact synthetic/hand-authored evaluation corpus hash/count;
- exact prompt/protocol digest;
- exact decoding parameters and seed policy;
- exact runtime/provider/hardware envelope;
- bounded number of candidate runs;
- failure/retry policy;
- artifact/output paths and hashes;
- no-test/no-training/no-retrieval/no-quantization boundaries.

No placeholder in these fields may be treated as execution authority.

## Stop conditions

Stop and report `BLOCKED` if:

- the Pilot-01 closeout adoption proof or ancestry check fails;
- canonical state moves materially during readiness;
- any non-empty roster candidate has unresolved identity, immutable revision, license/access, R2, security, or hardware/runtime feasibility evidence;
- any exact candidate identity/revision cannot be proven;
- candidate license/access terms are unresolved;
- R2 compatibility cannot be proven;
- fewer than two distinct non-empty roster candidates can be conclusively admitted for a later execution-authorization candidate;
- any of the six required evaluation axes cannot be frozen into the R2-compatible corpus/protocol contract;
- an equal-treatment decision would require observing model outputs;
- hardware/runtime feasibility cannot be established without model execution;
- protocol scoring/thresholds cannot be frozen pre-execution;
- scope expands toward weights, inference, training, external prohibited data, or downstream implementation.

## Post-readiness state

Even after a successful readiness episode:

```text
BACKBONE_TOURNAMENT_READINESS = COMPLETE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
```

Execution may begin only after a separate exact execution package is reviewed, adopted, and mechanically verified under its own founder decisions.
