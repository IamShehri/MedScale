# P01-04B2C Implementation Authorization — Acceptance Criteria

```text
Status:
DOCUMENTATION GATE — NOT ADOPTED

FD-B2C-1 through FD-B2C-12:
FOUNDER DECISIONS ISSUED —
NOT YET ADOPTED ON CANONICAL MAIN

P01-04B2C implementation authority:
RECORDED BUT INACTIVE
```

Two layers. Satisfying the first never satisfies the second.

---

## 1. This authorization-package gate

| Criterion | Requirement |
|---|---|
| Exact baseline | Branch created from exactly `3c4d7f153522128533fa9aba26209426b248b4f1`, tree `e548aab1342c8783c1b919e707e5036a18e4a80a`, ordered parents `d91f76e7...` then `a7b25f17...`, subject `Merge pull request #73 from IamShehri/docs/mesc-p01-04b2b-acceptance`; `origin/main` equal to that SHA; no rebase onto a later `main` |
| Exact five-path scope | Exactly `specs/mesc-pilot-01/p01-04b2c-authorization/README.md`, `acceptance.md`, `founder-authorization.md` and `implementation-contract.md` added, plus `specs/mesc-pilot-01/tasks.md` modified. No sixth path |
| One commit | Exactly one local commit with subject `docs(mesc): authorize P01-04B2C implementation`; no amend, rebase, squash, reset, cherry-pick, merge or force-push |
| Documentation only | No change to `src/**`, `tests/**`, `.github/**`, `docs/**`, `pyproject.toml`, `uv.lock`, serializers, exports, CLI files, configuration, dependencies, datasets, models or artifacts; no prior governance package modified |
| Unused identifiers | `FD-B2C-1` through `FD-B2C-12`, `P01-T03B14` and `specs/mesc-pilot-01/p01-04b2c-authorization/` verified unused on canonical `main` before creation |
| Complete FD-B2C-1 through FD-B2C-12 | All twelve decisions present, each with its exact subject, scope and prohibitions; the decision stated as `AUTHORIZE P01-04B2C IMPLEMENTATION SUBJECT TO VALID CANONICAL ADOPTION OF THIS PACKAGE` |
| No contradiction with prior authorities | Nothing contradicts P01-04A D1–D10, FD-B2-1..8, FD-B2A-1..8, FD-B2A-9, FD-B2B-1..10, FD-B2B-11, or the accepted B2A and B2B implementations; the subordination clause states that a senior authority controls on conflict |
| Request payload ambiguity resolved | `FixtureSplitRequest` carries all seventeen named fields with exact contracts; payload ownership is identity-only; caller-owned collections are snapshotted and unreachable after construction; `bool` never satisfies an `int` requirement |
| Result byte-surface ambiguity resolved | All six byte surfaces named and specified; the four B2A descriptor roles distinguished from the two B2C-level surfaces; `split_summary_identity_core/1` distinguished from the final `split-summary/1`; the non-circular construction order stated |
| Structural proof described honestly | The package states that structural fixture proof establishes internal identity consistency and is not a cryptographic or real-world provenance oracle, and that flags alone cannot detect a malicious caller repackaging real data |
| Exact two-path future allowlist | `src/medscale/mesc/_fixture_split_v1.py` and `tests/test_mesc_fixture_split_v1.py`, with the instruction to stop and return for a new authorization rather than expand |
| No unresolved latitude | No "implementation may choose" language for any identity-bearing or fingerprint-bearing value |
| Ledger integrity | `tasks.md` gains `P01-T03B14`; `P01-T03B12` and `P01-T03B13` are neither rewritten nor deleted; prior controlling-state snapshots preserved with their original time-relative truth and superseded only additively; exactly one unannotated live `Current controlling state` block remains |
| Internal links | All relative links resolve |
| No placeholders | Every value concrete; no unresolved drafting marker, stub token, unfilled substitution slot, provisional value or working-directory path anywhere in the package |
| Independent review | A genuinely independent clean-room exact-head review of **this package**, required before Ready |
| Separate Ready decision | A distinct founder decision taken after that review |
| Separate merge decision | A distinct founder decision taken after Ready |
| Mechanical post-merge verification | Performed after merge; activation is not achieved without it |
| No B2D or execution authority | Nothing in the package authorizes P01-04B2D, P01-04C–G, orchestration, dataset scanning, record-pair discovery, real execution, or any downstream phase |

### Stop conditions

Do not treat this gate as satisfied if any document authorizes P01-04B2D or its
three 1,000-row fixtures; accepts P01-04B as a whole; accepts the future B2C
implementation in advance; authorizes orchestration, dataset scanning,
record-pair discovery, a real or canonical leakage audit, real split
generation, B0 or B1 execution, dataset or model access, inference, retrieval,
metrics, benchmark execution, training or fine-tuning; expands the two-path
future allowlist; authorizes modification of an accepted B1, B2A or B2B module;
dispatches, reruns or cancels a workflow; claims `FD-B2C-1` through `FD-B2C-12`
are adopted while this package is local, Draft or unmerged; claims the
implementation authority is active before all five activation conditions pass;
claims the declared fixture flags prove real-world provenance; rewrites or
deletes a historical governance assertion; modifies any prior governance
package; leaves two blocks simultaneously claiming to be the current
controlling state; or modifies any path outside the authorized five.

Updating `specs/mesc-pilot-01/tasks.md` to record this gate is expected and is
not a stop condition.

---

## 2. The later B2C implementation gate

This package does **not** accept a future implementation. When the authority is
active and an implementation exists, its acceptance requires all of:

| Criterion | Requirement |
|---|---|
| Exact two implementation paths | `A src/medscale/mesc/_fixture_split_v1.py` and `A tests/test_mesc_fixture_split_v1.py`, and nothing else |
| No accepted-module modification | `__init__.py`, `split.py`, `_split_v1.py`, `_canonical_json_v1.py`, `_split_artifacts_v1.py` and `_leakage_v1.py` unchanged |
| Contract conformance | Criterion-by-criterion conformance to `implementation-contract.md` §§1–16 |
| All required tests | The complete §15 matrix — request boundary, deterministic integration, compatibility manifest, canonical artifacts with literal golden vectors, leakage integration, side-effect boundary and scope proof |
| Exact-head CI | CI and CodeQL green at the exact reviewed head, covering locked dependency sync, Ruff lint, Ruff format, Mypy strict, Pytest and `medscale check` |
| Independent review | A genuinely independent clean-room exact-head review of the implementation, with no blocking finding |
| Separate Ready decision | A distinct founder decision |
| Separate merge decision | A distinct founder decision |
| Post-merge mechanical verification | Performed after merge |
| Separate acceptance disposition | A distinct founder implementation-acceptance disposition, itself canonically adopted through its own five-condition gate |

Satisfying this package's gate authorizes the implementation to begin once
activated. It never accepts the implementation that results.

---

## 3. The later decisions this package does not make

| Decision | State |
|---|---|
| Canonical adoption of `FD-B2C-1` through `FD-B2C-12` | Requires the five activation conditions |
| Acceptance of the future B2C implementation | **NOT GRANTED** — a separate later disposition |
| P01-04B2D authorization | **NOT AUTHORIZED** |
| B2D fixture qualification (`exact-reference-1000-v1`, `constraint-stress-1000-v1`, `leakage-positive-v1`) | **NOT AUTHORIZED** |
| P01-04C through P01-04G | **NOT AUTHORIZED** |
| P01-04B whole-phase acceptance | **NOT ACHIEVED** |
| Leakage-audit orchestration, dataset scanning, record-pair discovery | **NOT AUTHORIZED** |
| Real split generation, real or canonical leakage audit | **NOT AUTHORIZED** |
| CLI, filesystem publication, public export | **NOT AUTHORIZED** |
| Model access, real dataset access, P01-03G | **NOT AUTHORIZED** |
| B0/B1 execution, inference, retrieval, metrics, benchmark execution | **NOT AUTHORIZED** |
| Training, fine-tuning | **NOT AUTHORIZED** |
| Publication, clinical use | **NOT AUTHORIZED** |

---

## 4. Standing prohibition

At no point does this package permit execution against real data, real split
generation, a real or canonical leakage audit, B0 or B1 execution, benchmark
execution, model training or fine-tuning, P01-03G or dataset access, model
access, inference, retrieval, publication, or clinical use.
