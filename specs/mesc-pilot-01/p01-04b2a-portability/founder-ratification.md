# MESC Pilot-01 — P01-04B2A Portability Validation Gate Founder Ratification

Status:
**CONTRACTS FOUNDER RATIFIED; REMEDIATION PROSPECTIVELY AUTHORIZED**

Contracts:
**FOUNDER RATIFIED**

Historical initial implementation:
**OCCURRED BEFORE CANONICAL AUTHORIZATION**

Current remediation implementation:
**PROSPECTIVELY AUTHORIZED AFTER THIS RECORD IS ADOPTED**

Infrastructure adoption:
**NOT ACHIEVED**

Execution:
**NOT AUTHORIZED**

Admissible evidence production:
**NOT AUTHORIZED**

B2A acceptance:
**NOT ACHIEVED**

B2B:
**NOT AUTHORIZED**

P01-04B:
**INCOMPLETE / NOT ACCEPTED**

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

---

# Addendum — FD-PV-11 through FD-PV-15

Founder:
Abdulaziz Alshehri

Founder decision date:
2026-07-30

Required canonical baseline for this record:
`f71c6abf2b2f905f605951605efd6c8ab016523e`

Affected Draft pull request:
`PR #61`

Exact reviewed head:
`8e484739ba72f4a3be357bd5934b305fd9e7cf41`

Exact reviewed tree:
`a6bfb21cb2bfa34964ce68190e53f5f809661002`

Reviewed commit series:
`023d0eeff535071cff96cf366b4c52d973347207` (tree
`8e222bf7cdc6ffc34e50b2059e40b47174157b84`), then
`8e484739ba72f4a3be357bd5934b305fd9e7cf41`.

## Accepted determination

The founder accepts the following verdict on the exact reviewed head:

```text
AUTHORITY GAP — PR #61 MUST REMAIN DRAFT UNTIL MISSING DECISIONS ARE CANONICALIZED
```

The determination is that binding implementation constraints were being applied
to PR #61 that could not be re-derived from any record committed to this
repository. This addendum canonicalizes the missing decisions so that a reviewer
working only from the repository can reconstruct the full constraint set.

**Independence disclosure.** The reviews of PR #61 produced to date were not
produced by an independent reviewer: they were produced by the same party that
authored the two commits. This record does not claim that a qualified
independent exact-head review has occurred. `FD-PV-11` requires one before any
Ready-transition decision, and that requirement is outstanding.

## FD-PV-11 — Historical truth and prospective remediation authorization

1. The PR #61 implementation work was created **before** a canonical
   infrastructure-implementation authorization was adopted.
2. This record does **not** retroactively claim that
   `023d0eeff535071cff96cf366b4c52d973347207` or
   `8e484739ba72f4a3be357bd5934b305fd9e7cf41` were authorized when authored.
   They were not.
3. Both commits remain Draft, unmerged, unadopted implementation work.
4. The founder now **prospectively** authorizes remediation of, and further
   review of, PR #61 — but only after this governance package is adopted on
   canonical main.
5. No current implementation is accepted merely because remediation is
   authorized. Authorizing repair is not accepting the thing repaired.
6. PR #61 must remain Draft until **all** of the following have occurred:
   - this governance package is adopted on canonical main;
   - the branch is synchronized with the new canonical main **without history
     rewriting**;
   - the required implementation corrections are completed;
   - exact-head workflows pass;
   - a **genuinely independent** exact-head review approves it;
   - a **separate** founder Ready-transition decision is issued.

## FD-PV-12 — Preserve FD-PV-6 through bounded artifact handling

The founder selects the security-preserving bounded-artifact-handling
architecture. The corrected infrastructure must enforce exactly:

| Limit | Bytes | Axis | Scope |
|---|---|---|---|
| Maximum compressed size per artifact | `1048576` | Compressed archive bytes | Per artifact |
| Maximum extracted size per artifact | `4194304` | Extracted regular-file bytes | Per artifact |
| Maximum compressed across six artifacts | `6291456` | Compressed archive bytes | Aggregate |
| Maximum extracted across six artifacts | `25165824` | Extracted regular-file bytes | Aggregate |

Requirements:

- compressed limits are measured against **artifact archive bytes**;
- extracted limits are measured against **actual extracted regular-file bytes**;
- compressed limits are enforced **before or during download**;
- archive structure is inspected **before** extraction;
- extracted limits are enforced **during** bounded extraction;
- post-extraction-only enforcement is **prohibited**;
- an oversized download or ZIP bomb must be stopped before it can exhaust runner
  disk;
- exactly six named artifacts are accepted;
- exactly three regular files per artifact are accepted;
- unsafe entries fail closed;
- no normalization of compared file bytes is permitted;
- all violations use the existing ratified failure taxonomy;
- the four limits themselves remain **unchanged**.

The value `1048576` **must not** be reinterpreted as an extracted per-file
limit. `FD-PV-6` does not ratify a general per-file 1 MiB extracted limit. Any
such limit is an invented constraint and must be **removed** during remediation.

## FD-PV-13 — Narrow read-only Actions permission

The earlier `contents: read` only rule is amended **solely** as follows:

```yaml
permissions:
  contents: read
  actions: read
```

`actions: read` is authorized solely for:

- enumerating the artifacts belonging to the **current exact workflow run**;
- reading artifact metadata, including archive byte size;
- downloading the exact expected artifacts through the documented GitHub Actions
  API.

It does **not** authorize workflow mutation, reruns, cancellation, dispatch,
artifact deletion, write permissions, secrets, OIDC, package or release
publication, cache use, or access to artifacts from another repository or an
unrelated run.

**No other permission expansion is authorized.**

Division of responsibility: the **workflow** performs artifact metadata lookup
and capped transport. The **Python helper remains network-free** and operates
only on bounded local ZIP files supplied to it by the workflow.

## FD-PV-14 — Canonical SHA binding in the evidence envelope

The canonical-main dispatch evidence envelope must support:

```json
"canonical_sha": "<40 lowercase hexadecimal commit SHA>"
```

Requirements:

- present **only** for a canonical-main `workflow_dispatch` evidence envelope;
- **absent** from pull-request validation envelopes;
- must equal the exact guarded checked-out canonical-main HEAD;
- passed **explicitly** from the already validated dispatch input;
- the helper must **not** infer it from `GITHUB_SHA`, a branch name, a tag, or
  any other uncontrolled environment value;
- validation requires exactly 40 lowercase hexadecimal characters;
- uppercase, empty, short, long, non-hex, ref-name, branch-name, and tag values
  fail closed;
- failure uses the existing `evidence_generation_failure` category — the
  twenty-one-category taxonomy is not extended;
- it never enters the three compared files;
- it never enters `split_fingerprint`;
- it remains in the non-promoted validation envelope only.

Because the evidence schema has **not** yet been adopted, and has never been
used by an authorized canonical-main dispatch, correct
`mesc-pilot-01-b2a-portability-evidence/1` **in place**. Do not create an
abandoned version 2.

## FD-PV-15 — Remediation and sequencing authority

After this governance package is merged and independently verified, and not
before, the following future sequence — and only this sequence — is authorized:

1. Synchronize the new canonical main into
   `feat/mesc-b2a-portability-infrastructure` using a normal **non-force merge
   commit**.
2. Preserve both existing commits and their exact object identities.
3. Do **not** rebase, amend, squash, reset, cherry-pick, or force-push them.
4. Add exactly two correction commits.

### Correction A

Recommended subject:

```text
fix(mesc): bind canonical SHA into portability evidence
```

Scope — exactly these three paths:

```text
.github/workflows/mesc-b2a-portability.yml
tests/_mesc_b2a_portability.py
tests/test_mesc_b2a_portability.py
```

Purpose: implement `FD-PV-14`; add strict SHA validation; ensure pull-request
envelopes omit `canonical_sha`; ensure dispatch envelopes contain the exact
guarded SHA; preserve deterministic serialization and the existing failure
taxonomy.

### Correction B

Recommended subject:

```text
fix(mesc): enforce bounded portability artifact extraction
```

Same three implementation paths only.

Purpose: implement `FD-PV-12` and `FD-PV-13`; replace automatic full extraction
with bounded artifact handling; enforce compressed limits before or during
transport; inspect ZIP entries before extraction; extract through bounded
chunked reads; enforce the exact extracted limits during extraction; remove the
invented per-file 1 MiB extracted limit; add real negative tests for every
safe-extraction guard; replace any tautological or non-executing safety test;
tighten tests that accept multiple unrelated error categories; preserve the
twenty-one-category ratified taxonomy; and introduce no dependency, lockfile,
`src/**`, dataset, model, or public-API change.

## Authorization boundary of this addendum

This addendum authorizes only its own governance record and the Draft pull
request that carries it. It does **not** authorize:

- any change to PR #61;
- workflow or helper implementation;
- the future synchronization merge commit;
- either correction commit;
- workflow rerun or `workflow_dispatch`;
- Ready transition, merge, or auto-merge;
- admissible evidence production;
- B2A acceptance or B2A execution;
- closure of the Windows or macOS obligations;
- B2B;
- branch deletion.

Each remains a separate founder act. `FD-PV-1` through `FD-PV-10`, `FD-B2A-1`
through `FD-B2A-8`, binding `N-12`, `D1`–`D10`, and `FD-B2-1` through `FD-B2-8`
are unamended except where `FD-PV-13` narrowly amends the permission rule.

B2A remains not accepted. B2B remains not authorized. P01-04B remains incomplete
and not accepted.
