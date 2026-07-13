# M6 — Collaboration Workflow

Deterministic multi-reviewer workflow on the same evidence corpus.

## Overview

M6 adds a collaboration integrity layer to `medscale.litdb`. It is **not** a collaboration
SaaS platform and does not add web UI, user accounts, authentication, cloud sync, hosted
services, real-time collaboration, notifications, chat/comments, or production deployment.
All artifacts live on the local filesystem under `data/litdb/collaboration/`.

## Allowed dependencies

```
collaboration
└── litdb
    └── core utilities / provenance / reproducibility
```

`collaboration` does not import `cli`, `research`, `dataset`, `backends`, or `fhirkit`.

## Structural decisions

### 1. Reviewer identity

Lightweight immutable audit label (`ReviewerIdentity`). It is **not** an authentication
token. Two identical identities compare by value. A machine-readable JSON identity file is
written under `data/litdb/collaboration/reviewers/<reviewer_id>.json`.

### 2. Review decisions remain in `medscale.litdb.review`

`ReviewEvent`, `RecordReview`, `ReviewDecision`, `prisma_summary`, and replay logic
already exist. M6 reuses these structures exactly and does not duplicate the decision model.

### 3. Append-only reviewer logs

Each reviewer writes canonical JSONL events to:

```
data/litdb/collaboration/reviewers/<reviewer_id>.jsonl
```

Key properties:
- entries are immutable
- ordering is deterministic by file line order
- `validate_reviewer_log()` checks first-event provenance and chain continuity
- tampering/chains breakage surfaces as `LogIntegrityReport.issues`

### 4. Deterministic merge

`merge_reviewer_logs(root, reviewer_a, reviewer_b)` produces:

- sorted record-id merge order
- explicit visibility for conflicting decisions
- no silent conflict resolution
- reproducible PRISMA counts from the merged artifact

Merge manifest stores:
- both reviewer identifiers
- deterministic merged-at timestamp
- total record scope
- conflict count + conflict list
- `manifest_hash = content_hash(manifest_payload_without_hash)`

Conflicts:
- same record, both reviewers produced a non-pending decision
- decisions differ
- output: conflict list + nonzero `conflict_count`
- downstream consumers may stop, surface to operator, or rerun reviewers

### 5. Storage layout

```
data/litdb/
└── collaboration/
    ├── reviewers/
    │   ├── reviewer_a.jsonl
    │   └── reviewer_b.jsonl
    └── merges/
        └── merge_<manifest_hash>.json
```

Path helpers live in `medscale._layout` and `medscale.litdb.collaboration`.

### 6. CLI surface

`medscale screen merge --reviewer-a <id> --reviewer-b <id> [--root <path>]`

Read-only merge tooling:
- no hidden mutation
- no external calls
- deterministic output

## Guarantees

- reviewer-scoped logs stay append-only
- merge is deterministic
- conflicts are visible, never silently resolved
- PRISMA counts are reproducible across independent reviewer runs
- integrity check covers missing logs, chain breaks, and manifest-unknown references

## Limitations

- no EHR, clinical workflow, or patient data
- no authentication, authorization, users, roles, or permissions
- no cloud sync, remote services, or network calls
- reviewer logs are local `.jsonl` only
- merge supports two reviewers; N-way merge is future scope