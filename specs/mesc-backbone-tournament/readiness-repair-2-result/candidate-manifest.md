# MESC Backbone Tournament — Repair-2 Candidate Manifest

Status: **REFRESHED READINESS EVIDENCE — NO WEIGHT ACCESS / NO EXECUTION**

Canonical MESC snapshot: `53f517e57602b1b721fce6edae71d6f9e64d3bc6`

All four non-empty candidates were refreshed from then-current first-party publisher/model-registry evidence during repair-2. Prior repair-1 admissions were not carried forward as proof.

## Common admission rules

A candidate is admitted here only if identity/revision, license/use restrictions, access state, architecture/runtime, R2/R3 compatibility, security implications, and a static future hardware-feasibility envelope are resolved. Admission means only `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`.

For every candidate, tokenizer/processor assets are pinned to the same immutable model-repository revision unless an additional runtime pin is explicitly listed. No floating `main` reference is permitted in a later execution package.

The conservative readiness feasibility envelope is one BF16-capable NVIDIA GPU with at least 48 GB VRAM. This is a static planning envelope, not executed hardware evidence and not the final execution hardware binding. `FD-MESC-BT-EXEC-1` must later bind exact hardware/provider identity.

## 1. OpenAI GPT-OSS 20B

```text
model_id = openai/gpt-oss-20b
revision = 6cee5e81ee83917806bbde320786a8fb61efebee
tokenizer_id = openai/gpt-oss-20b
tokenizer_revision = 6cee5e81ee83917806bbde320786a8fb61efebee
processor = AutoTokenizer / same pinned repository
license = Apache-2.0
access = public / ungated
architecture = GptOssForCausalLM
modalities = text -> text
native_quantization = MXFP4
trust_remote_code = false
future_readiness_envelope = >=48 GB VRAM GPU; conservative over published 20B deployment guidance
```

Authoritative evidence:
- `https://huggingface.co/api/models/openai/gpt-oss-20b`
- `https://huggingface.co/openai/gpt-oss-20b`
- `https://openai.com/index/introducing-gpt-oss/`
- `https://help.openai.com/en/articles/11870455-openai-open-weight-models-gpt-oss`

The current registry reports the exact immutable revision, Apache-2.0, `gated=false`, GPT-OSS architecture, and MXFP4 metadata. Apache-2.0 and the publisher's usage policy do not establish an R3 derivative/commercial-use conflict. No excluded-family or R2 conflict is identified.

Disposition:
`ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`

## 2. Swiss AI Apertus 1.5 8B

```text
model_id = swiss-ai/Apertus-v1.5-8B
revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
processor_id = swiss-ai/Apertus-v1.5-8B
processor_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
license = Apache-2.0 + Apertus 1.5 AUP obligations
access = gated; future explicit terms/access authorization required before weights
architecture = decoder-only transformer family
modalities = text/image/audio input -> text output
context = up to 262144 tokens per publisher card
precision = BF16-capable runtime
trust_remote_code = false for model repository; temporary exact Transformers compatibility pin required until upstream support
transformers_compatibility_pin = 3797303dda74844e3d1f8977ff5518bb91f818b4
future_readiness_envelope = >=48 GB VRAM GPU, common tournament limits 8192 input / 1024 output
```

Authoritative evidence:
- `https://huggingface.co/swiss-ai/Apertus-v1.5-8B`
- `https://github.com/swiss-ai/apertus-legal/tree/main/apertus_1.5`
- exact public AUP object recorded in `apertus-aup-resolution.md`

The exact AUP was independently byte-bound before interpretation. Its redistribution and compliance duties are material but do not establish a categorical derivative/commercial-use prohibition. Gated access was not requested or accepted during repair-2; it remains a later execution precondition.

Disposition:
`ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`

## 3. Microsoft Phi-4 Multimodal Instruct

```text
model_id = microsoft/Phi-4-multimodal-instruct
revision = 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
processor_id = microsoft/Phi-4-multimodal-instruct
processor_revision = 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
license = MIT
access = public / ungated
architecture = Phi-4 multimodal transformer, approximately 5.6B parameters
modalities = text/image/audio input -> text output
context = 128K
trust_remote_code = true, only at exact immutable model revision
future_readiness_envelope = >=48 GB VRAM GPU, common tournament limits 8192 input / 1024 output
```

Authoritative evidence:
- `https://huggingface.co/microsoft/Phi-4-multimodal-instruct`
- `https://huggingface.co/microsoft/Phi-4-multimodal-instruct/tree/main`

The publisher's current loading instructions require `trust_remote_code=True`. This is a security-sensitive runtime condition, not an unresolved fact. A future execution authorization must permit it only for the exact pinned repository revision and must hash/pin the executed repository code; no floating remote code is allowed. MIT permits derivative and commercial use, satisfying R3.

Disposition:
`ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`

## 4. Google MedGemma 1.5 4B IT

```text
model_id = google/medgemma-1.5-4b-it
revision = 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
processor_id = google/medgemma-1.5-4b-it
processor_revision = 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
license = Health AI Developer Foundations terms
access = gated; future explicit terms/access authorization required before weights
architecture = Gemma 3-derived 4B multimodal instruction-tuned model
modalities = text/image input -> text output
context = 128K input; publisher-documented bounded output
precision = BF16
trust_remote_code = false in current publisher Transformers example
future_readiness_envelope = >=48 GB VRAM GPU, common tournament limits 8192 input / 1024 output
```

Authoritative evidence:
- `https://huggingface.co/google/medgemma-1.5-4b-it`
- `https://developers.google.com/health-ai-developer-foundations/terms`
- Google Health AI Developer Foundations documentation/FAQ.

The HAI-DEF terms expressly define and allow model derivatives subject to the agreement and permit development of commercial products subject to applicable restrictions. The terms therefore do not establish an R3 derivative/commercial-use disqualifier. R2 removes real-patient/PHI evaluation from the tournament. Gated terms were not accepted during repair-2 and remain a future execution precondition.

Disposition:
`ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`

## 5. Challenger

```text
challenger = EMPTY
```

Repair-2 fixed the optional challenger as empty. No new model may be introduced by this result package.

## Roster proof

```text
non_empty_slots = 4
admitted = 4
not_admitted = 0
blocked = 0
challenger = EMPTY
minimum_distinct_admitted_required = 2
execution_viable_roster_requirement = PASS
```

This is readiness evidence only. No candidate has been downloaded, loaded, queried, scored, ranked, or selected.
