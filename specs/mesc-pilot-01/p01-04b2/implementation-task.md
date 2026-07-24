# MESC Pilot-01 — P01-04B2 Implementation Task

Founder ratification: FD-B2-1 through FD-B2-8, 2026-07-24.
Canonical baseline: `ce1272235cb48dbacdb18f20e1ae8db695b01328`.

Status: **NOT AUTHORIZED FOR EXECUTION**

This document is a future Hermes implementation brief. It describes what implementation would look like after separate founder authorization for each increment. It does not authorize any implementation action.

## B2C — Fixture-only in-memory facade

B2C defines a separate in-memory `FixtureSplitFacade`. It is library-only and in-memory.

The facade accepts only a structurally verified in-memory `FixtureSplitRequest`.

No capability or token is required.

No B2 CLI exists.

No arbitrary filesystem input path is accepted.

No arbitrary filesystem output path is accepted.

The fixture facade performs no publication.

No path checks are needed because no arbitrary paths exist.

No facade writing is performed.

No concurrency or overwrite handling exists inside the facade.

The current public `SourceDocumentGroupedSplitter.assign()` remains fail-closed.

Formal P01-04D execution remains a separate entry point under separate authorization.

## B2D — Integrated synthetic qualification

B2D uses exactly three fixtures:

- `exact-reference-1000-v1`
- `constraint-stress-1000-v1`
- `leakage-positive-v1`

## Future increment baseline

Each future increment authorization must record the exact then-current canonical main.
