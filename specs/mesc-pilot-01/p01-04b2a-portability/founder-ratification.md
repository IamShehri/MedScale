# MESC Pilot-01 — P01-04B2A Portability Validation Gate Founder Ratification

Status:
**FOUNDER RATIFIED — IMPLEMENTATION NOT AUTHORIZED**

Infrastructure implementation:
**NOT AUTHORIZED**

B2A implementation:
**NOT AUTHORIZED**

Execution:
**NOT AUTHORIZED**

Evidence production:
**NOT AUTHORIZED**

B2A acceptance:
**NOT ACHIEVED**

Founder:
Abdulaziz Alshehri

Founder decision date:
2026-07-27

Exact reviewed head:
`c555144b480b2334aeaaab0864cad59efe0a1e46`

Canonical planning baseline:
`0884971f68619be8f25c3b905a3dcad7c5212101`

---

## Authority and effect

The founder and controlling authority for MedScale ratifies the proposed
P01-04B2A portability-validation design decisions recorded at the exact reviewed
head above, following an independent exact-head delta review that returned
`PASS — PORTABILITY GATE CORRECTIONS INDEPENDENTLY VERIFIED; READY FOR FOUNDER
DECISION, NOT IMPLEMENTATION`.

PD-PV-1 through PD-PV-10 are adopted as:

- FD-PV-1 — Dedicated workflow boundary
- FD-PV-2 — Exact six-cell matrix
- FD-PV-3 — Least privilege, two-plane network boundary, and immutable pinning
- FD-PV-4 — Exact future infrastructure paths
- FD-PV-5 — Synthetic deterministic evidence set with binary LF-only writes
- FD-PV-6 — Fail-closed aggregate verification and safe extraction
- FD-PV-7 — Evidence-envelope separation
- FD-PV-8 — Controlled triggers and retention
- FD-PV-9 — Implementation and merge sequencing
- FD-PV-10 — Acceptance remains a separate authority act

This file is the canonical additive founder-authorization record for the
portability-validation design decisions. Pending-decision markers that remain in
the proposal documents describe their pre-ratification review state and do not
override this record.

Ratification freezes the design decisions only. It does not grant
infrastructure-implementation, B2A-implementation, execution, or
evidence-production authority.

This record does not amend FD-B2A-1 through FD-B2A-8, binding N-12, D1–D10, or
FD-B2-1 through FD-B2-8. Those remain controlling on conflict.

## Ratified decision content

The founder adopts:

- the dedicated portability workflow boundary, leaving `.github/workflows/ci.yml`
  unmodified at its current `ubuntu-latest` / Python 3.11 and 3.12 scope;
- the exact six-cell matrix of `ubuntu-latest`, `windows-latest` and
  `macos-latest` across Python 3.11 and 3.12, with `fail-fast: false` and no
  silent cell removal;
- least-privilege execution with `contents: read` only, no secrets, no write
  permissions, no OIDC, no publication, no releases, and no evidence-bearing
  cache;
- immutable full-commit-SHA pinning for **every** `uses:` entry, including
  GitHub-owned actions, with tag-only references such as `@v4` prohibited;
- the two-plane network boundary: bounded infrastructure-plane setup activity
  that may never supply evidence inputs, and a prohibited data plane;
- the exact three future infrastructure paths and no others;
- the synthetic deterministic three-file evidence set, written as raw bytes in
  binary mode with LF (`0x0A`) as the only line terminator;
- fail-closed aggregate verification with safe extraction, bounded resources, and
  byte-for-byte comparison without normalization of any kind;
- strict separation of `portability-evidence.json` from promoted B2A artifacts
  and from `split_fingerprint`;
- controlled `pull_request` and canonical-main `workflow_dispatch` triggers with
  14-day artifact retention;
- separate B2A and portability-infrastructure implementation and merge
  sequencing, never combined into one pull request;
- B2A acceptance as a separate founder authority act requiring canonical-main
  evidence and independent review.

## FD-PV-6 ratified numeric limits

The founder selects the following exact limits, which were left pending at the
reviewed head:

| Limit | Bytes | Equivalent |
|---|---|---|
| Maximum compressed size per matrix-cell artifact | `1048576` | 1 MiB |
| Maximum total extracted size per matrix-cell artifact | `4194304` | 4 MiB |
| Derived maximum compressed across exactly six artifacts | `6291456` | 6 MiB |
| Derived maximum extracted across exactly six artifacts | `25165824` | 24 MiB |

The derived aggregate values are exactly six times the corresponding per-artifact
limits and are recorded so that no aggregate total may silently exceed the
per-artifact contract.

Enforcement requirements:

- limits must be enforced **before or during** bounded extraction, never only
  after an artifact has been fully written to disk;
- a violation at artifact, file, or aggregate level must fail closed with
  `artifact_size_limit_exceeded`;
- no artifact, file, or aggregate may silently exceed these limits;
- changing any of these limits requires a **new founder decision**.

## Authorization boundary

This decision authorizes only a documentation commit recording this founder
ratification on the existing PR #57 branch.

It does not authorize:

- `.github/**` changes;
- portability-workflow implementation;
- B2A implementation;
- validation execution;
- evidence production;
- formal split generation;
- P01-03G or dataset access;
- model access;
- inference;
- retrieval;
- training;
- benchmark or metrics execution;
- B2A acceptance;
- B2B, B2C, B2D, or P01-04C through P01-04G;
- marking PR #57 Ready;
- merging PR #57;
- enabling auto-merge.

B2A remains not accepted. B2B remains not authorized. P01-04B remains incomplete
and not accepted.

## Authorized next steps

The only next steps authorized by this ratification record are:

1. run fresh exact-head CI and CodeQL for this additive documentation commit;
2. obtain an independent Opus exact-head review of the recording commit, from a
   reviewer that did not author it;
3. update PR #57 metadata to the actual head and verification state;
4. obtain a separate founder/ChatGPT decision before any Ready transition or
   merge.

No implementation may begin merely because this founder decision was issued,
recorded, reviewed, or merged.
