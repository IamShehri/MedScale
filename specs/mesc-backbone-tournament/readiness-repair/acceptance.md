# MESC Backbone Tournament Readiness Repair — Acceptance Contract

Status: **DRAFT / INACTIVE**

Date: 2026-08-20

## Package adoption criteria

This repair package is eligible for canonical adoption only if all are true:

- canonical `main` at review time is mechanically identified and the package is not relying on stale base truth;
- PR #126 / merge `24faa6fae47f96236407f8e1fa2b262abba5894f` remains in canonical ancestry;
- the prior one-shot readiness decision is canonically reconciled as consumed and terminally `BLOCKED`, not reusable;
- changes are documentation/governance only;
- no model access, gated acceptance, inference, training, retrieval, test access, quantization change, challenger addition, or downstream implementation is introduced;
- the proposed authorization is limited to one read-only repair/protocol-freeze-completion episode;
- exact-head CI passes;
- exact-head CodeQL passes;
- fresh independent exact-head review reports no unresolved blocking findings;
- all review threads are resolved or explicitly dispositioned with recorded evidence;
- founder separately exercises Ready;
- founder separately exercises Merge with exact-head protection;
- post-merge canonical main/tree/ordered parents are mechanically verified;
- canonical main remains equal to or a descendant of the readiness-gate merge after adoption.

## Required outputs of an activated repair episode

A valid episode must produce a deterministic package containing:

1. exact canonical main/tree inspected at episode start and end;
2. controlling governance inventory;
3. exact Apertus 1.5 legal/AUP artifact identity and readable authoritative terms, or an explicit blocker;
4. evidence binding the interpreted Apertus terms to the exact authoritative version inspected;
5. material Apertus use restrictions and deterministic R2 compatibility disposition;
6. refreshed exact model IDs and immutable revisions for all four non-empty strategy-preserved candidates;
7. refreshed exact tokenizer/processor IDs and immutable revisions;
8. refreshed authoritative license/access/gating evidence for every non-empty candidate;
9. architecture/context/modality/security/runtime/hardware-feasibility evidence for every non-empty candidate;
10. deterministic disposition for every non-empty candidate using `BLOCKED`, `NOT_ADMITTED`, or `ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE`;
11. challenger slot fixed `EMPTY`;
12. execution-viable roster proof showing at least two distinct admitted candidates;
13. if and only if items 3–12 contain no blocker, a frozen R2-compatible synthetic/hand-authored corpus specification covering all six required axes;
14. exact corpus count and deterministic corpus digest/hash;
15. frozen system prompt and task prompt templates;
16. frozen message formatting and input/output-length rules;
17. frozen decoding parameters and deterministic seed policy;
18. frozen stop, parser, timeout, retry, generation-failure, and abstention rules;
19. frozen metric definitions, weights if any aggregate is used, and all component reporting requirements;
20. frozen Compact eligibility, thresholds, tie-breaks, and `NO_SELECTION` rules;
21. frozen Flagship/Reasoner eligibility, thresholds, tie-breaks, resource envelope, and `NO_SELECTION` rules;
22. frozen latency/token/cost/memory/resource accounting contract;
23. reproducibility, raw-output, normalized-output, error, exclusion, report, and artifact schemas;
24. prompt/protocol digest and report-schema digest;
25. execution plan that remains non-authoritative;
26. terminal readiness verdict: `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE` or `BLOCKED`;
27. a separate inactive execution-authorization candidate only when item 26 is `READY_FOR_EXECUTION_AUTHORIZATION_CANDIDATE`.

## Six mandatory evaluation axes

The corpus/protocol freeze must cover all six:

1. medical knowledge and reasoning;
2. evidence fidelity;
3. uncertainty and abstention;
4. safety;
5. structured/FHIR readiness;
6. operational characteristics.

Omission of any axis forces `BLOCKED`.

## Candidate disposition semantics

### BLOCKED

Use when any required identity, immutable revision, tokenizer/processor revision, license/access fact, use restriction, R2 compatibility fact, security/loading requirement, architecture/context fact, or hardware/runtime feasibility fact remains unresolved, contradictory, incomplete, or unavailable.

Any `BLOCKED` non-empty candidate forces overall `BLOCKED`.

### NOT_ADMITTED

Use only when authoritative evidence conclusively proves a disqualifying policy, license/access, security, architecture, or feasibility condition.

Missing evidence may not be converted into `NOT_ADMITTED`.

### ADMITTED_FOR_EXECUTION_AUTH_CANDIDATE

Use only when all required admission evidence is proven for proposal into a later separately reviewed execution-authorization package.

This disposition grants no weight access, inference, or execution authority.

## Apertus-specific acceptance rule

The Apertus blocker is resolved only if the episode obtains a complete readable authoritative representation of the exact Apertus 1.5 terms and can bind that representation to the exact official artifact/version being relied upon.

An older Apertus policy, third-party summary, search snippet, model-generated legal summary without primary evidence, or unverified derivative copy is insufficient.

If exact terms conclusively prohibit the intended bounded R2 research use, Apertus may be `NOT_ADMITTED`. If exact terms remain ambiguous or unproven, Apertus remains `BLOCKED`.

## Refresh rule

All four non-empty candidate identities/revisions/access conditions must be refreshed during the new episode from then-current authoritative sources. Prior episode pins are historical evidence only.

No silent substitution, related checkpoint, newer release, older release, quantized derivative, or API-only replacement is allowed.

## Equal-treatment freeze

No prompt, parser, decoding, scoring, threshold, timeout, retry, or candidate accommodation may be tuned after observing candidate outputs.

Necessary architecture-specific loading accommodations may be frozen only when they preserve identical task semantics and are documented before execution.

## Stop conditions

Stop and report `BLOCKED` if:

- canonical state moves materially and cannot be reconciled within the authorization;
- the prior consumed authorization state cannot be proven;
- the exact Apertus 1.5 policy cannot be read and version-bound;
- any non-empty candidate has unresolved required evidence;
- fewer than two distinct candidates are admitted;
- any of the six axes cannot be frozen;
- R2 compatibility cannot be proven;
- hardware/runtime feasibility cannot be established without inference;
- equal-treatment or scoring requires observing model outputs;
- any required execution-candidate field remains a placeholder at the point a ready verdict would be claimed;
- scope expands toward weights, gated access, inference, training, retrieval, prohibited data, quantization changes, challenger addition, or downstream implementation.

## Post-repair authority state

Even after a successful repair episode:

```text
BACKBONE_TOURNAMENT_READINESS = COMPLETE
BACKBONE_TOURNAMENT_EXECUTION = NOT_AUTHORIZED
MODEL_WEIGHT_ACCESS = NOT_AUTHORIZED
INFERENCE = NOT_AUTHORIZED
TRAINING = NOT_AUTHORIZED
RETRIEVAL = NOT_AUTHORIZED
```

Execution may begin only after a separate exact execution authorization is reviewed, adopted, and mechanically verified under its own founder decisions.