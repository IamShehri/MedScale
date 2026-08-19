# P01-05 B0 — Google Colab Remote Model Readiness Runbook

Date: 2026-08-18
Status: HISTORICAL READINESS GATE — SATISFIED / SUPERSEDED AS NEXT GATE

> **Canonical reconciliation (2026-08-19):** This runbook records the bounded
> remote-readiness gate that preceded the separately authorized B0 execution.
> That later B0 execution was completed once and accepted canonically in PR #123
> at merge commit `3f34b35daf4050d010a5f0061d6e8387f9649c10`; see
> `specs/mesc-pilot-01/p01-05-b0-execution-acceptance/`. The readiness instructions
> and terminal state below are preserved as historical execution provenance. They
> are **not** a current instruction to acquire the model again or rerun B0. B1 and
> P01-06 remain NOT AUTHORIZED.

## Scope

This runbook covers **remote model acquisition/environment readiness only** for the Pilot-01 B0 control.

It does not authorize inference, scoring, training, fine-tuning, test-partition scientific-content access, retrieval, P01-06, B1, B2/B3, or MESC vNext work.

## Exact model identity

Model:

`meta-llama/Llama-3.2-3B-Instruct`

Immutable revision:

`0cb88a4f764b7a12671c53f0838cd831a0843b95`

No fallback model and no alternate revision are permitted.

## Proven validation-only input

Local preparation artifact:

`C:\MESCExecutionEvidence\P01-05-B0-validation-input-prep-1\b0-validation-input.jsonl`

Exact byte size:

`262968`

Exact SHA-256:

`0cb55ad4de0eb831e2475030e889ad9a6f0701ea59adbdd6a30cc0d0115be8d3`

Proven membership:

- train = 0
- validation = 150
- test = 0

Adopted B0 loader validation: `PASS`

## Colab notebook identity

Prepared conversation artifact:

`MESC_P01_05_B0_REMOTE_MODEL_ACQUISITION_READINESS.ipynb`

SHA-256:

`ccd2129781c3e76fb1f11ed4c924d5e7cbd9b78dbd034b2974f374732b2ba9ac`

The notebook is a convenience execution surface. This runbook is the durable repository record of its gate boundaries and exact identities.

## Required Colab environment

1. Use a Google Colab-hosted runtime.
2. Select a GPU runtime.
3. Do not mount Google Drive for this readiness gate.
4. Store the Hugging Face access token in Colab Secrets as `HF_TOKEN`; never print it.
5. The Hugging Face account must already have legitimate access to the gated Meta Llama 3.2 model.
6. Use ephemeral Colab storage for the model snapshot.
7. Before download, verify sufficient free ephemeral disk with a safety reserve.

## Required acquisition behavior

The readiness workflow must:

1. attest Python, PyTorch, CUDA availability, GPU model, GPU count, and runtime disk;
2. upload only the proven validation input and verify exact size/SHA-256;
3. authenticate to Hugging Face without printing the token;
4. query the exact model revision and require the resolved SHA to equal the pinned revision;
5. dry-run the snapshot selection before download;
6. download only the Transformers-compatible snapshot surfaces needed for later B0;
7. exclude duplicate `original/` exports and alternate `.bin` / `.pth` weights;
8. hash every acquired local model file;
9. preserve metadata-only provenance;
10. stop before any model/tokenizer instantiation for inference.

## Hard boundaries

MUST NOT:

- run `medscale mesc-eval`;
- invoke `run_b0`;
- instantiate `AutoModelForCausalLM`;
- instantiate a tokenizer for inference;
- call `.generate()`;
- produce predictions;
- score accuracy or other scientific results;
- quantize weights;
- train or fine-tune;
- use another model;
- use another revision;
- use a 1B fallback;
- inspect test-partition scientific content;
- mount Google Drive;
- push model files to Hugging Face or another registry;
- mutate repository source/test/script files.

## Required successful terminal state

The following block records the required terminal state **at the time this readiness gate was executed**. Its `NEXT_GATE` field is historical and has since been consumed by the separately authorized, accepted B0 execution.

```text
P01-05 B0 REMOTE MODEL ACQUISITION / ENVIRONMENT READINESS

FINAL_DECISION:
COMPLETE_AND_STOP

ENVIRONMENT:
GOOGLE_COLAB_HOSTED_RUNTIME

GPU_ATTESTATION:
PASS

VALIDATION_INPUT_REMOTE_ATTESTATION:
PASS

MODEL_ID:
meta-llama/Llama-3.2-3B-Instruct

MODEL_REVISION:
0cb88a4f764b7a12671c53f0838cd831a0843b95

GATED_MODEL_ACCESS:
PASS

REMOTE_REVISION_ATTESTATION:
PASS

EXACT_MODEL_ACQUISITION:
PASS

LOCAL_MODEL_BYTE_PROVENANCE:
PASS

QUANTIZATION:
NONE

MODEL_INSTANTIATION:
NOT_PERFORMED

MODEL_INFERENCE:
NOT_PERFORMED

TRAINING:
NOT_PERFORMED

TEST_SCIENTIFIC_CONTENT_ACCESSED:
NO

GOOGLE_DRIVE_MOUNT:
NOT_PERFORMED

REPOSITORY_MUTATION:
NONE

NEXT_GATE:
P01-05 B0 REAL ZERO-SHOT VALIDATION EXECUTION AUTHORIZATION

STOP_REASON:
NONE
```

At the time of this readiness gate, the required action was to stop and obtain a separate founder authorization before real B0 inference. That authorization was subsequently issued and consumed for exactly one B0 validation execution, which is now accepted canonically. This historical runbook grants no new authority: no second B0 run, B1 execution, test-partition execution or scientific-content inspection, P01-06+, training, retrieval, fallback substitution, or quantization change is authorized here.
