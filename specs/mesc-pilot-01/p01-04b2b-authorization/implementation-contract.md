# P01-04B2B Implementation Authorization — Implementation Contract

```text
Status:
PROSPECTIVE CONTRACT — NOT EXECUTABLE

THIS CONTRACT BINDS A FUTURE IMPLEMENTATION TASK.
IT BECOMES OPERATIVE ONLY AFTER ALL FIVE FD-B2B-10 ACTIVATION CONDITIONS ARE
SATISFIED AND MECHANICALLY VERIFIED. RECORDING IT IN A DRAFT PULL REQUEST
AUTHORIZES NO IMPLEMENTATION.
```

Canonical authority: [`founder-authorization.md`](founder-authorization.md).

---

## 1. Exact primitive definitions

All primitives are pure, pairwise, and total over their declared input domain.
Each takes explicit in-memory primitive values and returns a primitive result.

| Primitive | Inputs | Semantics | Result |
|---|---|---|---|
| `exact_example_identity` | two canonical `example_id` values | byte equality of UTF-8 bytes | `bool` |
| `exact_source_document_identity` | two canonical `source_document_id` values | byte equality of UTF-8 bytes | `bool` |
| `exact_question_equality` | two question strings | byte equality of UTF-8 bytes | `bool` |
| `exact_context_equality` | two context strings | byte equality of UTF-8 bytes | `bool` |
| `normalize_question` | one question string | the §2 pipeline | normalized `str` |
| `tokenize` | one normalized string | the §2 tokenization | `frozenset[str]` |
| `normalized_question_equality` | two question strings | equality of normalized forms | `bool` |
| `token_set_jaccard` | two token sets | exact set Jaccard, §3 | score or non-evaluable marker |

`exact_context_equality` is the exact-byte primitive corresponding to the
`context_equality` deliverable named in the adopted plan. Naming is clarified,
not changed.

**Input domain.** Exact built-in types only. Subclasses are rejected where exact
primitive identity is required — in particular `bool` must not satisfy an `int`
requirement. No implicit coercion, no registry lookup, and no filesystem,
network, environment, clock, locale, or process access. No primitive accepts
arbitrary records, dataset rows, paths, file handles, repository references,
evidence-root references, or P01-03G objects.

**Separation.** Exact equality and normalized or approximate equality are
separate methods producing separate finding types. No exact-equality primitive
normalizes its inputs.

## 2. Normalization and tokenization

Normalization pipeline, in this exact order:

```text
1. Unicode NFKC
2. Unicode case folding
3. collapse each run of Unicode whitespace to one ASCII space
4. remove leading and trailing whitespace
```

Tokenization:

```text
1. tokens are maximal consecutive Unicode alphanumeric runs
2. punctuation and whitespace are boundaries
3. empty tokens are discarded
4. tokens form a set, not a multiset
```

Punctuation is retained through normalization and acts as a token boundary at
tokenization. No locale-specific normalization. No stemming, lemmatization,
stop-word removal, transliteration, or semantic embedding.

## 3. Threshold behaviour

```text
Question near duplicate:         score >= 0.90
Approximate context overlap:     score >= 0.95
```

- Equality **at** the threshold is a match.
- No tolerance or epsilon adjustment.
- No rounded value determines threshold passage.
- The unrounded mathematical ratio `intersection_size / union_size` determines
  passage.
- Approximate context findings remain `unresolved` until separately classified.

Implementations must compare exactly. Comparing a rounded or float-formatted
value against the threshold is prohibited.

## 4. Empty-input behaviour

```text
Both normalized questions empty:
no score is fabricated; the condition maps to empty_normalized_question

Exactly one token set empty:
the comparison is not_evaluable
```

`not_evaluable` must never be silently reported as clean. An
`empty_normalized_question` condition is not auto-classified as non-leakage; its
initial classification is `unresolved`.

## 5. Rational score representation

For deterministic finding identity, a valid Jaccard score is represented in
exact reduced rational form:

```text
jaccard:<intersection_size>/<union_size>
```

```text
none            — for exact methods
not_evaluable   — when no score exists
```

The stored report `score` remains a finite float or null as defined by the
adopted contract. The rational form is used **only** in the deterministic
finding-ID payload. NaN and infinity are rejected wherever a score is accepted.

## 6. Finding-ID schema and payload

```text
Finding schema identifier:
mesc-pilot-01-leakage-finding/1

Finding-ID format:
mesc-pilot-01-leakage-finding/1:sha256:<64-lowercase-hex>
```

The SHA-256 payload binds, in this order:

```text
1. finding schema version
2. finding type
3. example IDs sorted lexicographically
4. source-document IDs sorted lexicographically
5. partitions sorted lexicographically
6. normalized score representation
```

A one-bit semantic change in any bound component must change the finding ID.

## 7. Finding ordering

Findings in a report are ordered by ascending `finding_id`. No insertion order,
hash iteration order, runtime locale, or caller ordering may influence the
result.

## 8. Classifications

Allowed classifications are exactly:

```text
unresolved
false_positive
confirmed_leakage
```

Every finding must carry exactly one. `false_positive` requires a non-empty
stable supporting-evidence reference.

## 9. Suppression prohibition

```text
suppressed must always be false
```

Suppression is prohibited. Dropping, omitting, filtering, or suppressing a
detected finding is fail-closed. `finding_count` must equal the exact number of
findings. A leakage-positive synthetic fixture must not produce a vacuous empty
report.

## 10. Aggregate `leaked` clarification

```text
leaked = true
when at least one finding is unresolved or confirmed_leakage

leaked = false
only when no findings exist or every finding is a supported false_positive
```

This is a fail-closed clarification of the existing aggregate-report wording. It
does not alter the three allowed classifications.

## 11. Raw-text boundary

Raw question, context, and answer text may exist only as transient in-memory
primitive inputs. It must never be stored in a `LeakageFinding`, enter canonical
bytes, or enter logs, exceptions, repr output, reports, manifests, fingerprints,
evidence references, or repository artifacts.

`shared_surface` may contain only these allowlisted semantic markers:

```text
example_id
source_document_id
question_bytes
normalized_question
question_token_set
context_bytes
context_token_set
empty_normalized_question
```

It must not contain a copied substring, token value, question, context, answer,
or other raw surface text.

## 12. Deterministic errors

Typed private errors are required for:

```text
invalid primitive input
invalid finding type
invalid classification
invalid score
invalid evidence reference
suppression attempt
raw-text-bearing promotable value
invalid finding identifier
invalid report invariant
```

Each carries a stable machine-readable error code. Validation order is
deterministic. Error messages contain no raw input text and no path, username,
hostname, environment, timestamp, or runtime metadata.

No file, network, subprocess, logging, telemetry, cache, or global-state side
effect is permitted. **No new dependency is authorized.**

## 13. Allowed implementation contents

The future implementation may include only:

```text
immutable private LeakageFinding
immutable private LeakageAuditReport
exact equality primitives
deterministic question normalization
deterministic Unicode-alphanumeric tokenization
exact token-set Jaccard
deterministic finding-ID generation
strict finding/report validation
canonical-document and canonical-byte generation through the already accepted
  B2A serializer
synthetic unit and golden-vector tests
```

The implementation **must** import and reuse the accepted B2A canonicalization
helpers where appropriate. It must not duplicate or fork canonical JSON
behaviour.

## 14. Prohibited orchestration and I/O

The implementation must not include:

```text
record-pair enumeration
dataset scanning
registry scanning
leakage-audit orchestration
automatic finding discovery over a collection
fixture facade
split facade
CLI
filesystem publication
path safety
concurrency
real execution
integrated qualification
```

A caller may construct and validate explicit synthetic findings **in tests**. No
production function may accept a sequence of dataset records and search it for
leakage.

## 15. Required tests

The later implementation gate requires at least the following.

### Type and validation

- exact built-in input type enforcement;
- `bool`/`int`/subclass confusion rejected where applicable;
- invalid finding types rejected;
- invalid classifications rejected;
- unsupported score values rejected;
- NaN and infinity rejected;
- suppression attempts rejected;
- `false_positive` without evidence reference rejected;
- raw-text-bearing promotable values rejected.

### Exact equality

- identical bytes pass;
- case differences fail;
- Unicode normalization differences fail under exact comparison;
- trailing or repeated whitespace differences fail under exact comparison.

### Normalization

- NFKC behaviour;
- case folding;
- Unicode whitespace collapse;
- leading/trailing whitespace removal;
- Arabic and Latin input stability;
- punctuation retained for normalization but treated as token boundaries;
- no locale dependence.

### Tokenization and Jaccard

- maximal Unicode alphanumeric runs;
- punctuation boundaries;
- token-set rather than multiset behaviour;
- exact `0.90` threshold pass;
- immediately below `0.90` fail;
- exact `0.95` threshold pass;
- immediately below `0.95` fail;
- both-empty normalized questions;
- exactly-one-empty token set;
- no fabricated score;
- deterministic rational score representation.

### Findings

- deterministic ID across reruns;
- caller-order independence;
- lexicographic ID/source/partition normalization;
- score representation included;
- exact methods bind `none`;
- non-evaluable comparisons bind `not_evaluable`;
- one-bit semantic changes alter the finding ID;
- report findings sorted by ID;
- raw text absent from canonical document and bytes.

### Classification and report

- unresolved sets `leaked=true`;
- confirmed leakage sets `leaked=true`;
- all supported false positives set `leaked=false`;
- empty report behaviour is explicit;
- finding count exact;
- suppression impossible;
- leakage-positive synthetic report cannot be vacuous.

### Determinism

- repeated canonical bytes identical;
- no timestamps;
- no paths;
- no environment metadata;
- no host/user metadata;
- no mutable caller-owned collections retained;
- no side effects.

## 16. Path scope for the future implementation

```text
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py
```

Exactly two paths. If implementation proves impossible within them, stop and
return for a new founder authorization. Do not expand the allowlist.
