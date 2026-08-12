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

- B0 orchestration: `src/medscale/mesc/_b0.py` — adopted at
  `ce1272235cb48dbacdb18f20e1ae8db695b01328`
- B0 CLI: `src/medscale/cli/mesc_eval.py` — adopted at
  `ce1272235cb48dbacdb18f20e1ae8db695b01328`
- B0 loader: `src/medscale/mesc/_pilot_loader.py` — adopted at
  `ce1272235cb48dbacdb18f20e1ae8db695b01328`
- B0 validation:
  `src/medscale/backends/transformers/validation.py` — APPROVED_B0_MODELS =
  frozenset({"google/medgemma-1.5-4b-it", "meta-llama/Llama-3.2-3B-Instruct"})
- B0 tests: `tests/test_mesc_b0.py`

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
