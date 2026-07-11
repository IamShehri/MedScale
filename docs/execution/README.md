# Execution

- **Status:** Placeholder (directory established during Foundation Consolidation)
- **Date:** 2026-07-09

This directory will hold MedScale's execution and phase-planning documents — the concrete
tickets and specifications that translate the strategic foundation into work. It is
intentionally empty at freeze time: **no phase (T0 onward) has started.**

## Intended contents (to be authored when each phase begins; not yet present)

| Document | Phase | Purpose | Status |
|---|---|---|---|
| [`search_strategy.md`](search_strategy.md) | T1 | Per-source queries, PRISMA workflow, and reproducible ingestion design | ✅ Authored (v1) |
| `benchmark_spec.md` | T3 | Task and metric definitions for MedScale-Bench | Missing — to author |
| `constrained_decoding_hypothesis.md` | T2 | The form-vs-content experiment design (referenced by the vision) | Missing — to author |
| Phase tickets (T0–T7) | all | One-ticket-per-session execution records | Missing — to author |

## Phase map (see the Strategic Blueprint §6–§8 and §17)

- **T0** — Repository foundation *(✅ complete — ADR-0003/0004)*
- **T1** — Literature database & evidence foundation *(🟡 in progress — `medscale.litdb`, ADR-0009)*

### Screening the corpus (`medscale screen`)

Human title/abstract screening turns the deduplicated corpus into a validated evidence
foundation. No model is involved — decisions are the operator's, recorded in an
append-only audit trail (`data/litdb/screening/review_log.jsonl`).

```
uv run medscale screen status                    # PRISMA counts (reproducible from the log)
uv run medscale screen next --reviewer <you>     # screen the pending queue; q to stop
uv run medscale screen resume --reviewer <you>   # same as next; picks up where you left off
uv run medscale screen next --limit 50           # cap a session
```

Per record: `[1] Include  [2] Exclude  [3] Maybe  [4] Duplicate  [5] Skip  [q] Quit`.
Exclude prompts for a machine-readable reason. Decisions map to PRISMA stages
(include→screened, exclude/duplicate→excluded); corrections are new events (history is
never edited). Interrupt any time — progress is saved after every decision.
- **T2** — FHIR toolkit (`fhirkit`)
- **T3** — MedScale-Bench
- **T4–T7** — Model landscape, training pipeline, MESC-v0 adapter, evaluation

> This is a documentation placeholder. No engineering content lives here. Nothing in this
> directory authorizes starting a phase; phases begin only under explicit operator approval.
