# P01-04F Freeze, Independent Rerun, and Conditional Acceptance — Founder Authorization

This is the controlling document of the P01-04F freeze-authorization package.
It authorizes exactly one independent verification rerun of the accepted
deterministic P01-04 outputs, write-once freeze into one fresh evidence root,
deterministic `p01-04-closeout-record.json`, and governance-only P01-04F
acceptance if every criterion passes. On any conflict with the other document in
this package, this document controls.

## 1. Decision identity

```text
Decision:
P01-04F FREEZE AND INDEPENDENT VERIFICATION — AUTHORIZED

Decision class:
EXECUTION AUTHORIZATION — CONDITIONAL, EXACTLY ONE INDEPENDENT RERUN
```

## 2. Scope

Authorized:

```text
canonical adoption of this P01-04F execution authorization
one independent verification rerun of the accepted deterministic P01-04 outputs
write-once freeze into one fresh evidence root
deterministic p01-04-closeout-record.json
governance-only P01-04F acceptance and canonical closeout if every criterion passes
```

Not authorized:

```text
P01-04G
modification of P01-04D or P01-04E scientific semantics
new split generation as a replacement result
source-data modification
threshold changes
finding suppression
model execution, training, fine-tuning
```

## 3. Bound accepted P01-04D result

```text
authoritative episode:
Episode #2

episode identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

terminal manifest:
sha256 b1c377f8886f1b5aa9c6c1589a9da654152e3aff6bfbdf3f2f180d283b8c0e3b
size   1247

authoritative split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91
```

Accepted seven-file D inventory:

```text
example-registry.jsonl
sha256 4783d57bf9e0cdb642e0b5410ec0a388bd90d5c3d73a9b466d34f2e7b04ba310
size   311432

excluded-ledger.json
sha256 786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050
size   97

generation-manifest.json
sha256 5ae5b91b8c11671e91bc9ca18f3d8741045ba04d83f1307c87ad71ac05f47bdd
size   2451

group-registry.jsonl
sha256 ec4a6a72b7524d703c58dd379a6888aff1c866b02025a05dccc4785059780341
size   343432

split-policy.json
sha256 f2883d0b7ff64abc2d1891af22dc5af795070fcd374b0f7069d36ccb58068786
size   857

split-summary-identity-core.json
sha256 1c587b9fa4dbc9e3105b136354911515b815eb671a29b59d6e525cfd6baeeca2
size   523

split-summary.json
sha256 704e4eaf9ffdd682055811c23284937d6523fe15981207a62bc62cca5adbab4b
size   628
```

## 4. Bound formal P01-04 input identities

```text
decision_record:
sha256 9e90e6f09950327cc6e685ca8cd6755acb9fc298836ebdaf0258c3ae4d96e521
size   19628

ordered_example_registry:
sha256 e3a4f44052665990244354241156115538697e37577bf1d1e6e80de6d9832e50
size   208664

source_document_registry:
sha256 1b8756a27c37f782c3bf1687aabc0d1e9eac2afdca55f578b9baa3685c3be032
size   77832

transformed_dataset_identity:
sha256 83094b76b98032cd8db07eb7a77240be7034c1e9cd02db6d1841f1b6c33a00a7
size   1948

source_records:
sha256 22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
size   2770193

derived execution-input manifest:
sha256 b0447a7ab59d0d2537a3aa247ab35a423642904148f808fb5a80648682046004
size   820
```

## 5. Bound accepted P01-04E final result

```text
initial detection audit:
sha256 8e203d84665de4dc7c22b20a81647ad2d825b1dd8aae50ccf7d7d99c901054e2
size   11524

review evidence:
schema mesc-p01-04e-review-evidence/1
sha256 a4eba45f5c87e26e2983870cc8fe51deeed03dd7fae202e2759b4ebd7310d5df
size   26237

classification ledger:
sha256 160111259c5ccf98b5a395a3fc707170ce0227fbcce5eaac19eb2be40276464b
size   4779
entries 17

accepted classified audit:
sha256 7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f
size   13293
finding_count 17
context_overlap 17
false_positive 17
confirmed_leakage 0
unresolved 0
leaked false
```

## 6. Independent verification definition

P01-04F independent verification means:

```text
1. A fresh independent P01-04D generation is executed in a new verification
   workspace. Its exact seven deterministic outputs must equal the accepted
   P01-04D seven-file bundle byte-for-byte.

2. The canonical P01-04E classified audit is executed against that
   independently regenerated D bundle, using the exact reviewed classification
   ledger. That independently produced leakage-audit.json must equal the
   accepted classified audit byte-for-byte.
```

This covers all eight deterministic formal outputs. It is verification only.
It does NOT create a new accepted P01-04D result or replace Episode #2.

## 7. Deterministic formal output set

```text
7 accepted P01-04D artifacts
+
1 accepted classified P01-04E leakage-audit.json
=
8 deterministic formal outputs
```

The final frozen evidence-root inventory is exactly:

```text
those 8 deterministic formal outputs
+
p01-04-closeout-record.json
=
9 files
```

No tenth file. External evidence and review inputs are NOT copied into the
frozen formal-output root.

## 8. Activation

This authorization becomes active upon canonical merge. The actual merge SHA
becomes the canonical execution commit for F and the value passed to
`--expected-canonical-commit` during the independent rerun.

## 9. Privacy and integrity

No absolute path, workspace location, custody location or timestamp is
persisted by this package. No raw scientific content, audit bytes,
review-evidence bytes, or classification-ledger bytes are persisted by this
package. The independent rerun mutates no tracked repository file, no accepted
P01-04D workspace, no source-record file, and no accepted P01-04E audit.