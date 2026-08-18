# MESC Capability Realization Layer (MCRL)

Date: 2026-08-18
Status: FOUNDER-DIRECTED STRATEGY DRAFT
Repository: TheHalfMoon/MESC

## Purpose

MESC should not rely on model weights alone to deliver reliable medical intelligence.

A capable model can still fail because the wrong clinical constraints are active, evidence is not carried across tool seams, uncertainty does not change behavior, verification coverage is incomplete, or a fluent partial result is mistaken for completion.

The **MESC Capability Realization Layer (MCRL)** is the proposed medical-native inference/control layer that reduces this gap between model capability and reliable clinical-task completion.

MCRL is not a new backbone model and is not a replacement for model training. It is a control, state, evidence, verification, and recovery layer around MESC inference.

## External design influence

J-Space Cognition Suite V3.6 is a useful external reference for model-agnostic inference-time control concepts such as selective workspace loading, durable state, verification, recovery, and task-mode routing.

Use policy:

- Treat the DeepSeek V4 × J-Space capability-realization report as a citation/reference only. Its report license is CC BY-ND 4.0 and must not be redistributed as an adapted work.
- J-Space Cognition Suite V3.6 is Apache-2.0 and may be studied or reused subject to its license.
- MCRL must remain a MESC-specific medical design, not a renamed copy of J-Space.
- DeepSeek is not added to the MESC core backbone tournament by this document.

## Design thesis

MESC quality is a product of at least two independent factors:

1. **Capability acquisition** — what the model learns through pretraining, medical post-training, SFT, preference optimization, RL, multimodal alignment, and safety training.
2. **Capability realization** — whether the system activates, preserves, verifies, coordinates, and safely acts on the right information during an actual task.

MESC should optimize both.

## Medical-native state model

MCRL should maintain a compact, typed state rather than an unstructured conversational memory.

### 1. Clinical goal state

Tracks what the task is actually trying to establish.

Examples:

- answer a biomedical question;
- produce a differential diagnosis;
- reconcile conflicting evidence;
- summarize a guideline;
- identify missing information;
- decide whether abstention is required;
- verify a medication safety constraint;
- compare longitudinal imaging.

### 2. Patient-state invariants

High-impact facts that must remain active across branches and tools.

Examples:

- age;
- sex where clinically relevant;
- pregnancy status;
- allergies;
- renal function;
- hepatic function;
- active medications;
- anticoagulation status;
- major diagnoses;
- recent procedures;
- immunosuppression;
- code status where relevant;
- time-sensitive observations.

MCRL must distinguish verified facts from assumptions and missing data.

### 3. Evidence ledger

Every clinically material claim should be linked to evidence state.

Minimum conceptual fields:

- claim_id;
- claim;
- evidence_id;
- source/provenance;
- source revision/hash where available;
- supporting span or structured observation;
- modality;
- temporal relevance;
- support status;
- contradiction status;
- verification status;
- confidence/calibration state.

### 4. Contraindication and safety ledger

Safety-sensitive constraints must be independently trackable and must not disappear when the reasoning path changes.

Examples:

- allergy conflicts;
- drug-drug interactions;
- renal/hepatic dosing restrictions;
- pregnancy contraindications;
- anticoagulation/procedure conflicts;
- emergency escalation triggers;
- pediatric/geriatric constraints;
- red-flag symptoms.

### 5. Temporal clinical state

Medical evidence is time-dependent.

MCRL must be able to distinguish:

- current vs historical findings;
- pre-treatment vs post-treatment state;
- baseline vs follow-up;
- active vs resolved diagnoses;
- stale vs current evidence;
- longitudinal trends;
- causal order where known.

### 6. Modality agreement state

For MESC 2.0 and MESC 3.0, evidence may come from text, imaging, 3D studies, speech, physiologic audio, laboratory data, FHIR resources, and tools.

MCRL should explicitly represent:

- modality agreement;
- modality disagreement;
- unresolved contradiction;
- missing modality;
- low-quality or non-diagnostic input;
- need for a follow-up view/test/record.

## Active workspace policy

Do not keep every fact equally active.

MCRL should maintain a small active working set containing the highest-value constraints for the current reasoning step while preserving the complete durable state externally.

The active set should typically include:

- current goal;
- one or two decisive clinical constraints;
- active evidence question;
- current uncertainty or contradiction;
- next verification action.

The durable ledger retains the rest.

## Constraint broadcast

Critical facts should be derived or verified once, then read from one canonical state object by every dependent reasoning branch.

Examples:

- allergy identity;
- medication list;
- eGFR;
- pregnancy state;
- selected guideline version;
- imaging acquisition date;
- patient age;
- evidence-source revision.

This reduces independent reconstruction and cross-branch inconsistency.

## Epistemic states

MCRL should not reduce uncertainty to one free-form confidence number.

Suggested typed states:

- VERIFIED;
- SUPPORTED;
- PLAUSIBLE_UNVERIFIED;
- UNKNOWN;
- CONFLICTED;
- REFUTED;
- OUTDATED;
- INSUFFICIENT_EVIDENCE;
- NOT_APPLICABLE.

These states must influence behavior.

## Uncertainty controller

A monitoring signal that changes no action is not useful control.

MCRL should map uncertainty/contradiction states to actions such as:

- answer;
- answer with bounded uncertainty;
- request additional context;
- retrieve/verify evidence;
- run an independent calculation;
- seek another modality;
- reconcile conflicting sources;
- abstain;
- escalate an emergency/safety warning.

## Bridge-before-conclusion rule

For load-bearing clinical conclusions, the required intermediate evidence and constraints should be active before the conclusion is committed.

MCRL should discourage conclusion-first rationalization by requiring a checkable bridge such as:

`observation -> interpretation -> evidence/constraint check -> conclusion`

The exact internal reasoning representation must remain implementation-specific and need not expose private chain-of-thought.

## Verification coverage

MCRL must distinguish **a verifier passed** from **the task is verified**.

Every verification result should record:

- verifier identity/type;
- input identity;
- what was checked;
- what was not checked;
- pass/fail/unresolved;
- evidence timestamp/revision;
- coverage scope.

Examples:

- medication interaction checker passed for the current medication list;
- FHIR schema validation passed for one Bundle;
- citation entailment passed for selected claims;
- dosage arithmetic independently recomputed;
- imaging segmentation quality not yet verified.

## Tool-seam continuity

Tool calls are high-risk state boundaries.

Before a tool call MCRL should preserve:

- task goal;
- active constraints;
- input identity;
- expected output/verification contract.

After a tool call MCRL should record:

- exact tool result identity;
- errors/warnings;
- what changed in state;
- what remains unresolved;
- whether an independent verification is needed.

A failed tool path must not be blindly repeated without carrying the failure diagnosis.

## Checkpoint and recovery

Long medical tasks should support explicit checkpoints.

A checkpoint should minimally preserve:

- Goal;
- Patient State;
- Evidence Ledger;
- Verified Claims;
- Active Contradictions;
- Safety Constraints;
- Missing Information;
- Open Tasks;
- Next Action;
- Verification Coverage.

Recovery should resume from the last verified checkpoint, not regenerate the case state from scratch.

## Completion contract

MCRL should refuse to call a task complete merely because a fluent answer exists.

Completion should require the task-specific contract to be satisfied.

Examples:

- all required answer fields present;
- all critical claims have evidence status;
- major contradictions resolved or surfaced;
- uncertainty/abstention state recorded;
- required safety checks performed;
- requested citations entailed;
- required tool outputs verified;
- known missing information explicitly surfaced.

## Integration with MESC Clinical Contract

MCRL operationalizes the existing MESC contract:

- CLAIM
- EVIDENCE
- SOURCE / PROVENANCE
- CONFIDENCE
- UNCERTAINTY
- CONTRADICTION
- MISSING_INFORMATION
- ABSTENTION
- RECOMMENDED_NEXT_EVIDENCE

MCRL should be the runtime mechanism that keeps these fields coherent across multi-step reasoning and multimodal workflows.

## Integration with MESC 1.0

MESC 1.0 should use MCRL for:

- evidence-grounded QA;
- guideline reasoning;
- medication/safety reasoning;
- uncertainty-aware answering;
- abstention;
- citation verification;
- clinical calculations;
- tool/FHIR workflows.

MCRL evaluation should be separate from raw model-quality evaluation so the project can measure:

- base model capability;
- post-training gain;
- capability-realization gain;
- end-to-end gain.

## Integration with MESC 2.0 / AMGE

AMGE should emit grounded medical observations into the same evidence/state contract.

Examples:

- imaging finding;
- location;
- measurement;
- segmentation identity;
- acquisition timestamp;
- modality;
- confidence/quality;
- longitudinal comparison;
- supporting image region reference.

MCRL then coordinates imaging evidence with clinical text and other data without collapsing visual uncertainty into unsupported textual certainty.

## Integration with MESC 3.0 / Medical Omni

MCRL becomes the common coordination layer for:

- clinical text;
- medical images;
- 3D imaging;
- physician dictation;
- patient speech;
- heart sounds;
- lung sounds;
- cough/breathing;
- structured EHR/FHIR data;
- evidence retrieval;
- external tools.

Speech-derived semantic content and physiologic acoustic evidence must remain distinguishable in provenance and uncertainty state.

## Safety requirements

MCRL must not be presented as autonomous clinical authority.

It should support:

- uncertainty-aware assistance;
- human-review boundaries;
- explicit emergency escalation rules;
- source and timestamp provenance;
- fail-closed behavior where required;
- auditability of tool and evidence decisions.

## Evaluation plan

Create a dedicated MCRL evaluation track rather than assuming general model benchmarks cover inference control.

Suggested metrics/tasks:

- constraint retention across long tasks;
- contradiction detection;
- stale-evidence detection;
- tool-seam state retention;
- recovery after injected tool failure;
- premature-completion rate;
- verification-coverage accuracy;
- abstention-trigger accuracy;
- emergency-escalation recall;
- medication-safety constraint retention;
- modality-disagreement detection;
- longitudinal-state consistency;
- citation-entailment preservation after multi-step tool use.

Ablations should compare at minimum:

1. Base model without MCRL;
2. Base model + lightweight state contract;
3. Full MCRL;
4. Full MCRL with selected verification tools.

## Data / privacy boundary

Do not persist PHI in experimental MCRL ledgers unless a future explicitly approved architecture provides the required privacy/security controls.

Current MESC research remains synthetic/open/permitted-data only under existing project governance.

## Implementation principle

Start small.

Do not immediately build a complex autonomous agent framework.

Recommended first implementation slice after explicit authorization:

1. typed `ClinicalState`;
2. typed `EvidenceClaim` / `EvidenceLedger`;
3. typed epistemic state;
4. deterministic checkpoint serialization;
5. verification-coverage records;
6. abstention/uncertainty action policy;
7. synthetic-fixture tests;
8. no clinical deployment claim.

Then measure whether each additional mechanism produces a reproducible gain.

## Non-goals

This strategy document does not authorize:

- changes to current Pilot-01 B0 execution;
- DeepSeek model use;
- model-weight changes;
- training;
- real patient use;
- AMGE implementation;
- audio implementation;
- retrieval activation;
- P01-06;
- autonomous diagnosis or treatment.

## Strategic outcome

MESC should compete on two axes simultaneously:

`best medical model capability`

and

`best medical capability realization`

The desired end state is not merely a model that knows medicine, but a system that preserves the right clinical constraints, grounds claims in evidence, notices contradictions, verifies critical operations, recovers from failures, and abstains when the evidence does not support a safe answer.
