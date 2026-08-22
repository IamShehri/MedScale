# Plan — GH1 Result-Binding Repair 1

Status: **DRAFT PLAN — NO EXECUTION AUTHORITY**

Date: 2026-08-21

`acceptance.md` is normative. This plan must not weaken its fail-closed, replay, exact-head, result-graph, binding, receipt, or adoption requirements.

## Phase 1 — Revalidate live GH1 state

Before any repair mutation or merge decision:

- require canonical `main` SHA exactly `4e259767a86c74a26967e0f19598a1f84a987df4` and tree exactly `c487c5a70abf865b364c96de1aa8c18da7bf6602`;
- require the authoritative hosting verification object for that activation merge to have `verification.verified=true`, `verification.reason=valid`, `verification.signature` non-null source text, and `verification.payload` non-null source text;
- re-read PR #134 structural identity and activation head;
- enumerate the complete open + closed/merged PR population and apply the exact selected-GH1-result and reserved-conflict rules from normative `acceptance.md` Section B;
- require exactly one selected GH1 activation PR, zero selected GH1 result PRs, and `GH1_RESERVED_RESULT_NAMESPACE_CONFLICTS = 0`;
- confirm no GH1 result root, terminal receipt, result merge, or adoption record on canonical main;
- confirm the **historical GH1 hosting-repair** acceptance blob remains `2d0c9765d22b435cd8e57d13e7d5972e9a095b40`;
- confirm the inherited old preflight acceptance blob remains `7c5ae9fadaa639d2d43b6cb8051d91f01fb7d1cf`;
- read the current result-binding-repair `acceptance.md` blob SHA externally from the exact repair head and keep it distinct from both historical blob identities;
- verify the defect directly: historical GH1 hosting-repair J.2 requires an exact inherited map object while old Section E supplies no literal JSON object/keyset.

Any current contradictory evidence => stop and reassess.

## Phase 2 — Publish repair candidate only

Create exactly four new governance files under:

```text
specs/mesc-backbone-tournament/execution-preflight-1-gh1-result-binding-repair-1/
```

No existing GH1 file, frozen Repair-2 artifact, source/runtime code, test, dependency, workflow, model configuration, or model artifact may change.

Keep the repair PR Draft.

## Phase 3 — Exact-head repair qualification

Require on the unchanged repair head:

- exact four-path cumulative delta;
- `git diff --check` / repository CI PASS;
- CodeQL PASS;
- fresh independent exact-head governance review with no blocker;
- zero unresolved blocking review threads;
- canonical `main` still exactly `4e259767a86c74a26967e0f19598a1f84a987df4` / tree `c487c5a70abf865b364c96de1aa8c18da7bf6602` and repair head unchanged;
- authoritative activation-merge hosting verification still satisfies `verified=true`, `reason=valid`, non-null source `signature`, and non-null source `payload`;
- complete replay still returns one GH1 activation PR, zero GH1 result PRs, and zero reserved result-namespace conflicts under the exact Section B selector;
- no GH1 result artifact appeared concurrently.

Every repair commit invalidates earlier exact-head evidence.

Only after Draft qualification may the repair be marked Ready following explicit Founder instruction. After Ready, require a fresh exact-head review cycle before merge.

## Phase 4 — Repair merge and post-merge verification

Merge only with `expected_head_sha = <fully reviewed exact repair head>`.

Immediately verify:

- canonical `main` equals returned merge SHA;
- ordered parents are exactly `[PREMERGE_MAIN_SHA, REVIEWED_REPAIR_HEAD_SHA]`;
- merge tree is expected;
- premerge-main to merge delta is exactly the four repair files;
- the authoritative repair-merge hosting verification object has `verification.verified=true`, `verification.reason=valid`, `verification.signature` non-null source text, and `verification.payload` non-null source text;
- the four repair blobs on canonical main equal the reviewed head;
- fresh complete PR replay still has exactly one historical GH1 activation PR, zero GH1 result PRs, and zero reserved GH1 result conflicts.

Only then record:

```text
FD-MESC-BT-EXEC-1-PREFLIGHT-GH1 = SUPERSEDED_NONREUSABLE_POST_ACTIVATION_CONTRACT_DEFECT
FD-MESC-BT-EXEC-1-PREFLIGHT-GH2 = AUTHORIZED_NOT_STARTED
```

Stop if post-merge verification fails. Do not create GH2 activation from an unverified repair merge.

## Phase 5 — GH2 one-shot activation

After separate continuation instruction:

1. derive `GH2_ACTIVATION_RECEIPT_ID` from exact repair merge SHA/tree and ordered four repair-package blob identities;
2. complete metadata-only GH2 replay; require UNUSED;
3. create exact deterministic GH2 activation branch/PR adding only `claim-record.json` and `activation-receipt.json`;
4. keep Draft until exact-head CI, CodeQL, fresh independent review, zero blockers, and stable main/head;
5. Ready only after explicit Founder instruction and fresh post-Ready review;
6. merge with expected-head protection;
7. verify canonical merge SHA/tree/parents/path/hosting-verification fields/bytes/replay;
8. only then permit GH2 frozen Repair-2 content access.

No model/provider interaction is allowed.

## Phase 6 — Repeat inherited A-D scientific audits under GH2

After valid GH2 activation only:

- re-read the exact frozen Repair-2 blobs from canonical Repair-2 merge `0ee6f6d2cfba8f5ac3850c08a0a9b1a9040144a3` / tree `60e900daecea1cb9e64db95314bf9358387072b7`;
- reproduce all frozen file SHA-256 values and prompt derivations;
- reject duplicate JSON members;
- reproduce compressed and decompressed corpus identities and 240 count;
- reproduce scoring-key shard count/hash/byte-length bindings and logical scoring-key digest;
- repeat R2 provenance and corpus conformance predicates;
- emit only GH2 canonical audit artifacts.

Earlier GH1 audit observations are not reused as GH2 artifact authority.

## Phase 7 — GH2 execution-binding inventory

Without model access, truthfully record every exact label and `BOUND|UNBOUND` status required by normative `acceptance.md` K.1, including:

- selected candidate subset status;
- exact candidate/tokenizer/processor/custom-code revisions;
- hardware/provider/runtime/precision binding status;
- peak-VRAM and latency measurement capability;
- gated-access authorization status;
- bounded attempts and artifact destinations;
- R2 provenance and corpus-conformance audit SHA-256 identities;
- report-validation/report-schema bindings;
- later exact-head execution-authorization gates.

Items may remain `UNBOUND`; they remain blockers for tournament execution but do not invalidate successful corpus preflight audits or themselves grant authority.

## Phase 8 — GH2 deterministic result package

Use only the literal `frozen_input_bindings` object in `acceptance.md` Section I. Do not construct or reference `frozen_input_digest_map`.

Build in non-cyclic order:

1. canonical audit bytes/digests;
2. execution-binding inventory bytes/digest;
3. optional inactive GH2 successor bytes/digest only if allowed;
4. exact `manifest_binding_core` and SHA-256;
5. verdict and digest;
6. exact result manifest and external digest;
7. terminal-content commit;
8. terminal receipt as direct child adding only `consumption-receipt.json`.

Every result commit is one-parent, fast-forward lineage from exact GH2 activation merge and changes only the result allowlist.

If any later predicate blocks, remove the provisional successor and rebuild the blocked package before terminal freeze.

## Phase 9 — Exact-head result merge and adoption

Open the exact structurally selected GH2 result PR only after the terminal-receipt head exists.

Require exact-head CI/CodeQL, fresh independent review, zero blocking threads, stable main/head, complete graph/binding/receipt proof, and expected-head merge.

Post-verify the result merge using the closed predicate→failure-code mapping in normative `acceptance.md` Section M, including exact SHA/tree/ordered parents/path scope/hosting verification source fields/bytes/replay.

Then create exactly one create-only adoption record PR under the result-merge-qualified GH2 adoption path. Require exact one-file scope, exact schema, exact-head gates, expected-head merge, and post-merge verification. A non-empty deterministic `failed_checks` set records failed result-merge verification and grants no terminal authority.

## Phase 10 — Stop

If canonical GH2 outcome is ready, report:

```text
PREFLIGHT_READY_FOR_EXECUTION_AUTHORIZATION
```

Do not access model weights, request gated access, send prompts, run inference/generation/training/retrieval, rank candidates, select winners, or execute the tournament. A separate Founder execution authorization is mandatory.
