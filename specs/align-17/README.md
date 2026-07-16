# ALIGN-17 — ModelKit Public Surface and Runtime Governance ADR

## Status

```text
ALIGN-17 ADR DECISION: ACCEPTED
IMPLEMENTATION REQUIRES SEPARATE FOUNDER AUTHORIZATION
```

## Purpose

ALIGN-17 converts the conditional ALIGN-16 audit outcome into an accepted architectural decision governing:

- ModelKit stable facade contracts;
- provisional and governance-public exports;
- compatibility-carried internal helpers;
- `DatasetRef` submodule exposure;
- registry governance;
- `ModelRef` identity and provenance;
- recipes and manifests;
- reporting ownership;
- compatibility migration policy;
- runtime exclusions and future ADR requirements.

## Canonical inputs

- `specs/align-16/`
- `docs/adr/0033-modelkit-public-surface-and-runtime-governance.md`
- `specs/align-15/`

Verified baseline:

```text
1d60f00826f7029c83706b7f97e2409b40f57d57
```

ALIGN-16 merge evidence:

```text
PR #15
Merge commit: 1d60f00826f7029c83706b7f97e2409b40f57d57
```

## File map

```text
README.md
adr-task.md
acceptance.md
docs/adr/0033-modelkit-public-surface-and-runtime-governance.md
```

## Decision summary

- three existing frozen contracts reaffirmed (`TextGenerator`, `SpanExtractor`, `ModelRef`);
- four envelopes newly frozen (`GenerationRequest`, `GenerationResult`, `FinishReason`, `Span`);
- wider facade classified without omission;
- no current export removed;
- `DatasetRef` remains submodule-only (`medscale.modelkit.recipes`);
- `backend` is execution provenance, not core scientific identity;
- no mandatory model-weight digest introduced;
- reporting ownership resolved among `modelkit.reporting`, `bench.scorers`, and `BenchmarkRunArtifact`;
- real runtime and absent governance systems remain blocked.

## Non-goals

```text
No implementation
No export change
No inference
No training
No routing
No promotion
No model lineage
No deployment
No infrastructure
No release
```

## Next governed gate

This package requires:

- documentation review;
- commit authorization;
- publication through normal governance;
- PR review and merge.

ADR acceptance alone authorizes preparation of future scoped tasks only.

Any implementation requires a new exact founder-approved allowlist.

Acceptance does not mean implementation is ready or authorized.
