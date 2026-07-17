# MESC Pilot-01 -- P01-03A Artifact Allowlist

Freeze date: 2026-07-17

## Frozen identity allowlist

```text
dataset_id: qiaojin/PubMedQA
configuration: pqa_labeled
repository_revision: 9001f2853fb87cab8d220904e0de81ac6973b318
representation: Parquet
```

Only artifacts proving this exact frozen identity are allowable for acquisition authorization.

## Allowable file categories

* Parquet data files belonging to `pqa_labeled`
* JSON or repository metadata explicitly required to prove artifact identity

## Prohibited file categories

* Python loading scripts
* pickle files
* joblib files
* executable content
* model files
* embedding-model files
* unrelated PubMedQA configurations
* SciFact files
* full article text or PDF
* arbitrary remote-code payloads

## Exact remote filename allowlist

Inspection timestamp:

```text
INSPECTION_TIMESTAMP: 2026-07-17T23:40:00Z
```

Inspected repository revision:

```text
INSPECTED_REVISION: 9001f2853fb87cab8d220904e0de81ac6973b318
```

```text
EXACT REMOTE FILENAME ALLOWLIST: VERIFIED VIA METADATA API
```

### Permitted artifact paths

```text
CLASSIFICATION: PQA_LABELED_DATA_ARTIFACT
PATH: pqa_labeled/train-00000-of-00001.parquet
SIZE: 1075513
BLOB_ID: d305f08a5a24ea3c4dde86923d16aef1139ca262
LFS_SHA256: 3d56bd1abc11884579ecc3aab9dd3cdfce8b7cf54715daeca93b8022b7be231c
LFS_SIZE: 1075513
XET_HASH: NOT EXPOSED BY METADATA API
```

Repository metadata files reviewed but excluded from acquisition allowlist:

```text
CLASSIFICATION: REPOSITORY_DOCUMENTATION
PATH: README.md
SIZE: 5192
BLOB_ID: 82e7e0167dd7afd840819c20418979195677b1ff
```

```text
CLASSIFICATION: REPOSITORY_DOCUMENTATION
PATH: .gitattributes
SIZE: 1174
BLOB_ID: 957b2579c6ef20995a09efd9a17f8fd90606f5ed
```

### Excluded categories

* OTHER_CONFIGURATION: `pqa_artificial`, `pqa_unlabeled`
* REPOSITORY_DOCUMENTATION: `README.md`, `.gitattributes`
* PROHIBITED_EXECUTABLE_OR_SCRIPT: none observed
* UNEXPECTED_OR_UNRESOLVED: none observed

### Requirement for future acquisition

Any future acquisition must confirm that the exact path, blob ID, and LFS SHA-256 above still resolve to the same revision before downloading.

## Requirement for metadata-only verification

A narrowly scoped metadata-only authorization is required before acquisition authorization can be considered complete. That authorization must verify exact remote artifact filenames, sizes, and content digests without downloading raw content into an unprotected location.
