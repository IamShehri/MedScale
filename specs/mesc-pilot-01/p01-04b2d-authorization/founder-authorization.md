# P01-04B2D Authorization — Founder Authorization

```text
Status:
FOUNDER AUTHORIZATION ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

Decision:
AUTHORIZE ONE BOUNDED P01-04B2D INTEGRATED SYNTHETIC QUALIFICATION
IMPLEMENTATION SUBJECT TO THE ACTIVATION GATE

FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
RECORDED BUT INACTIVE

P01-04B2D implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D qualification:
NOT EXECUTED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED

Real split generation, real or canonical leakage-audit execution,
real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Required canonical baseline:
`a0c623aa08354a343fccc1d066a7a6acaa5b8576`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`implementation-contract.md`](implementation-contract.md) or
[`acceptance.md`](acceptance.md), this document controls.

**No B2D fixture was constructed and no B2D qualification was executed while
drafting this authorization.** No 1,000-row batch was instantiated, no
`FixtureSplitFacade` invocation occurred, and no B2D fixture digest, request
identifier, compatibility hash, authoritative fingerprint or finding identifier
was calculated. Every numeric value in this package is either a founder-frozen
design value or a value read from already-adopted governance text.

---

## 1. Prerequisite chain and entering state

```text
Canonical main:
a0c623aa08354a343fccc1d066a7a6acaa5b8576

P01-04B2A:
ACCEPTED

P01-04B2B:
ACCEPTED

P01-04B2C:
ACCEPTED

FD-B2C-ACT-1:
CANONICALLY RECORDED

FD-B2C-13:
ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
SPENT

P01-04B2D:
ELIGIBLE FOR A SEPARATE AUTHORIZATION DECISION — NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

Eligibility is not authority. B2C acceptance did not automatically authorize
B2D. This package is that separate authorization decision, and it too activates
nothing until its own five adoption conditions pass.

Governing authority not restated here, and not modified by this package:

```text
D1 through D10
  specs/mesc-pilot-01/p01-04/decision-record.md

FD-B2-1 through FD-B2-8
  specs/mesc-pilot-01/p01-04b2/founder-ratification.md

accepted B2A, B2B and B2C behaviour
  specs/mesc-pilot-01/p01-04b2a-acceptance/
  specs/mesc-pilot-01/p01-04b2b-acceptance/
  specs/mesc-pilot-01/p01-04b2c-authorization/
  specs/mesc-pilot-01/p01-04b2c-acceptance/
```

## 2. Conflict resolution — FD-B2-7 preserved without amendment

An earlier drafting attempt proposed B2D fixture contracts that contradicted
founder-ratified FD-B2-7. `specs/mesc-pilot-01/p01-04b2/decision-record.md`
states that **FD-B2-7 controls on conflict**. The build was stopped rather than
silently reconciled.

```text
Selected resolution:
PATH 1 — CONFORM P01-04B2D TO RATIFIED FD-B2-7

FD-B2-7 amended:
NO

FD-B2-7 superseded, narrowed or overridden:
NO

The conflicting fixture requirements:
WITHDRAWN
```

The four recorded conflicts and their resolutions:

```text
Conflict A — exact-reference-1000-v1 group structure
Withdrawn proposal: 1000 groups, every group size exactly 1.
Ratified FD-B2-7 Fixture A: multi-example groups mandatory; sizes must
include 1, 2, 3, 5, 8, 13; each partition contains at least one
multi-example group.
RESOLVED: FD-B2D-4 conforms to FD-B2-7. 89 groups spanning all six sizes.

Conflict B — constraint-stress-1000-v1 feasibility
Withdrawn proposal: exact totals, exact matrix, zero deviation.
Ratified FD-B2-7 Fixture B: group sizes intentionally make exact targets
infeasible; acceptance is deterministic globally minimum deviation with
explicit recorded deviation.
RESOLVED: FD-B2D-5 conforms to FD-B2-7. 500 groups of size 2 make the
ratified matrix provably infeasible.

Conflict C — leakage-positive-v1 classifications
Withdrawn proposal: all five findings unresolved.
Ratified FD-B2-7 Fixture C: at least one finding classified as a supported
synthetic false_positive; at least one remains unresolved.
RESOLVED: FD-B2D-6 conforms to FD-B2-7. Nine findings, at least three
supported false positives, six unresolved.

Conflict D — leakage-positive-v1 case coverage
Withdrawn proposal: five scenarios omitting exact example identity, exact
source-document identity and exact context.
Ratified FD-B2-7 Fixture C item 2: deterministic cases for all nine listed
comparison behaviours.
RESOLVED: FD-B2D-6 covers all nine, using same-partition synthetic controls
that qualify primitive and classification behaviour without claiming
cross-partition duplicate membership.
```

## 3. FD-B2D-1 — Qualification-only surface and exact allowlist

```text
FD-B2D-1 — QUALIFICATION-ONLY SURFACE AND EXACT ALLOWLIST
```

The authorized increment is **test-only**. It adds no production code.

```text
Future implementation branch:
test/mesc-p01-04b2d-qualification

Future implementation subject:
test(mesc): qualify P01-04B2D synthetic suite
```

The future implementation may add exactly these three paths and no others:

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml
```

No modification to any existing path is authorized. In particular, these must
remain byte-identical:

```text
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
src/medscale/mesc/_fixture_split_v1.py
src/medscale/mesc/__init__.py

tests/test_mesc_split.py
tests/test_mesc_split_v1.py
tests/test_mesc_canonical_json_v1.py
tests/test_mesc_split_artifacts_v1.py
tests/test_mesc_leakage_v1.py
tests/test_mesc_fixture_split_v1.py

pyproject.toml
uv.lock

.github/workflows/ci.yml
.github/workflows/codeql.yml
.github/workflows/mesc-b2a-portability.yml
.github/workflows/optional-extras.yml
.github/workflows/release.yml
```

```text
Production code authorized:      NONE
New dependency authorized:       NONE
Public export authorized:        NONE
CLI authorized:                  NONE
Entry point authorized:          NONE
Existing workflow modification:  NONE
```

## 4. FD-B2D-2 — Exact fixture set

```text
FD-B2D-2 — EXACT FIXTURE SET
```

Qualification uses exactly these three named fixtures:

```text
exact-reference-1000-v1
constraint-stress-1000-v1
leakage-positive-v1
```

```text
No generic fixture-1000-v1 alias is permitted.
No fourth qualification fixture is permitted.
No document may reduce the suite to one generic 1,000-row fixture.
```

Every fixture contains exactly:

```text
1,000 OrderedExampleRow values
1,000 SourceLabelRow values
```

Derived negative mutations used inside individual tests are **not** separate
qualification fixtures. They must never receive an approved fixture namespace,
a fixture identity digest, or qualification status.

For every fixture:

```text
fixture_schema_version:
1

fixture_namespace:
mesc-fixture/p01-04b2/1/<fixture-id>

fixture_only:
true

non_evidence:
true

seed:
mesc-pilot-01-split-v1

policy_id:
mesc-pilot-01-split-policy/1

transformation_version:
mesc-pilot-01-b2d-transform/1
```

## 5. FD-B2D-3 — Shared synthetic identity contract

```text
FD-B2D-3 — SHARED SYNTHETIC IDENTITY CONTRACT
```

Frozen shared values:

```text
dataset_id:
mesc-pilot-01-synthetic-qualification

dataset_revision:
p01-04b2d-v1

row ordinals:
0 through 999 inclusive

partition totals:
train       700
validation  150
test        150

label totals:
yes    552
no     338
maybe  110
```

Ratified target matrix:

```text
              train  validation  test  total
yes             386          83    83    552
no              237          50    51    338
maybe            77          17    16    110
total           700         150   150   1000
```

Original-example identifiers follow exactly:

```text
mesc-b2d-<fixture-id>-example-<four-digit-row-ordinal>
```

Source-document identifiers follow the fixture-specific grouping contract in
FD-B2D-4, FD-B2D-5 and FD-B2D-6.

`source_record_hash` is the lowercase SHA-256 of the exact UTF-8 ASCII domain
string:

```text
mesc-pilot-01-b2d-source-record-v1|<fixture-id>|<original-example-id>|<source-document-id>|<decision>
```

The vertical bars are literal ASCII `|` bytes. No newline is included. No
trailing separator is appended.

Fixture construction must be pure, deterministic and in memory, with no:

```text
randomness      clock         environment    filesystem
network         subprocess    locale         timezone
database        cache         logging        telemetry
temporary file
```

### 5.1 Synthetic-identity proof

Each fixture carries:

```text
mesc-synthetic-batch/1:sha256:<64-lowercase-hex>
```

The digest is computed with the accepted B2A canonical serializer over an exact
generator-specification document containing exactly these members:

```text
schema
fixture_id
fixture_schema_version
generator_version
dataset_id
dataset_revision
configuration
transformation_version
policy_id
row_count
partition_totals
label_totals
grouping_contract
leakage_scenario_contract
```

Fixed values:

```text
schema:
mesc-pilot-01-b2d-generator-spec/1

generator_version:
mesc-pilot-01-b2d-generator/1

row_count:
1000
```

The proof binds the **generator specification**, never generated B2C result
bytes. It must not bind:

```text
fixture_sha256      request_id        split_hash
split_fingerprint   runtime           operating system
Python version      timestamp         path
workflow run ID
```

This is the anti-circularity guarantee: the proof is computable before the
facade runs and cannot be a restatement of the facade's own output.

## 6. FD-B2D-4 — `exact-reference-1000-v1` (conforms to FD-B2-7 Fixture A)

```text
FD-B2D-4 — EXACT-REFERENCE FIXTURE
```

This is the **successful exact-reference fixture**. It satisfies every
canonical FD-B2-7 Fixture A requirement.

```text
rows:
1000

labels:
yes    552
no     338
maybe  110

partitions:
train       700
validation  150
test        150

groups:
89

multi-example groups:
MANDATORY

required group sizes present:
1, 2, 3, 5, 8, 13
```

Required exact label matrix:

```text
              train  validation  test  total
yes             386          83    83    552
no              237          50    51    338
maybe            77          17    16    110
total           700         150   150   1000
```

### 6.1 Exact group-size vectors

Notation: `13x29` means twenty-nine groups of size 13.

```text
yes / train:        13x29, 8, 1        sum 386    31 groups
yes / validation:   13x6, 5            sum  83     7 groups
yes / test:         13x6, 5            sum  83     7 groups
yes total:                             sum 552    45 groups

no / train:         13x18, 2, 1        sum 237    20 groups
no / validation:    13x3, 8, 3         sum  50     5 groups
no / test:          13x3, 8, 3, 1      sum  51     6 groups
no total:                              sum 338    31 groups

maybe / train:      13x5, 8, 3, 1      sum  77     8 groups
maybe / validation: 13, 3, 1           sum  17     3 groups
maybe / test:       13, 3              sum  16     2 groups
maybe total:                           sum 110    13 groups

grand total:                           sum 1000   89 groups
```

Required group counts:

```text
yes:     45
no:      31
maybe:   13
total:   89
```

Every partition contains multiple multi-example groups. Every required size
`1, 2, 3, 5, 8, 13` occurs at least once. No group crosses a partition. No
group crosses a decision stratum.

### 6.2 Independent fixture construction

For each decision, in the order `yes`, `no`, `maybe`:

```text
1. generate exactly the required number of candidate source-document
   identifiers for that decision

2. compute each candidate's D6 partition key independently from the exact
   ratified canonical payload

3. use the no-terminal-LF D6 serialization contract for this ranking oracle

4. sort candidates by:
     digest ascending (lowercase hexadecimal)
     source-document identifier ascending
     defensive candidate ordinal ascending

5. concatenate that decision's train, validation and test group-size vectors
   in that order

6. bind the ordered group-size vector positionally to the ordered candidate
   identifiers

7. generate consecutive row ordinals across all groups
```

The D6 payload is exactly:

```json
{
  "algorithm_version": "mesc-pilot-01-split-algorithm/1",
  "seed": "mesc-pilot-01-split-v1",
  "stratum": "<yes|no|maybe>",
  "source_document_id": "<canonical source_document_id>"
}
```

serialized with recursively sorted keys, UTF-8, `ensure_ascii=False`,
`allow_nan=False`, separators `(",", ":")`, no indentation, no BOM and
**no terminal newline**.

While constructing the expected grouping plan the fixture generator must not
call:

```text
rank_groups
allocate_indivisible_groups
FixtureSplitFacade
```

The facade under test must then independently reproduce:

```text
700 / 150 / 150 partition totals
the exact ratified label matrix
89 groups
all six required group sizes
zero group crossing
zero exclusions
byte-identical outputs across all six workflow cells
```

## 7. FD-B2D-5 — `constraint-stress-1000-v1` (conforms to FD-B2-7 Fixture B)

```text
FD-B2D-5 — CONSTRAINT-STRESS FIXTURE
```

This fixture **must intentionally make the exact ratified label matrix
infeasible** under indivisible groups. It must not be redesigned to achieve
zero deviation.

```text
rows:
1000

labels:
yes    552
no     338
maybe  110

nominal partitions:
train       700
validation  150
test        150

groups:
500

group size:
exactly 2 for every group

homogeneous by decision:
every group
```

Group counts:

```text
yes:     276 groups
no:      169 groups
maybe:    55 groups
total:   500 groups
```

### 7.1 Mechanical infeasibility

Because every group has size 2 and no group may cross a partition or a decision
stratum, **every realized label-by-partition cell must be an even integer**.

The ratified target matrix contains exactly **six** odd-valued cells, comprising
**five** distinct odd values because `83` occurs twice:

```text
yes / validation    = 83
yes / test          = 83
no / train          = 237
no / test           = 51
maybe / train       = 77
maybe / validation  = 17
```

```text
Every constraint-stress group has size 2.

Therefore every realized label-by-partition cell must be even.

The six odd target cells make the exact ratified matrix infeasible.
```

The count is six cells, not five. Five is the number of distinct odd values.
No document may state or imply that the ratified matrix has five odd cells.

The qualification oracle must prove this mechanically rather than assert it.

### 7.2 Global minimum-deviation oracle

The independent qualification oracle must completely derive every matrix
satisfying:

```text
every label row total exactly
every partition column total exactly
every cell a non-negative even integer
```

Objective:

```text
minimize the sum of squared deviations from the ratified 3x3 target matrix
```

Tie-break:

```text
lexicographically smallest vector
label order:      yes, no, maybe
partition order:  train, validation, test
```

Minimum squared-deviation score:

```text
6
```

Exactly **two** feasible matrices attain score 6. Both are founder-frozen here so
the tie-break is provably examined rather than asserted.

Founder-frozen selected global optimum:

```text
Matrix A — lexicographic winner

              train  validation  test  total
yes             386          82    84    552
no              238          50    50    338
maybe            76          18    16    110
total           700         150   150   1000
```

Flattened vector:

```text
386,82,84,238,50,50,76,18,16
```

Deviation of Matrix A from the ratified matrix:

```text
yes:     0, -1, +1
no:     +1,  0, -1
maybe:  -1, +1,  0
```

Founder-frozen score-6 runner-up:

```text
Matrix B — score-6 runner-up

              train  validation  test  total
yes             386          84    82    552
no              236          50    52    338
maybe            78          16    16    110
total           700         150   150   1000
```

Flattened vector:

```text
386,84,82,236,50,52,78,16,16
```

Deviation of Matrix B from the ratified matrix:

```text
yes:     0, +1, -1
no:      -1,  0, +1
maybe:  +1, -1,  0
```

Controlling tie-break statement:

```text
Exactly two feasible matrices have minimum squared-deviation score 6.

Under the controlling lexicographic order:

label order:
yes, no, maybe

partition order:
train, validation, test

Matrix A is smaller than Matrix B and is therefore the uniquely selected
qualification oracle result.
```

The first differing position is `validation` under `yes`: Matrix A holds `82`
and Matrix B holds `84`, so Matrix A is strictly smaller.

It is not sufficient to state that a second score-6 matrix exists. Both vectors
are frozen above, and the implementation must reproduce both.

The implementation test must independently enumerate or prove the complete
feasible lattice and assert:

```text
minimum score = 6
number of score-6 matrices = 2
selected matrix = Matrix A
other score-6 matrix = Matrix B
```

The implementation test must additionally prove:

```text
the exact ratified matrix is infeasible
the lexicographically selected optimum equals the frozen Matrix A
zero source-document group overlap
partition totals remain 700 / 150 / 150
explicit deviation is recorded
```

### 7.3 Expected behaviour of the currently accepted implementation

The accepted B1/B2C implementation has **exact-target allocation only**. It does
not implement the required global minimum-deviation fallback:
`allocate_indivisible_groups` raises `SplitAllocationError` when a ranked group
would cross a target boundary rather than producing a minimum-deviation
allocation.

Therefore the current facade is **expected to fail closed** with that accepted
typed error when this fixture reaches the infeasible boundary. The qualification
test must assert that exact typed failure.

This is **not** a successful P01-04B criterion.

```text
B2D qualification harness:
PASS — EXPECTED BLOCKING CAPABILITY GAP DETECTED

constraint-stress requirement:
UNSATISFIED BY CURRENT ACCEPTED IMPLEMENTATION

P01-04B acceptance eligibility:
FALSE

P01-04B acceptance recommendation:
CHANGES REQUIRED
```

A passing test means the harness detected and classified the gap correctly. It
does **not** mean the production behaviour satisfies FD-B2-7.

```text
No production correction is authorized in B2D.

A separate founder correction authorization is required after B2D if this gap
remains confirmed.
```

## 8. FD-B2D-6 — `leakage-positive-v1` (conforms to FD-B2-7 Fixture C)

```text
FD-B2D-6 — LEAKAGE-POSITIVE FIXTURE
```

Base structure:

```text
rows:
1000

labels:
yes    552
no     338
maybe  110

partitions:
train       700
validation  150
test        150

source-document groups:
999

group structure:
- exactly one homogeneous two-example source-document group
- exactly 998 singleton source-document groups
- no other multi-example group

two-example group:
- both examples have the same decision
- both examples remain in one actual partition
- the group must never straddle a partition boundary
```

The `999` group count, the single homogeneous two-example group and the 998
singleton groups are **founder-frozen requirements of this fixture**. They are
not an inference, a derivation or a reviewer note. Any document, test or report
that states a different leakage-positive group count contradicts this
authorization.

This clarification is subordinate to and consistent with FD-B2-7. **It does not
amend FD-B2-7.** FD-B2-7 Fixture C requires deterministic cases for exact
source-document identity; a homogeneous multi-example source-document group is
the structure that makes that case expressible without claiming cross-partition
overlap, and the remaining 998 singletons keep the ratified label matrix
feasible.

The two-example group must never straddle a partition boundary. Its
source-document identifier is selected deterministically as the lowest-indexed
candidate in a documented candidate sequence whose independently computed D6
rank places the group strictly inside a partition run, and that identifier is
then frozen as a literal constant.

### 8.1 Required deterministic scenarios

The fixture must cover every canonical FD-B2-7 Fixture C case:

```text
1. exact example identity
2. exact source-document identity
3. exact question equality
4. normalized question equality
5. question Jaccard exactly at threshold
6. question Jaccard above threshold
7. exact context equality
8. approximate context overlap
9. both-empty normalized questions
```

The final synthetic audit contains exactly **9 predefined findings**.

### 8.2 Scenario contracts

**Scenario 1 — exact example identity**

One valid fixture example used as a deterministic self-identity control.

```text
finding_type:         exact_example
classification:       false_positive
partitions:           the one actual partition of that example
shared_surface:       example_id
score_representation: none
evidence_reference:
mesc-pilot-01-b2d-leakage-scenario/1/exact-example-self-control
```

**Scenario 2 — exact source-document identity**

One deterministic two-example, same-decision source-document group. Both
examples remain in the same actual partition.

```text
finding_type:         source_document
classification:       false_positive
partitions:           the one actual partition of the group
shared_surface:       source_document_id
score_representation: none
evidence_reference:
mesc-pilot-01-b2d-leakage-scenario/1/expected-same-group-source-document
```

**Scenario 3 — exact question equality**

Both raw surfaces exactly:

```text
does alpha therapy reduce beta outcome?
```

```text
finding_type:         exact_question
score_representation: none
shared_surface:       question_bytes
classification:       unresolved
```

**Scenario 4 — normalized question equality**

The left surface is specified by exact byte composition rather than as a literal
fenced line, because its leading and trailing ASCII spaces are significant and
invisible whitespace must not depend on how a document is copied or trimmed.

```text
left surface = concatenation, in order, of:

  U+0020 SPACE
  U+0020 SPACE
  "Does"
  U+00A0 NO-BREAK SPACE
  "ALPHA"
  U+0020 SPACE
  "Therapy reduce beta outcome?"
  U+0020 SPACE
  U+0020 SPACE
```

The left surface therefore carries exactly two leading ASCII spaces, one
U+00A0 NO-BREAK SPACE between `Does` and `ALPHA`, and exactly two trailing ASCII
spaces. It contains no tab and no line feed.

Right:

```text
does alpha therapy reduce beta outcome?
```

```text
finding_type:         normalized_question
score_representation: none
shared_surface:       normalized_question
classification:       unresolved
```

**Scenario 5 — question Jaccard exactly at threshold**

```text
left tokens:
alpha beta gamma delta epsilon zeta eta theta iota kappa

right tokens:
alpha beta gamma delta epsilon zeta eta theta iota
```

```text
finding_type:         near_duplicate_question
intersection:         9
union:                10
score_representation: jaccard:9/10
threshold:            passed exactly at 0.90
shared_surface:       question_token_set
classification:       unresolved
```

**Scenario 6 — question Jaccard above threshold**

```text
left tokens:
alpha beta gamma delta epsilon zeta eta theta iota kappa lambda

right tokens:
alpha beta gamma delta epsilon zeta eta theta iota kappa
```

```text
finding_type:         near_duplicate_question
intersection:         10
union:                11
score_representation: jaccard:10/11
threshold:            passed above 0.90
shared_surface:       question_token_set
classification:       unresolved
```

**Scenario 7 — exact context equality**

Identical deterministic context surfaces on both sides.

```text
finding_type:         context_overlap
score_representation: none
shared_surface:       context_bytes
classification:       unresolved
```

**Scenario 8 — approximate context overlap**

Left contains exactly these twenty tokens:

```text
ctx01 ctx02 ctx03 ctx04 ctx05 ctx06 ctx07 ctx08 ctx09 ctx10
ctx11 ctx12 ctx13 ctx14 ctx15 ctx16 ctx17 ctx18 ctx19 ctx20
```

Right contains exactly the first nineteen.

```text
finding_type:         context_overlap
intersection:         19
union:                20
score_representation: jaccard:19/20
threshold:            passed exactly at 0.95
shared_surface:       context_token_set
classification:       unresolved
```

**Scenario 9 — both-empty normalized questions**

```text
left:   ASCII space + horizontal tab + line feed
right:  U+2003 EM SPACE + U+00A0 NO-BREAK SPACE
```

```text
finding_type:         empty_normalized_question
score_representation: not_evaluable
shared_surface:       empty_normalized_question
classification:       false_positive
evidence_reference:
mesc-pilot-01-b2d-leakage-scenario/1/whitespace-only-control
```

### 8.3 Detection methods

The exact detection-method tuple, in exactly this caller order:

```text
exact_context_equality
exact_example_identity
exact_question_equality
exact_source_document_identity
normalize_question
normalized_question_equality
token_set_jaccard
tokenize
```

### 8.4 Final audit classification

```text
finding_count:            9
leaked:                   true
suppressed findings:      0
supported false positives: at least 3
unresolved findings:      at least 1
```

Under the frozen scenario set: scenarios 1, 2 and 9 are `false_positive`;
scenarios 3 through 8 are `unresolved`. `leaked` is `true` because at least one
finding is `unresolved`.

Every false positive must carry a stable supporting-evidence reference. All
unresolved findings may carry stable synthetic scenario references but must not
be silently reclassified or suppressed. `suppressed` must always be `false`.

Evidence-reference format:

```text
mesc-pilot-01-b2d-leakage-scenario/1/<scenario-slug>
```

### 8.5 Raw-text exclusion

No raw synthetic question or context text may appear in:

```text
finding canonical documents
finding IDs
audit-report bytes
fixture result bytes
fingerprint payload
split-summary bytes
registries
```

Raw synthetic surfaces may exist only inside the non-promotable test helper.

### 8.6 Semantic boundary

The exact-example and source-document scenarios are **same-partition synthetic
controls**. They qualify:

```text
primitive behaviour
finding construction
canonical identity
classification
evidence-reference enforcement
```

They do **not** claim:

```text
cross-partition duplicate membership
cross-partition source-document overlap
real leakage
real dataset scanning
```

This distinction must be explicit in all four authorization documents.

## 9. FD-B2D-7 — Literal qualification vectors

```text
FD-B2D-7 — LITERAL QUALIFICATION VECTORS
```

The authorized implementation must freeze literal expected values for every
fixture. For each fixture, literal constants must include:

```text
synthetic_identity_proof
fixture_sha256
request_id
compatibility split_hash
authoritative split_fingerprint

group-registry SHA-256 and byte size
example-registry SHA-256 and byte size
excluded-ledger SHA-256 and byte size
split-summary identity-core SHA-256 and byte size
final split-summary SHA-256 and byte size
leakage-audit-report SHA-256 and byte size

record count
group count
partition counts
label matrix
excluded count
finding count
leaked
ordered finding IDs
```

For `constraint-stress-1000-v1`, the frozen expectation is the typed
fail-closed outcome of FD-B2D-5 §7.3 together with the infeasibility proof and
the frozen minimum-deviation matrix — not a successful result document.

For `leakage-positive-v1`, literal constants must include:

```text
all 9 ordered finding IDs
all 9 classifications
all 9 evidence-reference outcomes
finding_count = 9
leaked = true
```

```text
No B2D output value may be calculated during this authorization-package task.
```

The implementation commit may produce these literal constants only after its
implementation authority is active. The future implementation report must label
them:

```text
SYNTHETIC QUALIFICATION VECTORS
NOT REAL DATASET EVIDENCE
NOT A CANONICAL SPLIT
NOT A REAL LEAKAGE AUDIT
```

Literal expected output values must not be computed at test runtime from the
facade result under test.

## 10. FD-B2D-8 — Cross-platform qualification workflow

```text
FD-B2D-8 — CROSS-PLATFORM QUALIFICATION WORKFLOW
```

Exactly one new workflow is authorized:

```text
.github/workflows/mesc-p01-04b2d-qualification.yml

name:
MESC P01-04B2D Qualification
```

Triggers exactly:

```text
pull_request
push to main
```

Prohibited triggers:

```text
workflow_dispatch    schedule    repository_dispatch
issue trigger        release trigger
```

Permissions exactly:

```yaml
permissions:
  contents: read
```

```text
No write permission.   No secrets.          No artifact upload.
No cache publication.  No branch mutation.
```

Required matrix, with `fail-fast: false`:

```text
ubuntu-latest    Python 3.11
ubuntu-latest    Python 3.12
windows-latest   Python 3.11
windows-latest   Python 3.12
macos-latest     Python 3.11
macos-latest     Python 3.12
```

Each cell must:

```text
checkout exact head
install uv
install the matrix Python version
sync from uv.lock without updating it
run only tests/test_mesc_p01_04b2d_qualification_v1.py
```

The workflow must mirror the repository's accepted setup-action versions and
locked-sync conventions as observed at the canonical baseline.

Every cell compares against the same committed literal golden vectors. Success
in all six cells is the cross-runtime byte-identity evidence. **No OS-specific
expected value is permitted.**

Required path filters:

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml

src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
src/medscale/mesc/_fixture_split_v1.py

pyproject.toml
uv.lock
```

No existing workflow may be modified.

## 11. FD-B2D-9 — P01-04B acceptance-criteria mapping

```text
FD-B2D-9 — P01-04B ACCEPTANCE-CRITERIA MAPPING
```

The future qualification test must map **13 unique criteria** separately.

```text
The mapping contains:
- the ten P01-04B tooling-acceptance criteria; and
- three additional non-duplicative future-code criteria from
  p01-04b2/acceptance.md.
```

The ten P01-04B tooling-acceptance criteria:

```text
 1. SourceDocumentGroupedSplitter.assign remains unconditionally fail-closed
 2. FixtureSplitFacade exists as the separate fixture-only facade
 3. the qualification path is library-only and in-memory
 4. no B2 CLI exists
 5. the 64-hex split_fingerprint is authoritative
 6. the 16-hex split_hash is compatibility/display only
 7. leakage normalization follows FD-B2-6
 8. exactly the three named fixtures form the suite
 9. stable synthetic inputs produce byte-identical results
10. no real P01-03G membership is generated or disclosed
```

The three additional non-duplicative future-code criteria:

```text
11. atomic publication
12. write-path protections
13. date-free promotable artifacts
```

No document may claim that the ten tooling rows alone represent every canonical
criterion.

### 11.1 Criterion 11 — Atomic publication

```text
Status:
NOT APPLICABLE TO THE B2D FIXTURE-ONLY IN-MEMORY PATH

Reason:
FixtureSplitFacade performs no filesystem publication.
Atomic finalization, overwrite protection and concurrent-writer rejection
belong to a separately authorized artifact-publication component.

P01-04B consequence:
THIS CRITERION IS NOT SATISFIED FOR P01-04B OVERALL BY B2D.
NO PUBLICATION CAPABILITY OR ACCEPTANCE IS CREATED.
```

No B2D test may fabricate or simulate a publication capability.

### 11.2 Criterion 12 — Write-path protections

```text
Status:
NOT APPLICABLE TO THE B2D FIXTURE-ONLY IN-MEMORY PATH

Reason:
B2D accepts no filesystem input or output path and performs no write.

P01-04B consequence:
B2D CANNOT MARK WORKSPACE-ONLY TEMP FILES, NO-OVERWRITE RENAME OR
REPOSITORY/EVIDENCE-ROOT WRITE PROTECTION AS SATISFIED.
THEY REMAIN SEPARATELY AUTHORIZED PUBLICATION-COMPONENT WORK.
```

The absence of a write path is not equivalent to qualification of a future write
path.

### 11.3 Criterion 13 — Date-free promotable artifacts

```text
Status:
NOT APPLICABLE TO B2D OUTPUT PROMOTION;
DATE-FREE CANONICAL-BYTE INVARIANT TESTABLE

Reason:
Every B2D output is synthetic, fixture-only and non-promotable.
The B2D harness may and must verify that its canonical bytes contain no date,
timestamp, local path, hostname, username or runtime metadata.

P01-04B consequence:
A successful date-free byte-surface assertion does not make B2D outputs
promotable and does not satisfy repository promotion or publication acceptance.
```

The future test must assert that every canonical B2D byte surface is free of:

```text
date fields        timestamps        local paths
usernames          hostnames         runtime durations
workflow IDs       command logs      workspace locations
```

The mapping status remains bounded to B2D and must not claim real promotability.

### 11.4 Common mapping requirements

Each criterion must have:

```text
one dedicated test or test group
an exact assertion
a clear failure message
a link in the implementation report to the test symbol
```

Allowed result classes:

```text
SATISFIED
UNSATISFIED
BLOCKED
NOT APPLICABLE
```

The current expected result for the indivisible-group minimum-deviation
requirement is:

```text
UNSATISFIED
```

because the accepted implementation fails closed rather than producing the
canonical global minimum-deviation allocation.

Required statuses across the thirteen criteria:

```text
minimum-deviation capability:
UNSATISFIED

atomic publication:
NOT APPLICABLE TO B2D;
NOT SATISFIED FOR P01-04B OVERALL

write-path protections:
NOT APPLICABLE TO B2D;
NOT SATISFIED FOR P01-04B OVERALL

date-free promotable artifacts:
NOT APPLICABLE TO B2D OUTPUT PROMOTION;
DATE-FREE BYTE INVARIANT TESTABLE

P01-04B:
INCOMPLETE / NOT ACCEPTED
```

No aggregate acceptance algorithm may treat the suite as accepting P01-04B while
any criterion is `UNSATISFIED` or `BLOCKED`, or while any P01-04B-level criterion
remains unresolved. A `NOT APPLICABLE` disposition records that B2D cannot
qualify the criterion; it never converts to `SATISFIED` and never counts toward
P01-04B acceptance.

The B2D suite may be green when it correctly and deterministically establishes
this unsatisfied criterion.

```text
GREEN B2D QUALIFICATION CI
DOES NOT EQUAL P01-04B ACCEPTANCE.
```

Passing the tests does not accept P01-04B. It only makes B2D and P01-04B
eligible for a separate founder acceptance disposition.

The future implementation report must separate:

```text
qualification-harness correctness
fixture-specific observations
implementation capability gaps
P01-04B acceptance recommendation
```

It must not report P01-04B as accepted.

## 12. FD-B2D-10 — Oracle independence and anti-circularity

```text
FD-B2D-10 — ORACLE INDEPENDENCE AND ANTI-CIRCULARITY
```

The committed tests may invoke:

```text
FixtureSplitFacade.run
accepted B1 dataclasses and functions
accepted B2A canonical and fingerprint APIs
accepted B2B primitives and finding types
```

They must not use any private helper from `_fixture_split_v1.py` to construct
expected values. Expected registries, summaries, hashes, fingerprints and audit
identities must be literal constants.

The constraint fixture's D6 ranking oracle must be independently implemented
from the ratified canonical payload and must not call B1 ranking or allocation
functions while generating the fixture. The same independence applies to the
exact-reference fixture's grouping plan.

The leakage-positive scenario selection may be derived in untracked
implementation scratch after activation, but the committed helper must contain
literal selected identities.

No committed:

```text
golden regeneration command
--update-goldens option
automatic expected-value rewrite
self-approval routine
```

## 13. FD-B2D-11 — Fail-closed and golden-change policy

```text
FD-B2D-11 — FAIL-CLOSED AND GOLDEN-CHANGE POLICY
```

Any mismatch in:

```text
fixture identity        request identity        assignment membership
partition total         label count             group count
group boundary          canonical bytes         descriptor digest
descriptor byte size    compatibility hash      authoritative fingerprint
finding identity        finding count           audit leaked value
raw-text exclusion      cross-platform golden value
```

must fail the qualification.

```text
No tolerance is authorized.
No flaky retry is authorized.
No xfail is authorized.
No skip is authorized in the dedicated six-cell qualification workflow.
```

A literal golden change requires:

```text
a new founder decision
a new fixture or generator version when semantics change
a fresh independent review
```

A builder may not update a golden merely because the current implementation
emits a different value.

## 14. FD-B2D-12 — Evidence classification

```text
FD-B2D-12 — EVIDENCE CLASSIFICATION
```

All B2D inputs and outputs are:

```text
synthetic
fixture-only
non-evidence
non-clinical
non-promotable as a real split
non-promotable as a real leakage audit
```

The dedicated workflow proves only:

```text
deterministic synthetic qualification behaviour
cross-runtime equality against frozen literals
integration of accepted B1, B2A, B2B and B2C layers
```

It does not prove:

```text
the real dataset is leak-free    the real split is valid
P01-03G membership               scientific performance
model quality                    clinical safety
```

Workflow logs and status are external CI evidence only. No B2D result file is
promoted into the repository.

## 15. FD-B2D-13 — Prohibitions and downstream non-authority

```text
FD-B2D-13 — PROHIBITIONS AND DOWNSTREAM NON-AUTHORITY
```

This authorization does not permit:

```text
real P01-03G access               real source-records.jsonl access
real ordered registry access      real split generation
real partition membership         real leakage scanning
generic record-pair discovery     real leakage findings
dataset download                  model download
model access                      inference
retrieval                         metrics
benchmark execution               training
fine-tuning                       adapter creation
publication                       clinical use

P01-04C implementation or execution
P01-04D implementation or execution
P01-04E implementation or execution
P01-04F implementation or execution
P01-04G implementation or execution
P01-05 or later
```

It must not alter:

```text
D1 through D10
FD-B2-1 through FD-B2-8
accepted B2A behaviour
accepted B2B behaviour
accepted B2C behaviour
```

```text
No CLI.  No public API.  No filesystem-facing product capability.
```

## 16. FD-B2D-14 — Activation and one bounded implementation

```text
FD-B2D-14 — ACTIVATION AND ONE BOUNDED IMPLEMENTATION
```

Implementation authority activates only after all five conditions:

```text
1. genuinely independent clean-room exact-head review
   of this authorization package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset activates authority.
```

After activation:

```text
one branch
one implementation commit
exactly three authorized paths
one bounded implementation attempt
```

The authority is **spent** when that implementation commit is created. A
correction after the authorized commit requires a separate founder correction
decision. No silent second implementation commit is authorized.

## 17. Required post-implementation gates

Even after the future implementation is built:

```text
P01-04B2D is not accepted
P01-04B is not accepted
P01-04C is not authorized
```

Required later gates:

```text
1. independent clean-room exact-head implementation review
2. exact-head standard CI and CodeQL success
3. all six dedicated B2D workflow cells successful
4. separate Founder Ready decision
5. separate Founder Merge decision
6. canonical merge with expected-head lock
7. mechanical post-merge verification
8. separate founder qualification-and-P01-04B acceptance disposition
9. independent review and canonical adoption of that acceptance disposition
```

```text
No implementation merge automatically accepts B2D or P01-04B.
No B2D acceptance automatically authorizes P01-04C.
```

After a future B2D implementation is merged and mechanically verified:

```text
P01-04B2D harness:
may become eligible for separate acceptance

P01-04B:
remains NOT ACCEPTED while any criterion is UNSATISFIED
```

The separate founder qualification disposition may:

```text
accept the B2D qualification harness
reject or defer P01-04B acceptance
record the minimum-deviation capability gap
authorize nothing downstream
```

A separate correction authorization must precede any production implementation
of globally minimum-deviation grouped allocation.

## 18. Classification before canonical adoption

While this package is local, Draft, Ready-but-unmerged, or merged-but-not-
mechanically-verified:

```text
FD-B2D-1 through FD-B2D-14:
FOUNDER DECISIONS ISSUED — NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
RECORDED BUT INACTIVE

P01-04B2D implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D qualification:
NOT EXECUTED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

No retroactive authority may be claimed. P01-04B2D must not be described as
authorized merely because this local package exists.

## 19. Classification after canonical adoption

Only after all five adoption conditions of §16 pass:

```text
FD-B2D-1 through FD-B2D-14:
ADOPTED ON CANONICAL MAIN

P01-04B2D implementation authority:
ACTIVE FOR ONE BOUNDED IMPLEMENTATION ONLY

P01-04B2D implementation:
AUTHORIZED TO BEGIN
NOT YET IMPLEMENTED
NOT YET QUALIFIED
NOT ACCEPTED

P01-04B:
INCOMPLETE / NOT ACCEPTED

P01-04C through P01-04G:
NOT AUTHORIZED
```

This block is a future conditional state. It must never be presented as current.

## 20. Standing status

P01-04B remains incomplete and not accepted. P01-04C through P01-04G remain
unauthorized. No execution authority of any kind is created by this
authorization. The bounded P01-04B2D implementation authority, once active, may
be exercised exactly once and is then spent; it does not authorize a second
attempt, a correction series, a production correction of the minimum-deviation
gap, or a follow-up expansion.
