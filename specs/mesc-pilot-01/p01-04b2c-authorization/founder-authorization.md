# P01-04B2C Implementation Authorization — Founder Authorization

```text
Status:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

Decision:
AUTHORIZE P01-04B2C IMPLEMENTATION
SUBJECT TO VALID CANONICAL ADOPTION OF THIS PACKAGE

FD-B2C-1 through FD-B2C-12:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
RECORDED BUT INACTIVE

P01-04B2C implementation:
NOT AUTHORIZED TO BEGIN

P01-04B2D:
NOT AUTHORIZED

P01-04B:
INCOMPLETE / NOT ACCEPTED

Real split generation, real or canonical leakage-audit execution,
P01-03G or real-data access, model access, inference, retrieval, metrics,
benchmark execution, training, fine-tuning, publication and clinical use:
NOT AUTHORIZED
```

Founder:
Abdulaziz Alshehri

Decision date:
2026-08-02

Required canonical baseline:
`3c4d7f153522128533fa9aba26209426b248b4f1`

This document is **controlling** for this package. On any conflict between this
document and [`README.md`](README.md),
[`implementation-contract.md`](implementation-contract.md) or
[`acceptance.md`](acceptance.md), this document controls.

---

## 0. Subordination

These decisions are subordinate to, and must not be read as amending, any of:

```text
P01-04A decisions D1 through D10
FD-B2-1 through FD-B2-8
FD-B2A-1 through FD-B2A-8
FD-B2A-9
FD-B2B-1 through FD-B2B-10
FD-B2B-11
the accepted B2A implementation
the accepted B2B implementation
```

Prior governance history is adopted at
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/)
and
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/)
and is not restated here. Those packages are immutable historical authorities.

Where this package appears to conflict with a senior authority, the senior
authority controls and the conflicting B2C text is void to the extent of the
conflict.

### Accepted implementation identities this package builds on

```text
B2A — canonical implementation merge
5736b1171f1aa467105d931713f5749fb81acd5b
final implementation head
7307fcf9085d3d15114984731b49d484523f09eb
accepted private modules
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py

B2B — canonical implementation merge
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863
reviewed implementation head
86cfdca1797cf1be60761284af1cc81e25047f41
accepted tree
070b177194094e5ae55d34570a86997fde956302
accepted private module
src/medscale/mesc/_leakage_v1.py

B1 split core — accepted private module
src/medscale/mesc/_split_v1.py
```

The future B2C implementation **reuses** these accepted modules. It must not
fork or reimplement their canonical serialization, fingerprint, allocation or
leakage contracts.

## FD-B2C-1 — Private module and exact future path allowlist

The future implementation may add exactly two paths:

```text
A src/medscale/mesc/_fixture_split_v1.py
A tests/test_mesc_fixture_split_v1.py
```

No third implementation path is authorized. If the implementation proves
impossible within these two paths, stop and return for a new founder
authorization. Do not expand the allowlist.

The future implementation must not modify:

```text
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
any CLI
any workflow
any dependency or lockfile
any governance document
```

The module is private. It must not be publicly exported, must not be added to
`medscale.mesc.__all__`, and must not be reachable from any public façade,
entry point or CLI.

## FD-B2C-2 — Stateless fixture-only facade

One private facade is authorized:

```text
FixtureSplitFacade
```

Required behaviour:

```text
library-only
in-memory only
stateless
deterministic
no constructor access to environment or configuration
accepts exactly one FixtureSplitRequest
returns exactly one FixtureSplitResult
```

The accepted invocation shape is exactly:

```python
FixtureSplitFacade.run(request: FixtureSplitRequest) -> FixtureSplitResult
```

`type(request) is FixtureSplitRequest` is required. **No coercion is
permitted.** The facade must reject, fail-closed and without attempting
conversion:

```text
dict or mapping substitutes
duck-typed objects
path-like objects
arbitrary sequences
real-registry adapters
filesystem handles
file names
directory names
URLs
database connections
iterators backed by external resources
```

The facade holds no instance state that can influence a result. Two invocations
with the same semantic request must produce identical bytes in every byte
surface.

## FD-B2C-3 — Exact immutable request contract

One frozen, slotted private dataclass is authorized:

```text
FixtureSplitRequest
```

Exact semantic fields, and no others:

```text
fixture_schema_version
fixture_namespace
fixture_id
fixture_sha256
fixture_only
non_evidence
synthetic_identity_proof
request_id
seed
policy_id
transformation_version
ordered_rows
source_labels
partition_totals
leakage_findings
detection_methods
execution_evidence_ref
```

Required field contracts:

```text
fixture_schema_version:
exact str equal to "1"

fixture_id:
exact non-empty ASCII identifier;
lowercase letters, digits and hyphen only;
must begin and end with a letter or digit

fixture_namespace:
exactly "mesc-fixture/p01-04b2/1/<fixture_id>"

fixture_sha256:
64 lowercase hexadecimal characters;
must equal the recomputed canonical fixture-identity digest

fixture_only:
exact bool true

non_evidence:
exact bool true

synthetic_identity_proof:
stable non-path identifier with format
"mesc-synthetic-batch/1:sha256:<64-lowercase-hex>"

request_id:
stable deterministic identifier with format
"mesc-pilot-01-fixture-request/1:sha256:<64-lowercase-hex>";
must equal the recomputed request identity

seed:
exactly medscale.mesc._split_v1.SPLIT_SEED

policy_id:
exact non-empty stable identifier;
no local path or runtime metadata

transformation_version:
exact non-empty stable identifier

ordered_rows:
exact tuple of accepted B1 OrderedExampleRow values

source_labels:
exact tuple of accepted B1 SourceLabelRow values

partition_totals:
immutable snapshot with exactly train, validation and test;
every value exact non-negative int;
bool prohibited;
sum equals ordered-row count

leakage_findings:
exact tuple of accepted B2B LeakageFinding values

detection_methods:
exact tuple accepted by LeakageAuditReport.create()

execution_evidence_ref:
stable non-empty non-path reference;
B2C does not create or write the referenced evidence
```

**Payload ownership is identity-only.** The request carries the accepted B1
identity-and-label row types. It never carries raw question text, context text
or answer text, and the facade never reads such text because no field can hold
it.

**Caller-owned collections must never remain reachable.** Every supplied
mapping or sequence is snapshotted into an immutable value during
construction, so a later mutation by the caller cannot change any canonical
byte surface, digest or fingerprint already derived from it. `bool` must never
satisfy an `int` requirement.

## FD-B2C-4 — Fixture identity and honest proof semantics

### Fixture identity document

The fixture identity document contains exactly these members and no others:

```text
schema
fixture_schema_version
fixture_namespace
fixture_id
fixture_only
non_evidence
synthetic_identity_proof
seed
policy_id
transformation_version
ordered_rows
source_labels
partition_totals
leakage_finding_documents
detection_methods
execution_evidence_ref
```

Canonical ordering rules:

```text
ordered_rows:
ascending row_ordinal, then original_example_id

source_labels:
ascending original_example_id

partition_totals:
canonical object-key ordering

leakage_finding_documents:
ascending finding_id

detection_methods:
caller order preserved because method order is semantic
```

Canonical bytes must come **exclusively** from:

```text
medscale.mesc._canonical_json_v1.canonical_json_bytes
```

`fixture_sha256` is:

```text
SHA-256 of the exact canonical fixture identity bytes
```

### Request identity document

The request identity document contains exactly:

```text
schema
fixture_sha256
fixture_namespace
request_id_domain
```

where:

```text
schema = "mesc-pilot-01-fixture-request-identity/1"
request_id_domain = "p01-04b2c"
```

The derived request ID is:

```text
mesc-pilot-01-fixture-request/1:sha256:
<64-lowercase-hex SHA-256 of the canonical request identity bytes>
```

Both digests are **recomputed and compared** against the caller-supplied
values. A caller-supplied `fixture_sha256` or `request_id` is never trusted.

### Honest structural-proof semantics

The implementation must state honestly:

```text
Structural fixture proof establishes internal identity consistency.
It is not a cryptographic or real-world provenance oracle.
```

`fixture_only`, `non_evidence` and `synthetic_identity_proof` are **declared
markers**. They prove that the request is internally consistent with the
identity it claims. They do **not** prove the underlying rows are synthetic,
and no combination of flags can detect a caller who deliberately repackages
real data into the accepted row types.

B2C safety therefore derives from structure, not from the flags:

```text
private module
no public export
no CLI
no path input
no registry adapter
no filesystem access
no real-data entry point
SourceDocumentGroupedSplitter.assign remaining fail-closed
```

The implementation **must not** claim that flags alone can detect a malicious
caller repackaging real data. Any documentation or docstring asserting
provenance, authenticity or real-world guarantees from these markers is a
contract violation.

## FD-B2C-5 — Exact B1 integration pipeline

The facade must use the accepted B1 functions directly, in this exact order:

```text
 1. validate and freeze FixtureSplitRequest
 2. call join_labels(...)
 3. derive label totals from the joined examples
 4. call constrained_apportionment(label_totals, partition_totals)
 5. call allocate_indivisible_groups(joined_examples, targets)
 6. construct deterministic compatibility assignments and manifest
 7. construct canonical in-memory artifact bytes
 8. build and verify the authoritative B2A split fingerprint
 9. construct the B2B LeakageAuditReport from explicit findings
10. construct FixtureSplitResult
11. run final cross-object invariant verification
```

The following must not be reimplemented, forked, inlined or partially
duplicated:

```text
derive_example_id
join_labels
constrained_apportionment
rank_groups
allocate_indivisible_groups
canonical_json_bytes
canonical_jsonl_bytes
B2A fingerprint construction
B2B finding identity
B2B report aggregation
```

In particular, `example_id` values are produced only by `join_labels`, which
calls `derive_example_id` internally. B2C must never derive an example ID
itself.

The facade must **never** call:

```text
SourceDocumentGroupedSplitter.assign()
```

That public method must remain unconditionally fail-closed and byte-identical.
B2C introduces no path by which it can succeed.

## FD-B2C-6 — B1 compatibility manifest

The facade may construct an in-memory:

```text
PilotSplitManifest
```

using:

```text
PilotSplitAssignment
```

Requirements:

```text
one PilotSplitAssignment per joined example
no holdout assignment
exact train/validation/test partitions only
partition_key copied from the accepted B1 group assignment
source_document_id preserved exactly
example_id preserved exactly
split_seed explicitly equal to _split_v1.SPLIT_SEED
```

`PilotSplitManifest.split_seed` carries a different default. The implementation
must pass `_split_v1.SPLIT_SEED` **explicitly**; relying on the default is a
contract violation.

Compatibility assignment ordering:

```text
train, validation, test;
then row_ordinal;
then example_id
```

The 16-hex compatibility value must be obtained from:

```text
PilotSplitManifest.computed_split_hash
```

`computed_split_hash` returns a caller-supplied `split_hash` when one is
present, so the manifest must be constructed with an empty `split_hash` for the
value to be genuinely computed. Do not reimplement the B1 compatibility-hash
algorithm.

The 16-hex value remains:

```text
display and compatibility only
never authoritative
never interchangeable with split_fingerprint
```

The authoritative identity is the 64-hex `split_fingerprint` of FD-B2C-7. The
two values must never be substituted for one another, compared to one another,
or presented as alternatives.

## FD-B2C-7 — Canonical in-memory artifacts

The facade must construct these byte surfaces **in memory only**:

```text
group_registry_jsonl
example_registry_jsonl
excluded_ledger_json
split_summary_identity_core_json
split_summary_document_json
leakage_audit_report_json
```

No byte surface may be written to disk, published, uploaded or persisted.

### Group registry record

Exact members:

```text
schema_version
group_id
source_document_id
example_count
row_ordinals
assigned_split
partition_key
```

Required schema:

```text
mesc-pilot-01-group-registry/1
```

`group_id` must be derived from canonical bytes containing exactly:

```text
schema
source_document_id
assigned_split
example_ids
row_ordinals
partition_key
```

Format:

```text
mesc-pilot-01-group/1:sha256:<64-lowercase-hex>
```

Group-registry ordering:

```text
assigned_split lexicographically;
then group_id lexicographically
```

### Example registry record

Exact members:

```text
schema_version
example_id
source_document_id
row_ordinal
assigned_split
partition_key
```

Required schema:

```text
mesc-pilot-01-example-registry/1
```

Example-registry ordering:

```text
assigned_split lexicographically;
then row_ordinal ascending;
then example_id lexicographically
```

### Excluded ledger

B2C authorizes **no exclusion**. The document is exactly:

```json
{
  "count": 0,
  "excluded_ids": [],
  "reason": "none",
  "schema_version": "mesc-pilot-01-excluded-ledger/1"
}
```

Any unassigned or excluded example is a fail-closed integration error.

### Summary identity core

Construct the accepted B2A:

```text
SplitSummaryIdentityCore
```

from:

```text
total example count
total group count
excluded record count = 0
partition totals
label totals
partition-label matrix
group counts by partition
B1 algorithm version
```

Its `schema_version` is fixed by B2A as
`mesc-pilot-01-split-summary-identity-core/1`. This is **not** the same
document as the final split-summary document below, and the two schemas must
never be conflated.

### Authoritative fingerprint

Use only:

```text
build_split_fingerprint_identity
build_split_fingerprint_record
verify_split_fingerprint_record
```

Required values:

```text
algorithm_version = _split_v1.ALGORITHM_VERSION
split_seed        = _split_v1.SPLIT_SEED
policy_id         = request.policy_id
```

`verify_split_fingerprint_record` verifies the `split_summary` descriptor
binding and recomputes the fingerprint. It does **not** verify the other three
descriptors, whose payloads the record does not carry. B2C must therefore
independently verify the `group_registry`, `example_registry` and
`excluded_ledger` descriptors against the exact bytes it constructed, and must
not claim that fingerprint verification alone covers them.

### Final split-summary document

The final non-identity summary document is constructed **only after** the
authoritative fingerprint exists. It contains:

```text
schema_version
all SplitSummaryIdentityCore members
split_hash
split_fingerprint
```

Required schema:

```text
mesc-pilot-01-split-summary/1
```

The authoritative fingerprint binds the fingerprint-free identity core, **not**
the final summary document. No circular fingerprinting is permitted: no value
derived from the fingerprint may re-enter the hashed payload.

## FD-B2C-8 — Leakage integration without scanning

B2C must not:

```text
enumerate record pairs
scan a dataset
discover findings automatically
search a registry
read raw question or context text
run a real leakage audit
```

The request supplies explicit accepted B2B `LeakageFinding` values. The facade
must construct the report using exactly:

```python
LeakageAuditReport.create(
    findings=request.leakage_findings,
    detection_methods=request.detection_methods,
)
```

B2C may validate, sort and aggregate explicit findings only. Sorting and
aggregation are performed by the accepted B2B code, not by B2C.

An empty report is permitted at B2C unit level. B2D later determines the
required findings for:

```text
exact-reference-1000-v1
constraint-stress-1000-v1
leakage-positive-v1
```

B2C must not claim qualification of any of those fixtures, must not implement
them, and must not treat an empty report as evidence that a fixture is clean.

## FD-B2C-9 — Exact immutable result contract

One frozen, slotted private dataclass is authorized:

```text
FixtureSplitResult
```

Exact fields:

```text
request_id
split_manifest
group_registry_bytes
example_registry_bytes
excluded_ledger_bytes
split_summary_identity_core
split_summary_identity_core_bytes
split_summary_document_bytes
split_fingerprint_record
audit_report
audit_report_bytes
execution_evidence_ref
```

Requirements:

```text
all byte fields are exact bytes
all referenced accepted objects have exact expected types
request_id equals the validated request ID
execution_evidence_ref equals the validated request reference
split_manifest contains every and only input example
no group crosses partitions
no example occurs twice
no row ordinal occurs twice
partition totals reconcile
label totals reconcile
group totals reconcile
excluded count is zero
all descriptors match exact bytes
split fingerprint verifies
audit_report_bytes equal audit_report.to_canonical_bytes()
```

`FixtureSplitResult` is:

```text
non-promotable
not written
not published
not clinical evidence
not research evidence
not a real split artifact
```

Any documentation, docstring or test that presents a `FixtureSplitResult` as a
real split artifact, as evidence, or as publishable output is a contract
violation.

## FD-B2C-10 — Typed errors and validation order

One private base error is authorized:

```text
FixtureFacadeContractError
```

Required stable error categories:

```text
FixtureOnlyModeError
code: fixture_only_mode_error

InvalidFixtureRequestError
code: invalid_fixture_request

FixtureIdentityMismatchError
code: fixture_identity_mismatch

FixtureIntegrationInvariantError
code: fixture_integration_invariant

InvalidExecutionEvidenceReferenceError
code: invalid_execution_evidence_reference
```

B1, B2A and B2B typed exceptions must **not** be silently translated into
generic facade errors. A `SplitInputError`, `SplitAllocationError`,
`CanonicalContractError` subclass or `LeakageContractError` subclass raised by
an accepted module propagates as itself, so the failing contract remains
attributable to the layer that owns it.

Facade-specific validation order must be deterministic:

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

A value violating several rules always fails at the earliest applicable step.

Error messages must contain no:

```text
raw question text
raw context text
answer text
local path
username
hostname
environment value
timestamp
runtime duration
command
PID
```

## FD-B2C-11 — Side-effect and authority prohibition

The future implementation must perform none of:

```text
filesystem read
filesystem write
network access
database access
subprocess execution
environment access
clock access
locale access
timezone access
logging
telemetry
cache access
global mutable state
randomness
temporary-file creation
artifact publication
workflow dispatch
```

It must add no:

```text
public export
CLI
entry-point registration
capability token
authentication mechanism
path-safety layer
overwrite handling
concurrency handling
```

The last four are unnecessary **because B2C has no paths and performs no
writes**. Adding them would create the very surface this increment excludes.

B2C does not authorize:

```text
B2D qualification
P01-04C
P01-04D
P01-04E
P01-04F
P01-04G
real P01-03G membership
real split generation
real leakage audit
dataset/model access
B0/B1 execution
inference
retrieval
metrics
benchmarks
training
fine-tuning
publication
clinical use
```

## FD-B2C-12 — Activation and sequencing

The B2C implementation authority is **not active** merely because this package
is committed or published.

Activation requires all five:

```text
1. genuinely independent clean-room exact-head review of this authorization
   package
2. separate Founder Ready decision
3. separate Founder Merge decision
4. merge into canonical main
5. mechanical post-merge verification
```

```text
No subset activates P01-04B2C implementation authority.
```

Local commit creation activates nothing. Draft creation activates nothing.
Review approval alone, Ready alone, merge alone, review plus merge, and merge
without mechanical verification are each insufficient.

### Before activation

```text
FD-B2C-1 through FD-B2C-12:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
RECORDED BUT INACTIVE

P01-04B2C implementation:
NOT AUTHORIZED TO BEGIN
```

### After valid activation

```text
P01-04B2C implementation authority:
ACTIVE FOR ONE BOUNDED IMPLEMENTATION ONLY

Exact future implementation scope:
src/medscale/mesc/_fixture_split_v1.py
tests/test_mesc_fixture_split_v1.py
```

The authority is **spent** after one implementation commit series is accepted
for publication. It does not authorize a second attempt, a correction series,
or a follow-up expansion.

**Implementation does not equal acceptance.** After implementation, B2C still
requires:

```text
independent exact-head implementation review
exact-head CI and CodeQL
separate Ready decision
separate Merge decision
post-merge mechanical verification
separate implementation-acceptance disposition
canonical adoption of that disposition
```

B2D remains unauthorized until B2C is canonically accepted.

## Continuing prohibitions

Before and after canonical adoption, `FD-B2C-1` through `FD-B2C-12` do not
authorize:

```text
P01-04B2D or its three 1,000-row fixtures
P01-04C through P01-04G
P01-04B whole-phase acceptance
acceptance of the future B2C implementation
a second B2C implementation attempt
real split generation
a real or canonical leakage audit
leakage-audit orchestration over a collection
dataset scanning or registry scanning
record-pair enumeration or automatic finding discovery
CLI or filesystem publication
P01-03G or real dataset access
B0 or B1 execution
model access
inference
retrieval
metrics or benchmark execution
training or fine-tuning
publication
clinical use
any workflow dispatch, rerun or cancellation
modification of any prior governance package
modification of any accepted B1, B2A or B2B module
a second commit on this package
amendment, rebase, squash, reset, cherry-pick or force-push
marking this package's pull request Ready
merging this package
auto-merge
deleting any branch
```

## Standing status

P01-04B remains incomplete and not accepted. P01-04B2D remains unauthorized. No
execution authority of any kind is created by this authorization.
