# MedScale Roadmap

This roadmap is a **filter, not a backlog.** Only Horizon 1 is committed work; everything
beyond is directional and gated on the prior horizon's artifacts existing. The
authoritative scope document is the
[Research Vision](docs/vision/MEDSCALE_RESEARCH_VISION.md); the narrative is the
[Strategic Blueprint](docs/vision/MEDSCALE_STRATEGIC_BLUEPRINT_V1.md).

## Phases (Horizon 1 — committed)

| Phase | Title | Status | Depends on |
|---|---|---|---|
| **T0** | Repository & engineering foundation | ✅ complete | — |
| **T1** | Literature database & evidence foundation (`medscale.litdb`, ADR-0009) | 🟡 in progress | T0 |
| **T2** | `fhirkit`: validation + grammar | ⬜ not started | T0, JRE + HL7 validator |
| **T3** | MedScale-Bench v0 (deterministic, executable) | ⬜ not started | T2 |
| **T4** | Base-model landscape + constrained-decoding 2×2 | ⬜ not started | T2, T3 |
| **T5** | Training-data pipeline (validator-as-teacher) | ⬜ not started | T3 |
| **T6** | MESC-v0 QLoRA adapter | ⬜ not started | T4, T5 |
| **T7** | Honest evaluation + model card | ⬜ not started | T3, T6 |

**Horizon 1 success** = a green benchmark, a published adapter *or* a published null
result, and a reproducible pipeline — all on Colab-class compute.

### Founder's phase vocabulary → T-phases (one plan, two names)

The founder's directive names five engineering phases; they map onto the T-phases —
this table exists so the two vocabularies never drift into two plans:

| Directive phase | T-phase(s) | Status |
|---|---|---|
| Phase 1 — `medscale.core` (identifiers, hashing, provenance, repro metadata) | T0 | ✅ built as `medscale.reproducibility` + `medscale.provenance`; namespace consolidation proposed in [ADR-0014](docs/adr/0014-core-namespace.md) |
| Phase 2 — `medscale.litdb` (source→raw→parse→record→candidate→verify) | T1 | 🟡 in progress (parsers = next step) |
| Phase 3 — `medscale.evidence` (evidence operating system) | ADR-0009 (schema live); populated by T1 output | 🟡 schema + guards implemented |
| Phase 4 — MedScale-Bench | T3 | ⬜ gated on T2 |
| Phase 5 — AI infrastructure (models, adapters, evaluation) | T4–T7 | 🟡 contracts live: model-agnostic interfaces, registry, recipes, manifests ([ADR-0015](docs/adr/0015-model-agnostic-platform.md)); backends/training/selection gated at T4/T5; landscape + licences in [llm_landscape](docs/models/llm_landscape.md) |

Language policy for all phases: [ADR-0013](docs/adr/0013-language-strategy.md)
(Python-first; Rust/Go role-gated by evidenced triggers).

## Horizons (directional)

- **Horizon 1 — Foundations (2026–2027) · committed.** The above.
- **Horizon 2 — Breadth & rigor (2027–2029) · directional.** More FHIR resources /
  profiles; terminology grounding under licence; MedScale-Bench v1.
- **Horizon 3 — Platform (2029–2032) · directional.** A cited, community-used open
  benchmark and toolkit; reproducibility infrastructure others run.
- **Horizon 4 — Ambition, gated on evidence (2032–2036) · aspirational.** Broader
  verified clinical reasoning; interoperability beyond FHIR where evidence justifies it.

> Horizon definitions follow the Research Vision (the scope authority). Where the
> Blueprint's condensed 3-tier presentation and the Vision's 4-horizon model differ, the
> **Vision governs.**

## Current gate before T1+

See the [handover / T0 exit checklist](docs/execution/README.md) and open issues.
Notably: provision a JRE + pinned HL7 validator (blocks T2). The T1 search strategy is
authored ([search_strategy.md](docs/execution/search_strategy.md)); remaining T1 work:
parsers (raw → `LiteratureRecord`), full round-1 ingestion (needs a Semantic Scholar
API key or long backoffs), PRISMA screening.
