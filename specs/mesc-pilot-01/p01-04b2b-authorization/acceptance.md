# P01-04B2B Implementation Authorization — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

Package revision:
CORRECTED REPLACEMENT — supersedes unmerged Draft PR #68

P01-04B2B implementation authority:
RECORDED BUT INACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 0. Findings disposition from the PR #68 review

```text
BLOCKING-1:
CORRECTED — authoritative canonical score representation is a frozen string;
runtime float is derived and excluded from canonical bytes and identity.

BLOCKING-2:
CORRECTED — finding-ID payload is the accepted B2A canonical single-object JSON
serialization of an exact six-member identity document.

NB-1:
ACCEPTED AS NON-BLOCKING — Windows WSL/bash review-host limitation.

NB-2:
INCORPORATED — explicit reduced-rational golden-vector requirement.

NB-3:
ACCEPTED AS NON-BLOCKING — expected duplicate-name warning in a negative ZIP
test.
```

PR #68 was **not** approved. Its head
`a309f0789c48646e36a87181b23673551a23d74d` was rejected by independent
exact-head review, is non-canonical, and was never adopted. This replacement
requires a **new** genuinely independent exact-head review.

---

## 1. This documentation package

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `bfc4254b6a028ea7ec5969b505d73e7d66751272`, tree `4208ea672a01ac942a1caeee764167d530cc8f1e`, ordered parents `1f2d9152...` then `c59e4e16...`, subject `docs(mesc): record P01-04B2A acceptance (#67)` |
| Replacement topology | Branched directly from canonical main; exactly one commit whose single parent is `bfc4254b...`; the rejected commit is neither cherry-picked nor an ancestor |
| PR #68 not adopted | Recorded as rejected, non-canonical and never adopted; not recorded as approved; its branch unmodified |
| B2A state recorded | `FD-B2A-9` adopted at `bfc4254b...`; P01-04B2A accepted; `N-12` discharged; Windows and macOS obligations closed — all scoped to P01-04B2A |
| Identifiers unused | `FD-B2B-1` … `FD-B2B-10` and `P01-T03B12` verified absent from canonical main before mutation |
| New directory | `specs/mesc-pilot-01/p01-04b2b-authorization/` did not exist on canonical main |
| Dependency DAG satisfied | The `B2B requires B2A acceptance` prerequisite recorded as satisfied, with the package stating this makes a B2B decision *eligible* rather than automatic |
| Design authority grounded | B2B recorded as the leakage primitive library with its nine adopted deliverables and its nine excluded B2C/B2D concerns |
| Ten decisions complete | `FD-B2B-1` through `FD-B2B-10` each recorded in full and mutually consistent |
| No senior conflict | Subordinate to `D1`–`D10`, `FD-B2-1`–`FD-B2-8`, `FD-B2A-1`–`FD-B2A-8` and the accepted B2A implementation, amending none; conforms to the accepted canonical value domain rather than extending it |
| **No binary float in canonical form** | No canonical identity or report document carries a binary float; the runtime float is recorded as derived, runtime-only, non-authoritative, and excluded from canonical documents, canonical bytes, fingerprints and finding-ID payload bytes |
| **score_representation frozen** | Allowed values exactly `none`, `not_evaluable`, `jaccard:<i>/<u>`; reduced by GCD; unsigned base-10 ASCII; no leading zeros except the single digit `0`; denominator strictly positive; `0 <= i <= u`; `jaccard:0/1` and `jaccard:1/1` pinned |
| **Consistent use** | The same authoritative representation appears in the canonical finding document and in the finding-ID payload; no statement anywhere in the package confines the exact representation to the identity payload alone or implies the canonical document carries a float instead |
| **Exact threshold comparison** | Threshold passage defined by `100 * i >= 90 * u` and `100 * i >= 95 * u`; no rounded or binary-floating-point value may decide passage |
| **Identity document exactly six frozen members** | `schema`, `finding_type`, `example_ids`, `source_document_ids`, `partitions`, `score_representation` — no aliases, no omissions, no additions, no alternate container shapes; arrays lexicographically sorted before serialization |
| **Payload bytes pinned to B2A** | `FINDING_IDENTITY_BYTES` defined as the accepted B2A canonical single-object JSON byte serialization of the identity document, including domain validation, member ordering, UTF-8 encoding, escaping, single-object framing, the terminal-line-feed rule, and float rejection; canonical JSON is not duplicated or reimplemented |
| **Finding-ID formula pinned** | `digest = SHA-256(FINDING_IDENTITY_BYTES).hexdigest()`; `finding_id = mesc-pilot-01-leakage-finding/1:sha256:<digest>`; exactly 64 lowercase hex characters; no other prefix, separator, concatenation, newline convention, JSON shape or serialization |
| **Identity validation** | The implementation must regenerate the expected ID from validated semantic fields and fail closed on mismatch with the typed invalid-finding-identifier error; caller-supplied IDs are never trusted |
| **Correction tests recorded** | The `6/9 → jaccard:2/3`, `0/9 → jaccard:0/1`, `9/9 → jaccard:1/1`, `none` and `not_evaluable` cases, the five float-exclusion verifications, and the four literal golden-vector artifacts with their six verification requirements |
| Preserved boundaries | `FD-B2B-1`, `-2`, `-3`, `-4`, `-7`, `-8`, `-9`, `-10` preserved in substance, together with the private-module boundary, two-path allowlist, strict input domain, exact equality rules, NFKC/casefold/whitespace/tokenization rules, suppression prohibition, fail-closed `leaked` rule, raw-text boundary, deterministic errors, side-effect prohibitions, five activation conditions, and B2C/B2D and downstream non-authority |
| Exact future allowlist | Exactly `src/medscale/mesc/_leakage_v1.py` and `tests/test_mesc_leakage_v1.py`, both status `A`, with the named prohibited paths and expansion forbidden |
| No implementation performed | No `_leakage_v1.py`, no `tests/test_mesc_leakage_v1.py`, no code, test, workflow, dependency, serializer, public-export or configuration change |
| Inactive authority | While Draft or unmerged: decisions issued but not adopted; authority recorded but inactive; implementation not authorized to begin |
| Activation conditions | All five stated, with `No subset activates P01-04B2B implementation authority.` |
| No B2C/B2D or execution authority | No B2C, B2D, P01-04B acceptance, real split, P01-03G or real-dataset access, real leakage-audit execution, fixture facade, CLI, filesystem publication, B0/B1, model access, inference, retrieval, metrics, benchmark execution, training, fine-tuning, publication or clinical use |
| Acceptance separation | Completing the implementation will not accept B2B, and B2C stays blocked until B2B is accepted rather than merely implemented |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| Prior packages untouched | No previous canonical governance package modified |
| Task-ledger integrity | Every historical canonical statement preserved; exactly one `P01-T03B12` entry; PR #68 not recorded as adopted or canonical; the previous live block annotated as a superseded historical snapshot; exactly one unannotated live `Current controlling state` block remains |
| Terminology | The governed concepts kept distinct; none substituted for another |
| Internal links | All relative links resolve |
| No unresolved markers | Every value concrete; no unresolved drafting marker, stub token, unfilled substitution slot, provisional-value token or working-directory reference |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review | A **new** genuinely independent clean-room exact-head review of this replacement, required before Ready |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document implements B2B; creates the
future implementation or test file; modifies B1 or B2A implementation, the
serializer, public exports, a CLI, workflows, dependencies or repository
settings; permits a binary float in a canonical document, in canonical bytes or
in the finding-ID payload; permits a rounded or floating-point value to decide
threshold passage; leaves the finding-ID payload bytes unpinned or defines them
by manual concatenation; alters the six frozen identity members; claims PR #68
was approved; claims the authority is active while the pull request is Draft or
unmerged; expands the two-path allowlist; amends `D1`–`D10`,
`FD-B2-1`–`FD-B2-8` or `FD-B2A-1`–`FD-B2A-8`; rewrites or deletes a historical
governance assertion; leaves two blocks simultaneously claiming to be the
current controlling state; or modifies any path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later B2B implementation gate

Not satisfied by this package. Defined in
[`implementation-contract.md`](implementation-contract.md) §14 and reachable
only after all five activation conditions pass.

| Criterion | Requirement |
|---|---|
| Activation | All five conditions satisfied and mechanically verified |
| Path scope | Exactly the two allowlisted paths, both added |
| Contract conformance | Every §1–§13 requirement of the implementation contract satisfied |
| Test coverage | Every §14 test group present and passing, including the canonical score-representation and finding-ID golden vectors |
| Independent review | A genuinely independent clean-room exact-head implementation review |
| Ready and merge | Separate founder decisions |
| Acceptance | A later, separate B2B implementation-acceptance decision |

Meeting every row still does not accept B2B, authorize B2C or B2D, complete
P01-04B, or authorize any execution.

---

## 3. Standing prohibition

At no point does this package permit B2B implementation before adoption,
execution against real data, the real Pilot-01 split, a real leakage audit, B0
or B1, benchmark execution, model training or fine-tuning, P01-03G or dataset
access, model access, inference, retrieval, publication, or clinical use.
