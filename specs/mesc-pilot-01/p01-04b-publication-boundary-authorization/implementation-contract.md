# P01-04B Publication Boundary — Implementation Contract

```text
Status:
FUTURE IMPLEMENTATION CONTRACT — INACTIVE

Implementation authority:
RECORDED BUT INACTIVE until the FD-BPUB-18 activation sequence completes,
including the separate explicit founder activation of the implementation gate
```

This document defines, criterion by criterion, what the future bounded
implementation must satisfy. It creates no authority.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

Nothing in this document may be started before all nine activation conditions
have passed. Conditions 1 through 8 establish eligibility only.

---

## 1. Exact implementation identity

| Criterion | Requirement |
|---|---|
| C-1 branch | Exactly one branch named `feat/mesc-p01-04b-publication-boundary`, cut from the canonical main that adopts this package |
| C-2 commit | Exactly one normal commit; one parent; subject `feat(mesc): implement P01-04B publication boundary`; one-line message with no body, no trailer and no `Co-Authored-By` |
| C-3 scope | Exactly four paths; no fifth path; zero deletions |
| C-4 no amend | No amend, rebase, squash, reset, cherry-pick, merge or force-push; a defect after commit requires `STOP / REPORT / NO AMEND / NO SECOND COMMIT / SEPARATE FOUNDER CORRECTION AUTHORIZATION` |

The exact four paths:

```text
src/medscale/mesc/_fixture_publication_v1.py
tests/test_mesc_fixture_publication_v1.py
tests/test_mesc_p01_04b_publication_qualification_v1.py
.github/workflows/mesc-p01-04b-publication-qualification.yml
```

Paths explicitly **outside** the allowlist, which must remain byte-identical:

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
every specs/ path
```

## 2. Imports and dependency boundary

| Criterion | Requirement |
|---|---|
| C-5 stdlib only | The module imports only the standard library and existing private MESC modules already present at the adopting baseline |
| C-6 no dependency change | `pyproject.toml` and `uv.lock` are unchanged; no new distribution, extra or optional dependency is introduced |
| C-7 no network import | No `socket`, `http`, `urllib`, `ftplib`, `smtplib`, `requests`, `httpx` or equivalent import appears |
| C-8 no subprocess import | No `subprocess`, `os.system`, `os.exec*`, `os.spawn*`, `multiprocessing` or shell invocation appears |
| C-9 no clock or randomness import | No `time`, `datetime`, `random`, `secrets`, `uuid` or monotonic-clock read participates in any published byte, directory name, filename or control-flow decision |
| C-10 no real-data import | No dataset loader, registry reader, model, tokenizer, weight, adapter or retrieval surface is imported |

## 3. Private module boundary

| Criterion | Requirement |
|---|---|
| C-11 private module | All new production code lives in the single module `src/medscale/mesc/_fixture_publication_v1.py` |
| C-12 no public export | The name of the publisher, the receipt, the plan and every error class is absent from every `__all__`, every package `__init__`, every public re-export and every documented surface |
| C-13 `mesc/__init__.py` unchanged | `src/medscale/mesc/__init__.py` is byte-identical; `medscale` and `medscale.mesc` expose no new name |
| C-14 no CLI | No console entry point, no argument parser, no subcommand and no `medscale` CLI surface references the publisher |
| C-15 no environment switch | No environment variable, configuration file, feature flag or dotted setting enables, disables or alters any behaviour |
| C-16 splitter unchanged | `SourceDocumentGroupedSplitter.assign` continues to raise unconditionally on every call for every argument value; a dedicated test asserts this and fails if any execution path is introduced |

## 4. Private classes and functions

| Criterion | Requirement |
|---|---|
| C-17 private names | Every class and function introduced by the module is module-private by name |
| C-18 frozen slotted plan | The publication plan is a frozen, slotted, immutable value object |
| C-19 frozen slotted receipt | The runtime receipt is a frozen, slotted, immutable value object |
| C-20 no mutable default | No mutable default argument, no module-level mutable registry, no cache and no global state |
| C-21 no monkey patching | The module patches, wraps, shadows or reassigns nothing in any other module |

## 5. Exact request, result and path inputs

| Criterion | Requirement |
|---|---|
| C-22 exact types | The entry point accepts exactly one `FixtureSplitRequest` and exactly one `FixtureSplitResult`, each verified with an exact type identity check rather than an `isinstance` check that would admit a subclass |
| C-23 publication parent | Exactly one `pathlib.Path`, verified with an exact type check |
| C-24 protected roots | Exactly one `tuple[pathlib.Path, ...]`, verified to be a `tuple`, non-empty, and to contain only exact `Path` values |
| C-25 rejected input kinds | Mappings, strings, duck-typed objects, implicit paths, environment defaults, URLs, file handles, generators, iterators and adapters are each rejected by a dedicated test |
| C-26 no default paths | No parameter has a filesystem default; omitting the publication parent or the protected roots is an error, never an inferred value |

## 6. Validation order

| Criterion | Requirement |
|---|---|
| C-27 fixed order | Validation executes in exactly the FD-BPUB-8 order: input types, request/result binding, authoritative fingerprint, fingerprint record, artifact descriptors where present, six byte surfaces, digests, sizes, plan, manifest bytes, filename uniqueness, seven-name inventory, directory names, path safety, staging absence, final absence, rename-primitive availability, plan freeze |
| C-28 order is tested | A dedicated test proves the order by supplying an input that is invalid at two stages and asserting the earlier category is raised |
| C-29 no mutation during validation | No filesystem entry is created, opened for write, renamed or removed at any point during validation |

## 7. Request and result cross-binding

| Criterion | Requirement |
|---|---|
| C-30 identity binding | The result is proven to have been produced from that exact request through the accepted request-identity invariants before any mutation |
| C-31 `request_id` equality | `result.request_id` equals `request.request_id` exactly |
| C-32 authoritative fingerprint | The lowercase 64-hex fingerprint is taken from the verified accepted fingerprint record on the result, and from no other source |
| C-33 fingerprint record verified | The accepted fingerprint-record verification is invoked and must succeed before the plan is built |
| C-34 descriptors where present | Every artifact descriptor carried by the accepted fingerprint record is verified against the corresponding byte surface |
| C-35 no invented descriptor | No descriptor is required, synthesized or asserted for a byte surface that the accepted fingerprint record does not describe; their absence is not treated as a defect |
| C-36 universal byte binding | Every one of the six surfaces — described or not — is bound through direct byte equality, recomputed SHA-256 and recomputed byte size |

## 8. Path identity and disjointness

| Criterion | Requirement |
|---|---|
| C-37 parent properties | The publication parent is explicitly supplied, an exact `Path`, absolute, already existing, a directory, and not a symlink, junction, reparse indirection or alias |
| C-38 parent never created | The publisher never creates the publication parent, and a missing parent is an error |
| C-39 root properties | Every protected root is an exact `Path`, absolute, already existing and a real directory |
| C-40 immutable snapshot | Protected roots are snapshotted immutably at validation time; later caller mutation of the supplied sequence cannot affect the run |
| C-41 duplicate rejection | Duplicate protected roots, after canonical identity resolution, are rejected |
| C-42 disjointness | The publication parent is disjoint from every protected root: not equal, not inside, not an ancestor, in both directions |
| C-43 canonical identity | Comparison uses safely established canonical filesystem identity appropriate to the platform, not raw string comparison of unresolved paths |
| C-44 fail closed on unknown identity | Where canonical identity cannot be established, the publisher raises the unsafe-or-protected-path category and performs no mutation |
| C-45 child-name safety | Staging and final are direct one-component children of the publication parent, with no separator injection, no traversal, no dot component, no alternate data stream and no caller-selected filename |

## 9. Directory naming

| Criterion | Requirement |
|---|---|
| C-46 final name | Exactly `mesc-p01-04b-split-<split_fingerprint>` |
| C-47 staging name | Exactly `.mesc-p01-04b-split-<split_fingerprint>.staging` |
| C-48 mandatory component | The literal `-split-` is present in both names; a test asserts its presence in each |
| C-49 sole input | The only variable input is the verified lowercase 64-hex authoritative fingerprint |
| C-50 forbidden inputs | No clock, timestamp, PID, hostname, username, randomness, UUID, retry counter, environment value or caller suffix participates; a test asserts name stability across repeated construction |

## 10. Six byte bindings

| Criterion | Requirement |
|---|---|
| C-51 exact bindings | The six payload files bind exactly as follows |

```text
group-registry.jsonl              <- result.group_registry_bytes
example-registry.jsonl            <- result.example_registry_bytes
excluded-ledger.json              <- result.excluded_ledger_bytes
split-summary-identity-core.json  <- result.split_summary_identity_core_bytes
split-summary.json                <- result.split_summary_document_bytes
leakage-audit.json                <- result.audit_report_bytes
```

| Criterion | Requirement |
|---|---|
| C-52 no transformation | No re-encoding, re-serialization, normalization, whitespace change, newline change or trailing-byte change is applied to any surface |
| C-53 binding test | A dedicated test asserts each of the six file/attribute pairs individually |

## 11. Seven filenames

| Criterion | Requirement |
|---|---|
| C-54 exact set | The published inventory is exactly the six payload names plus `publication-manifest.json` |
| C-55 leakage name | The leakage audit file is named exactly `leakage-audit.json`; a test asserts that a `-report` infix variant of that filename is never produced |
| C-56 uniqueness | The six payload filenames are verified unique before any mutation |
| C-57 no extra file | No compatibility manifest file, request dump, pickle, log, marker, checksum sidecar, receipt file, lock file, temp file, README or eighth file is created |

## 12. Five-member manifest

| Criterion | Requirement |
|---|---|
| C-58 schema | `schema_version` is exactly `mesc-pilot-01-fixture-publication-manifest/1` |
| C-59 top-level members | The canonical top-level document has exactly five members: `schema_version`, `request_id`, `split_fingerprint`, `publication_directory_name`, `files`; a test asserts the exact key set |
| C-60 no sixth member | A test asserts that `fixture_only`, `non_evidence`, `fixture_id`, `synthetic_identity_proof`, `split_hash` and `execution_evidence_ref` are absent from the top level |
| C-61 directory name member | `publication_directory_name` equals the FD-BPUB-5 final directory basename and is never an absolute path |
| C-62 six records | `files` contains exactly six records, ordered by ascending filename |
| C-63 record members | Each record has exactly four members: `filename`, `surface`, `sha256`, `byte_size`; a test asserts the exact key set per record |
| C-64 non-circular | The manifest carries no digest of itself and no size of itself |
| C-65 no metadata | The manifest carries no absolute path, protected root, date, time, timestamp, runtime metadata, host metadata, user metadata, repository metadata, clinical claim, research claim or evidence-promotion claim |
| C-66 serializer | The manifest bytes are produced by the accepted canonical JSON serializer, preserving its accepted terminal-LF behaviour |

## 13. Surface descriptors

| Criterion | Requirement |
|---|---|
| C-67 field name | The per-file descriptor field is exactly `surface` |
| C-68 not `schema_version` | A per-file `schema_version` member is prohibited inside a manifest file record; a test asserts its absence |
| C-69 exact identifiers | The six `surface` values are exactly `group_registry`, `example_registry`, `excluded_ledger`, `split_summary_identity_core`, `split_summary_document`, `leakage_audit` |
| C-70 no inference | `ARTIFACT_SCHEMA_VERSIONS` is not consulted, projected or mapped when constructing this manifest; a test asserts no manifest value equals any artifact schema-version string |

## 14. Immutable plan

| Criterion | Requirement |
|---|---|
| C-71 complete before mutation | The full seven-entry plan, including the exact canonical manifest bytes, is built and frozen before the first filesystem mutation |
| C-72 frozen | The plan object is frozen and slotted; a test asserts that attribute assignment raises |
| C-73 no late construction | No planning step, digest computation, size computation or canonical-byte construction occurs after attempt acquisition; a test asserts the manifest bytes are byte-identical before and after the write phase |
| C-74 rename primitive checked early | Availability of a supported atomic no-replace rename primitive is verified during planning, before staging is created |

## 15. Write ordering

| Criterion | Requirement |
|---|---|
| C-75 payload order | The six payload files are written first, in exact ascending filename order |
| C-76 manifest last | `publication-manifest.json` is written last |
| C-77 not a status | Manifest presence in staging never marks staging as accepted or final; a test asserts that a staging directory containing all seven files is still not published until the rename succeeds |

## 16. Exclusive creation

| Criterion | Requirement |
|---|---|
| C-78 attempt acquisition | The single attempt is acquired only through exclusive creation of the deterministic staging directory as a direct child of the publication parent |
| C-79 collision fails | An existing staging path — of any type — fails; no indirection is followed or replaced |
| C-80 no write on failure | If exclusive staging creation fails, no payload file is written; a test asserts an empty mutation set |
| C-81 no alternate name | No alternate staging name is derived and no second attempt is constructed within one call |
| C-82 exclusive files | Every one of the seven files is created with exclusive-creation semantics: binary, no append, no truncation, no overwrite, no temporary sibling, no individual-file rename, no reopen for modification and no partial rewrite |
| C-83 no-follow | No-follow and exclusive facilities are used where the platform provides them; where a required safety property cannot be established the publisher fails closed |

## 17. Supported synchronization

| Criterion | Requirement |
|---|---|
| C-84 flush and sync | Immediately after each write the language-level buffer is flushed and a supported file synchronization primitive — such as `os.fsync` or a platform equivalent supported by the implementation — is applied, then the handle is closed |
| C-85 bounded claim | No docstring, comment, test name or document claims universal power-loss durability, storage-controller durability, filesystem-journal durability or directory-entry durability across every supported platform |
| C-86 stated guarantee | The only durability guarantee stated is atomic namespace visibility |

## 18. Readback verification

| Criterion | Requirement |
|---|---|
| C-87 reopen | Each file is reopened read-only without following an indirection |
| C-88 exact bytes | The read bytes equal the planned bytes exactly |
| C-89 digest | The recomputed SHA-256 equals the planned digest |
| C-90 size | The observed byte size equals the planned size |
| C-91 regular file | The reopened entry is verified to be a regular file |

## 19. Filesystem-derived inventory

| Criterion | Requirement |
|---|---|
| C-92 enumerated from disk | The pre-rename inventory is enumerated from the filesystem, never from the in-memory plan; a test asserts detection of an out-of-band extra entry |
| C-93 exactly seven | Exactly seven entries with exactly the seven expected names |
| C-94 all regular | No directory, symlink, junction, reparse indirection, socket, FIFO or device; no missing file, no duplicate, no unexpected entry and no alternate filename |
| C-95 contents reverified | All seven contents are reverified |
| C-96 manifest bindings | The manifest describes exactly the six payload files, its `request_id` matches the exact request, its `split_fingerprint` matches the exact result, and its `publication_directory_name` matches the FD-BPUB-5 final name |
| C-97 hard-link detection | Hard-link substitution is detected and rejected where the platform exposes reliable identity or link-count information; where it does not, no detection is claimed and the limitation is stated plainly |

## 20. Atomic no-replace rename

| Criterion | Requirement |
|---|---|
| C-98 one rename | Publication occurs through exactly one same-parent staging-directory-to-final-directory rename |
| C-99 required properties | Same parent, same filesystem namespace, atomic directory namespace visibility, destination must not exist |
| C-100 prohibited behaviours | No replace-existing behaviour, no merge with an existing directory, no copy fallback, no cross-device fallback, no recursive move and no per-file publication |
| C-101 `os.replace` prohibited | `os.replace` does not appear in the module; a test asserts its absence from the module source |
| C-102 precheck is not semantics | A destination precheck is never treated as providing no-replace semantics |
| C-103 conditional plain rename | A plain `os.rename` is used only on a platform and invocation where that exact primitive guarantees atomic no-replace behaviour for this directory rename |
| C-104 otherwise typed error | Otherwise the implementation uses a private supported atomic no-replace primitive, or raises the typed unsupported-atomic-rename error **before** attempt acquisition |
| C-105 no substitute pattern | "Precheck, rename and postcheck" is never implemented or described as a substitute for an atomic no-replace primitive |

## 21. Failure preservation

| Criterion | Requirement |
|---|---|
| C-106 preserve staging | After staging creation, any failure preserves staging exactly as left |
| C-107 no remediation | No deletion, cleanup, retry, resume, repair, alternate name, overwrite or final rename occurs on failure |
| C-108 no recovery surface | No recovery, reconciliation or garbage-collection helper is introduced |
| C-109 tested | Injected failures at each phase are asserted to leave the staging tree byte-identical to its state at failure |

## 22. Post-rename verification

| Criterion | Requirement |
|---|---|
| C-110 staging gone | Staging no longer exists |
| C-111 final present | Final exists under the exact FD-BPUB-5 name, is a real directory and is not an indirection |
| C-112 parent identity | The final directory's parent identity matches the verified publication parent |
| C-113 inventory | The exact seven-entry inventory is reverified |
| C-114 contents | All seven files are reread and reverified |
| C-115 manifest | Manifest bindings are reverified |
| C-116 typed failure | Failure raises the typed post-rename verification error and leaves the visible final directory untouched, with no rollback, cleanup, replacement or repair |

## 23. Five-field receipt

| Criterion | Requirement |
|---|---|
| C-117 exact fields | Fields equivalent to exactly `publication_directory: pathlib.Path`, `request_id: str`, `split_fingerprint: str`, `publication_manifest_sha256: str`, `published_filenames: tuple[str, ...]` |
| C-118 no substitutes | The names `final_directory` and `publication_manifest_bytes` are not used as substitutes for the selected fields; a test asserts they are absent from the receipt |
| C-119 filename tuple | `published_filenames` is the exact ascending seven-file inventory |
| C-120 return condition | The receipt is returned only after successful post-rename verification, and no receipt is returned on failure in any error category |
| C-121 receipt properties | The receipt is not written to disk, is not canonical evidence, is not exported, contains no timestamp and contains no clinical or research claim |
| C-122 no promotion | Returning a receipt does not promote the fixture result |

## 24. Error taxonomy

| Criterion | Requirement |
|---|---|
| C-123 one private base | Exactly one private base publication error class, with narrowly typed subcategories |
| C-124 required categories | The taxonomy covers at least: invalid input or identity binding; unsafe or protected path; existing staging or final conflict; unsupported atomic no-replace rename; exclusive staging creation failure; exclusive file creation or write failure; content verification failure; inventory verification failure; final rename failure; post-rename verification failure |
| C-125 upstream preserved | Accepted upstream typed exceptions are preserved where that gives more precise attribution |
| C-126 class-based dispatch | Dispatch is class-based only; no `str(error)`, `error.args` inspection, substring test, `startswith` or regular-expression match participates in any dispatch decision |
| C-127 dedicated tests | Each category has at least one dedicated test that asserts the exact class |

## 25. Qualification tests

| Criterion | Requirement |
|---|---|
| C-128 unit module | `tests/test_mesc_fixture_publication_v1.py` covers input validation, path safety, naming, planning, write ordering, verification, failure preservation, receipt and error taxonomy |
| C-129 qualification module | `tests/test_mesc_p01_04b_publication_qualification_v1.py` carries the criterion-mapped qualification assertions for this contract |
| C-130 synthetic only | Every test uses synthetic fixture material and a temporary directory tree; no real dataset, registry, source record, model or network resource is touched |
| C-131 deterministic | Tests are deterministic and order-independent, with no clock, randomness, hostname or username dependence |
| C-132 workflow | `.github/workflows/mesc-p01-04b-publication-qualification.yml` runs the qualification module; workflow success is qualification-harness evidence only and is never scientific, clinical, dataset or real-split evidence |

## 26. Protected-path assertions

| Criterion | Requirement |
|---|---|
| C-133 byte-identity test | A test asserts that every protected existing path listed in section 1 is unchanged by the implementation commit |
| C-134 export surface test | A test asserts that `medscale` and `medscale.mesc` expose no new public name |
| C-135 no governance edit | No file under `specs/` is modified by the implementation commit |

## 27. Prohibited behaviour

The implementation fails this contract if it does any of the following:

```text
exports any new public name
adds a CLI, entry point or subcommand
reads an environment variable to alter behaviour
opens a network connection or spawns a subprocess
reads a clock or draws randomness
touches real data, a real registry or a real source record
executes a real split or establishes real partition membership
executes a canonical leakage audit
promotes any output to an evidence root or the repository root
publishes into the source tree or a dataset registry
accesses a model, weights, an adapter, inference or retrieval
uses os.replace
implements a copy, cross-device or recursive-move fallback
publishes per file instead of by one directory rename
treats a destination precheck as no-replace semantics
deletes, cleans, retries, resumes or repairs after a failure
returns a receipt on failure
writes the receipt to disk
adds an eighth file to the publication directory
emits a manifest with a sixth top-level member
emits a per-file manifest record with a schema_version member
uses a -report infix variant of the leakage-audit filename
omits the mandatory -split- component from a directory name
parses an exception message to choose a code path
claims durability beyond atomic namespace visibility
claims universal hard-link detection
adds a fifth path
```

## 28. Continuing non-authority

This contract grants nothing. It becomes actionable only after the complete
nine-condition activation sequence, including the separate explicit founder
activation of the implementation gate. Implementation merge is not implementation
acceptance, and implementation acceptance is not P01-04B acceptance.

```text
ELIGIBILITY IS NEVER AUTHORITY.
```
