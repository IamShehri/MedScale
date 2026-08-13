"""B1 CLI operator-safety tests: explicit paths, no overwrite, fail-closed wiring.

Synthetic fixtures only — no real registry, subset, annotation, evidence pack,
model, network, or retrieval. The eval command is exercised with an injected
generator; the evidence command writes/validates deterministic JSON artifacts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from medscale.cli import mesc_b1_eval, mesc_b1_evidence
from medscale.mesc._b1 import B1Config
from medscale.mesc._b1_evidence import (
    B1SourceRecord,
    build_evidence_pack,
    build_final_cue_from_agreement,
    make_annotation_submission,
    pack_to_document,
)
from medscale.mesc._split_v1 import canonical_json_bytes
from medscale.modelkit.interfaces import GenerationRequest, GenerationResult, ModelRef

_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
_SHA = "a" * 40
_COMMIT = "c" * 40
_SPLIT_FINGERPRINT = "43bd2b2f1777139927960df72d6f540525d216a239048f596e35d8befb58fb91"


class _FakeB1Generator:
    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text="yes",
            model=ModelRef(model_id=_MODEL, revision=_SHA, backend="transformers"),
        )


def _fake_factory(config: B1Config) -> _FakeB1Generator:
    return _FakeB1Generator()


def _failing_factory(config: B1Config) -> _FakeB1Generator:
    from medscale.backends.transformers.backend import TransformersLoadError

    raise TransformersLoadError("simulated local load failure")


def _write_b0_input(path: Path) -> None:
    path.write_text(
        '{"example_id":"e0","row_ordinal":0,"source_document_id":"pmid:1",'
        '"dataset_id":"ds","dataset_revision":"rev-1","configuration":"cfg",'
        '"question":"does aspirin help?","context":["some context"],"decision":"yes"}\n',
        encoding="utf-8",
    )


def _write_evidence_pack(path: Path) -> str:
    source = B1SourceRecord(
        example_id="e0",
        source_document_id="pmid:1",
        question="does aspirin help?",
        context=("some context",),
    )
    submission = make_annotation_submission(
        reviewer_id="r1",
        example_id="e0",
        source_document_id="pmid:1",
        selected_segment_indices=[0],
        annotation_status="AVAILABLE",
    )
    from medscale.mesc._b1_evidence import B1AnnotationComparison

    comparison = B1AnnotationComparison(
        example_id="e0",
        source_document_id="pmid:1",
        outcome="AGREED",
        submission_a=submission,
        submission_b=submission,
    )
    pack = build_evidence_pack(
        [build_final_cue_from_agreement(comparison, source_record=source)],
        source_split_fingerprint=_SPLIT_FINGERPRINT,
        subset_digest="0" * 64,
    )
    raw = canonical_json_bytes(pack_to_document(pack)) + b"\n"
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def _eval_args(tmp_path: Path) -> list[str]:
    pack_sha = _write_evidence_pack(tmp_path / "pack.json")
    _write_b0_input(tmp_path / "in.jsonl")
    input_sha = hashlib.sha256((tmp_path / "in.jsonl").read_bytes()).hexdigest()
    input_size = (tmp_path / "in.jsonl").stat().st_size
    return [
        "--input",
        str(tmp_path / "in.jsonl"),
        "--input-sha256",
        input_sha,
        "--input-size",
        str(input_size),
        "--evidence-pack",
        str(tmp_path / "pack.json"),
        "--evidence-pack-sha256",
        pack_sha,
        "--model-id",
        _MODEL,
        "--model-revision",
        _SHA,
        "--tokenizer-revision",
        _SHA,
        "--code-commit",
        _COMMIT,
        "--output",
        str(tmp_path / "out.json"),
    ]


# ---------------------------------------------------------------- mesc-b1-eval
def test_b1_eval_runs_with_injected_generator(tmp_path: Path) -> None:
    assert mesc_b1_eval.main(_eval_args(tmp_path), generator_factory=_fake_factory) == 0
    assert (tmp_path / "out.json").is_file()


def test_b1_eval_requires_arguments(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert mesc_b1_eval.main(["--output", str(tmp_path / "o.json")]) == 2
    assert "--input is required" in capsys.readouterr().err


def test_b1_eval_missing_input_file_is_friendly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    pack_sha = _write_evidence_pack(tmp_path / "pack.json")
    args = [
        "--input",
        str(tmp_path / "missing.jsonl"),
        "--input-sha256",
        "0" * 64,
        "--input-size",
        "1",
        "--evidence-pack",
        str(tmp_path / "pack.json"),
        "--evidence-pack-sha256",
        pack_sha,
        "--model-id",
        _MODEL,
        "--model-revision",
        _SHA,
        "--tokenizer-revision",
        _SHA,
        "--code-commit",
        _COMMIT,
        "--output",
        str(tmp_path / "out.json"),
    ]
    rc = mesc_b1_eval.main(args, generator_factory=_fake_factory)
    assert rc == 2
    assert "input file not found" in capsys.readouterr().err


def test_b1_eval_refuses_to_overwrite_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "out.json").write_text("existing", encoding="utf-8")
    rc = mesc_b1_eval.main(_eval_args(tmp_path), generator_factory=_fake_factory)
    assert rc == 2
    assert "output already exists" in capsys.readouterr().err


def test_b1_eval_rejects_unapproved_model(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    args = _eval_args(tmp_path)
    args[args.index(_MODEL)] = "Qwen/Qwen2.5-7B-Instruct"
    rc = mesc_b1_eval.main(args, generator_factory=_fake_factory)
    assert rc == 2
    assert "model_id must be one of" in capsys.readouterr().err


def test_b1_eval_validates_before_constructing_runtime(tmp_path: Path) -> None:
    called = {"n": 0}

    def _spy_factory(config: B1Config) -> _FakeB1Generator:
        called["n"] += 1
        return _FakeB1Generator()

    args = _eval_args(tmp_path)
    args[args.index(_MODEL)] = "Qwen/Qwen2.5-7B-Instruct"
    assert mesc_b1_eval.main(args, generator_factory=_spy_factory) == 2
    assert called["n"] == 0


def test_b1_eval_requires_code_commit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    args = _eval_args(tmp_path)
    index = args.index("--code-commit")
    del args[index : index + 2]
    assert mesc_b1_eval.main(args, generator_factory=_fake_factory) == 2
    assert "--code-commit is required" in capsys.readouterr().err


def test_b1_eval_rejects_mutable_revision(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    args = _eval_args(tmp_path)
    args[args.index(_SHA)] = "main"
    assert mesc_b1_eval.main(args, generator_factory=_fake_factory) == 2
    assert "--model-revision must be a full lowercase 40-hex commit SHA" in capsys.readouterr().err


def test_b1_eval_rejects_bad_pack_sha(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    args = _eval_args(tmp_path)
    args[args.index("--evidence-pack-sha256") + 1] = "not-a-sha"
    assert mesc_b1_eval.main(args, generator_factory=_fake_factory) == 2
    assert "64-hex SHA-256" in capsys.readouterr().err


def test_b1_eval_backend_failure_uses_engine_exit_code(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = mesc_b1_eval.main(_eval_args(tmp_path), generator_factory=_failing_factory)
    assert rc == 1
    assert "backend error" in capsys.readouterr().err


def test_b1_eval_help_makes_no_training_or_clinical_claim() -> None:
    description = mesc_b1_eval.DESCRIPTION.lower()
    assert "no training" in description
    assert "no retrieval" in description
    assert "no model download" in description
    assert "no real split execution" in description
    assert "no clinical claim" in description


# ---------------------------------------------------------------- mesc-b1-evidence
def _source_record_line(example_id: str = "e0", context: list[str] | None = None) -> str:
    return json.dumps(
        {
            "example_id": example_id,
            "source_document_id": "pmid:1",
            "question": "does aspirin help?",
            "context": context if context is not None else ["some context"],
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _write_source_records(path: Path, count: int = 1) -> None:
    lines = "\n".join(_source_record_line(f"e{i}") for i in range(count)) + "\n"
    path.write_text(lines, encoding="utf-8")


def _write_single_subset_manifest(path: Path) -> str:
    """Write a one-member development-subset manifest matching the source fixture.

    Returns the manifest's ``subset_digest``.
    """
    from medscale.mesc._b1_evidence import (
        load_example_registry_from_bytes,
        select_development_subset,
        write_subset_manifest,
    )

    registry_bytes = b"".join(
        json.dumps(
            {
                "schema_version": "mesc-pilot-01-example-registry/1",
                "example_id": f"e{i}",
                "source_document_id": f"pmid:{i + 1}",
                "assigned_split": "validation",
                "partition_key": f"pk-{i}",
                "row_ordinal": i,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
        for i in range(1)
    )
    registry_rows, registry_sha256 = load_example_registry_from_bytes(registry_bytes)
    selection = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
    )
    write_subset_manifest(selection, path)
    return selection.subset_digest


def _registry_line(example_id: str, split: str, ordinal: int) -> str:
    return json.dumps(
        {
            "schema_version": "mesc-pilot-01-example-registry/1",
            "example_id": example_id,
            "source_document_id": f"pmid:{ordinal}",
            "assigned_split": split,
            "partition_key": f"pk-{ordinal}",
            "row_ordinal": ordinal,
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _write_registry(path: Path, count: int = 20) -> None:
    lines = "".join(_registry_line(f"e{i}", "validation", i) + "\n" for i in range(count))
    path.write_text(lines, encoding="utf-8")


def test_b1_evidence_select_subset(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    registry = tmp_path / "registry.jsonl"
    _write_registry(registry)
    out = tmp_path / "subset.json"
    rc = mesc_b1_evidence.main(
        [
            "select-subset",
            "--registry",
            str(registry),
            "--output",
            str(out),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
        ]
    )
    assert rc == 0
    assert out.is_file()
    document = json.loads(out.read_text(encoding="utf-8"))
    assert document["selected_count"] == 20
    assert document["schema_version"] == "mesc-pilot-01-b1-development-subset/1"
    assert "subset_digest" in capsys.readouterr().out


def test_b1_evidence_select_subset_refuses_overwrite(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    registry = tmp_path / "registry.jsonl"
    _write_registry(registry)
    out = tmp_path / "subset.json"
    out.write_text("existing", encoding="utf-8")
    rc = mesc_b1_evidence.main(
        [
            "select-subset",
            "--registry",
            str(registry),
            "--output",
            str(out),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
        ]
    )
    assert rc == 2
    assert "output already exists" in capsys.readouterr().err


def test_b1_evidence_render_annotation_view(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    out = tmp_path / "view.jsonl"
    rc = mesc_b1_evidence.main(
        ["render-annotation-view", "--source-record", str(source), "--output", str(out)]
    )
    assert rc == 0
    view = json.loads((out).read_text(encoding="utf-8"))
    assert set(view) == {
        "schema_version",
        "example_id",
        "source_document_id",
        "question",
        "context",
    }
    assert "decision" not in view


def test_b1_evidence_validate_submission(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    submission = tmp_path / "submission.json"
    submission.write_text(
        json.dumps(
            {
                "reviewer_id": "r1",
                "example_id": "e0",
                "source_document_id": "pmid:1",
                "selected_segment_indices": [0],
                "annotation_status": "AVAILABLE",
            }
        ),
        encoding="utf-8",
    )
    rc = mesc_b1_evidence.main(
        [
            "validate-submission",
            "--submission",
            str(submission),
            "--source-record",
            str(source),
        ]
    )
    assert rc == 0


def test_b1_evidence_validate_submission_rejects_bad_status(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    submission = tmp_path / "submission.json"
    submission.write_text(
        json.dumps(
            {
                "reviewer_id": "r1",
                "example_id": "e0",
                "source_document_id": "pmid:1",
                "selected_segment_indices": [0],
                "annotation_status": "UNKNOWN",
            }
        ),
        encoding="utf-8",
    )
    rc = mesc_b1_evidence.main(
        [
            "validate-submission",
            "--submission",
            str(submission),
            "--source-record",
            str(source),
        ]
    )
    assert rc == 2
    assert "invalid submission" in capsys.readouterr().err


def _write_submission(path: Path, reviewer: str, indices: list[int]) -> None:
    path.write_text(
        json.dumps(
            {
                "reviewer_id": reviewer,
                "example_id": "e0",
                "source_document_id": "pmid:1",
                "selected_segment_indices": indices,
                "annotation_status": "AVAILABLE",
            }
        ),
        encoding="utf-8",
    )


def test_b1_evidence_compare_annotations_agreed(tmp_path: Path) -> None:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    _write_submission(a, "r1", [0])
    _write_submission(b, "r2", [0])
    out = tmp_path / "comparison.json"
    rc = mesc_b1_evidence.main(
        [
            "compare-annotations",
            "--submission-a",
            str(a),
            "--submission-b",
            str(b),
            "--output",
            str(out),
        ]
    )
    assert rc == 0
    comparison = json.loads(out.read_text(encoding="utf-8"))
    assert comparison["outcome"] == "AGREED"


def test_b1_evidence_compare_annotations_requires_adjudication(tmp_path: Path) -> None:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    _write_submission(a, "r1", [0])
    _write_submission(b, "r2", [1])
    out = tmp_path / "comparison.json"
    rc = mesc_b1_evidence.main(
        [
            "compare-annotations",
            "--submission-a",
            str(a),
            "--submission-b",
            str(b),
            "--output",
            str(out),
        ]
    )
    assert rc == 0
    comparison = json.loads(out.read_text(encoding="utf-8"))
    assert comparison["outcome"] == "ADJUDICATION_REQUIRED"


def test_b1_evidence_finalize_cues_from_agreement(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    manifest = tmp_path / "subset-manifest.json"
    subset_digest = _write_single_subset_manifest(manifest)
    a = tmp_path / "a.json"
    _write_submission(a, "r1", [0])
    comparison = tmp_path / "comparison.json"
    rc = mesc_b1_evidence.main(
        [
            "compare-annotations",
            "--submission-a",
            str(a),
            "--submission-b",
            str(a),
            "--output",
            str(comparison),
        ]
    )
    assert rc == 0
    pack = tmp_path / "pack.json"
    rc = mesc_b1_evidence.main(
        [
            "finalize-cues",
            "--comparison",
            str(comparison),
            "--source-record",
            str(source),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
            "--subset-digest",
            subset_digest,
            "--subset-manifest",
            str(manifest),
            "--output",
            str(pack),
        ]
    )
    assert rc == 0
    document = json.loads(pack.read_text(encoding="utf-8"))
    assert document["record_count"] == 1
    assert document["schema_version"] == "mesc-pilot-01-b1-evidence-pack/1"
    assert document["cues"][0]["review_status"] == "FINAL"


def test_b1_evidence_finalize_cues_refuses_adjudication_required(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    _write_submission(a, "r1", [0])
    _write_submission(b, "r2", [1])
    comparison = tmp_path / "comparison.json"
    assert (
        mesc_b1_evidence.main(
            [
                "compare-annotations",
                "--submission-a",
                str(a),
                "--submission-b",
                str(b),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    rc = mesc_b1_evidence.main(
        [
            "finalize-cues",
            "--comparison",
            str(comparison),
            "--source-record",
            str(source),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
            "--subset-digest",
            "0" * 64,
            "--subset-manifest",
            str(tmp_path / "manifest.json"),
            "--output",
            str(tmp_path / "pack.json"),
        ]
    )
    assert rc == 2
    assert "human adjudication" in capsys.readouterr().err


def test_b1_evidence_finalize_cues_recomputes_not_trusts_outcome(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    _write_submission(a, "r1", [0])
    _write_submission(b, "r2", [1])
    comparison = tmp_path / "comparison.json"
    assert (
        mesc_b1_evidence.main(
            [
                "compare-annotations",
                "--submission-a",
                str(a),
                "--submission-b",
                str(b),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    document = json.loads(comparison.read_text(encoding="utf-8"))
    assert document["outcome"] == "ADJUDICATION_REQUIRED"
    document["outcome"] = "AGREED"
    comparison.write_text(
        json.dumps(document, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    rc = mesc_b1_evidence.main(
        [
            "finalize-cues",
            "--comparison",
            str(comparison),
            "--source-record",
            str(source),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
            "--subset-digest",
            "0" * 64,
            "--subset-manifest",
            str(tmp_path / "manifest.json"),
            "--output",
            str(tmp_path / "pack.json"),
        ]
    )
    assert rc == 2
    assert "human adjudication" in capsys.readouterr().err


def test_b1_evidence_finalize_cues_from_adjudication(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    manifest = tmp_path / "subset-manifest.json"
    subset_digest = _write_single_subset_manifest(manifest)
    adjudication = tmp_path / "adjudication.json"
    adjudication.write_text(
        json.dumps(
            {
                "reviewer_id": "r3",
                "example_id": "e0",
                "source_document_id": "pmid:1",
                "selected_segment_indices": [0],
                "annotation_status": "AVAILABLE",
            }
        ),
        encoding="utf-8",
    )
    pack = tmp_path / "pack.json"
    rc = mesc_b1_evidence.main(
        [
            "finalize-cues",
            "--adjudication",
            str(adjudication),
            "--source-record",
            str(source),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
            "--subset-digest",
            subset_digest,
            "--subset-manifest",
            str(manifest),
            "--output",
            str(pack),
        ]
    )
    assert rc == 0
    document = json.loads(pack.read_text(encoding="utf-8"))
    assert document["record_count"] == 1
    assert document["cues"][0]["review_status"] == "FINAL"


def test_b1_evidence_finalize_cues_binds_subset_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from medscale.mesc._b1_evidence import (
        load_example_registry_from_bytes,
        select_development_subset,
        write_subset_manifest,
    )

    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    a = tmp_path / "a.json"
    _write_submission(a, "r1", [0])
    comparison = tmp_path / "comparison.json"
    assert (
        mesc_b1_evidence.main(
            [
                "compare-annotations",
                "--submission-a",
                str(a),
                "--submission-b",
                str(a),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    registry_bytes = b"".join(
        json.dumps(
            {
                "schema_version": "mesc-pilot-01-example-registry/1",
                "example_id": f"e{i}",
                "source_document_id": f"pmid:{i + 1}",
                "assigned_split": "validation",
                "partition_key": f"pk-{i}",
                "row_ordinal": i,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
        for i in range(200)
    )
    registry_rows, registry_sha256 = load_example_registry_from_bytes(registry_bytes)
    selection = select_development_subset(
        registry_rows,
        registry_sha256=registry_sha256,
        source_split_fingerprint=_SPLIT_FINGERPRINT,
    )
    manifest = tmp_path / "subset-manifest.json"
    write_subset_manifest(selection, manifest)
    assert "e0" in selection.ordered_selected_example_ids
    args = [
        "finalize-cues",
        "--comparison",
        str(comparison),
        "--source-record",
        str(source),
        "--split-fingerprint",
        _SPLIT_FINGERPRINT,
        "--subset-digest",
        selection.subset_digest,
        "--subset-manifest",
        str(manifest),
        "--output",
        str(tmp_path / "pack.json"),
    ]
    rc = mesc_b1_evidence.main(args)
    assert rc == 2
    assert "exactly" in capsys.readouterr().err
    without_manifest = list(args)
    manifest_flag = without_manifest.index("--subset-manifest")
    del without_manifest[manifest_flag : manifest_flag + 2]
    with pytest.raises(SystemExit):
        mesc_b1_evidence.main(without_manifest)
    bad_digest = list(args)
    bad_digest[bad_digest.index("--subset-digest") + 1] = "0" * 64
    bad_digest[bad_digest.index("--output") + 1] = str(tmp_path / "pack-bad.json")
    rc = mesc_b1_evidence.main(bad_digest)
    assert rc == 2
    assert "does not match the supplied development subset" in capsys.readouterr().err


def test_b1_evidence_finalize_cues_requires_input(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    rc = mesc_b1_evidence.main(
        [
            "finalize-cues",
            "--source-record",
            str(source),
            "--split-fingerprint",
            _SPLIT_FINGERPRINT,
            "--subset-digest",
            "0" * 64,
            "--subset-manifest",
            str(tmp_path / "manifest.json"),
            "--output",
            str(tmp_path / "pack.json"),
        ]
    )
    assert rc == 2
    assert "provide --comparison or --adjudication" in capsys.readouterr().err


def test_b1_evidence_validate_pack(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    manifest = tmp_path / "subset-manifest.json"
    subset_digest = _write_single_subset_manifest(manifest)
    a = tmp_path / "a.json"
    _write_submission(a, "r1", [0])
    comparison = tmp_path / "comparison.json"
    assert (
        mesc_b1_evidence.main(
            [
                "compare-annotations",
                "--submission-a",
                str(a),
                "--submission-b",
                str(a),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    pack = tmp_path / "pack.json"
    assert (
        mesc_b1_evidence.main(
            [
                "finalize-cues",
                "--comparison",
                str(comparison),
                "--source-record",
                str(source),
                "--split-fingerprint",
                _SPLIT_FINGERPRINT,
                "--subset-digest",
                subset_digest,
                "--subset-manifest",
                str(manifest),
                "--output",
                str(pack),
            ]
        )
        == 0
    )
    rc = mesc_b1_evidence.main(
        ["validate-pack", "--pack", str(pack), "--source-record", str(source)]
    )
    assert rc == 0


def test_b1_evidence_validate_pack_rejects_tampered_pack(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_source_records(source)
    manifest = tmp_path / "subset-manifest.json"
    subset_digest = _write_single_subset_manifest(manifest)
    a = tmp_path / "a.json"
    _write_submission(a, "r1", [0])
    comparison = tmp_path / "comparison.json"
    assert (
        mesc_b1_evidence.main(
            [
                "compare-annotations",
                "--submission-a",
                str(a),
                "--submission-b",
                str(a),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    pack = tmp_path / "pack.json"
    assert (
        mesc_b1_evidence.main(
            [
                "finalize-cues",
                "--comparison",
                str(comparison),
                "--source-record",
                str(source),
                "--split-fingerprint",
                _SPLIT_FINGERPRINT,
                "--subset-digest",
                subset_digest,
                "--subset-manifest",
                str(manifest),
                "--output",
                str(pack),
            ]
        )
        == 0
    )
    document = json.loads(pack.read_text(encoding="utf-8"))
    document["pack_sha256"] = "f" * 64
    pack.write_text(json.dumps(document, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    rc = mesc_b1_evidence.main(
        ["validate-pack", "--pack", str(pack), "--source-record", str(source)]
    )
    assert rc == 2
