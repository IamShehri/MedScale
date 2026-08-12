# P01-05 B1 Evidence-Source Annotation Protocol

This document defines the deterministic, label-blind annotation protocol for
the B1 supplied-evidence channel ratified by FD-P01-05-B1-EVIDENCE-1. It
controls annotation behavior only; it does not authorize B1 implementation or
execution.

```text
Annotation protocol version:
mesc-pilot-01-b1-annotation/1

Evidence-cue contract:
mesc-pilot-01-b1-evidence-cue/1
```

## 1. Annotation task

For each selected example, human annotators identify which native context
segments are materially relevant to answering the question.

Allowed annotation result:

```text
one or more relevant segment references

OR:

EVIDENCE_INSUFFICIENT

OR:

EVIDENCE_AMBIGUOUS
```

The annotator MUST NOT:

- rewrite evidence
- summarize evidence
- generate a rationale
- write a proposed answer
- write yes/no/maybe
- create claims
- infer final_decision
- create synthetic scientific text

This is evidence SELECTION only.

## 2. Annotation input (strict label blinding)

Annotator access is limited to:

```text
example identity
source-document identity
question
ordered native context segments
```

plus only operational metadata required to perform annotation.

The annotator MUST NOT have access to:

```text
final_decision
long_answer
gold decision
gold answer
gold claims
existing model prediction
B0 prediction
B1 prediction
model confidence
test-result information
```

## 3. Annotation output record

Each per-example record conforms to `mesc-pilot-01-b1-evidence-cue/1`:

```text
schema_version: mesc-pilot-01-b1-evidence-cue/1
evidence_id: <deterministic id>
example_id: <immutable example identity>
source_document_id: <accepted local source-record document id>
ordered_segment_references: <source_document_id + context segment index, ordered>
ordered_segment_sha256s: <sha256 per resolved segment, ordered>
annotation_status: AVAILABLE | INSUFFICIENT | AMBIGUOUS
annotation_protocol_version: mesc-pilot-01-b1-annotation/1
review_status: <review state>
```

Raw scientific text is not persisted in canonical repository artifacts.
Segment references resolve deterministically against the accepted local
source-record artifact and are bound by SHA-256.

## 4. Deterministic 100-example subset selection

Selection is label-blind. No stratification using final_decision, yes/no/maybe
labels, model accuracy, difficulty, model output, or manual preference is
permitted.

Domain separator (canonical, fixed before subset production):

```text
mesc-pilot-01-b1-evidence-subset/1
```

Deterministic procedure:

1. take all 150 frozen validation example identities;
2. compute a domain-separated SHA-256 ordering key from each immutable
   example_id using the domain separator above;
3. sort ascending by that hash;
4. choose the first 100.

The exact key derivation:

```text
key = SHA-256( domain_separator || ":" || example_id )
```

No random seed alone. No manual cherry-picking. No label balancing. The
resulting 100-example identity set is frozen before annotation begins.

```text
DEVELOPMENT PARTITION: validation (frozen)
VALIDATION POPULATION: 150
DETERMINISTIC SUBSET SIZE: 100
SUBSET SELECTION METHOD: domain-separated SHA-256 ordering of immutable
example_ids, ascending, first 100
```

## 5. Human review protocol

Use at least two independent annotators:

```text
Annotator A
Annotator B
```

Both are blinded under the strict label-blinding rule. If their ordered
evidence selections differ materially, require human adjudication. The
adjudicator remains label-blind. Only stable reviewer-role identities or
pseudonymous reviewer IDs are recorded in canonical evidence. Personal data is
not recorded unnecessarily.

## 6. Disagreement / insufficiency

The protocol permits:

```text
AVAILABLE
INSUFFICIENT
AMBIGUOUS
```

An evidence span is not forced when the context is insufficient. B1 preserves
the abstention philosophy. An evidence pack is not valid merely because every
example has at least one selected segment.

## 7. Development evidence pack scope

The initial B1 evidence pack is DEVELOPMENT / QUALIFICATION evidence only,
using exactly 100 examples from the frozen validation partition (size 150).

```text
Train examples: NOT USED
Test examples: NOT USED
```

## 8. Test-set protection

The frozen test partition (150 examples) is NOT used, annotated, inspected, or
hash-matched for B1 development in this phase. A test B1 evidence pack is NOT
created. After B1 implementation acceptance, prompt/contract freezing, and
validation qualification, a separate founder-authorized test
evidence-production gate may create a label-blind test evidence pack under
this same protocol. This prevents test evidence from becoming a
prompt-development surface.

## 9. Gold-separation

The B1 evidence-cue ledger is INPUT CONDITION DATA. It is not Layer-2 gold
claim-support truth, gold answer data, gold final-decision data, or a scoring
target. Any Layer-2 gold claim-support ledger is a logically separate artifact
and is never supplied to the model as B1 input.

## 10. Execution boundary

This protocol does NOT authorize:

- B1 implementation
- evidence-pack production
- model execution
- B0 execution
- retrieval of any kind
- test-partition inspection
- P01-06

Paired future qualification comparison (B0 vs B1) must use the exact same
selected 100 validation example identities, holding model, model revision,
tokenizer revision, generation configuration, prompt-family versioning
discipline, seed, scoring, and example ordering constant where scientifically
possible. Any unavoidable prompt-template difference must be explicitly
versioned. No execution is authorized by this protocol.