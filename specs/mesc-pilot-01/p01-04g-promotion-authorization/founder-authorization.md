# P01-04G Repository Promotion — Founder Authorization

This is the controlling document of the P01-04G promotion-authorization
package. It authorizes exact promotion of the accepted P01-04F frozen artifact
set into the canonical repository, promotable-artifact verification,
governance-only P01-04G acceptance, and final P01-04 closeout. On any conflict
with the other document in this package, this document controls.

## 1. Decision identity

```text
Decision:
P01-04G REPOSITORY PROMOTION — AUTHORIZED

Decision class:
PROMOTION AUTHORIZATION — FINAL P01-04 STAGE CLOSEOUT
```

## 2. Bound canonical pre-G state

```text
canonical pre-G main:
c8bb893f756e553347efc0c51537987ab2d3a1a4

canonical pre-G tree:
90fecd0b29ab9e852f8f8db9e665ffdba32f1192
```

## 3. Bound P01-04F acceptance

```text
P01-04F acceptance merge:
c8bb893f756e553347efc0c51537987ab2d3a1a4

P01-04F frozen-root stable identity:
mesc-p01-04f-frozen-root/1:sha256:5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

frozen file count:
9

pre-freeze inventory sha256:
5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

post-freeze inventory sha256:
5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290
```

## 4. Bound nine-file frozen inventory

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

leakage-audit.json
sha256 7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f
size   13293

p01-04-closeout-record.json
sha256 afaa091a20439b895d1c8facb4f1fadc70c9ffe524f2aa752fc62a1e84c65665
size   4372

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

## 5. Bound authoritative scientific identities

```text
P01-04D Episode #2 identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

authoritative split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

classified leakage-audit identity:
sha256 7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f
size   13293
finding_count 17
false_positive 17
confirmed_leakage 0
unresolved 0
leaked false

closeout-record identity:
sha256 afaa091a20439b895d1c8facb4f1fadc70c9ffe524f2aa752fc62a1e84c65665
size   4372

P01-04F independent verification:
8 / 8 deterministic formal outputs reproduced
```

## 6. Scope

Authorized:

```text
exact promotion of the accepted P01-04F frozen artifact set into
specs/mesc-pilot-01/p01-04/
promotable-artifact verification
governance-only P01-04G acceptance
final P01-04 closeout
```

Not authorized:

```text
P01-05
model execution
training
fine-tuning
split regeneration
leakage audit rerun
freeze rerun
source-data modification
scientific content modification
```

## 7. Promotion target

The nine frozen artifacts are promoted to exactly:

```text
specs/mesc-pilot-01/p01-04/example-registry.jsonl
specs/mesc-pilot-01/p01-04/excluded-ledger.json
specs/mesc-pilot-01/p01-04/generation-manifest.json
specs/mesc-pilot-01/p01-04/group-registry.jsonl
specs/mesc-pilot-01/p01-04/leakage-audit.json
specs/mesc-pilot-01/p01-04/p01-04-closeout-record.json
specs/mesc-pilot-01/p01-04/split-policy.json
specs/mesc-pilot-01/p01-04/split-summary-identity-core.json
specs/mesc-pilot-01/p01-04/split-summary.json
```

Bytes must be exact frozen bytes — no reformatting, normalization,
re-serialization, or metadata injection.