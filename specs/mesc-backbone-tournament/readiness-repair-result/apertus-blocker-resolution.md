# Apertus 1.5 Blocker Resolution Report

Status: **UNRESOLVED / TERMINAL BLOCKER**

Date: 2026-08-20

## Finding

```text
ID = BT-RDY-BLK-APERTUS-AUP-001
CANDIDATE = swiss-ai/Apertus-v1.5-8B
CATEGORY = LICENSE / ACCEPTABLE-USE EVIDENCE
DISPOSITION = BLOCKED
```

## Exact model identity refreshed

```text
model_id = swiss-ai/Apertus-v1.5-8B
model_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
processor_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
tokenizer_revision = a411d838600baf0e3635a3daf66fb7c55fc97bb6
```

The public first-party model card records Apache-2.0 plus an explicit gated-access agreement to the Apertus 1.5 AUP and privacy policy.

## Exact authoritative AUP artifact

The authoritative public legal repository exposes:

```text
repository = swiss-ai/apertus-legal
path = apertus_1.5/USAGE_POLICY.pdf
git_blob_sha = 8ddd8e25b6672340dd4f921ba623578571a65526
size = 53794 bytes
```

The same exact path is referenced by the current Apertus v1.5 model-card gate.

## Evidence attempts

The bounded episode performed public read-only inspection only.

1. GitHub directory metadata mechanically resolved the exact path, blob SHA, and size.
2. GitHub UTF-8 content interfaces could not decode the binary PDF blob.
3. Direct public raw GitHub retrieval exposed the artifact as `application/octet-stream`; the available web PDF renderer therefore could not produce a page screenshot or complete text representation.
4. The Hugging Face model page exposes the AUP reference but requires clicking an agreement/request gate before repository-file access. The repair authorization prohibits requesting or accepting gated model access, gated-access terms, or model-access agreements for any purpose, so that route was not used.
5. No third-party summary, search snippet, older Apertus policy, newer Apertus policy, or model-generated legal summary was substituted because the canonical acceptance contract explicitly rejects those as admission evidence.

## Material conclusion

The episode proves **artifact identity**, but it does not prove the complete material use restrictions contained in that exact artifact.

Therefore it cannot establish either:

- compatibility with MESC Program Rule R2 and R3; or
- conclusive incompatibility with the bounded R2 tournament scope.

The canonical disposition semantics require:

```text
missing / unreadable / incomplete / ambiguous exact terms => BLOCKED
conclusive authoritative incompatibility => NOT_ADMITTED
```

Accordingly:

```text
APERTUS_DISPOSITION = BLOCKED
NOT_ADMITTED = NO
BLOCKER_RESOLVED = NO
```

## Consequence

Because Apertus is a non-empty roster slot, this unresolved blocker forces:

```text
READINESS_RESULT = BLOCKED
PROTOCOL_FREEZE = NOT_PERFORMED
EXECUTION_AUTHORIZATION_CANDIDATE = NOT_PRODUCED
```

No gated agreement was accepted, no weights were accessed, and no model execution occurred.

## Primary sources

- https://huggingface.co/swiss-ai/Apertus-v1.5-8B
- https://huggingface.co/swiss-ai/Apertus-v1.5-8B/commit/a411d838600baf0e3635a3daf66fb7c55fc97bb6
- https://github.com/swiss-ai/apertus-legal/tree/main/apertus_1.5
- https://github.com/swiss-ai/apertus-legal/blob/main/apertus_1.5/USAGE_POLICY.pdf
