# Paper Publication Workflow

- **Status:** Strategy (ADR-0010, Proposed)
- **Date:** 2026-07-10
- **Related:** [research questions](../research/research_questions.md),
  [reproducibility policy](../research/reproducibility_policy.md), Rule R1/R7,
  [Blueprint §12](../vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md) (the four-paper arc)

## The pipeline

```
Research question (RQ, falsifiable, pre-registered criteria)
        ↓
Code (tagged; quality gate green)
        ↓
Experiments (manifests: seeds, data hashes, env)
        ↓
Results (committed artifacts; 3 seeds, mean ± 95% CI; negative results first-class)
        ↓
Paper (citations from litdb only — R1; claims trace to artifacts — R7)
        ↓
Artifacts (released: bench/dataset/model versions the paper cites)
        ↓
Replication package (tag + manifests + data snapshots + exact commands)
```

No stage may cite a later stage: a paper claim without a released artifact behind it
does not go in the paper.

## Stage gates

1. **Before experiments:** the RQ's falsification criteria are already written in
   `research_questions.md` — experiments test them, never redefine them post hoc.
2. **Before drafting:** every number in the results tables exists as a committed
   artifact with a manifest. Writing starts from artifacts, not from memory.
3. **Citations:** every reference resolves through litdb (identifier + `verified_at` +
   `source_api`). No citation from memory survives review — `check_citations`-style
   validation runs before submission.
4. **Before submission:** the replication package is tagged
   (`paper-<n>-replication-v1`) and verified by re-running headline numbers from the
   package alone, on a clean environment.
5. **Preprint:** arXiv (CC-BY-4.0 where possible) unless the venue forbids;
   the preprint cites artifact versions, not "latest".

## Replication package contents

Repo tag · release manifests of every cited artifact · dataset snapshot hashes ·
environment spec (Python, uv.lock, tool versions) · exact commands with seeds ·
expected outputs (the committed result artifacts) · a README that a stranger can
follow. The test of done: the stranger reproduces the headline table without asking
questions.

## Honesty clauses (restated because they bind hardest here)

- A null result on a pre-registered RQ is submitted with the same effort as a win.
- "State of the art" and superlatives do not appear (Vision §3).
- The benchmark firewall holds in prose too: no paper spins a result the manifest
  does not support.

## Authorship & acknowledgment

Solo-operator phase: operator is author; substantive future contributors per standard
authorship norms (contribution-based, recorded in the paper's repo). Tools (including
AI assistants) are acknowledged per venue policy, never authors.
