# P01-04B2A Evidence Production Gate — Prospective Dispatch Brief

```text
THIS BRIEF IS NOT EXECUTABLE.
IT BECOMES EXECUTABLE ONLY AFTER ALL FIVE FD-PV-18 ACTIVATION CONDITIONS ARE
SATISFIED AND MECHANICALLY VERIFIED. RECORDING IT IN A DRAFT PULL REQUEST
ACTIVATES NOTHING.
```

Canonical authority: [`founder-disposition.md`](founder-disposition.md).

## Step 0 — resolve the activated canonical SHA

Do not proceed on a guessed or remembered value.

```bash
git fetch origin
git rev-parse origin/main
git show -s --format='%H%n%T%n%P%n%s' origin/main
```

Verify the merge object's ordered parents, tree, subject, and path scope, then
bind:

```text
ACTIVATED_SHA = the verified canonical-main SHA created by merging this package
```

`ACTIVATED_SHA` is **not** `69f16455eb7ffb33f019dfe1f885cbb1cc8fc6a3`. Stop if
`origin/main` is not the merge of this package, or if the merge introduces any
path outside the five authorized documentation paths.

## Step 1 — the single authorized dispatch

```text
Workflow:  .github/workflows/mesc-b2a-portability.yml
Ref:       main
Event:     workflow_dispatch
Input:     expected_sha = ACTIVATED_SHA
Attempts:  exactly one
```

The authority is consumed when GitHub accepts the request, regardless of
outcome. Do not retry, rerun, cancel-and-reissue, or dispatch a replacement run.
A failed, cancelled, timed-out, or malformed run requires a new founder
decision.

## Step 2 — required run properties

```text
event:          workflow_dispatch
run_attempt:    1
head_branch:    main
head_sha:       ACTIVATED_SHA
expected_sha:   exactly equal to head_sha
```

All six matrix jobs must succeed:

```text
linux-py3.11    linux-py3.12
macos-py3.11    macos-py3.12
windows-py3.11  windows-py3.12
```

Aggregate verification must succeed. Both dispatch-guard copies must execute and
pass. The pull-request aggregation step must be **skipped**. The dispatch
aggregation step must **execute**. The evidence upload step must execute
**exactly once**.

## Step 3 — required artifact inventory

```text
b2a-portability-linux-py3.11
b2a-portability-linux-py3.12
b2a-portability-macos-py3.11
b2a-portability-macos-py3.12
b2a-portability-windows-py3.11
b2a-portability-windows-py3.12
b2a-portability-evidence
```

```text
7 total artifacts
6 cell artifacts
1 evidence artifact
0 duplicates
0 unexpected artifacts
0 expired artifacts at inspection time
```

## Step 4 — required envelope properties

```text
schema:         mesc-pilot-01-b2a-portability-evidence/1
result:         pass
canonical_sha:  exactly ACTIVATED_SHA
```

The envelope must identify all six ratified cells and the exact canonical file
set — `canonical.json`, `canonical.jsonl`, `manifest.json` — with their byte
sizes and SHA-256 digests.

## Step 5 — required content boundary

The evidence and cell outputs must remain synthetic and must contain no real
dataset content, model weights, inference outputs, patient data, training
artifacts, runtime-derived timestamps, hostnames, usernames, runner
identifiers, secrets, environment paths, or unratified metadata.

## Step 6 — offline verification only

Download the seven artifacts from that one run and verify them offline. Verify
byte identity across all six cells, recompute every digest from bytes, and
confirm the envelope matches the cells it claims.

Do not dispatch a second run to "confirm" a result, and do not treat any earlier
pull-request artifact as satisfying the canonical-main obligation.

## Step 7 — what happens next

```text
Successful evidence production does not itself accept B2A.
```

Required sequence, in order:

1. mechanical run and artifact verification;
2. a genuinely independent clean-room evidence review;
3. a separate founder evidence-acceptance decision;
4. only then, if every governing criterion is satisfied — B2A acceptance, the
   binding `N-12` disposition, closure of the Windows and macOS obligations, and
   consideration of B2B authorization.

This brief authorizes step 1 only.

## Preservation

The dispatch must run the adopted workflow unmodified. Preserve
`permissions: contents: read` and `actions: read`; the six-cell matrix and the
six ratified artifact names; the four `FD-PV-6` limits and their axes; bounded
limit-plus-one transport; producer and consumer status checks; partial-file
cleanup; declared-versus-actual verification; bounded network-free ZIP
inspection and extraction; every archive-safety protection; the `FD-PV-14`
canonical-SHA rules; schema `mesc-pilot-01-b2a-portability-evidence/1`; every
immutable action pin; exactly twenty-one taxonomy categories; and the two
settled mappings:

```text
expired expected artifact:              missing_matrix_cell
post-validation archive-count mismatch: aggregate_verifier_internal_error
```

## Prohibited throughout

No `.github/**`, `tests/**`, `src/**`, `pyproject.toml`, `uv.lock`, dataset,
model, contract, serializer, or public-API change. No second dispatch, rerun, or
replacement run. No evidence acceptance, B2A acceptance, `N-12` discharge,
platform closure, or B2B authorization. No real Pilot-01 split, B0, model
access, dataset access, inference, retrieval, training, fine-tuning,
publication, or clinical use. No direct push to `main`, no force-push, no branch
deletion, and no rewriting of historical governance records.
