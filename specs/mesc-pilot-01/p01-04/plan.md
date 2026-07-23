# MESC Pilot-01 — P01-04 Plan

Status: **specification and policy only — no execution authorized**

---

## Phase overview

| Stage | Name | Authorization required | Current status |
|-------|------|----------------------|----------------|
| P01-04A | Specification and Policy Ratification | Founder ratification | **Ratified** |
| P01-04B | Split Contracts and Tooling | Separate founder authorization | Incomplete; B1 adopted privately; B2 specification in preparation |
|| P01-04B1 | Pure deterministic split core | Adopted on canonical main (`2937d73`) | **ADOPTED** — private, in-memory, fixture-only; execution authority: none |
|| P01-04B2 | Remaining tooling entry gate | Separate founder authorization | **SPECIFICATION ONLY** — implementation not authorized; execution not authorized |
|| P01-04B acceptance | Tooling complete and accepted | **NOT MET** |
| P01-04C | Fixture and Dry-Run Qualification | Separate founder authorization | Not authorized |
| P01-04D | Formal Split Generation | Separate founder authorization | Not authorized |
| P01-04E | Leakage Audit and Finding Resolution | Separate founder authorization | Not authorized |
| P01-04F | Freeze and Independent Acceptance | Separate founder authorization | Not authorized |
| P01-04G | Repository Promotion and Closeout | Separate promotion authorization | Not authorized |

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

P01-04B and later produce:

- `split-policy.json`
- `group-registry.jsonl`
- `example-split-registry.jsonl`
- `split-summary.json`
- `split-fingerprint.json`
- `leakage-audit-report.json`
- `excluded-or-unassigned-ledger.json`
- `p01-04-closeout-record.json`

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
