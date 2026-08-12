# P01-04E Acceptance Verification

This record verifies the accepted P01-04E result against the existing nine
criteria. It does not change those criteria.

## Bound execution identities

```text
execution canonical main used by the rerun:
0fb260b43bcbd72b9ad19169279343242e4f78b8

P01-04D authoritative episode:
Episode #2

episode identity:
731ec4d6cb879eec935ce70667648a9acae656fbb36c791689fa615df04d385a

split fingerprint:
43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91

generation-manifest.json:
sha256 5ae5b91b8c11671e91bc9ca18f3d8741045ba04d83f1307c87ad71ac05f47bdd
size   2451

example-registry.jsonl:
sha256 4783d57bf9e0cdb642e0b5410ec0a388bd90d5c3d73a9b466d34f2e7b04ba310
size   311432

source-records.jsonl:
sha256 22495853cf8a395f962f9d2a2f9023ecb277f2b10cd875f69aa4b592d5b00dce
size   2770193

P01-04E operator blob:
085a83ac504552d2e726b0956f3d329199c674c1

P01-04E orchestration-module blob:
596adae652b1eec8545baafa12342b49341ac6a7
```

## Historical and classified audit identities

The earlier refused invocation remains historical and unchanged. The initial
successful detection audit remains the original unclassified result:

```text
initial detection audit:
sha256 8e203d84665de4dc7c22b20a81647ad2d825b1dd8aae50ccf7d7d99c901054e2
size   11524
findings 17 context_overlap
classification unresolved = 17
leaked true
```

The independent review package and ledger remain external and unchanged:

```text
review evidence:
schema mesc-p01-04e-review-evidence/1
sha256 a4eba45f5c87e26e2983870cc8fe51deeed03dd7fae202e2759b4ebd7310d5df
size   26237

classification ledger:
sha256 160111259c5ccf98b5a395a3fc707170ce0227fbcce5eaac19eb2be40276464b
size   4779
entries 17

stable evidence reference:
mesc-p01-04e-review-evidence/1:sha256:a4eba45f5c87e26e2983870cc8fe51deeed03dd7fae202e2759b4ebd7310d5df
```

## Classified rerun

The single classified rerun used the exact ledger and a fresh audit workspace,
with no source-data, split or code modification. Its artifact identity is:

```text
schema:
mesc-pilot-01-leakage-audit/1

sha256:
7aad5ac6248284f58adfa5dd8c342540a61dd2ab11d6b879d0cb9000b430045f

byte_size:
13293

finding_count:
17
finding_type:
context_overlap = 17
classification:
false_positive = 17
confirmed_leakage = 0
unresolved = 0
leaked:
false
```

The classified rerun finding ID set exactly equals the initial detection audit
set. Every finding retains the same finding type, example IDs,
source-document IDs, partition pair, score representation and shared surface.
Only `classification` and `evidence_reference` differ.

The classified artifact has exactly one output file, `leakage-audit.json`, and
contains no raw scientific content. Its split, source-record, generation-
manifest and example-registry identities are exact. Thresholds remain 90 for
question Jaccard and 95 for context Jaccard.

## Nine-criterion result

```text
1. exact-example cross-partition:
PASS — zero

2. source-document cross-partition:
PASS — zero

3. exact-question:
PASS — zero unresolved

4. normalized-question:
PASS — zero unresolved

5. question Jaccard >= 0.90:
PASS — zero unresolved

6. FD-E-CTX-1 context checks:
PASS — 17 detected; all independently reviewed false_positive, zero unresolved

7. no suppression:
PASS — all 17 findings preserved and classified

8. finding disposition:
PASS — all 17 explicitly classified non-leakage with stable evidence

9. leakage-audit.json:
PASS — exact schema and leaked=false
```

The accepted disposition does not claim that no similarity findings existed.
Seventeen context-overlap candidates were detected, preserved, independently
reviewed, and classified as supported non-leakage findings with stable
external evidence.
