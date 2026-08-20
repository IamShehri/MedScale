# MESC Backbone Tournament — Reproducibility and Artifact Schema

Status: **FROZEN READINESS CONTRACT — FUTURE EXECUTION ONLY**

This schema defines what a separately authorized tournament must record. It creates no execution authority.

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
system_prompt_sha256
corpus_sha256
corpus_item_count
hardware_identity
provider_identity
runtime_versions
run_started_at_utc
run_finished_at_utc
```

No field that determines executable identity may float to `main`, `latest`, or an unpinned package version.

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

For every admitted/executed candidate, report:

- item count attempted/completed;
- every failure/error count;
- six visible axis scores;
- aggregate score using only frozen weights;
- critical safety failure count;
- Compact gate result;
- Flagship/Reasoner gate result;
- median/p95 latency;
- peak VRAM where measurable;
- total generated tokens;
- provider cost where applicable;
- exclusions with explicit reasons;
- all negative results.

No silent candidate removal is permitted after execution begins.

## 5. Deterministic run digest

A future implementation must construct a canonical run manifest as UTF-8 canonical JSON with sorted keys and compact separators. The run digest is SHA-256 over that canonical manifest. Timestamps and filesystem paths may be included in the evidence report but must not substitute for content hashes.

The manifest must reference every per-item raw-output hash and the materialized corpus/protocol hashes so a third party can prove what was evaluated.

## 6. Access and secret handling

Credentials, access tokens, private gated artifacts, and accepted-terms receipts must never be committed as secrets. A future execution package may record non-secret evidence that the explicitly authorized operator completed required access steps, but repair-2 neither performs nor authorizes those steps.

## 7. Claim boundary

No tournament performance, role winner, clinical capability, or publication claim exists until a separately authorized run executes and the committed artifacts satisfy R5 and R7. This readiness package records only static evidence and a frozen protocol.
