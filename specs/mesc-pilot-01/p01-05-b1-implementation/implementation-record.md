# P01-05 B1 Evidence-Cued Baseline and Development-Evidence-Pack Tooling — Implementation Record

Status: IMPLEMENTATION RECORD — ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES

Controlling founder decision: FD-P01-05-B1-EVIDENCE-1

## Scope

This record documents the implementation of the deterministic B1 manually
evidence-cued baseline runner and the tooling required for later production of
the 100-example development evidence pack. The task authorized IMPLEMENTATION
and SYNTHETIC/FIXTURE VALIDATION only. All tests use synthetic scientific text
fixtures. No real evidence pack, annotation, subset, worksheet, or model
execution was produced or performed.

## Canonical state

- BASE CANONICAL MAIN: `bc6b65d0ba6224652cf272778d824e12d92cf72d`
- BASE TREE: `8d25d6307213ca0b17d1b15d520472940c384af5`
- B0 PRE-IMPLEMENTATION BLOBS (unchanged by this implementation):
  - `src/medscale/mesc/_b0.py`: `27c36f7fad8224c89ab8403b7abb94482d8cbbf2`
  - `src/medscale/mesc/_pilot_loader.py`: `05ad43a4aa4be778de52ab2fafc283d41956d755`
  - `src/medscale/cli/mesc_eval.py`: `84cff1a093f0daff30f4b7f7f58eb718513bff0e`
  - `src/medscale/backends/transformers/validation.py`: `74e421cbb42d348eca6183a6b208090f8139d971`
  - `src/medscale/backends/transformers/backend.py`: `d4097fb1943ed41a9deacd0d6b09f1a6cc3cb127`
- B0 POST-IMPLEMENTATION BLOBS: identical to pre-implementation (no B0 file changed)
- B0 SEMANTIC DRIFT: NONE

## Implementation principle

B1 is implemented as the smallest safe extension of the existing B0
architecture. B0 is not rebuilt and its scientific semantics are unchanged. B1
differs from B0 ONLY by the explicit manually supplied native-context
evidence-cue channel. Additive private modules were preferred.

## New modules

- `src/medscale/mesc/_b1_evidence.py` — B1 evidence domain: segment references,
  segment SHA-256 hashing, evidence IDs, annotation workflow types (input,
  submission, comparison, adjudication), label-blind annotation view, final-cue
  construction, development subset selector, subset manifest, evidence pack
  build/load/validate, atomic writes.
- `src/medscale/mesc/_b1.py` — B1 configuration, runtime manifest, prompt
  builder, input join, runner, report document/writer. Reuses B0 parse states,
  scoring, aggregation, prompt hashing, and run-digest discipline.
- `src/medscale/cli/mesc_b1_evidence.py` — `mesc-b1-evidence` CLI: subcommands
  `select-subset`, `render-annotation-view`, `validate-submission`,
  `compare-annotations`, `finalize-cues`, `validate-pack`. Explicit paths only,
  refuse overwrite, no discovery, no network, no retrieval.
- `src/medscale/cli/mesc_b1_eval.py` — `mesc-b1-eval` CLI: explicit input
  path + SHA/size, evidence-pack path + SHA/size, model path/revision,
  tokenizer revision, code commit, output path. No auto-download, no evidence
  discovery, no fallback to B0.

## Updated CLI surfaces

- `src/medscale/cli/__init__.py` — registers `mesc-b1-evidence` and
  `mesc-b1-eval` subcommands with help text.

## Updated governance paths

- `specs/mesc-pilot-01/p01-05-b1-implementation/` — this package
  (README.md, acceptance.md, implementation-record.md).
- `specs/mesc-pilot-01/p01-05/plan.md`,
  `specs/mesc-pilot-01/p01-05/data-model.md`,
  `specs/mesc-pilot-01/p01-05/execution-protocol.md`,
  `specs/mesc-pilot-01/p01-05/decision-record.md`,
  `specs/mesc-pilot-01/p01-05/acceptance.md` — minimal current-truth updates,
  including reconciliation of the prospective `B1Config.evidence_reference`
  wording to the run-level evidence-pack identity.

## Canonical contracts (implemented)

- EVIDENCE CUE SCHEMA: `mesc-pilot-01-b1-evidence-cue/1`
- ANNOTATION PROTOCOL: `mesc-pilot-01-b1-annotation/1`
- ANNOTATION VIEW SCHEMA: `mesc-pilot-01-b1-annotation-view/1`
- SUBSET MANIFEST SCHEMA: `mesc-pilot-01-b1-development-subset/1`
- EVIDENCE PACK SCHEMA: `mesc-pilot-01-b1-evidence-pack/1`
- EXAMPLE REGISTRY SCHEMA (input authority): `mesc-pilot-01-example-registry/1`
- SEGMENT INDEX CONVENTION: zero-based integer resolving against the exact
  ordered native context tuple
- SEGMENT HASH ALGORITHM: SHA-256 of the exact UTF-8 bytes of the native context
  segment string; no Unicode normalization, trimming, case folding, newline
  rewriting, or semantic normalization
- EVIDENCE ID ALGORITHM: `"mesc-b1-evidence:" + SHA-256(canonical identity
  payload)` where the payload binds schema_version, example_id,
  source_document_id, annotation_status, ordered_segment_references,
  ordered_segment_sha256s, and annotation_protocol_version. No annotator
  identity, timestamps, hostname, path, UUID, or PID enters the identity.
- SUBSET DOMAIN SEPARATOR: `mesc-pilot-01-b1-evidence-subset/1`
- SUBSET KEY: `SHA-256(UTF8("mesc-pilot-01-b1-evidence-subset/1" + ":" +
  example_id))`; sort ascending by key, tie-break example_id ascending; select
  the first 100 of the 150 frozen validation examples
- VALIDATION POPULATION CONTRACT: exactly 150 records with
  `assigned_split == "validation"` from the P01-04 example registry
- DEVELOPMENT SUBSET CONTRACT: 100 selected examples, deterministic manifest
  with `source_split_fingerprint`, `example_registry_sha256`,
  `selection_domain_separator`, ordered selected IDs, `subset_digest`; no raw
  scientific text, no labels
- REAL SUBSET PRODUCED: NO

## B1 experiment identity

- EXPERIMENT ID: `mesc-b1`
- PROMPT TEMPLATE VERSION: `mesc-b1-prompt/1`
- EVIDENCE CONDITION: `manual_native_context_cues`
- B1 RUN IDENTITY: B1 report binds `run_id`, `run_digest`, B1 config, B1 runtime
  manifest, `input_sha256`, `input_size`, `evidence_pack_sha256`,
  `evidence_pack_size`, `subset_digest`, predictions, scores, aggregate
- B1 CONFIG evidence-pack identity: `evidence_pack_sha256`, `evidence_pack_size`,
  `evidence_schema_version` (`mesc-pilot-01-b1-evidence-pack/1`),
  `annotation_protocol_version` (`mesc-pilot-01-b1-annotation/1`), `subset_digest`
- EVIDENCE PACK IDENTITY: binds `schema_version`, `annotation_protocol_version`,
  source split fingerprint, `subset_digest`, ordered cue identities, pack
  SHA-256, record count
- RAW SCIENTIFIC TEXT IN PACK: NONE — pack artifacts carry references, indices,
  hashes, statuses, and protocol metadata only; runtime tooling resolves text
  locally from an explicit source-record input

## Annotation workflow

- ANNOTATION VIEW LABEL-BLIND: YES — view contains example_id,
  source_document_id, question, ordered native context segments, and minimal
  operational metadata only; prohibited gold/prediction fields are structurally
  excluded and tested
- A/B COMPARISON: deterministic — exact agreement on annotation_status +
  ordered selected segment indices classifies AGREED; material difference
  classifies ADJUDICATION_REQUIRED
- ADJUDICATION: human adjudication submission required; no automatic consensus,
  no preferred annotator, no majority vote; adjudicator remains label-blind
- FINAL CUE: created only from A/B exact agreement or a valid adjudication
  submission; INSUFFICIENT/AMBIGUOUS require empty segment references and empty
  segment hashes; unreviewed/draft records fail closed
- REAL ANNOTATION PERFORMED: NO

## B1 prompt and isolation

- B1 PROMPT: native B0 question + complete native context plus a delimited
  `SUPPLIED EVIDENCE CUE` block; AVAILABLE resolves selected segments verbatim
  in canonical order; INSUFFICIENT and AMBIGUOUS emit explicit machine-authored
  status markers with no selected text; response contract identical to B0
- B1 GOLD ISOLATION: prompt builder has no gold parameter; generator request
  never receives gold; adversarial tests prove gold changes do not alter prompt
  bytes, prompt SHA-256, or generation request
- B1 RETRIEVAL: NONE
- B1 NETWORK ACCESS: NONE
- ABSTENTION STATES: `parsed`, `unparseable`, `ambiguous`, `generation_failed`
  preserved exactly; evidence-layer failures are typed errors raised BEFORE
  generator invocation

## Validation performed

- FOCUSED TESTS: 88 passed
  (`python -m pytest tests/test_mesc_b1_evidence.py tests/test_mesc_b1.py
  tests/test_cli_mesc_b1.py -q`; 33 + 29 + 26 test functions in the three
  cited files)
- B0 REGRESSION TESTS: 57 passed
  (`tests/test_mesc_b0.py`, `tests/test_architecture.py`,
  `tests/test_cli_ux.py`)
- FULL PYTEST: 2653 passed, 54 failed, 9 skipped — all 54 failures confined to
  `tests/test_mesc_b2a_portability.py` and reproduced identically on clean
  canonical main (pre-existing Windows bash temp-path mangling in the test
  harness, unrelated to this implementation; CI runs on Linux)
- RUFF: clean
- FORMAT: clean
- MYPY: success, no issues in 200 source files (whole repository, including
  tests, matching the CI gate)

## Review-fix round (PR #119 review findings, all resolved)

- `finalize-cues` no longer trusts the serialized `outcome` field: the
  comparison is recomputed from `submission_a`/`submission_b` via
  `compare_annotations` and only a genuinely AGREED recomputation can
  finalize; a tampered "AGREED" file with divergent submissions fails closed
  (covered by `test_b1_evidence_finalize_cues_recomputes_not_trusts_outcome`)
- Pack construction now verifies subset identity: `--subset-manifest` is
  REQUIRED by `finalize-cues` and binds the pack to the manifest
  (`subset_digest` and `source_split_fingerprint` must match, every cue
  `source_document_id` must match the manifest per-example document, and the
  record count must equal the subset `selected_count`, so a partial cue set
  can never claim the subset's identity); the manifest loader
  `load_development_subset_from_bytes` verifies the manifest's self-digest
- Durable write-once publication: `_write_atomic_json` and `write_b1_report`
  now fsync the temporary file (plus best-effort parent-directory fsync) and
  publish via exclusive-create hard link so a file created between the
  existence check and the rename can never be silently replaced
- Domain cleanliness: `annotation_input_from_source_record` exported in
  `__all__`; `_require_status`/`_require_review_status` simplified;
  `_final_cue_from_selection` validates `example_id` and
  `source_document_id` directly instead of a self-comparison
- Test quality: reviewer-independence evidence-identity assertion,
  adjudication-path and subset-manifest CLI coverage, no-artifact run
  isolated in a fresh working directory
- Governance reconciliation: `p01-05/acceptance.md` marks the no-source-change
  checklist rows as historical entry-contract acceptance superseded by this
  package; `p01-05/README.md` document index lists the implementation package;
  `p01-05/decision-record.md` and `p01-05/plan.md` already carry the
  FD-P01-05-B1-EVIDENCE-1 delta/status reconciliation

## Boundaries honored

- No real development evidence pack produced
- No real subset manifest produced
- No real annotation worksheets produced
- No real Annotator A/B submissions or adjudications produced
- No real annotation performed
- Test partition untouched; synthetic records named "test" are synthetic
  partition fixtures only
- No model execution, no weight download, no network model access
- No P01-06 authority introduced
- No vNext Stage 1 implementation introduced
- No retrieval path exists

The next founder gate after merge is:
P01-05 B1 DEVELOPMENT EVIDENCE-PACK PRODUCTION AUTHORIZATION.