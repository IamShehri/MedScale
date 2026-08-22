# Founder Authorization — FD-MESC-BT-EXEC-1

Status: **FOUNDER APPROVED FOR CONDITIONAL CANONICAL ADOPTION — EXECUTION INACTIVE UNTIL SEPARATE ACTIVATION VERIFICATION**

Date: 2026-08-22

## Decision identity

`FD-MESC-BT-EXEC-1`

## Founder decision

I authorize the repository to adopt a **conditional, bounded execution authorization contract** for one MESC Backbone Tournament over the four canonically admitted candidates listed in this package.

This decision is intentionally non-self-activating. It grants **no present authority** to access model weights, request or accept gated terms, serialize prompts to a model, run inference/generation, rank candidates, select winners, or execute the tournament.

Execution may become active only after a separate canonical execution-activation package proves every condition in `acceptance.md`, including the executable harness, exact runtime and hardware identity, measurement implementation, artifact destinations, all exact model/tokenizer/processor/custom-code pins, and any separately required gated-access Founder decision.

## Bound scientific scope

The later activated run, if activation succeeds, is limited to:

```text
TOURNAMENT_COUNT = 1
CANDIDATE_COUNT = 4
CORPUS_ITEM_COUNT_PER_CANDIDATE = 240
PRIMARY_ITEM_ATTEMPTS = 1
MAX_INFRASTRUCTURE_RETRIES_PER_ITEM = 1
PARSE_RETRIES = 0
SCHEMA_RETRIES = 0
SEMANTIC_RETRIES = 0
TIMEOUT_SECONDS_PER_ATTEMPT = 180
TOOLS = DISABLED
WEB = DISABLED
RETRIEVAL = DISABLED
FUNCTION_CALLS = DISABLED
SINGLE_TURN = TRUE
CANDIDATE_SPECIFIC_PROMPT_OPTIMIZATION = PROHIBITED
```

The frozen protocol, prompt, parser, scoring, report, corpus, and audit identities remain unchanged. No new challenger is authorized.

## Selected candidates

```text
openai/gpt-oss-20b@6cee5e81ee83917806bbde320786a8fb61efebee
swiss-ai/Apertus-v1.5-8B@a411d838600baf0e3635a3daf66fb7c55fc97bb6
microsoft/Phi-4-multimodal-instruct@93f923e1a7727d1c4f446756212d9d3e8fcc5d81
google/medgemma-1.5-4b-it@91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
```

This four-candidate set is fixed by this authorization candidate. Removing or replacing a candidate requires a separately reviewed Founder amendment before execution activation.

## Gated access is not authorized here

Apertus and MedGemma are canonically recorded as gated. This decision does **not** authorize requesting access, accepting terms, clicking acceptance controls, transferring credentials, or accessing their weights.

Define the separate future decision identity:

`FD-MESC-BT-EXEC-1-GATED-ACCESS-1`

The four-candidate execution activation must fail closed unless that separate decision is canonical and the human operator's access/terms state is explicitly attested without credential disclosure.

## Target compute class

The intended activation target is one `NVIDIA H100 80GB HBM3` in `RunPod Secure Cloud`, used sequentially for all candidates. This is a target class, not a sufficient runtime identity.

Activation must additionally bind the actual provider region/instance identity available from the provider, GPU UUID and model, immutable container digest, driver/CUDA/runtime versions, dependency lock, and model-specific runtime identities.

## Missing executable implementation

At this authorization baseline, repository search does not establish a canonical Backbone Tournament executor/evidence harness. Therefore `AUTHORIZATION_BASE_SHA=a78bcec4cf7daccc933315df8d5ce60bca005ed9` is a governance/scientific baseline, **not** an execution-code readiness claim.

Before activation, an executor/harness implementation package must be canonically adopted and independently reviewed. The activation package must bind its exact code commit/tree and relevant blob identities. No ad-hoc notebook, shell script, provider UI, or unreviewed local code may substitute for that canonical executor.

## Effect of this package

Before canonical merge:

```text
FD-MESC-BT-EXEC-1 = DRAFT_INACTIVE
EXECUTION_AUTHORITY = NONE
```

After a verified canonical merge of this exact package:

```text
FD-MESC-BT-EXEC-1 = CONDITIONAL_AUTHORIZATION_CANONICAL
EXECUTION_ACTIVATION = REQUIRED
EXECUTION_AUTHORITY = NONE_UNTIL_ACTIVATION_PASS
```

Only a later separately reviewed and canonically verified activation may change the final line.

Training, fine-tuning, corpus substitution/rematerialization, hidden prompt optimization, additional models, PHI, real patient data, external benchmark substitution, and any execution beyond this single bounded tournament remain outside scope.
