# P01-04D Entry-Readiness Remediation — Implementation Contract

```text
Contract status:
PROSPECTIVE ONLY

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

Every path, type and error named in this document:
ABSENT OR UNCHANGED AT THIS BASELINE
```

This document defines the **prospective** future implementation contract for the
controlled formal P01-04D executor. It implements nothing. It authorizes
nothing. It creates no module, no test, no script and no command.

[`founder-authorization.md`](founder-authorization.md) controls. Where this
document is silent, no behaviour is implied; where it would conflict with
`FD-DREADY-1` through `FD-DREADY-12`, the founder authorization controls.

---

## 1. Prospective candidate allowlist

A future implementation authorization, if issued, would be bounded to exactly
these six prospective paths:

```text
src/medscale/mesc/_formal_split_v1.py

src/medscale/mesc/_formal_generation_v1.py

scripts/mesc_p01_04d_operator.py

tests/test_mesc_formal_split_v1.py

tests/test_mesc_formal_generation_v1.py

tests/test_mesc_p01_04d_operator.py
```

Exactly six prospective paths. No seventh path.

These paths are prospective only and remain absent or unchanged in this task.
None of them exists at canonical baseline
`78bab082bde3b53cbdbd5f37109437b68ba2e5c5`, and this package creates none of
them.

## 2. Protected existing paths

A future implementation must leave the accepted fixture-only surface
byte-identical:

```text
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_fixture_split_v1.py
src/medscale/mesc/_fixture_publication_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
pyproject.toml
uv.lock
every prior governance package
```

Per `FD-DREADY-2`, `FixtureSplitFacade` and `_fixture_publication_v1` retain no
role in formal execution. They remain private, fixture-only, synthetic-only,
non-evidence, unexported and unchanged.

## 3. Module boundary

```text
src/medscale/mesc/_formal_split_v1.py
src/medscale/mesc/_formal_generation_v1.py
```

Both future modules are private by leading underscore. Neither is exported from
`medscale.mesc`. Neither is registered as a `medscale` CLI subcommand. Neither is
installed as a public console script. Neither is reachable through an
environment-variable activation switch.

The only supported operator interface is `scripts/mesc_p01_04d_operator.py`.

## 4. Operator surface

```text
script:
scripts/mesc_p01_04d_operator.py

commands:
generate
compare

command count:
2
```

No third command exists on this surface.

### 4.1 `generate`

Executes exactly one generation per process. Generation identity is exactly `A`
or `B`. One invocation never executes both generations.

Required explicit, safely parameterized operator inputs:

```text
expected canonical commit
read-only repository root
generation identity
fresh generation workspace
external evidence root
future evidence root
ordered-example registry
source-document registry
transformed-dataset identity
external source-records label source
ratified decision record
exact Python version
```

Required fail-closed rejections, evaluated before any mutation:

```text
workspace reuse
repository-root output
P01-03G output
future-evidence-root output
relative or unresolved protected-root aliases
unknown generation identity
missing expected commit
canonical commit movement
```

### 4.2 `compare`

Runs only after Generation A and Generation B have terminated.

Required behaviour:

```text
read completed A and B inventories
verify exact expected inventory
compare every D artifact byte-for-byte
recompute the authoritative split fingerprint
verify all descriptors and manifests
record the equality disposition externally
```

Prohibited behaviour:

```text
repair an artifact
rewrite a generation workspace
copy one generation over the other
suppress an inequality
promote to the final evidence root
perform P01-04E leakage execution
```

Any inequality invalidates both candidates.

## 5. Exact generation inventory

Each Generation A and Generation B workspace contains exactly seven P01-04D
candidate artifacts:

```text
split-policy.json
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
generation-manifest.json
```

```text
P01-04D artifact count:
7
```

No eighth artifact. No log, receipt, lock, marker, PID file, timestamp file or
sidecar belongs to the deterministic generation bundle. All seven files are
compared byte-for-byte between Generation A and Generation B.

## 6. Supersession map

```text
example-split-registry.jsonl       ->  example-registry.jsonl
excluded-or-unassigned-ledger.json ->  excluded-ledger.json
split-fingerprint.json             ->  no standalone file
```

```text
standalone fingerprint file:
none
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through `split-summary.json` and `generation-manifest.json`. The 16-hex
`split_hash` is compatibility/display-only.

## 7. Stage-separated filenames

```text
leakage-audit.json            P01-04E output
p01-04-closeout-record.json   P01-04F output
publication-manifest.json     existing fixture-only publication artifact
generation-manifest.json      formal P01-04D candidate-bundle manifest
```

None of `leakage-audit-report.json`, `leakage-audit.json`,
`p01-04-closeout-record.json` or `publication-manifest.json` is a P01-04D
generation output.

## 8. Required future types

The following types are defined **conceptually**. No Python is written here, no
field list is frozen as an implementation signature, and no runtime behaviour is
invented beyond `FD-DREADY-1` through `FD-DREADY-12`.

### `FormalSplitInputIdentity`

The verified identity of the formal scientific inputs: the ordered-example
registry, the source-document registry, the transformed-dataset identity, the
ratified decision record and the external source-records label source, each
bound by digest and byte size. It carries identity only — never content, never
labels, never membership, never a local path.

### `FormalSplitRequest`

One immutable, fully validated request for exactly one generation. It binds the
expected canonical commit, the generation identity `A` or `B`, the verified
`FormalSplitInputIdentity`, the resolved fresh generation workspace, the
read-only repository root, the protected roots that must never receive output,
and the exact Python version. It is complete and verified before any mutation.

### `FormalGenerationResult`

The in-memory outcome of one generation: the exact seven candidate artifact
payloads keyed by filename, their digests and byte sizes, and the authoritative
64-hex split fingerprint. It is produced once and never mutated.

### `FormalGenerationManifest`

The non-circular deterministic manifest described by `FD-DREADY-10`. It binds
schema version, algorithm version, generation-bundle filenames, surface
identifiers, schema versions, SHA-256 digests, byte sizes, the authoritative
split fingerprint and the input identity digests. It carries no generation
identity, no workspace path, no process ID, no timestamp, no hostname, no
username, no command line and no external-evidence path, and it carries neither
its own digest nor its own byte size.

### `FormalComparisonResult`

The outcome of `compare`: the verified inventory of both generations, the
per-filename byte-equality disposition across all seven artifacts, the
recomputed authoritative split fingerprint, the descriptor and manifest
verification disposition, and the overall equality verdict. It records a
disposition; it never repairs, rewrites, copies, suppresses or promotes.

## 9. Required future typed errors

Every failure is typed and fail-closed. The required error identities are:

```text
FormalInputIdentityError
FormalInputSchemaError
FormalLabelJoinError
FormalWorkspaceSafetyError
FormalGenerationError
FormalInventoryError
FormalByteEqualityError
FormalFingerprintError
FormalMetadataError
FormalEvidenceConfigurationError
```

| Error | Raised for |
|---|---|
| `FormalInputIdentityError` | a formal input whose digest or byte size does not match its recorded identity, or a canonical commit that is missing or has moved |
| `FormalInputSchemaError` | a formal input that does not satisfy its declared schema |
| `FormalLabelJoinError` | a label join that is not exact and total under the fail-closed join rules |
| `FormalWorkspaceSafetyError` | workspace reuse, repository-root output, P01-03G output, future-evidence-root output, or a relative or unresolved protected-root alias |
| `FormalGenerationError` | a failure inside one generation, including an unknown generation identity |
| `FormalInventoryError` | a workspace whose contents are not exactly the seven candidate artifacts |
| `FormalByteEqualityError` | any byte inequality between Generation A and Generation B |
| `FormalFingerprintError` | an authoritative split fingerprint that cannot be recomputed to the same 64-hex value |
| `FormalMetadataError` | prohibited runtime metadata reaching a deterministic artifact |
| `FormalEvidenceConfigurationError` | an evidence-root configuration that would allow a generator or validator to write into the final evidence root |

No error type outside this list is defined by this contract, and no error is
downgraded to a warning, a return code or a suppressed condition.

## 10. Scientific identity

```text
D1 through D10:
UNCHANGED
```

The future implementation reuses the ratified partition set, the exact
700 / 150 / 150 totals, `source_document_id` grouping, `decision`
stratification, constrained integer apportionment, deterministic SHA-256
ranking, the ratified minimum sizes, the no-holdout policy, the public
repository content boundary and the split-version policy. It amends none of
them.

## 11. Future qualification boundary

Per `FD-DREADY-11`, a later implementation authorization may permit only
**synthetic** construction and qualification of the controlled formal executor.

```text
implementation authorization:
SEPARATE FROM REAL EXECUTION AUTHORIZATION

future implementation access to P01-03G registry content:
PROHIBITED

future implementation access to external source-records.jsonl:
PROHIBITED

future implementation access to real labels:
PROHIBITED

future implementation access to real membership:
PROHIBITED
```

The future implementation package must use synthetic formal-input fixtures that
exercise the same schemas and the same fail-closed paths.

## 12. Continuing non-authority

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-04D entry:
NOT AUTHORIZED

P01-03G registry access:
NOT AUTHORIZED

External source-record access:
NOT AUTHORIZED

Real dataset access:
NOT AUTHORIZED

Real split generation:
NOT AUTHORIZED

Real partition membership:
NOT AUTHORIZED

Canonical leakage execution:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

This contract is a design record. It does not begin, schedule, stage or activate
any implementation.
