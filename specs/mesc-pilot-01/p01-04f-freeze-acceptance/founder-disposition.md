# P01-04F Freeze — Acceptance Disposition

This is the controlling document of the P01-04F freeze-acceptance package.
It records the founder acceptance disposition after the independent verification
rerun, write-once freeze, and post-freeze verification all passed. On any
conflict with the other documents in this package, this document controls.

## 1. Decision identity

```text
Decision:
P01-04F FREEZE AND INDEPENDENT VERIFICATION — ACCEPTED

Decision class:
STAGE ACCEPTANCE AND CLOSEOUT — NO P01-04G AUTHORITY
```

## 2. Substantive disposition

```text
P01-04F:
ACCEPTED / CLOSED

INDEPENDENT VERIFICATION:
PASS

FORMAL OUTPUTS REPRODUCED:
8 / 8

D ARTIFACTS BYTE-EQUAL:
7 / 7

E AUDIT BYTE-EQUAL:
true

FROZEN FILE COUNT:
9

PRE == POST INVENTORY:
true

POST-FREEZE MUTATION:
none

CLOSEOUT RECORD:
sha256 afaa091a20439b895d1c8facb4f1fadc70c9ffe524f2aa752fc62a1e84c65665
byte_size 4372

FROZEN-ROOT STABLE IDENTITY:
mesc-p01-04f-frozen-root/1:sha256:5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290
```

## 3. Independent verification summary

A fresh independent P01-04D generation was executed in a new verification
workspace. Its exact seven deterministic outputs were byte-for-byte identical to
the accepted P01-04D seven-file bundle. The canonical P01-04E classified audit
was then executed against that independently regenerated D bundle using the exact
reviewed classification ledger. That independently produced leakage-audit.json
was byte-for-byte identical to the accepted classified audit. All eight
deterministic formal outputs were reproduced.

This was verification only. It did not create a new accepted P01-04D result or
replace Episode #2. The frozen root preserves the accepted output lineage; the
independent rerun bytes were verified equal but not substituted.

## 4. Scope and non-authority

This disposition accepts and closes P01-04F only. P01-04 overall is not yet
closed until P01-04G promotion. This disposition does not authorize P01-04G,
model execution, training, fine-tuning, split regeneration, source-data
modification, or publication of raw scientific text.

```text
P01-04G:
NOT STARTED / NOT AUTHORIZED
```

No frozen artifact bytes, external evidence bytes, absolute paths, timestamps,
hostnames, usernames, or raw scientific content are persisted by this
governance package.