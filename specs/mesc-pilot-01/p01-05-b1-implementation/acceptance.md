# P01-05 B1 Evidence-Cued Baseline and Development-Evidence-Pack Tooling — Acceptance

Status: **implementation acceptance criteria**

Authorization: FD-P01-05-B1-EVIDENCE-1 — implementation and synthetic/fixture
validation only

---

## Acceptance criteria

Implementation acceptance requires:

1. B0 scientific semantics unchanged — PASS
2. B1 evidence-cue contract implemented exactly — PASS
3. deterministic segment reference/hash validation — PASS
4. deterministic subset-selection tooling implemented — PASS
5. label-blind annotation view implemented — PASS
6. A/B comparison and human-adjudication requirement implemented — PASS
7. final cue builder fails closed — PASS
8. evidence-pack validator implemented — PASS
9. B1 prompt adds only the ratified evidence-cue channel — PASS
10. gold-decision isolation proven — PASS
11. B1 runner deterministic with fake generator — PASS
12. B1 run identity binds evidence-pack/subset identity — PASS
13. no retrieval path exists — PASS
14. no raw scientific text persisted in canonical pack artifacts — PASS
15. no real validation evidence pack produced — PASS
16. test partition untouched — PASS
17. no model execution/download/network access performed — PASS
18. B0 and full regression tests pass — PASS
19. no P01-06 authority introduced — PASS
20. no vNext Stage 1 implementation introduced — PASS

---

## Verification checklist

- [x] B0 files byte-identical pre/post implementation (blob hashes recorded in
      `implementation-record.md`)
- [x] B1 evidence domain implemented as additive private module
  (`src/medscale/mesc/_b1_evidence.py`)
- [x] B1 runner implemented as additive private module
  (`src/medscale/mesc/_b1.py`), reusing B0 parse states, scoring, aggregation,
  prompt hashing, and run-digest discipline
- [x] Evidence-cue contract versioned as `mesc-pilot-01-b1-evidence-cue/1`
- [x] Annotation protocol versioned as `mesc-pilot-01-b1-annotation/1`
- [x] Segment index convention zero-based; negative/out-of-range/duplicate/
      non-canonical/wrong-document references rejected
- [x] Segment hashing exact UTF-8 bytes, no normalization
- [x] Evidence ID deterministic and domain-separated; no personal identity,
      timestamps, hostname, path, UUID, or PID
- [x] Annotation view label-blind; prohibited fields excluded and tested
- [x] A/B comparison deterministic; ADJUDICATION_REQUIRED on material
      difference; no automatic consensus
- [x] Final cue construction requires A/B agreement or valid adjudication;
      INSUFFICIENT/AMBIGUOUS require empty references; unreviewed records fail
      closed
- [x] Development subset selector deterministic
      (`mesc-pilot-01-b1-evidence-subset/1`, 150 -> 100, no labels read)
- [x] Evidence-pack loader/validator identity-bound and fail-closed
- [x] B1 prompt adds only the ratified evidence-cue channel; gold never enters
      prompt or generation request
- [x] B1 run identity binds evidence-pack/subset identity
- [x] No retrieval path in any B1 module or CLI
- [x] No raw scientific text in canonical pack/subset artifacts
- [x] No real evidence pack, subset, worksheet, or annotation produced
- [x] No model execution, weight download, or network access performed
- [x] No P01-06 or vNext Stage 1 authority introduced

---

## Blocking findings

NONE

---

## Current acceptance status

B1 EVIDENCE SOURCE: RATIFIED — MANUAL LABEL-BLIND NATIVE-CONTEXT EVIDENCE CUES

B1 IMPLEMENTATION: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES

B1 DEVELOPMENT EVIDENCE-PACK TOOLING: ADOPTED / QUALIFIED WITH SYNTHETIC FIXTURES

B1 DEVELOPMENT EVIDENCE PACK: NOT PRODUCED

B0 EXECUTION: NOT AUTHORIZED

B1 EXECUTION: NOT AUTHORIZED

TEST EVIDENCE PACK: NOT AUTHORIZED

P01-06: NOT AUTHORIZED

vNext Stage 1: NOT AUTHORIZED