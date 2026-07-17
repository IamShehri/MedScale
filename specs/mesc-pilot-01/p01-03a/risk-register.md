# MESC Pilot-01 -- P01-03A Risk Register

Freeze date: 2026-07-17

| ID | Risk | Severity | Likelihood | Evidence | Preventive control | Detection control | Stop condition | Residual risk | Owner |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | Revision drift | HIGH | Medium | Remote repository can change revision contents or metadata | Require exact immutable revision match before acquisition | Verify remote revision against committed identity after acquisition start | Mismatch aborts acquisition and reports to governance | LOW | MedScale lead |
| R-02 | Configuration drift | HIGH | Low | Configuration enumeration could select wrong split | Require exact `pqa_labeled` configuration and reject any alternative | Verify downloaded artifact categorization against committed target | Non-`pqa_labeled` files abort acquisition | LOW | MedScale lead |
| R-03 | Wrong artifact selection | HIGH | Medium | Remote repository contains multiple configurations and files | Use explicit filename allowlist after metadata verification | Manifest review before and after acquisition | Unexpected filename aborts acquisition | LOW | Repository maintainer |
| R-04 | Unexpected loading script | HIGH | Medium | Hugging Face may embed loading logic | Prohibit `trust_remote_code`; require allowlisted artifact categories only | Review repository metadata before acquisition permission | Loading script required aborts authorization | LOW | Founder/governance |
| R-05 | Remote-code requirement | HIGH | Medium | Dataset may declare remote dependencies | Prohibit arbitrary loading scripts as a hard gate | Review repository loading metadata before acquisition | Remote code required blocks acquisition | LOW | Founder/governance |
| R-06 | Git contamination | HIGH | Medium | Proposed path overlaps with OneDrive-synchronized MedScale worktrees | Require external storage outside every worktree and repository root | Review resolved path before acquisition begins | Path resolves inside tracked tree aborts acquisition | LOW | MedScale lead |
| R-07 | Cloud-sync leakage | HIGH | Medium | OneDrive could synchronize raw abstracts outside Git | Require storage path outside OneDrive and known sync trees | Inspect resolved cloud-sync coverage before acquisition | Synchronized tree detected aborts acquisition | MEDIUM | MedScale lead |
| R-08 | Rights-metadata change | MEDIUM | Low | Repository license or redistribution terms may change | Record committed rights identity in manifest; abort on metadata change | Verify repository metadata before acquisition | Rights change aborts acquisition | LOW | Founder/governance |
| R-09 | Incomplete filename allowlist | HIGH | High | Exact remote filenames are not yet verified | Require metadata-only authorization before acquisition authorization is considered complete | Cross-check filenames against repository metadata | Unverified filename blocks acquisition completion | MEDIUM | MedScale lead |
| R-10 | Path privacy | MEDIUM | Medium | External path may expose raw data to other users or backends | Use owner-only filesystem permissions after later verification | Review path ACLs after directory creation if authorized | Permissions not restrictive enough blocks acquisition | MEDIUM | MedScale lead |
| R-11 | Partial download | MEDIUM | Medium | Network or tool interruption could produce incomplete artifacts | Compute size and SHA-256 per file; abort on mismatch | Verify all expected files exist with matching digests | Missing or mismatched file aborts acquisition | LOW | Repository maintainer |
| R-12 | Hash failure | HIGH | Low | Digest computation may fail or mismatch | Abort on any hash failure; do not acquire inconsistent artifacts | Record expected versus actual digests in manifest | Hash mismatch aborts acquisition | LOW | Repository maintainer |
| R-13 | Duplicate or stale files | MEDIUM | Low | Re-run could leave stale artifacts in external storage | Use revision-specific directory only; do not merge into existing trees | Compare revision directory against expected empty state | Unexpected files abort acquisition | LOW | Repository maintainer |
| R-14 | Accidental transition into schema inspection | HIGH | Medium | Post-acquisition workflow could attempt to open Parquet files | Explicit stop condition after manifest generation; separate governance for schema inspection | Review changed-path boundary before any later stage | Acquisition workflow proceeds beyond manifest aborts | LOW | Founder/governance |
| R-15 | Mistaken interpretation of acquisition as broader execution authority | HIGH | Medium | Governance state documents could be misread as permitting inference, training, or publication | Repeat explicit execution prohibition in all readiness and governance documents | Review P01-03A and future PRs for accidental authorization language | Any unauthorized execution language blocks merge | LOW | Founder/governance |

## Guardrail requirement

Current `.gitignore` does not contain explicit raw-dataset guardrails.

Pending a separate guardrail implementation PR, acquisition authorization should remain blocked. Preferred fail-closed position:

```text
ACQUISITION BLOCKED UNTIL STORAGE AND REPOSITORY GUARDRAILS ARE VERIFIED
```
