# MESC Pilot-01 -- P01-03A Acquisition Protocol

Freeze date: 2026-07-17

## Future P01-03B stages

```text
EXAMPLE ONLY -- NOT AUTHORIZED FOR EXECUTION
```

This document describes a planned future acquisition procedure. It is not an executable instruction. It may not be executed without separate founder authorization and a subsequent failed-closed review of every parameter.

### Stage 1 -- Preflight

1. Verify that founder authorization has been recorded for `P01-03B IMMUTABLE ARTIFACT ACQUISITION ONLY`.
2. Verify that the approved storage root exists outside every Git worktree, repository root, and synchronized cloud directory.
3. Verify that the approved revision-specific directory is empty or does not yet exist.
4. Verify that the authorized dataset identity matches `qiaojin/PubMedQA`, configuration `pqa_labeled`, revision `9001f2853fb87cab8d220904e0de81ac6973b318`.
5. Verify that `trust_remote_code` remains false and prohibited.
6. Verify that no loading mechanism executes remote Python code.

### Stage 2 -- Revision verification

1. Retrieve only repository metadata required to confirm the immutable revision.
2. Abort if the remote revision does not exactly match `9001f2853fb87cab8d220904e0de81ac6973b318`.
3. Abort if repository metadata has changed in a way that alters rights notices, licenses, or loading requirements.

### Stage 3 -- Artifact allowlist verification

1. Retrieve exact remote artifact filenames for `pqa_labeled` only.
2. Compare filenames against the verified allowlist.
3. Abort if any file is not on the allowlist.
4. Abort if artifact count or categories contradict committed authority.

### Stage 4 -- Acquisition boundary

1. Download only files on the verified allowlist into the revision-specific directory.
2. Reject any path resolution that would place files under a Git worktree, repository root, or synchronized cloud directory.
3. Reject any file that requires `trust_remote_code` or executes remote Python code.
4. Stop immediately on partial download, duplicate artifact, or unexpected file.
5. Perform no transformation, no Parquet opening, no schema inspection, and no content interpretation beyond digest verification.

### Stage 5 -- Digest generation

1. Compute SHA-256 for every acquired file.
2. Record artifact identity, size, digest, acquisition timestamp, tool version, and environment identity.
3. Abort on any hash failure.

### Stage 6 -- Manifest generation

Generate a repository-safe manifest containing only portable scientific identity and content digests. Record a separate local full manifest containing machine-specific operational provenance outside Git.

### Stage 7 -- Post-acquisition stop

1. Halt after artifact acquisition and manifest recording.
2. Do not open Parquet files.
3. Do not normalize, transform, annotate, validate, or infer.
4. Return control for a separate governance decision on later stages.

### Non-goals

* no Parquet schema interpretation
* no dataset transformation
* no annotation or label generation
* no inference, retrieval, or baseline execution
* no model download
* no training
* no release or publication
* no integration with production or clinical systems
