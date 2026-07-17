# MESC Pilot-01 Foundation

Status: **frozen foundation implementation**
Branch: `research/mesc-pilot-01-foundation`
Worktree: `C:\Users\Shehr\OneDrive\Desktop\MedScaleFiles\MedScale-mesc-pilot-01`

Context
-------

MESC is a multi-model medical intelligence ecosystem. Pilot-01 is one bounded component of MESC, not the whole system and not a replacement for it. The general MESC reasoning core family is Llama; the Pilot-01 primary training target is `meta-llama/Llama-3.2-3B-Instruct`.

This directory contains the deterministic foundation contracts, specification documents, and proof-of-constraint tests for Pilot-01. No inference, training, dataset download, or remote execution occurs in this pass.

Guarantees
----------

- Deterministic scientific contracts only.
- Stable public MedScale facade is unchanged.
- Protected ALIGN branches and worktrees are unchanged.
- No model weights or datasets are downloaded in this repository.
- No staging, commits, push, PR creation, release, publication, clinical use, or production use occurs here.

Related Documents
-----------------

- `spec.md`
- `specs/mesc-pilot-01/model-selection.md`
- `specs/mesc-pilot-01/model-landscape.md`
- `specs/mesc-pilot-01/data-contract.md`
- `specs/mesc-pilot-01/evaluation-contract.md`
- `specs/mesc-pilot-01/risk-register.md`
- `src/medscale/mesc/contracts.py`
- `src/medscale/mesc/split.py`
- `src/medscale/mesc/manifests.py`
- `src/medscale/mesc/evaluation.py`
