# MESC Pilot-01 — P01-05 Acceptance

Status: **entry contract acceptance criteria**

Authorization: Entry *** defined — real execution not authorized

---

## Acceptance criteria

P01-05 entry documentation passes when:

1. P01-05 purpose and boundaries are unambiguous.
2. Existing B0 implementation truth is reconciled rather than duplicated.
3. B0 vs B1 evidence semantics are explicit.
4. B1 evidence source is either canonically identified or explicitly BLOCKED.
5. No retrieval is smuggled into B1.
6. Current model restrictions are canonically reconciled.
7. Chinese model entries remain historical only and are not execution-authorized.
8. MESC vNext compatibility is documented without implementation.
9. Real model execution remains unauthorized.
10. Exact implementation delta is recorded.
11. No P01-06 or later phase is authorized.
12. No source/test/script code changes occur.

---

## Verification checklist

- [ ] `specs/mesc-pilot-01/p01-05/` package present with all seven documents
- [ ] B0 definition reconciled with existing implementation
- [ ] B1 definition explicit and bounded
- [ ] B1 evidence source status explicitly recorded
- [ ] Model authority supersession present without erasing historical records
- [ ] Implementation delta table present and accurate
- [ ] No implementation source files added
- [ ] No tests changed
- [ ] No scripts changed
- [ ] P01-06 not authorized
- [ ] vNext Stage 1 implementation not authorized

---

## Blocking findings

If any of the following are true, the entry contract is not accepted:

- B1 evidence source is fabricated
- Retrieval is smuggled into B1 definition
- Model authority reconciliation erases historical records instead of superseding them
- Real execution is authorized
- P01-06 or later phase is authorized
- Any source, test, or script code is changed

---

## Current acceptance status

**P01-05 entry contract: CANONICALLY DEFINED**

The entry contract is defined by the seven documents in
`specs/mesc-pilot-01/p01-05/`. The B0 implementation identity is reconciled
against the existing adopted code rather than duplicated.

**Existing B0 implementation blob identities (reconciled):**

| surface | repository_path | current_blob_sha | historical_adoption_commit | status |
|---|---|---|---|---|
| B0 orchestration | `src/medscale/mesc/_b0.py` | `27c36f7fad8224c89ab8403b7abb94482d8cbbf2` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| B0 CLI | `src/medscale/cli/mesc_eval.py` | `84cff1a093f0daff30f4b7f7f58eb718513bff0e` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| B0 loader | `src/medscale/mesc/_pilot_loader.py` | `05ad43a4aa4be778de52ab2fafc283d41956d755` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| B0 validation | `src/medscale/backends/transformers/validation.py` | `74e421cbb42d348eca6183a6b208090f8139d971` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| B0 backend | `src/medscale/backends/transformers/backend.py` | `d4097fb1943ed41a9deacd0d6b09f1a6cc3cb127` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| B0 tests | `tests/test_mesc_b0.py` | `84ab4270228a662e4e1d7900ebfd34fc577bb4f8` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |
| CLI verification tests | `tests/test_cli_ux.py` | `2aa3b344457ab124a7c0e15af30f8c219d8003a5` | `ce1272235cb48dbacdb18f20e1ae8db695b01328` | RECONCILED |

Historical adoption commit `ce1272235cb48dbacdb18f20e1ae8db695b01328` is retained as provenance only. Current blob identities above are actual `HEAD` Git blob identities verified with both `git rev-parse 'HEAD:<path>'` and `git ls-tree HEAD -- <path>`.

**Verification checklist status:**

- [x] `specs/mesc-pilot-01/p01-05/` package present with all seven documents
- [x] B0 definition reconciled with existing implementation
- [x] B1 definition explicit and bounded
- [x] B1 evidence source status explicitly recorded (UNRESOLVED)
- [x] Model authority supersession present without erasing historical records
- [x] Implementation delta table present and accurate
- [x] No implementation source files added
- [x] No tests changed
- [x] No scripts changed
- [x] P01-06 not authorized
- [x] vNext Stage 1 implementation not authorized

Blocking findings: NONE

B1 evidence source: UNRESOLVED

B1 implementation: BLOCKED PENDING EVIDENCE-SOURCE RATIFICATION

B0 execution: NOT AUTHORIZED

B1 execution: NOT AUTHORIZED
