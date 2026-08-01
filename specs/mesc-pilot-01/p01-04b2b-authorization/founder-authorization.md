# P01-04B2B Implementation Authorization — Founder Authorization

```text
Status:
FOUNDER AUTHORIZATION RECORDED

FD-B2B-1 through FD-B2B-10:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
RECORDED BUT INACTIVE

P01-04B2B implementation:
NOT AUTHORIZED TO BEGIN
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-01

Required canonical baseline:
`bfc4254b6a028ea7ec5969b505d73e7d66751272`

This document is controlling for this package. Prior governance history is
adopted at [`../p01-04b2/`](../p01-04b2/), [`../p01-04b2a/`](../p01-04b2a/) and
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/) and is not restated.

---

## 0. Subordination

`FD-B2B-1` through `FD-B2B-10` are subordinate to:

```text
P01-04A D1 through D10
FD-B2-1 through FD-B2-8
FD-B2A-1 through FD-B2A-8
the accepted P01-04B2A implementation
```

They **amend none of those authorities**. On any conflict, the senior authority
controls and this package yields. In particular, the accepted B2A canonical
value domain and serializer are binding: this package conforms to them and does
not extend them.

## FD-B2B-1 — Private module boundary

```text
B2B implementation is authorized only as a private Python module.

Authorized future module:
src/medscale/mesc/_leakage_v1.py

No public export is authorized.

No change to:
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
```

`SourceDocumentGroupedSplitter.assign()` must remain unconditionally
fail-closed.

## FD-B2B-2 — Strict input domain

All B2B primitives:

- operate only on explicit in-memory primitive values;
- require exact built-in value types;
- reject type subclasses where exact primitive identity is required;
- perform no implicit coercion;
- perform no registry lookup;
- perform no filesystem, network, environment, clock, locale, or process access.

No primitive accepts:

- arbitrary records;
- dataset rows;
- paths;
- file handles;
- repository references;
- evidence-root references;
- P01-03G objects.

## FD-B2B-3 — Exact equality semantics

Pure pairwise primitives with these semantics are authorized:

```text
exact_example_identity:
byte equality of canonical example_id UTF-8 bytes

exact_source_document_identity:
byte equality of canonical source_document_id UTF-8 bytes

exact_question_equality:
byte equality of question UTF-8 bytes

exact_context_equality:
byte equality of context UTF-8 bytes
```

No normalization is permitted in an exact-equality primitive. Exact equality and
normalized or approximate equality remain separate methods and separate finding
types.

`exact_context_equality` is the exact-byte primitive corresponding to the
`context_equality` deliverable named in the adopted plan and to the `FD-B2-6`
rule "Exact context: byte equality of UTF-8 context bytes". The naming is
clarified, not changed.

## FD-B2B-4 — Question normalization and tokenization

The exact normalization pipeline is:

1. Unicode NFKC;
2. Unicode case folding;
3. collapse each run of Unicode whitespace to one ASCII space;
4. remove leading and trailing whitespace.

Tokenization is:

- maximal consecutive Unicode alphanumeric runs;
- punctuation and whitespace are boundaries;
- empty tokens are discarded;
- tokens form a set, not a multiset.

No locale-specific normalization is permitted. No language-specific stemming,
lemmatization, stop-word removal, transliteration, or semantic embedding is
authorized.

## FD-B2B-5 — Jaccard, score representation, and empty-input semantics

Exact set Jaccard is authorized:

```text
intersection_size / union_size
```

### Authoritative canonical score representation

Exactly one authoritative representation is defined:

```text
score_representation
```

Allowed values are exactly:

```text
none

not_evaluable

jaccard:<reduced_intersection>/<reduced_union>
```

Rules:

- `none` is used for exact methods with no approximate score.
- `not_evaluable` is used when no valid Jaccard score exists.
- A valid Jaccard score uses a reduced rational pair.
- Numerator and denominator are base-10 ASCII integers with no sign and no
  leading zeros, except the single digit `0`.
- The denominator is strictly positive.
- `0 <= numerator <= denominator`.
- The fraction is reduced by the greatest common divisor.
- A zero Jaccard value is represented as `jaccard:0/1`.
- A full match is `jaccard:1/1`.

Worked example:

```text
intersection = 6
union = 9

score_representation:
jaccard:2/3
```

### Runtime float is derived and non-authoritative

The adopted in-memory compatibility contract is preserved:

```text
LeakageFinding.score:
finite float or null
```

That field is:

```text
runtime-only
derived
non-authoritative for canonical identity
excluded from canonical documents
excluded from canonical bytes
excluded from fingerprints and finding-ID payload bytes
```

A binary float must never be passed into the accepted B2A canonical serializer.
The accepted serializer's canonical value domain is
`None | bool | int | str | sequence | string-keyed mapping`; a float raises
`FloatingPointValueProhibitedError` with the stable code
`floating_point_value_prohibited`.

```text
The exact score representation is authoritative in both the canonical finding
document and the deterministic finding-ID payload. A derived finite runtime
float may additionally exist in memory but is never canonicalized or hashed.
```

The runtime float, when present, is derived from the integer intersection and
union counts for caller convenience only. It must not influence threshold
passage, canonical bytes, equality, ordering, finding identity, report identity,
or evidence identity.

### Canonical document rule

Every promotable finding canonical document must carry `score_representation`
with the authoritative string defined above, and must not carry a binary float.
The representation in the finding document must be **identical** to the
representation bound into the finding-ID payload.

### Thresholds and exact comparison

```text
Question near duplicate:
score >= 0.90

Approximate context overlap:
score >= 0.95
```

Threshold passage must use exact integer or rational comparison. Equivalent
exact rules are:

```text
Question threshold:
100 * intersection_size >= 90 * union_size

Context threshold:
100 * intersection_size >= 95 * union_size
```

Equality at the threshold is a match. No tolerance or epsilon adjustment. No
rounded or binary-floating-point value may determine threshold passage.

### Empty-input semantics

- if both normalized questions are empty, no score is fabricated and the
  condition maps to `empty_normalized_question`;
- if exactly one token set is empty, the comparison is `not_evaluable`;
- `not_evaluable` must never be silently reported as clean;
- approximate context findings remain unresolved until separately classified.

## FD-B2B-6 — Finding identity and ordering

Authorized finding schema identifier:

```text
mesc-pilot-01-leakage-finding/1
```

Authorized finding-ID format:

```text
mesc-pilot-01-leakage-finding/1:sha256:<64-lowercase-hex>
```

### Exact identity document

The finding-ID identity document is one canonical JSON object containing exactly
these six members and no others:

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

The member names above are **frozen**. Aliases, omitted members, additional
members, and alternate container shapes are prohibited. The semantic ordering
listed above is controlling even though the accepted canonical JSON serializer
deterministically orders object members. Arrays must already be in canonical
lexicographic order **before** serialization.

### Exact payload bytes

```text
FINDING_IDENTITY_BYTES =
the accepted B2A canonical single-object JSON byte serialization of the exact
identity document
```

This includes every accepted B2A rule, including accepted primitive-domain
validation, canonical object-member ordering, canonical UTF-8 encoding,
canonical escaping, exact single-object framing, the accepted terminal-line-feed
rule, and rejection of floats and other prohibited values.

Canonical JSON must not be duplicated or reimplemented. The existing accepted
B2A canonicalization helpers must be used.

### Exact finding-ID formula

```text
digest =
SHA-256(FINDING_IDENTITY_BYTES).hexdigest()

finding_id =
mesc-pilot-01-leakage-finding/1:sha256:<digest>
```

The lowercase hexadecimal digest must contain exactly 64 characters. No other
prefix, separator, concatenation, newline convention, JSON shape, or
serialization is valid.

### Identity validation

The implementation must regenerate the expected finding ID from the validated
semantic fields and compare it with the supplied value. A mismatch must fail
closed with the typed private invalid-finding-identifier error. Caller-supplied
IDs must never be trusted without deterministic regeneration.

### Ordering

Finding ordering in a report is ascending `finding_id`. No insertion order, hash
iteration order, runtime locale, or caller ordering may influence the result.

## FD-B2B-7 — Classification, suppression, and report semantics

Allowed classifications are exactly:

```text
unresolved
false_positive
confirmed_leakage
```

Rules:

- every finding must have one classification;
- `false_positive` requires a non-empty stable supporting-evidence reference;
- suppression is prohibited;
- `suppressed` must always be `false`;
- dropping, omitting, filtering, or suppressing a detected finding is
  fail-closed;
- `finding_count` must equal the exact number of findings;
- a leakage-positive synthetic fixture must not produce a vacuous empty report.

The aggregate `leaked` rule is clarified as:

```text
leaked = true
when at least one finding is unresolved or confirmed_leakage

leaked = false
only when no findings exist or every finding is a supported false_positive
```

This is an explicit **fail-closed implementation clarification** of the existing
aggregate-report wording. It does not alter the three allowed classifications
and it does not amend `FD-B2-6`.

## FD-B2B-8 — Raw-text and promotable-artifact boundary

Raw question, context, and answer text:

- may exist only as transient in-memory primitive inputs;
- must never be stored in a `LeakageFinding`;
- must never enter canonical bytes;
- must never enter logs, exceptions, repr output, reports, manifests,
  fingerprints, evidence references, or repository artifacts.

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

## FD-B2B-9 — Deterministic errors and side-effect prohibition

Typed private errors are authorized for:

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

Requirements:

- stable machine-readable error code;
- deterministic validation order;
- no raw input text in error messages;
- no path, username, hostname, environment, timestamp, or runtime metadata;
- no file, network, subprocess, logging, telemetry, cache, or global-state side
  effect.

**No new dependency is authorized.**

## FD-B2B-10 — Activation and sequencing

The B2B implementation authorization becomes active only after all five
conditions are satisfied:

1. genuinely independent clean-room exact-head review of this authorization
   package;
2. separate founder Ready decision;
3. separate founder merge decision;
4. merge into canonical `main`;
5. mechanical post-merge verification.

```text
No subset activates P01-04B2B implementation authority.
```

### Before activation

```text
FD-B2B-1 through FD-B2B-10:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
RECORDED BUT INACTIVE

P01-04B2B implementation:
NOT AUTHORIZED TO BEGIN
```

### After successful canonical adoption

```text
FD-B2B-1 through FD-B2B-10:
ADOPTED ON CANONICAL MAIN

P01-04B2B implementation authority:
ACTIVE

P01-04B2B implementation:
AUTHORIZED — NOT STARTED
```

## Exact future implementation allowlist

After canonical adoption, a separate implementation task may modify exactly:

```text
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py
```

No other path is authorized. In particular, changes are **not** authorized to:

```text
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/cli/**
tests/test_mesc_split.py
tests/test_mesc_split_v1.py
tests/test_mesc_canonical_json_v1.py
tests/test_mesc_split_artifacts_v1.py
.github/**
pyproject.toml
uv.lock
```

If implementation proves impossible within this two-path allowlist, stop and
return for a new founder authorization. **Do not expand the allowlist during
implementation.**

## Continuing separation — B2C, B2D and execution

Even after this package is adopted:

```text
P01-04B2B implementation:     AUTHORIZED — NOT STARTED
P01-04B2B acceptance:         NOT ACHIEVED
P01-04B2C:                    NOT AUTHORIZED
P01-04B2D:                    NOT AUTHORIZED
P01-04B as a whole:           INCOMPLETE / NOT ACCEPTED
P01-04C through P01-04G:      NOT AUTHORIZED
Real Pilot-01 split:          NOT AUTHORIZED
P01-03G / real dataset:       NOT AUTHORIZED
Real leakage-audit execution: NOT AUTHORIZED
Fixture facade:               NOT AUTHORIZED
CLI:                          NOT AUTHORIZED
Filesystem publication:       NOT AUTHORIZED
B0/B1 execution:              NOT AUTHORIZED
Model access:                 NOT AUTHORIZED
Inference · Retrieval:        NOT AUTHORIZED
Metrics / benchmarks:         NOT AUTHORIZED
Training / fine-tuning:       NOT AUTHORIZED
Publication · Clinical use:   NOT AUTHORIZED
```

Completing the B2B implementation will not accept B2B. Acceptance requires an
independent exact-head implementation review, a separate founder Ready decision,
a separate merge decision, canonical merge, mechanical verification, and then a
later separate B2B implementation-acceptance decision. **B2C remains blocked
until B2B is accepted, not merely implemented.**

`FD-B2B-1` through `FD-B2B-10` do not authorize, before or after adoption: any
B2B code or test file written before adoption; any path outside the two-path
allowlist; a public export; a CLI; a new dependency; record-pair enumeration or
dataset, registry or collection scanning; leakage-audit orchestration; a fixture
or split facade; filesystem publication; real execution; B2C or B2D; P01-04B
acceptance; the real Pilot-01 split; B0 or B1; model or real-dataset access;
inference, retrieval, metrics, benchmark execution, training or fine-tuning;
publication; clinical use; a second commit on this package; amendment, rebase,
squash, reset, cherry-pick or force-push; marking this package's pull request
Ready; merging it; auto-merge; or deleting any branch.
