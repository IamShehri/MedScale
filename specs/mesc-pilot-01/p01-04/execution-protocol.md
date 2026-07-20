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

Input identities must be verified against recorded SHA-256 digests before every formal operation. Any input mismatch stops execution.

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
