# MESC Frontier Program — Path to a Top-Tier Open Medical Model Family

Date: 2026-08-18
Status: FOUNDER-DIRECTED STRATEGY DRAFT
Repository: TheHalfMoon/MESC

## Objective

The goal is not to create another medical fine-tune.

The goal is to make MESC a leading open medical model family on three dimensions simultaneously:

1. **Scientific capability** — strong medical reasoning across realistic tasks, not only exam QA.
2. **Trust and auditability** — evidence provenance, abstention, uncertainty, verification, decontamination, reproducibility, and transparent evaluation.
3. **Adoption** — a compact model people can actually run, a flagship model researchers respect, excellent Hugging Face packaging, demos, quantizations, documentation, and reproducible results.

## Frontier conclusion

Recent evidence suggests that MESC should not compete primarily by parameter count.

The strongest opportunity is to combine:

- fully auditable medical post-training;
- a carefully selected modern backbone;
- evidence-grounded reasoning;
- explicit abstention and calibration;
- MCRL capability-realization control;
- longitudinal EHR/FHIR competence;
- multimodal medical perception;
- dynamic, process-oriented evaluation;
- open release engineering.

## 1. Preserve Pilot-01 as scientific control

Do not rewrite the current Llama-3.2-3B-Instruct B0 experiment because newer models exist.

Pilot-01 remains valuable as a clean, pinned, general-model control.

This protects scientific provenance and gives later MESC systems a meaningful before/after comparison.

## 2. Backbone tournament, not backbone ideology

Current core tournament:

1. `gpt-oss-20b` — reasoning/flagship candidate.
2. `Apertus 1.5 8B` — compact, fully open, multilingual, native text/image/audio candidate.
3. `Phi-4 Multimodal 5.6B` — lightweight native multimodal control.
4. `MedGemma 1.5 4B IT` — medical-specialist control.

Keep one challenger slot for a new model that appears before tournament freeze.

Selection must use MESC-specific evidence, not vendor benchmark claims.

Tournament outputs:

- one **MESC-Compact** backbone;
- one **MESC-Reasoner / Flagship** backbone.

Do not deeply train every candidate.

## 3. Fully open medical post-training is a first-class moat

Fully Open Meditron (2026) is an important reference point.

Its key lessons for MESC:

- expose the data construction pipeline, not only weights;
- normalize multiple medical data sources into one auditable schema;
- include guideline-grounded examples;
- perform system-wide contamination controls;
- use gold-label resampling / teacher-output quality control rather than accepting synthetic generations blindly;
- include clinician validation;
- evaluate on use-aligned clinical tasks, not only medical exams.

MESC should aim to exceed this standard with stronger provenance, uncertainty/abstention labels, longitudinal structure, multimodality, and Arabic coverage.

## 4. MESC Data Engine should become a research contribution itself

Every training item should be independently traceable where licensing permits.

Core fields should include:

- example_id;
- source_id;
- source_revision;
- source_license;
- source_hash;
- source timestamp;
- evidence spans / observation references;
- task type;
- specialty;
- patient population;
- language;
- answer/target;
- uncertainty class;
- abstention target;
- contradiction state;
- verification state;
- clinician review state;
- contamination state;
- synthetic-generation provenance if applicable.

### Required data classes

Training must intentionally contain:

- sufficient evidence;
- insufficient evidence;
- contradictory evidence;
- stale evidence;
- misleading distractors;
- missing information;
- ambiguous clinical states;
- emergency situations;
- medication safety conflicts;
- guideline conflicts/version differences;
- longitudinal changes;
- modality disagreement.

## 5. Abstention must be trained, not requested by prompt

MedAbstain-style evidence shows that high accuracy does not guarantee appropriate abstention, and that larger models/prompting alone do not solve the problem.

MESC should therefore treat abstention as a supervised and evaluated capability.

Suggested abstention targets:

- `ANSWER_SUPPORTED`;
- `ANSWER_WITH_UNCERTAINTY`;
- `REQUEST_MORE_INFORMATION`;
- `VERIFY_EVIDENCE`;
- `ABSTAIN_INSUFFICIENT_EVIDENCE`;
- `ABSTAIN_CONFLICTED_EVIDENCE`;
- `ESCALATE_SAFETY`.

Calibration metrics should be reported alongside accuracy.

## 6. Verification should become trainable

Recent medical reasoning work supports tool-integrated verification and iterative evidence access rather than one scalar reward.

MESC should eventually separate:

- generator;
- verifier;
- evidence retriever/tool layer;
- MCRL state/control layer.

A MESC verifier should be able to provide structured justification/coverage, not only a numeric score.

Potential training path:

1. SFT generator;
2. SFT verifier;
3. evidence-grounded verifier training;
4. tool-integrated verification;
5. verifiable RL only on tasks with objective or clinically defensible reward functions.

Do not use RL where the reward is merely another model's uncalibrated preference.

## 7. MESC-Eval must be harder than the training objective

Core external reference families:

- HealthBench;
- HealthBench Professional;
- MedHELM;
- Medmarks;
- MedR-Bench;
- CSEDB-style safety/effectiveness evaluation;
- BRIDGE real-world clinical text tasks;
- MedAgentBench;
- FHIR-AgentBench;
- LongMedBench;
- TIMER-style longitudinal reasoning;
- MedAraBench for Arabic medical QA.

### MESC-Eval tracks

#### A. Knowledge and reasoning

- medical knowledge;
- diagnostic reasoning;
- examination/test selection;
- treatment planning;
- clinical calculations.

#### B. Evidence and truthfulness

- evidence fidelity;
- citation entailment;
- unsupported-claim rate;
- contradiction detection;
- stale-evidence recognition;
- provenance preservation.

#### C. Uncertainty and safety

- abstention accuracy;
- calibration error;
- emergency escalation;
- medication safety;
- guideline adherence;
- high-risk-case degradation;
- harmful overconfidence.

#### D. Process stability

Inspired by dynamic/process-oriented evaluation:

- omitted evidence;
- delayed evidence;
- contradictory evidence;
- state updates after new evidence;
- hallucination propagation;
- self-correction;
- premature completion.

#### E. Longitudinal intelligence

- temporal boundary adherence;
- trend detection;
- medication changes;
- disease trajectory;
- treatment response;
- cross-visit memory;
- implicit time inference;
- long-horizon decision making.

#### F. Agent/FHIR competence

- correct FHIR resource retrieval;
- tool selection;
- API/tool parameter correctness;
- multi-step EHR tasks;
- verification after write-like operations in synthetic environments;
- recovery after tool failure.

#### G. Multimodal medical intelligence

- image interpretation;
- localization/segmentation grounding;
- multi-image/longitudinal comparison;
- 3D imaging;
- modality disagreement;
- speech understanding;
- physiologic sound reasoning;
- future biosignal integration.

#### H. Population/language robustness

- English;
- Arabic;
- age groups;
- pregnancy;
- CKD/CLD;
- immunocompromised patients;
- sex/gender where clinically relevant;
- geographic variation;
- specialty-specific performance.

## 8. Longitudinal EHR reasoning is a major MESC opportunity

Recent work consistently shows that modern LLMs remain weak at longitudinal and structured clinical reasoning.

MESC should treat time as a first-class data type.

Required design elements:

- explicit timestamps;
- episode boundaries;
- medication start/stop/change events;
- problem-state transitions;
- lab trends;
- imaging chronology;
- treatment-response events;
- temporal provenance;
- stale/current distinction.

MCRL's temporal clinical state should become the runtime counterpart of this training representation.

## 9. FHIR should be an evaluation and tool-use surface, not just a serialization format

MESC should support realistic FHIR-native agent evaluation.

Important capabilities:

- navigating resource relationships;
- selecting the right FHIR endpoint/tool;
- multi-resource synthesis;
- temporal joins;
- medication/condition/observation reconciliation;
- provenance-aware answers;
- fail-closed behavior on missing resources;
- deterministic tool-call auditing.

MedAgentBench and FHIR-AgentBench demonstrate that this remains an unsolved area and should become a core MESC differentiator.

## 10. MCRL should be evaluated as an independent contribution

Do not hide MCRL inside the model and claim all gain comes from weights.

Required ablations:

1. base model;
2. medical post-trained model;
3. medical model + lightweight state contract;
4. medical model + full MCRL;
5. medical model + MCRL + verification tools.

Measure:

- accuracy;
- safety;
- abstention;
- contradiction handling;
- state retention;
- tool recovery;
- verification coverage;
- cost/latency.

## 11. MESC 1.0 — Evidence-Calibrated Medical Reasoning

MESC 1.0 should ship only after demonstrating gains across multiple independent axes.

Core training ladder:

1. base evaluation;
2. optional medical continued pretraining if ablation proves value;
3. evidence-grounded SFT;
4. clinical-reasoning SFT;
5. uncertainty/abstention SFT;
6. safety SFT;
7. preference optimization;
8. verifier training;
9. bounded verifiable RL;
10. calibration;
11. adversarial evaluation;
12. held-out clinician review.

### Success should not mean

- highest MedQA score only;
- one benchmark win;
- LLM-as-judge win without human calibration;
- synthetic-only evaluation;
- training/test contamination;
- performance without subgroup analysis.

## 12. MESC 1.1 — Arabic as a major differentiator

MedAraBench 2026 confirms that Arabic medical evaluation remains underdeveloped relative to English and spans 19 specialties with multiple difficulty levels.

MESC should build an Arabic medical track with:

- bilingual terminology normalization;
- Arabic medical reasoning;
- English-Arabic evidence alignment;
- Arabic patient communication;
- dialect sensitivity where appropriate;
- Saudi/Gulf and broader Arab-region clinical-context evaluation;
- Arabic safety and emergency communication;
- independent Arabic clinician review.

Do not translate English datasets blindly and call the result Arabic clinical competence.

## 13. MESC 2.0 — AMGE should be a medical perception system

AMGE should not be one generic image adapter.

Reference directions:

- MedGemma 1.5 for compact multimodal medical generation;
- CT-FM for 3D CT representations;
- multi-view/video foundation approaches such as EchoPrime for echocardiography;
- specialist pathology/ophthalmology/radiology encoders where licensing permits;
- segmentation/localization experts.

AMGE outputs should enter the same MESC Evidence Contract and MCRL state.

Every imaging finding should preserve, where feasible:

- modality;
- study identity;
- acquisition time;
- anatomical location;
- measurement;
- region/patch/frame provenance;
- image quality;
- uncertainty;
- comparison with prior study.

## 14. MESC 3.0 — Medical Omni should distinguish speech, sound, and signals

### Clinical speech

- physician dictation;
- patient speech;
- clinical conversation;
- radiology/pathology dictation;
- multilingual speech.

### Physiologic acoustics

- heart sounds;
- lung sounds;
- cough;
- breathing/exhalation;
- digital stethoscope signals.

StethoLM/StethoBench and health-acoustic foundation work demonstrate that physiologic sound is a real modeling domain, not a transcription problem.

### Future biosignal extension

After audio is stable, MESC should evaluate adding:

- ECG;
- PPG;
- continuous vital signs;
- wearable sensor streams.

Recent ECG foundation models and cardiac sensing foundation models show that large-scale self-supervised biosignal pretraining can transfer across devices and tasks, but device/domain shift remains a major risk.

Do not fold biosignals into MESC 3.0 without their own provenance, sampling, device, and calibration contracts.

## 15. Do not assume a medical-specialized model always beats a frontier general model

Recent independent evaluations show that newer general-purpose frontier models can outperform older specialized clinical AI tools or older medical fine-tunes.

Therefore MESC must continuously compare against:

- current strong general models;
- current open-weight reasoning models;
- current medical specialists;
- its own previous releases.

The backbone tournament and recurring challenger slot should remain permanent governance mechanisms.

## 16. Compact + Flagship is the right release architecture

### MESC-Compact

Optimize for:

- Colab;
- consumer/workstation GPUs;
- low operational cost;
- fast inference;
- research reproducibility;
- quantization;
- easy fine-tuning.

### MESC-Reasoner

Optimize for:

- maximum reasoning quality;
- complex evidence synthesis;
- difficult clinical workflows;
- verifier/tool integration;
- research leadership.

Both should use the same MESC data/eval contracts where technically possible.

## 17. Hugging Face leadership is a release-engineering problem too

Hugging Face's current release guidance favors:

- one repository per checkpoint/variant;
- safetensors;
- comprehensive model cards;
- correct metadata for discoverability;
- linked training datasets;
- structured evaluation results;
- library integration;
- Collections for model families;
- interactive Spaces;
- separate quantized variants such as GGUF.

MESC should release as a coherent Hub ecosystem:

- `MESC-Compact`;
- `MESC-Reasoner`;
- `MESC-AMGE`;
- `MESC-Omni`;
- MESC datasets;
- MESC-Eval datasets;
- MESC demo Space;
- MESC leaderboard Space;
- paper/technical report;
- collection linking all assets.

Model-card metadata should expose real evaluation results so Hugging Face can surface them in model and benchmark views.

## 18. Build a MESC public leaderboard, not only a private scorecard

A public MESC-Eval leaderboard can become a project asset independent of MESC model weights.

Requirements:

- reproducible evaluation harness;
- versioned benchmark sets;
- contamination policy;
- private/held-out subsets where legally/ethically needed;
- result provenance;
- model/version hashes;
- inference configuration;
- cost/latency reporting;
- safety dimensions;
- subgroup dimensions;
- explicit uncertainty/abstention metrics.

This creates ecosystem pull: other medical models will benchmark against MESC, increasing scientific visibility even when they are competitors.

## 19. Clinician calibration is mandatory for serious claims

Use LLM judges for scale, but calibrate them against clinicians.

For major releases:

- define physician-authored rubrics;
- use blinded randomized review;
- measure inter-rater agreement;
- calibrate automated judges;
- adjudicate high-risk disagreements;
- publish the evaluation protocol;
- preserve anonymized evaluation provenance where permitted.

## 20. Top ten MESC moats

The strongest defensible MESC combination is:

1. fully auditable medical data/training pipeline;
2. modern backbone selection via tournament;
3. evidence-grounded reasoning;
4. trained abstention/calibration;
5. MCRL medical capability-realization control;
6. verifier + tool-integrated verification;
7. longitudinal EHR/FHIR intelligence;
8. AMGE multimodal medical perception;
9. Arabic + global-health capability;
10. public, dynamic, process-aware MESC-Eval + excellent Hugging Face release engineering.

No single competitor currently owns all ten as one coherent open system.

## 21. Priority order

### P0 — Do now

- preserve the completed, canonically accepted Pilot-01 B0 result and exact provenance;
- merge/review strategic docs separately from execution;
- design backbone tournament protocol;
- design MESC-Eval v0 taxonomy;
- design data provenance/decontamination contract.

### P1 — After Pilot-01 closeout and separate authorization

- open the zero-shot tournament only after separate authorization;
- select Compact + Reasoner finalists;
- reproduce Fully Open Meditron-style medical post-training baselines;
- add MESC-specific abstention/contradiction/evidence data;
- establish clinician-calibrated evaluation subset.

### P2 — MESC 1.0

- train selected finalists;
- build verifier;
- implement first bounded MCRL slice;
- evaluate HealthBench/MedHELM/Medmarks/BRIDGE-style tasks;
- add longitudinal + FHIR agent tracks;
- release Compact first if quality threshold is met.

### P3 — MESC 1.1

- Arabic medical data/evals;
- bilingual evidence grounding;
- Arabic clinician evaluation.

### P4 — MESC 2.0

- AMGE specialists;
- 2D + 3D + longitudinal imaging;
- region/measurement provenance;
- multimodal contradiction evaluation.

### P5 — MESC 3.0

- clinical speech;
- cardiopulmonary audio;
- medical audio reasoning;
- later biosignal/wearable extension after separate validation.

## 22. Hard boundaries

- No benchmark/test leakage into training.
- No untracked synthetic teacher data.
- No silent license incompatibilities.
- No unsupported clinical deployment claims.
- No model-family weight merging without a scientifically valid method and explicit authorization.
- No replacing clinician evaluation with LLM judges alone for high-stakes claims.
- No adding DeepSeek or other excluded model families to the core stack without explicit founder policy revision.
- No claiming best-in-class from one benchmark.
- No hiding negative subgroup or safety results.

## Final strategic thesis

MESC should aim to become **the open medical AI system that is hardest to fool, easiest to audit, most explicit about uncertainty, strongest across real clinical workflows, and easiest for researchers to reproduce and extend**.

If MESC only competes on medical QA accuracy, it can be overtaken by the next general-purpose model release.

If MESC owns the complete stack — data provenance, post-training, abstention, verification, longitudinal/FHIR reasoning, MCRL, multimodality, Arabic capability, and public process-aware evaluation — it can remain scientifically valuable even as backbones change.
