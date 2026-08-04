# P01-04D Entry-Readiness Remediation

```text
Package status:
RECORDED — NOT ADOPTED

FD-DREADY-1 THROUGH FD-DREADY-12:
ISSUED ON 2026-08-04

Decision class:
DESIGN AND CONTRACT AUTHORITY ONLY

P01-04D readiness blockers B-1 and B-2:
CONFIRMED

P01-04D remediation design:
AUTHORIZED

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-04D entry:
NOT AUTHORIZED
```

This README is **descriptive**.
[`founder-authorization.md`](founder-authorization.md) **controls**.

## The problem

P01-04B tooling is accepted and canonically adopted. P01-04C synthetic fixture
qualification is accepted and canonically closed, and its post-merge truth
reconciliation is canonically adopted. The next scientific stage, P01-04D formal
split generation, was therefore submitted to a founder-authorized entry-readiness
review.

That review completed with the verdict **NOT READY** on two blocking findings.
Both concern governance surface, not scientific policy: the project had ratified
*what* a formal split must be without ever fixing *how* an operator would run one
or *exactly which files* one produces.

This package resolves both findings at the design and contract level. It does
not perform P01-04D, and it does not implement the formal executor.

## The two blockers

```text
B-1:
No controlled formal operator invocation path exists for Generation A and
Generation B.

B-2:
The P01-04A/E policy artifact inventory is not reconciled with the accepted
fixture-only implementation inventory.
```

```text
B-1 resolved at design level by:
FD-DREADY-2, FD-DREADY-3, FD-DREADY-4, FD-DREADY-5

B-2 resolved at design level by:
FD-DREADY-6, FD-DREADY-7, FD-DREADY-8, FD-DREADY-9, FD-DREADY-10
```

Design-level resolution of a readiness blocker is not entry, not implementation
authority and not execution authority.

## Founder decisions

```text
FD-DREADY-1   scope and authority — design and contracts only
FD-DREADY-2   a separate private formal executor; fixture tooling
              untouched and never reused for formal execution
FD-DREADY-3   one controlled operator surface; exactly two commands
FD-DREADY-4   one generation per invocation; explicit inputs;
              fail-closed rejections
FD-DREADY-5   comparison boundary; any inequality invalidates both
              candidates
FD-DREADY-6   the exact seven-file P01-04D generation inventory
FD-DREADY-7   the artifact-name supersession map
FD-DREADY-8   stage separation across P01-04D, E, F and G
FD-DREADY-9   deterministic, date-free formal policy snapshot
FD-DREADY-10  non-circular, identity-free formal generation manifest
FD-DREADY-11  future implementation boundary — synthetic only
FD-DREADY-12  D1 through D10 preserved unchanged
```

[`founder-authorization.md`](founder-authorization.md) carries the exact meaning
of each identifier and controls. No identifier beyond `FD-DREADY-12` exists, and
none may be renumbered, remapped, merged or shifted.

## Exact formal operator surface

```text
script:
scripts/mesc_p01_04d_operator.py

commands:
generate
compare

command count:
2
```

Prospective only. The script does not exist at this baseline and is not created
by this package.

It shall be a canonical repository-controlled script — never an improvised
one-off — and shall not be exported from `medscale.mesc`, registered as a
`medscale` CLI subcommand, installed as a public console script, or reachable
through an environment-variable activation switch.

`generate` runs exactly one generation per process, with generation identity
exactly `A` or `B`; one invocation never runs both. `compare` runs only after
both generations have terminated, compares all seven artifacts byte-for-byte,
recomputes the authoritative split fingerprint, and records the disposition
externally. It never repairs, rewrites, copies, suppresses or promotes.

## Exact seven-file D inventory

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
sidecar belongs to the deterministic bundle. All seven are compared byte-for-byte
between Generation A and Generation B.

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

## Stage separation

```text
P01-04D   formal split generation candidate bundle
P01-04E   canonical leakage audit and finding resolution
P01-04F   freeze, independent verification and closeout record
P01-04G   separately authorized repository promotion
```

```text
leakage-audit.json            P01-04E output, not P01-04D output
p01-04-closeout-record.json   P01-04F output, not P01-04D output
publication-manifest.json     existing fixture-only publication artifact;
                              not the formal P01-04D generation manifest
generation-manifest.json      formal P01-04D candidate-bundle manifest
```

No stage may mutate an immutable artifact from an earlier stage. Later stages
reference earlier artifacts by stable identity.

## Future implementation boundary

A later implementation authorization, if the founder issues one, may permit only
**synthetic** construction and qualification of the controlled formal executor,
bounded to exactly six prospective paths:

```text
src/medscale/mesc/_formal_split_v1.py
src/medscale/mesc/_formal_generation_v1.py
scripts/mesc_p01_04d_operator.py
tests/test_mesc_formal_split_v1.py
tests/test_mesc_formal_generation_v1.py
tests/test_mesc_p01_04d_operator.py
```

All six are prospective only and remain absent or unchanged at this baseline.

```text
implementation authorization:
SEPARATE FROM REAL EXECUTION AUTHORIZATION

future implementation access to P01-03G registry content,
external source-records.jsonl, real labels or real membership:
PROHIBITED
```

[`implementation-contract.md`](implementation-contract.md) records the
prospective types and typed errors without implementing them.

## Scientific identity

```text
D1 through D10:
UNCHANGED
```

The remediation reconciles operator and artifact-contract ambiguity only. On any
conflict between this package and D1–D10, D1–D10 control.

## Continuing prohibitions

```text
source changes                     test changes
script changes                     workflow changes
dependency or lockfile changes     implementation
formal executor construction       operator script construction
public export                      CLI registration
console-script installation        environment activation switch
network                            subprocess
clock                              randomness
P01-03G registry access            external source-record access
real-data access                   real-data adapter
real split generation              real partition membership
canonical leakage execution        leakage-audit orchestration
dataset or registry scanning       record-pair discovery
generation workspace creation      split artifact generation
evidence-root promotion            repository-root promotion
model or weight access             inference
retrieval                          metrics
benchmark execution                training
fine-tuning                        adapter creation
publication                        clinical use
P01-04D entry                      P01-04D through P01-04G
P01-05 or later
```

## Authority hierarchy

```text
1. founder-authorization.md   controlling
2. implementation-contract.md prospective future implementation contract
3. acceptance.md              this package's documentation gate
4. README.md                  overview only
```

On any conflict, [`founder-authorization.md`](founder-authorization.md)
controls. `README.md` never controls.

## Document index

- [`README.md`](README.md) — this overview, descriptive only
- [`founder-authorization.md`](founder-authorization.md) — **controlling**
- [`implementation-contract.md`](implementation-contract.md) — prospective future
  implementation contract
- [`acceptance.md`](acceptance.md) — this package's documentation gate

Prior governance history is adopted at
[`../p01-04/`](../p01-04/),
[`../p01-04b2/`](../p01-04b2/),
[`../p01-04b-publication-boundary-authorization/`](../p01-04b-publication-boundary-authorization/)
and
[`../p01-04c-fixture-qualification/`](../p01-04c-fixture-qualification/),
and is not restated here.

## Next gate

```text
NEXT GATE:

INDEPENDENT CLEAN-ROOM REVIEW OF THE EXACT P01-04D
ENTRY-READINESS REMEDIATION DESIGN COMMIT

NO PUSH
NO PR
NO IMPLEMENTATION
NO P01-04D EXECUTION
NO P01-03G ACCESS
NO REAL DATASET ACCESS
```

A later, separately governed implementation decision is eligible for founder
consideration.

```text
ELIGIBILITY IS NEVER AUTHORITY.
```
