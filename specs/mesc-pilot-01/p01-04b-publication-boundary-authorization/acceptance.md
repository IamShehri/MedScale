# P01-04B Publication Boundary — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-BPUB-1 THROUGH FD-BPUB-18:
FOUNDER DECISIONS ISSUED;
NOT YET ADOPTED ON CANONICAL MAIN

PUBLICATION-BOUNDARY IMPLEMENTATION AUTHORITY:
RECORDED BUT INACTIVE

P01-04B:
CHANGES REQUIRED / NOT ACCEPTED
```

This document defines the gate for **this documentation package only**. Satisfying
it does not adopt `FD-BPUB-1` through `FD-BPUB-18`, does not activate
implementation authority, does not accept P01-04B, does not authorize publication,
and does not authorize any downstream phase.
[`founder-authorization.md`](founder-authorization.md) controls on any conflict.

```text
DOCUMENTATION ACCEPTANCE DOES NOT ACTIVATE IMPLEMENTATION AUTHORITY.
```

---

## 1. Commit and scope

| Criterion | Requirement |
|---|---|
| A-1 exact canonical parent | The single parent is exactly `1e8b78379ee4af0c2870a5388001f528ae977221`, tree `0dba04f0baf8107e5b52e0f5f5f1b7014c818ced`, ordered parents `70bf280f…` then `97bec19b…`, merge subject `Merge pull request #81 from IamShehri/fix/mesc-p01-04b-minimum-deviation` |
| A-2 single parent | Exactly one parent; the commit is a normal commit and not a merge |
| A-3 commit identity | Exactly one commit, on branch `docs/mesc-p01-04b-publication-boundary-authorization-r2`, with subject `docs(mesc): authorize P01-04B publication boundary`; empty body; no trailer; no `Co-Authored-By` |
| A-4 commit count | Exactly one commit above the canonical parent |
| A-5 no history rewrite | No amend, rebase, squash, reset, cherry-pick, merge, patch application or force-move |
| A-6 exact five paths | Exactly these five paths and no sixth |

```text
A specs/mesc-pilot-01/p01-04b-publication-boundary-authorization/README.md
A specs/mesc-pilot-01/p01-04b-publication-boundary-authorization/acceptance.md
A specs/mesc-pilot-01/p01-04b-publication-boundary-authorization/founder-authorization.md
A specs/mesc-pilot-01/p01-04b-publication-boundary-authorization/implementation-contract.md
M specs/mesc-pilot-01/tasks.md
```

| Criterion | Requirement |
|---|---|
| A-7 four additions, one modification | Exactly four additions and exactly one modification; zero deletions, zero renames, zero copies, zero binary files |
| A-8 zero source, test and workflow changes | No change under `src/**`, `tests/**`, `.github/**` or `docs/**` |
| A-9 no dependency change | `pyproject.toml` and `uv.lock` unchanged |
| A-10 no prior package modified | No file inside any prior governance package under `specs/` is modified |
| A-11 unused identifiers | `FD-BPUB-1` through `FD-BPUB-18`, `P01-T03B19` and `specs/mesc-pilot-01/p01-04b-publication-boundary-authorization/` verified unused on the exact baseline before creation |

## 2. FD-BPUB identifier and meaning preservation

| Criterion | Requirement |
|---|---|
| A-12 all eighteen present | `FD-BPUB-1` through `FD-BPUB-18` each appear, each stated in full |
| A-13 no identifier beyond eighteen | No identifier numbered above `FD-BPUB-18` appears anywhere |
| A-14 controlling meanings | Each identifier carries exactly the meaning fixed by [`founder-authorization.md`](founder-authorization.md); none is renumbered, remapped, merged, split or shifted |
| A-15 cohesion | `FD-BPUB-1` states that atomic publication and write-path protection are one cohesive capability that is never partially operable |
| A-16 boundary | `FD-BPUB-2` states the private, unexported, library-only, fixture-only, synthetic-only, non-evidence boundary with no CLI and no public API, and that `SourceDocumentGroupedSplitter.assign` stays non-executable |
| A-17 bounded durability | `FD-BPUB-12` claims atomic namespace visibility only, and no document claims universal power-loss, storage-controller, filesystem-journal or directory-entry durability |
| A-18 no unsafe rename | `FD-BPUB-14` prohibits `os.replace`, prohibits treating a destination precheck as no-replace semantics, and prohibits "precheck, rename and postcheck" as a substitute |

## 3. Exact mechanical values

| Criterion | Requirement |
|---|---|
| A-19 final directory name | The literal `mesc-p01-04b-split-` appears as the mandatory component of the final directory name `mesc-p01-04b-split-<split_fingerprint>` |
| A-20 staging directory name | The literal `.mesc-p01-04b-split-` appears as the mandatory component of the staging directory name `.mesc-p01-04b-split-<split_fingerprint>.staging` |
| A-21 leakage filename | The leakage audit file is named exactly `leakage-audit.json`; no document produces or authorizes a `-report` infix variant of that filename |
| A-22 seven-file inventory | Exactly six payload files plus exactly one `publication-manifest.json`; no eighth file, sidecar, marker, log, lock file, temp file or receipt file |
| A-23 six byte bindings | The six file-to-attribute bindings of `FD-BPUB-6` appear exactly |
| A-24 manifest schema | `mesc-pilot-01-fixture-publication-manifest/1` |
| A-25 manifest top level | Exactly five top-level members: `schema_version`, `request_id`, `split_fingerprint`, `publication_directory_name`, `files`; no sixth member |
| A-26 no unauthorized top-level member | `fixture_only`, `non_evidence`, `fixture_id`, `synthetic_identity_proof`, `split_hash` and `execution_evidence_ref` appear only as explicit prohibitions, never as manifest members |
| A-27 file record members | Each of the six file records has exactly four members: `filename`, `surface`, `sha256`, `byte_size` |
| A-28 no per-file schema version | No manifest file record carries a `schema_version` member; that name appears at the file-record level only as an explicit prohibition |
| A-29 six surface identifiers | Exactly `group_registry`, `example_registry`, `excluded_ledger`, `split_summary_identity_core`, `split_summary_document`, `leakage_audit` |
| A-30 non-circular manifest | The manifest carries no digest and no size of itself |
| A-31 receipt fields | Exactly `publication_directory`, `request_id`, `split_fingerprint`, `publication_manifest_sha256`, `published_filenames` |
| A-32 no receipt substitutes | `final_directory` and `publication_manifest_bytes` appear only as explicit prohibitions, never as receipt fields |
| A-33 nine activation conditions | All nine conditions appear individually and in order; no document claims a smaller number of activation conditions, and no grouped, implied or subset substitute is offered |
| A-34 eligibility statement | Conditions 1 through 8 are stated to establish canonical adoption and eligibility only, with condition 9 separately required |

## 4. Governing-state truthfulness

| Criterion | Requirement |
|---|---|
| A-35 canonical main | Recorded as `1e8b78379ee4af0c2870a5388001f528ae977221` |
| A-36 PR #81 | Recorded as `MERGED` |
| A-37 minimum-deviation state | Recorded as `BUILT`, `INDEPENDENTLY REVIEWED`, `PUBLISHED`, `READY`, `MERGED`, `MECHANICALLY VERIFIED`, `FOUNDER-ACCEPTED` |
| A-38 capability | Minimum-deviation capability recorded as `SATISFIED` |
| A-39 FD-BR-1 order | Step 1 `COMPLETE`, step 2 `NEXT`, step 3 `NOT YET ELIGIBLE` |
| A-40 P01-04B | Recorded as `CHANGES REQUIRED / NOT ACCEPTED` |
| A-41 publication state | Atomic publication and write-path protections each recorded as `NOT SATISFIED` and `NOT IMPLEMENTATION-AUTHORIZED` |
| A-42 execution prohibitions | Real split execution, real partition membership and canonical leakage audit each recorded as `NOT AUTHORIZED` |
| A-43 downstream | P01-04C through P01-04G recorded as `NOT AUTHORIZED` |
| A-44 five concepts distinguished | Founder acceptance decision, canonical repository adoption, implementation merge, implementation acceptance and P01-04B acceptance are each stated and never conflated |
| A-45 no invented acceptance package | No document claims that the minimum-deviation acceptance was adopted through a separate acceptance pull request, and no such package is referenced or implied |
| A-46 no invented execution result | No workflow run identifier, check result, timing, artifact or execution output is asserted that was not independently established |
| A-47 future implementation nonexistent | The future implementation is stated as nonexistent at this baseline and its authority as inactive |

## 5. Document integrity

| Criterion | Requirement |
|---|---|
| A-48 four package files | `README.md`, `acceptance.md`, `founder-authorization.md` and `implementation-contract.md` all exist in the package directory |
| A-49 authority hierarchy | Every document names [`founder-authorization.md`](founder-authorization.md) as controlling |
| A-50 relative links | Every relative Markdown link in the four package documents resolves at this commit; no broken anchor is relied upon |
| A-51 zero placeholders | No `TODO`, `TBD`, `TBC`, `FIXME`, `XXX`, `PLACEHOLDER`, template variable, unfilled value or conflict marker |
| A-52 no environment leakage | No local username, hostname, local absolute path, temporary path, working-directory path or session identifier |
| A-53 no embedded data | No workflow log, artifact bytes, raw synthetic question, raw synthetic context, real data or model output |
| A-54 future allowlist | The exact four future paths are listed with `no fifth path`, and the protected existing paths are named explicitly |
| A-55 future identity | Branch `feat/mesc-p01-04b-publication-boundary` and subject `feat(mesc): implement P01-04B publication boundary` |

## 6. `tasks.md` chronology

| Criterion | Requirement |
|---|---|
| A-56 historical text preserved | All historical text preserved; zero removed lines; earlier entries changed only by additive supersession annotation |
| A-57 P01-T03B18 superseded | The previously live `P01-T03B18` state is annotated as a clearly superseded historical snapshot |
| A-58 true later facts | PR #80 adoption, PR #81 implementation merge, independent implementation review, mechanical post-merge verification, founder acceptance and the satisfied minimum-deviation capability are each recorded |
| A-59 one new block | Exactly one `P01-T03B19` task block appended, appearing exactly once as a task definition |
| A-60 exact contract | `P01-T03B19` uses the exact `FD-BPUB` numbering and contract of this package |
| A-61 one live state block | Exactly one live `--- Current controlling state ---`; every earlier snapshot visibly marked `HISTORICAL CONTROLLING-STATE SNAPSHOT — SUPERSEDED` |
| A-62 required state values | The live block records `FD-BPUB-1 THROUGH FD-BPUB-18: ISSUED — NOT YET ADOPTED`; `PUBLICATION-BOUNDARY IMPLEMENTATION AUTHORITY: RECORDED BUT INACTIVE`; `ATOMIC PUBLICATION: NOT YET IMPLEMENTED`; `WRITE-PATH PROTECTIONS: NOT YET IMPLEMENTED`; `MINIMUM-DEVIATION CAPABILITY: SATISFIED`; `P01-04B: CHANGES REQUIRED / NOT ACCEPTED`; `REAL EXECUTION: NOT AUTHORIZED`; `P01-04C THROUGH P01-04G: NOT AUTHORIZED` |

## 7. Repository quality gates

Run without writing:

```text
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run python -m mypy
uv run pytest -q
uv run medscale check
```

| Criterion | Requirement |
|---|---|
| A-63 no write-mode formatter | No formatter is run in write mode |
| A-64 gate results reported | Every gate is run and its exact result reported |
| A-65 environment-only failure handling | A pre-existing environment-only test failure is reported exactly, its test module verified byte-identical to the canonical parent, and confirmed not to be caused by the five documentation paths; full `pytest` `PASS` is not claimed in that case |
| A-66 no concealment | The repository is not modified to hide or work around an environment-only failure |
| A-67 documentation contract failures not excused | An environment limitation never excuses a documentation-contract failure |

## 8. Final state

| Criterion | Requirement |
|---|---|
| A-68 clean worktree | Worktree and index clean after the commit |
| A-69 remote branch absent | An authoritative `git ls-remote --heads origin` query shows the branch absent on the actual remote; a stale local remote-tracking ref is not treated as remote existence |
| A-70 no upstream | No upstream is configured for the branch |
| A-71 no push | No push, no remote branch creation |
| A-72 no PR | No pull request created, no Ready transition, no merge, no auto-merge, no review request, no comment, no review submission |
| A-73 no workflow operation | No workflow dispatch, rerun or cancellation |
| A-74 no implementation | No source, test or workflow file created or changed; the publisher does not exist |

### Stop conditions

Do not treat this gate as satisfied if any document states or implies that:

```text
the publisher is already implemented
implementation authority is active before adoption
condition nine may be inferred from conditions one through eight
a smaller set of activation conditions is sufficient
atomic publication or write-path protection may ship alone
a partially operable publisher is an acceptable intermediate state
SourceDocumentGroupedSplitter.assign may execute
os.replace is acceptable
a destination precheck provides no-replace semantics
a copy or cross-device fallback is acceptable
staging may be cleaned up, retried or repaired after a failure
a receipt may be returned on failure
the receipt is evidence
the manifest may carry a sixth top-level member
a manifest file record may carry a schema_version member
descriptor schemas may be inferred from ARTIFACT_SCHEMA_VERSIONS
a -report infix variant of the leakage-audit filename is acceptable
the -split- component is optional
durability beyond atomic namespace visibility is guaranteed
universal hard-link detection is guaranteed
a fifth future implementation path is authorized
P01-04B is accepted
P01-04C through P01-04G are authorized
real data, real split execution or a canonical leakage audit is authorized
```

Also do not treat this gate as satisfied if the package:

```text
modifies any source, test or workflow path
modifies pyproject.toml, uv.lock or any prior governance package
adds a sixth path
carries a second commit, an amend or a force operation
rewrites or deletes a historical ledger assertion
leaves more than one live Current controlling state
claims premature adoption of any FD-BPUB decision
invents a canonically adopted minimum-deviation acceptance package
invents a workflow run, check result or execution output
treats eligibility for a later decision as authority
```

Updating [`../tasks.md`](../tasks.md) to record this gate is expected and is not a
stop condition.

---

## 9. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of `FD-BPUB-1` through `FD-BPUB-18` | Requires activation conditions 1 through 8 |
| Activation of publication-boundary implementation authority | Requires all nine conditions, including condition 9 |
| The publication-boundary implementation itself | **NOT AUTHORIZED TO BEGIN** |
| Acceptance of the future implementation | **NOT ACHIEVED** — requires its own separate disposition |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** |
| Integrated P01-04B requalification | **NOT AUTHORIZED** — FD-BR-1 step 3, not yet eligible |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-05 or later | **NOT AUTHORIZED** |
| Real split execution, real partition membership | **NOT AUTHORIZED** |
| Canonical leakage audit, leakage-audit orchestration | **NOT AUTHORIZED** |
| Dataset or registry scanning, record-pair discovery | **NOT AUTHORIZED** |
| CLI, filesystem publication, public export | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| Inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning, adapter creation | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

A later, separately governed decision is **eligible for founder consideration**.
Eligibility is never authority, and this package authorizes none of that work.

---

## 10. Standing prohibition

At no point does this package permit execution against real data, real split
generation, real partition membership, a real or canonical leakage audit, B0 or B1
execution, fixture or facade execution, filesystem publication, benchmark
execution, model training or fine-tuning, P01-03G or dataset access, model access,
inference, retrieval, publication, or clinical use.
