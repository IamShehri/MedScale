# MESC Backbone Tournament Readiness Repair 2 — Acceptance Contract

Status: **INACTIVE UNTIL CANONICALLY ADOPTED**

Date: 2026-08-20

## Package adoption criteria

This package is eligible for canonical adoption only if all are true:

- canonical `main` is mechanically identified at review time;
- PR #128 remains in canonical ancestry and proves repair-1 ended `CONSUMED / BLOCKED / REUSABLE = NO`;
- changes are documentation/governance only;
- exact-head CI passes;
- exact-head CodeQL passes;
- fresh independent exact-head review reports no unresolved blocking finding;
- zero unresolved or undispositioned review threads remain;
- Ready is exercised only after those gates pass;
- merge uses expected-head protection;
- post-merge canonical main/tree/ordered parents/signature are mechanically verified.

## Required outputs of the activated episode

A valid episode must produce:

1. exact canonical main/tree at episode start and end;
2. controlling governance inventory;
3. exact Apertus 1.5 AUP repository/path/blob identity and size from the authoritative public legal repository;
4. locally retrieved AUP byte length, SHA-256, and computed Git blob SHA-1;
5. proof that the computed Git blob identity equals the authoritative repository blob identity before text interpretation;
6. rendered and/or extracted complete readable representation of that exact verified PDF, or an explicit blocker;
7. material Apertus restrictions with primary-evidence references;
8. deterministic Apertus R2/R3 compatibility disposition;
9. refreshed exact model IDs and immutable revisions for all four non-empty roster candidates;
10. refreshed tokenizer/processor identities and revisions where applicable;
11. refreshed authoritative license/access/gating evidence for every non-empty candidate;
12. refreshed architecture/context/modality/loading/security/precision/runtime/hardware-feasibility evidence for every non-empty candidate;
13. deterministic disposition for every non-empty candidate using only `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
14. challenger fixed `EMPTY`;
15. proof of at least two distinct admitted candidates for a ready comparative roster;
16. if and only if items 3–15 contain no blocker, a frozen synthetic/hand-authored R2-compatible corpus covering all six canonical axes;
17. exact corpus count and deterministic corpus digest;
18. frozen system/task prompts, formatting, input/output limits, decoding, deterministic seed policy, stop/parser/timeout/retry/failure/abstention rules;
19. frozen metric definitions and any aggregate weights;
20. frozen Compact and Flagship/Reasoner eligibility thresholds, tie-breaks, resource envelopes, and `NO_SELECTION` rules;
21. frozen latency/token/cost/memory/resource accounting contract;
22. reproducibility/raw-output/normalized-output/error/exclusion/report/artifact schemas;
23. prompt/protocol digest and report-schema digest;
24. non-authoritative execution plan;
25. terminal verdict `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` or `BLOCKED`;
26. a separate inactive execution-authorization candidate only if item 25 is ready.

## Six mandatory axes

1. medical knowledge and reasoning;
2. evidence fidelity;
3. uncertainty and abstention;
4. safety;
5. structured/FHIR readiness;
6. operational characteristics.

Omission of any axis forces `BLOCKED`.

## Stop conditions

Stop and report `BLOCKED` if:

- canonical state moves materially and cannot be reconciled;
- the public AUP bytes cannot be retrieved without gated access;
- computed Git blob identity does not exactly equal the authoritative blob;
- the exact verified PDF cannot be read completely enough to resolve material restrictions;
- any material term remains ambiguous or contradictory;
- any non-empty candidate has unresolved required evidence;
- fewer than two distinct candidates are admitted;
- R2 or R3 compatibility cannot be proven;
- hardware/runtime feasibility cannot be established without inference;
- any mandatory evaluation axis or protocol field cannot be frozen before model outputs exist;
- scope expands into a prohibited action.

## Candidate semantics

`BLOCKED`: required evidence remains unresolved, incomplete, contradictory, unavailable, or unbindable.

`NOT_ADMITTED`: authoritative evidence conclusively proves a disqualifying condition.

`ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`: all required admission evidence is proven for proposal into a later separately reviewed execution package; no execution authority is granted.

Any non-empty `BLOCKED` slot forces overall `BLOCKED`.

## Post-episode authority

Even after a ready result:

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```
