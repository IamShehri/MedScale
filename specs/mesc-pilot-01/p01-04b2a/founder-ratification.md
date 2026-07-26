# MESC Pilot-01 — P01-04B2A Founder Ratification

Status:
**FOUNDER RATIFIED — IMPLEMENTATION NOT AUTHORIZED**

Implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Founder:
Abdulaziz Alshehri

Founder decision date:
2026-07-26

Exact reviewed head:
`574ec3ba646b7f005d04c6af5a8a8f40542fb720`

Canonical planning baseline:
`1a9169f7229bb72eba6772448724c54ec71937c5`

---

## Authority and effect

The founder and controlling authority for MedScale ratifies the proposed
P01-04B2A decisions recorded at the exact reviewed head above.

PD-B2A-1 through PD-B2A-8 are adopted as:

- FD-B2A-1 — Private module boundary
- FD-B2A-2 — Canonical value domain
- FD-B2A-3 — Canonical JSON and JSONL
- FD-B2A-4 — Artifact descriptors
- FD-B2A-5 — Non-circular fingerprint model
- FD-B2A-6 — Split-summary identity core
- FD-B2A-7 — Fail-closed validation
- FD-B2A-8 — Determinism evidence

FD-B2A-5 includes the non-circular fingerprint clarification and validation
sequence recorded under the historical proposal label PD-B2A-5.1.

This file is the canonical additive founder-authorization record for the B2A
contract decisions. Pending-decision markers in the proposal documents describe
their pre-ratification review state and do not override this record.

Ratification freezes the contract decisions only. It does not grant
implementation or execution authority.

## Ratified contract content

The founder adopts:

- the private B2A module boundary;
- the canonical value domain;
- the explicit separation of boolean and integer types;
- canonical in-memory JSON and JSONL serialization;
- immutable artifact descriptors;
- the non-circular split-fingerprint identity model;
- the deterministic split-summary identity core;
- typed fail-closed validation;
- deterministic golden-vector and portability evidence requirements.

## N-12 sequencing decision

B2A implementation acceptance must not be declared while the Windows and macOS
portability obligation remains open.

Linux evidence on Python 3.11 and Python 3.12 is partial evidence only.

Before B2A may be declared accepted, deterministic golden-vector bytes and
hashes must be demonstrated as identical across:

- Linux;
- Windows;
- macOS;
- Python 3.11;
- Python 3.12 where supported by the authorized validation infrastructure.

Until that evidence is produced and independently reviewed:

- B2A remains not accepted;
- the portability obligation remains open;
- B2B authorization must not be granted;
- no artifact may be promoted on the claim of completed cross-platform
  determinism.

Any workflow or validation-infrastructure change requires separate founder
authorization.

## Authorization boundary

This decision ratifies the P01-04B2A contracts and decision package only.

It does not authorize:

- B2A implementation;
- execution;
- formal split generation;
- P01-03G or dataset access;
- model access;
- inference;
- retrieval;
- training;
- metrics or benchmark execution;
- publication;
- clinical use;
- B2B, B2C, or B2D;
- P01-04C through P01-04G.

P01-04B remains incomplete and not accepted.

## Authorized next steps

The only next steps authorized by this ratification record are:

1. run fresh exact-head CI and CodeQL for this additive documentation commit;
2. obtain an independent Opus exact-head review;
3. update PR #55 metadata to the actual head and verification state;
4. obtain a separate founder/ChatGPT merge decision.

No implementation may begin merely because this founder decision was issued,
recorded, reviewed, or merged.
