# ADR-0016 — Raw-Archive Storage Policy (In-Repo, Trimmed, Capped)

- **Status:** Accepted (2026-07-10, founder approval — **Option A**: in-repo,
  field-trimmed, capped, ~75 MB tripwire. Ingestion unblocked.)
- **Date:** 2026-07-10
- **Deciders:** Founder
- **Related:** [search strategy §4](../execution/search_strategy.md) (archival policy),
  [post-round-1 review](../architecture/reviews/2026-07-10-post-round1.md), Rules R1/R7

## Context

R1 requires raw API responses archived verbatim with recorded hashes. Round 1 (cap 50)
put 18 MB into `data/litdb/` — dominated by OpenAlex, whose default work objects carry
many fields litdb never reads. Git history never shrinks: at cap 200, plus a Semantic
Scholar re-run, plus future rounds, the repository plausibly crosses 100 MB+, hurting
clone times and contributor experience forever. The policy question: where do audit
archives live, and how large may they grow?

## Options

**A — In-repo, field-trimmed, capped (recommended).** Keep archives in git (simplest,
fully self-contained reproducibility) but request only needed fields (OpenAlex
`select=`, S2 `fields=` already minimal) and hold the 50-per-query cap until screening
proves more coverage is needed. Est. footprint per full round: ~4–6 MB.
*Benefits:* zero new infrastructure; clone = complete replay capability; R1 intact
(the trimmed response **is** the verbatim response — trimming happens at request time,
so the archived bytes still match their hash).
*Risks:* repo still grows monotonically, just slower; a future cap-200 round revisits
this.
*Dependencies:* small adapter change (OpenAlex `select=` parameter) + one test.

**B — Git LFS for `data/litdb/raw/`.** *Benefits:* repo stays small; archives keep
versioning. *Risks:* LFS bandwidth quotas on free GitHub; contributors need LFS
installed; replay now depends on LFS availability — a reproducibility dependency on a
quota'd service. *Dependencies:* `.gitattributes`, CI changes, migration of existing
18 MB.

**C — External artifact store (Zenodo/HF dataset per round), hashes committed.**
*Benefits:* repo minimal; DOIs for rounds. *Risks:* replay requires network + a third
party; violates "clone = complete audit trail"; premature before any published dataset
exists. *Dependencies:* release automation (ADR-0010, itself unratified).

## Decision (proposed)

**Option A.** Reproducibility-in-one-clone is worth megabytes; it is not yet worth a
service dependency. Revisit (B or C) via a superseding ADR if `data/` exceeds ~75 MB or
when litdb v1 export ships through the release pipeline.

## Consequences

Positive: audit trail stays self-contained; smallest possible change. Negative: the
repo carries data weight permanently; the ~75 MB tripwire must actually be honored.

## Compliance

On acceptance: add OpenAlex `select=` field list to the adapter (tested), record the
field list in search_strategy §4, and note the tripwire in the data README. Until
accepted: **no further ingestion rounds run.**
