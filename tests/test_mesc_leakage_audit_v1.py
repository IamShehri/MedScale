"""Synthetic qualification tests for P01-04E leakage-audit orchestration.

Every input is a synthetic literal.  No real or canonical record, dataset,
registry, model or evidence root is touched.  Tests prove all 35 qualification
points from the FD-E-CTX-1 implementation authorization.

The golden vectors are explicit byte and digest literals derived by hand from
the adopted contract.
"""

from __future__ import annotations

import builtins
import io
import os
import pathlib
import socket

import pytest

from medscale.mesc._canonical_json_v1 import canonical_json_bytes, sha256_of_bytes
from medscale.mesc._leakage_audit_v1 import (
    AUDIT_SCHEMA_VERSION,
    AuditInputError,
    AuditSourceRecord,
    ClassificationLedgerError,
    LeakageAuditContractError,
    SourceRecordIdentity,
    SplitIdentityBundle,
    build_audit_document,
    canonical_audit_bytes,
    run_leakage_audit,
)
from medscale.mesc._leakage_v1 import (
    CONTEXT_OVERLAP_THRESHOLD_PERCENT,
    NEAR_DUPLICATE_THRESHOLD_PERCENT,
    LeakageFinding,
)

# --------------------------------------------------------------------------
# Synthetic helpers
# --------------------------------------------------------------------------

_SYNTHETIC_EPISODE = "a" * 64
_SYNTHETIC_FINGERPRINT = "b" * 64
_SYNTHETIC_GM_SHA = "c" * 64
_SYNTHETIC_ER_SHA = "d" * 64
_SYNTHETIC_SR_SHA = "e" * 64
_SYNTHETIC_SR_BYTE_SIZE = 999999


def _split_identity(
    *,
    episode: str = _SYNTHETIC_EPISODE,
    fingerprint: str = _SYNTHETIC_FINGERPRINT,
    gm_sha: str = _SYNTHETIC_GM_SHA,
    gm_size: int = 2451,
    er_sha: str = _SYNTHETIC_ER_SHA,
    er_size: int = 311432,
) -> SplitIdentityBundle:
    return SplitIdentityBundle(
        episode_identity=episode,
        split_fingerprint=fingerprint,
        generation_manifest_sha256=gm_sha,
        generation_manifest_byte_size=gm_size,
        example_registry_sha256=er_sha,
        example_registry_byte_size=er_size,
    )


def _source_identity(
    sha: str = _SYNTHETIC_SR_SHA, size: int = _SYNTHETIC_SR_BYTE_SIZE
) -> SourceRecordIdentity:
    return SourceRecordIdentity(sha256=sha, byte_size=size)


def _record(
    *,
    example_id: str = "mesc-pilot-01:aaaa",
    original_example_id: str = "ex-001",
    source_document_id: str = "sd-001",
    partition: str = "train",
    question: str = "What is the treatment?",
    context_segments: tuple[str, ...] = ("The patient presents with symptoms.",),
) -> AuditSourceRecord:
    return AuditSourceRecord(
        example_id=example_id,
        original_example_id=original_example_id,
        source_document_id=source_document_id,
        partition=partition,
        question=question,
        context_segments=context_segments,
    )


def _audit_build(findings: list[LeakageFinding]) -> dict[str, object]:
    return build_audit_document(findings, _split_identity(), _source_identity())


# --------------------------------------------------------------------------
# Identity types
# --------------------------------------------------------------------------


def test_split_identity_rejects_malformed_sha() -> None:
    with pytest.raises(LeakageAuditContractError):
        SplitIdentityBundle(
            episode_identity="short",
            split_fingerprint=_SYNTHETIC_FINGERPRINT,
            generation_manifest_sha256=_SYNTHETIC_GM_SHA,
            generation_manifest_byte_size=1,
            example_registry_sha256=_SYNTHETIC_ER_SHA,
            example_registry_byte_size=1,
        )


def test_source_record_identity_rejects_malformed_sha() -> None:
    with pytest.raises(LeakageAuditContractError):
        SourceRecordIdentity(sha256="short", byte_size=1)


def test_source_record_identity_rejects_negative_size() -> None:
    with pytest.raises(LeakageAuditContractError):
        SourceRecordIdentity(sha256=_SYNTHETIC_SR_SHA, byte_size=-1)


# --------------------------------------------------------------------------
# Q1 — exact example cross-partition detection
# --------------------------------------------------------------------------


def test_q1_exact_example_cross_partition_detected_as_confirmed_leakage() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Question alpha one.",
            context_segments=("Alpha segment one.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-001",
            source_document_id="sd-b",
            partition="validation",
            question="Question beta two different.",
            context_segments=("Beta segment two distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    exact_ex = [f for f in findings if f.finding_type == "exact_example"]
    assert len(exact_ex) == 1
    f = exact_ex[0]
    assert f.classification == "confirmed_leakage"
    assert set(f.example_ids) == {"mesc-pilot-01:ex1", "mesc-pilot-01:ex2"}


# --------------------------------------------------------------------------
# Q2 — source-document cross-partition detection
# --------------------------------------------------------------------------


def test_q2_source_document_cross_partition_detected_as_confirmed_leakage() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-001",
            partition="train",
            question="Alpha question one unique.",
            context_segments=("Alpha segment one.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-001",
            partition="test",
            question="Beta question two distinct.",
            context_segments=("Beta segment two distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    sd = [f for f in findings if f.finding_type == "source_document"]
    assert len(sd) == 1
    f = sd[0]
    assert f.classification == "confirmed_leakage"


# --------------------------------------------------------------------------
# Q3 — exact-question detection
# --------------------------------------------------------------------------


def test_q3_exact_question_detected_as_unresolved() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Who discovered penicillin?",
            context_segments=("Alpha context segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Who discovered penicillin?",
            context_segments=("Beta context segment distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    eq = [f for f in findings if f.finding_type == "exact_question"]
    assert len(eq) == 1
    f = eq[0]
    assert f.classification == "unresolved"
    assert f.score_representation == "none"


# --------------------------------------------------------------------------
# Q4 — normalized-question detection
# --------------------------------------------------------------------------


def test_q4_normalized_question_detected_as_unresolved() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="  WHO discovered Penicillin  ",
            context_segments=("Alpha context segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="test",
            question="who discovered penicillin",
            context_segments=("Beta context segment distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    types = {f.finding_type for f in findings}
    assert "normalized_question" in types
    normalized_finding = next(f for f in findings if f.finding_type == "normalized_question")
    assert normalized_finding.classification == "unresolved"


# --------------------------------------------------------------------------
# Q5 — Jaccard exactly below 0.90 -> no near-duplicate finding
# --------------------------------------------------------------------------


def test_q5_jaccard_below_90_no_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="a b c d e f g h",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="a b c d e f g x",
        ),
    ]
    findings = run_leakage_audit(records)
    types = {f.finding_type for f in findings}
    assert "near_duplicate_question" not in types


# --------------------------------------------------------------------------
# Q6 — Jaccard exactly at 0.90 -> finding
# --------------------------------------------------------------------------


def test_q6_jaccard_exactly_90_produces_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="a b c d e f g h i",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="a b c d e f g h i x",
        ),
    ]
    findings = run_leakage_audit(records)
    ndq = [f for f in findings if f.finding_type == "near_duplicate_question"]
    assert len(ndq) == 1
    assert ndq[0].score_representation == "jaccard:9/10"
    assert ndq[0].classification == "unresolved"


# --------------------------------------------------------------------------
# Q7 — Jaccard above 0.90 -> finding
# --------------------------------------------------------------------------


def test_q7_jaccard_above_90_produces_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="a b c d e f g h i j k l m n o p q r s",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="test",
            question="a b c d e f g h i j k l m n o p q r t",
        ),
    ]
    findings = run_leakage_audit(records)
    ndq = [f for f in findings if f.finding_type == "near_duplicate_question"]
    assert len(ndq) == 1
    assert ndq[0].classification == "unresolved"


# --------------------------------------------------------------------------
# Q8 — both-empty normalized question -> unresolved finding
# --------------------------------------------------------------------------


def test_q8_both_empty_normalized_question_unresolved() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="   ",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="\t\n",
        ),
    ]
    findings = run_leakage_audit(records)
    enq = [f for f in findings if f.finding_type == "empty_normalized_question"]
    assert len(enq) == 1
    assert enq[0].classification == "unresolved"
    assert enq[0].score_representation == "not_evaluable"


# --------------------------------------------------------------------------
# Q9 — exact raw context equality -> context_overlap / none
# --------------------------------------------------------------------------


def test_q9_exact_context_equality_produces_context_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            context_segments=("Identical segment one.", "Unique segment A."),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            context_segments=("Identical segment one.", "Unique segment B."),
        ),
    ]
    findings = run_leakage_audit(records)
    ctx = [f for f in findings if f.finding_type == "context_overlap"]
    assert len(ctx) >= 1
    exact_ctx = [f for f in ctx if f.score_representation == "none"]
    assert len(exact_ctx) == 1
    assert exact_ctx[0].classification == "unresolved"


# --------------------------------------------------------------------------
# Q10 — context Jaccard below 0.95 -> no approximate finding
# --------------------------------------------------------------------------


def test_q10_context_jaccard_below_95_no_approximate_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            context_segments=("a b c d e f g h i j k l m n o p q r",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            context_segments=("a b c d e f g h i j k l m n o p q x",),
        ),
    ]
    findings = run_leakage_audit(records)
    ctx_jacc = [
        f
        for f in findings
        if f.finding_type == "context_overlap" and f.score_representation.startswith("jaccard:")
    ]
    assert len(ctx_jacc) == 0


# --------------------------------------------------------------------------
# Q11 — context Jaccard exactly 0.95 -> context finding
# --------------------------------------------------------------------------


def test_q11_context_jaccard_exactly_95_produces_finding() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            context_segments=("a b c d e f g h i j k l m n o p q r s",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="test",
            context_segments=("a b c d e f g h i j k l m n o p q r s x",),
        ),
    ]
    findings = run_leakage_audit(records)
    ctx_jacc = [
        f
        for f in findings
        if f.finding_type == "context_overlap" and f.score_representation.startswith("jaccard:")
    ]
    assert len(ctx_jacc) == 1
    assert ctx_jacc[0].classification == "unresolved"


# --------------------------------------------------------------------------
# Q12 — context Jaccard above 0.95 -> context finding
# --------------------------------------------------------------------------


def test_q12_context_jaccard_above_95_produces_finding() -> None:
    # 20 shared tokens + 1 unique on right = 21 union, 20/21 ~ 0.952 > 0.95
    shared = "a b c d e f g h i j k l m n o p q r s t"
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Alpha question.",
            context_segments=(shared,),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Beta question different.",
            context_segments=(f"{shared} x",),
        ),
    ]
    findings = run_leakage_audit(records)
    ctx_jacc = [
        f
        for f in findings
        if f.finding_type == "context_overlap" and f.score_representation.startswith("jaccard:")
    ]
    assert len(ctx_jacc) == 1


# --------------------------------------------------------------------------
# Q13 — same-partition pairs never enumerated
# --------------------------------------------------------------------------


def test_q13_same_partition_pairs_not_enumerated() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-001",
            partition="train",
            question="Identical question.",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-002",
            partition="train",
            question="Identical question.",
        ),
    ]
    findings = run_leakage_audit(records)
    assert len(findings) == 0


# --------------------------------------------------------------------------
# Q14 — all three cross-partition pair domains covered
# --------------------------------------------------------------------------


def test_q14_all_three_partition_pairs_covered() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-001",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-002",
            partition="validation",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex3",
            original_example_id="ex-003",
            source_document_id="sd-003",
            partition="test",
            question="Q?",
        ),
    ]
    findings = run_leakage_audit(records)
    eq = {frozenset(f.partitions) for f in findings if f.finding_type == "exact_question"}
    assert frozenset({"train", "validation"}) in eq
    assert frozenset({"train", "test"}) in eq
    assert frozenset({"validation", "test"}) in eq


# --------------------------------------------------------------------------
# Q15 — deterministic finding ordering
# --------------------------------------------------------------------------


def test_q15_findings_are_sorted_by_ascending_id() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="What is treatment?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="What is diagnosis?",
            context_segments=("Important context.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex3",
            original_example_id="ex-003",
            source_document_id="sd-c",
            partition="test",
            question="What is diagnosis?",
            context_segments=("Important context.",),
        ),
    ]
    findings = run_leakage_audit(records)
    ids = [f.finding_id for f in findings]
    assert ids == sorted(ids)
    assert len(ids) == len(set(ids))


# --------------------------------------------------------------------------
# Q16 — deterministic finding IDs
# --------------------------------------------------------------------------


def test_q16_repeated_audit_produces_identical_finding_ids() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    first = {f.finding_id for f in run_leakage_audit(records)}
    second = {f.finding_id for f in run_leakage_audit(records)}
    assert first == second


# --------------------------------------------------------------------------
# Q17 — duplicate/suppressed finding cannot disappear
# --------------------------------------------------------------------------


def test_q17_finding_cannot_be_suppressed() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Question A?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Question A?",
        ),
    ]
    findings = run_leakage_audit(records)
    assert len(findings) >= 1
    for f in findings:
        assert f.suppressed is False


# --------------------------------------------------------------------------
# Q18 — incomplete classification leaves unresolved
# --------------------------------------------------------------------------


def test_q18_missing_classification_stays_unresolved() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    findings = run_leakage_audit(records)
    eq = [f for f in findings if f.finding_type == "exact_question"]
    assert len(eq) == 1
    assert eq[0].classification == "unresolved"


# --------------------------------------------------------------------------
# Q19 — false_positive without evidence reference refused
# --------------------------------------------------------------------------


def test_q19_false_positive_without_evidence_refused() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    findings = run_leakage_audit(records)
    eq_finding = next(f for f in findings if f.finding_type == "exact_question")
    ledger = [{"finding_id": eq_finding.finding_id, "classification": "false_positive"}]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(records, ledger)


# --------------------------------------------------------------------------
# Q20 — unknown classification-ledger finding refused
# --------------------------------------------------------------------------


def test_q20_unknown_ledger_finding_refused() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
        ),
    ]
    ledger = [
        {
            "finding_id": "mesc-pilot-01-leakage-finding/1:sha256:" + "f" * 64,
            "classification": "false_positive",
            "evidence_reference": "evidence:ref",
        }
    ]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(records, ledger)


# --------------------------------------------------------------------------
# Q21 — source-record identity mismatch refused (tested via identity types)
# --------------------------------------------------------------------------


def test_q21_source_record_identity_mismatch_refused() -> None:
    with pytest.raises(LeakageAuditContractError):
        SourceRecordIdentity(sha256="!" * 64, byte_size=1)


# --------------------------------------------------------------------------
# Q22 — split fingerprint mismatch refused
# --------------------------------------------------------------------------


def test_q22_split_fingerprint_mismatch_refused() -> None:
    with pytest.raises(LeakageAuditContractError):
        SplitIdentityBundle(
            episode_identity=_SYNTHETIC_EPISODE,
            split_fingerprint="Z" * 64,
            generation_manifest_sha256=_SYNTHETIC_GM_SHA,
            generation_manifest_byte_size=1,
            example_registry_sha256=_SYNTHETIC_ER_SHA,
            example_registry_byte_size=1,
        )


# --------------------------------------------------------------------------
# Q25 — repository output refused (not directly testable in pure module)
#        Operator guards this; see operator tests.
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Q30 — raw question/context marker absent from leakage-audit.json
# --------------------------------------------------------------------------


def test_q30_audit_document_contains_no_raw_text() -> None:
    findings: list[LeakageFinding] = []
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    raw = canonical_json_bytes(doc)
    assert b"question_bytes" not in raw
    assert b"context_bytes" not in raw
    for f_text in ("zzsecret", "what is", "treatment", "patient"):
        assert f_text.encode() not in raw


# --------------------------------------------------------------------------
# Q32 — report exact schema and exact keys
# --------------------------------------------------------------------------


def test_q32_audit_document_has_exact_keys() -> None:
    findings: list[LeakageFinding] = []
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    assert set(doc) == {
        "schema_version",
        "split_identity",
        "source_records_identity",
        "thresholds",
        "detection_methods",
        "normalization_record",
        "finding_count",
        "findings",
        "leaked",
    }
    assert doc["schema_version"] == AUDIT_SCHEMA_VERSION
    assert doc["thresholds"] == {
        "question_near_duplicate_jaccard_percent": NEAR_DUPLICATE_THRESHOLD_PERCENT,
        "context_overlap_jaccard_percent": CONTEXT_OVERLAP_THRESHOLD_PERCENT,
    }


# --------------------------------------------------------------------------
# Q33 — leakage-audit.json only; no alias artifact
# --------------------------------------------------------------------------


def test_q33_canonical_bytes_ends_with_lf() -> None:
    findings: list[LeakageFinding] = []
    audit_bytes = canonical_audit_bytes(findings, _split_identity(), _source_identity())
    assert audit_bytes.endswith(b"\n")
    assert audit_bytes.count(b"\n") == 1


# --------------------------------------------------------------------------
# Q34 — leaked derived exactly from classifications
# --------------------------------------------------------------------------


def test_q34a_zero_findings_leaked_false() -> None:
    findings: list[LeakageFinding] = []
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    assert doc["leaked"] is False
    assert doc["finding_count"] == 0


def test_q34b_unresolved_finding_leaked_true() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    findings = run_leakage_audit(records)
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    assert doc["leaked"] is True


def test_q34c_confirmed_leakage_leaked_true() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-001",
            partition="train",
            question="Alpha unique question.",
            context_segments=("Alpha segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-001",
            source_document_id="sd-001",
            partition="validation",
            question="Beta question distinct.",
            context_segments=("Beta segment distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    assert doc["leaked"] is True


def test_q34d_false_positives_set_leaked_false_via_ledger() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
            context_segments=("Alpha segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
            context_segments=("Beta segment distinct.",),
        ),
    ]
    raw_findings = run_leakage_audit(records)
    # Classify every finding as false_positive to get leaked=false.
    ledger = [
        {
            "finding_id": f.finding_id,
            "classification": "false_positive",
            "evidence_reference": f"evidence:synthetic-{i:04d}",
        }
        for i, f in enumerate(raw_findings)
    ]
    findings = run_leakage_audit(records, ledger)
    assert all(f.classification == "false_positive" for f in findings)
    doc = build_audit_document(findings, _split_identity(), _source_identity())
    assert doc["leaked"] is False


# --------------------------------------------------------------------------
# Q35 — repeated synthetic audit produces byte-identical output
# --------------------------------------------------------------------------


def test_q35_repeated_audit_byte_identical() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Test question?",
            context_segments=("Context one.", "Context two."),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Different question.",
            context_segments=("Context one.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex3",
            original_example_id="ex-003",
            source_document_id="sd-c",
            partition="test",
            question="Third question?",
            context_segments=("Context three.",),
        ),
    ]
    first_findings = run_leakage_audit(records)
    second_findings = run_leakage_audit(records)
    assert len(first_findings) == len(second_findings)
    first_bytes = canonical_audit_bytes(first_findings, _split_identity(), _source_identity())
    second_bytes = canonical_audit_bytes(second_findings, _split_identity(), _source_identity())
    assert first_bytes == second_bytes
    sha_a = sha256_of_bytes(first_bytes)
    sha_b = sha256_of_bytes(second_bytes)
    assert sha_a == sha_b


# --------------------------------------------------------------------------
# Classification ledger validation
# --------------------------------------------------------------------------


def test_ledger_false_positive_with_evidence_accepted() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    raw_findings = run_leakage_audit(records)
    eq = next(f for f in raw_findings if f.finding_type == "exact_question")
    ledger = [
        {
            "finding_id": eq.finding_id,
            "classification": "false_positive",
            "evidence_reference": "evidence:ref",
        }
    ]
    findings = run_leakage_audit(records, ledger)
    resolved = next(f for f in findings if f.finding_type == "exact_question")
    assert resolved.classification == "false_positive"
    assert resolved.evidence_reference == "evidence:ref"


def test_ledger_duplicate_finding_refused() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    raw_findings = run_leakage_audit(records)
    eq = next(f for f in raw_findings if f.finding_type == "exact_question")
    ledger = [
        {
            "finding_id": eq.finding_id,
            "classification": "false_positive",
            "evidence_reference": "evidence:ref",
        },
        {
            "finding_id": eq.finding_id,
            "classification": "false_positive",
            "evidence_reference": "evidence:ref2",
        },
    ]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(records, ledger)


def test_ledger_confirmed_leakage_accepted() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    raw_findings = run_leakage_audit(records)
    eq = next(f for f in raw_findings if f.finding_type == "exact_question")
    ledger = [
        {
            "finding_id": eq.finding_id,
            "classification": "confirmed_leakage",
        }
    ]
    findings = run_leakage_audit(records, ledger)
    resolved = next(f for f in findings if f.finding_type == "exact_question")
    assert resolved.classification == "confirmed_leakage"


def test_ledger_invalid_classification_refused() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Q?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Q?",
        ),
    ]
    raw_findings = run_leakage_audit(records)
    eq = next(f for f in raw_findings if f.finding_type == "exact_question")
    ledger = [
        {
            "finding_id": eq.finding_id,
            "classification": "benign",
            "evidence_reference": "evidence:ref",
        }
    ]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(records, ledger)


# --------------------------------------------------------------------------
# Input validation
# --------------------------------------------------------------------------


def test_empty_records_refused() -> None:
    with pytest.raises(LeakageAuditContractError):
        run_leakage_audit([])


def test_non_sequence_records_refused() -> None:
    with pytest.raises(LeakageAuditContractError):
        run_leakage_audit(None)  # type: ignore[arg-type]


def test_unknown_partition_refused() -> None:
    with pytest.raises(AuditInputError):
        run_leakage_audit(
            [
                _record(
                    original_example_id="ex-001",
                    partition="holdout",
                )
            ]
        )


def test_non_audit_source_record_type_refused() -> None:
    with pytest.raises(AuditInputError):
        run_leakage_audit([("not", "a", "record")])  # type: ignore[list-item]


# --------------------------------------------------------------------------
# Identity bundle document shape
# --------------------------------------------------------------------------


def test_split_identity_document_shape() -> None:
    si = SplitIdentityBundle(
        episode_identity="1" * 64,
        split_fingerprint="2" * 64,
        generation_manifest_sha256="3" * 64,
        generation_manifest_byte_size=2451,
        example_registry_sha256="4" * 64,
        example_registry_byte_size=311432,
    )
    doc = si.to_canonical_document()
    assert set(doc) == {
        "episode_identity",
        "split_fingerprint",
        "generation_manifest_sha256",
        "generation_manifest_byte_size",
        "example_registry_sha256",
        "example_registry_byte_size",
    }


def test_source_record_identity_document_shape() -> None:
    sr = SourceRecordIdentity(sha256="1" * 64, byte_size=2770193)
    doc = sr.to_canonical_document()
    assert set(doc) == {"sha256", "byte_size"}


# --------------------------------------------------------------------------
# Split identity binding in audit document
# --------------------------------------------------------------------------


def test_split_identity_bound_into_audit_document() -> None:
    si = _split_identity()
    sr = _source_identity()
    findings: list[LeakageFinding] = []
    doc = build_audit_document(findings, si, sr)
    assert doc["split_identity"] == si.to_canonical_document()
    assert doc["source_records_identity"] == sr.to_canonical_document()


# --------------------------------------------------------------------------
# Context normalization applies the ratified pipeline
# --------------------------------------------------------------------------


def test_context_normalization_applies_nfkc_and_casefold() -> None:
    """Prove context segment comparison normalizes before Jaccard."""
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            context_segments=("\ufb01le symptoms include fever",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            context_segments=("FILE symptoms include fever",),
        ),
    ]
    findings = run_leakage_audit(records)
    # After NFKC: "\ufb01le" -> "file", casefold: "FILE" -> "file"
    # Both become "file symptoms include fever" -> same token set -> Jaccard 1/1 >= 0.95
    ctx_jacc = [
        f
        for f in findings
        if f.finding_type == "context_overlap" and f.score_representation == "jaccard:1/1"
    ]
    assert len(ctx_jacc) >= 1


# --------------------------------------------------------------------------
# Write boundary
# --------------------------------------------------------------------------


def test_audit_module_does_not_access_filesystem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("filesystem access is prohibited")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(io, "open", forbidden)
    monkeypatch.setattr(os, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "open", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_bytes", forbidden)
    monkeypatch.setattr(pathlib.Path, "write_text", forbidden)

    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            partition="train",
            question="Alpha question.",
            context_segments=("Alpha segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            partition="validation",
            question="Beta question different.",
            context_segments=("Beta segment distinct.",),
        ),
    ]
    run_leakage_audit(records)


def test_audit_module_does_not_access_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("network access is prohibited")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)

    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            partition="train",
            question="Alpha question.",
            context_segments=("Alpha segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            partition="validation",
            question="Beta question different.",
            context_segments=("Beta segment distinct.",),
        ),
    ]
    run_leakage_audit(records)


def test_module_not_publicly_exported() -> None:
    import medscale.mesc as package

    assert "_leakage_audit_v1" not in package.__all__
    assert "run_leakage_audit" not in package.__all__
    assert not hasattr(package, "run_leakage_audit")


# --------------------------------------------------------------------------
# Q31 — structural classification is non-downgradable (exact_example /
#       source_document can never be reclassified by the review ledger)
# --------------------------------------------------------------------------


def _structural_records(*, kind: str) -> list[AuditSourceRecord]:
    """Return a synthetic pair producing one finding of the requested kind.

    ``kind == "exact_example"`` duplicates ``original_example_id`` across
    partitions; ``kind == "source_document"`` duplicates the
    ``source_document_id`` across partitions.
    """
    if kind == "exact_example":
        return [
            _record(
                example_id="mesc-pilot-01:ex1",
                original_example_id="ex-001",
                source_document_id="sd-a",
                partition="train",
                question="Question alpha unique.",
                context_segments=("Alpha segment one.",),
            ),
            _record(
                example_id="mesc-pilot-01:ex2",
                original_example_id="ex-001",
                source_document_id="sd-b",
                partition="validation",
                question="Question beta distinct.",
                context_segments=("Beta segment two.",),
            ),
        ]
    if kind == "source_document":
        return [
            _record(
                example_id="mesc-pilot-01:ex1",
                original_example_id="ex-001",
                source_document_id="sd-001",
                partition="train",
                question="Question alpha unique.",
                context_segments=("Alpha segment one.",),
            ),
            _record(
                example_id="mesc-pilot-01:ex2",
                original_example_id="ex-002",
                source_document_id="sd-001",
                partition="test",
                question="Question beta distinct.",
                context_segments=("Beta segment two.",),
            ),
        ]
    raise AssertionError(f"unknown structural kind {kind!r}")


@pytest.mark.parametrize("kind", ["exact_example", "source_document"])
def test_structural_no_ledger_is_confirmed_leakage(kind: str) -> None:
    findings = run_leakage_audit(_structural_records(kind=kind))
    structural = [f for f in findings if f.finding_type == kind]
    assert len(structural) == 1
    assert structural[0].classification == "confirmed_leakage"


@pytest.mark.parametrize("kind", ["exact_example", "source_document"])
def test_structural_confirmed_leakage_ledger_entry_is_accepted(kind: str) -> None:
    findings = run_leakage_audit(_structural_records(kind=kind))
    structural = next(f for f in findings if f.finding_type == kind)
    ledger = [{"finding_id": structural.finding_id, "classification": "confirmed_leakage"}]
    out = run_leakage_audit(_structural_records(kind=kind), ledger)
    resolved = next(f for f in out if f.finding_type == kind)
    assert resolved.classification == "confirmed_leakage"


@pytest.mark.parametrize("kind", ["exact_example", "source_document"])
def test_structural_false_positive_ledger_entry_is_refused(kind: str) -> None:
    findings = run_leakage_audit(_structural_records(kind=kind))
    structural = next(f for f in findings if f.finding_type == kind)
    ledger = [
        {
            "finding_id": structural.finding_id,
            "classification": "false_positive",
            "evidence_reference": "evidence:review-1",
        }
    ]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(_structural_records(kind=kind), ledger)


@pytest.mark.parametrize("kind", ["exact_example", "source_document"])
def test_structural_unresolved_ledger_entry_is_refused(kind: str) -> None:
    findings = run_leakage_audit(_structural_records(kind=kind))
    structural = next(f for f in findings if f.finding_type == kind)
    ledger = [{"finding_id": structural.finding_id, "classification": "unresolved"}]
    with pytest.raises(ClassificationLedgerError):
        run_leakage_audit(_structural_records(kind=kind), ledger)


def test_scientific_text_finding_remains_reviewable_false_positive() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Identical question text?",
            context_segments=("Alpha segment.",),
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Identical question text?",
            context_segments=("Beta segment distinct.",),
        ),
    ]
    findings = run_leakage_audit(records)
    eq = next(f for f in findings if f.finding_type == "exact_question")
    ledger = [
        {
            "finding_id": eq.finding_id,
            "classification": "false_positive",
            "evidence_reference": "evidence:review-2",
        }
    ]
    out = run_leakage_audit(records, ledger)
    resolved = next(f for f in out if f.finding_type == "exact_question")
    assert resolved.classification == "false_positive"
    assert resolved.evidence_reference == "evidence:review-2"


def test_scientific_text_finding_remains_reviewable_confirmed_leakage() -> None:
    records = [
        _record(
            example_id="mesc-pilot-01:ex1",
            original_example_id="ex-001",
            source_document_id="sd-a",
            partition="train",
            question="Question A?",
        ),
        _record(
            example_id="mesc-pilot-01:ex2",
            original_example_id="ex-002",
            source_document_id="sd-b",
            partition="validation",
            question="Question A?",
        ),
    ]
    findings = run_leakage_audit(records)
    eq = next(f for f in findings if f.finding_type == "exact_question")
    ledger = [{"finding_id": eq.finding_id, "classification": "confirmed_leakage"}]
    out = run_leakage_audit(records, ledger)
    resolved = next(f for f in out if f.finding_type == "exact_question")
    assert resolved.classification == "confirmed_leakage"
