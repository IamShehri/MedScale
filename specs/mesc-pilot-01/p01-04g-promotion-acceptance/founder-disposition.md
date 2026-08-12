# P01-04G Repository Promotion — Acceptance Disposition

This is the controlling document of the P01-04G promotion-acceptance package.
It records the founder acceptance disposition after the accepted P01-04F frozen
artifact set was promoted byte-for-byte into the canonical repository, the
promotable-artifact scan passed, and all six P01-04G criteria were satisfied.
On any conflict with the other documents in this package, this document
controls.

## 1. Decision identity

```text
Decision:
P01-04G REPOSITORY PROMOTION — ACCEPTED

Decision class:
STAGE ACCEPTANCE AND FINAL P01-04 CLOSEOUT
```

## 2. Substantive disposition

```text
P01-04D:
ACCEPTED / CLOSED

P01-04E:
ACCEPTED / CLOSED

P01-04F:
ACCEPTED / CLOSED

P01-04G:
ACCEPTED / CLOSED

P01-04:
COMPLETE / CLOSED

P01-05:
NOT STARTED / NOT AUTHORIZED
```

## 3. Promotion summary

The nine accepted P01-04F frozen artifacts were promoted byte-for-byte into
`specs/mesc-pilot-01/p01-04/`. Each promoted file was verified to have the
exact frozen SHA-256 and byte size. The promotable-artifact scan found zero
runtime metadata, zero local paths, and zero raw scientific content in any
promoted artifact.

The frozen root remains immutable at stable identity
`mesc-p01-04f-frozen-root/1:sha256:5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290`.

## 4. Scope and non-authority

This disposition accepts and closes P01-04G and completes P01-04. It does not
authorize P01-05 or any later Pilot-01 phase. It does not authorize model
execution, training, fine-tuning, split regeneration, leakage audit rerun,
freeze rerun, source-data modification, or scientific content modification.

```text
P01-05:
NOT STARTED / NOT AUTHORIZED
```

No frozen artifact bytes, external evidence bytes, absolute paths, timestamps,
hostnames, usernames, or raw scientific content are persisted by this
governance package beyond the already-promoted frozen artifacts themselves.