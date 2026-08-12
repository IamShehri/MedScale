# P01-04D Execution-Input Identity — Verification Record

The measurement and verification evidence satisfying the XD-EXEC-3 closure
condition of
[`founder-authorization.md`](founder-authorization.md) (P-C1a, §10), which
controls on any conflict.

```text
Canonical baseline (original verification):
c6657b7213f817462b75f4abfda32018cba1f32a

Verification class:
READ-ONLY FORMAL EXECUTOR MEASUREMENT — NO EXECUTION

Authority:
the founder dispositions authorizing (1) the P-C1b bounded implementation
within the exact §9 allowlist, and (2) narrowly bounded read-only access to
the five formal input surfaces solely to sequentially read bytes, measure
them, and derive the execution-input manifest identity
```

This record was corrected and re-verified on the adopted real-input contract
reconciliation (PR #104). It deliberately preserves both states:

```text
historical/superseded measurement:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939 / 973

current corrected authoritative measurement:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004 / 820
```

Supersession reason, concise:

```text
formal executor real-input contract reconciliation;
prior schema-version descriptors were executor-internal assumptions rather
than content-validated canonical input schemas
```

## 1. P-C1b identity

```text
commit:
df2412866f0b4cb3da2f09a9e7b5d74fd231c697

subject:
feat(mesc): record formal execution input identity

canonically adopted:
PR #101 merge c6657b7213f817462b75f4abfda32018cba1f32a

production tree at adoption:
0eacc52ce0b7d54a26be1f70fcbc2bd574c1cbc8 —
byte-identical to the independently reviewed candidate tree
```

## 2. Original five-surface measurement — HISTORICAL / SUPERSEDED

The measurement of record at the original adoption (PR #101, baseline
`c6657b72`) was produced with executor-invented schema descriptors later
proven inconsistent with the canonical P01-03E/P01-03G input contracts.
It is retained for history and treated as:

```text
HISTORICAL
SUPERSEDED
NOT VALID FOR A FUTURE EXECUTION EPISODE
```

```text
surface                      sha256                                                            byte_size  schema_version (historical)
decision_record              9e90e6f09950327cc6e685ca8cd6755acb9fc298836ebdaf0258c3ae4d96e521  19628      (none exists)
ordered_example_registry     e3a4f44052665990244354241156115538697e37577bf1d1e6e80de6d9832e50  208664     mesc-pilot-01-ordered-example-id-registry/1
source_document_registry     1b8756a27c37f782c3bf1687aabc0d1e9eac2afdca55f578b9baa3685c3be032  77832      mesc-pilot-01-source-document-id-registry/1
source_records               22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce  2770193    mesc-pilot-01-source-records/1
transformed_dataset_identity 83094b76b98032cd8db07eb7a77440be7034c1e9cd02db6d1841f1b6c33a00a7  1948       mesc-pilot-01-transformed-dataset-identity/1
```

```text
historical execution-input-manifest identity (superseded):
sha256     85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939
byte_size  973
```

The four schema literals above were executor-internal assumptions, not
content-validated canonical input schemas; they were removed by the
correction (PR #104).

## 3. Correction adoption

```text
PR:
104

reviewed head:
768b83e1b8b6f2bf71f40db6224ffce6d2562fbd

merge:
493564d144633a18b3ba535d94681efc70b122ea

merge tree:
e1619632369da19c21a57bd2cf40c9cd302dfee6 (== reviewed candidate tree)

correction scope:
exactly four paths — _formal_split_v1.py, _formal_generation_v1.py
(import/reference-only rename INPUT_SCHEMA_VERSIONS ->
CANONICAL_SCHEMA_VERSIONS), and their two test modules

required checks:
PASS — CI (py3.11, py3.12), analyze, CodeQL at the exact head
```

The correction is reused, not re-reviewed: canonical adoption already proved
reviewed-head preservation, candidate tree == merge tree, required CI PASS,
B-1/B-2/F1/F2/F3 PASS, privacy/output minimization PASS, and real canonical
input compatibility PASS.

## 4. Corrected five-surface measurement — CURRENT AUTHORITATIVE

Fresh read-only re-measurement on canonical `main` at the correction baseline
`493564d`, by the formal executor's own direct byte measurement, with the
accepted external `source-records.jsonl` held in custody (XD-EXEC-2). The
`source_records` digest and byte size reconcile exactly with the XD-EXEC-2
custody attestation and with the transformed-dataset identity attestation.
Exactly five surfaces, no omissions, no duplicates, no sixth surface.

```text
surface                      sha256                                                            byte_size  schema_version (corrected)
decision_record              9e90e6f09950327cc6e685ca8cd6755acb9fc298836ebdaf0258c3ae4d96e521  19628      (none exists — omitted)
ordered_example_registry     e3a4f44052665990244354241156115538697e37577bf1d1e6e80de6d9832e50  208664     (none exists — omitted)
source_document_registry     1b8756a27c37f782c3bf1687aabc0d1e9eac2afdca55f578b9baa3685c3be032  77832      (none exists — omitted)
source_records               22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce  2770193    mesc-pubmedqa-source/1
transformed_dataset_identity 83094b76b98032cd8db07eb7a77440be7034c1e9cd02db6d1841f1b6c33a00a7  1948       mesc-pubmedqa-transform/1
```

Schema versions are derived from the actual canonical content, never
invented. Leakage search of the recomputed manifest for the four former
executor-internal literals:

```text
mesc-pilot-01-transformed-dataset-identity/1: ZERO
mesc-pilot-01-ordered-example-id-registry/1:  ZERO
mesc-pilot-01-source-document-id-registry/1:  ZERO
mesc-pilot-01-source-records/1:               ZERO
```

Required result: ZERO — satisfied.

## 5. Corrected execution-input-manifest identity — CURRENT AUTHORITATIVE

Serialized by the frozen canonical serializer as one canonical JSON document
with one terminal line feed, schema
`mesc-p01-04d-execution-input/manifest/v1`, two top-level fields:

```text
execution-input-manifest identity (corrected and authoritative):
sha256     b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004
byte_size  820
```

The manifest carries no path, timestamp or commit, so it is a pure
deterministic function of the five input byte streams. This is the identity a
future superseding execution authorization must bind.

## 6. Corrected cross-input consistency

```text
transformed identity record count == 1000
ordered row count                  == 1000
source-label count                 == 1000
dataset identity singular and consistent
source-records digest/size == transformed-dataset attestation
ordered/source-label identities reconcile exactly (join 1000/1000)
source-document counts reconcile (sum 1000; every joined row mapped)

reduction:
strict canonical validation
→ immediate reduction
→ identity + final_decision only
no scientific content survives the reduction boundary
```

All PASS on the corrected measurement.

## 7. Corrected independence (P-C1a)

```text
separate measurement:     PASS — manifest derived from the executor's own
                          direct read-only measurement of the five byte streams
separate code path:       PASS — constructed in the formal executor modules
                          (src/medscale/mesc/_formal_split_v1.py); no manifest
                          logic in the adopted evidence harness
no consumption of P-A2:   PASS — measurement reads exactly the five raw byte
                          streams; P-A2 evidence absent -> same manifest
                          identity (manifest derived from raw bytes alone)
```

## 8. Re-verification gates

```text
correction acceptance (PR #104):      PASS — reused, not re-reviewed
fresh canonical measurement:          PASS (§4–§7 above)
post-merge main checks:               PASS — CI, CodeQL; Optional Extras
                                      initially failed on a transient GitHub API
                                      certificate error in setup-uv and PASSED on
                                      re-run (three jobs) — reclassified as
                                      infrastructure, not correction-related
```

## 9. Result — RE-CLOSED

```text
historical/superseded measurement:
85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939 / 973
HISTORICAL — NOT VALID FOR A FUTURE EXECUTION EPISODE

current corrected authoritative measurement:
b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004 / 820

XD-EXEC-1:
DECIDED — CLOSED FOR P01-04D EXECUTION READINESS (unchanged)

XD-EXEC-2:
CLOSED FOR P01-04D EXECUTION READINESS (unchanged)

XD-EXEC-3:
CLOSED FOR P01-04D EXECUTION READINESS
(re-closed on corrected canonical inputs, baseline 493564d)

P01-04D execution:
NOT AUTHORIZED

P01-04D EPISODE #2:
NOT AUTHORIZED

old execution authorization:
NOT VALID FOR A NEW EPISODE — bound the historical identity above, remains
historical and unmodified; a separate superseding execution authorization
follows

Episode #1:
historically terminal EPISODE_FAILED
reuse: PROHIBITED
custody-location reconciliation: PENDING SEPARATE READ-ONLY CHECK BEFORE
EPISODE #2
```