# P01-04B2B Implementation Authorization — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

Package revision:
R3 — CLEAN POST-INCIDENT RECONSTRUCTION

Canonical baseline:
06078180eb7c85da80878f3a86c5fdf3655462c5

P01-04B2B implementation authority:
RECORDED BUT INACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 0. Historical provenance

```text
PR #68:
reviewed and rejected at its exact head
a309f0789c48646e36a87181b23673551a23d74d;
CHANGES REQUIRED with two blocking findings;
never merged, never adopted; non-canonical.

PR #69:
corrected historical package
1c446def4c064b21c2cc60bc894aab3ed8e9ccff;
entered main through an unauthorized Draft merge
c8e476e42aa7c6f0e433836e278cba8940f0ea26;
never validly reviewed, never validly adopted;
neither substantively approved nor substantively rejected;
mechanically contained through PR #70.

PR #70:
validly merged and mechanically verified as
06078180eb7c85da80878f3a86c5fdf3655462c5;
restored the exact last valid canonical tree.

R3:
fresh reconstruction directly from the protected canonical main;
introduces, merges and cherry-picks no historical package commit;
inherits the preserved incident ancestry through canonical main;
requires a completely new independent review and adoption cycle.
```

Because PR #70 preserved rather than rewrote incident history, the PR #69 head
`1c446def4c064b21c2cc60bc894aab3ed8e9ccff` and the unauthorized merge
`c8e476e42aa7c6f0e433836e278cba8940f0ea26` remain reachable ancestors of
canonical `main` and therefore of every branch created from it, including r3.
`a309f0789c48646e36a87181b23673551a23d74d` is not an ancestor. That inherited
reachability is not adoption, approval, reuse, or introduction by r3, and no
criterion below may require its absence.

The two blocking findings raised against PR #68 are resolved here:

```text
BLOCKING-1:
CORRECTED — authoritative canonical score representation is a frozen string;
runtime float is derived and excluded from canonical bytes and identity.

BLOCKING-2:
CORRECTED — finding-ID payload is the accepted B2A canonical single-object JSON
serialization of an exact six-member identity document.
```

---

## 1. This documentation package

| Criterion | Requirement |
|---|---|
| Canonical baseline | Exactly `06078180eb7c85da80878f3a86c5fdf3655462c5`, tree `4208ea672a01ac942a1caeee764167d530cc8f1e` |
| Clean-reconstruction topology | Branch created directly from the canonical baseline; exactly one commit; single parent equals the canonical baseline; no historical authorization commit cherry-picked or newly merged; no historical package commit introduced by the r3 commit; all four package blobs differ from the corresponding r1 and r2 package blobs; PR #69 ancestry explicitly acknowledged as inherited through preserved canonical history and **not** required to be absent |
| Historical classification | PR #68 rejected and never adopted; PR #69 never validly reviewed or adopted and neither substantively approved nor rejected; PR #70 validly merged and mechanically verified |
| Identifiers unused canonically | `FD-B2B-1` … `FD-B2B-10` and `P01-T03B12` verified absent from canonical main before the branch was created |
| New directory | `specs/mesc-pilot-01/p01-04b2b-authorization/` did not exist on canonical main |
| Dependency DAG satisfied | The `B2B requires B2A acceptance` prerequisite recorded as satisfied, with the package stating this makes a B2B decision *eligible* rather than automatic |
| Design authority grounded | B2B recorded as the leakage primitive library with its nine adopted deliverables and its nine excluded B2C/B2D concerns |
| Ten decisions complete | `FD-B2B-1` through `FD-B2B-10` each recorded in full and mutually consistent |
| No senior conflict | Subordinate to `D1`–`D10`, `FD-B2-1`–`FD-B2-8`, `FD-B2A-1`–`FD-B2A-8` and the accepted B2A implementation, amending none |
| **No binary float in canonical form** | No canonical identity or report document carries a binary float; the runtime float is recorded as derived, runtime-only, non-authoritative, and excluded from canonical documents, canonical bytes, fingerprints and finding-ID payload bytes |
| **score_representation frozen** | Allowed values exactly `none`, `not_evaluable`, `jaccard:<i>/<u>`; reduced by GCD; unsigned base-10 ASCII; no leading zeros except the single digit `0`; denominator strictly positive; `0 <= i <= u` |
| **Golden vectors present** | `6/9 → jaccard:2/3` and `both non-empty and disjoint → jaccard:0/1` stated explicitly, together with `9/9 → jaccard:1/1`, `none` and `not_evaluable`; every `jaccard:` vector scoped to two non-empty token sets |
| **Golden-vector witness scoped** | The zero-score vector is stated with the literal witness `frozenset({"a"}), frozenset({"b"}) → intersection 0, union 2, jaccard:0/1, runtime score 0.0, neither threshold passed`, and no document instantiates it with an empty token set |
| **Consistent use** | The same authoritative representation appears in the canonical finding document and in the finding-ID payload; no statement confines the exact representation to the identity payload alone or implies the canonical document carries a float instead |
| **Exact threshold comparison** | `100 * i >= 90 * u` and `100 * i >= 95 * u`; no rounded or binary-floating-point value may decide passage |
| **Empty-input precedence pinned** | Empty-input rules stated as authoritative exceptions evaluated **before** general Jaccard fraction construction, with the controlling evaluation order (normalized-question routing → token-set empty-input rules → fraction only if both sets non-empty → integer threshold comparison) and the rule that the earlier applicable rule controls, present in `founder-authorization.md`, `implementation-contract.md`, `README.md` and this document; no conforming implementation may choose the general fraction rule over an applicable empty-input rule |
| **Union-zero semantics pinned** | `token_set_jaccard` stated total over its declared token-set domain; both-token-sets-empty pinned to `intersection_size 0`, `union_size 0`, `score_representation = not_evaluable`, runtime score `null`, no fraction constructed, neither threshold passed; `jaccard:0/0` prohibited and `jaccard:0/1` explicitly not used for this case; punctuation-only or symbol-only normalized strings that tokenize to two empty sets routed to the union-zero rule rather than `empty_normalized_question`; union zero stated to apply **only** when both token sets are empty |
| **Exactly-one-empty semantics pinned** | Pinned to `intersection_size 0`, `union_size > 0`, `score_representation = not_evaluable`, runtime score `null`, no fraction constructed, neither threshold passed; described as **policy-defined non-evaluable under senior `FD-B2-6`** rather than mathematically undefined; `jaccard:0/1` explicitly not used for this case; not classified as a union-zero case; kept distinct from the both-normalized-questions-empty rule |
| **Non-empty disjoint semantics pinned** | Two non-empty disjoint token sets pinned to `intersection_size 0`, `union_size > 0`, `score_representation = jaccard:0/1`, runtime score `0.0`, neither threshold passed; `not_evaluable` explicitly not used for this case |
| **Empty-input tests present and consistent** | Required tests present for `frozenset(), frozenset()`; punctuation-only or symbol-only inputs; `frozenset(), frozenset({"x"})` and its reversed operand order; the non-empty disjoint case `frozenset({"a"}), frozenset({"b"}) → jaccard:0/1`; and an explicit precedence test proving an exactly-one-empty input does not use the general intersection-zero / union-positive branch |
| **Test-section headings correct** | No heading classifies an exactly-one-empty input as a union-zero case; separate `Required empty-input cases` and `Required non-empty zero-similarity case` headings used |
| **Test consistency** | No required test prescribes two representations for the same input; the required prohibitions state that `jaccard:0/0` is never constructed, `jaccard:0/1` is not emitted when either token set is empty, and `not_evaluable` is not emitted for two non-empty disjoint token sets |
| **Identity document exactly six frozen members** | `schema`, `finding_type`, `example_ids`, `source_document_ids`, `partitions`, `score_representation` — no aliases, omissions, additions, or alternate container shapes; arrays lexicographically sorted before serialization; no timestamp or runtime metadata |
| **Identity-array multiplicity pinned** | `example_ids`, `source_document_ids` and `partitions` each a unique-value list; duplicates invalid and never silently removed or collapsed; unique values sorted lexicographically after type and duplicate validation and before B2A canonical serialization; a duplicate fails closed through the existing typed invalid-finding-identifier error category; input ordering non-semantic, so permutations of the same unique values yield identical canonical arrays, identical `FINDING_IDENTITY_BYTES` and identical `finding_id`; multiplicity non-semantic; no new dependency or public error surface; required permutation and duplicate-rejection tests present for all three arrays, including an explicit no-silent-deduplication test |
| **Payload bytes pinned to B2A** | `FINDING_IDENTITY_BYTES` defined as the accepted B2A canonical single-object JSON byte serialization of the identity document, including the accepted terminal LF rule and float rejection; canonical JSON not duplicated or reimplemented; manual concatenation and alternate serialization prohibited |
| **Finding-ID formula pinned** | `digest = SHA-256(FINDING_IDENTITY_BYTES).hexdigest()`; `finding_id = mesc-pilot-01-leakage-finding/1:sha256:<digest>`; exactly 64 lowercase hex characters |
| **Identity validation** | The implementation must regenerate the expected ID from validated semantic fields and fail closed on mismatch; caller-supplied IDs never trusted |
| Exact future allowlist | Exactly `src/medscale/mesc/_leakage_v1.py` and `tests/test_mesc_leakage_v1.py`, both status `A`, with the named prohibited paths and expansion forbidden |
| No implementation performed | No `_leakage_v1.py`, no `tests/test_mesc_leakage_v1.py`, no code, test, workflow, dependency, serializer, public-export or configuration change |
| Inactive authority | While unadopted: decisions issued but not adopted; authority recorded but inactive; implementation not authorized to begin |
| Valid adoption required | Five conditions, with `No subset activates P01-04B2B implementation authority.`, and an explicit statement that a merge bypassing review or the founder decisions does not adopt the package regardless of resulting Git state |
| No B2C/B2D or execution authority | No B2C, B2D, P01-04B acceptance, real split, real or canonical leakage audit, P01-03G or real-dataset access, fixture facade, CLI, filesystem publication, B0/B1, model access, inference, retrieval, metrics, benchmark execution, training, fine-tuning, publication or clinical use |
| Acceptance separation | Completing the implementation will not accept B2B, and B2C stays blocked until B2B is accepted rather than merely implemented |
| Protected-main context | Ruleset `20172239` recorded as security context only, explicitly not a substitute for governance review or founder decisions |
| Path scope | Only this package's four documents plus `specs/mesc-pilot-01/tasks.md` |
| Prior packages untouched | No previous canonical governance package modified |
| Task-ledger integrity | Historical statements preserved; the P01-04B2B task registration bounded; implementation not marked complete, started, accepted or authorized |
| Internal links | All relative links resolve |
| No unresolved markers | Every value concrete; no unresolved drafting marker, stub token, unfilled substitution slot, provisional-value token or working-directory reference |
| Exact-head verification | CI and CodeQL succeed on this package's exact head |
| Independent review | A **new** genuinely independent clean-room exact-head review of this r3 package, required before Ready |
| Ready and merge | Each a separate founder decision, after that review |

### Stop conditions

Do not treat this gate as satisfied if any document implements B2B; creates the
future implementation or test file; modifies B1 or B2A implementation, the
serializer, public exports, a CLI, workflows, dependencies or repository
settings; permits a binary float in a canonical document, in canonical bytes or
in the finding-ID payload; permits a rounded or floating-point value to decide
threshold passage; leaves the finding-ID payload bytes unpinned or defines them
by manual concatenation; leaves the union-zero token-set case without a pinned
`score_representation` or constructs `jaccard:0/0`; **permits `jaccard:0/1` when
either token set is empty**; permits `not_evaluable` for two non-empty disjoint
token sets; leaves the empty-input precedence unstated, or allows the general
fraction rule to be chosen over an applicable empty-input rule; classifies an
exactly-one-empty input as a union-zero case; instantiates the zero-score golden
vector with an empty token set; prescribes two representations for the same
input in any required test; leaves identity-array
multiplicity unpinned or permits silent deduplication; alters the six frozen
identity members; describes PR #69 as substantively approved or substantively
rejected; claims that `1c446def…` or `c8e476e4…` is absent from the ancestry of
r3 or of canonical `main`, or states any equivalent graph-reachability claim;
claims either historical commit is an adopted authority; claims the authority is
active while the package is unadopted; expands the two-path allowlist; amends `D1`–`D10`,
`FD-B2-1`–`FD-B2-8` or `FD-B2A-1`–`FD-B2A-8`; treats ruleset `20172239` as a
substitute for governance gates; rewrites or deletes a historical governance
assertion; or modifies any path outside the authorized five.

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
| Test coverage | Every §14 test group present and passing, including the canonical score-representation and finding-ID golden vectors, the §14.6 empty-input cases, the §14.6 non-empty zero-similarity and precedence cases, and the §14.2 identity-array permutation and duplicate-rejection cases |
| Independent review | A genuinely independent clean-room exact-head implementation review |
| Ready and merge | Separate founder decisions |
| Acceptance | A later, separate B2B implementation-acceptance decision |

Meeting every row still does not accept B2B, authorize B2C or B2D, complete
P01-04B, or authorize any execution.

---

## 3. Standing prohibition

At no point does this package permit B2B implementation before valid adoption,
execution against real data, the real Pilot-01 split, a real or canonical
leakage audit, B0 or B1, benchmark execution, model training or fine-tuning,
P01-03G or dataset access, model access, inference, retrieval, publication, or
clinical use.
