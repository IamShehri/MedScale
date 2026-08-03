# P01-04B Publication Boundary Authorization

```text
Package status:
RECORDED — NOT ADOPTED

FD-BPUB-1 THROUGH FD-BPUB-18:
FOUNDER DECISIONS ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

PUBLICATION-BOUNDARY IMPLEMENTATION AUTHORITY:
RECORDED BUT INACTIVE

PUBLICATION-BOUNDARY IMPLEMENTATION:
NOT AUTHORIZED TO BEGIN

ATOMIC PUBLICATION:
NOT SATISFIED; NOT IMPLEMENTATION-AUTHORIZED

WRITE-PATH PROTECTIONS:
NOT SATISFIED; NOT IMPLEMENTATION-AUTHORIZED

MINIMUM-DEVIATION CAPABILITY:
SATISFIED

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED

P01-04C THROUGH P01-04G:
NOT AUTHORIZED
```

## Purpose

This package prospectively authorizes **one** tightly bounded future
implementation of the P01-04B atomic publication and write-path protection
boundary as **FD-BPUB-1 through FD-BPUB-18**.

```text
This package does not implement the publisher.
It implements nothing, executes nothing and publishes nothing.
```

It is FD-BR-1 increment 2, authorized only because FD-BR-1 increment 1 — the
global minimum-deviation grouped allocation correction — is complete and
founder-accepted.

## Canonical baseline

```text
Required canonical main:
1e8b78379ee4af0c2870a5388001f528ae977221

Required tree:
0dba04f0baf8107e5b52e0f5f5f1b7014c818ced

Ordered parent 1:
70bf280fccff4d9f4ecc24839dd9f7597c18e489

Ordered parent 2:
97bec19bca47933bd6f81cf482f668779f9a8298

Merge subject:
Merge pull request #81 from IamShehri/fix/mesc-p01-04b-minimum-deviation

Merge body:
fix(mesc): implement P01-04B minimum-deviation allocation
```

## Accepted PR #81 identity

```text
Authorization PR #80   head 823ca6d5…                merge 70bf280f…
Implementation PR #81  head 97bec19b…  tree 0dba04f0…  merge 1e8b7837…
```

The implementation commit is one normal single-parent commit over exactly the
four FD-BMD allowlist paths, 1539 insertions and 68 deletions, no path added and
no path deleted:

```text
src/medscale/mesc/_split_v1.py                 f755771b…
src/medscale/mesc/_fixture_split_v1.py         1e73ddf2…
tests/test_mesc_split_v1.py                    2f38d7a3…
tests/test_mesc_p01_04b2d_qualification_v1.py  ffc776cf…
```

## Minimum-deviation state

```text
BUILT
INDEPENDENTLY REVIEWED
PUBLISHED
READY
MERGED
MECHANICALLY VERIFIED
FOUNDER-ACCEPTED

Minimum-deviation capability:
SATISFIED
```

Five states are distinguished and never conflated:

| Concept | State |
|---|---|
| Founder acceptance decision | **GRANTED** |
| Canonical repository adoption | **ACHIEVED** — merge `1e8b7837…` |
| Implementation merge | **ACHIEVED** — merge is not acceptance |
| Implementation acceptance through a separate canonically adopted acceptance package | **DOES NOT EXIST AT THIS BASELINE** |
| P01-04B acceptance | **NOT ACHIEVED** |

This package relies on the founder's explicit acceptance decision. It does not
claim that acceptance was adopted through a separate acceptance pull request, and
no such package is invented or implied.

## FD-BR-1 recovery order

```text
Step 1  global minimum-deviation grouped allocation correction
        COMPLETE

Step 2  atomic publication and write-path protection boundary
        NEXT — the subject of this package

Step 3  integrated P01-04B requalification and acceptance disposition
        NOT YET ELIGIBLE
```

## FD-BPUB decision summary

```text
FD-BPUB-1   atomic publication and write-path protection are one
            cohesive capability; never partially operable
FD-BPUB-2   private, unexported, library-only, fixture-only,
            synthetic-only, non-evidence; no CLI; no public API
FD-BPUB-3   exact FixtureSplitRequest and FixtureSplitResult, one
            absolute publication-parent Path, one exact tuple of
            protected roots; binding verified before mutation
FD-BPUB-4   publication parent and protected-root fail-closed rules;
            full disjointness; canonical filesystem identity
FD-BPUB-5   exact directory names; the -split- component is mandatory
FD-BPUB-6   exact seven-file inventory and six exact byte bindings
FD-BPUB-7   exact non-circular manifest; five top-level members;
            four-member file records keyed by surface
FD-BPUB-8   complete verified plan frozen before any mutation
FD-BPUB-9   one attempt, acquired by exclusive staging creation
FD-BPUB-10  seven exact-once exclusive writes
FD-BPUB-11  six payloads in ascending order, manifest last
FD-BPUB-12  per-file readback verification; bounded durability claim
FD-BPUB-13  filesystem-derived seven-entry staging inventory
FD-BPUB-14  one same-parent atomic no-replace directory rename
FD-BPUB-15  failure preserves staging exactly as left
FD-BPUB-16  full post-rename verification; no rollback or repair
FD-BPUB-17  one private five-field runtime receipt
FD-BPUB-18  typed error taxonomy; adoption and activation boundary
```

[`founder-authorization.md`](founder-authorization.md) carries the exact meaning
of each identifier and controls. The numbering above is the controlling
numbering; no identifier may be renumbered, remapped, merged or shifted, and no
identifier beyond `FD-BPUB-18` exists.

## Exact directory names

```text
final directory:
mesc-p01-04b-split-<split_fingerprint>

staging directory:
.mesc-p01-04b-split-<split_fingerprint>.staging
```

Both are derived only from the verified lowercase 64-hex authoritative split
fingerprint. The literal `-split-` component is mandatory. No clock, timestamp,
PID, hostname, username, randomness, UUID, retry counter, environment value or
caller suffix participates.

## Exact seven-file inventory

```text
group-registry.jsonl               <- result.group_registry_bytes
example-registry.jsonl             <- result.example_registry_bytes
excluded-ledger.json               <- result.excluded_ledger_bytes
split-summary-identity-core.json   <- result.split_summary_identity_core_bytes
split-summary.json                 <- result.split_summary_document_bytes
leakage-audit.json                 <- result.audit_report_bytes
publication-manifest.json          <- canonical manifest bytes
```

The leakage audit filename is exactly `leakage-audit.json`; a `-report` infix
variant of that filename is prohibited. There is no eighth file, no sidecar, no
marker, no log, no lock file and no receipt file.

## Exact manifest shape

```text
schema      mesc-pilot-01-fixture-publication-manifest/1

top level   exactly five members
            schema_version
            request_id
            split_fingerprint
            publication_directory_name
            files

files       exactly six records, ascending by filename

record      exactly four members
            filename
            surface
            sha256
            byte_size

surface     group_registry
            example_registry
            excluded_ledger
            split_summary_identity_core
            split_summary_document
            leakage_audit
```

The manifest is non-circular — it carries no digest or size of itself — and
`publication_directory_name` is the final directory basename, never an absolute
path. Descriptor schemas are not inferred from `ARTIFACT_SCHEMA_VERSIONS` for
this manifest: the exact per-file field is `surface`, not `schema_version`.

## Exact receipt fields

```text
publication_directory        pathlib.Path
request_id                   str
split_fingerprint            str
publication_manifest_sha256  str
published_filenames          tuple[str, ...]
```

Private, frozen, slotted, returned only after successful post-rename
verification. Never written, never exported, never evidence. The names
`final_directory` and `publication_manifest_bytes` must not be used as
substitutes for the selected fields.

## Activation boundary

Implementation authority remains inactive until all nine conditions occur:

```text
1. independent clean-room exact-head documentation review
2. exact reviewed head pushed
3. Draft PR opened from that exact head
4. CI and CodeQL verified at that exact head
5. separate Founder Ready decision
6. separate Founder Merge decision
7. merge-commit adoption on canonical main
8. mechanical post-merge verification
9. separate explicit founder activation of the implementation gate
```

Conditions 1 through 8 establish canonical adoption and eligibility only.

```text
NO SEVEN-CONDITION SUBSTITUTE.
NO GROUPED OR IMPLIED SUBSTITUTE.
NO SUBSET ACTIVATES AUTHORITY.
```

## Future implementation allowlist

Prospective only. None of it exists at this baseline.

```text
branch:
feat/mesc-p01-04b-publication-boundary

subject:
feat(mesc): implement P01-04B publication boundary

exactly four paths:
src/medscale/mesc/_fixture_publication_v1.py
tests/test_mesc_fixture_publication_v1.py
tests/test_mesc_p01_04b_publication_qualification_v1.py
.github/workflows/mesc-p01-04b-publication-qualification.yml

no fifth path
```

Protected existing paths, required to stay byte-identical:

```text
src/medscale/mesc/__init__.py
src/medscale/mesc/split.py
src/medscale/mesc/_split_v1.py
src/medscale/mesc/_fixture_split_v1.py
src/medscale/mesc/_canonical_json_v1.py
src/medscale/mesc/_split_artifacts_v1.py
src/medscale/mesc/_leakage_v1.py
tests/_mesc_p01_04b2d_fixtures_v1.py
pyproject.toml
uv.lock
every prior governance package
```

## Authority hierarchy

```text
1. founder-authorization.md   controlling
2. implementation-contract.md future criterion-by-criterion contract
3. acceptance.md              this package's documentation gate
4. README.md                  overview only
```

On any conflict, [`founder-authorization.md`](founder-authorization.md) controls.
`README.md` never controls.

## Document index

```text
README.md                  — this overview
founder-authorization.md   — controlling
implementation-contract.md — future criterion-by-criterion contract
acceptance.md              — this package's documentation gate
```

- [`README.md`](README.md)
- [`founder-authorization.md`](founder-authorization.md) — **controlling**
- [`implementation-contract.md`](implementation-contract.md)
- [`acceptance.md`](acceptance.md)

Prior governance history is adopted at
[`../p01-04/`](../p01-04/),
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b2a/`](../p01-04b2a/),
[`../p01-04b2a-acceptance/`](../p01-04b2a-acceptance/),
[`../p01-04b2b-authorization/`](../p01-04b2b-authorization/),
[`../p01-04b2b-acceptance/`](../p01-04b2b-acceptance/),
[`../p01-04b2c-authorization/`](../p01-04b2c-authorization/),
[`../p01-04b2c-acceptance/`](../p01-04b2c-acceptance/),
[`../p01-04b2d-authorization/`](../p01-04b2d-authorization/),
[`../p01-04b2d-acceptance/`](../p01-04b2d-acceptance/)
and
[`../p01-04b-min-deviation-authorization/`](../p01-04b-min-deviation-authorization/)
and is not restated here.

## Continuing prohibitions

```text
source changes                     test changes
workflow changes                   dependency or lockfile changes
implementation                     public export
CLI                                environment switch
network                            subprocess
clock                              randomness
real-data access                   real-data adapter
real split execution               real partition membership
canonical leakage execution        leakage-audit orchestration
dataset or registry scanning       record-pair discovery
evidence-root promotion            repository-root promotion
source-tree publication            dataset-registry publication
model or weight access             inference
retrieval                          metrics
benchmark execution                training
fine-tuning                        adapter creation
publication                        clinical use
P01-04B acceptance                 P01-04C through P01-04G
P01-05 or later
```

## What this package does not do

```text
does not implement the publisher
does not activate implementation authority before adoption and condition nine
does not create any directory, manifest or receipt
does not make SourceDocumentGroupedSplitter.assign executable
does not promote any fixture output to evidence
does not change any artifact, serialization or leakage schema
does not modify any prior governance package
does not accept P01-04B
does not authorize a fifth future implementation path
does not authorize real dataset, registry or source-record access
does not authorize real split execution or real partition membership
does not authorize a canonical leakage audit
does not authorize model access, inference, retrieval, training,
  fine-tuning or adapter creation
does not authorize publication or clinical use
does not authorize P01-04C through P01-04G, or P01-05 or later
does not dispatch, rerun or cancel any workflow
```

A later, separately governed decision is eligible for founder consideration.

```text
ELIGIBILITY IS NEVER AUTHORITY.
```
