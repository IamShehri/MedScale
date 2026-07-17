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

## Exact filename allowlist status

```text
EXACT REMOTE FILENAME ALLOWLIST: NOT YET VERIFIED
```

Remote file enumeration is prohibited in this readiness turn. No exact filenames were retrieved from the remote repository. Any future acquisition must perform metadata-only verification before downloading any file whose name is not independently confirmed.

## Requirement for metadata-only verification

A narrowly scoped metadata-only authorization is required before acquisition authorization can be considered complete. That authorization must verify exact remote artifact filenames, sizes, and content digests without downloading raw content into an unprotected location.
