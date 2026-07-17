# MESC Pilot-01 -- P01-03A Decision Record

Freeze date: 2026-07-17

## Storage-root strategy

Decision: external-only storage at `C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\`

Rationale: committed authority documents require that raw abstracts must not be committed to Git and must not be published or redistributed. External storage outside every worktree, repository, and synchronized tree is the only known control that satisfies this boundary.

Rejected alternative: repository-local raw-data directory under the MedScale repository or any worktree.

## `.gitignore` guardrail requirement

Decision: acquisition authorization must remain blocked until a separate guardrail implementation PR adds explicit deny-list protection.

Rationale: committed `.gitignore` covers tooling, build outputs, environments, caches, and editor noise, but does not contain an explicit raw-dataset boundary. A defense-in-depth ignore rule is a prerequisite to a fail-closed acquisition posture.

Rejected alternative: acquire artifacts before implementing guardrails.

## Manifest ownership

Decision: dual-manifest design.

Rationale:
* reproducibility: repository-safe manifest preserves portable scientific identity and content digests.
* path privacy: local full manifest contains machine-specific operational provenance and remains outside Git.
* reviewability: repository-safe manifest is trackable without exposing absolute paths or sensitive environment details.
* Git contamination risk: minimized because only non-sensitive identity records are tracked.
* release and redistribution risk: minimized because raw abstracts, proprietary paths, and operational provenance remain outside the repository.

## Remote filename enumeration requirement

Decision: metadata-only remote inspection is required before acquisition authorization can be considered complete.

Rationale: exact artifact filenames are not yet verified. Inventing filenames is prohibited. A narrow metadata-only authorization can verify filenames, sizes, and digests without executing loading code or downloading raw content into an unprotected location.

Rejected alternative: complete acquisition authorization without exact filename verification.

## Acquisition mechanism class

Decision: explicit allowlist with fail-closed path guards.

Rationale: future acquisition must request the exact dataset repository, exact immutable revision, exact configuration, and exact allowlisted filenames. Any deviation aborts acquisition.

Rejected alternative: broad pattern-based download or configuration enumeration.

## `trust_remote_code`

Decision: permanently prohibited.

Rationale: committed authority documents explicitly prohibit `trust_remote_code` and arbitrary Python loading scripts. No later governance decision may override this prohibition.

Rejected alternative: conditional allowance for trusted repository owners.

## One-run versus continuing authorization

Decision: `P01-03B` is a one-run acquisition event.

Rationale: continuation into later execution stages requires separate explicit governance. Authorization must not be interpreted as continuing permission for transformation, inference, training, or release.

Rejected alternative: blanket execution authorization through acquisition.

## Retention and cleanup

Decision: not yet determined.

Rationale: the current readiness package does not contain sufficient evidence to set retention duration, secure-erasure requirements, or cleanup ownership. Future governance must answer these questions before or alongside acquisition authorization.

## Boundary between P01-03B and P01-03C

Decision: explicit stop after manifest generation.

Rationale: `P01-03B` ends with immutable artifact acquisition and manifest recording. `P01-03C` begins with Parquet opening, schema inspection, normalization, transformation, validation, annotation, inference, retrieval, baseline execution, training, or release. Any transition requires a separate governance decision.

Rejected alternative: continuous pipeline from acquisition through transformation and publication without separate gates.
