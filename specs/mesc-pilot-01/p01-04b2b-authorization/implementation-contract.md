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
| `token_set_jaccard` | two token sets | exact set Jaccard, §3–§5 | integer counts plus `score_representation` |

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

## 3. Threshold behaviour — exact comparison only

```text
Question near duplicate:         score >= 0.90
Approximate context overlap:     score >= 0.95
```

Threshold passage must use exact integer or rational comparison:

```text
Question threshold:
100 * intersection_size >= 90 * union_size

Context threshold:
100 * intersection_size >= 95 * union_size
```

Equality **at** the threshold is a match. No tolerance or epsilon adjustment.
**No rounded or binary-floating-point value may determine threshold passage.**
Comparing a float-formatted value against the threshold is prohibited.

Approximate context findings remain `unresolved` until separately classified.

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

## 5. Score representation — authoritative and canonical

Exactly one authoritative representation is defined:

```text
score_representation
```

Allowed values are exactly:

```text
none                                       — exact methods, no approximate score
not_evaluable                              — no valid Jaccard score exists
jaccard:<reduced_intersection>/<reduced_union>
```

Rules:

- numerator and denominator are base-10 ASCII integers with no sign and no
  leading zeros, except the single digit `0`;
- the denominator is strictly positive;
- `0 <= numerator <= denominator`;
- the fraction is reduced by the greatest common divisor;
- zero is `jaccard:0/1`; a full match is `jaccard:1/1`.

| intersection / union | `score_representation` |
|---|---|
| 6 / 9 | `jaccard:2/3` |
| 0 / 9 | `jaccard:0/1` |
| 9 / 9 | `jaccard:1/1` |
| exact method | `none` |
| non-evaluable | `not_evaluable` |

### Runtime float is derived and non-authoritative

The adopted in-memory compatibility contract is preserved:

```text
LeakageFinding.score:
finite float or null
```

That field is **runtime-only, derived, and non-authoritative for canonical
identity**. It is excluded from canonical documents, canonical bytes,
fingerprints, and finding-ID payload bytes.

```text
The exact score representation is authoritative in both the canonical finding
document and the deterministic finding-ID payload. A derived finite runtime
float may additionally exist in memory but is never canonicalized or hashed.
```

A binary float must never be passed into the accepted B2A canonical serializer.
The accepted canonical value domain is
`None | bool | int | str | sequence | string-keyed mapping`; a float raises
`FloatingPointValueProhibitedError` with the stable code
`floating_point_value_prohibited`.

The runtime float, when present, is derived from the integer intersection and
union counts for caller convenience only. It must not influence threshold
passage, canonical bytes, equality, ordering, finding identity, report identity,
or evidence identity.

### Canonical document rule

Every promotable finding canonical document must carry `score_representation`
with the authoritative string above and must not carry a binary float. The
representation in the finding document must be **identical** to the
representation bound into the finding-ID payload.

## 6. Finding-ID identity document, payload bytes, and formula

```text
Finding schema identifier:
mesc-pilot-01-leakage-finding/1

Finding-ID format:
mesc-pilot-01-leakage-finding/1:sha256:<64-lowercase-hex>
```

### 6.1 Exact identity document

Exactly these six frozen members and no others:

```json
{
  "schema": "mesc-pilot-01-leakage-finding/1",
  "finding_type": "<validated finding type>",
  "example_ids": ["<lexicographically sorted canonical example IDs>"],
  "source_document_ids": ["<lexicographically sorted source-document IDs>"],
  "partitions": ["<lexicographically sorted partition names>"],
  "score_representation": "<authoritative score representation>"
}
```

Aliases, omitted members, additional members, and alternate container shapes are
prohibited. The semantic ordering above is controlling even though the accepted
canonical JSON serializer deterministically orders object members. Arrays must
already be in canonical lexicographic order **before** serialization.

### 6.2 Exact payload bytes

```text
FINDING_IDENTITY_BYTES =
the accepted B2A canonical single-object JSON byte serialization of the exact
identity document
```

This carries every accepted B2A rule: accepted primitive-domain validation,
canonical object-member ordering, canonical UTF-8 encoding, canonical escaping,
exact single-object framing, the accepted terminal-line-feed rule, and rejection
of floats and other prohibited values. The terminal LF is inside the hashed
bytes.

**Do not duplicate or reimplement canonical JSON.** Use the existing accepted
B2A canonicalization helpers.

### 6.3 Exact finding-ID formula

```text
digest =
SHA-256(FINDING_IDENTITY_BYTES).hexdigest()

finding_id =
mesc-pilot-01-leakage-finding/1:sha256:<digest>
```

The lowercase hexadecimal digest must contain exactly 64 characters. No other
prefix, separator, concatenation, newline convention, JSON shape, or
serialization is valid.

### 6.4 Identity validation

The implementation must regenerate the expected finding ID from the validated
semantic fields and compare it with the supplied value. A mismatch must fail
closed with the typed private invalid-finding-identifier error. Caller-supplied
IDs must never be trusted without deterministic regeneration.

### 6.5 Ordering

Findings in a report are ordered by ascending `finding_id`. No insertion order,
hash iteration order, runtime locale, or caller ordering may influence the
result.

## 7. Classifications

Allowed classifications are exactly:

```text
unresolved
false_positive
confirmed_leakage
```

Every finding must carry exactly one. `false_positive` requires a non-empty
stable supporting-evidence reference.

## 8. Suppression prohibition

```text
suppressed must always be false
```

Suppression is prohibited. Dropping, omitting, filtering, or suppressing a
detected finding is fail-closed. `finding_count` must equal the exact number of
findings. A leakage-positive synthetic fixture must not produce a vacuous empty
report.

## 9. Aggregate `leaked` clarification

```text
leaked = true
when at least one finding is unresolved or confirmed_leakage

leaked = false
only when no findings exist or every finding is a supported false_positive
```

A fail-closed clarification of the existing aggregate-report wording. It does
not alter the three allowed classifications.

## 10. Raw-text boundary

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

## 11. Deterministic errors

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

## 12. Allowed implementation contents

```text
immutable private LeakageFinding
immutable private LeakageAuditReport
exact equality primitives
deterministic question normalization
deterministic Unicode-alphanumeric tokenization
exact token-set Jaccard over integer counts
authoritative score_representation construction
deterministic finding-ID generation
strict finding/report validation
canonical-document and canonical-byte generation through the already accepted
  B2A serializer
synthetic unit and golden-vector tests
```

The implementation **must** import and reuse the accepted B2A canonicalization
helpers where appropriate. It must not duplicate or fork canonical JSON
behaviour.

## 13. Prohibited orchestration and I/O

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

## 14. Required tests

### 14.1 Canonical score representation

Required cases:

```text
6 / 9  → jaccard:2/3
0 / 9  → jaccard:0/1
9 / 9  → jaccard:1/1
exact method → none
non-evaluable → not_evaluable
```

Verify:

- no float exists in a canonical finding document;
- accepted B2A serialization succeeds for score-bearing findings;
- direct attempted serialization of the runtime float remains prohibited and
  raises the accepted floating-point-prohibited error;
- runtime float changes cannot change canonical bytes when the authoritative
  integer counts and `score_representation` are unchanged;
- malformed, unreduced, signed, zero-denominator, or leading-zero
  representations fail closed.

### 14.2 Finding-ID payload

Commit literal synthetic golden vectors for:

- the exact identity object;
- exact canonical identity bytes;
- the SHA-256 digest;
- the complete finding ID.

Verify:

- alternate JSON key names fail;
- missing or additional identity members fail;
- array-order changes are normalized before serialization;
- semantic changes change the ID;
- alternate separators or manual concatenation cannot substitute for B2A
  canonical serialization;
- repeated runs produce identical bytes and IDs.

### 14.3 Type and validation

- exact built-in input type enforcement;
- `bool`/`int`/subclass confusion rejected where applicable;
- invalid finding types rejected;
- invalid classifications rejected;
- unsupported score values rejected;
- NaN and infinity rejected;
- suppression attempts rejected;
- `false_positive` without evidence reference rejected;
- raw-text-bearing promotable values rejected.

### 14.4 Exact equality

- identical bytes pass;
- case differences fail;
- Unicode normalization differences fail under exact comparison;
- trailing or repeated whitespace differences fail under exact comparison.

### 14.5 Normalization

- NFKC behaviour;
- case folding;
- Unicode whitespace collapse;
- leading/trailing whitespace removal;
- Arabic and Latin input stability;
- punctuation retained for normalization but treated as token boundaries;
- no locale dependence.

### 14.6 Tokenization and Jaccard

- maximal Unicode alphanumeric runs;
- punctuation boundaries;
- token-set rather than multiset behaviour;
- exact `0.90` threshold pass via `100 * i >= 90 * u`;
- immediately below `0.90` fail;
- exact `0.95` threshold pass via `100 * i >= 95 * u`;
- immediately below `0.95` fail;
- both-empty normalized questions;
- exactly-one-empty token set;
- no fabricated score.

### 14.7 Findings

- deterministic ID across reruns;
- caller-order independence;
- lexicographic ID/source/partition normalization;
- `score_representation` included in the identity document;
- exact methods bind `none`;
- non-evaluable comparisons bind `not_evaluable`;
- one-bit semantic changes alter the finding ID;
- report findings sorted by ID;
- raw text absent from canonical document and bytes.

### 14.8 Classification and report

- unresolved sets `leaked=true`;
- confirmed leakage sets `leaked=true`;
- all supported false positives set `leaked=false`;
- empty report behaviour is explicit;
- finding count exact;
- suppression impossible;
- leakage-positive synthetic report cannot be vacuous.

### 14.9 Determinism

- repeated canonical bytes identical;
- no timestamps;
- no paths;
- no environment metadata;
- no host/user metadata;
- no mutable caller-owned collections retained;
- no side effects.

## 15. Path scope for the future implementation

```text
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py
```

Exactly two paths. If implementation proves impossible within them, stop and
return for a new founder authorization. Do not expand the allowlist.
