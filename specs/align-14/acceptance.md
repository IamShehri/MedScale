# ALIGN-14 — Deterministic Dataset Split-Assignment Freeze Contract

- **Planning status:** Complete
- **Implementation status:** Implemented / Merged / Closed

## Implementation closeout

- Capability PR: #12
- Merge commit: `65f3685bac1668149550003382ca2da95715346e`
- Merged head: `56ffe65bda2be170cd2834fbb038af439d72e3d6`
- Merge timestamp: `2026-07-15T11:33:29Z`
- Merge method: merge commit

Final canonical contract:

- Public symbol: `SplitAssignmentFreeze`
- Public constructor input: `Sequence[str]`
- Immutable stored representation: `tuple[str, ...]`
- Builder facade: 9 symbols
- Contract version: `split-freeze/v1`

Final implementation validation evidence:

- `uv run ruff format --check .` PASS
- `uv run ruff check .` PASS
- `uv run mypy` PASS — 143 source files
- `uv run pytest` PASS — 427 passed, 2 skipped
- CI run `29411540771` SUCCESS
- CodeQL run `29411540965` SUCCESS

Deferred integration:

- Release-manifest integration: deferred
- Benchmark-manifest integration: deferred

Implementation correction history:

1. implementation commit `6b68b6852ed4c228ee6ba61161f3ae39e7274500`
2. Ruff-format correction `7c13240b0581a63daadb93426a49ae151a1769d5`
3. Sequence-typing correction `56ffe65bda2be170cd2834fbb038af439d72e3d6`

- identical explicit inputs produce identical freeze identity;
- input iterable order does not change identity;
- mapping insertion order does not change identity;
- assignment tuples are canonicalized;
- timestamps and runtime environment do not affect identity;
- strategy, seed, source fingerprint, version, or membership changes alter identity;
- Unicode and case are preserved without normalization.

## Integrity

- no duplicate identifier within a split;
- no identifier appears in more than one split;
- total count equals unique assigned identifier count;
- individual empty splits are accepted when at least one other split contains identifiers;
- a completely empty assignment is rejected.

## Immutability

- dataclass is frozen;
- nested assignment structures are immutable;
- mutation of caller-owned inputs after construction cannot change contract state;
- `freeze_fingerprint` is derived and read-only;
- no fingerprint field exists in constructor state.

## Seed and identifier validation

- seed must be an integer; `True` and `False` are rejected;
- each identifier must be a non-empty string;
- identifiers must contain at least one non-whitespace character;
- whitespace-only identifiers are rejected;
- leading and trailing whitespace are not silently removed from otherwise valid identifiers;
- case is preserved;
- Unicode is preserved.

## Serialization

- output is JSON-compatible;
- keys and collections have canonical order;
- serialization excludes runtime-only values;
- round-trip expectations are defined in implementation, not required by planning.

## Public API

- exact builder `__all__` allowlist is defined in ADR-0032;
- existing eight exports unchanged;
- proposed addition is `SplitAssignmentFreeze` only;
- no public `split_assignment_fingerprint` export is proposed;
- fingerprint calculation remains internal to `freeze.py`;
- `freeze_fingerprint` is absent from constructor arguments;
- clean-wheel imports verified.

## Release-integration boundary

- no modification to `DatasetReleaseManifest` in the minimum slice;
- no formal release-manifest integration is claimed by ALIGN-14 planning;
- the standalone freeze identity is suitable for future reference by release and benchmark artifacts, but formal integration is deferred.

## Measurable acceptance conditions

The minimum slice must satisfy all of the following measurable conditions:

- Boolean seeds are rejected.
- Whitespace-only identifiers are rejected.
- Case is preserved for identical string content with different case.
- Unicode is preserved for non-ASCII identifiers.
- Leading/trailing whitespace is preserved for otherwise valid identifiers.
- Individual empty splits are accepted when at least one other split is populated.
- A fully empty assignment is rejected.
- `split-freeze/v1` is accepted.
- Unsupported contract versions are rejected.
- `assignment_count` equals the total unique identifier count across splits.
- `freeze_fingerprint` is computed from normalized immutable state.
- `freeze_fingerprint` is read-only and not accepted as a constructor argument.
- The proposed builder facade delta contains one symbol only: `SplitAssignmentFreeze`.
- The proposed future facade is the existing eight exports plus `SplitAssignmentFreeze`.

## Repository-wide validation requirements

- `ruff check .`
- `ruff format --check .`
- `mypy`
- `pytest`
- coverage at or above repository minimum
- `medscale check`
- `uv build`
- isolated clean-wheel import verification for proposed public symbols
- `git diff --check`
- exact cumulative scope audit against three-file allowlist

## Post-merge verification

- CI success;
- CodeQL success;
- Optional Extras / Backends success.

If any required check fails, merge authorization is not granted.
