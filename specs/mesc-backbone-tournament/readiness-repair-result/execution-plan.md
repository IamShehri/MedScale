# MESC Backbone Tournament — Non-Authoritative Execution Plan

Status: **BLOCKED / NOT EXECUTABLE / NO EXECUTION AUTHORITY**

Date: 2026-08-20

## Purpose

This file satisfies the readiness-repair requirement to record an execution plan while preserving the terminal `BLOCKED` result. It is a planning record only and cannot be used to access weights, run inference, or start the tournament.

## Current authority state

```text
FD-MESC-BT-READINESS-REPAIR-1 = CONSUMED
READINESS_RESULT = BLOCKED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```

## Preconditions before any future execution package can exist

A new separately reviewed founder authorization must first resolve readiness from then-current canonical truth. At minimum it must:

1. mechanically reverify canonical `main`, tree, and controlling governance;
2. decide how to handle the non-empty Apertus slot without reusing `FD-MESC-BT-READINESS-REPAIR-1`;
3. if Apertus remains in scope, obtain a complete readable authoritative representation of the exact then-current Apertus AUP and bind it to the exact official artifact/version without violating any new authorization boundary;
4. refresh all required candidate IDs, immutable model revisions, tokenizer/processor revisions, license/access/gating facts, architecture/runtime/security requirements, and hardware feasibility;
5. reach zero `BLOCKED` non-empty candidates and at least two admitted candidates;
6. only then freeze all six R2-compatible evaluation axes, synthetic/hand-authored corpus, prompts, decoding, parsing, abstention/failure rules, metrics, Compact and Flagship/Reasoner thresholds, accounting, schemas, and deterministic digests before model outputs exist;
7. produce and independently review a separate inactive execution-authorization candidate containing exact code/runtime/corpus/model pins and bounded inference-run counts.

## Future execution design constraints — not frozen here

Any later execution proposal should preserve these already-canonical constraints:

- zero-shot comparative backbone selection only;
- synthetic or hand-authored R2-compatible evaluation data only;
- no Pilot-01 test scientific content;
- no PHI, real patient data, product telemetry, or credentialed clinical benchmark ingestion;
- identical task semantics across candidates;
- no prompt or scoring adaptation after observing candidate outputs;
- deterministic retention of negative results and failures;
- `NO_SELECTION` remains possible for Compact and Flagship/Reasoner roles;
- exact model/tokenizer/processor revisions and runtime versions must be pinned;
- remote custom code, when required, must be exact-revision pinned and separately security-reviewed;
- all execution must remain bounded by a later explicit authorization.

## Reference hardware feasibility record — not an execution pin

The repair episode used an analytical reference envelope of one NVIDIA H100 80GB-class accelerator, batch size 1, and bounded context materially below native model limits solely to determine whether admitted candidates were obviously infeasible. No model was loaded or run, no latency was measured, and this envelope is not frozen for execution.

## Prohibited transition

There is no valid direct transition from this file to tournament execution.

```text
THIS_PLAN -> EXECUTION = INVALID
```

The only valid next transition is:

```text
NEW_FOUNDER_AUTHORIZATION
  -> NEW_BOUNDED_READINESS_EPISODE
  -> READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE (only if all gates pass)
  -> SEPARATE_EXECUTION_AUTHORIZATION_REVIEW
  -> FOUNDER_READY / FOUNDER_MERGE / POST-MERGE_VERIFICATION
  -> EXECUTION (only if explicitly authorized)
```

Until that full chain is satisfied, execution remains prohibited.
