# MESC Pilot-01 — P01-05 B0 Real Zero-Shot Validation Execution Acceptance

Status: **COMPLETE / ARTIFACT-INTEGRITY VERIFIED**

Founder decision: `FD-P01-05-B0-EXEC-1`

Execution date: 2026-08-19

This package records the later, separately authorized real B0 execution that followed
the historical P01-05 entry contract. It does **not** rewrite the historical fact
that the original P01-05 entry-contract adoption did not itself authorize real
execution.

## Accepted execution

```text
experiment:
P01-05 B0 REAL ZERO-SHOT VALIDATION EXECUTION

model:
meta-llama/Llama-3.2-3B-Instruct

model revision:
0cb88a4f764b7a12671c53f0838cd831a0843b95

tokenizer revision:
0cb88a4f764b7a12671c53f0838cd831a0843b95

dataset:
qiaojin/PubMedQA / pqa_labeled

dataset revision:
9001f2853fb87cab8d220904e0de81ac6973b318

frozen validation examples:
150

code commit:
5e073db72149266a4e14993cc2501ea2e0e163f5

code tree:
07443a6b9cc0845c5e83de6a80012e6fcfacba47

run digest:
66797ef270714a482bc1346513e9c61b98a7ffa5880b12bfb79834b1baeb6ae9
```

## Result

```text
total:                 150
parsed:                150
unparseable:           0
ambiguous:             0
generation_failed:     0
correct:               104
accuracy:              0.6933333333333334
coverage:              1.0

predicted distribution:
maybe 1
no    47
yes   102

gold distribution:
maybe 17
no    50
yes   83
```

These are validation results only. They are not test-set results, a clinical
performance claim, a publication claim, or evidence that any later Pilot-01 phase
is successful.

## Evidence model

The execution evidence remains external. Canonical repository state records the
stable identities, hashes, sizes, run digest, protocol facts, and acceptance
disposition. No model weights, PubMedQA question/context text, or test scientific
content are added to Git.

The externally preserved evidence bundle is identified by:

```text
filename:
mesc-p01-05-b0-real-zero-shot-validation-1-evidence.zip

sha256:
3502ba1b2ddaf006d2465db01ef9722b0da171a6eeb667837110d93c44a40aa1

size:
22957
```

Artifact-integrity verification recomputed the canonical run digest from the
preserved report and checked internal identities, hashes, prediction uniqueness,
row-ordinal uniqueness, and aggregate consistency. This is **not** an independent
model rerun or scientific replication.

## Hard boundaries

This acceptance record does not authorize:

- B1 real model execution
- a second B0 run
- test-partition execution or scientific-content inspection
- P01-06 or later Pilot-01 phases
- retrieval
- training or fine-tuning
- fallback-model substitution
- quantization changes
- MESC vNext implementation
- publication or clinical claims

No source, test, runtime, or product behavior is changed by this package.
