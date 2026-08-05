# MESC Pilot-01 — P01-04 Plan

Status: **specification and policy only — no execution authorized**

---

## Phase overview

### Historical phase table — SUPERSEDED FOR CURRENT STATUS

The table below is the original P01-04A phase table. It is preserved unrewritten
as a truthful historical record of the baseline it describes. It is superseded
for current status by the **Current maintenance disposition** section further
below. No row in it has been edited.

| Stage | Name | Authorization required | Current status |
|---|---|---|---|
| P01-04A | Specification and Policy Ratification | Founder ratification | **Ratified** |
| P01-04B | Split Contracts and Tooling | Separate founder authorization | Incomplete; B1 adopted; B2 design ratified; B2A–B2D not authorized |
| P01-04B1 | Pure deterministic split core | Adopted by PR #51 merge `2937d735df09851384bfa9a15fb8b1f908c62b6d` | **ADOPTED** — private, in-memory, fixture-only; execution authority: none |
| P01-04B2 | Remaining tooling design gate | Founder-ratified FD-B2-1 through FD-B2-8 | **DESIGN RATIFIED** — implementation and execution not authorized |
| P01-04B acceptance | Tooling complete and accepted | Separate founder acceptance | **NOT MET** |
| P01-04C | Fixture and Dry-Run Qualification | Separate founder authorization | Not authorized |
| P01-04D | Formal Split Generation | Separate founder authorization | Not authorized |
| P01-04E | Leakage Audit and Finding Resolution | Separate founder authorization | Not authorized |
| P01-04F | Freeze and Independent Acceptance | Separate founder authorization | Not authorized |
| P01-04G | Repository Promotion and Closeout | Separate promotion authorization | Not authorized |

### Current maintenance note

The P01-04A row above preserves the historical identity of the ratified policy
phase. This document is currently maintained under the broader P01-04 record
on canonical baseline
`ce1272235cb48dbacdb18f20e1ae8db695b01328`.

The current maintenance context does not replace the original P01-04A
ratification identity or authority.

### Current maintenance disposition

This section is the current controlling status of the phase overview. It
supersedes the historical phase table above for current status only. It records
no new scientific policy and amends no ratified decision.

```text
P01-04B:
ACCEPTED AND CANONICALLY ADOPTED

P01-04C:
ACCEPTED AND CANONICALLY CLOSED

P01-04D original entry-readiness review:
COMPLETE — ORIGINAL VERDICT NOT READY

B-1:
CLOSED AT IMPLEMENTATION LEVEL

B-2:
CLOSED AT IMPLEMENTATION LEVEL

P01-04D remediation design:
CANONICALLY ADOPTED

formal operator design:
RATIFIED

formal operator implementation code:
CANONICALLY ADOPTED

formal-executor adoption truth:
CANONICALLY RECONCILED

formal executor correction findings F1 / F2 / F3:
CLOSED

entry-readiness re-evaluation:
READY FOR FOUNDER ENTRY DISPOSITION

founder P01-04D entry authorization:
ISSUED ON 2026-08-05

P01-04D entry:
AUTHORIZED

P01-04D control state:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D execution:
NOT AUTHORIZED

P01-04E through P01-04G:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

The founder entry decision is recorded in
[`../p01-04d-entry-authorization/founder-authorization.md`](../p01-04d-entry-authorization/founder-authorization.md).
Entry moves P01-04D into a controlled pre-execution governance state only. It
grants no execution authority, opens no protected input, creates no generation
workspace and permits neither `generate` nor `compare` to be invoked. A separate
founder execution authorization is required before any protected input may be
opened or any generation command may run. P01-04D is neither executed nor
complete.

The earlier line `P01-04D readiness blockers B-1 and B-2: RESOLVED AT DESIGN AND
CONTRACT LEVEL` was true after the remediation design was adopted, and the
earlier line `P01-04D entry-readiness re-evaluation: NOT YET AUTHORIZED` was
true before that re-evaluation was authorized. Both are superseded for current
status by the block above, in which P01-04D execution remains `NOT AUTHORIZED`.

The formal-executor implementation code was adopted on canonical main through
PR #90, merge `e924027f1c8ea08ac4e5e4281fdcf75e5b419693`, whose tree is
identical to the independently reviewed implementation head
`962a5ef432c14aa74940e018373168f46a299669` and its tree
`d5b51ee1569c30b0866e24c65fd15a77836787e5`. The canonical implementation
adoption record is
[`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md).

Adoption of executor code is not P01-04D readiness, not entry authorization and
not execution authorization. **Historical as of the adoption-truth
reconciliation.** The original entry-readiness verdict is unchanged, and a
separately authorized entry-readiness re-evaluation is required before any entry
decision.

That re-evaluation was subsequently authorized and returned
`READY FOR FOUNDER ENTRY DISPOSITION`, and the founder issued P01-04D entry
authorization on 2026-08-05; see
[`../p01-04d-entry-authorization/entry-readiness-re-evaluation.md`](../p01-04d-entry-authorization/entry-readiness-re-evaluation.md).
The original entry-readiness verdict remains unchanged and historical.

The earlier disposition line `P01-04D: NOT AUTHORIZED` — and the earlier
`formal operator implementation: NOT AUTHORIZED / NOT IMPLEMENTED` — were true
before PR #90. They are superseded for current status by the block above, in
which P01-04D entry and P01-04D execution both remain `NOT AUTHORIZED`.

The remediation design was adopted on canonical main through PR #88, merge
`c208085dfcdbf8f2cab5e9308f938bcc609260c5`, whose tree is identical to the
independently reviewed remediation head
`8aa599e1eae0f53726ef63f08886cf2ba67c188e` and its tree
`530808443825e080b75177f70943ca201efe16b8`. The post-merge canonical-adoption
identity and verification record is
[`../p01-04d-entry-readiness-remediation/canonical-adoption-record.md`](../p01-04d-entry-readiness-remediation/canonical-adoption-record.md).

The two blocking findings returned by the founder-authorized P01-04D
entry-readiness review are:

```text
B-1:
No controlled formal operator invocation path exists for Generation A and
Generation B.

B-2:
The P01-04A/E policy artifact inventory is not reconciled with the accepted
fixture-only implementation inventory.
```

Both are resolved at the design and contract level by `FD-DREADY-1` through
`FD-DREADY-12`, recorded in
[`../p01-04d-entry-readiness-remediation/founder-authorization.md`](../p01-04d-entry-readiness-remediation/founder-authorization.md).
Design-level resolution is not entry, not implementation authority and not
execution authority.

Historical as of the remediation-design adoption:

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

The `P01-04D implementation` line above was true when the remediation design was
adopted. Implementation was subsequently authorized and the code canonically
adopted through PR #90; see
[`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md).
`P01-04D execution: NOT AUTHORIZED` remains current and in force.

No P01-04 stage authorizes P01-05.

## Prerequisites

P01-04 of any stage requires:

1. P01-03G promotion merged to canonical main.
2. P01-03G ordered example registry present and valid on canonical main.
3. P01-03G source-document registry present and valid on canonical main.
4. Founder ratification of split policy, ratios, grouping invariant, stratification, leakage taxonomy.
5. Founder authorization for P01-04B (tooling) before any split generation.

## Outputs

P01-04A produces:

- `specs/mesc-pilot-01/p01-04/README.md`
- `specs/mesc-pilot-01/p01-04/plan.md`
- `specs/mesc-pilot-01/p01-04/spec.md`
- `specs/mesc-pilot-01/p01-04/decision-record.md`
- `specs/mesc-pilot-01/p01-04/acceptance.md`
- `specs/mesc-pilot-01/p01-04/execution-protocol.md`
- `specs/mesc-pilot-01/p01-04/artifact-contracts.md`
- `specs/mesc-pilot-01/p01-04/data-model.md`

### Historical P01-04A proposed downstream inventory — SUPERSEDED FOR CURRENT FORMAL STAGE CONTRACTING

The list below is the original undifferentiated "P01-04B and later produce"
inventory. It is preserved unrewritten as a historical P01-04A proposal. It is
superseded for current formal stage contracting by the stage-scoped contracts
that follow, and it must not be read as the formal P01-04D inventory.

P01-04B and later produce:

- `split-policy.json`
- `group-registry.jsonl`
- `example-split-registry.jsonl`
- `split-summary.json`
- `split-fingerprint.json`
- `leakage-audit-report.json`
- `excluded-or-unassigned-ledger.json`
- `p01-04-closeout-record.json`

### Current stage-scoped output contracts

These are the current contracts. They supersede the historical proposal above
for current formal stage contracting. Nothing here is produced: no stage below
P01-04D or above is authorized to execute.

**P01-04D — formal split generation candidate bundle.** Each Generation A and
Generation B workspace contains exactly these seven candidate artifacts:

```text
split-policy.json
group-registry.jsonl
example-registry.jsonl
excluded-ledger.json
split-summary-identity-core.json
split-summary.json
generation-manifest.json
```

```text
P01-04D artifact count:
7
```

No eighth artifact. No log, receipt, lock, marker, PID file, timestamp file or
sidecar belongs to the deterministic bundle. All seven are compared
byte-for-byte between Generation A and Generation B.

Superseded names:

```text
example-split-registry.jsonl       ->  example-registry.jsonl
excluded-or-unassigned-ledger.json ->  excluded-ledger.json
split-fingerprint.json             ->  no standalone file
```

```text
standalone fingerprint file:
none
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through `split-summary.json` and `generation-manifest.json`. The 16-hex
`split_hash` is compatibility/display-only.

**P01-04E — canonical leakage audit and finding resolution.** Output:

```text
leakage-audit.json
```

**P01-04F — freeze, independent verification and closeout record.** Output:

```text
p01-04-closeout-record.json
```

**P01-04G — separately authorized repository promotion.** Produces no new
scientific artifact; it is a promotion boundary only.

**Existing fixture-only publication inventory.** The accepted fixture-only
publication manifest is:

```text
publication-manifest.json
```

It is not the formal P01-04D generation manifest. The formal P01-04D
candidate-bundle manifest is `generation-manifest.json`.

The single supported prospective operator surface for P01-04D is:

```text
scripts/mesc_p01_04d_operator.py

commands:
generate
compare
```

Historical as of the remediation-design adoption: it does not exist at this
baseline.

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

Both statements above were true when the remediation design was adopted. The
operator script and the two private formal modules now exist on canonical main,
and the implementation code was canonically adopted through PR #90; see
[`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md).
`P01-04D execution: NOT AUTHORIZED` remains current and in force, so the
operator has never been run against a protected or real input.

No future stage produces real partition membership until founder authorization explicitly permits it.

## Gates

Each stage transition requires explicit founder authorization. Authorization for an earlier stage does not automatically authorize a later stage.

## Stop conditions

Stop without mutation if:

- the canonical main SHA does not match the exact SHA recorded in the applicable founder execution authorization;
- P01-03G artifacts have changed;
- any documentation contradicts a ratified decision;
- a document claims execution has started;
- a document claims leakage has been ruled out;
- a document includes source-data redistribution claims not in the canonical rights record;
- any unauthorized path is modified.
