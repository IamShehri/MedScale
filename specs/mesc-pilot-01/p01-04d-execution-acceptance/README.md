# P01-04D Execution Acceptance

Governance-only package recording the founder acceptance disposition for the
completed P01-04D formal split execution, and the durable-custody status of both
execution episodes.

```text
P01-04D:
ACCEPTED

FORMAL SPLIT GENERATION:
COMPLETE

AUTHORITATIVE RESULT:
Episode #2

AUTHORITATIVE SPLIT FINGERPRINT:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91
```

## Documents

| Document | Role |
|----------|------|
| [`founder-disposition.md`](founder-disposition.md) | Controlling acceptance decision, bound identities, scope and prohibition boundary |
| [`acceptance-verification.md`](acceptance-verification.md) | Read-only verification evidence and the ten-criterion acceptance mapping |

`founder-disposition.md` controls on any conflict.

## What this package is

It records a stage acceptance. It contains identities and dispositions only: no
execution artifact bytes, no external evidence files, no absolute custody path,
no workspace location, no timestamp, no process identifier, no hostname and no
username.

It changes nothing under `src/`, `tests/` or `scripts/`.

## Execution context

The execution was performed under the superseding execution authorization in
[`../p01-04d-execution-authorization-supersession/founder-authorization.md`](../p01-04d-execution-authorization-supersession/founder-authorization.md),
at canonical main `d76d35664af4ae9e7fd567ffb44dbc624e7036fe`, after its two
activation conditions — `MODEL A′` post-merge activation verification and the
Episode #1 custody reconciliation — both returned PASS. That authorization
permitted exactly one fresh episode and is now spent.

The canonical acceptance criteria are the ten recorded under **P01-04D — Formal
Split Generation** in [`../p01-04/acceptance.md`](../p01-04/acceptance.md). They
were not modified after the result was known.

## Two episodes

```text
Episode #1:
HISTORICAL FAILED ATTEMPT — EPISODE_FAILED — IMMUTABLE
SUPERSEDED BY EPISODE #2 FOR P01-04D RESULT PURPOSES
DURABLY PRESERVED

Episode #2:
EPISODE_COMPLETE_EQUAL — the authoritative result
DURABLY PRESERVED
```

Episode #1 is preserved rather than hidden. It failed closed, its refusal was
never repaired, the underlying defect was corrected under separate review and
adoption, and a completely fresh episode was then executed.

## What this package does not do

```text
P01-04E:
NOT STARTED — NOT AUTHORIZED BY THIS PACKAGE

P01-04F and P01-04G:
NOT AUTHORIZED

a further P01-04D episode:
NOT AUTHORIZED

model execution, training, fine-tuning:
NOT AUTHORIZED

P01-05:
NOT UNLOCKED
```

P01-04D establishes a deterministic, formally verified, independently reproduced
split. It establishes nothing about model quality, clinical validity, benchmark
performance or training effectiveness.
