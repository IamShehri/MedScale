# P01-04F Acceptance Verification

This record verifies the accepted P01-04F result against the existing six
criteria. It does not change those criteria.

## Bound identities

```text
F authorization:
commit 0ca9a098dc29a6f6a8ee32e0170b0fe8f4f705b3
blob   442dd6b70c784344c4678e81049f8e62d4b1028f
path   specs/mesc-pilot-01/p01-04f-freeze-authorization/founder-authorization.md

F execution canonical commit:
0aa5a89e0ca54242c2da227830e41105d94b78da

P01-04D Episode #2 identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

classified E audit:
sha256 7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f
byte_size 13293
finding_count 17
leaked false

review evidence:
sha256 a4eba45f5c87e26e2983870cc8fe51deeed03dd7fae202e2759b4ebd7310d5df
byte_size 26237

classification ledger:
sha256 160111259c5ccf98b5a395a3fc707170ce0227fbcce5eaac19eb2be40276464b
byte_size 4779
entries 17

closeout record:
sha256 afaa091a20439b895d1c8facb4f1fadc70c9ffe524f2aa752fc62a1e84c65665
byte_size 4372

pre-freeze inventory sha256:
5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

post-freeze inventory sha256:
5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

frozen-root stable identity:
mesc-p01-04f-frozen-root/1:sha256:5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

independent verification result:
PASS — 7/7 D artifacts byte-identical, E audit byte-identical, 8/8 formal outputs reproduced
```

## Six-criterion result

```text
1. All outputs written exactly once to frozen evidence root:
PASS — 9/9 files

2. Pre-freeze and post-freeze inventories match:
PASS — 5888707d342602012b97fd7406cfd68146e4f3e5b643e1023954ea085614d290

3. Independent rerun produces identical outputs:
PASS — 7/7 D byte-equal, E byte-equal, 8/8 deterministic formal outputs

4. No post-freeze mutation occurred:
PASS — second read-only rehash matches

5. p01-04-closeout-record.json contains required bindings:
PASS — 12 top-level fields, canonical JSON, exact identities

6. Invalidated candidates preserved and never rewritten:
PASS — Episode #1, Episode #2, refused E invocation, initial unclassified audit all preserved
```