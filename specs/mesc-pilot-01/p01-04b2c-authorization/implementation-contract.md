# P01-04B2C Implementation Authorization — Implementation Contract

```text
Status:
PROSPECTIVE CONTRACT — NOT EXECUTABLE

THIS CONTRACT BINDS A FUTURE IMPLEMENTATION TASK.
IT BECOMES OPERATIVE ONLY AFTER ALL FIVE FD-B2C-12 ACTIVATION CONDITIONS ARE
SATISFIED AND MECHANICALLY VERIFIED. RECORDING IT IN A DRAFT PULL REQUEST
AUTHORIZES NO IMPLEMENTATION.
```

Canonical authority: [`founder-authorization.md`](founder-authorization.md).

Every identity-bearing and fingerprint-bearing value in this contract is
specified exactly. Where this document says "exactly", no implementation
latitude exists.

---

## 1. Allowed imports

The module may import from the Python standard library and from exactly these
accepted MESC internals:

```text
medscale.mesc._split_v1
  ALGORITHM_VERSION
  SPLIT_SEED
  DECISIONS
  PARTITIONS
  Decision
  Partition
  OrderedExampleRow
  SourceLabelRow
  LabeledExample
  LabelTarget
  GroupAssignment
  join_labels
  constrained_apportionment
  allocate_indivisible_groups

medscale.mesc._canonical_json_v1
  canonical_json_bytes
  canonical_jsonl_bytes
  sha256_of_bytes

medscale.mesc._split_artifacts_v1
  ARTIFACT_SCHEMA_VERSIONS
  SplitSummaryIdentityCore
  SplitFingerprintRecord
  descriptor_for_bytes
  verify_descriptor_against_bytes
  build_split_fingerprint_identity
  build_split_fingerprint_record
  verify_split_fingerprint_record

medscale.mesc._leakage_v1
  LeakageFinding
  LeakageAuditReport

medscale.mesc.split
  PilotSplitAssignment
  PilotSplitManifest
```

**No new dependency is authorized.**

`medscale.mesc._split_v1` defines its own local `canonical_json_bytes` which
emits **no** terminal LF. It must never be used for any B2C canonical byte
surface. Every B2C canonical byte surface uses
`medscale.mesc._canonical_json_v1.canonical_json_bytes`, whose terminal LF is
inside the returned bytes and therefore inside every digest computed over them.

`rank_groups` and `derive_example_id` are reached only transitively, through
`allocate_indivisible_groups` and `join_labels` respectively. B2C must not call
them directly and must not reimplement them.

## 2. Exact classes

Four private classes are authorized, and no others:

```text
FixtureSplitRequest      frozen, slotted dataclass
FixtureSplitResult       frozen, slotted dataclass
FixtureSplitFacade       stateless facade
FixtureFacadeContractError + five subclasses
```

The module defines no `__all__` entry, is not imported by
`medscale/mesc/__init__.py`, and adds no public name.

## 3. `FixtureSplitRequest` — exact fields

```text
fixture_schema_version    str
fixture_namespace         str
fixture_id                str
fixture_sha256            str
fixture_only              bool
non_evidence              bool
synthetic_identity_proof  str
request_id                str
seed                      str
policy_id                 str
transformation_version    str
ordered_rows              tuple[OrderedExampleRow, ...]
source_labels             tuple[SourceLabelRow, ...]
partition_totals          Mapping[str, int]  (immutable snapshot)
leakage_findings          tuple[LeakageFinding, ...]
detection_methods         tuple[str, ...]
execution_evidence_ref    str
```

### 3.1 Exact field contracts

| Field | Contract |
|---|---|
| `fixture_schema_version` | `type(...) is str` and exactly `"1"` |
| `fixture_id` | `type(...) is str`, non-empty; characters drawn only from `abcdefghijklmnopqrstuvwxyz0123456789-`; first and last character is a lowercase letter or digit |
| `fixture_namespace` | exactly `f"mesc-fixture/p01-04b2/1/{fixture_id}"` |
| `fixture_sha256` | `type(...) is str`, length 64, characters drawn only from `0123456789abcdef`; equals the recomputed fixture-identity digest of §5 |
| `fixture_only` | `type(...) is bool` and exactly `True` |
| `non_evidence` | `type(...) is bool` and exactly `True` |
| `synthetic_identity_proof` | `type(...) is str` matching `mesc-synthetic-batch/1:sha256:` + 64 lowercase hex; not a local path |
| `request_id` | `type(...) is str` matching `mesc-pilot-01-fixture-request/1:sha256:` + 64 lowercase hex; equals the recomputed request identity of §6 |
| `seed` | `type(...) is str` and exactly `_split_v1.SPLIT_SEED` |
| `policy_id` | `type(...) is str`, non-empty, stripped, not a local path, no runtime metadata |
| `transformation_version` | `type(...) is str`, non-empty, stripped |
| `ordered_rows` | `type(...) is tuple`; every element `type(...) is OrderedExampleRow`; non-empty |
| `source_labels` | `type(...) is tuple`; every element `type(...) is SourceLabelRow`; non-empty |
| `partition_totals` | exactly the keys `train`, `validation`, `test`; every value `type(...) is int` and `>= 0`; `bool` rejected; `sum(values) == len(ordered_rows)` |
| `leakage_findings` | `type(...) is tuple`; every element `type(...) is LeakageFinding` |
| `detection_methods` | `type(...) is tuple`; every element `type(...) is str`; accepted by `LeakageAuditReport.create()` |
| `execution_evidence_ref` | `type(...) is str`, non-empty, stripped, not a local path |

`type(...) is int` is required rather than `isinstance`, because Python makes
`bool` an `int` subclass and a boolean count must never satisfy a count
invariant.

### 3.2 Path and external-resource rejection

A value is rejected as a local path or external resource when it is empty
after stripping, differs from its stripped form, contains a backslash, begins
with `/`, `./`, `../` or `~`, or has the shape `<letter>:` in its first two
characters. Any `os.PathLike`, file object, socket, connection, generator or
iterator is rejected outright by the exact-type checks of §3.1 before any
content inspection.

### 3.3 Snapshot obligation

`partition_totals` is snapshotted into an immutable mapping during
`__post_init__` **before** validation, so that the values validated are exactly
the values stored. `ordered_rows`, `source_labels`, `leakage_findings` and
`detection_methods` are required to be exact tuples on entry. After
construction, no caller-owned mutable object remains reachable from the
request.

### 3.4 Duplicate rejection

```text
duplicate ordered_rows.original_example_id   -> InvalidFixtureRequestError
duplicate ordered_rows.row_ordinal           -> InvalidFixtureRequestError
duplicate source_labels.original_example_id  -> InvalidFixtureRequestError
duplicate leakage_findings.finding_id        -> InvalidFixtureRequestError
duplicate detection_methods entry            -> InvalidFixtureRequestError
```

Duplicates are never silently deduplicated.

## 4. Validation order — controlling

```text
 1. exact request type
 2. fixture_only and non_evidence markers
 3. schema and namespace
 4. primitive field types
 5. path and external-resource rejection
 6. collection snapshots and duplicate checks
 7. fixture identity
 8. request identity
 9. B1 integration
10. artifact construction and fingerprint verification
11. B2B report construction
12. final cross-object invariants
```

The earlier applicable rule controls. A value violating several rules always
fails at the earliest step, so failures are deterministic and reproducible.

## 5. Exact fixture identity payload

The fixture identity document contains **exactly** these sixteen members:

```json
{
  "schema": "mesc-pilot-01-fixture-identity/1",
  "fixture_schema_version": "1",
  "fixture_namespace": "mesc-fixture/p01-04b2/1/<fixture_id>",
  "fixture_id": "<fixture_id>",
  "fixture_only": true,
  "non_evidence": true,
  "synthetic_identity_proof": "mesc-synthetic-batch/1:sha256:<64-hex>",
  "seed": "<_split_v1.SPLIT_SEED>",
  "policy_id": "<policy_id>",
  "transformation_version": "<transformation_version>",
  "ordered_rows": [],
  "source_labels": [],
  "partition_totals": {},
  "leakage_finding_documents": [],
  "detection_methods": [],
  "execution_evidence_ref": "<execution_evidence_ref>"
}
```

Aliases, omitted members, additional members and alternate container shapes are
prohibited.

### 5.1 Member element shapes

`ordered_rows` elements contain exactly:

```text
original_example_id
row_ordinal
source_document_id
```

`source_labels` elements contain exactly:

```text
configuration
dataset_id
dataset_revision
decision
original_example_id
source_document_id
source_record_hash
```

`leakage_finding_documents` elements are exactly
`LeakageFinding.to_canonical_document()` — B2C constructs no finding document
of its own.

`partition_totals` is the three-key mapping `train`, `validation`, `test`.

### 5.2 Canonical ordering — controlling

```text
ordered_rows              ascending row_ordinal, then original_example_id
source_labels             ascending original_example_id
partition_totals          canonical object-key ordering (serializer sorts keys)
leakage_finding_documents ascending finding_id
detection_methods         caller order preserved — method order is semantic
```

Arrays are placed in canonical order **before** serialization, because the
accepted serializer sorts object members but never reorders arrays.

### 5.3 Digest

```text
FIXTURE_IDENTITY_BYTES = canonical_json_bytes(<fixture identity document>)
fixture_sha256         = sha256_of_bytes(FIXTURE_IDENTITY_BYTES)
```

The recomputed digest is compared with `request.fixture_sha256`. A mismatch
raises `FixtureIdentityMismatchError`.

## 6. Exact request identity payload

```json
{
  "schema": "mesc-pilot-01-fixture-request-identity/1",
  "fixture_sha256": "<recomputed fixture_sha256>",
  "fixture_namespace": "mesc-fixture/p01-04b2/1/<fixture_id>",
  "request_id_domain": "p01-04b2c"
}
```

Exactly four members.

```text
REQUEST_IDENTITY_BYTES = canonical_json_bytes(<request identity document>)
derived_request_id     = "mesc-pilot-01-fixture-request/1:sha256:"
                         + sha256_of_bytes(REQUEST_IDENTITY_BYTES)
```

The derived value is compared with `request.request_id`. A mismatch raises
`FixtureIdentityMismatchError`. The recomputed `fixture_sha256` — not the
caller-supplied one — is the value bound into this document.

## 7. Exact integration pipeline

```text
 1. request = validated FixtureSplitRequest
 2. joined  = join_labels(request.ordered_rows,
                          request.source_labels,
                          transformation_version=request.transformation_version)
 3. label_totals = exact count of joined examples per decision,
                   with every key in DECISIONS present (zero when absent)
 4. targets = constrained_apportionment(label_totals, request.partition_totals)
 5. assignments = allocate_indivisible_groups(joined, targets)
 6. compatibility manifest per §8
 7. canonical artifact bytes per §9
 8. fingerprint per §10
 9. audit_report = LeakageAuditReport.create(
                       findings=request.leakage_findings,
                       detection_methods=request.detection_methods)
10. FixtureSplitResult per §11
11. cross-object invariants per §12
```

`join_labels` returns examples ordered by ascending `row_ordinal` and derives
every `example_id` through `derive_example_id`. B2C consumes that order and
those identifiers unchanged.

`label_totals` must contain every decision in `DECISIONS` with an explicit
integer, including `0`, because `constrained_apportionment` requires exact
keys.

`SourceDocumentGroupedSplitter.assign()` is never called.

## 8. Compatibility manifest — exact rules

For each `GroupAssignment` returned by `allocate_indivisible_groups`, emit one
`PilotSplitAssignment` per `example_id` in that group:

```text
example_id          the group's example_id
split               the group's partition
source_document_id  the group's source_document_id
partition_key       the group's partition_key
```

Ordering, exactly:

```text
1. partition in the order train, validation, test
2. then ascending row_ordinal
3. then ascending example_id
```

The manifest is constructed as:

```python
PilotSplitManifest(
    split_assignments=<ordered assignments>,
    split_hash="",
    split_seed=_split_v1.SPLIT_SEED,
)
```

`split_hash` **must** be the empty string, because
`PilotSplitManifest.computed_split_hash` returns a supplied `split_hash`
verbatim when one is present and only computes the 16-hex value when it is
empty. `split_seed` **must** be passed explicitly; the class default differs
from `_split_v1.SPLIT_SEED`.

```text
split_hash (16 hex) = manifest.computed_split_hash
```

No holdout assignment is permitted. The B1 compatibility-hash algorithm is
never reimplemented. The 16-hex value is display and compatibility only, is
never authoritative, and is never interchangeable with the 64-hex
`split_fingerprint`.

## 9. Canonical artifact byte surfaces — exact schemas and ordering

### 9.1 Group registry — `group_registry_jsonl`

Group ID payload, exactly six members:

```json
{
  "schema": "mesc-pilot-01-group/1",
  "source_document_id": "<source_document_id>",
  "assigned_split": "<train|validation|test>",
  "example_ids": ["<ascending>"],
  "row_ordinals": [0],
  "partition_key": "<partition_key>"
}
```

```text
group_id = "mesc-pilot-01-group/1:sha256:"
           + sha256_of_bytes(canonical_json_bytes(<group id payload>))
```

`example_ids` is ascending lexicographic; `row_ordinals` is ascending numeric.

Group registry record, exactly seven members:

```json
{
  "schema_version": "mesc-pilot-01-group-registry/1",
  "group_id": "<group_id>",
  "source_document_id": "<source_document_id>",
  "example_count": 0,
  "row_ordinals": [0],
  "assigned_split": "<train|validation|test>",
  "partition_key": "<partition_key>"
}
```

Ordering:

```text
assigned_split lexicographically ("test" < "train" < "validation");
then group_id lexicographically
```

```text
group_registry_jsonl = canonical_jsonl_bytes(<ordered group records>)
```

### 9.2 Example registry — `example_registry_jsonl`

Record, exactly six members:

```json
{
  "schema_version": "mesc-pilot-01-example-registry/1",
  "example_id": "<example_id>",
  "source_document_id": "<source_document_id>",
  "row_ordinal": 0,
  "assigned_split": "<train|validation|test>",
  "partition_key": "<partition_key>"
}
```

Ordering:

```text
assigned_split lexicographically;
then row_ordinal ascending;
then example_id lexicographically
```

```text
example_registry_jsonl = canonical_jsonl_bytes(<ordered example records>)
```

### 9.3 Excluded ledger — `excluded_ledger_json`

Exactly:

```json
{
  "count": 0,
  "excluded_ids": [],
  "reason": "none",
  "schema_version": "mesc-pilot-01-excluded-ledger/1"
}
```

```text
excluded_ledger_json = canonical_json_bytes(<the document above>)
```

Any unassigned or excluded example raises
`FixtureIntegrationInvariantError`. The ledger is a constant, never derived
from a non-empty exclusion set.

### 9.4 Summary identity core — `split_summary_identity_core_json`

```python
SplitSummaryIdentityCore(
    total_example_count=len(joined),
    total_group_count=len(assignments),
    excluded_record_count=0,
    partition_totals=<exact per-partition example counts>,
    label_totals=<exact per-decision example counts>,
    partition_label_matrix=<partition -> decision -> count>,
    group_counts_by_partition=<partition -> group count>,
    algorithm_version=_split_v1.ALGORITHM_VERSION,
)
```

`schema_version` is supplied by B2A as
`mesc-pilot-01-split-summary-identity-core/1` and must not be overridden.

```text
split_summary_identity_core_json = core.canonical_bytes()
```

Every mapping passed in is a complete mapping over its domain: `partition_totals`
and `group_counts_by_partition` carry all three partitions; `label_totals`
carries all three decisions; `partition_label_matrix` carries all three
partitions each with all three decisions. Absent combinations are explicit
zeros.

### 9.5 Leakage audit report — `leakage_audit_report_json`

```text
leakage_audit_report_json = audit_report.to_canonical_bytes()
```

B2C constructs no report document of its own.

### 9.6 Descriptor-role boundary

Only four of the six byte surfaces map to B2A descriptor roles:

```text
group_registry     -> group_registry_jsonl
example_registry   -> example_registry_jsonl
excluded_ledger    -> excluded_ledger_json
split_summary      -> split_summary_identity_core_json
```

`split_summary_document_json` and `leakage_audit_report_json` are B2C-level
surfaces outside the B2A descriptor set. They are never given a descriptor
role, never enter the fingerprint payload, and must not be presented as
fingerprint-covered.

## 10. Fingerprint construction — exact and non-circular

```python
identity = build_split_fingerprint_identity(
    policy_id=request.policy_id,
    algorithm_version=_split_v1.ALGORITHM_VERSION,
    split_seed=_split_v1.SPLIT_SEED,
    group_registry_payload=group_registry_jsonl,
    example_registry_payload=example_registry_jsonl,
    excluded_ledger_payload=excluded_ledger_json,
    split_summary_identity_core=core,
)
record = build_split_fingerprint_record(identity)
verify_split_fingerprint_record(record)
```

`build_split_fingerprint_identity` computes the `split_summary` descriptor from
the core itself, so that descriptor can only ever digest the fingerprint-free
identity core.

`verify_split_fingerprint_record` verifies the `split_summary` binding and
recomputes the fingerprint. It does **not** verify the other three descriptors,
whose payloads the record does not carry. B2C must therefore additionally call
`verify_descriptor_against_bytes` for each of `group_registry`,
`example_registry` and `excluded_ledger` against the exact bytes it
constructed, and must not claim fingerprint verification alone covers them.

### 10.1 Final split-summary document — `split_summary_document_json`

Constructed **only after** `record.split_fingerprint` exists:

```json
{
  "schema_version": "mesc-pilot-01-split-summary/1",
  "algorithm_version": "<core.algorithm_version>",
  "excluded_record_count": 0,
  "group_counts_by_partition": {},
  "label_totals": {},
  "partition_label_matrix": {},
  "partition_totals": {},
  "total_example_count": 0,
  "total_group_count": 0,
  "split_hash": "<16 hex>",
  "split_fingerprint": "<64 hex>"
}
```

The members are the core's own members with `schema_version` replaced by
`mesc-pilot-01-split-summary/1` and with `split_hash` and `split_fingerprint`
added.

```text
split_summary_document_json = canonical_json_bytes(<the document above>)
```

This document is **never** an input to the fingerprint. No value derived from
the fingerprint re-enters the hashed payload. The authoritative fingerprint
binds the fingerprint-free identity core only.

## 11. `FixtureSplitResult` — exact fields

```text
request_id                         str
split_manifest                     PilotSplitManifest
group_registry_bytes               bytes
example_registry_bytes             bytes
excluded_ledger_bytes              bytes
split_summary_identity_core        SplitSummaryIdentityCore
split_summary_identity_core_bytes  bytes
split_summary_document_bytes       bytes
split_fingerprint_record           SplitFingerprintRecord
audit_report                       LeakageAuditReport
audit_report_bytes                 bytes
execution_evidence_ref             str
```

Every byte field is `type(...) is bytes`. Every referenced accepted object is
checked with `type(...) is <ExactClass>`.

## 12. Final cross-object invariants

All are verified before the result is returned; any failure raises
`FixtureIntegrationInvariantError`:

```text
request_id equals the validated request ID
execution_evidence_ref equals the validated request reference
split_manifest contains every input example exactly once, and only those
no group crosses a partition
no example_id occurs twice
no row_ordinal occurs twice
per-partition example counts equal request.partition_totals
label totals reconcile with the joined examples
group totals reconcile with the assignments
excluded count is zero
each of the four descriptors matches the exact bytes it describes
verify_split_fingerprint_record(record) succeeds
audit_report_bytes == audit_report.to_canonical_bytes()
split_summary_document_bytes carries the record's split_fingerprint
```

## 13. Errors and codes

```text
FixtureFacadeContractError                  fixture_facade_contract_error
  FixtureOnlyModeError                      fixture_only_mode_error
  InvalidFixtureRequestError                invalid_fixture_request
  FixtureIdentityMismatchError              fixture_identity_mismatch
  FixtureIntegrationInvariantError          fixture_integration_invariant
  InvalidExecutionEvidenceReferenceError    invalid_execution_evidence_reference
```

Each carries a stable machine-readable `code` class variable. The base class is
private and is not exported from `medscale.mesc`.

B1, B2A and B2B typed exceptions propagate **as themselves**. They must not be
caught and re-raised as a generic facade error, so the failing contract remains
attributable to the layer that owns it.

Error messages contain no raw question text, raw context text, answer text,
local path, username, hostname, environment value, timestamp, runtime duration,
command or PID.

## 14. Side-effect boundary

The module performs no filesystem read or write, no network access, no database
access, no subprocess execution, no environment access, no clock access, no
locale access, no timezone access, no logging, no telemetry, no cache access,
no global mutable state, no randomness, no temporary-file creation, no artifact
publication and no workflow dispatch.

It adds no public export, CLI, entry-point registration, capability token,
authentication mechanism, path-safety layer, overwrite handling or concurrency
handling. The last four are unnecessary because B2C has no paths and performs
no writes.

## 15. Required tests

The committed synthetic suite must cover at least the following.

### 15.1 Request boundary

```text
exact type required
dataclass frozen
primitive subclasses rejected
mapping and list substitutes rejected
fixture_only false rejected
non_evidence false rejected
invalid schema rejected
namespace mismatch rejected
malformed fixture ID rejected
malformed SHA-256 rejected
fixture digest mismatch rejected
request ID mismatch rejected
path-shaped evidence reference rejected
wrong seed rejected
wrong partition keys rejected
partition-total mismatch rejected
duplicate example identity rejected
duplicate source-label identity rejected
duplicate row ordinal rejected
```

### 15.2 Deterministic integration

```text
same semantic request produces identical result
caller input ordering is non-semantic where contractually normalized
B1 join used without reimplementation
B1 apportionment used without reimplementation
B1 allocation used without reimplementation
exact targets reconcile
source-document groups remain indivisible
every example assigned exactly once
no exclusion permitted
public SourceDocumentGroupedSplitter.assign remains fail-closed
```

### 15.3 Compatibility manifest

```text
one assignment per example
no holdout
explicit B1 private seed
16-hex split_hash obtained from computed_split_hash
split_hash never treated as authoritative
```

### 15.4 Canonical artifacts

```text
literal golden vectors for every canonical byte surface
terminal LF rules preserved
group IDs deterministic
registry ordering deterministic
zero-exclusion ledger exact
summary identity core exact
final summary non-circular
descriptor digests and sizes exact
authoritative fingerprint verifies
tampered payload fails closed
tampered descriptor fails closed
tampered fingerprint fails closed
```

### 15.5 Leakage integration

```text
explicit findings only
findings sorted through LeakageAuditReport.create
aggregate leaked derived
detection methods validated
no pair enumeration
no dataset scanning
no raw text retained
empty report permitted for B2C unit fixtures
non-empty explicit report preserved exactly
```

### 15.6 Side-effect boundary

```text
no filesystem
no network
no subprocess
no environment
no clock
no logging
no cache
no randomness
no public export
no CLI
no dependency addition
```

### 15.7 Scope proof

```text
exactly two future implementation paths
no modification to accepted B1, B2A or B2B files
no modification to split.py
no modification to __init__.py
```

B2D's three 1,000-row fixtures — `exact-reference-1000-v1`,
`constraint-stress-1000-v1` and `leakage-positive-v1` — must not be
implemented or qualified during B2C.

## 16. Path scope for the future implementation

```text
A src/medscale/mesc/_fixture_split_v1.py
A tests/test_mesc_fixture_split_v1.py
```

Exactly two paths. If implementation proves impossible within them, stop and
return for a new founder authorization. Do not expand the allowlist.
