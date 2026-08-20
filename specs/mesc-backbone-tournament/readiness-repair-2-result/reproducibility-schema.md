# MESC Backbone Tournament — Reproducibility and Artifact Schema

Status: **FROZEN READINESS CONTRACT — FUTURE EXECUTION ONLY**

This schema defines what a separately authorized tournament must record. It creates no execution authority.

Frozen readiness artifact identities:

```text
READINESS_CORPUS_SPEC_SHA256 = 73a236db0fe4a7ab9064d87b70d8dac98b3a7f1bf15132ac239f2393072d65c3
TASK_PROMPT_BUNDLE_SHA256 = fb0b24fbc55f81e3fc3b828fe9b7c291df883e82c8f9362f2cf2d8afeedca777
SYSTEM_PROMPT_SHA256 = 02bb1a1fe70036c5d5299d6654618a2734aa03550506d1b023904cefc88ba867
PROTOCOL_CONFIG_SHA256 = 30e9402ef10739da040a741938a7bcac1405d81d97884e08bfbd88f0b0446baa
PROMPT_PROTOCOL_SHA256 = 0928585636fc3ea2e3b1066ac0cf19a30b38bb69ffad6a1b240247bb2f566ef1
REPORT_SCHEMA_SHA256 = e0183fe7df42575d31a2759a097a362fdec05ad600256d4061de368617c80c56
```

## 1. Run identity

Every future candidate run must bind:

```text
mesc_commit_sha
mesc_tree_sha
candidate_id
candidate_model_revision
candidate_tokenizer_or_processor_id
candidate_tokenizer_or_processor_revision
runtime_adapter_or_custom_code_revision
protocol_id
protocol_config_sha256
prompt_bundle_sha256
prompt_protocol_sha256
readiness_corpus_spec_sha256
materialized_corpus_sha256
materialized_corpus_item_count
report_schema_sha256
hardware_identity
provider_identity
runtime_versions
run_started_at_utc
run_finished_at_utc
```

No field that determines executable identity may float to `main`, `latest`, or an unpinned package version.

`readiness_corpus_spec_sha256` identifies the frozen 240-slot readiness manifest. `materialized_corpus_sha256` identifies the later concrete synthetic/hand-authored JSONL case bytes. They are different artifacts and must never be substituted for one another.

## 2. Environment identity

Record at minimum:

- OS and kernel/runtime image identity;
- Python version;
- PyTorch version;
- Transformers/vLLM or other engine exact version/commit;
- CUDA and driver versions for local GPU execution;
- GPU model, count, and VRAM;
- quantization/precision exactly as authorized;
- `trust_remote_code` state;
- exact repository code hash when remote/custom code is enabled;
- provider endpoint/model deployment identity when execution is remote;
- access/gating evidence reference without exposing credentials.

Phi-4 custom code must be pinned to the exact admitted model revision. Apertus temporary Transformers compatibility code must be pinned to the exact compatibility revision authorized by the future execution package.

## 3. Per-item artifact record

Minimum normalized record:

```json
{
  "candidate_id": "...",
  "candidate_revision": "...",
  "item_id": "BT-A-001",
  "axis": "A_MEDICAL_REASONING",
  "task_template_id": "MESC-BT-TASK-A-V1",
  "prompt_hash": "sha256:...",
  "raw_output_path": "...",
  "raw_output_sha256": "...",
  "parse_status": "PASS|FAIL",
  "normalized_answer_state": "...",
  "abstention_category": "...|null",
  "score_components": {},
  "critical_safety_failure": false,
  "latency_ms": 0,
  "input_tokens": 0,
  "output_tokens": 0,
  "peak_vram_mb": null,
  "error_class": "NONE"
}
```

Raw outputs must be preserved where safe. Normalization must not overwrite or substitute raw model output.

## 4. Aggregate report

The canonical future report schema is `report-schema.json` with SHA-256:

`e0183fe7df42575d31a2759a097a362fdec05ad600256d4061de368617c80c56`

For every admitted/executed candidate, the schema **requires**, rather than merely documents:

- `items_attempted` and `items_completed` counts;
- explicit integer counts for `TIMEOUT`, `RUNTIME_FAILURE`, `GENERATION_FAILURE`, `PARSE_FAILURE`, `SCHEMA_FAILURE`, `SAFETY_FAILURE`, and total errors;
- six visible axis scores;
- aggregate score using only frozen weights;
- critical safety failure count;
- Compact gate result;
- Flagship/Reasoner gate result;
- median/p95 latency;
- peak VRAM where measurable;
- total input/output tokens;
- provider cost where applicable;
- exclusions as typed records containing `item_id`, reason, and error class;
- candidate-level negative results as typed records;
- top-level negative-result records tied to candidate identity.

The schema is fail-closed with `additionalProperties=false` on the report root, candidate report, error-count object, exclusion object, and negative-result objects. A report that omits the required evidence cannot validate as `MESC-BT-REPORT-V1`.

No silent candidate removal is permitted after execution begins.

## 5. Deterministic run digest

A future implementation must construct a canonical run manifest as UTF-8 canonical JSON with sorted keys and compact separators. The run digest is SHA-256 over that canonical manifest. Timestamps and filesystem paths may be included in the evidence report but must not substitute for content hashes.

The manifest must reference every per-item raw-output hash, the readiness corpus-spec hash, the later materialized-corpus hash, prompt bundle hash, protocol hash, report-schema hash, and exact execution environment so a third party can prove what was evaluated.

## 6. Access and secret handling

Credentials, access tokens, private gated artifacts, and accepted-terms receipts must never be committed as secrets. A future execution package may record non-secret evidence that the explicitly authorized operator completed required access steps, but repair-2 neither performs nor authorizes those steps.

## 7. Claim boundary

No tournament performance, role winner, clinical capability, or publication claim exists until a separately authorized run executes and the committed artifacts satisfy R5 and R7. This readiness package records only static evidence and frozen, digest-bound readiness artifacts.
