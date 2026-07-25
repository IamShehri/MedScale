# MESC Pilot-01 — P01-04B2 Research

Status: **design decisions ratified — implementation and execution not authorized**

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

---
## B1 source inspection
## B1 source inspection

The following is derived from static inspection of canonical main at `ce1272235cb48dbacdb18f20e1ae8db695b01328` only. No real execution occurred.

### Adopted classes in `src/medscale/mesc/split.py`

- `PilotSplitAssignment`: frozen dataclass with fields `example_id`, `split`, `source_document_id`, `partition_key`. Provides `is_train`, `is_validation`, `is_test`, `is_holdout` property accessors.
- `PilotSplitManifest`: frozen dataclass with fields `split_assignments`, `split_hash`, `split_seed`, `note`. Computes `computed_split_hash` as 16-hex truncated SHA-256 of canonical payload via `_canonical_payload()`.
- `PilotSplitNotAuthorizedError(NotImplementedError)`: explicitly raised by `SourceDocumentGroupedSplitter.assign()`.
- `SourceDocumentGroupedSplitter`: public facade with `__init__(seed)` and `assign(example_ids, source_document_ids)` that raises `PilotSplitNotAuthorizedError` with message: "SourceDocumentGroupedSplitter.assign is not implemented: real split allocation is P01-04B scope and requires explicit authorization. Refusing to fabricate split assignments."
- `PilotLeakageFinding`: frozen dataclass with fields `example_id`, `duplicate_type`, `match_example_id`, `similarity`, `shared_surface`. Provides `to_dict()` serialization.
- `PilotLeakageAuditReport`: frozen dataclass with fields `findings`, `leaked`. Provides `finding_count` property and `to_dict()` serialization.

### Adopted private core in `src/medscale/mesc/_split_v1.py`

- Private module (underscore prefix) implementing deterministic in-memory split core.
- Fixture-safe: operates only on injected rows; does not read canonical P01-03G registries from disk.
- Not publicly executable through the current `SourceDocumentGroupedSplitter` facade.

### Adopted tests in `tests/test_mesc_split.py` and `tests/test_mesc_split_v1.py`

- Synthetic fixture tests exercising data contracts, hash computation, and error behavior.
- No real P01-03G registry reads.
- No real partition membership produced.
- Tests pass on canonical main CI.

## P01-04 acceptance gap analysis

Comparing adopted B1 behavior against P01-04B acceptance criteria in `specs/mesc-pilot-01/p01-04/acceptance.md`:

| Criterion | Status | Gap |
|---|---|---|
| `SourceDocumentGroupedSplitter` deterministic grouped assignment | **Partially satisfied** | Private core exists; public facade raises; no real allocation |
| Leakage-detection primitives (exact, normalized, Jaccard) | **Unsatisfied** | Data types exist; detection logic not implemented |
| Canonical split-hash computation | **Substantially satisfied** | B1 provides 16-hex truncated hash; B2 may add full 64-hex fingerprint |
| Output artifact schemas match contracts | **Unsatisfied** | No JSONL artifact builders exist |
| CLI or formal execution entry point | **Unsatisfied** | No CLI entry point exists |
| Fixture tests pass (1,000-row, byte-identical) | **Partially satisfied** | Private core has synthetic tests; end-to-end 1,000-row integration not demonstrated |
| No execution against real P01-03G registry | **Satisfied** | Public facade raises; no real execution path exists |

## Deterministic allocation rationale

P01-04A decision D6 defines deterministic ranking via SHA-256 digest of canonical JSON keys. This design is sound for the following reasons:

- **Reproducibility:** Identical inputs produce identical outputs across Python versions implementing canonical JSON serialization correctly.
- **Auditability:** The ranking key schema is explicit and versioned.
- **Collision resistance:** SHA-256 collision resistance makes rank collisions practically impossible for the 1,000-example dataset.
- **Domain separation:** The `seed` parameter provides domain separation, not RNG entropy.

The private B1 core validates this rationale with synthetic fixture tests. B2 must preserve the same ranking key schema and serialization rules without modification.

## Leakage taxonomy

P01-04A defines six leakage detection categories:

1. `exact_example`: byte-identical `example_id` in multiple partitions
2. `source_document`: byte-identical `source_document_id` in multiple partitions (structural invariant violation)
3. `exact_question`: byte-identical question text
4. `normalized_question`: NFKC, case-folded, whitespace-collapsed question equality
5. `near_duplicate_question`: token-set Jaccard >= 0.90
6. `context_overlap`: identical normalized context segments

Category 2 (source-document) is structurally impossible during P01-04 version 1 because the registry contains exactly 1,000 source documents with maximum group size 1. It remains in the taxonomy for forward compatibility. Categories 3–6 require access to question and context text, which is prohibited from promotable artifacts per D9.

The B2 leakage primitive library must define exact input/output contracts for each category without implementing them.

## Canonical serialization constraints

P01-04A decision D6 specifies canonical serialization for ranking keys:

- recursively sorted keys;
- UTF-8;
- `ensure_ascii=False`;
- `allow_nan=False`;
- separators: `(",", ":")`;
- no indentation;
- no BOM;
- no terminal newline.

P01-04B2 proposes extending these constraints to all JSONL split artifacts:

- LF-only line endings (no CRLF);
- terminal newline at end of each line;
- identical output on repeated runs with identical inputs.

Empirically, `json.dumps(canonical, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))` produces deterministic output across standard Python implementations. B2 tooling must pin the same parameters explicitly.

## Safe-publication risks

P01-04B2 tooling must enforce the following safe-publication constraints from P01-04A D9:

- No question text in split registries, leakage reports, or summary artifacts.
- No context text in any promotable artifact.
- No per-example answer labels in group registries or example registries.
- No local paths, usernames, or hostnames.
- No timestamps beyond ISO date in `ratified_at` and `generated_at`.
- No command logs, execution durations, or workspace locations.

The risk of accidental text leakage is highest in leakage findings, where semantic labels like `"shared_surface": ["question"]` could invite unstructured free-text fields. The B2 contracts explicitly prohibit raw text in all `LeakageFinding` fields.

## Single-writer and concurrency risk

The B0 report writer documents a single-writer limitation. P01-04B2 tooling must not introduce implicit concurrency assumptions:

- Each generation workspace must be isolated.
- Write operations must use unique temporary names.
- Atomic rename must be the only finalization mechanism.
- Concurrent writer attempts must be rejected explicitly rather than silently serialized.
- Invalidated candidates must be preserved, never overwritten or deleted.

## Why real data remains prohibited

Real P01-03G registry execution is prohibited for the following reasons:

1. **No authorization:** P01-04D authorization does not exist.
2. **Incomplete specification:** P01-04B is incomplete; P01-04B2 does not complete it.
3. **Architectural safety:** The current `SourceDocumentGroupedSplitter.assign()` raises unconditionally. Accidental invocation must remain impossible until P01-04B is complete and accepted.
4. **Prohibition preservation:** P01-04A does not authorize execution. P01-04 adoption did not authorize execution. B2 documentation must not be read as implicit authorization.
5. **Evidence integrity:** Real execution would produce external evidence (workspace identity, command logs, process IDs) that must not enter the repository.
