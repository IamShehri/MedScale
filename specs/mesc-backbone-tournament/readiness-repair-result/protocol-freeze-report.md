# MESC Backbone Tournament — Protocol Freeze Report

Status: **NOT PERFORMED — STOP CONDITION TRIGGERED**

Date: 2026-08-20

## Controlling rule

`FD-MESC-BT-READINESS-REPAIR-1` permits corpus/protocol freezing **if and only if** no non-empty candidate remains `BLOCKED`.

The refreshed candidate manifest contains:

```text
swiss-ai/Apertus-v1.5-8B = BLOCKED
blocker = BT-RDY-BLK-APERTUS-AUP-001
```

Therefore the authorized episode stopped before protocol-freeze completion.

## Six mandatory evaluation axes

The canonical axes remain requirements for any future separately authorized readiness episode:

1. medical knowledge and reasoning;
2. evidence fidelity;
3. uncertainty and abstention;
4. safety;
5. structured/FHIR readiness;
6. operational characteristics.

No corpus examples were created or admitted in this terminally blocked episode.

## Outputs intentionally not frozen

The following fields remain **UNFROZEN / NOT AUTHORIZED TO COMPLETE AFTER THE BLOCKER**:

```text
R2 synthetic/hand-authored corpus specification = NOT_FROZEN
corpus_count = NOT_ASSIGNED
corpus_digest = NOT_ASSIGNED
system_prompt = NOT_FROZEN
task_prompt_templates = NOT_FROZEN
message_format = NOT_FROZEN
input_limit = NOT_FROZEN
output_limit = NOT_FROZEN
decoding_parameters = NOT_FROZEN
seed_policy = NOT_FROZEN
stop_rules = NOT_FROZEN
parser = NOT_FROZEN
timeout_policy = NOT_FROZEN
retry_policy = NOT_FROZEN
generation_failure_classes = NOT_FROZEN
abstention_categories = NOT_FROZEN
metric_definitions = NOT_FROZEN
aggregate_weights = NOT_FROZEN
Compact_thresholds = NOT_FROZEN
Compact_tie_breaks = NOT_FROZEN
Compact_NO_SELECTION = NOT_FROZEN
Flagship_Reasoner_thresholds = NOT_FROZEN
Flagship_Reasoner_tie_breaks = NOT_FROZEN
Flagship_Reasoner_resource_envelope = NOT_FROZEN
Flagship_Reasoner_NO_SELECTION = NOT_FROZEN
latency_token_cost_memory_accounting = NOT_FROZEN
raw_output_schema = NOT_FROZEN
normalized_output_schema = NOT_FROZEN
error_schema = NOT_FROZEN
exclusion_schema = NOT_FROZEN
report_schema = NOT_FROZEN
artifact_schema = NOT_FROZEN
prompt_protocol_digest = NOT_ASSIGNED
report_schema_digest = NOT_ASSIGNED
```

This is not missing work inside the consumed authorization. It is the required fail-closed consequence of the blocker.

## Equal-treatment protection

No candidate output was observed. No prompt, parser, scoring rule, threshold, timeout, retry behavior, or architecture-specific accommodation was tuned against candidate behavior.

## R2 boundary preserved

No Pilot-01 test scientific content, real patient data, PHI, product telemetry, credentialed clinical dataset, or external benchmark corpus was accessed or ingested.

## Execution boundary

```text
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```

A future protocol freeze would require a new, separately reviewed authorization. The consumed repair authorization cannot be reused.
