# P01-04D Entry-Readiness Remediation — Founder Authorization

## Current-truth reconciliation note

This document is the controlling record of the PR #88 design-and-contract
decision, and of nothing else. Every state line it carries — including the
header block immediately below and section 17 — describes the FD-DREADY
issuance baseline of 2026-08-04.

```text
authority issued by this document:
DESIGN AND CONTRACT AUTHORITY ONLY — UNCHANGED

P01-04D implementation:
ADOPTED ON CANONICAL MAIN through PR #90; adoption truth reconciled
through PR #91

P01-04D entry:
AUTHORIZED by the separate founder decision of 2026-08-05, canonically
adopted through PR #92

P01-04D execution:
NOT AUTHORIZED
```

Those later decisions are separate and independent. They do not retroactively
expand, reinterpret or enlarge the authority issued by this document, and this
document did not grant them. Current implementation and entry status are
controlled by the later canonical records:

- [`canonical-adoption-record.md`](canonical-adoption-record.md) — PR #88
  design adoption;
- [`../p01-04d-formal-executor/canonical-adoption-record.md`](../p01-04d-formal-executor/canonical-adoption-record.md)
  — PR #90 implementation adoption, reconciled through PR #91;
- [`../p01-04d-entry-authorization/founder-authorization.md`](../p01-04d-entry-authorization/founder-authorization.md)
  — the founder entry decision adopted through PR #92.

Execution remains unauthorized. `FD-DREADY-1` through `FD-DREADY-12` are
unchanged in text and in meaning, and no line below has been rewritten.

```text
Package status:
CANONICALLY ADOPTED

Canonical adoption:
PR #88 merge c208085dfcdbf8f2cab5e9308f938bcc609260c5

Historical pre-merge package status:
RECORDED — NOT ADOPTED

FD-DREADY-1 THROUGH FD-DREADY-12:
ISSUED ON 2026-08-04

Decision class:
DESIGN AND CONTRACT AUTHORITY ONLY

P01-04D readiness blockers B-1 and B-2:
CONFIRMED

P01-04D remediation design:
AUTHORIZED

P01-04D implementation authority:
NOT ISSUED

P01-04D execution authority:
NOT ISSUED

P01-04D entry:
NOT AUTHORIZED

P01-03G registry access:
NOT AUTHORIZED

Real dataset access:
NOT AUTHORIZED
```

This document is the controlling record of this package. On any conflict between
this document and [`README.md`](README.md),
[`implementation-contract.md`](implementation-contract.md) or
[`acceptance.md`](acceptance.md), this document controls.

Canonical adoption does not expand the authority recorded here.

The post-merge canonical-adoption identity and verification record is:
[`canonical-adoption-record.md`](canonical-adoption-record.md)

---

## 1. Controlling authority

This package records twelve founder decisions, `FD-DREADY-1` through
`FD-DREADY-12`, issued on 2026-08-04. Their class is **design and contract
authority only**.

```text
design and contract remediation:
AUTHORIZED

implementation authority:
NOT ISSUED

execution authority:
NOT ISSUED
```

No identifier beyond `FD-DREADY-12` exists. No identifier may be renumbered,
remapped, merged, split or shifted. Each identifier appears exactly once as a
numbered decision section below, in ascending order.

## 2. Exact canonical baseline

```text
Required canonical main:
78bab082bde3b53cbdbd5f37109437b68ba2e5c5

Required tree:
9ca9a042f71fa6df09d73198698043719b770cf7

Ordered parent 1:
fe2dc1e6fe65d4823655f6d958cf3307629623ec

Ordered parent 2:
a9f789d04a54315ad9d68deeac173cce861cd8f8

Merge subject:
Merge pull request #87 from IamShehri/docs/mesc-p01-04c-post-merge-truth-reconciliation

Merge body:
docs(mesc): reconcile P01-04C canonical adoption
```

If canonical `origin/main` differs from the commit above, this package is not
applicable and no work proceeds.

## 3. Canonical state entering this decision

```text
P01-04B:
ACCEPTED AND CANONICALLY ADOPTED

P01-04C:
ACCEPTED AND CANONICALLY CLOSED

P01-04C post-merge truth reconciliation:
CANONICALLY ADOPTED

P01-04D entry-readiness review:
COMPLETE

P01-04D readiness verdict:
NOT READY

P01-04D implementation:
NOT AUTHORIZED

P01-04D execution:
NOT AUTHORIZED

P01-03G registry access:
NOT AUTHORIZED

Real dataset access:
NOT AUTHORIZED

Real split generation:
NOT AUTHORIZED

Real partition membership:
NOT AUTHORIZED

Canonical leakage execution:
NOT AUTHORIZED

P01-04 overall:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

P01-04B tooling acceptance and P01-04C synthetic fixture acceptance are both
bounded to private, fixture-only, synthetic-only, non-evidence tooling. Neither
acceptance grants entry to P01-04D.

## 4. The two confirmed readiness blockers

The founder-authorized P01-04D entry-readiness review returned **NOT READY** on
two blocking findings. Both are confirmed.

```text
B-1:
No controlled formal operator invocation path exists for Generation A and
Generation B.

B-2:
The P01-04A/E policy artifact inventory is not reconciled with the accepted
fixture-only implementation inventory.
```

`FD-DREADY-1` through `FD-DREADY-12` resolve B-1 and B-2 **at the design and
contract level only**. Resolution of a readiness blocker at the design level is
not entry, not implementation authority and not execution authority.

---

# FD-DREADY decisions

## 5. FD-DREADY-1 — Scope and authority

This package resolves P01-04D readiness blockers B-1 and B-2 at the design and
contract level only.

It does not:

```text
implement a formal executor
create an operator script
create a CLI command
open real inputs
create execution workspaces
generate artifacts
calculate partition membership
run leakage checks
authorize P01-04D entry
authorize P01-04D execution
```

The deliverable of this decision is documentation and contracts. No source
module, no test module, no script, no workflow, no dependency and no lockfile is
created or changed under this authority.

## 6. FD-DREADY-2 — Separate formal executor

Formal P01-04D execution shall use a new **private formal-execution component**.

It shall not reuse the fixture-only execution authority of:

```text
FixtureSplitFacade
_fixture_publication_v1
```

Existing fixture tooling remains:

```text
private
fixture-only
synthetic-only
non-evidence
unexported
unchanged
```

The accepted fixture surface is not widened, not re-scoped, not promoted and not
made executable against real inputs by this decision or by any future decision
that does not say so explicitly.

Reusable **pure primitives** may be called by the future formal executor only
after separate implementation authorization. Examples include:

```text
canonical serialization
fail-closed label joining
constrained apportionment
deterministic ranking
indivisible-group allocation
artifact fingerprint verification
metadata rejection
write-path validation
```

Permission to call a pure primitive is not permission to call the fixture
facade, and is not granted by this package.

## 7. FD-DREADY-3 — Controlled operator surface

The future supported operator interface shall be exactly:

```text
scripts/mesc_p01_04d_operator.py
```

It shall be a canonical repository-controlled script, not an improvised or
one-off script.

It shall not be:

```text
exported from medscale.mesc
registered as a medscale CLI subcommand
installed as a public console script
callable through an environment-variable activation switch
```

The future script shall provide exactly two operator commands:

```text
generate
compare
```

No third command. No alias, no hidden command, no debug command, no repair
command and no promotion command exists on this surface.

This decision resolves blocker **B-1** at the design level. The script does not
exist at this baseline and is not created under this authority.

## 8. FD-DREADY-4 — One generation per invocation

The future `generate` command shall execute exactly one generation per process.

Required generation identity:

```text
A
or
B
```

One invocation must never execute both generations.

Each invocation shall require explicit, safely parameterized operator inputs
for:

```text
expected canonical commit
read-only repository root
generation identity
fresh generation workspace
external evidence root
future evidence root
ordered-example registry
source-document registry
transformed-dataset identity
external source-records label source
ratified decision record
exact Python version
```

The operator must reject:

```text
workspace reuse
repository-root output
P01-03G output
future-evidence-root output
relative or unresolved protected-root aliases
unknown generation identity
missing expected commit
canonical commit movement
```

Every rejection is fail-closed and occurs before any mutation. The listed input
roles name parameters of a future interface; naming a role is not access to the
artifact that role would later designate.

## 9. FD-DREADY-5 — Comparison boundary

The future `compare` command shall run only after Generation A and Generation B
have terminated.

It shall:

```text
read completed A and B inventories
verify exact expected inventory
compare every D artifact byte-for-byte
recompute the authoritative split fingerprint
verify all descriptors and manifests
record the equality disposition externally
```

It shall not:

```text
repair an artifact
rewrite a generation workspace
copy one generation over the other
suppress an inequality
promote to the final evidence root
perform P01-04E leakage execution
```

Any inequality invalidates both candidates. An invalidated candidate is never
overwritten, never deleted and never modified in place.

## 10. FD-DREADY-6 — Exact P01-04D generation inventory

Each future Generation A and Generation B workspace shall contain exactly these
seven P01-04D candidate artifacts:

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

No eighth artifact.

No log, receipt, lock, marker, PID file, timestamp file or sidecar is part of
the deterministic generation bundle.

All seven files are compared byte-for-byte between Generation A and Generation
B.

This decision resolves the inventory half of blocker **B-2** at the design
level.

## 11. FD-DREADY-7 — Artifact-name supersession map

For formal P01-04D, the following earlier proposed names are superseded:

```text
example-split-registry.jsonl
->
example-registry.jsonl
```

```text
excluded-or-unassigned-ledger.json
->
excluded-ledger.json
```

```text
split-fingerprint.json
->
no standalone file
```

The authoritative full lowercase 64-hex `split_fingerprint` is carried and
verified through:

```text
split-summary.json
generation-manifest.json
```

The 16-hex `split_hash` remains compatibility/display-only. It is never the
authoritative fingerprint and never substitutes for the 64-hex value in any
verification.

The following are not P01-04D generation outputs:

```text
leakage-audit-report.json
leakage-audit.json
p01-04-closeout-record.json
publication-manifest.json
```

This decision resolves the naming half of blocker **B-2** at the design level.

## 12. FD-DREADY-8 — Stage separation

The exact stage boundaries are:

```text
P01-04D:
formal split generation candidate bundle
```

```text
P01-04E:
canonical leakage audit and finding resolution
```

```text
P01-04F:
freeze, independent verification and closeout record
```

```text
P01-04G:
separately authorized repository promotion
```

Therefore:

```text
leakage-audit.json:
P01-04E output, not P01-04D output

p01-04-closeout-record.json:
P01-04F output, not P01-04D output

publication-manifest.json:
existing fixture-only publication artifact;
not the formal P01-04D generation manifest

generation-manifest.json:
formal P01-04D candidate-bundle manifest
```

No stage may mutate an immutable artifact from an earlier stage. Later stages
reference earlier artifacts by stable identity.

## 13. FD-DREADY-9 — Formal policy snapshot

`split-policy.json` shall be deterministic and contain no runtime or
ratification date.

It shall bind exactly the versioned scientific policy needed for generation:

```text
schema version
algorithm version
partition order
exact target counts
grouping key
stratification field
label order
seed/domain separator
ranking-key schema
apportionment method
minimum partition sizes
canonical serialization rules
holdout policy
```

It shall contain:

```text
no floats where exact integer or rational representation is available
no timestamps
no local paths
no usernames
no hostnames
no commands
no environment values
```

## 14. FD-DREADY-10 — Formal generation manifest

`generation-manifest.json` shall be non-circular and deterministic.

It shall bind:

```text
schema version
algorithm version
generation-bundle filenames
surface identifiers
schema versions
SHA-256 digests
byte sizes
authoritative split fingerprint
input identity digests
```

It shall not contain:

```text
generation identity A or B
workspace path
process ID
timestamp
hostname
username
command line
external-evidence path
```

Generation A and Generation B must therefore produce identical manifest bytes
when all scientific inputs and code are identical.

Non-circular means the manifest carries no digest and no byte size of itself.

## 15. FD-DREADY-11 — Future implementation boundary

A later implementation authorization may permit only synthetic construction and
qualification of the controlled formal executor.

Implementation authorization shall remain separate from real execution
authorization.

Future implementation must not access:

```text
P01-03G registry content
external source-records.jsonl
real labels
real membership
```

The future implementation package must use synthetic formal-input fixtures that
exercise the same schemas and fail-closed paths.

No part of this decision issues that later implementation authorization.

## 16. FD-DREADY-12 — D1–D10 preservation

The remediation does not amend:

```text
D1 partition set
D2 exact 700 / 150 / 150 totals
D3 source_document_id grouping
D4 decision stratification
D5 constrained integer apportionment
D6 deterministic SHA-256 ranking
D7 minimum sizes
D8 no holdout
D9 public repository content boundary
D10 split-version policy
```

Scientific identity is unchanged. Only operator and artifact-contract ambiguity
is reconciled.

On any conflict between this package and D1–D10, **D1–D10 control**.

---

## 17. Historical controlling state at FD-DREADY issuance — superseded for current implementation and entry status

**Historical as of the FD-DREADY issuance baseline of 2026-08-04.** The block
below is preserved unrewritten. It was the controlling state when
`FD-DREADY-1` through `FD-DREADY-12` were issued, and it is not the current
governing status. Three of its lines have since been superseded —
`FORMAL OPERATOR SCRIPT`, `P01-04D IMPLEMENTATION` and `P01-04D ENTRY` — and
current truth is recorded in the block that follows it.

```text
P01-04D READINESS BLOCKERS B-1 AND B-2:
CONFIRMED

P01-04D REMEDIATION DESIGN:
AUTHORIZED

FD-DREADY-1 THROUGH FD-DREADY-12:
ISSUED ON 2026-08-04 AS DESIGN AND CONTRACT AUTHORITY ONLY

FORMAL OPERATOR SCRIPT:
scripts/mesc_p01_04d_operator.py — PROSPECTIVE, ABSENT AT THIS BASELINE

OPERATOR COMMANDS:
generate
compare

P01-04D CANDIDATE ARTIFACT COUNT:
7

STANDALONE FINGERPRINT FILE:
NONE

P01-04E AUDIT FILENAME:
leakage-audit.json

P01-04F CLOSEOUT FILENAME:
p01-04-closeout-record.json

FIXTURE PUBLICATION MANIFEST:
publication-manifest.json

FORMAL P01-04D GENERATION MANIFEST:
generation-manifest.json

P01-04D IMPLEMENTATION:
NOT AUTHORIZED

P01-04D EXECUTION:
NOT AUTHORIZED

P01-04D ENTRY:
NOT AUTHORIZED

P01-03G REGISTRY ACCESS:
NOT AUTHORIZED

EXTERNAL SOURCE-RECORD ACCESS:
NOT AUTHORIZED

REAL DATASET ACCESS:
NOT AUTHORIZED

REAL SPLIT GENERATION:
NOT AUTHORIZED

REAL PARTITION MEMBERSHIP:
NOT AUTHORIZED

CANONICAL LEAKAGE EXECUTION:
NOT AUTHORIZED

P01-04 OVERALL:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

### 17A. Current controlling state

This block records current governing truth. It issues no authority and expands
nothing granted by this package.

```text
FORMAL OPERATOR SCRIPT:
scripts/mesc_p01_04d_operator.py — PRESENT AND CANONICALLY ADOPTED

P01-04D IMPLEMENTATION:
ADOPTED ON CANONICAL MAIN THROUGH PR #90

FORMAL-EXECUTOR ADOPTION TRUTH:
CANONICALLY RECONCILED THROUGH PR #91

FOUNDER P01-04D ENTRY AUTHORIZATION:
ISSUED ON 2026-08-05 AND CANONICALLY ADOPTED THROUGH PR #92

CANONICAL ENTRY-AUTHORIZATION MERGE:
693c900bbe5e0f752ca915b527c89d1d9aaa43ad

P01-04D ENTRY:
AUTHORIZED

P01-04D CONTROL STATE:
ENTERED — PRE-EXECUTION GOVERNANCE ONLY

P01-04D EXECUTION:
NOT AUTHORIZED

P01-03G REGISTRY CONTENT ACCESS:
NOT AUTHORIZED

EXTERNAL REAL SOURCE-RECORD ACCESS:
NOT AUTHORIZED

REAL DATASET ACCESS:
NOT AUTHORIZED

GENERATION A:
NOT AUTHORIZED

GENERATION B:
NOT AUTHORIZED

COMPARE:
NOT AUTHORIZED

P01-04E THROUGH P01-04G EXECUTION:
NOT AUTHORIZED

P01-04 OVERALL:
NOT COMPLETE

P01-05:
NOT UNLOCKED

CURRENT NEXT GATE:
P01-04D EXECUTION-AUTHORIZATION READINESS RE-EVALUATION
```

The operator-contract lines in the historical block above — operator commands,
candidate artifact count, standalone fingerprint file, P01-04E and P01-04F
filenames, fixture publication manifest and formal generation manifest — are
unchanged and remain current.

## 18. Continuing prohibitions

The list below is the scope of authority issued by the PR #88 package: none of
these actions was authorized by this document, and this document authorized
neither P01-04D entry nor P01-04D execution.

**Superseded within this list.** `P01-04D entry` was subsequently authorized by
a separate founder decision of 2026-08-05, canonically adopted through PR #92.
That later decision is not an authority of this package. `P01-04D entry` is
therefore no longer currently prohibited, and it is preserved in the list only
as a record of what this package withheld.

Every other item in the list remains prohibited as current truth, including
implementation execution, formal executor invocation, P01-03G registry access,
external source-record access, real-data access, real split generation, real
partition membership, canonical leakage execution, generation workspace
creation, split artifact generation, evidence and repository promotion,
publication, model or weight access, inference, training, fine-tuning, and
P01-04D execution through P01-04G.

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

## 19. Historical non-execution record at the FD-DREADY baseline

**Historical as of the FD-DREADY issuance baseline of 2026-08-04.** The record
below is preserved unrewritten with its original values. It describes what the
PR #88 package itself did, and it is not the current status. Current truth
follows it.

```text
formal executor implemented:            NO
operator script created:                NO
CLI command created:                    NO
generation workspace created:           NO
split artifact generated:               NO
partition membership calculated:        NO
leakage check executed:                 NO
P01-03G registry content accessed:      NO
external source-records.jsonl accessed: NO
real dataset accessed:                  NO
evidence published:                     NO
prior governance package modified:      NO
D1 through D10 amended:                 NO
```

A later, separately governed implementation decision is eligible for founder
consideration.

```text
ELIGIBILITY IS NEVER AUTHORITY.
```

### 19A. Current non-execution record

```text
formal executor implemented:
YES — CANONICALLY ADOPTED THROUGH PR #90

operator script created:
YES — CANONICALLY ADOPTED THROUGH PR #90

protected input opened:
NO

generation workspace created:
NO

Generation A executed:
NO

Generation B executed:
NO

compare executed:
NO

split artifact generated:
NO

partition membership calculated:
NO

P01-04E leakage execution:
NO
```

The adopted executor exists as canonical repository code and has been exercised
only against freshly generated synthetic fixtures under temporary directories.
It has never been run against a protected P01-03G input, the external real
`source-records.jsonl` or any real dataset, and P01-04D execution remains
unauthorized.
