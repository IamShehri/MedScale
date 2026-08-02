# P01-04B2D Authorization — Implementation Contract

```text
Status:
EXACT FUTURE IMPLEMENTATION CONTRACT — NOT YET ADOPTED

Implementation authority:
RECORDED BUT INACTIVE

Implementation:
NOT AUTHORIZED TO BEGIN
```

This contract binds the future P01-04B2D implementation once — and only once —
implementation authority has activated under FD-B2D-14.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

Every requirement below is **exact**. None is an example, a recommendation, a
default or a starting point. Where this contract states a value, that value is
the requirement.

**No B2D fixture was constructed and no B2D qualification was executed while
drafting this contract.**

---

## 1. Three-path allowlist

The implementation adds exactly these three paths:

```text
tests/_mesc_p01_04b2d_fixtures_v1.py
tests/test_mesc_p01_04b2d_qualification_v1.py
.github/workflows/mesc-p01-04b2d-qualification.yml
```

```text
Branch:
test/mesc-p01-04b2d-qualification

Commit subject:
test(mesc): qualify P01-04B2D synthetic suite

Commit count:
1
```

No existing path may be modified, renamed, deleted or reformatted. No fourth
path may be added. No production module, no dependency, no public export, no
CLI and no entry point is authorized.

`tests/_mesc_p01_04b2d_fixtures_v1.py` is a non-promotable test helper. It is
not a package module, is not importable from `medscale`, and must not be
referenced by any production file.

## 2. Shared synthetic identity contract

```text
dataset_id:              mesc-pilot-01-synthetic-qualification
dataset_revision:        p01-04b2d-v1
fixture_schema_version:  1
fixture_namespace:       mesc-fixture/p01-04b2/1/<fixture-id>
fixture_only:            true
non_evidence:            true
seed:                    mesc-pilot-01-split-v1
policy_id:               mesc-pilot-01-split-policy/1
transformation_version:  mesc-pilot-01-b2d-transform/1
row ordinals:            0 through 999 inclusive
```

Partition totals and label totals for every fixture:

```text
train 700   validation 150   test 150
yes   552   no         338   maybe 110
```

Ratified target matrix:

```text
              train  validation  test  total
yes             386          83    83    552
no              237          50    51    338
maybe            77          17    16    110
total           700         150   150   1000
```

Original-example identifiers:

```text
mesc-b2d-<fixture-id>-example-<four-digit-row-ordinal>
```

`source_record_hash` is the lowercase SHA-256 of the exact UTF-8 ASCII string:

```text
mesc-pilot-01-b2d-source-record-v1|<fixture-id>|<original-example-id>|<source-document-id>|<decision>
```

Literal ASCII `|` bytes. No newline. No trailing separator.

Fixture construction is pure, deterministic and in memory. Prohibited during
construction:

```text
randomness   clock       environment   filesystem   network
subprocess   locale      timezone      database     cache
logging      telemetry   temporary file
```

## 3. Generator-specification identity

Each fixture carries:

```text
synthetic_identity_proof:
mesc-synthetic-batch/1:sha256:<64-lowercase-hex>
```

The digest is the accepted B2A canonical serialization of a document with
exactly these fourteen members:

```text
schema                    fixture_id
fixture_schema_version    generator_version
dataset_id                dataset_revision
configuration             transformation_version
policy_id                 row_count
partition_totals          label_totals
grouping_contract         leakage_scenario_contract
```

```text
schema:            mesc-pilot-01-b2d-generator-spec/1
generator_version: mesc-pilot-01-b2d-generator/1
row_count:         1000
```

The proof binds the generator specification only. It must not bind
`fixture_sha256`, `request_id`, `split_hash`, `split_fingerprint`, runtime,
operating system, Python version, timestamp, path or workflow run ID. It must be
computable before the facade runs.

## 4. `exact-reference-1000-v1`

Conforms to FD-B2-7 Fixture A without amendment.

```text
rows:    1000
groups:  89
group sizes present: 1, 2, 3, 5, 8, 13
multi-example groups: mandatory
exact ratified matrix: FEASIBLE
```

### 4.1 Exact group-size vectors

`13x29` means twenty-nine groups of size 13.

```text
yes / train:        13x29, 8, 1        sum 386    31 groups
yes / validation:   13x6, 5            sum  83     7 groups
yes / test:         13x6, 5            sum  83     7 groups

no / train:         13x18, 2, 1        sum 237    20 groups
no / validation:    13x3, 8, 3         sum  50     5 groups
no / test:          13x3, 8, 3, 1      sum  51     6 groups

maybe / train:      13x5, 8, 3, 1      sum  77     8 groups
maybe / validation: 13, 3, 1           sum  17     3 groups
maybe / test:       13, 3              sum  16     2 groups
```

```text
group counts:  yes 45   no 31   maybe 13   total 89
row counts:    yes 552  no 338  maybe 110  total 1000
```

Every partition contains multiple multi-example groups. No group crosses a
partition. No group crosses a decision stratum.

### 4.2 Independent construction procedure

For each decision in the order `yes`, `no`, `maybe`:

```text
1. generate exactly the required number of candidate source-document
   identifiers for that decision
2. compute each candidate's D6 partition key independently from the exact
   ratified canonical payload
3. use the no-terminal-LF D6 serialization contract
4. sort candidates by:
     digest ascending (lowercase hexadecimal)
     source-document identifier ascending
     defensive candidate ordinal ascending
5. concatenate that decision's train, validation and test group-size vectors
   in that order
6. bind the ordered group-size vector positionally to the ordered candidates
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

Serialization: recursively sorted keys, UTF-8, `ensure_ascii=False`,
`allow_nan=False`, separators `(",", ":")`, no indentation, no BOM,
**no terminal newline**.

While constructing the expected grouping plan the generator must not call
`rank_groups`, `allocate_indivisible_groups` or `FixtureSplitFacade`.

### 4.3 Required proofs

The facade under test must independently reproduce:

```text
partition totals 700 / 150 / 150
the exact ratified label matrix
89 groups
all six required group sizes present
zero group crossing a partition
zero group crossing a decision stratum
no duplicate example ID
no duplicate row ordinal
zero excluded examples
clean leakage report
byte-identical outputs in all six workflow cells
```

## 5. `constraint-stress-1000-v1`

Conforms to FD-B2-7 Fixture B without amendment. This fixture **must** make the
exact ratified matrix infeasible. It must not be redesigned to reach zero
deviation.

```text
rows:    1000
groups:  500
group size: exactly 2 for every group
homogeneous by decision: every group
exact ratified matrix: INFEASIBLE
```

```text
group counts:  yes 276   no 169   maybe 55   total 500
row counts:    yes 552   no 338   maybe 110  total 1000
```

### 5.1 Mechanical infeasibility proof

Every group has size 2 and no group may cross a partition or a decision
stratum, so every realized label-by-partition cell is even.

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

The test must prove this mechanically, not assert it.

### 5.2 Global minimum-deviation oracle

The oracle must completely derive every matrix satisfying:

```text
every label row total exactly
every partition column total exactly
every cell a non-negative even integer
```

```text
objective:
minimize the sum of squared deviations from the ratified 3x3 target matrix

tie-break:
lexicographically smallest vector
label order:      yes, no, maybe
partition order:  train, validation, test
```

```text
minimum squared-deviation score:
6
```

Exactly **two** feasible matrices attain score 6. Both are frozen here.

Founder-frozen selected global optimum:

```text
Matrix A — lexicographic winner

              train  validation  test  total
yes             386          82    84    552
no              238          50    50    338
maybe            76          18    16    110
total           700         150   150   1000
```

```text
flattened vector:
386,82,84,238,50,50,76,18,16

deviation:  yes    0, -1, +1
            no    +1,  0, -1
            maybe -1, +1,  0
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

```text
flattened vector:
386,84,82,236,50,52,78,16,16

deviation:  yes    0, +1, -1
            no    -1,  0, +1
            maybe +1, -1,  0
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
and Matrix B holds `84`, so Matrix A is strictly smaller. Stating only that a
second score-6 matrix exists is insufficient; both vectors are frozen above.

The test must independently enumerate or prove the complete feasible lattice and
assert:

```text
minimum score = 6
number of score-6 matrices = 2
selected matrix = Matrix A
other score-6 matrix = Matrix B
```

Required additional proofs:

```text
the exact ratified matrix is infeasible
the lexicographically selected optimum equals the frozen Matrix A
zero source-document group overlap
partition totals remain 700 / 150 / 150
explicit deviation is recorded
```

### 5.3 Expected typed failure of the accepted implementation

The accepted B1/B2C implementation performs exact-target allocation only.
`allocate_indivisible_groups` raises `SplitAllocationError` when a ranked group
would cross a target boundary. It does not implement the required global
minimum-deviation fallback.

The test must assert that exact typed failure when this fixture reaches the
infeasible boundary, including the accepted error type and its stable
boundary-crossing semantics.

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

A green test means the harness detected and classified the gap correctly. It
does not mean production behaviour satisfies FD-B2-7.

```text
No production correction is authorized in B2D.
```

### 5.4 Derived negative mutations

Derived negative mutations must include:

```text
a group that would cross one exact boundary
a source-document group crossing decision strata
```

They must fail closed through the accepted typed B1/B2C errors. They are **not**
additional approved fixtures, receive no fixture namespace, no identity digest
and no qualification status.

## 6. `leakage-positive-v1`

Conforms to FD-B2-7 Fixture C without amendment.

```text
rows:                    1000
source-document groups:  999
findings:                9

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
singleton groups are **founder-frozen requirements**, not derived values. A
fixture with any other group count does not satisfy this contract.

The two-example group's source-document identifier is the lowest-indexed
candidate in a documented candidate sequence whose independently computed D6
rank places the group strictly inside a partition run. That identifier is frozen
as a literal constant.

### 6.1 Required deterministic scenarios

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

### 6.2 Scenario table

| # | finding_type | shared_surface | score_representation | classification |
|---|---|---|---|---|
| 1 | `exact_example` | `example_id` | `none` | `false_positive` |
| 2 | `source_document` | `source_document_id` | `none` | `false_positive` |
| 3 | `exact_question` | `question_bytes` | `none` | `unresolved` |
| 4 | `normalized_question` | `normalized_question` | `none` | `unresolved` |
| 5 | `near_duplicate_question` | `question_token_set` | `jaccard:9/10` | `unresolved` |
| 6 | `near_duplicate_question` | `question_token_set` | `jaccard:10/11` | `unresolved` |
| 7 | `context_overlap` | `context_bytes` | `none` | `unresolved` |
| 8 | `context_overlap` | `context_token_set` | `jaccard:19/20` | `unresolved` |
| 9 | `empty_normalized_question` | `empty_normalized_question` | `not_evaluable` | `false_positive` |

### 6.3 Exact synthetic surfaces

**Scenario 3 — exact question.** Both sides exactly:

```text
does alpha therapy reduce beta outcome?
```

**Scenario 4 — normalized question.** The left surface is specified by exact
byte composition rather than as a literal fenced line, because its leading and
trailing ASCII spaces are significant and invisible whitespace must not depend
on how a document is copied or trimmed.

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

Exactly two leading ASCII spaces, one U+00A0 NO-BREAK SPACE between `Does` and
`ALPHA`, exactly two trailing ASCII spaces, no tab, no line feed.

Right:

```text
does alpha therapy reduce beta outcome?
```

**Scenario 5 — Jaccard exactly at threshold.**

```text
left:   alpha beta gamma delta epsilon zeta eta theta iota kappa
right:  alpha beta gamma delta epsilon zeta eta theta iota

intersection 9   union 10   jaccard:9/10   passed exactly at 0.90
```

**Scenario 6 — Jaccard above threshold.**

```text
left:   alpha beta gamma delta epsilon zeta eta theta iota kappa lambda
right:  alpha beta gamma delta epsilon zeta eta theta iota kappa

intersection 10   union 11   jaccard:10/11   passed above 0.90
```

**Scenario 7 — exact context.** Identical deterministic context surfaces on both
sides.

**Scenario 8 — approximate context overlap.** Left contains exactly:

```text
ctx01 ctx02 ctx03 ctx04 ctx05 ctx06 ctx07 ctx08 ctx09 ctx10
ctx11 ctx12 ctx13 ctx14 ctx15 ctx16 ctx17 ctx18 ctx19 ctx20
```

Right contains exactly the first nineteen.

```text
intersection 19   union 20   jaccard:19/20   passed exactly at 0.95
```

**Scenario 9 — both-empty normalized questions.**

```text
left:   ASCII space + horizontal tab + line feed
right:  U+2003 EM SPACE + U+00A0 NO-BREAK SPACE
```

### 6.4 Evidence references

```text
scenario 1:
mesc-pilot-01-b2d-leakage-scenario/1/exact-example-self-control

scenario 2:
mesc-pilot-01-b2d-leakage-scenario/1/expected-same-group-source-document

scenario 9:
mesc-pilot-01-b2d-leakage-scenario/1/whitespace-only-control
```

General format:

```text
mesc-pilot-01-b2d-leakage-scenario/1/<scenario-slug>
```

Every `false_positive` must carry a stable supporting-evidence reference.

### 6.5 Detection methods

Exact tuple, in exactly this caller order:

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

### 6.6 Final audit

```text
finding_count:             9
leaked:                    true
suppressed findings:       0
supported false positives: 3   (scenarios 1, 2, 9)
unresolved findings:       6   (scenarios 3 through 8)
```

`leaked` is `true` because at least one finding is `unresolved`. `suppressed`
must always be `false`. No finding may be dropped, omitted or silently
reclassified.

### 6.7 Raw-text exclusion

No raw synthetic question or context text may appear in:

```text
finding canonical documents   finding IDs        audit-report bytes
fixture result bytes          fingerprint payload
split-summary bytes           registries
```

Raw synthetic surfaces exist only inside the non-promotable test helper.

### 6.8 Semantic boundary

Scenarios 1 and 2 are same-partition synthetic controls. They qualify primitive
behaviour, finding construction, canonical identity, classification and
evidence-reference enforcement. They do **not** claim cross-partition duplicate
membership, cross-partition source-document overlap, real leakage or real
dataset scanning.

## 7. Scenario and identity freezing

During the activated implementation only:

```text
1. derive the fixture's expected valid assignments independently
2. identify actual partitions
3. choose deterministic scenario records
4. freeze as literal constants:
     original example IDs
     derived example IDs
     source-document IDs
     actual partitions
     expected finding IDs
```

The committed qualification tests must not dynamically choose scenario
identities from the facade result under test. The exact-example self-control and
the exact-source-document same-group control must use actual valid fixture
membership. **No fabricated partition claim is permitted.**

## 8. Literal golden requirements

For each fixture, literal constants must include:

```text
synthetic_identity_proof     fixture_sha256
request_id                   compatibility split_hash
authoritative split_fingerprint

group-registry SHA-256 and byte size
example-registry SHA-256 and byte size
excluded-ledger SHA-256 and byte size
split-summary identity-core SHA-256 and byte size
final split-summary SHA-256 and byte size
leakage-audit-report SHA-256 and byte size

record count      group count       partition counts
label matrix      excluded count    finding count
leaked            ordered finding IDs
```

For `constraint-stress-1000-v1` the frozen expectation is the typed fail-closed
outcome of §5.3 together with the infeasibility proof and the frozen
minimum-deviation matrix — not a successful result document.

For `leakage-positive-v1` literal constants must include:

```text
all 9 ordered finding IDs
all 9 classifications
all 9 evidence-reference outcomes
finding_count = 9
leaked = true
```

Literal expected values must never be computed at test runtime from the facade
result under test. The future implementation report must label every produced
value:

```text
SYNTHETIC QUALIFICATION VECTORS
NOT REAL DATASET EVIDENCE
NOT A CANONICAL SPLIT
NOT A REAL LEAKAGE AUDIT
```

## 9. Six-cell qualification workflow

```text
path:  .github/workflows/mesc-p01-04b2d-qualification.yml
name:  MESC P01-04B2D Qualification
```

Triggers exactly `pull_request` and `push` to `main`. Prohibited:
`workflow_dispatch`, `schedule`, `repository_dispatch`, issue triggers, release
triggers.

```yaml
permissions:
  contents: read
```

No write permission, no secrets, no artifact upload, no cache publication, no
branch mutation.

Matrix, with `fail-fast: false`:

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

The workflow mirrors the repository's accepted setup-action versions and locked
sync convention as observed at the canonical baseline: SHA-pinned
`actions/checkout` and `astral-sh/setup-uv` with an explicit pinned uv version,
`persist-credentials: false`, and `uv sync --frozen`.

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

## 10. P01-04B criteria mapping

Every criterion gets one dedicated test or test group, an exact assertion, a
clear failure message and a report link to the test symbol.

The mapping covers **13 unique criteria**.

```text
The mapping contains:
- the ten P01-04B tooling-acceptance criteria; and
- three additional non-duplicative future-code criteria from
  p01-04b2/acceptance.md.
```

The ten tooling rows alone do not represent every canonical criterion.

| # | P01-04B / B2 future-code criterion | Expected result |
|---|---|---|
| 1 | `SourceDocumentGroupedSplitter.assign` remains unconditionally fail-closed | SATISFIED |
| 2 | `FixtureSplitFacade` exists as the separate fixture-only facade | SATISFIED |
| 3 | the qualification path is library-only and in-memory | SATISFIED |
| 4 | no B2 CLI exists | SATISFIED |
| 5 | the 64-hex `split_fingerprint` is authoritative | SATISFIED |
| 6 | the 16-hex `split_hash` is compatibility/display only | SATISFIED |
| 7 | leakage normalization follows FD-B2-6 | SATISFIED |
| 8 | exactly the three named fixtures form the suite | SATISFIED |
| 9 | stable synthetic inputs produce byte-identical results | SATISFIED |
| 10 | no real P01-03G membership is generated or disclosed | SATISFIED |
| 11 | atomic publication | **NOT APPLICABLE** to B2D; **NOT SATISFIED** for P01-04B overall |
| 12 | write-path protections | **NOT APPLICABLE** to B2D; **NOT SATISFIED** for P01-04B overall |
| 13 | date-free promotable artifacts | **NOT APPLICABLE** to B2D output promotion; date-free byte invariant testable |
| — | indivisible-group global minimum-deviation allocation (FD-B2-7 Fixture B) | **UNSATISFIED** |

Allowed result classes:

```text
SATISFIED   UNSATISFIED   BLOCKED   NOT APPLICABLE
```

### 10.1 Criterion 11 — Atomic publication

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

### 10.2 Criterion 12 — Write-path protections

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

### 10.3 Criterion 13 — Date-free promotable artifacts

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

The test must assert that every canonical B2D byte surface — every registry, the
excluded ledger, the split-summary identity core, the final split summary, the
leakage-audit report and the fingerprint payload — is free of:

```text
date fields        timestamps        local paths
usernames          hostnames         runtime durations
workflow IDs       command logs      workspace locations
```

The mapping status remains bounded to B2D and must not claim real promotability.

### 10.4 Aggregate acceptance rule

```text
minimum-deviation capability:
UNSATISFIED

atomic publication:
NOT APPLICABLE TO B2D; NOT SATISFIED FOR P01-04B OVERALL

write-path protections:
NOT APPLICABLE TO B2D; NOT SATISFIED FOR P01-04B OVERALL

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

```text
GREEN B2D QUALIFICATION CI
DOES NOT EQUAL P01-04B ACCEPTANCE.
```

The implementation report must separate:

```text
qualification-harness correctness
fixture-specific observations
implementation capability gaps
P01-04B acceptance recommendation
```

It must not report P01-04B as accepted. Expected recommendation:
`CHANGES REQUIRED`.

## 11. Anti-circularity rules

The committed tests may invoke:

```text
FixtureSplitFacade.run
accepted B1 dataclasses and functions
accepted B2A canonical and fingerprint APIs
accepted B2B primitives and finding types
```

They must not use any private helper from `_fixture_split_v1.py` to construct
expected values. Expected registries, summaries, hashes, fingerprints and audit
identities are literal constants.

Both the exact-reference grouping plan and the constraint-stress D6 ranking
oracle must be independently implemented from the ratified canonical payload and
must not call `rank_groups`, `allocate_indivisible_groups` or
`FixtureSplitFacade` while generating a fixture.

Prohibited in committed code:

```text
golden regeneration command    --update-goldens option
automatic expected-value rewrite   self-approval routine
```

## 12. Fail-closed rules

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
No tolerance.  No flaky retry.  No xfail.
No skip in the dedicated six-cell qualification workflow.
```

A literal golden change requires a new founder decision, a new fixture or
generator version when semantics change, and a fresh independent review. A
builder may not update a golden merely because the implementation emits a
different value.

## 13. Evidence classification

All B2D inputs and outputs are synthetic, fixture-only, non-evidence,
non-clinical, non-promotable as a real split and non-promotable as a real
leakage audit.

The workflow proves only deterministic synthetic qualification behaviour,
cross-runtime equality against frozen literals, and integration of accepted B1,
B2A, B2B and B2C layers. It does not prove the real dataset is leak-free, the
real split is valid, P01-03G membership, scientific performance, model quality
or clinical safety.

Workflow logs and status are external CI evidence only. No B2D result file is
promoted into the repository.

## 14. Prohibitions

The implementation must not perform or enable:

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

P01-04C through P01-04G implementation or execution
P01-05 or later
```

It must not alter D1–D10, FD-B2-1–FD-B2-8, or accepted B2A, B2B or B2C
behaviour. No CLI, no public API, no filesystem-facing product capability.

## 15. Implementation report requirements

The future implementation report must record:

```text
exact head, tree, parent and subject
exactly three added paths with blob SHAs and statistics
zero modified existing paths
the three fixture identities and their generator-spec proofs
the full literal golden vector set, labelled SYNTHETIC QUALIFICATION VECTORS
the P01-04B criteria matrix covering all 13 unique criteria with one result
  class per criterion, including the three non-duplicative future-code rows
the UNSATISFIED minimum-deviation criterion stated explicitly
the complete score-6 tie-break evidence: minimum score 6, exactly two score-6
  matrices, selected Matrix A and runner-up Matrix B
the constraint-stress typed fail-closed observation
all six workflow cell results
a P01-04B acceptance recommendation of CHANGES REQUIRED
an explicit statement that green CI does not equal P01-04B acceptance
an explicit statement that no production correction was made
```

It must not report B2D as accepted, P01-04B as accepted, or any downstream phase
as authorized.

## 16. One bounded implementation

```text
one branch          test/mesc-p01-04b2d-qualification
one commit          test(mesc): qualify P01-04B2D synthetic suite
three paths         exactly the FD-B2D-1 allowlist
one attempt         authority is spent at that commit
```

A correction after the authorized commit requires a separate founder correction
decision. No silent second implementation commit is authorized.
