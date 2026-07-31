# Canonical Main Incident Record — 2026-07-31

```text
Classification:
CONTAINED TECHNICALLY
GOVERNANCE RECORD REQUIRED
NOT, BY ITSELF, A PR #61 IMPLEMENTATION BLOCKER
```

## What happened

An accidental commit was briefly placed on canonical `main`, and the `main` ref
was then rewound to its previous position through a **non-fast-forward force
update**. This record states that plainly. The rewind was a history rewrite of
the canonical branch, not a normal fast-forward, and it is recorded as such.

## Accidental commit

```text
SHA:
d2c5ecc96b093613bc9b5863720715dba6395227

Parent:
3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9

Tree:
b1de9fc9758c81d62c84224f33ea84ff4094d1ad

Timestamp:
2026-07-31T02:04:27Z

Commit message:
(empty)

Changed path:
dummy

Content:
zero-byte file
```

## Observed sequence

1. `main` moved from `3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9` to
   `d2c5ecc96b093613bc9b5863720715dba6395227`.
2. `main` was restored to `3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9` through a
   **non-fast-forward ref rewind**, because `3a0fd67c…` is the parent of
   `d2c5ecc…` and is therefore behind it.
3. The accidental commit is no longer an ancestor of current `main`.
4. It is not in PR #61 ancestry.
5. `dummy` is absent from current `main`.
6. PR #61's head and tree were not changed.
7. No PR #61 commit was rewritten.

## Containment evidence

Verified mechanically against the live repository and immutable Git objects:

| Check | Result |
|---|---|
| Current canonical `main` | `3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9` |
| Current canonical main tree | `f8c80688c1a31ef06cedad4ce44cc13546a92919` |
| `d2c5ecc…` parent | `3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9` |
| `d2c5ecc…` tree | `b1de9fc9758c81d62c84224f33ea84ff4094d1ad` |
| `d2c5ecc…` files | `dummy`, added, zero bytes |
| `d2c5ecc…` ancestor of current `main`? | **No** |
| `d2c5ecc…` ancestor of PR #61 head? | **No** |
| `dummy` present on current `main`? | **No** |
| PR #61 head | `2260fa540c440ce3584535f30e74323381568b98` — unchanged |
| PR #61 head tree | `eb5cd1757f89bca2b42e1e9c61d3fcd1270a5e94` — unchanged |
| PR #61 commit identities | all seven unchanged; none rewritten |

The accidental commit remains **directly addressable by SHA** on the remote, as
orphaned objects normally do. It is unreachable from any branch. This record
exists so that a future reader who encounters the object, or who notices the
`main` ref history, finds the explanation rather than an unexplained anomaly.

## Effect on the FD-PV-15 activation record

`FD-PV-15` activation condition 5 required mechanical verification of the
canonical merge SHA and the resulting main tree. That verification was performed
against merge commit `3a0fd67c8433bd25eab77c05b44aa84a3a86ddb9`, ordered parents
`f71c6abf2b2f905f605951605efd6c8ab016523e` and
`1e4a701a2359ce0b53cb4ee04429794c364590db`, and main tree
`f8c80688c1a31ef06cedad4ce44cc13546a92919`.

Every one of those object identities is unchanged today. Git objects are
immutable and content-addressed: the incident moved a **ref**, never a commit or
a tree. The verified merge commit and the verified tree are the same objects
they were, and canonical `main` points at that same merge commit now.

The founder records the following determination: the incident **does not
invalidate** the `FD-PV-15` activation record, because no verified object
changed. It does, however, demonstrate that a ref pointing at a verified object
is not by itself a durable guarantee, which is why the preventive controls in
[`founder-disposition.md`](founder-disposition.md) are adopted alongside this
record.

## Classification and consequence

```text
CONTAINED TECHNICALLY
GOVERNANCE RECORD REQUIRED
NOT, BY ITSELF, A PR #61 IMPLEMENTATION BLOCKER
```

The incident is not a defect in PR #61 and does not, on its own, hold PR #61.
PR #61 is held by the four blocking findings in
[`review-findings.md`](review-findings.md), which are independent of this
incident.

The preventive control decision responding to this incident is recorded in
[`founder-disposition.md`](founder-disposition.md) §2. No repository setting is
changed by this record.
