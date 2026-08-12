# P01-04B2A Evidence Acceptance — Evidence Ledger

```text
Status:
IMMUTABLE EVIDENCE RECORD

Evidence run:
30678040133

Canonical SHA:
e3478da94e62ad9af5858a69e28de7e5d5fc04f4

Mechanical verification:
PASSED
```

This ledger records what was produced and verified. It embeds no artifact bytes.

---

## 1. Run identity

```text
Workflow:        MESC B2A Portability
Workflow ID:     323476626
Workflow path:   .github/workflows/mesc-b2a-portability.yml
Run ID:          30678040133
Run number:      8
Event:           workflow_dispatch
Run attempt:     1
Head branch:     main
Head SHA:        e3478da94e62ad9af5858a69e28de7e5d5fc04f4
Actor:           IamShehri
Created:         2026-08-01T01:30:04Z
Updated:         2026-08-01T01:30:55Z
Status:          completed
Conclusion:      success
```

Complete workflow history:

```text
Total runs:                8
pull_request runs:         7
workflow_dispatch runs:    1
Runs with run_attempt > 1: 0
```

The seven `pull_request` runs are infrastructure validation on
`feat/mesc-b2a-portability-infrastructure` and are **not** admissible evidence.
Run `30678040133` is the sole canonical-main evidence run.

## 2. Job topology

Six generation jobs plus one aggregate verification job. All seven completed
with conclusion `success`.

| Job | Steps | Status | Conclusion |
|---|---|---|---|
| `portability (linux-py3.11)` | 12 | completed | success |
| `portability (linux-py3.12)` | 12 | completed | success |
| `portability (macos-py3.11)` | 12 | completed | success |
| `portability (macos-py3.12)` | 12 | completed | success |
| `portability (windows-py3.11)` | 12 | completed | success |
| `portability (windows-py3.12)` | 12 | completed | success |
| `aggregate verification` | 15 | completed | success |

### Generation-job step conclusions

Identical across all six cells:

```text
1.  Set up job                          success
2.  Checkout exact head                 success
3.  Guard canonical-main dispatch       success
4.  Install uv                          success
5.  Verify uv runtime identity          success
6.  Sync (locked)                       success
7.  Generate canonical artifacts        success
8.  Verify exactly three files exist    success
9.  Upload cell artifact                success
17. Post Install uv                     success
18. Post Checkout exact head            success
19. Complete job                        success
```

Every generation job executed the canonical-main dispatch guard, checked out the
exact activated SHA, and uploaded its single cell artifact.

### Aggregate-job step conclusions

```text
1.  Set up job                                                    success
2.  Checkout exact head                                           success
3.  Guard canonical-main dispatch                                 success
4.  Install uv                                                    success
5.  Verify uv runtime identity                                    success
6.  Sync (locked)                                                 success
7.  Validate the current-run artifact set and download within caps success
8.  Verify archive cardinality                                    success
9.  Aggregate and compare all six cells (pull request)            skipped
10. Aggregate and compare all six cells (canonical-main dispatch) success
11. Publish non-admissible envelope to the job summary            success
12. Upload evidence envelope (canonical-main dispatch only)       success
23. Post Install uv                                               success
24. Post Checkout exact head                                      success
25. Complete job                                                  success
```

The pull-request aggregation path was **skipped** and the workflow-dispatch
aggregation path **executed**, as required. The evidence upload step executed
exactly once.

## 3. Artifact inventory

Exactly seven artifacts. Zero duplicates, zero missing, zero unexpected, zero
expired at inspection and at review.

| Artifact | ID | GitHub archive bytes | Expired |
|---|---:|---:|---|
| `b2a-portability-evidence` | 8811187770 | 509 | false |
| `b2a-portability-linux-py3.11` | 8811182197 | 855 | false |
| `b2a-portability-linux-py3.12` | 8811180460 | 855 | false |
| `b2a-portability-macos-py3.11` | 8811181809 | 855 | false |
| `b2a-portability-macos-py3.12` | 8811181195 | 855 | false |
| `b2a-portability-windows-py3.11` | 8811182814 | 855 | false |
| `b2a-portability-windows-py3.12` | 8811183686 | 855 | false |

### Archive SHA-256 digests

```text
b2a-portability-evidence
3ffc97d97b1e43eb0a3c45ca2436a79e681e47f4183b171231d5b1522ca12090

b2a-portability-linux-py3.11
c09d7e98e9d1aedf06eabd8702db9321f82c959cda0f8f456b232695525c8812

b2a-portability-linux-py3.12
c6c502d3ab204902c437ce528178f778fc03d24b101a7cbb77383ac4c0866d79

b2a-portability-macos-py3.11
d11e437a930f6ae17aff3149678f891751b79757c6682b86417e171d627eb1cb

b2a-portability-macos-py3.12
3f3fc93878bbedabad67226ae8d969c3d68511a72df4bc23c26014992bcb3bc4

b2a-portability-windows-py3.11
b2b45e1042fe9d87936a6974e74d6a7771899b466435306ef199a889f030770b

b2a-portability-windows-py3.12
91f394c14c7c08de666422725034ae2bffaa0e11ce0b54b7e071f96a856e7e4b
```

The six cell archives share an identical 855-byte size but distinct archive
digests. That is expected and non-blocking: ZIP container metadata differs by
producer platform while the contained payload bytes are identical. See NB-01.

### Run binding

All seven artifacts report:

```text
workflow_run.id:           30678040133
workflow_run.head_branch:  main
workflow_run.head_sha:     e3478da94e62ad9af5858a69e28de7e5d5fc04f4
expired at inspection:     false
expired at review:         false
```

Artifact expiry after the completed independent review does not retroactively
invalidate this ledger, the recorded review, or the founder decision.

## 4. Accepted payload identities

Each of the six cell artifacts contains exactly this canonical file set, and the
bytes are identical across every OS and Python cell:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical.json` | 228 | `7c5668f7b90c5c4cbe62bb0b073c97ed8e8084419d34cad41bc245d98f3873b8` |
| `canonical.jsonl` | 79 | `bb1dcc82390f4168ba2a644c0bf4d40313d735c9a59db97d90a383dfa3a7b266` |
| `manifest.json` | 308 | `da30b9ad0ba9d30547075ecb4ab7e7798b9e354d6d3f068e27c702eba6f5244d` |

### Cross-cell identity matrix

Every cell resolves to the same three digests above:

| Cell | `canonical.json` | `canonical.jsonl` | `manifest.json` |
|---|---|---|---|
| `linux-py3.11` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |
| `linux-py3.12` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |
| `macos-py3.11` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |
| `macos-py3.12` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |
| `windows-py3.11` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |
| `windows-py3.12` | `7c5668f7…3873b8` | `bb1dcc82…a7b266` | `da30b9ad…f5244d` |

```text
Cross-cell byte identity:
PASSED ACROSS ALL SIX CELLS
```

## 5. Schemas and envelope

```text
Manifest schema:
mesc-pilot-01-b2a-portability-manifest/1

Evidence schema:
mesc-pilot-01-b2a-portability-evidence/1

Evidence result:
pass

Evidence canonical_sha:
e3478da94e62ad9af5858a69e28de7e5d5fc04f4
```

The envelope identifies exactly the six ratified cells:

```text
linux-py3.11    linux-py3.12
macos-py3.11    macos-py3.12
windows-py3.11  windows-py3.12
```

and exactly the three canonical files, with the byte sizes and SHA-256 digests
recorded in section 4.

## 6. NB3 explicit checks

```text
NB3-A archive-to-manifest binding:
PASS — each cell archive contains exactly one manifest.json whose declared file
set, byte sizes and digests bind the extracted canonical files from that same
archive.

NB3-B envelope-to-cell binding:
PASS — the envelope's six cell records match the recomputed identities of the
six cell artifacts. No cell is omitted, duplicated, renamed or substituted.

NB3-C run-to-artifact binding:
PASS — every accepted artifact ID belongs to run 30678040133, and that run is
event workflow_dispatch, run_attempt 1, head_branch main, head_sha
e3478da94e62ad9af5858a69e28de7e5d5fc04f4.
```

## 7. Content boundary

```text
Content-boundary inspection:
PASS
```

The evidence payload contains no real dataset content, model weights, inference
outputs, patient data, training artifacts, runtime-derived timestamps,
hostnames, usernames, runner identifiers, secrets or tokens, environment paths,
or unratified metadata.

GitHub artifact API metadata outside the evidence payload — artifact IDs,
creation timestamps and expiry timestamps — is transport metadata, not embedded
evidence content, and is distinguished from prohibited runtime-derived fields.

## 8. Independent reviewer verdict

```text
APPROVE WITH NON-BLOCKING NOTES — CANONICAL PORTABILITY EVIDENCE
ELIGIBLE FOR A SEPARATE FOUNDER EVIDENCE-ACCEPTANCE DECISION

Blocking findings:
NONE

Non-blocking observations:
TWO — NB-01 and NB-02, both accepted; neither requires an evidence correction,
a new run, a rerun, a replacement artifact, or an implementation change
```

## 9. Immutable relationships

```text
canonical main SHA  e3478da94e62ad9af5858a69e28de7e5d5fc04f4
   └── is the head_sha of run  30678040133
          └── which owns exactly the seven artifacts listed in section 3
                 └── whose six cell payloads are byte-identical
                        └── and whose envelope binds canonical_sha back to
                            e3478da94e62ad9af5858a69e28de7e5d5fc04f4
```

Each link was verified mechanically. An artifact with correct bytes belonging to
a different run is inadmissible; an envelope naming a different canonical SHA is
inadmissible; a cell set that is not byte-identical is inadmissible. None of
those conditions occurred.

## 10. Standing status

This ledger records evidence. It accepts no B2A, discharges no `N-12`, closes no
platform obligation, and authorizes no B2B.
