# ADR-0008 — FHIR as the Single Canonical Representation; Other Standards via Boundary Adapters

- **Status:** Proposed (awaiting operator approval)
- **Date:** 2026-07-10
- **Deciders:** Operator (solo founder)
- **Supersedes:** none
- **Superseded by:** none
- **Related:** [interoperability strategy](../architecture/interoperability_strategy.md),
  [ecosystem analysis §3–4](../architecture/ecosystem_analysis.md#3-fhir-and-the-ehr-functional-model),
  [ADR-0003](0003-repository-topology.md), RQ7

## Context

MedScale is FHIR-native by founding thesis: FHIR StructureDefinitions give correctness an
executable definition (validator + grammar). The ecosystem review raised two boundary
questions: (1) how much of the FHIR world MedScale owns — the EHR Functional Model shows
FHIR also underwrites EHR *system* capabilities (workflow, audit, business rules) far
beyond MedScale's remit; (2) whether openEHR (and eventually DICOM) should enter the
architecture — the Cistec `openEHR2FHIRquestionnaire` utility (MIT) demonstrates that
openEHR↔FHIR conversion is viable as a small edge component.

## Decision (proposed)

1. **FHIR is MedScale's single canonical clinical representation.** All internal
   artifacts — grammars, validation, benchmark tasks, training data, knowledge
   extraction — are FHIR. No second clinical model ever lives in the core.
2. **fhirkit scope (T2) is resource-level intelligence only:** validation (structural /
   terminology / profile), StructureDefinition→grammar, FHIRPath query/repair,
   note↔bundle transformation. EHR-*system* functionality (EHR-FM territory: workflow,
   business rules, audit infrastructure, hospital messaging) is permanently out of scope;
   hospital integration belongs to consumers (Afia), per ADR-0003.
3. **Other standards integrate only as optional boundary adapters** (e.g. a future
   `medscale[openehr]` extras group), converting to/from FHIR at the edge; adapter
   output receives no trust and passes fhirkit validation like any input. openEHR is
   Horizon-3 earliest; DICOM later still, metadata-level only, and only behind an
   executable ground truth.
4. **CQL is acknowledged, not adopted:** a natural extension of "executable ground
   truth" beyond FHIRPath, revisited only when a benchmark task requires it.

## Consequences

**Positive:** one validator, one grammar family, one benchmark vocabulary — the
"executable correctness" property stays intact; interop breadth remains possible without
core complexity; fhirkit's T2 scope is sharpened against EHR-system drift.

**Negative / costs:** openEHR-first institutions cannot use MedScale natively until an
adapter exists; conversion at the edge can be lossy (accepted: losses are visible at
validation, not hidden in a dual core).

## Alternatives considered

- **Dual-representation core (FHIR + openEHR).** Rejected: doubles every validator,
  grammar, and benchmark task; destroys the single-oracle property.
- **Adopt openEHR adapter now.** Rejected: no Horizon-1 research question needs it;
  evidence before implementation.
- **Abstract "clinical data model" layer over both.** Rejected: an empty abstraction
  today (architecture rule against premature interfaces).

## Compliance

fhirkit's T2 ticket inherits the scope table in the
[interoperability strategy](../architecture/interoperability_strategy.md). Any future
adapter requires its own ADR naming the demand evidence and licence review.
