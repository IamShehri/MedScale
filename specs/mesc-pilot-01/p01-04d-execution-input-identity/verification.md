# P01-04D Execution-Input Identity — Verification Record

The measurement and verification evidence satisfying the XD-EXEC-3 closure
condition of
[`founder-authorization.md`](founder-authorization.md) (P-C1a, §10), which
controls on any conflict.

```text
Canonical baseline:
c6657b7213f817462b75f4abfda32018cba1f32a

Verification class:
READ-ONLY FORMAL EXECUTOR MEASUREMENT — NO EXECUTION

Authority:
the founder dispositions authorizing (1) the P-C1b bounded implementation
within the exact §9 allowlist, and (2) narrowly bounded read-only access to
the five formal input surfaces solely to sequentially read bytes, measure
them, and derive the execution-input manifest identity
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

## 2. Five-surface measurement

Measured read-only at the canonical baseline by the formal executor's own
`build_input_identity`, with the accepted external `source-records.jsonl` held
in custody (XD-EXEC-2). The five surface literals are exactly the P-A2 harness
surface set (reconciliation, contract §4.1 — the records are not
interchangeable, and no P-A evidence root exists at this baseline so no P-A2
record is consumed). The `source_records` measurement reconciles exactly with
the XD-EXEC-2 custody attestation.

```text
surface                      sha256                                                            byte_size  schema_version
decision_record              9e90e6f09950327cc6e685ca8cd6755acb9fc298836ebdaf0258c3ae4d96e521  19628      (none exists)
ordered_example_registry     e3a4f44052665990244354241156115538697e37577bf1d1e6e80de6d9832e50  208664     mesc-pilot-01-ordered-example-id-registry/1
source_document_registry     1b8756a27c37f782c3bf1687aabc0d1e9eac2afdca55f578b9baa3685c3be032  77832      mesc-pilot-01-source-document-id-registry/1
source_records               22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce  2770193    mesc-pilot-01-source-records/1
transformed_dataset_identity 83094b76b98032cd8db07eb7a77440be7034c1e9cd02db6d1841f1b6c33a00a7  1948       mesc-pilot-01-transformed-dataset-identity/1
```

Exactly five surfaces, ordered by surface name ascending, no omissions, no
duplicates, no sixth surface.

## 3. Execution-input-manifest identity

Serialized by the frozen canonical serializer as one canonical JSON document
with one terminal line feed, schema
`mesc-p01-04d-execution-input/manifest/v1`, two top-level fields:

```text
execution-input-manifest identity:
sha256     85c6233327bb6beabc0c88e232f0dd8677c2fea8431c518f3de07ef178ff9939
byte_size  973
```

This is the exact identity `MODEL A′` §5.6 activation verification will
recompute read-only and bind. The manifest carries no path, timestamp or
commit, so it is a pure deterministic function of the five input byte streams.

## 4. Independence

The P-C1b independence rule of the contract §6 was demonstrated, not assumed:

```text
separate measurement:     PASS — manifest derived from the executor's own
                          direct read-only measurement of the five byte streams
separate code path:       PASS — constructed in the formal executor modules;
                          no manifest logic in the adopted harness
no consumption of P-A2:   PASS — harness absent -> identical manifest and
                          identity; corrupting a P-A2 inputs_hashed record
                          changes nothing (differential probe)
```

## 5. Preserved findings

Fresh independent re-verification of the §8 required findings at the adopted
P-C1b tree, by at least the named discriminators:

```text
B-1   PASS — exactly two operator commands, argument surface unchanged, one
             generation per invocation, fail-closed rejections unchanged
B-2   PASS — exact seven-file candidate inventory; generation run creates no
             eighth workspace file
F1    PASS — identically-corrupted-workspaces discriminator still rejects
F2    PASS — second repository-identity verification remains the last step
             before first mutation; no manifest work between them (trace +
             profiler)
F3    PASS — generation-manifest validation unchanged (modified
             algorithm_version and extra top-level key still rejected); the
             two manifests remain distinct artifacts with distinct schema
             literals
```

## 6. Gates

```text
bounded implementation gates:  PASS — 174 passed / 1 platform skip
frozen P-A2 harness suite:     PASS — 366 passed / 3 platform skips
ruff check / format:           PASS
mypy (strict):                 PASS
PR #101 required checks:       PASS — analyze, quality (py3.11), quality
                               (py3.12), CodeQL, all at the exact head
post-merge main checks:        PASS — CI, CodeQL and Optional Extras on the
                               merge commit
```

## 7. Result

```text
condition 1 — P-C1a canonically adopted:             SATISFIED (PR #100)
condition 2 — founder-authorized P-C1b, §9 allowlist: SATISFIED (six paths,
                                                      nothing else)
condition 3 — independent recording + §5/§6 contract: SATISFIED
condition 4 — bounded implementation gates:           SATISFIED
condition 5 — fresh B-1/B-2/F1/F2/F3 re-verification: SATISFIED
condition 6 — P-C1b canonically adopted:              SATISFIED (PR #101)

XD-EXEC-3:
CLOSED FOR P01-04D EXECUTION READINESS

P01-04D execution:
NOT AUTHORIZED
```