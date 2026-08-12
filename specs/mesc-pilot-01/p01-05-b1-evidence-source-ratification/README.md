# P01-05 B1 Evidence-Source Ratification

This package records the founder ratification of the B1 supplied-evidence
source for P01-05. It resolves the sole remaining P01-05 scientific entry
blocker: the B1 evidence channel was previously recorded as UNRESOLVED /
BLOCKING in the canonical P01-05 entry-contract decision record.

This package is documentation / governance / protocol-ratification only.

```text
B1 EVIDENCE SOURCE:
RATIFIED - MANUAL LABEL-BLIND NATIVE-CONTEXT EVIDENCE CUES

B1 DEVELOPMENT EVIDENCE PACK:
NOT PRODUCED

B1 IMPLEMENTATION:
NOT AUTHORIZED

B1 EXECUTION:
NOT AUTHORIZED

B0 EXECUTION:
NOT AUTHORIZED

TEST EVIDENCE PACK:
NOT AUTHORIZED

P01-06:
NOT AUTHORIZED

vNext Stage 1:
NOT AUTHORIZED
```

## Documents

- [`founder-decision.md`](founder-decision.md) - controlling ratification decision (FD-P01-05-B1-EVIDENCE-1).
- [`annotation-protocol.md`](annotation-protocol.md) - label-blind evidence-selection protocol and deterministic subset-selection procedure.
- [`acceptance.md`](acceptance.md) - acceptance criteria and review findings.
- `README.md` - this navigation note; non-controlling.

## Boundaries preserved by this ratification

- B1 uses NO external evidence corpus, NO retrieval, NO RAG, NO teacher model, NO LLM-generated evidence.
- B1 evidence cues resolve only to native ordered context segments of the SAME accepted source record.
- Annotation is strictly label-blind under the P01-05 B1 evidence-source contract.
- `long_answer` is prohibited as an evidence source; `final_decision` remains scoring-only gold truth.
- The 100-example development evidence pack is selected deterministically from the frozen validation partition only.
- Raw PubMed abstract/context text remains outside Git tracking.

No raw scientific text, absolute paths, timestamps, hostnames, or usernames are
committed by this package. Evidence records bind segments by stable reference
(`source_document_id` + context segment index) and SHA-256 only.