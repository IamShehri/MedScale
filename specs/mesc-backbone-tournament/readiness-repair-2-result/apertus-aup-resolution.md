# Apertus 1.5 AUP — Repair-2 Resolution

Status: **EVIDENCE COMPLETE — CANDIDATE DISPOSITION RECORDED**

Authority: `FD-MESC-BT-READINESS-REPAIR-2`

## 1. Authoritative artifact

Repository: `swiss-ai/apertus-legal`

Path: `apertus_1.5/USAGE_POLICY.pdf`

The authoritative GitHub contents metadata identified:

```text
byte_length = 53794
git_blob_sha1 = 8ddd8e25b6672340dd4f921ba623578571a65526
```

The episode retrieved only this public legal artifact. No model weights or gated repository contents were requested or accessed.

## 2. Binary-safe reconstruction and binding

The public PDF Base64 was fetched from GitHub in exact line-bounded ranges. The reconstructed bytes were verified locally before interpretation:

```text
reconstructed_byte_length = 53794
sha256 = 424b0a0d24ee1369f9a8614d9e4c7eb0fc3ee8a9ad7ece39baea3a83f0d4ba76
computed_git_blob_sha1 = 8ddd8e25b6672340dd4f921ba623578571a65526
authoritative_git_blob_sha1 = 8ddd8e25b6672340dd4f921ba623578571a65526
binding = EXACT_MATCH
```

The computed Git object identity used the canonical `blob <length>\0<bytes>` construction. Interpretation was performed only after exact object equality was proven.

## 3. Render/text verification

The exact bound artifact:

- is a one-page PDF;
- renders without observed corruption, clipping, overlap, or unreadable material text;
- identifies itself as `Apertus LLM Acceptable Use Policy (AUP)`;
- identifies the version as `v1.5`;
- identifies the date as `July 14, 2026`.

No OCR was required.

## 4. Material restrictions relevant to MESC

The exact v1.5 AUP includes obligations relevant to future use and distribution, including:

- compliance with the AUP and applicable law;
- indemnification obligations in favor of ETH Zurich / EPFL for covered third-party claims;
- when Apertus is redistributed, provision of the then-current AUP, express recipient assent, and contractual pass-through of the same obligations to downstream redistribution;
- independent-controller responsibilities when Personal Data is processed;
- an output-filter mechanism associated with deletion requests and a recommendation to apply the filter periodically.

These obligations are material and must be carried into any later exact execution, derivative-release, or distribution decision. They do not themselves authorize any such action.

## 5. Program-rule assessment

### R2

The future MESC tournament is restricted to synthetic or hand-authored fixtures. No Personal Data, patient data, PHI, product telemetry, or external prohibited clinical content is admitted. The AUP does not require violating R2.

### R3

Apertus 1.5 is published under Apache-2.0 with the additional AUP obligations above. The evidence reviewed does not establish a prohibition on model derivatives or commercial use. Redistribution creates compliance/pass-through duties rather than a categorical derivative/commercial-use ban.

Therefore the evidence does not establish an R3 disqualifier.

### Gated access

The model repository is gated and requires acceptance of publisher terms before weight access. The readiness contract expressly separates current admission evidence from later model-weight access. Repair-2 neither requested access nor accepted terms. A future execution authorization must bind and separately authorize any gated-access action before it occurs.

Gating is therefore a future execution precondition, not an unresolved readiness fact.

## 6. Resolution

The prior blocker:

`BT-RDY-BLK-APERTUS-AUP-001`

is resolved because the exact v1.5 AUP artifact is now byte-bound, readable, materially interpreted, and assessed against R2/R3 without prohibited weight or gated access.

Candidate disposition:

```text
swiss-ai/Apertus-v1.5-8B
revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
DISPOSITION = ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE
```

This disposition grants no model access or execution authority.
