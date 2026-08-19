# MESC Backbone Tournament — Design-Time Candidate Roster

Status: **FAMILY-LEVEL DESIGN REFERENCES ONLY — NO ADMISSION / NO WEIGHT ACCESS / NO EXECUTION**

Date: 2026-08-19

## Canonical strategy roster

| Slot | Family-level candidate | Intended role | Current readiness state |
|---|---|---|---|
| 1 | OpenAI `gpt-oss-20b` | Flagship / reasoning candidate | `UNRESOLVED — READINESS REQUIRED` |
| 2 | Swiss AI `Apertus 1.5 8B` | Compact / open / multilingual candidate | `UNRESOLVED — READINESS REQUIRED` |
| 3 | Microsoft `Phi-4 Multimodal 5.6B` | Lightweight multimodal control | `UNRESOLVED — READINESS REQUIRED` |
| 4 | Google `MedGemma 1.5 4B IT` | Medical-specialist control | `UNRESOLVED — READINESS REQUIRED` |
| 5 | Challenger slot | Optional pre-execution challenger | `EMPTY` |

## What readiness must resolve per candidate

For each non-empty slot, the readiness episode must record:

- exact model repository/identifier;
- immutable model revision;
- exact tokenizer/processor repository and immutable revision;
- authoritative publisher/source;
- model family/architecture and parameter class;
- supported modalities relevant to the tournament;
- context/output limitations relevant to equal treatment;
- license and material use restrictions;
- gating/access requirements;
- whether weight access can be performed under later explicit authorization;
- whether remote/API-only execution would create unequal treatment or reproducibility concerns;
- hardware/runtime feasibility;
- required library/runtime versions where authoritative documentation makes them material;
- security implications such as remote code requirements;
- one deterministic disposition: `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`, `NOT_ADMITTED`, or `BLOCKED`.

Disposition semantics are mandatory:

- `BLOCKED`: required evidence remains unresolved, unproven, contradictory, or unavailable. Any `BLOCKED` non-empty roster slot forces the overall readiness verdict to `BLOCKED`.
- `NOT_ADMITTED`: authoritative evidence conclusively proves a disqualifying policy, license/access, architecture, security, or feasibility condition. It cannot be used merely because evidence is missing.
- `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`: all required admission evidence is proven; this only permits inclusion in a later inactive execution-authorization candidate and grants no execution authority.

## Challenger rule

The challenger slot may be populated only before any tournament execution and only if:

- it is not from an excluded model family;
- its exact identity/revision/license/access can be proven;
- it can be evaluated under materially equivalent zero-shot rules;
- it has a clear scientific rationale relative to the four strategy-preserved candidates;
- adding it does not require weakening R2, safety, reproducibility, or equal-treatment rules.

If no challenger meets these conditions, the slot remains empty.

An intentionally empty challenger slot is not `BLOCKED`; only a populated or required non-empty roster slot with unresolved evidence can create a candidate-level blocker.

## No silent substitution

A missing, gated, withdrawn, incompatible, or infeasible candidate may not be silently replaced with a related checkpoint or quantized derivative.

Any substitution changes candidate identity and must be explicitly recorded in the readiness package before execution authorization is proposed.

## No ranking yet

This roster contains no tournament result and no implied winner.

No candidate may be described as Compact/Flagship-selected until a separately authorized tournament is executed and its outputs pass their own acceptance and review gates.
