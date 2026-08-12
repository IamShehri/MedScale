# P01-04G Acceptance Verification

This record verifies the accepted P01-04G result against the existing six
criteria. It does not change those criteria.

## Bound identities

```text
G authorization:
commit fd4e617481984c55128358b184556f337dcfe5ae
blob   (specs/mesc-pilot-01/p01-04g-promotion-authorization/founder-authorization.md)
merge  793b80de0a77961e3d8264a97d7a526fc49dc1dc

frozen-root stable identity:
mesc-p01-04f-frozen-root/1:sha256:5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

promoted artifacts (9/9 byte-exact):
example-registry.jsonl      4783d57bf9e0cdb642e0b5410ec0a388bd90d5c3d73a9b466d34f2e7b04ba310  311432
excluded-ledger.json        786ba24fd619636052cfb3bd42b49f7bcaeb481e3745a8becb626dc064d80050  97
generation-manifest.json    5ae5b91b8c11671e91bc9ca18f3d8741045ba04d83f1307c87ad71ac05f47bdd  2451
group-registry.jsonl        ec4a6a72b7524d703c58dd379a6888aff1c866b02025a05dccc4785059780341  343432
leakage-audit.json          7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f  13293
p01-04-closeout-record.json afaa091a20439b895d1c8facb4f1fadc70c9ffe524f2aa752fc62a1e84c65665  4372
split-policy.json           f2883d0b7ff64abc2d1891af22dc5af795070fcd374b0f7069d36ccb58068786  857
split-summary-identity-core.json 1c587b9fa4dbc9e3105b136354911515b815eb671a29b59d6e525cfd6baeeca2  523
split-summary.json          704e4eaf9ffdd682055811c23284937d6523fe15981207a62bc62cca5adbab4b  628

promotable-artifact scan:
PASS — zero runtime metadata, zero local paths, zero raw scientific content

split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

classified leakage audit:
leaked false
finding_count 17
false_positive 17
confirmed_leakage 0
unresolved 0

closeout schema:
mesc-pilot-01-p01-04-closeout/1
```

## Six-criterion result

```text
1. Separate promotion authorization granted:
PASS

2. Frozen artifacts promoted to specs/mesc-pilot-01/p01-04/:
PASS — exact 9/9 frozen files

3. All promoted artifacts pass promotable-artifact scan:
PASS — zero runtime metadata, zero local paths, zero raw scientific content

4. Closeout record finalized:
PASS — schema mesc-pilot-01-p01-04-closeout/1, 12 fields

5. No unauthorized paths modified:
PASS — only the nine promoted artifacts plus governance/current-truth paths

6. P01-04 promotion does not authorize P01-05:
PASS — P01-05 explicitly NOT AUTHORIZED
```