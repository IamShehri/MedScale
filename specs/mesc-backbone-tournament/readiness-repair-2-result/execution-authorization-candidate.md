# FD-MESC-BT-EXEC-1 — Execution Authorization Candidate

Status: **DRAFT / INACTIVE / NOT AUTHORIZED**

Date: 2026-08-20

This document is produced only because a successful readiness verdict requires a separate founder execution-disposition/authorization candidate. It is intentionally incomplete as executable authority and cannot authorize any model access or inference.

## Candidate scope if later completed, separately reviewed, adopted, and mechanically verified

A future `FD-MESC-BT-EXEC-1` may authorize one bounded zero-shot Backbone Tournament using only the candidates and protocol canonically admitted by the readiness result.

It may not become active until every activation field below is exact and non-placeholder.

## Required exact activation bindings

### Canonical code

```text
MESC_COMMIT_SHA = REQUIRED
MESC_TREE_SHA = REQUIRED
```

### Candidate set

The later package must explicitly choose from the readiness-admitted exact revisions; it may not silently substitute, quantize, or update a candidate. Current admissible revision candidates are:

```text
openai/gpt-oss-20b @ 6cee5e81ee83917806bbde320786a8fb61efebee
swiss-ai/Apertus-v1.5-8B @ a411d838600baf0e3635a3daf66fb7c55fc97bb6
microsoft/Phi-4-multimodal-instruct @ 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
google/medgemma-1.5-4b-it @ 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
```

Tokenizer/processor revisions must equal the selected model-repository revision unless the later package proves and binds a different authoritative immutable asset.

### Corpus

```text
CORPUS_PATH = REQUIRED
CORPUS_ITEM_COUNT = REQUIRED; must equal 240 under MESC-BT-PROTOCOL-V1
CORPUS_SHA256 = REQUIRED
R2_PROVENANCE_AUDIT = REQUIRED / PASS
```

No corpus hash may be invented before the 240-item synthetic/hand-authored corpus is materialized and independently validated.

### Protocol

```text
PROTOCOL_ID = MESC-BT-PROTOCOL-V1
PROTOCOL_CONFIG_SHA256 = 30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
```

### Runtime and hardware

```text
HARDWARE_IDENTITY = REQUIRED
PROVIDER_IDENTITY = REQUIRED
PYTHON_VERSION = REQUIRED
TORCH_VERSION = REQUIRED
ENGINE_VERSION_OR_COMMIT = REQUIRED
CUDA_DRIVER_RUNTIME = REQUIRED where applicable
PRECISION_QUANTIZATION_PER_CANDIDATE = REQUIRED
CUSTOM_CODE_HASHES = REQUIRED where applicable
```

Phi-4 may use `trust_remote_code=True` only if the exact pinned repository code is separately reviewed and bound. Apertus compatibility code must be pinned to an exact approved runtime revision. No floating remote code is permitted.

### Gated access

Apertus and MedGemma require gated-access/terms decisions. This candidate does **not** make those decisions.

Before activation, a later exact package must state, for each gated candidate:

```text
ACCESS_REQUIRED = YES
TERMS_VERSION_OR_REFERENCE = REQUIRED
FOUNDER_OPERATOR_EXPLICIT_ACCESS_AUTHORIZATION = REQUIRED
NON_SECRET_ACCESS_EVIDENCE = REQUIRED
```

No assistant or automation may request access, accept terms, or obtain weights merely because this draft exists.

### Run bound

The later package must bind an explicit maximum number of runs/attempts per candidate and the retry semantics from `MESC-BT-PROTOCOL-V1`. No open-ended inference is authorized.

### Artifact destinations

Exact result/output paths, canonical serialization rules, and expected artifact hashes/digests must be specified before execution.

## Mandatory review/adoption gates

Before `FD-MESC-BT-EXEC-1` can become active:

1. the repair-2 terminal result must be canonically merged and verified;
2. ADR-0034 must be canonical;
3. the exact 240-item corpus must be committed and R2-audited;
4. every activation binding above must be concrete;
5. exact-head CI/CodeQL must pass;
6. a fresh independent exact-head review must report no unresolved blocking findings;
7. all review threads must be resolved/dispositioned;
8. Founder Ready and Founder Merge must be exercised on the exact execution package;
9. merge must use expected-head protection;
10. post-merge canonical verification must prove adoption.

## Current state

```text
FD-MESC-BT-EXEC-1 = INACTIVE_CANDIDATE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
GATED_ACCESS_REQUEST_OR_ACCEPTANCE = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```

This state remains controlling after readiness succeeds until a later exact execution package satisfies every activation gate.
