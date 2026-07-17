# MESC Pilot-01 -- P01-03A Acquisition Authorization Readiness Research

Freeze date: 2026-07-17

## Canonical repository snapshot

Canonical main at merge of PR #24:

`561041341827ee1ae496400a32b810960e459437`

This package was created from exact canonical `origin/main`. No branch mutation, rebase, or force-push occurred.

## Frozen dataset identity

Committed P01-03 authority documents pin the primary dataset as:

Repository: `qiaojin/PubMedQA`
Configuration: `pqa_labeled`
Immutable revision: `9001f2853fb87cab8d220904e0de81ac6973b318`
Representation: `Parquet`

## Rights and redistribution boundary

Committed P01-03 documents state:

* raw abstracts must not be committed to Git
* raw abstracts must not be published or redistributed by MedScale
* MIT repository metadata does not transfer publisher copyright in underlying abstracts
* no full article text or PDF is authorized
* no arbitrary Python loading script is authorized
* `trust_remote_code` must remain false and prohibited

These boundaries are unchanged in this package. No contradiction was found in committed authority documents.

## `.gitignore` finding

Committed `.gitignore` at canonical main covers:

* Python bytecode and build outputs
* virtual environments
* tool caches
* docs site build
* OS and editor noise

It does not contain an explicit raw-dataset boundary.

This is recorded as a readiness issue. Acquisition authorization may remain blocked until a separate guardrail implementation PR adds explicit deny-list protection.

## Task-registry finding

Top-level task registry states:

```
P01-T04 -- Acquire PQA-L
Outputs: acquisition authorization record; artifact allowlist; storage boundary confirmation; acquisition manifest; downloaded Parquet artifacts
```

The staged plan separates execution into:

```
P01-03A -- acquisition authorization
P01-03B -- immutable artifact acquisition
```

The task registry combines authorization and execution outputs at a high level. This is acceptable as an aggregate summary, but it does not replace finer-grained governance gates.

Recommendation: `TASK REGISTRY SHOULD LATER BE RECONCILED TO SEPARATE AUTHORIZATION FROM ACQUISITION`

## Storage-boundary inspection

Proposed raw-data root:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\`

Proposed revision-specific directory:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\9001f2853fb87cab8d220904e0de81ac6973b318\pqa_labeled\`

Read-only inspection performed from canonical main worktree provided the following evidence:

* the proposed path does not currently exist
* parent directory `C:\Users\Shehr\MedScaleData` does not currently exist
* home directory `C:\Users\Shehr` contains no `.git` repository
* OneDrive path `C:\Users\Shehr\OneDrive` exists, but proposed `C:\Users\Shehr\MedScaleData` lies outside it
* no junction, symlink, or reparse point can redirect the non-existent path into a tracked location
* Windows path resolution appears normal with no unexpected redirection detected
* filesystem permissions for later local-only research access cannot be verified without creating the directory; current evidence does not block the proposed boundary

Decision: `PROPOSED STORAGE BOUNDARY ACCEPTABLE FOR LATER AUTHORIZATION`

This is evidence for a later decision only. It is not acquisition authorization.

## Unresolved questions

* metadata-only remote inspection authorization was not in scope for this package
* `.gitignore` guardrail implementation is pending a separate PR
* external storage permissions and cleanup policy are not yet confirmed
* Windows filesystem permissions for `C:\\Users\\Shehr\\MedScaleData` are unverified

No remote dataset access was performed. No dataset content was inspected. No row counts, schemas, or hashes were claimed for unacquired files.

## Metadata inspection evidence

Freeze date: 2026-07-17

This section records metadata-only inspection evidence from a separate authorized founder turn.

* API method: `huggingface_hub.HfApi.repo_info` with `files_metadata=True`, `token=False`
* Anonymous access: `token=False`, no stored credentials transmitted
* Exact revision requested: `9001f2853fb87cab8d220904e0de81ac6973b318`
* Exact revision returned: `9001f2853fb87cab8d220904e0de81ac6973b318`
* Repository public: `True`
* Repository configuration names: `pqa_artificial`, `pqa_labeled`, `pqa_unlabeled`
* Tree count: `8`
* `pqa_labeled` paths found: `1` data artifact
* License metadata: `mit`
* File content downloaded: `None`
* Parquet file opened: `None`
* Dataset cache or raw-data directory created: `None`

Remote call was performed only after separate founder authorization in a subsequent turn. This documentation records the resulting contractual metadata only and does not authorize acquisition, transformation, or execution.
