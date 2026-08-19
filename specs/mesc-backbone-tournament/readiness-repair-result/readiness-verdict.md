# MESC Backbone Tournament — Readiness Verdict

Status: **TERMINAL**

Date: 2026-08-20

## Authorization consumption

```text
FD-MESC-BT-READINESS-REPAIR-1 = CONSUMED
EPISODE_COUNT = 1
REUSABLE = NO
```

The single bounded read-only repair/protocol-freeze episode has ended.

## Canonical state inspected

```text
START_MAIN = dea2b05516e0fafadcc5902fdad0558d77c020cd
START_TREE = 2860cbfdc568ab2564d5c8e8e9063ba9f056dd1e
END_MAIN = dea2b05516e0fafadcc5902fdad0558d77c020cd
END_TREE = 2860cbfdc568ab2564d5c8e8e9063ba9f056dd1e
```

No material canonical drift occurred during the episode.

## Candidate dispositions

```text
openai/gpt-oss-20b = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
swiss-ai/Apertus-v1.5-8B = BLOCKED
microsoft/Phi-4-multimodal-instruct = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
google/medgemma-1.5-4b-it = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
optional_challenger = EMPTY
```

The roster contains at least two admitted candidates, but that condition is insufficient because a non-empty candidate remains `BLOCKED`.

## Blocking finding

```text
BLOCKER_ID = BT-RDY-BLK-APERTUS-AUP-001
BLOCKER_CATEGORY = LICENSE / ACCEPTABLE-USE EVIDENCE
BLOCKER_REASON = exact authoritative Apertus 1.5 AUP artifact identity proven, complete exact-version readable terms not proven/bindable through authorized interfaces
```

No authoritative evidence conclusively established that Apertus is incompatible, so the slot cannot be labeled `NOT_ADMITTED`.

## Terminal verdict

```text
READINESS_RESULT = BLOCKED
READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE = NO
BACKBONE_TOURNAMENT_READINESS = BLOCKED
```

The canonical rule is deterministic: any `BLOCKED` non-empty roster candidate forces overall `BLOCKED`.

## Protocol consequence

```text
PROTOCOL_FREEZE = NOT_PERFORMED
R2_CORPUS = NOT_CREATED
PROMPTS = NOT_FROZEN
DECODING = NOT_FROZEN
METRICS = NOT_FROZEN
SELECTION_THRESHOLDS = NOT_FROZEN
PROTOCOL_DIGEST = NOT_ASSIGNED
REPORT_SCHEMA_DIGEST = NOT_ASSIGNED
```

## Execution authority

```text
FD-MESC-BT-EXEC-1 = NOT_PRODUCED
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
TEST_PARTITION_ACCESS = NOT_AUTHORIZED
B1_B2_B3_EXECUTION = NOT_AUTHORIZED
P01_06_PLUS = NOT_AUTHORIZED
```

No execution authorization candidate is produced because the terminal verdict is not `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`.

## Required next-governance boundary

The consumed authorization cannot be reused to refresh model versions, resolve the AUP later, populate a challenger, freeze the protocol, or execute the tournament.

Any further work requires a **new separately reviewed founder authorization** based on then-current canonical truth.
