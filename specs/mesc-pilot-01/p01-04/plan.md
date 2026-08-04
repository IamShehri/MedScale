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

P01-04D:
NOT AUTHORIZED

P01-04D entry-readiness review:
COMPLETE — ORIGINAL VERDICT NOT READY

P01-04D readiness blockers B-1 and B-2:
RESOLVED AT DESIGN AND CONTRACT LEVEL

P01-04D remediation design:
CANONICALLY ADOPTED

formal operator design:
RATIFIED

formal operator implementation:
NOT AUTHORIZED / NOT IMPLEMENTED

P01-04D entry:
NOT AUTHORIZED
```

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

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

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

It does not exist at this baseline.

```text
P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED
```

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
