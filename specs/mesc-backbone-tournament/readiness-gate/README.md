# MESC Backbone Tournament Readiness Gate

Status: **DRAFT GOVERNANCE PACKAGE — NO TOURNAMENT EXECUTION AUTHORITY**

Date: 2026-08-19

Canonical base intended for adoption:

- `main`: `c0a9acfc678149736bd9054f7fadae1c31b488a1`
- tree: `71f36f2e49932f82a6ee733833b93306ab5f1f41`

## Purpose

Open the next bounded governance stage after canonical Pilot-01 closeout without starting model execution.

This package defines a readiness and protocol-freeze gate for the future MESC Backbone Tournament. It exists because canonical strategy requires both Pilot-01 closeout and separate authorization before the zero-shot tournament may open.

If this package is later canonically adopted, `FD-MESC-BT-READINESS-1` authorizes exactly one bounded **read-only readiness/protocol-freeze episode**. It does not authorize model-weight access, model download, inference, benchmark execution, training, retrieval, or candidate selection by score.

## Strategic basis

Canonical strategy establishes the following sequence:

1. preserve the accepted Pilot-01 B0 control and provenance;
2. close Pilot-01 under separate governance;
3. design the Backbone Tournament protocol;
4. only after Pilot-01 closeout and separate authorization, open the zero-shot tournament;
5. select one Compact and one Flagship/Reasoner backbone;
6. proceed toward MESC 1.0 only under later gates.

Pilot-01 closeout is a hard prerequisite, not an assumption. Before this readiness authorization may activate, the following objective adoption proof must be mechanically verified against then-current canonical repository truth:

- PR #125 is merged;
- closeout merge commit: `c0a9acfc678149736bd9054f7fadae1c31b488a1`;
- closeout merge tree: `71f36f2e49932f82a6ee733833b93306ab5f1f41`;
- ordered closeout merge parents:
  1. `f69a1b2f1c050aad6fe77eb6273016c764c109f5`
  2. `1e52fa581af8f7894e2cfe3dbd1b07683ae0de72`;
- GitHub merge verification: `verified=true`, `reason=valid`;
- then-current canonical `main` is equal to or descends from `c0a9acfc678149736bd9054f7fadae1c31b488a1`.

If any element of that adoption proof cannot be verified, `FD-MESC-BT-READINESS-1` remains inactive and readiness must not begin.

This package therefore opens only the next governance prerequisite: tournament readiness and protocol freeze.

## Design-time roster

The strategy-preserved design-time roster is:

1. OpenAI `gpt-oss-20b` — flagship/reasoning candidate;
2. Swiss AI `Apertus 1.5 8B` — compact/open/multilingual candidate;
3. Microsoft `Phi-4 Multimodal 5.6B` — lightweight multimodal control;
4. Google `MedGemma 1.5 4B IT` — medical-specialist control;
5. one optional challenger slot, unfilled until the readiness episode applies the same admissibility rules.

These names are family-level design references only. No exact repository ID, immutable revision, tokenizer revision, license conclusion, weight access, or execution authority is granted by listing them here.

## Authorized readiness outputs after adoption

The one bounded readiness episode may produce only documentation/governance outputs that:

- resolve exact public candidate repository/model/tokenizer identities from authoritative sources;
- record immutable revisions or fail closed if they cannot be pinned;
- record license/access/use restrictions and compatibility conclusions;
- record architecture/context/hardware/runtime requirements from authoritative sources;
- freeze candidate admissibility/disqualification rules;
- freeze a synthetic/hand-authored R2-compatible zero-shot evaluation contract;
- freeze prompts, decoding parameters, seeds, parsing, abstention handling, metrics, cost/latency accounting, and deterministic report schemas;
- freeze Compact and Flagship selection rules before any model output is observed;
- produce a candidate manifest, protocol-freeze report, execution plan, and separate **inactive** execution-authorization candidate.

## Explicit non-authority

This package does not authorize:

- downloading or opening candidate model weights;
- Hugging Face gated-model acceptance or access requests;
- any inference or generation;
- any benchmark or tournament execution;
- a second Pilot-01 B0 run or replication;
- B1/B2/B3 execution;
- P01-06+;
- test-partition access, execution, or scientific-content inspection;
- external patient/product/telemetry/PHI data;
- external benchmark ingestion when not R2-compatible;
- training, continued pretraining, SFT, fine-tuning, QLoRA, adapters, preference optimization, RL, or verifier training;
- retrieval activation;
- fallback-model substitution;
- quantization changes or quantized tournament entries;
- MCRL implementation;
- AMGE/audio/biosignal implementation;
- donor runtime dependency import;
- DeepSeek or any other currently excluded model family;
- publication, release, clinical, safety, efficacy, or production claims.

## Fail-closed rule

Readiness must stop and report `BLOCKED` if the Pilot-01 closeout adoption proof fails, or if any required candidate identity, immutable revision, license/access fact, evaluation contract element, R2 boundary, or equal-treatment rule remains materially ambiguous.

No ambiguity may be resolved by downloading weights, running a model, inspecting prohibited data, or inferring permission from strategy text.

## Adoption sequence

1. mechanically verify the Pilot-01 closeout adoption proof above against then-current canonical truth;
2. review this package on one exact head;
3. exact-head CI and CodeQL pass;
4. fresh independent exact-head review reports no unresolved blocking findings;
5. all review threads are resolved/dispositioned;
6. founder separately exercises Ready;
7. founder separately exercises Merge with an expected-head guard;
8. post-merge canonical main/tree/ordered parents are mechanically verified;
9. reverify that canonical `main` remains equal to or descends from the verified Pilot-01 closeout merge;
10. only then may `FD-MESC-BT-READINESS-1` become active for one bounded readiness episode.

Canonical repository truth overrides this package if state moves before adoption.
