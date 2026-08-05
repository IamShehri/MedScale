# MESC Pilot-01 — P01-04 Execution Protocol

Status: **specification and policy only — no execution authorized**

This document defines the execution-safety protocol for P01-04 formal split generation and leakage audit. Nothing herein authorizes execution. Implementation of this protocol requires separate founder authorization for P01-04B.

---

## Authorization hierarchy

| Gate | Required authorization |
|------|----------------------|
| Split generation (P01-04D) | Founder authorization for P01-04D after P01-04B and P01-04C acceptance |
| Leakage audit (P01-04E) | Founder authorization for P01-04E after P01-04D acceptance |
| Freeze (P01-04F) | Founder authorization for P01-04F |
| Repository promotion (P01-04G) | Separate promotion authorization |

Earlier-stage authorization does not automatically authorize a later stage.

## Isolated paths

P01-04 execution must occur in an isolated writable workspace separate from the canonical repository checkout. The canonical repository checkout must remain read-only and frozen during generation.

Workspace convention:

- canonical repository: read-only, detached at canonical main commit
- generation workspace: writable, separate directory, distinct from repository root
- evidence root: writable, receives outputs only after freeze
- no generator or validator writes directly into the evidence root during generation

## Accepted inputs

Formal generation accepts only:

- `specs/mesc-pilot-01/p01-03g/ordered-example-id-registry.jsonl`
- `specs/mesc-pilot-01/p01-03g/source-document-id-registry.jsonl`
- `specs/mesc-pilot-01/p01-03g/transformed-dataset-identity.json`
- `specs/mesc-pilot-01/p01-04/decision-record.md`
- the accepted external `source-records.jsonl`, read-only and outside the repository,
  solely as the per-example `final_decision` label source

Input identities must be verified against recorded SHA-256 digests before every formal operation. Any input mismatch stops execution.

Before the external `source-records.jsonl` is read, its identity must equal both
attested values from the accepted P01-03G transformed-dataset identity:

- SHA-256: `22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce`
- byte size: `2770193`

The external file must not be copied into the repository. P01-04 may retain only
the identity fields and `final_decision` needed for the fail-closed label join;
question, context, answer, and annotation content must not appear in split outputs.

## Independent generations

Formal split generation must be executed twice independently:

- **Generation A**: first workspace, first process
- **Generation B**: second workspace, second process

Generations must use identical:

- input artifacts (byte-identical)
- algorithm implementation (same code version)
- serialization settings (UTF-8, sort_keys, separators)
- ranking key schema
- apportionment algorithm

Generations must be executed without knowledge of each other's outputs. Comparison occurs only after both finish.

## Finalization

Complete byte equality between Generation A and Generation B outputs is required before any output is treated as final. Byte equality is tested on every promoted artifact.

If byte equality fails:

- both candidates are invalidated;
- both generation work directories are preserved unchanged;
- a root-cause analysis is recorded externally;
- a new generation is required after the issue is resolved.

No in-place repair is permitted after generation.

## Anti-writeback controls

The following writes are prohibited during formal generation:

- writing into the frozen P01-03G artifact directory;
- writing into the canonical repository checkout;
- writing directly into the final evidence root from a generator or validator;
- modifying an artifact after it has been written to the generation workspace;
- overwriting an invalidated candidate without preserving the prior state;
- silent suppression of findings or metrics.

Writes must be:

- append-only within the generation workspace;
- isolated per generation;
- verified against writable-path safety before each write.

## Stop conditions

Stop formal generation immediately if:

- canonical main has moved from the expected commit;
- input artifacts do not match recorded SHA-256 digests;
- a generator or validator attempts to write outside its designated workspace;
- Generation A and Generation B outputs are not byte-identical;
- leakage findings are suppressed or silently discarded;
- the output contains runtime metadata, local paths, usernames, hostnames, or timestamps;
- the split hash cannot be recomputed to the same value from the canonical manifest;
- any required acceptance metric returns `not_applicable` without a recorded reason;
- a checkpoint fails validation after any write.

## Invalidation rules

An invalidated candidate:

- is never overwritten;
- is never deleted;
- is never modified in place;
- is preserved with its original generation workspace identity;
- causes a new candidate identity to be generated;
- is referenced in the execution record with its invalidation reason.

A new candidate requires:

- a new generation workspace;
- new Generation A and Generation B executions;
- new byte-equality verification.

## Required reporting

Every formal execution must produce external evidence (outside the repository and outside the evidence root):

- complete command lines used for Generation A and Generation B;
- process IDs, start timestamps, end timestamps, exit codes;
- input artifact SHA-256 digests at execution time;
- output artifact byte hashes for every promoted artifact;
- Generation A vs Generation B byte-equality result;
- any invalidation events and root-cause analysis;
- freeze timestamp and evidence-root identity;
- verification rerun results.

External evidence must not be committed to the repository. It must be stored in a designated external-evidence location and referenced by stable identity only.

---

## Prospective operator interface

```text
DESIGN RATIFIED / IMPLEMENTATION NOT AUTHORIZED / EXECUTION NOT AUTHORIZED
```

This section records the design ratified by `FD-DREADY-3`, `FD-DREADY-4` and
`FD-DREADY-5` in
[`../p01-04d-entry-readiness-remediation/founder-authorization.md`](../p01-04d-entry-readiness-remediation/founder-authorization.md),
which controls. It resolves readiness blocker **B-1** at the design level.

Design-level resolution is not entry, not implementation authority and not
execution authority. Nothing in this section is a runnable command, and no
real input path, workspace path or evidence path is recorded here.

### Supported operator surface

```text
script:
scripts/mesc_p01_04d_operator.py

commands:
generate
compare

command count:
2
```

**Historical as of the remediation-design baseline.** The script does not exist
at this baseline. When it exists, it is a canonical repository-controlled
script, never an improvised or one-off script, and it is not exported from
`medscale.mesc`, not registered as a `medscale` CLI subcommand, not installed as
a public console script and not callable through an environment-variable
activation switch. No third command exists on this surface.

**Current truth.** The sentence `The script does not exist at this baseline.`
describes the remediation-design baseline and is preserved for it. The script
now exists on canonical main. Its implementation code was adopted by PR #90, and
PR #91 reconciled the canonical implementation truth; see
[`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md).
Every property described in the paragraph above holds of the adopted script: it
is canonical and repository-controlled, unexported, unregistered, not installed
as a console script, not environment-activated, and it carries no third command.

Entry is now authorized under the founder decision recorded in
[`../p01-04d-entry-authorization/founder-authorization.md`](../p01-04d-entry-authorization/founder-authorization.md).
Execution remains unauthorized. No protected input has been opened, and no
Generation A or Generation B has occurred. The invocation parameters, validation
order, artifact inventory, stage separation and execution semantics recorded in
this protocol are unchanged by this note.

Formal execution uses a separate private formal-execution component. It does not
reuse the fixture-only execution authority of `FixtureSplitFacade` or
`_fixture_publication_v1`, which remain private, fixture-only, synthetic-only,
non-evidence, unexported and unchanged.

### `generate`

Executes exactly one generation per process. Generation identity is exactly `A`
or `B`. One invocation never executes both generations.

Each invocation requires explicit, safely parameterized operator inputs for:

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

The operator rejects, fail-closed and before any mutation:

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

### `compare`

Runs only after Generation A and Generation B have terminated.

It shall:

```text
read completed A and B inventories
verify exact expected inventory
compare every D artifact byte-for-byte
recompute the authoritative split fingerprint
verify all descriptors and manifests
record the equality disposition externally
```

It shall not:

```text
repair an artifact
rewrite a generation workspace
copy one generation over the other
suppress an inequality
promote to the final evidence root
perform P01-04E leakage execution
```

Any inequality invalidates both candidates. The invalidation rules recorded
above apply unchanged: an invalidated candidate is never overwritten, never
deleted and never modified in place.

### Exact seven-file A/B comparison requirements

The expected inventory of each generation workspace is exactly these seven
P01-04D candidate artifacts, and nothing else:

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

Comparison requirements:

1. Each workspace inventory is derived from the workspace itself and must equal
   the exact seven filenames above — no missing file, no eighth artifact.
2. No log, receipt, lock, marker, PID file, timestamp file or sidecar is part of
   the deterministic generation bundle or of the comparison.
3. All seven files are compared **byte-for-byte** between Generation A and
   Generation B. Byte equality is required for all seven, not a subset.
4. The authoritative full lowercase 64-hex `split_fingerprint` is recomputed and
   must match the value carried in `split-summary.json` and in
   `generation-manifest.json`. The 16-hex `split_hash` is
   compatibility/display-only and is never the authoritative value. Under the
   `FD-DREADY-7` supersession map, `split-fingerprint.json` maps to
   **no standalone file**:

```text
standalone fingerprint file:
none
```
5. All descriptors and manifests are verified. `generation-manifest.json` must
   be non-circular and must carry no generation identity, workspace path,
   process ID, timestamp, hostname, username, command line or external-evidence
   path, so Generation A and Generation B produce identical manifest bytes when
   all scientific inputs and code are identical.
6. The equality disposition is recorded externally. It is never recorded by
   mutating a generation workspace.
7. Any inequality in any of the seven files invalidates both candidates. No
   repair, rewrite, copy, suppression or promotion is permitted.

### Stage boundary

```text
P01-04D   formal split generation candidate bundle
P01-04E   canonical leakage audit and finding resolution — leakage-audit.json
P01-04F   freeze, independent verification and closeout record —
          p01-04-closeout-record.json
P01-04G   separately authorized repository promotion
```

`publication-manifest.json` is the existing fixture-only publication artifact and
is not the formal P01-04D generation manifest. The formal P01-04D
candidate-bundle manifest is `generation-manifest.json`. `compare` never performs
P01-04E leakage execution.

```text
P01-04D entry:
NOT AUTHORIZED

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```
