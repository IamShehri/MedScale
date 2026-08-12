# FD-P01-05-B1-EVIDENCE-1 - B1 Supplied-Evidence Source Ratification

This is the controlling document of the P01-05 B1 evidence-source
ratification package. It ratifies the canonical source and protocol for the B1
supplied-evidence channel. On any conflict with the other documents in this
package, this document controls.

## 1. Decision identity

```text
Founder decision:
FD-P01-05-B1-EVIDENCE-1

Decision class:
EVIDENCE-SOURCE RATIFICATION - P01-05 B1 SUPPLIED-EVIDENCE CHANNEL

Scope:
DOCUMENTATION / GOVERNANCE / PROTOCOL RATIFICATION ONLY
```

## 2. Bound canonical pre-ratification state

```text
BASE CANONICAL MAIN:
4e5e8d13aa85da03e1b366813874cd2f0d178769

BASE CANONICAL TREE:
b6e10ab4e6d38c262cc8ffe14fdb7719cae0febf

P01-04:
COMPLETE / CLOSED

MESC vNext:
CANONICALLY RATIFIED

P01-05 ENTRY CONTRACT:
CANONICALLY ADOPTED

B0 IMPLEMENTATION:
EXISTING / RECONCILED / IDENTITY-BOUND

B0 EXECUTION:
NOT AUTHORIZED

B1 EVIDENCE SOURCE:
UNRESOLVED / BLOCKING

B1 IMPLEMENTATION:
NOT AUTHORIZED

B1 EXECUTION:
NOT AUTHORIZED
```

## 3. Ratified B1 supplied-evidence source

```text
B1 SUPPLIED-EVIDENCE SOURCE:
MANUAL, LABEL-BLIND, DETERMINISTIC EVIDENCE-CUE ANNOTATIONS
OVER THE NATIVE PUBMEDQA CONTEXT
```

- B1 does NOT use an external evidence corpus.
- B1 does NOT perform retrieval.
- B1 does NOT use RAG.
- B1 does NOT use a teacher model.
- B1 does NOT use LLM-generated evidence.

Every B1 evidence cue resolves to one or more existing ordered context
segments belonging to the SAME scientific example/source document. The source
is therefore:

```text
accepted local PilotPubMedQASourceRecord
+
native ordered context segments
+
manual evidence-selection annotation
```

No external document, additional PubMed article, guideline, or retrieved
document may enter B1. Those belong to later retrieval/evidence phases.

## 4. B0 / B1 semantic boundary

```text
B0 =
question
+
native PubMedQA context
+
no additional evidence channel

B1 =
the exact same scientific question/context input
+
an explicit supplied-evidence cue channel
```

B1 differs from B0 ONLY by the explicit evidence cue. Native context is NOT
removed from B1. B0 prompt semantics are NOT altered by this decision.

## 5. Strict label blinding

The evidence annotator MUST NOT have access to:

- `final_decision`
- `long_answer`
- gold decision
- gold answer
- gold claims
- existing model prediction
- B0 prediction
- B1 prediction
- model confidence
- test-result information

Annotation input is limited to:

- example identity
- source-document identity
- question
- ordered native context segments

plus only operational metadata required to perform annotation.

## 6. Canonical evidence-cue contract

Versioned contract:

```text
mesc-pilot-01-b1-evidence-cue/1
```

Each per-example record contains only deterministic metadata:

```text
schema_version
evidence_id
example_id
source_document_id
ordered_segment_references
ordered_segment_sha256s
annotation_status
annotation_protocol_version
review_status
```

Raw scientific text is NOT persisted in the canonical repository artifact. A
segment reference resolves deterministically against the accepted local
source-record artifact using:

```text
source_document_id
+
context segment index
```

Every resolved segment is also bound by SHA-256.

## 7. Raw text boundary

Raw PubMed abstract/context text remains outside Git tracking. Canonical
repository artifacts may contain IDs, indices, hashes, status values, protocol
metadata, and aggregate counts. They MUST NOT contain copied raw abstract
passages. At B1 runtime, the locally available accepted source record may
resolve an authorized segment reference to its text; that runtime resolution
does NOT authorize redistribution of the text.

## 8. Scientific interpretation

B1 is recorded accurately as:

```text
MANUALLY EVIDENCE-CUED BASELINE
```

B1 is NOT described as: RAG, retrieval augmented, autonomous evidence
discovery, literature search, or external evidence retrieval. B1 measures the
effect of an explicit bounded evidence cue while the underlying native
benchmark context is otherwise held constant.

## 9. Critical gold-separation rule

The B1 evidence-cue ledger is INPUT CONDITION DATA. It is NOT Layer-2 gold
claim-support truth, gold answer data, gold final-decision data, or a scoring
target. If a Layer-2 manually reviewed gold claim-support ledger exists or is
created, it must be a logically separate artifact. Layer-2 gold claim-support
annotations MUST NOT be supplied to the model as B1 input. B1 citation
correctness must not be evaluated merely by checking whether the model repeats
the same evidence annotations that were supplied to it.

## 10. Prohibitions

- `long_answer` is NOT a B1 evidence source. It may not be copied, used to
  derive evidence spans, used to select context, shown to annotators, used for
  adjudication, or hash-matched against as an annotation guide. It remains
  outside the B1 prompt/input condition.
- `final_decision` remains scoring-only gold truth. It must not influence
  evidence selection, subset selection, annotation, adjudication, or B1
  prompting.
- No vector database, BM25, embedding, reranker, search API, PubMed search,
  Europe PMC search, web search, external corpus search, or document ranking
  is permitted in B1. Retrieval remains a separate later experimental
  condition.

## 11. Rights boundary

Repository/package licensing does not transfer copyright in underlying PubMed
abstracts. Raw abstract/context text is not promoted into Git merely because
it is used locally for research. The B1 annotation artifact prefers stable
references and hashes over copied scientific text.

## 12. New controlling status after adoption

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

This decision does NOT authorize implementation of B1, production of the
100-example evidence pack, inspection of the test partition, or any model
execution.