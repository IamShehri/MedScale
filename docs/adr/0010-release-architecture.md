# ADR-0010 — Release Architecture: GitHub-Canonical, CI-Published, Gated Distribution

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [ADR-0003](0003-repository-topology.md) (topology),
  [ADR-0005](0005-research-intelligence-scope.md) (identity),
  [docs/releases/](../releases/README.md) (the strategy this ADR ratifies),
  [distribution_hf.md](../architecture/distribution_hf.md) (HF identity record)

## Context

MedScale will publish artifacts across five classes (package, models, datasets,
benchmarks, papers/replication packages) to at least three surfaces (GitHub Releases,
PyPI, Hugging Face). Without a decided architecture, each release becomes an ad-hoc
event: manual uploads, mutable artifacts, cards drifting from sources, and numbers in
papers that no longer trace to bytes. The Hugging Face identity (user `MedScale`, org
`MedScaleAI`) already exists, which makes the temptation to publish early — and
manually — concrete.

## Decision (proposed)

1. **Canonical flow:** `GitHub → CI → GitHub Releases → Hugging Face → users`, never
   the reverse. GitHub is the only source of truth; HF is a distribution mirror; a HF
   repo that drifts from its source tag is a defect.
2. **Releases are immutable.** Tags never move; published artifacts never change;
   fixes are new versions. Deprecation and retraction mark artifacts visibly and never
   delete them.
3. **CI is the only publisher.** PyPI via trusted publishing; HF via release workflows
   behind an operator-approval environment gate. Manual uploads (CLI/web) are
   prohibited. Until the automation exists, distribution simply waits.
4. **Every release carries a manifest** ([releases/reproducibility.md](../releases/reproducibility.md)):
   git SHA, build timestamp, lock hash, tool versions, Python version, seeds, dataset
   snapshot hashes, evaluation manifest, environment, reproduction instructions.
   Release validation fails without it.
5. **Lifecycle states are governed:** PLANNED → IN_DEVELOPMENT → RELEASE_CANDIDATE →
   RELEASED → DEPRECATED/RETRACTED, with per-class checklists
   ([releases/release_process.md](../releases/release_process.md)).
6. **Cards are verification documents.** Model/dataset cards carry mandatory verbatim
   safety statements (not-a-medical-device; synthetic-only) and machine-lintable
   structure.
7. **Model naming reconciliation:** the released family is **MESC** (`mesc-fhir`,
   `mesc-evidence`); "MedScale-Base" exists only as `medscale-base-ref`, a pinned
   configuration release (base id + revision + grammar + decoding params), never
   MedScale-trained base weights — preserving "adapt, don't pretrain".

## Consequences

**Positive:** publication becomes a pipeline with the same integrity properties as the
science (immutable, verified, reproducible); HF can grow without ever becoming a second
source of truth; a future collaborator inherits procedures, not tribal knowledge.

**Negative / costs:** release automation must be built before anything ships to
PyPI/HF (accepted: it is built lazily, per-workflow, when its first consumer release
exists); immutability forces version discipline even for trivial fixes; the operator
approval gate adds a manual step to every distribution (intended).

## Alternatives considered

- **Manual publishing with checklists only.** Rejected: checklists without enforcement
  decay; one tired-evening `hf upload` breaks the provenance chain invisibly.
- **HF as primary home for models/datasets** (common in ML). Rejected: MedScale's
  claims trace to git tags and manifests; HF repos lack the repo-wide gate, CI, and
  ADR context that make a release auditable here.
- **Separate release repositories per artifact.** Rejected: contradicts ADR-0004's
  single-repo discipline; prefixed tags achieve independent cadences without the split.

## Compliance

On acceptance: `docs/releases/` becomes binding policy; the first automation ticket is
`release-package.yml` at v0.2 (PyPI). Until then, nothing is uploaded anywhere beyond
GitHub. Violations (any manual HF/PyPI upload) are treated as integrity incidents and
retracted per the retraction checklist.
