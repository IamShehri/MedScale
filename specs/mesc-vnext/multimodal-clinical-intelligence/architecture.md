# MESC vNext Target Architecture

## 1. Target architectural position

MESC is ratified as:

- open
- auditable
- evidence-grounded
- FHIR-native
- uncertainty-aware
- model-agnostic
- multimodal clinical intelligence

## 2. Architecture planes

### Trust / Authority / Safety Plane

Governs who may observe, suggest, recommend, authorize, and execute. Clinician
authority remains a first-class contract. Autonomous clinical execution is not
authorized by architecture alone.

### FHIR-native Clinical Data Fabric

FHIR remains the canonical interoperability boundary. All clinical data enters
and exits MESC through FHIR-native contracts. Multimodal perception augments but
does not replace structured longitudinal clinical state.

### Modality Adapters

Future modality adapters may serve:

- text
- documents
- medical images
- CT / MRI / pathology
- ECG / waveforms
- medical audio / ASR
- live video
- wearables / biosignals

Each adapter is replaceable. No adapter is a hard dependency of the core
orchestrator.

### Clinical Observation Ledger

A future typed ledger that persists perceptual and model-derived observations
rather than leaving them as hidden model context. Each observation carries:

- observation identity
- modality
- clinical concept or value
- source / provenance
- confidence / uncertainty
- temporal binding
- supporting evidence reference
- contradiction state

### Longitudinal Patient State

First-class reasoning input derived from FHIR resources and accumulated
observations. Not a replacement for structured FHIR data; a derived reasoning
view over it.

### Clinical Intelligence Orchestrator

Coordinates:

- fast interaction loop
- clinical planner
- perception coordinator
- evidence engine
- contradiction / safety engine
- optional specialist routing

The orchestrator is not a single monolithic agent; it is a coordination
contract.

### Information-Need / Next-Best-Clinical-Action Planner

Actively reasons about missing information and proposes the next useful
clinical information action.

### Uncertainty + Abstention Engine

Preserves explicit uncertainty at every clinical intelligence layer. Abstention
is a valid clinical action.

### Clinician Oversight / Cockpit Contract

Distinguishes observation, suggestion, recommendation, authorization, and
execution. The clinician retains authority over clinical actions.

### Evaluation and Reproducibility Lab

Each modality and capability requires explicit evaluation before being
considered mature. Reproducibility remains a first-class contract.

## 3. Relationship to AMIE

AMIE and related research are reference architecture / competitive research.
MESC is not an AMIE clone. MESC differentiators:

- open architecture
- model agnosticism
- FHIR-native longitudinal state
- typed provenance
- evidence grounding
- reproducibility
- explicit uncertainty
- auditable observation state
- clinician authority
- formal evaluation contracts