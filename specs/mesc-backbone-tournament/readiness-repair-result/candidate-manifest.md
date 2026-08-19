# MESC Backbone Tournament — Refreshed Candidate Manifest

Status: **TERMINAL READINESS EVIDENCE / NO EXECUTION AUTHORITY**

Verified: 2026-08-20

## Admission semantics

This manifest uses only:

- `BLOCKED`
- `NOT_ADMITTED`
- `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`

No disposition grants weight access, inference, or tournament execution.

For analytical hardware feasibility only, the episode used a conservative future reference envelope of one NVIDIA H100 80GB-class accelerator, batch size 1, and bounded tournament-length inputs materially below each admitted candidate's documented native context. This is not an execution configuration and no model was run.

## Slot 1 — OpenAI gpt-oss-20b

```text
family = OpenAI gpt-oss-20b
model_id = openai/gpt-oss-20b
model_revision = 6cee5e81ee83917806bbde320786a8fb61efebee
tokenizer_id = openai/gpt-oss-20b
tokenizer_revision = 6cee5e81ee83917806bbde320786a8fb61efebee
processor = AutoTokenizer
license = Apache-2.0
access = public / ungated
architecture = GptOssForCausalLM / mixture-of-experts
parameter_class = ~21B total / ~3.6B active per token
modalities = text -> text
context = 131072 tokens
precision = native MXFP4 checkpoint
trust_remote_code = false
hardware_feasibility = PROVEN ANALYTICALLY for the future reference envelope; OpenAI documents ~16GB memory suitability for gpt-oss-20b
DISPOSITION = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
```

Admission rationale:

- exact immutable model/tokenizer revision is publicly resolvable;
- repository is ungated;
- Apache 2.0 permits modification, redistribution, derivatives, and commercial use subject to the gpt-oss usage policy;
- current gpt-oss usage policy requires compliance with applicable law and does not conflict with the bounded synthetic R2 research scope;
- the model is text-only, which is compatible with text representations of every future R2 task even though it cannot consume image/audio inputs directly;
- no Chinese-family policy conflict exists.

Primary evidence:

- https://huggingface.co/api/models/openai/gpt-oss-20b
- https://developers.openai.com/api/docs/models/gpt-oss-20b
- https://help.openai.com/en/articles/11870455-openai-open-weight-models
- https://huggingface.co/openai/gpt-oss-20b/blob/main/USAGE_POLICY

## Slot 2 — Swiss AI Apertus 1.5 8B

```text
family = Swiss AI Apertus 1.5 8B
model_id = swiss-ai/Apertus-v1.5-8B
model_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
processor_id = swiss-ai/Apertus-v1.5-8B
processor_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
tokenizer_id = swiss-ai/Apertus-v1.5-8B
tokenizer_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
license = Apache-2.0 plus Apertus 1.5 Acceptable Use Policy
access = gated:auto; repository files require explicit agreement/request
architecture = decoder-only transformer / xIELU, with multimodal image/audio support
parameter_class = 8B family
modalities = text + image + audio -> text
context = 262144 tokens
runtime_requirement = Swiss AI Transformers branch pin 3797303dda74844e3d1f8977ff5518bb91f818b4 until upstream support is released
hardware_feasibility = public deployment guidance demonstrates bounded single-model serving; exact execution envelope was not frozen
AUP_artifact_repo = swiss-ai/apertus-legal
AUP_artifact_path = apertus_1.5/USAGE_POLICY.pdf
AUP_git_blob_sha = 8ddd8e25b6672340dd4f921ba623578571a65526
AUP_size = 53794 bytes
AUP_readable_exact_version = NO
DISPOSITION = BLOCKED
```

Blocking rationale:

- exact AUP artifact identity is proven;
- the current model repository explicitly requires agreement to that AUP and sharing contact information before file access;
- this repair authorization absolutely prohibits requesting or accepting gated model access, gated-access terms, or model-access agreements for any purpose;
- the public GitHub artifact is binary and the authorized read interfaces did not produce a complete readable representation bound to blob `8ddd8e25b6672340dd4f921ba623578571a65526`;
- third-party summaries and older/newer policies are explicitly inadmissible under the canonical acceptance contract.

Because the exact terms remain unreadable/unproven, the deterministic disposition is `BLOCKED`. It is not `NOT_ADMITTED`, because no authoritative evidence conclusively established incompatibility.

Primary evidence:

- https://huggingface.co/swiss-ai/Apertus-v1.5-8B
- https://huggingface.co/swiss-ai/Apertus-v1.5-8B/commit/a411d838600baf0e3635a3daf66fb7c55fc97bb6
- https://github.com/swiss-ai/apertus-legal/tree/main/apertus_1.5
- https://github.com/swiss-ai/apertus-legal/blob/main/apertus_1.5/USAGE_POLICY.pdf

## Slot 3 — Microsoft Phi-4 Multimodal

```text
family = Microsoft Phi-4 Multimodal 5.6B
model_id = microsoft/Phi-4-multimodal-instruct
model_revision = 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
processor_id = microsoft/Phi-4-multimodal-instruct
processor_revision = 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
tokenizer_id = microsoft/Phi-4-multimodal-instruct
tokenizer_revision = 93f923e1a7727d1c4f446756212d9d3e8fcc5d81
license = MIT
access = public / ungated
architecture = multimodal transformer built on Phi-4-Mini-Instruct with vision and speech encoders/adapters
parameter_class = 5.6B
modalities = text + image + audio -> text
context = 128K tokens
precision = BF16 checkpoint
trust_remote_code = true, exact revision pin mandatory
repository_size = ~12.9 GB
hardware_feasibility = PROVEN ANALYTICALLY for the future reference envelope
DISPOSITION = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
```

Admission rationale:

- exact model, processor, tokenizer, and custom-code revision is public and verified;
- MIT permits derivatives and commercial use;
- repository is not gated;
- the model card requires `trust_remote_code=True`; therefore any later execution authorization must pin the exact revision and prohibit unpinned remote code;
- documented model size is comfortably within the future 80GB-class feasibility envelope for bounded batch-1 evaluation;
- no Chinese-family policy conflict exists.

Primary evidence:

- https://huggingface.co/microsoft/Phi-4-multimodal-instruct
- https://huggingface.co/microsoft/Phi-4-multimodal-instruct/commit/93f923e1a7727d1c4f446756212d9d3e8fcc5d81
- https://huggingface.co/microsoft/Phi-4-multimodal-instruct/tree/93f923e1a7727d1c4f446756212d9d3e8fcc5d81

## Slot 4 — Google MedGemma 1.5 4B IT

```text
family = Google MedGemma 1.5 4B IT
model_id = google/medgemma-1.5-4b-it
model_revision = 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
processor_id = google/medgemma-1.5-4b-it
processor_revision = 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
tokenizer_id = google/medgemma-1.5-4b-it
tokenizer_revision = 91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
license = Health AI Developer Foundations Terms of Use
access = gated; acknowledgement of HAI-DEF terms required to obtain repository files
architecture = Gemma 3 decoder-only transformer / GQA
parameter_class = 4B
modalities = text + vision -> text
context = at least 128K input tokens
max_output = 8192 tokens
precision = BF16 checkpoint
trust_remote_code = false under documented Transformers loading path
hardware_feasibility = PROVEN ANALYTICALLY for the future reference envelope
DISPOSITION = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
```

Admission rationale:

- exact current model revision and same-revision processor/tokenizer inventory are publicly resolvable without accepting access;
- access is gated, but candidate admission does not itself obtain weights; the episode did not click, acknowledge, or accept the gated terms;
- public HAI-DEF terms explicitly define Model Derivatives and permit use, modification, and distribution subject to stated restrictions; Google's current FAQ explicitly permits developing commercial products;
- the Prohibited Use Policy does not conclusively prohibit a bounded synthetic, non-clinical, non-patient-facing R2 research evaluation;
- the future execution package, if ever proposed, must separately handle lawful terms acceptance and keep the tournament outside prohibited automated healthcare decision-making or unauthorized medical practice;
- no Chinese-family policy conflict exists.

Primary evidence:

- https://huggingface.co/google/medgemma-1.5-4b-it
- https://huggingface.co/google/medgemma-1.5-4b-it/commit/91850547d9f0b2fdd21aa7c5f4f3d1a8a52c243b
- https://developers.google.com/health-ai-developer-foundations/terms
- https://developers.google.com/health-ai-developer-foundations/prohibited-use-policy
- https://developers.google.com/health-ai-developer-foundations/faqs

## Slot 5 — Optional challenger

```text
challenger = EMPTY
population = PROHIBITED_BY_FD-MESC-BT-READINESS-REPAIR-1
```

The empty challenger is not a blocker.

## Roster proof

Three distinct candidates are independently admissible for proposal into a future execution-authorization candidate, satisfying the minimum competitive-roster count in isolation. However, Apertus is a non-empty roster slot and remains `BLOCKED`; therefore canonical semantics force the **overall readiness verdict to `BLOCKED`** regardless of the three admitted candidates.
