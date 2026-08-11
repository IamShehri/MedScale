# P-A2 External Execution-Evidence Harness — Implementation Acceptance

Status: **local implementation candidate — not canonically adopted, no execution
authorized**

This document records the actual implementation truth of the P-A2 build. It is
governed by [`founder-authorization.md`](founder-authorization.md) and
[`evidence-contract.md`](evidence-contract.md), which control on any conflict.

## 1. P-A2 scope

```text
Package:
P-A2 — P01-04D EXTERNAL EXECUTION-EVIDENCE HARNESS IMPLEMENTATION

Blocker:
XD-EXEC-1 — external execution-evidence recording

Blocker state:
DECIDED / OPEN

Package class:
IMPLEMENTATION AND SYNTHETIC QUALIFICATION ONLY

Build class:
LOCAL CORRECTION CANDIDATE — NOT PUSHED, NOT PUBLISHED, NOT ADOPTED

P01-04D execution:
NOT AUTHORIZED
```

P-A2 implements the harness defined by P-A1. It executes no scientific episode,
opens no protected input and invokes the canonical operator zero times.

### 1.1 Correction rebuild

This candidate is a **correction rebuild**. An earlier candidate was built,
independently reviewed and rejected for publication.

```text
historical candidate:
94b22c9b2f99d6105ef00793b92519002345b75a

historical tree:
112dc95a683e52b445545b6d11a3762897a3132a

historical disposition:
REVIEWED — CHANGES REQUIRED — NOT APPROVED FOR PUBLICATION

correction reason:
PA2-R1 — BLOCKING review finding

additional founder-authorized corrections:
PA2-R2, PA2-R3, PA2-R6

historical candidate status:
PRESERVED UNCHANGED AS LOCAL REVIEW EVIDENCE — never amended, reset, rewritten,
deleted or published
```

The corrected candidate is a fresh single commit built directly from the same
canonical baseline, not a rebase, amend or cherry-pick of the historical
candidate. The historical implementation bytes were materialized into the new
worktree by exact Git blob identity and then corrected; §1.2 records the exact
implemented behaviour of each correction.

Review observations `PA2-R4`, `PA2-R5`, `PA2-R7`, `PA2-R8`, `PA2-R9` and
`PA2-R10` were explicitly **not** authorized for correction at this gate and are
unchanged. No opportunistic cleanup, refactoring or renaming was performed.

### 1.2 Exact implemented correction behaviour

All three production corrections are confined to two functions:
`require_scientific_continuation` and `command_invalidate`. No command, evidence
record class, schema field, enumeration, enumeration value, terminal disposition,
sidecar, marker or persisted state was added.

**`PA2-R1` — durable invalidation is a scientific-continuation barrier.**

```text
any valid durable event in episode-invalidation.jsonl
-> generate REFUSE, compare REFUSE, verify REFUSE

invalidation bytes malformed, or present with zero durable events
-> REFUSE identically, as unsafe to interpret; never repaired

invalidate:  still permitted — its own contract still governs it
finalize:    still permitted under the existing containment and
             terminalization rules, so EPISODE_INVALIDATED stays reachable
```

The barrier is **derived** from the exact existing evidence bytes at read time.
It is evaluated inside the PRE-STAGE gate, so the refusal happens before
protected-input hashing, before any generation workspace is inspected or
created, before any child process is launched, before any scientific comparison
or verification, and before the stage journal for the attempted continuation is
created. There is no automatic re-pin, resume, repair or new episode.

Terminal precedence is unchanged: evidence corruption still outranks
invalidation, so an invalidated episode that also carries corrupt evidence still
seals `EPISODE_EVIDENCE_CORRUPT`.

**`PA2-R2` — a stage journal that never durably opened is a barrier.**

```text
stage journal exclusively created:            SUCCEEDS
first required stage_opened append:           does not durably succeed
resulting residue, for example a zero-byte journal
-> exact bytes preserved
-> stage_opened, stage_failed and stage_sealed all absent and never fabricated
-> no delete, truncate, rewrite, repair, backfill or rename
-> every later generate, compare and verify in that episode REFUSES
```

A journal whose required first `stage_opened` event never durably landed cannot
represent a valid completed scientific predecessor, so it bars continuation. The
residue is deliberately **not** described as structurally unsealed: the canonical
structural-unseal definition requires `stage_opened` to exist, and that
definition is unchanged. The barrier is derived from the bytes; nothing named
`stage_open_failed`, `continuation_blocked`, `residue_state` or any equivalent is
persisted.

`finalize` still binds the exact existing bytes read-only under the existing
manifest rules — `record_integrity` `WELL_FORMED` with the actual
`event_count` — mutates nothing, invents no terminal value, and can never yield
`EPISODE_COMPLETE_EQUAL` because of this residue.

The already-canonical barriers for `STAGE_REFUSED`, `STAGE_FAILED`, structural
unseal and malformed evidence are preserved unchanged, and a valid
`STAGE_COMPLETE` predecessor still permits the next contract-permitted stage.

**`PA2-R3` — controlled pre-mutation argument refusal.**

```text
invalidate --failure-class CHILD_NONZERO_EXIT
with --operator-error-class missing or outside the closed enumeration
-> ArgumentRefusalError, the existing harness argument-refusal surface

no episode-invalidation.jsonl creation
no append
no repository mutation
no uncaught ValueError
no traceback
```

The refusal is raised before the invalidation record is created or appended, so
it is strictly pre-mutation. An out-of-enumeration value supplied on the command
line is additionally refused by the existing parser `choices` surface with exit
code 2. `derive_failure_triad`'s closed tables are **not** weakened: the function
still raises on an absent or non-enumerated `operator_error_class`, and that
internal contract is asserted directly by test.

### 1.3 Greptile supplemental security review and correction

The `2f1fb05f` candidate of §1.1 was published as Draft PR #97 and then received
Greptile supplemental review at that exact head.

```text
reviewed PR:              97
reviewed head:            2f1fb05f8d10dc0f23a63942665fbd416b1fc25b
Greptile P1 findings:     3
independent validation:   ALL THREE CONFIRMED BLOCKING
published 2f1fb05f:       NOT READY FOR READY-TRANSITION OR ADOPTION
```

The three findings are path-safety defects in the harness, all of which allowed
a redirect or an escape to be honoured rather than refused:

```text
GREPTILE-G1  a symbolic HEAD reference was joined to the metadata base with
             ordinary Path semantics, so an absolute reference replaced that
             base and a parent-traversing reference escaped it

GREPTILE-G2  a relative gitdir or commondir path was resolved before it was
             inspected, so Path.resolve erased the very reparse components the
             harness is required to refuse

GREPTILE-G3  only the external evidence root was validated, so an episode
             directory that had become a reparse redirect was followed for
             evidence reads and writes
```

Independent validation reproduced all three against the unchanged published
parent. Each yielded a concrete compromise, not a theoretical one:

```text
G1  the harness returned an attacker-controlled commit, read from a file
    outside the repository, as canonical repository identity
G2  a junctioned gitdir produced the same attacker-controlled identity
G3  finalize completed and wrote episode-manifest.json outside the validated
    external evidence root
```

Against the corrected candidate the same three probes are refused —
`PathSeparationRefusalError`, `ReparsePointRefusalError` and
`ReparsePointRefusalError` respectively — and nothing is written outside the
evidence root. The exact implemented behaviour is recorded in §15.1.

```text
correction class:                     SECURITY CORRECTION
new evidence record / field / enum:   NONE
new command:                          NONE
new terminal disposition:             NONE
canonical adoption:                   NONE
execution authorization:              NONE
```

This correction changes no governance state. The published `2f1fb05f` candidate
and its review history are not rewritten; they remain the truthful record of what
was published and what review then found.

## 2. Baseline commit and tree

```text
Canonical main at build time:
c75df5bc08937f1ec19bad5aae4c2dc66b22f54e

Canonical tree:
6e42f58c7e3517cba0f0821fa0cd591026a2322e

Baseline verified live:
git ls-remote origin refs/heads/main — exact match, before the correction
worktree was created and again immediately before the correction commit

Isolated correction worktree:
C:\MedScaleTmp\pa2-evidence-harness-correction-20260810-01

Local branch:
fix/mesc-p01-04d-evidence-harness-review-corrections

Historical worktree and branch, preserved untouched:
C:\MedScaleTmp\pa2-evidence-harness-20260810
feat/mesc-p01-04d-evidence-harness
```

The correction worktree was created from that exact commit. Neither the
correction branch nor the correction worktree existed beforehand, locally or
remotely.

## 3. The three added paths

```text
added:     3
modified:  0
deleted:   0
renamed:   0
outside allowlist: 0
```

| Path | Role |
|------|------|
| `scripts/mesc_p01_04d_evidence_harness.py` | The production harness. |
| `tests/test_mesc_p01_04d_evidence_harness.py` | Synthetic-only qualification. |
| `specs/mesc-pilot-01/p01-04d-execution-evidence-harness/implementation-acceptance.md` | This document. |

No fourth repository path was created. No dependency, lockfile, packaging,
workflow or configuration file was touched.

## 4. Frozen implementation ledger

Verified read-only at the canonical baseline before implementation, and again at
the candidate commit.

| Path | Expected blob | Result |
|------|---------------|--------|
| `scripts/mesc_p01_04d_operator.py` | `c1010c8ec227312e5b86e2599b1365ae4f2be4f4` | EXACT |
| `src/medscale/mesc/_formal_generation_v1.py` | `cc23fbffbce4ccb87a36136c1cd13ee0b6f42fb4` | EXACT |
| `src/medscale/mesc/_formal_split_v1.py` | `7b921f915282d4d970af1ad8adff61ef6ca5be7a` | EXACT |
| `tests/test_mesc_formal_generation_v1.py` | `3db877fb123c895c0bf3c196f39cdb05f8c15ac2` | EXACT |
| `tests/test_mesc_formal_split_v1.py` | `e1c190a965a68c45cb587392447eb6a500bfbd47` | EXACT |
| `tests/test_mesc_p01_04d_operator.py` | `d1045fcf946a78fa4f989c48600116c49cab14c1` | EXACT |
| `src/medscale/mesc/_canonical_json_v1.py` | `b2d358170774a75344b488c2271f83d712ddf2ec` | EXACT |

```text
before build:      7 / 7 EXACT
at candidate HEAD: 7 / 7 EXACT
```

The four governing P-A1 documents were also verified 4 / 4 exact before and
after; P-A2 modifies none of them.

## 5. Production import boundary

```text
medscale.mesc._formal_generation_v1:  NOT IMPORTED
medscale.mesc._formal_split_v1:       NOT IMPORTED

permitted reuse actually taken:
from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
```

That is the only `medscale` import in the production script, and the only two
symbols taken from it. The audit is programmatic, over the final production AST
(`test_production_never_imports_the_formal_modules`,
`test_production_medscale_imports_are_only_the_canonical_serializer`,
`test_production_imports_only_canonical_serializer_symbols`).

Production carries the five input-surface literals, the seven candidate
filenames, the ten allowlisted exception tokens and the canonical exception
module literal `medscale.mesc._formal_split_v1` as exact string constants (§27).
The module literal is a classification constant; it is never imported.

## 6. Test import boundary

```text
the only formal execution-module import at test scope:
from medscale.mesc._formal_generation_v1 import resolve_repository_commit

medscale.mesc._formal_split_v1:            NOT IMPORTED
frozen formal test helpers:                NOT IMPORTED
make_environment / SYNTHETIC_COMMIT:       NOT IMPORTED
```

The oracle is used solely for differential conformance of the independent
resolver over synthetic repositories. Every contract literal the test asserts is
an expected value transcribed from the P-A1 documents, never one discovered by
importing a formal module (`test_test_scope_formal_import_is_exactly_the_oracle`,
`test_no_frozen_formal_test_helper_is_imported`).

## 7. Six-command implementation status

| Command | Status | Child | Mutation |
|---------|--------|-------|----------|
| `open` | IMPLEMENTED | none | creates `episode-core.json` once |
| `generate` | IMPLEMENTED | exactly one operator `generate` | appends one stage record |
| `compare` | IMPLEMENTED | exactly one operator `compare` | appends one stage record |
| `verify` | IMPLEMENTED | exactly one operator `compare` | appends one stage record |
| `invalidate` | IMPLEMENTED | none | appends the pre-seal invalidation record |
| `finalize` | IMPLEMENTED | none | creates `episode-manifest.json` once |

```text
command count:   6
seventh command: NONE
record-freeze:   DOES NOT EXIST
```

`run`, `execute`, `repair`, `resume`, `recover`, `status`, `inspect`, `replay`,
`seal`, `retry` and `record-freeze` are all absent and are each asserted absent.

No production flag weakens the boundary: there is no `--fake-operator`,
`--test-mode`, `--skip-identity`, `--unsafe`, `--no-verify` or `--mock`.
Qualification substitutes the evidence store and the child runner through
internal class boundaries (`EvidenceStore`, `ChildRunner`) that the CLI always
constructs unchanged.

## 8. Seven-record inventory status

```text
evidence record classes implemented: 7
eighth record class:                 NONE
```

`episode-core.json`, `stage-generate-a.jsonl`, `stage-generate-b.jsonl`,
`stage-compare.jsonl`, `stage-verify.jsonl`, `episode-invalidation.jsonl` and
`episode-manifest.json`. A completed successful episode was enumerated after
seal and contained exactly the six records a successful episode requires and no
other file. Fourteen named prohibited filenames were each asserted absent.

## 9. Schema and lifecycle implementation status

Exact and closed field sets are enforced for `episode-core.json`,
`episode-invalidation.jsonl` and `episode-manifest.json`, and asserted by tests
that compare the full sorted key tuple.

```text
schema versions implemented exactly:
mesc-p01-04d-execution-evidence/episode-core/v1
mesc-p01-04d-execution-evidence/stage-event/v1
mesc-p01-04d-execution-evidence/invalidation-event/v1
mesc-p01-04d-execution-evidence/episode-manifest/v1

event_ordinal:  one-based, per physical file, +1 per successful append only
timestamps:     UTC RFC3339 YYYY-MM-DDTHH:MM:SS.ffffffZ, as strings
absence:        fields the contract defines as absent are omitted, never null
```

`generation_identity` is absent on comparison stages rather than null.
`canonical_main_movement` is present exactly when the movement is real and
material. `event_count` is omitted for `MALFORMED_PRESERVED` records.

The observed generate lifecycle is exactly:

```text
stage_opened
repository_identity_observed
inputs_hashed
repository_identity_observed        (immediately pre-child)
child_started
child_exited
outputs_hashed
split_fingerprint_observed
stage_sealed
```

`compare` records two repository observations and `verify` exactly one, matching
the §5 observation matrix.

## 10. Failure mapping coverage

```text
failure_class values implemented:            21 / 21
CHILD_NONZERO_EXIT operator branches:        11 / 11
root_cause_class values:                     15
remediation_disposition values:               4
```

`failure_class` is observed and the other two members of the triad are derived
by `derive_failure_triad`. No call site chooses a root cause or remediation
independently. `LATER_STAGE_GOVERNANCE_REQUIRED` is present in the enumeration
and is never derivable from a P-A2 `stage_failed`.

The `CHILD_NONZERO_EXIT` + `NO_ERROR` contract contradiction is implemented as an
actual eleventh branch deriving `UNDETERMINED` /
`FOUNDER_DISPOSITION_REQUIRED`, and the harness fails closed.

Both tables are table-driven in tests against values transcribed from §19.1 and
§19.2, and a totality test proves every one of the values is reachable.

### 10.1 Ledger delta — `EPISODE_PATH_IDENTITY_DRIFT`

The `PA2G-R1` remediation adds exactly one `failure_class`, under explicit
founder authorization (`D4`), because a real-directory-for-real-directory swap
passes both reparse and containment and no existing class describes it.

| Ledger | Before | After |
|---|---|---|
| `failure_class` values | 20 | **21** |
| `FAILURE_TRIAD` rows | 19 | **20** (+ `CHILD_NONZERO_EXIT` special case = 21 / 21) |
| named closed enumerations | 10 | 10 — unchanged |
| named closed-enumeration values | 77 | **78** |
| `root_cause_class` | 15 | 15 — unchanged |
| `remediation_disposition` | 4 | 4 — unchanged |
| `terminal_disposition` | 5 | 5 — unchanged |
| `COMMANDS` | 6 | 6 — unchanged |
| `EVIDENCE_FILENAMES` | 7 | 7 — unchanged |

```text
EPISODE_PATH_IDENTITY_DRIFT
    root_cause_class:         PATH_SAFETY_FAILURE
    remediation_disposition:  FOUNDER_DISPOSITION_REQUIRED
```

`FOUNDER_DISPOSITION_REQUIRED` rather than `NEW_EPISODE_REQUIRED`, because a
detected in-flight swap evidences a host-level adversary; retrying in a fresh
episode on the same host would not address it.

The class never reaches `seal_after_failure`: a path-safety refusal is fatal and
writes nothing, so the value is carried by the terminal refusal rather than by a
`stage_failed` record. It is therefore absent from `REFUSAL_FAILURE_CLASSES` and
from the `STAGE_FAILED` parametrization, which `R1-T4` asserts.

The totality tests were retargeted in the same commit —
`test_failure_class_enumeration_is_exactly_twenty_one` and
`test_failure_mapping_is_total_over_twenty_one` — so totality is enforced at the
new count, not silently broken.

```text
DIVERGENCE FROM THE IMMUTABLE P-A1 LEDGER
evidence-contract.md §20 fixes the named ledger at 10 enumerations / 77 values.
The implementation now carries 10 / 78. The governing document is immutable at
this gate and was not edited, so reconciling the two requires a founder P-A1
amendment. This is recorded as an open item, not as a silent divergence.
```

## 11. Evidence-write A / B / C coverage

```text
CASE A  zero-byte failed append, journal still WELL_FORMED, later append safe
        -> EVIDENCE_WRITE_FAILURE / EVIDENCE_INTEGRITY_FAILURE /
           NO_REMEDIATION_AUTHORIZED, stage_failed -> stage_sealed, STAGE_FAILED

CASE B  partial or malformed bytes remain
        -> exact bytes preserved, MALFORMED_PRESERVED, event_count omitted,
           NO stage_failed and NO stage_sealed fabricated, no stage_disposition

CASE C  bytes well formed, required append no longer safely recordable
        -> nothing fabricated, stage STRUCTURALLY UNSEALED,
           continuation prohibited immediately
```

All three are exercised by injecting controlled append failures through the
evidence store. Case B additionally proves the preserved bytes never change
again after the failure.

One defect was found and fixed during qualification: the first implementation
sealed the stage after malformed bytes, violating §18.3. `run_stage` now returns
on `EvidenceMalformedPreservedError` before any further append is attempted, and
`test_case_b_partial_bytes_are_preserved_exactly` is the regression guard.

## 12. Structural-unseal coverage

Structural unseal is a computed condition (`JournalScan.structurally_unsealed`),
never a persisted field, enumeration or file. A stage is structurally unsealed
exactly when `stage_opened` exists and the journal does not end in exactly one
valid `stage_sealed` event.

```text
persisted representation of structural unseal: NONE
journal repair:                                NOT IMPLEMENTED
journal backfill after recovery:               PROHIBITED AND TESTED
```

After structural unseal, `generate`, `compare` and `verify` all refuse. A
subsequent `finalize` binds the exact existing bytes read-only, records
`record_integrity` `WELL_FORMED` with the actual `event_count`, and selects
`EPISODE_EVIDENCE_CORRUPT`. Syntactic integrity and lifecycle completeness are
kept separate: the record is not falsely demoted to `MALFORMED_PRESERVED`.

## 13. TM-0 / TM-1 / TM-2 coverage

`classify_terminal_manifest` returns exactly one of three structural states and
persists nothing.

```text
TM-0  path physically absent
      -> no seal, no terminal identity, no durable terminal disposition;
         a containment-only retry is permitted while the path stays absent

TM-1  path exists, bytes are not one complete canonical schema-valid manifest
      -> exact bytes preserved; retry, repair, truncation, deletion, overwrite,
         replacement, rename, append-to-complete and a second manifest are all
         refused; no terminal identity and no durable terminal disposition

TM-2  path exists and the bytes are a complete canonical schema-valid manifest
      -> canonical seal established, terminal identity established,
         post-seal immutability absolute
```

Nine TM-1 shapes are each asserted TM-1 and immutable: zero-byte, partial JSON,
malformed JSON, wrong `schema_version`, missing mandatory field, invalid
`terminal_disposition`, prohibited extra field, noncanonical serialization and
incomplete `records[]` binding. A physically existing zero-byte manifest is
asserted TM-1 and never TM-0.

`EPISODE_EVIDENCE_CORRUPT` is never claimed durable under TM-1: the TM-1 branch
raises before any manifest is written and reports that no terminal disposition or
terminal identity exists.

Terminal identity is `SHA-256` plus byte size of the exact complete manifest
bytes, exists if and only if TM-2, is not stored inside the manifest, and is
recomputable read-only after a crash without any mutation.

## 14. Terminal precedence coverage

```text
1. evidence corruption      -> EPISODE_EVIDENCE_CORRUPT
2. explicit invalidation    -> EPISODE_INVALIDATED
3. post-open refusal        -> EPISODE_REFUSED
4. failure                  -> EPISODE_FAILED
5. complete equal success   -> EPISODE_COMPLETE_EQUAL
```

All five are reachable in synthetic tests, and precedence is proved directly:
corruption outranks invalidation, and invalidation outranks refusal and failure.
An incomplete but clean episode seals `EPISODE_FAILED` rather than
`EPISODE_COMPLETE_EQUAL`. No sixth value exists.

## 15. Path safety coverage

The external evidence root must be absolute, resolved, existing, writable and
disjoint from the repository root, from each generation workspace and from the
future evidence root. Containment is evaluated on resolved path components.

```text
sibling prefix collision (repo vs repository-other): NOT treated as inside
relative path:                                       REFUSED
absent evidence root:                                REFUSED
evidence root inside the repository:                 REFUSED
workspace inside the evidence root:                  REFUSED
future evidence root inside the evidence root:       REFUSED
reparse-point redirect on any path component:        REFUSED
```

The harness refuses reparse shapes even where `resolve_repository_commit`
resolves them; that stricter refusal is the only authorized divergence, and it is
asserted directly against the oracle. The harness never pre-creates a generation
workspace, which is asserted after a child-launch failure.

### 15.1 Greptile G1 / G2 / G3 hardening

**G1 — symbolic references are metadata-relative or refused.** A symbolic `HEAD`
reference is validated by `require_safe_metadata_reference` before any candidate
path is built or read. Absolute, drive-rooted, UNC-rooted and parent-traversing
references are refused with `PathSeparationRefusalError`, and the resulting
candidate is additionally required to be contained by the metadata base it was
joined to. `PureWindowsPath` performs the validation on every host because it is
the stricter parser: it recognizes both separators and both root forms, where a
POSIX parser would accept `C:/attacker/ref` as an ordinary relative name. A file
outside the metadata base is never read, even when it holds a syntactically valid
forty-character commit.

**G2 — reparse components are inspected before anything is followed.**
`resolve_metadata_path` walks a gitdir or commondir path one real component at a
time and refuses the moment a symlink, junction or other reparse point appears,
before descending through it. `Path.resolve` is no longer called first, because
resolving erases exactly the components that must be inspected. Lexical `.` and
`..` are honoured rather than rejected, so a legitimate worktree `commondir` of
`../..` still resolves — that case is asserted directly. The `.git` metadata
entry, the `commondir` file and `packed-refs` are each inspected before being
read.

**G3 — the episode directory is validated at every operation.**
`require_safe_episode_directory` refuses a redirected or escaped episode
directory, and is applied on entry to every episode command, before every journal
scan, before the terminal-manifest state is classified, and before each durable
write. `require_safe_evidence_path` additionally refuses a redirected durable
evidence file before it is read or appended. A redirected episode directory
therefore refuses `generate`, `compare`, `verify`, `invalidate` and `finalize`
without hashing an input, launching a child, appending an invalidation record or
creating a manifest, and the redirect target is left byte-identical.

```text
race guarantee claimed:  NONE BEYOND RE-VALIDATION AT EACH OPERATION
```

The checks are re-applied per operation rather than cached, which narrows the
window between validation and use. It does not eliminate it: a redirect
introduced between a check and the immediately following open is not prevented,
and no stronger guarantee is claimed here.

### 15.2 PA2G-R1 — in-flight episode-path TOCTOU closure

Independent review of the G1/G2/G3 correction found that the G3 gates fired only
at command entry, leaving the whole in-flight span of a running stage unguarded.

**Condition.** A co-resident unprivileged attacker observes the episode path
after `open`, then swaps the episode directory for a junction while a stage child
is in flight.

**Reproduced against the pre-fix candidate `5ddf1778`:**

```text
generate outcome:            rc=0
episode path:                junction=True
records written OUTSIDE the evidence root:  9 / 9
    stage_opened, repository_identity_observed, inputs_hashed,
    repository_identity_observed, child_started, child_exited,
    outputs_hashed, split_fingerprint_observed, stage_sealed
stage_sealed outside the root:  YES — a clean-looking sealed stage
```

`inputs_hashed` escaped as well, so finalize-only hardening would not have been a
fix. The next command was refused at entry, which is precisely why the escape was
silent: the gates fired only after the damage.

**Causal mechanism of the fix.** Two independent layers.

*Prevention.* `EpisodeContext.pinned` holds an open handle on `episode-core.json`
for the whole write-bearing span of `generate`, `compare`, `verify`, `invalidate`
and `finalize`. On Windows an open handle inside a directory makes that directory
unrenamable and undeletable, so the swap fails outright with a sharing violation
rather than being merely detected. Where a platform does not offer that
guarantee the span is unaffected and the gate below is the protection.

*Detection.* `measure_episode_path_identity` reduces
`(st_dev, st_ino)` — the volume serial and file index on Windows — through the
frozen canonical serializer to a digest. It names the directory *object*, not the
path that currently leads to it. The identity is pinned when the episode context
opens, and `require_safe_episode_directory` runs one ordered gate before every
durable write:

```text
1. no reparse redirect on any component of the episode path
2. containment inside the validated external evidence root
3. equality with the pinned episode_path_identity
```

`StageJournal` runs that gate before **each of the nine stage events**, and again
immediately after `stage_sealed` is written. A path-safety refusal is fatal: it
propagates out of `run_stage` without writing `stage_failed` or `stage_sealed`,
because the destination is no longer provably the authorized directory.

**Observed against the fixed candidate:**

```text
with the OS pin active:      swap BLOCKED (PermissionError / sharing violation);
                             stage completes normally inside the evidence root
with the OS pin disabled:    swap succeeds; generate REFUSES
                             (ReparsePointRefusalError); NO stage_sealed anywhere
```

Only the digest is used anywhere; no host device or inode number is persisted,
reported or exposed, which `R1-T6` asserts directly.

#### 15.2.1 Residual window, disclosed

```text
prevention layer:  removes the swap entirely on hosts that pin an open directory
detection layer:   refuses at the next gated write on every host
residual window:   the sub-syscall interval between the gate and the write it
                   guards, on hosts without the prevention guarantee
```

A swap landing inside that interval could still place one record outside the
root. It cannot yield a *clean sealed stage*: the seal is gated immediately
before and re-verified immediately after, so a swap in either position refuses
with `rc=1` and no `stage_sealed`. Eliminating the interval itself would require
handle-relative writes (`dir_fd`), which CPython does not offer on this platform.
That residual is disclosed rather than claimed closed.

#### 15.2.2 Manifest binding — not implemented, and why

Directive `D3` also asked for `episode_path_identity` to be bound into the sealed
manifest. **That is not implemented here**, because
`evidence-contract.md` §15.4 fixes the `episode-manifest.json` field set as
*exact and closed*, and that document is immutable at this gate. Adding the field
would violate a governing contract in order to satisfy a remediation directive.

The directive makes the binding conditional — it is required only where a
residual window leaves an escape that would otherwise be invisible. The
prevention plus fatal-gate design reaches outcome **(A)**: there is no path from
a swap to a clean sealed stage. Binding therefore remains available as a
follow-up if the founder amends §15.4, and is recorded here as an open item
rather than silently skipped.

## 16. Sensitive-data minimization coverage

```text
raw stdout:              NEVER PERSISTED
raw stderr:              NEVER PERSISTED
raw exception class:     NEVER PERSISTED
raw exception message:   NEVER PERSISTED
input bytes:             NEVER PERSISTED
input locations:         NEVER PERSISTED in input evidence
labels / membership:     NEVER READ, NEVER PERSISTED
environment variables:   NEVER READ, NEVER PERSISTED
dedicated username:      NO FIELD
dedicated hostname:      NO FIELD
```

For child streams only the SHA-256, byte size and exactly one
`operator_error_class` value persist. A test plants marker bytes in synthetic
stdout and stderr and proves neither reaches durable evidence while the recorded
digests still match. A second test plants a protected-looking identifier inside a
typed exception message and proves that neither the message nor the exception
class token appears in the journal, while the mapped closed value does.

Required absolute path values — `repository_root`, `external_evidence_root`,
`resolved_python_executable_path` and the complete child `argv` — are recorded in
full and are not redacted for incidental username-like components, exactly as
`R5` requires.

## 17. Synthetic-only qualification statement

```text
protected inputs:            NONE
real dataset bytes:          NONE
real source records:         NONE
real generation workspaces:  NONE
real external evidence:      NONE
canonical operator executed: NO
network access:              NONE
model execution:             NONE
```

Every repository, workspace, input, evidence root, stdout/stderr stream, process
outcome and filesystem failure used in qualification is constructed inside
`tmp_path`. The frozen operator is copied read-only into synthetic repositories
for identity binding and is never executed, never imported and never invoked
through any interface.

Qualification loads the harness from the synthetic repository copy, so the
harness's own `__file__` identity rule holds under test without weakening it.

## 18. Exact test commands run

```text
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest tests/test_mesc_p01_04d_evidence_harness.py -q
uv run pytest tests/test_mesc_p01_04d_operator.py tests/test_mesc_formal_generation_v1.py tests/test_mesc_formal_split_v1.py -q
uv run pytest --cov --cov-report=term-missing -q
uv run medscale check
```

The correction regression gate additionally selected each finding's cases:

```text
uv run pytest tests/test_mesc_p01_04d_evidence_harness.py -q -k "<PA2-R1 selection>"
uv run pytest tests/test_mesc_p01_04d_evidence_harness.py -q -k "<PA2-R2 selection>"
uv run pytest tests/test_mesc_p01_04d_evidence_harness.py -q -k "<PA2-R3 selection>"
```

The environment was prepared with `uv sync --frozen`, matching `.github/workflows/ci.yml`.

## 19. Exact test results

```text
focused P-A2 gate
tests/test_mesc_p01_04d_evidence_harness.py
passed:    347
failed:    0
skipped:   3
duration:  20.10s

frozen regression gate
tests/test_mesc_p01_04d_operator.py
tests/test_mesc_formal_generation_v1.py
tests/test_mesc_formal_split_v1.py
passed:    157
failed:    0
skipped:   1
duration:  26.98s
frozen test files modified: 0
```

The focused count rose 282 → 310 for the review corrections, 310 → 337 for the
Greptile G1/G2/G3 corrections, and 337 → 347 for the `PA2G-R1` TOCTOU
remediation, which added ten further cases. The frozen gate is unchanged
throughout at 157 passed / 1 skipped.

The third focused skip is new and is a genuine host limitation: this Windows host
permits unprivileged **junction** creation but not unprivileged file symlinks, so
the file-level reparse case skips while every directory-level reparse case runs
for real.

The other two focused skips and the one frozen skip are the same pre-existing
environment condition: this Windows host does not permit unprivileged symlink
creation. Three other repository test files skip for the identical reason. The
reparse-refusal contract is additionally covered by three
privilege-independent tests that exercise the component walk, the resolver
refusal and the `open` refusal without creating a symlink.

**`PA2C-F2` is an environmental-conditions caveat, not a candidate claim.** The
failures previously reported in `tests/test_mesc_b2a_portability.py` are
host-dependent bash-portability failures, and that file is not touched by any
P-A2 candidate.

Observed in this correction worktree, in the full-suite run recorded in §21:

```text
tests/test_mesc_b2a_portability.py:  0 failed, 1 skipped
```

The previously reported figure of 54 failures did **not** reproduce here. This
session performed no fetch and no `origin/main` clone, so the comparison against
`origin/main` asserted in the remediation brief is carried forward as the
brief's finding and is *not* independently re-verified here. Either way the file
is untouched by this candidate and the condition is out of scope for this
ticket.

### 19.1 Explicit correction regression gate

Each correction was additionally proved by a selected subset, reported
independently:

```text
PA2-R1  durable-invalidation continuation barrier      13 passed, 0 failed
PA2-R2  never-durably-opened stage-journal barrier      5 passed, 0 failed
PA2-R3  controlled pre-mutation argument refusal       29 passed, 0 failed

GREPTILE-G1  symbolic-ref metadata escape               16 passed, 0 failed
GREPTILE-G2  reparse component erased by resolve()       7 passed, 0 failed
GREPTILE-G3  episode-directory redirect                  4 passed, 1 skipped

PA2G-R1      in-flight episode-path TOCTOU               9 passed, 0 failed
```

The ten new cases added for `PA2G-R1` (nine test functions plus one new
parametrized `failure_class` case) are:

```text
R1-T1  test_r1_t1_midflight_swap_refuses_without_sealing
R1-T1  test_r1_t1_midflight_swap_is_prevented_while_pinned
R1-T2  test_r1_t2_swap_after_inputs_hashed_refuses_at_the_next_gate
R1-T3  test_r1_t3_parent_component_swap_is_refused
R1-T4  test_r1_t4_non_reparse_identity_swap_is_refused
R1-T4  test_r1_t4_drift_class_maps_to_the_path_safety_triad
R1-T5  test_r1_t5_negative_control_ordinary_run_seals_normally
R1-T6  test_r1_t6_identity_is_recomputable_and_detects_a_swap
       test_r1_every_stage_event_is_gated
       test_failure_triad_mapping[EPISODE_PATH_IDENTITY_DRIFT]
```

**Discriminator against the pre-fix base `5ddf1778`**, with the corrected test
file and the base production harness: **7 failed, 1 passed, 1 skipped.** The one
pass is `R1-T5`, the negative control, which must pass on both builds; the one
skip is the prevention test, which correctly skips at base because the pin does
not exist there. All nine pass at HEAD.

The G1/G2/G3 subsets were additionally run as **negative controls** against the
unchanged published parent `2f1fb05f`, with the corrected test file and the
parent's production harness. Twenty of them fail there and pass here, so they
detect the defects rather than merely describing them; the positive controls —
ordinary loose refs, packed-refs, a normal `.git` directory, a legitimate
worktree `../..` commondir, and a normal episode reaching
`EPISODE_COMPLETE_EQUAL` — pass against both builds, so the hardening is
narrowly targeted.

For `PA2-R1` and `PA2-R2` the refusal is proved by instrumentation, not only by
the terminal disposition. A spy wraps the real `hash_input_surfaces` function and
a counting child runner replaces `ChildRunner`, and both are asserted at zero
before the refusal:

```text
protected-input hashing calls before refusal:  0
child launches before refusal:                 0
generation workspace created:                  NO
stage journal for the refused continuation:    NOT CREATED
```

The counting runner raises rather than returning, so a launch could not pass
silently even if its counter were not asserted.

`PA2-R2` additionally asserts the residue journal exists, is exactly zero bytes,
contains no `stage_opened`, `stage_failed` or `stage_sealed`, is unchanged after
every refused continuation, and is still byte-identical after `finalize`.

`PA2-R3` covers the missing value, an out-of-enumeration value, the absence of
any `Traceback` or `ValueError` text on the CLI error surface, the absence of any
invalidation record for a refused invocation, and all eleven
`operator_error_class` branches through the `invalidate` surface with their
mappings unchanged.

## 20. Static, type and lint results

```text
uv run ruff check .          All checks passed!
uv run ruff format --check . 189 files already formatted
uv run mypy                  Success: no issues found in 189 source files
uv run medscale check        status: CLEAN
```

No configured quality gate was skipped, disabled or narrowed, and no
configuration file was edited to accommodate the new paths.

Suppressions are enumerated exactly, because their count is part of the audit:

```text
production script
  # noqa: E402   1 occurrence, on the canonical-serializer import that must
                 follow the sys.path bootstrap — the same pattern and the same
                 justification the frozen operator already uses
  type: ignore   0 occurrences
  mypy override  0 occurrences

qualification test
  # noqa         0 occurrences
  type: ignore   4 occurrences, all `[misc,name-defined]`, each on a subclass of
                 a class reached through a dynamically loaded module object,
                 which mypy cannot type; they suppress no contract check
  mypy override  0 occurrences
```

No suppression was added to make a correction defect disappear. The fourth
`type: ignore` is on the counting child runner introduced by the `PA2-R1` /
`PA2-R2` regression tests, and is the same dynamically-loaded-module pattern as
the existing three.

The Greptile security correction added **no** suppression of any kind. It removed
one: a `# noqa: S603` written on the junction fixture was unnecessary, because
that rule is not enabled in this repository, and `ruff` flagged it as an unused
directive. It was dropped **before** the commit, so no such directive ever
entered the tree; the counts above are the committed state.

The `PA2G-R1` correction likewise added no suppression. `ruff` asked for
`Path.stat` in place of `os.stat` on the new identity primitive; that was
satisfied by using `Path.stat(follow_symlinks=False)`, which is equivalent, not
by silencing the rule.

## 21. Full-suite result

```text
uv run pytest --cov --cov-report=term-missing -q

passed:    2438
failed:    0
skipped:   8
warnings:  1
duration:  160.87s

repository coverage:  85.55%
configured gate:      77.0%  (reached)
```

The full suite is self-contained. It resolves no P01-03G path, reads no
`source-records.jsonl`, runs no real P01-04D episode, performs no model
execution and uses no protected Generation A or Generation B workspace. No test
was excluded.

### 21.1 Coverage scope — what 85.55% does and does not measure

`85.55%` is the **repository-wide** result of the repository's configured
coverage gate. It is not a harness-specific figure, and it must not be read as
one.

```text
pyproject.toml [tool.coverage.run]
source = ["src/medscale"]

measured by that configuration:
src/medscale/**

NOT measured by that configuration:
scripts/**, which includes
scripts/mesc_p01_04d_evidence_harness.py — the entire P-A2 production artifact
```

```text
85.55% is the configured src/medscale repository coverage result.
85.55% is NOT the P-A2 harness coverage percentage.
```

No harness-specific coverage percentage is claimed here, because no correctly
scoped harness-specific measurement is reported in this document. Reporting one
would require an explicitly scoped run, which this correction gate does not
require. The evidence that the harness is exercised is the focused suite itself:
310 synthetic cases driving the real parser, the real `dispatch` and the real
evidence-write path.

## 22. Known limitations and observations

1. **Symlink tests skip on this host.** Two P-A2 tests and one frozen test skip
   because unprivileged symlink creation is unavailable on this Windows host.
   They run wherever symlinks are permitted, including the Linux CI runner. The
   privilege-independent reparse tests keep the refusal covered locally.

2. **Writability is gated by `os.access` plus fail-closed real writes.** The
   declared evidence-root writability gate uses `os.access(..., os.W_OK)`, which
   is advisory on Windows. Actual durability is proved by the real exclusive
   creation and append operations, which fail closed. No probe file is written
   into the evidence root.

3. **Child streams are buffered in memory.** `subprocess.communicate` holds
   stdout and stderr in memory to compute their digests. Nothing is persisted,
   but the in-memory size is not bounded by the harness.

4. **`generation-manifest.json` is read whole.** The authoritative fingerprint is
   read by parsing that one scientific artifact read-only after the child exits.
   Candidate digests are computed in bounded chunks.

5. **Two deterministic derivations are stated here explicitly**, because the
   contract fixes the surrounding vocabulary without naming the branch:
   - a compare or verify stage whose harness ledger is `EQUAL` while the child
     exited nonzero records `comparison_disposition` `INTEGRITY_FAILURE` and
     `failure_class` `CHILD_NONZERO_EXIT`, keeping child provenance distinct from
     harness provenance;
   - `verify` classifies a rerun that contradicts the sealed comparison as
     `VERIFY_FAILURE`, which is the only state in which that value is reachable,
     because `verify` runs only after `compare` sealed `EQUAL_VERIFIED`.

6. **`new_episode_required` is always `true`** in an invalidation record, and the
   harness now **enforces** that value rather than only asserting it. After a
   valid durable invalidation, `generate`, `compare` and `verify` all refuse in
   that episode (`PA2-R1`, §1.2), so a fresh scientific attempt does in fact
   require a new episode.

   In the historical candidate `94b22c9b` this claim was **false**: the constant
   was written but no barrier enforced it, and a full generation stage — including
   protected-input hashing and a child launch — could still run in an invalidated
   episode. That was the blocking review finding, and it is closed here.

7. **Workspace-related path separation is checked where the workspace is known.**
   `open` has no workspace argument in the contract, so the workspace and
   future-evidence disjointness conditions are enforced at `generate`, `compare`
   and `verify` — exactly the PRE-STAGE step 3 position of §21.1.

8. **One contract defect was found and fixed during the original build**,
   recorded in §11 above: events were being appended after malformed bytes. It is
   fixed and guarded by a regression test.

9. **Three further defects were found by independent review and corrected in this
   rebuild**: `PA2-R1` (blocking), `PA2-R2` and `PA2-R3`. Their exact implemented
   behaviour is recorded in §1.2 and their regression evidence in §19.1.

10. **A fourth review finding, `PA2-R6`, was documentation-only** and is corrected
    in §21.1: the previously reported `85.55%` is repository coverage of
    `src/medscale` and never measured the harness.

11. **Six further review observations were not authorized for correction at this
    gate** — `PA2-R4` (unraised `StructurallyUnsealedError`), `PA2-R5`
    (`CONTAINMENT` unreachable in durable evidence), `PA2-R7` (the founder P-A2
    authorization is not recorded in the repository), `PA2-R8` (`_byte_size`
    returning zero when `stat` fails), `PA2-R9` (blank lines skipped by the
    journal scan) and `PA2-R10` (TM-2 revalidation re-hashing bound records).
    None was changed. They remain open observations for the founder.

12. **Three P1 security defects were found by Greptile supplemental review of the
    published `2f1fb05f` candidate and corrected here** — `GREPTILE-G1`,
    `GREPTILE-G2` and `GREPTILE-G3`, all independently confirmed blocking and all
    reproduced as concrete compromises against the unchanged parent. Their exact
    implemented behaviour is in §15.1, their origin in §1.3 and their regression
    evidence in §19.1.

13. **The G3 guard narrows a race; it does not remove one.** The episode-directory
    and evidence-path checks are re-applied at every operation rather than cached,
    but a redirect introduced between a check and the immediately following open
    is not prevented. No stronger guarantee is claimed.

## 23. Authority consequence

```text
P-A1:
CANONICALLY ADOPTED

P-A1 implementation clarification:
CANONICALLY ADOPTED

historical P-A2 candidate 94b22c9b:
REVIEWED — NOT APPROVED FOR PUBLICATION — PRESERVED AS LOCAL REVIEW EVIDENCE

published P-A2 candidate 2f1fb05f (Draft PR #97):
PUBLISHED — GREPTILE P1 SECURITY FINDINGS CONFIRMED BLOCKING —
NOT READY FOR READY-TRANSITION OR ADOPTION

corrected P-A2 security implementation:
LOCAL CANDIDATE BUILT — NOT PUBLISHED — NOT CANONICALLY ADOPTED

XD-EXEC-1:
DECIDED / OPEN — NOT CLOSED BY THIS BUILD

XD-EXEC-2:
OPEN

XD-EXEC-3:
OPEN

P01-04:
NOT COMPLETE

P01-05:
NOT UNLOCKED
```

Building this candidate satisfies none of the `PA1-FD-20` closure conditions that
require independent review and canonical adoption. XD-EXEC-1 remains open.

## 24. Execution authority

```text
P01-04D execution:
NOT AUTHORIZED
```

No part of this build authorizes P01-04D execution, P01-03G access,
source-record access, real dataset access, generation workspace creation,
Generation A, Generation B, compare or verify over real inputs, P01-04E through
P01-04G, model execution, training or fine-tuning.

## 25. Adoption status

```text
P-A2 security-correction candidate:
LOCAL ONLY — NOT PUSHED — NOT CANONICALLY ADOPTED

published Draft PR #97 at 2f1fb05f:
UNCHANGED — STILL OPEN, STILL DRAFT, STILL NOT MERGED

P01-04D execution:
NOT AUTHORIZED
```

The security-correction candidate is one local commit on a local correction
branch whose parent is the published head `2f1fb05f`. It has not been pushed, PR
#97 has not been updated, no review of it has been performed and no merge has
occurred. GitHub mutations performed by this security correction: zero.

The historical candidate `94b22c9b` remains preserved unchanged on its own local
branch as review evidence. It was not amended, reset, rebased, rewritten, deleted
or published. The published `2f1fb05f` commit is likewise not amended, rewritten
or force-pushed.

This document does not claim that P-A2 is adopted, that XD-EXEC-1 is closed, that
P01-04D execution is authorized, that source records were recovered or that any
real execution was validated. It does not claim that these security corrections
have been independently reviewed — only that they were built, qualified
synthetically, and validated against the unchanged published parent.

## 26. Next gate

```text
FRESH INDEPENDENT LOCAL SECURITY-CORRECTION REVIEW REQUIRED
```

Publication, review on GitHub, adoption and any execution authorization remain
separate founder decisions that have not been made.
