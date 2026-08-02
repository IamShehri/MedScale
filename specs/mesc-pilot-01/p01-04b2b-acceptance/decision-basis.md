# P01-04B2B Acceptance — Decision Basis

```text
Status:
IMMUTABLE EVIDENCE LEDGER

FD-B2B-11:
FOUNDER DECISION ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN
```

This is the evidence record supporting
[`founder-disposition.md`](founder-disposition.md), which controls on any
conflict. It duplicates no raw implementation or test file; the accepted
sources are identified by path and blob only.

---

## 1. Authorization identity

```text
Authorization package:
PR #71 — MERGED / CLOSED / NOT DRAFT
canonical merge  aeff056cb02fc9f72d2d861cadb84622c5558032
merge tree       c265f6ec84de8b7bfcc56b5b569e52ac08ef9a91
merged head      3aa452092a269ab7d62d807bce2339dda8a9533e
merged           2026-08-01T23:45:40Z
5 files / +2197 / -0

Adopted content:
FD-B2B-1 through FD-B2B-10 and the r3 implementation contract at
../p01-04b2b-authorization/implementation-contract.md

Package revision:
R3 — CLEAN POST-INCIDENT RECONSTRUCTION
```

The authorization was adopted on canonical `main` **before** the implementation
commit was authored, satisfying the FD-B2B-10 activation sequencing.

## 2. Implementation commit, tree and parent

```text
Implementation commit:
86cfdca1797cf1be60761284af1cc81e25047f41

Tree:
070b177194094e5ae55d34570a86997fde956302

Parent:
aeff056cb02fc9f72d2d861cadb84622c5558032

Subject:
feat(mesc): implement P01-04B2B leakage primitives

Authored / committed:
2026-08-02T00:12:32Z

Commit count above the implementation base:
1
```

The single parent is exactly the authorization merge. The implementation
introduces no merge, cherry-pick or unrelated ancestry.

## 3. PR and merge identity

```text
Implementation PR:
#72 — MERGED / CLOSED / NOT DRAFT
head ref     feat/mesc-p01-04b2b-leakage-primitives
head oid     86cfdca1797cf1be60761284af1cc81e25047f41
base ref     main
merged       2026-08-02T00:57:57Z

Canonical implementation merge:
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863

Merge tree:
070b177194094e5ae55d34570a86997fde956302

Ordered parent 1:
aeff056cb02fc9f72d2d861cadb84622c5558032

Ordered parent 2:
86cfdca1797cf1be60761284af1cc81e25047f41

Merge subject:
Merge pull request #72 from IamShehri/feat/mesc-p01-04b2b-leakage-primitives
feat(mesc): implement P01-04B2B leakage primitives
```

The merge tree is **identical** to the reviewed implementation tree. The merge
introduced no content beyond the reviewed head.

## 4. Path and blob identity

```text
A src/medscale/mesc/_leakage_v1.py
  blob 61f2bf4dff7e71f0a7f2be21b425ba8686badf16
  964 lines / +964

A tests/test_mesc_leakage_v1.py
  blob a7a77ceee84206c5bfb64b07e64083bb4b0af660
  1296 lines / +1296
```

Both blobs are present on canonical `main` at
`d91f76e77c4753e556b2ca9c2ee1bfcd5923d863` at exactly these paths. No third
path was added, modified, renamed or deleted.

## 5. Diff statistics

```text
Implementation delta  aeff056..86cfdca
2 files changed, 2260 insertions(+), 0 deletions(-)
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py

Canonical delta       aeff056..d91f76e
2 files changed, 2260 insertions(+), 0 deletions(-)
A src/medscale/mesc/_leakage_v1.py
A tests/test_mesc_leakage_v1.py

Reviewed-head-to-merge delta  86cfdca..d91f76e
0 files changed
```

The implementation delta and the canonical delta are identical in path set,
status set and statistics. `964 + 1296 = 2260` reconciles the per-path line
counts with the reported additions.

## 6. Independent review evidence

```text
Independent implementation review:
APPROVE WITH NON-BLOCKING NOTES

Independence:
SATISFIED

Blocking findings:
NONE

Reviewed head:
86cfdca1797cf1be60761284af1cc81e25047f41

Reviewed tree:
070b177194094e5ae55d34570a86997fde956302
```

The review was performed at the exact head that was subsequently merged. No
commit was added after the review, so no review carry-over question arises.

Six non-blocking observations were returned — `NB-1` through `NB-6`. Their
verbatim substance and accepted dispositions are recorded in
[`founder-disposition.md`](founder-disposition.md) §5. None is a blocking
finding, none was corrected, and none is a deferred obligation.

## 7. CI and CodeQL evidence — exact head

All checks below are bound to head `86cfdca1797cf1be60761284af1cc81e25047f41`.

```text
CI
run            30725954034
event          pull_request
run_attempt    1
status         completed
conclusion     success
head_sha       86cfdca1797cf1be60761284af1cc81e25047f41
head_branch    feat/mesc-p01-04b2b-leakage-primitives

  quality (py3.11)   completed / success
  quality (py3.12)   completed / success

CodeQL
run            30725954031
event          pull_request
run_attempt    1
status         completed
conclusion     success
head_sha       86cfdca1797cf1be60761284af1cc81e25047f41
head_branch    feat/mesc-p01-04b2b-leakage-primitives

  analyze (python)   completed / success
```

Both `quality` jobs passed the full canonical gate:

```text
locked dependency sync
Ruff lint
Ruff format
Mypy strict
Pytest
medscale check
```

```text
Reruns, retries, replacement workflows, manual dispatches:
NONE — run_attempt is 1 for both runs
```

No separate post-merge CI workflow is claimed to have run. The recorded checks
are `pull_request` checks on the exact reviewed head. Any post-merge workflow
claim would require new evidence and is not asserted here.

## 8. Ready transition evidence

```text
Ready decision:
SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED

PR #72 draft state at merge:
NOT DRAFT
```

The Ready transition was a distinct founder decision taken after the
independent exact-head review and before the merge decision. It was not
combined with, implied by, or substituted for either.

## 9. Merge evidence

```text
Merge decision:
SEPARATELY FOUNDER-AUTHORIZED AND EXECUTED

Merged at:
2026-08-02T00:57:57Z

Merged from:
86cfdca1797cf1be60761284af1cc81e25047f41 — the exact reviewed head

Resulting canonical main:
d91f76e77c4753e556b2ca9c2ee1bfcd5923d863

Source branch after merge:
refs/heads/feat/mesc-p01-04b2b-leakage-primitives
RETAINED AT 86cfdca1797cf1be60761284af1cc81e25047f41 — NOT DELETED
```

## 10. Post-merge mechanical verification

The five mechanical criteria, each independently checked:

| # | Criterion | Result |
|---|---|---|
| 1 | PR #72 merged from the exact reviewed head `86cfdca1...` | PASS |
| 2 | Canonical `main` equals `d91f76e77c4753e556b2ca9c2ee1bfcd5923d863` | PASS |
| 3 | Both reviewed blobs present on `main` at their exact paths | PASS |
| 4 | Canonical delta contains only the two accepted paths | PASS |
| 5 | Source branch not deleted during the merge task | PASS |

```text
Mechanical post-merge verification:
PASSED
```

This is the complete definition of mechanical post-merge verification for this
increment. It asserts nothing about workflow runs beyond §7.

## 11. Criterion-by-criterion mapping to the adopted implementation contract

Mapping of the accepted implementation at tree
`070b177194094e5ae55d34570a86997fde956302` against
[`../p01-04b2b-authorization/implementation-contract.md`](../p01-04b2b-authorization/implementation-contract.md)
§§1–15, as established by the independent exact-head review.

| § | Requirement | Conformance basis | Result |
|---|---|---|---|
| 1 | Exact primitive definitions; pure, pairwise, total; exact built-in input domain; `bool` never satisfies `int`; exact and normalized equality kept separate | All eight primitives present with the contracted signatures and results; exact type validation rejects subclasses and coerces nothing; exact-equality primitives perform no normalization | CONFORMS |
| 2 | NFKC → case folding → Unicode whitespace collapse to one ASCII space → trim; tokens are maximal Unicode alphanumeric runs; set not multiset; punctuation retained through normalization and a boundary at tokenization | Normalization applies the four steps in the contracted order; tokenization accumulates maximal alphanumeric runs into a `frozenset`; no stemming, stop-word removal, transliteration or locale dependence | CONFORMS — see `NB-6` |
| 3 | Threshold passage by exact integer comparison `100 * i >= 90 * u` and `100 * i >= 95 * u`; equality at threshold matches; no float may decide passage | Threshold passage is computed from the integer counts against integer percent constants; no float participates | CONFORMS — see `NB-2` |
| 4 | `token_set_jaccard` total; empty-input rules are authoritative exceptions evaluated before fraction construction; both-empty and exactly-one-empty yield `not_evaluable` with null runtime score; `jaccard:0/0` prohibited; `jaccard:0/1` never emitted when either set is empty; `empty_normalized_question` distinct from the token-set rules | Empty-input routing precedes fraction construction; both-empty and exactly-one-empty (in both operand orders) yield `not_evaluable`; no fraction is constructed when either set is empty; the punctuation-only case routes to the union-zero rule, not to `empty_normalized_question` | CONFORMS |
| 5 | Exactly one authoritative `score_representation`; allowed values `none`, `not_evaluable`, reduced `jaccard:<i>/<u>`; unsigned base-10 ASCII, no leading zeros, positive denominator, `0 <= i <= u`; runtime float derived, non-authoritative, excluded from canonical documents, bytes, fingerprints and identity payload; no float reaches the B2A serializer | Representation is constructed as a frozen string reduced by GCD with the contracted lexical form and validated on ingestion; the runtime float is derived from the integer counts, excluded from every canonical surface, and cannot alter canonical bytes | CONFORMS |
| 6 | Finding-ID identity document of exactly six frozen members; `FINDING_IDENTITY_BYTES` from the accepted B2A canonical single-object serialization including the terminal LF; `sha256` formula and 64-hex prefix form; caller IDs regenerated and compared; findings ordered by ascending `finding_id`; identity arrays are unique-value lists with duplicates failing closed and never silently deduplicated | The identity document carries exactly the six contracted members; bytes come from the imported B2A `canonical_json_bytes` with `sha256_of_bytes` — canonical JSON is reused, never reimplemented or hand-concatenated; supplied IDs are regenerated and compared; duplicates raise the typed invalid-finding-identifier error; arrays are sorted after validation so permutation is non-semantic; report findings sort by ID | CONFORMS — see `NB-1`, `NB-4` |
| 7 | Exactly three classifications; every finding carries one; `false_positive` requires a non-empty stable supporting-evidence reference | Classification validated against the closed three-value domain; `false_positive` without a reference fails closed | CONFORMS — see `NB-3` |
| 8 | `suppressed` always false; suppression, dropping, omitting and filtering are fail-closed; `finding_count` exact; a leakage-positive fixture cannot yield a vacuous report | `suppressed` accepts only exact `False`; any true value raises the typed suppression error; count derives from the findings tuple | CONFORMS |
| 9 | `leaked = true` when any finding is `unresolved` or `confirmed_leakage`; `leaked = false` only when there are no findings or every finding is a supported false positive | Aggregate `leaked` derived fail-closed from the classifications | CONFORMS |
| 10 | Raw text transient only; never stored in a finding, canonical bytes, logs, exceptions, repr, reports, manifests, fingerprints, evidence references or artifacts; `shared_surface` limited to the eight allowlisted markers | No raw question, context or answer text is retained; `shared_surface` accepts only the eight allowlisted markers and rejects anything else as raw surface text; error messages carry no raw input | CONFORMS |
| 11 | Typed private errors for the nine categories with stable machine-readable codes; deterministic validation order; no raw text or runtime metadata in messages; no file, network, subprocess, logging, telemetry, cache or global-state side effect; no new dependency | Nine typed error classes descend from a private base, each with a stable code; validation order is fixed; the module imports only the standard library plus already-accepted MESC internals | CONFORMS |
| 12 | Allowed contents only — immutable finding and report, equality primitives, normalization, tokenization, integer Jaccard, score representation, finding-ID generation, strict validation, canonical generation **through the accepted B2A serializer**, and synthetic tests | Contents match the allowlist; both dataclasses are frozen and slotted; canonical bytes are produced by the imported B2A helpers rather than a fork | CONFORMS — see `NB-5` |
| 13 | No record-pair enumeration, dataset or registry scanning, orchestration, automatic finding discovery, fixture facade, split facade, CLI, filesystem publication, path safety, concurrency, real execution or integrated qualification | No production function accepts a record collection or searches it; no facade, CLI, filesystem or concurrency surface exists; findings are constructed explicitly by synthetic tests only | CONFORMS |
| 14 | Required tests §§14.1–14.9 — canonical score representation, finding-ID payload golden vectors and multiplicity, type and validation, exact equality, normalization, tokenization and Jaccard including both threshold boundaries and every empty-input case, findings, classification and report, determinism | The committed synthetic suite covers each required case, including the literal `frozenset({"a"}), frozenset({"b"}) -> jaccard:0/1` zero-score vector, both operand orders of the exactly-one-empty case, the precedence case, permutation and duplicate-rejection cases, and the golden finding-ID vector; all passed on the exact head under both Python 3.11 and 3.12 | CONFORMS — see `NB-2` |
| 15 | Exactly two paths: `A src/medscale/mesc/_leakage_v1.py`, `A tests/test_mesc_leakage_v1.py`; allowlist must not be expanded | The canonical delta adds exactly those two paths and nothing else | CONFORMS |

```text
Sections conforming:  15 of 15
Blocking findings:    NONE
```

The six accepted observations are attached to §§2, 3, 6, 7, 12 and 14 above.
Each is non-blocking, none was corrected, and none alters the conformance
result of its section.

## 12. Ledger integrity

This ledger records only what was mechanically observed or independently
reviewed at the identities named above. It contains no forward-looking claim,
no authorization, and no assertion that `FD-B2B-11` is canonical.
