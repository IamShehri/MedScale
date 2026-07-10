# MedScale Documentation

The canonical documentation for MedScale. Start here.

## Reading order

1. [README](../README.md) — what MedScale is, in one page.
2. [Strategic Blueprint](vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md) — the full narrative.
3. [Research Vision](vision/MEDSCALE_RESEARCH_VISION.md) — scope authority (what is / is not).
4. [Research Questions](research/research_questions.md) — RQ1–RQ7.
5. [Program Rules R1–R7](governance/rules.md) — the rules the docs cite by number.
6. [Glossary](glossary.md) — terminology.

## Map

| Area | Documents |
|---|---|
| **Vision** | [Strategic Blueprint](vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md) · [Research Vision](vision/MEDSCALE_RESEARCH_VISION.md) |
| **Research** | [index](research/README.md) · [research questions](research/research_questions.md) · [paper taxonomy](research/paper_taxonomy.md) · [reproducibility policy](research/reproducibility_policy.md) |
| **Governance** | [rules R1–R7](governance/rules.md) · [governance index](governance/README.md) |
| **Architecture** | [ecosystem analysis](architecture/ecosystem_analysis.md) · [reference architecture](architecture/medscale_reference_architecture.md) · [AI model strategy](architecture/ai_model_strategy.md) · [OpenMed strategy](architecture/openmed_integration_strategy.md) · [interoperability strategy](architecture/interoperability_strategy.md) · [HF distribution](architecture/distribution_hf.md) |
| **Decisions** | [ADR template](adr/0000-template.md) · [0003 topology](adr/0003-repository-topology.md) · [0004 T0 scope](adr/0004-t0-foundation-scope.md) · [0005 research-intelligence scope](adr/0005-research-intelligence-scope.md) · [0006 model access](adr/0006-model-access-strategy.md) · [0007 OpenMed adapter](adr/0007-openmed-adapter.md) · [0008 FHIR canonical](adr/0008-interoperability-fhir-canonical.md) · [0009 evidence model](adr/0009-evidence-model.md) — all Accepted |
| **Guides** | [developer guide](guides/developer_guide.md) |
| **Execution** | [phase planning (T0–T7)](execution/README.md) |
| **Archive** | [superseded material](archive/) |

## Canonical sources & precedence

To avoid drift between overlapping documents, precedence is explicit:

- **Scope** (what is in/out of the program) → the **Research Vision** governs.
- **Narrative / external presentation** → the **Strategic Blueprint**.
- **Rules cited by number** → **`governance/rules.md`**.
- **A decision of record** → the relevant **ADR** overrides prose elsewhere.

Where the Blueprint's condensed 3-horizon presentation and the Vision's 4-horizon model
differ, the **Vision governs** (see [ROADMAP](../ROADMAP.md)).

## Naming conventions

- Docs: `lower_snake_case.md` (except the two flagship vision docs and root community
  files such as `README`, `LICENSE`, which are `SCREAMING_SNAKE` / conventional).
- ADRs: `NNNN-kebab-title.md`, append-only numbering.
- Front-matter: a short block of `Status` / `Date` / `Related` at the top of each doc.
