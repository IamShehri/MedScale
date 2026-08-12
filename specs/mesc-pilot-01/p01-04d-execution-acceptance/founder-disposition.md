# P01-04D Formal Split Execution — Acceptance Disposition

This is the controlling document of the P01-04D execution-acceptance package. It
records the founder acceptance disposition for the completed P01-04D formal
split execution. On any conflict with the other documents in this package, this
document controls.

## 1. Decision identity

```text
Decision:
P01-04D FORMAL SPLIT EXECUTION — ACCEPTED

Decision class:
STAGE ACCEPTANCE AND CLOSEOUT — NO NEW EXECUTION AUTHORITY

Execution canonical main:
d76d35664af4ae9e7fd567ffb44dbc624e7036fe

Authoritative result:
Episode #2
```

The execution itself was performed under the superseding execution authorization
recorded in
[`../p01-04d-execution-authorization-supersession/founder-authorization.md`](../p01-04d-execution-authorization-supersession/founder-authorization.md),
whose activation conditions — `MODEL A′` post-merge activation verification and
the Episode #1 custody reconciliation — both returned PASS before any mutation.

## 2. Substantive disposition

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

All ten canonical P01-04D acceptance criteria recorded in
[`../p01-04/acceptance.md`](../p01-04/acceptance.md) are SATISFIED. The
criterion-by-criterion mapping is in
[`acceptance-verification.md`](acceptance-verification.md).

## 3. Bound acceptance identities

```text
execution canonical main:
d76d35664af4ae9e7fd567ffb44dbc624e7036fe

Episode #2 episode identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

Episode #2 terminal manifest identity:
b1c377f8886f1b5aa9c6c1589a9da654152e3aff6bfbdf3f2f180d283b8c0e3b

Episode #2 terminal manifest byte_size:
1247

Episode #2 terminal disposition:
EPISODE_COMPLETE_EQUAL

execution-input manifest:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004
820

accepted source-record identity:
22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
2770193

authoritative split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

canonical compare disposition:
EQUAL_VERIFIED
```

Every identity above is a digest or a byte size. No absolute path, no workspace
location, no evidence-root location, no timestamp, no process identifier, no
hostname and no username is recorded by this package.

Terminal identity is the full 64-character lowercase SHA-256 of the exact
terminal-manifest bytes together with the byte size of those same bytes. Any
truncated recital of it is therefore detectably not the identity.

## 4. Scope of the acceptance

P01-04D establishes a deterministic, formally verified, independently reproduced
split. That is the entire scope of this acceptance.

```text
this disposition establishes:
a deterministic formally verified split
byte-identical independent reproduction
an authoritative split fingerprint
a sealed terminal execution evidence episode
```

```text
this disposition does NOT establish:
model quality
clinical validity
benchmark superiority
training effectiveness
P01-04E acceptance
```

Accepting a split-generation stage is not a scientific result about any model.
No inference, benchmark, training, fine-tuning or clinical claim is supported by
this record.

## 5. Episode #1 — historical failed attempt

```text
Episode #1 episode identity:
86dde167ce6a6c66d1792e4a84bf36627a090955e1cf27b2514e17c14a34c11d

Episode #1 terminal manifest identity:
66fc12b6f6e372448b68cd0eee104be589d78eb3011f112f2b9e07fceaf758a4

Episode #1 terminal manifest byte_size:
706

Episode #1 terminal disposition:
EPISODE_FAILED
```

```text
status:
HISTORICAL FAILED ATTEMPT
EPISODE_FAILED
IMMUTABLE
SUPERSEDED BY SUCCESSFUL FRESH EPISODE #2 FOR P01-04D RESULT PURPOSES
```

Episode #1 is neither hidden nor erased. It failed closed on an input-schema
refusal under the pre-correction executor, the refusal was preserved rather than
repaired, the defect was corrected under a separate reviewed and adopted
correction, and a completely fresh episode was executed. That sequence
strengthens the audit history: the fail-closed behaviour is demonstrated by
preserved evidence rather than asserted.

No Episode #1 byte was edited, normalized, renamed, re-sealed, re-finalized,
repaired, moved or deleted by this package.

## 6. Durable external custody

```text
durable founder-controlled external custody:
ESTABLISHED

Episode #1:
DURABLY PRESERVED — byte-preserving archival copy, complete three-record
inventory, every record verified byte-identical to the original

Episode #2:
DURABLY PRESERVED — byte-preserving archival copy, complete six-record
inventory, every record verified byte-identical to the original
```

Custody is bound by identity, not by location, consistent with
[`../p01-04d-source-record-custody/founder-authorization.md`](../p01-04d-source-record-custody/founder-authorization.md)
§6. No absolute custody path is persisted here, and no physical copy is
designated canonical by this record.

An archival copy preserves bytes. It does not reproduce
`episode_path_identity`, which binds a manifest to the directory object it was
sealed in. An archival copy is therefore durable evidence of the exact episode
bytes and is not a relocated canonical episode; the originally sealed episode
directory remains the one that satisfies the `episode_path_identity` check.

## 7. What this disposition does not authorize

```text
P01-04E:
NOT STARTED
NOT AUTHORIZED BY THIS PACKAGE

P01-04F:
NOT AUTHORIZED

P01-04G:
NOT AUTHORIZED

a further P01-04D execution episode:
NOT AUTHORIZED

re-execution, repair or amendment of Episode #1 or Episode #2:
PROHIBITED

model execution:
NOT AUTHORIZED

training:
NOT AUTHORIZED

fine-tuning:
NOT AUTHORIZED

P01-05:
NOT UNLOCKED
```

The superseding execution authorization permitted exactly one fresh episode. It
is spent. Nothing in this package revives it or creates a new one.

## 8. Scope and non-authority

```text
records a stage acceptance disposition only
creates no execution authority
creates no implementation authority
grants no new input access
creates no generation workspace
generates no artifact
executes no leakage analysis
publishes no dataset
unlocks no later stage
```

This decision amends no earlier founder decision. It does not alter
`FD-DREADY-1` through `FD-DREADY-12`, the formal operator contract, the
seven-file candidate artifact inventory, the artifact-name supersession map, the
P01-04D/E/F/G stage separation, or the ratified scientific decisions D1 through
D10. On any conflict, D1 through D10 control.
