"""`medscale mesc-b1-evidence` — deterministic P01-05 B1 evidence tooling.

A narrow research-tooling command surface for the ratified B1 supplied-evidence
channel (FD-P01-05-B1-EVIDENCE-1). It supports: ``select-subset``,
``render-annotation-view``, ``validate-submission``, ``compare-annotations``,
``finalize-cues``, and ``validate-pack``.

Every operation requires explicit input/output paths, refuses to overwrite
existing outputs, performs no automatic discovery, performs no network access,
performs no retrieval, never defaults to repository evidence roots, and never
discovers user home/workspace data.

Exit codes: 2 for usage/configuration errors, 1 for runtime/write failures, 0
on success.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from medscale.cli import _common
from medscale.mesc._b1_evidence import (
    B1AdjudicationSubmission,
    B1AnnotationComparison,
    B1AnnotationSubmission,
    B1EvidenceError,
    B1EvidencePack,
    B1SourceRecord,
    DevelopmentSubsetSelection,
    annotation_input_from_source_record,
    build_evidence_pack,
    build_final_cue_from_adjudication,
    build_final_cue_from_agreement,
    compare_annotations,
    load_b1_source_records_from_path,
    load_example_registry_from_path,
    make_adjudication_submission,
    make_annotation_submission,
    pack_from_document,
    render_annotation_view,
    select_development_subset,
    validate_evidence_cue,
    validate_evidence_pack,
    write_evidence_pack,
    write_subset_manifest,
)

DESCRIPTION = (
    "Deterministic P01-05 B1 evidence tooling: label-blind annotation views, "
    "A/B comparison, adjudicated final cues, deterministic subset selection, and "
    "evidence-pack validation. No retrieval, no network access, no model execution."
)


def _require_file(path: Path, label: str) -> None:
    if not path.is_file():
        print(f"error: {label} file not found: {path}", file=sys.stderr)
        raise SystemExit(2)


def _refuse_overwrite(path: Path) -> None:
    if path.exists():
        print(f"error: output already exists: {path}", file=sys.stderr)
        print(
            "hint : choose a new --output path; mesc-b1-evidence refuses to overwrite",
            file=sys.stderr,
        )
        raise SystemExit(2)


def _read_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {label} {path}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    if not isinstance(obj, dict):
        print(f"error: {label} must be a JSON object: {path}", file=sys.stderr)
        raise SystemExit(2)
    return obj


def _write_json(path: Path, document: Mapping[str, object]) -> None:
    path.write_text(
        json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# select-subset
# ---------------------------------------------------------------------------


def _cmd_select_subset(args: argparse.Namespace) -> int:
    registry = Path(args.registry)
    output = Path(args.output)
    _require_file(registry, "registry")
    _refuse_overwrite(output)
    try:
        rows, registry_sha256 = load_example_registry_from_path(registry)
        selection: DevelopmentSubsetSelection = select_development_subset(
            rows,
            registry_sha256=registry_sha256,
            source_split_fingerprint=args.split_fingerprint,
            require_production_counts=args.require_production_counts,
        )
        write_subset_manifest(selection, output)
    except B1EvidenceError as exc:
        return _common.fail(f"invalid registry input: {exc}")
    except OSError as exc:
        print(f"error: failed to write subset manifest: {exc}", file=sys.stderr)
        return 1
    print(f"mesc-b1-evidence select-subset: wrote {output}")
    print(f"validation population: {selection.validation_population}")
    print(f"selected: {selection.selected_count}  subset_digest: {selection.subset_digest}")
    return 0


# ---------------------------------------------------------------------------
# render-annotation-view
# ---------------------------------------------------------------------------


def _cmd_render_annotation_view(args: argparse.Namespace) -> int:
    source = Path(args.source_record)
    output = Path(args.output)
    _require_file(source, "source-record")
    _refuse_overwrite(output)
    try:
        records = load_b1_source_records_from_path(source)
        lines = [
            json.dumps(
                render_annotation_view(annotation_input_from_source_record(record)),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            for record in records
        ]
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except B1EvidenceError as exc:
        return _common.fail(f"invalid source record input: {exc}")
    except OSError as exc:
        print(f"error: failed to write annotation view: {exc}", file=sys.stderr)
        return 1
    print(f"mesc-b1-evidence render-annotation-view: wrote {output}")
    return 0


# ---------------------------------------------------------------------------
# validate-submission
# ---------------------------------------------------------------------------


def _submission_from_document(doc: Mapping[str, object]) -> B1AnnotationSubmission:
    return make_annotation_submission(
        reviewer_id=_required_str(doc, "reviewer_id"),
        example_id=_required_str(doc, "example_id"),
        source_document_id=_required_str(doc, "source_document_id"),
        selected_segment_indices=_required_int_list(doc, "selected_segment_indices"),
        annotation_status=_required_str(doc, "annotation_status"),
    )


def _adjudication_from_document(doc: Mapping[str, object]) -> B1AdjudicationSubmission:
    return make_adjudication_submission(
        reviewer_id=_required_str(doc, "reviewer_id"),
        example_id=_required_str(doc, "example_id"),
        source_document_id=_required_str(doc, "source_document_id"),
        selected_segment_indices=_required_int_list(doc, "selected_segment_indices"),
        annotation_status=_required_str(doc, "annotation_status"),
    )


def _required_str(doc: Mapping[str, object], field: str) -> str:
    value = doc.get(field)
    if not isinstance(value, str):
        print(f"error: {field} must be a string", file=sys.stderr)
        raise SystemExit(2)
    return value


def _required_int_list(doc: Mapping[str, object], field: str) -> list[int]:
    value = doc.get(field)
    if not isinstance(value, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) for item in value
    ):
        print(f"error: {field} must be a list of integers", file=sys.stderr)
        raise SystemExit(2)
    return list(value)


def _required_mapping(doc: Mapping[str, object], field: str) -> Mapping[str, object]:
    value = doc.get(field)
    if not isinstance(value, dict):
        print(f"error: {field} must be a JSON object", file=sys.stderr)
        raise SystemExit(2)
    return value


def _source_record_for(
    records: Sequence[B1SourceRecord], example_id: str, source_document_id: str
) -> B1SourceRecord:
    for record in records:
        if record.example_id == example_id and record.source_document_id == source_document_id:
            return record
    raise B1EvidenceError(f"no source record for ({example_id}, {source_document_id})")


def _cmd_validate_submission(args: argparse.Namespace) -> int:
    submission = Path(args.submission)
    source = Path(args.source_record)
    _require_file(submission, "submission")
    _require_file(source, "source-record")
    try:
        submission_obj = _submission_from_document(_read_json_object(submission, "submission"))
        records = load_b1_source_records_from_path(source)
        record = _source_record_for(
            records, submission_obj.example_id, submission_obj.source_document_id
        )
        cue = build_final_cue_from_agreement(
            B1AnnotationComparison(
                example_id=submission_obj.example_id,
                source_document_id=submission_obj.source_document_id,
                outcome="AGREED",
                submission_a=submission_obj,
                submission_b=submission_obj,
            ),
            source_record=record,
        )
        validate_evidence_cue(cue, record.context)
    except B1EvidenceError as exc:
        return _common.fail(f"invalid submission: {exc}")
    print(
        f"mesc-b1-evidence validate-submission: OK "
        f"({submission_obj.example_id} {submission_obj.annotation_status})"
    )
    return 0


# ---------------------------------------------------------------------------
# compare-annotations
# ---------------------------------------------------------------------------


def _cmd_compare_annotations(args: argparse.Namespace) -> int:
    submission_a = Path(args.submission_a)
    submission_b = Path(args.submission_b)
    output = Path(args.output)
    _require_file(submission_a, "submission-a")
    _require_file(submission_b, "submission-b")
    _refuse_overwrite(output)
    try:
        a = _submission_from_document(_read_json_object(submission_a, "submission-a"))
        b = _submission_from_document(_read_json_object(submission_b, "submission-b"))
        comparison = compare_annotations(a, b)
        document = {
            "schema_version": "mesc-pilot-01-b1-annotation-comparison/1",
            "example_id": comparison.example_id,
            "source_document_id": comparison.source_document_id,
            "outcome": comparison.outcome,
            "submission_a": _submission_document(a),
            "submission_b": _submission_document(b),
        }
        _write_json(output, document)
    except B1EvidenceError as exc:
        return _common.fail(f"invalid comparison input: {exc}")
    except OSError as exc:
        print(f"error: failed to write comparison: {exc}", file=sys.stderr)
        return 1
    print(f"mesc-b1-evidence compare-annotations: wrote {output}")
    print(f"outcome: {comparison.outcome}")
    return 0


def _submission_document(submission: B1AnnotationSubmission) -> dict[str, object]:
    return {
        "reviewer_id": submission.reviewer_id,
        "example_id": submission.example_id,
        "source_document_id": submission.source_document_id,
        "selected_segment_indices": list(submission.selected_segment_indices),
        "annotation_status": submission.annotation_status,
        "annotation_protocol_version": submission.annotation_protocol_version,
    }


# ---------------------------------------------------------------------------
# finalize-cues
# ---------------------------------------------------------------------------


def _cmd_finalize_cues(args: argparse.Namespace) -> int:
    source = Path(args.source_record)
    output = Path(args.output)
    _require_file(source, "source-record")
    _refuse_overwrite(output)
    try:
        records = load_b1_source_records_from_path(source)
        by_key = {(record.example_id, record.source_document_id): record for record in records}
        submissions: dict[tuple[str, str], B1AnnotationSubmission | B1AdjudicationSubmission] = {}
        if args.comparison is not None:
            comparison_path = Path(args.comparison)
            _require_file(comparison_path, "comparison")
            comparison = _read_json_object(comparison_path, "comparison")
            if comparison.get("outcome") != "AGREED":
                raise B1EvidenceError(
                    "cannot finalize a comparison that is not AGREED; "
                    "human adjudication is required"
                )
            a = _submission_from_document(_required_mapping(comparison, "submission_a"))
            b = _submission_from_document(_required_mapping(comparison, "submission_b"))
            key = (a.example_id, a.source_document_id)
            if key != (b.example_id, b.source_document_id):
                raise B1EvidenceError("comparison submissions disagree on example identity")
            submissions[key] = a
        if args.adjudication is not None:
            adjudication_path = Path(args.adjudication)
            _require_file(adjudication_path, "adjudication")
            adjudication = _adjudication_from_document(
                _read_json_object(adjudication_path, "adjudication")
            )
            key = (adjudication.example_id, adjudication.source_document_id)
            if key in submissions:
                raise B1EvidenceError(f"duplicate finalization source for {key}")
            submissions[key] = adjudication
        if not submissions:
            raise B1EvidenceError("provide --comparison or --adjudication")
        cues = []
        for key in sorted(submissions):
            submission = submissions[key]
            record = by_key.get(key)
            if record is None:
                raise B1EvidenceError(f"no source record for {key}")
            if isinstance(submission, B1AdjudicationSubmission):
                cues.append(build_final_cue_from_adjudication(submission, source_record=record))
            else:
                cues.append(
                    build_final_cue_from_agreement(
                        B1AnnotationComparison(
                            example_id=submission.example_id,
                            source_document_id=submission.source_document_id,
                            outcome="AGREED",
                            submission_a=submission,
                            submission_b=submission,
                        ),
                        source_record=record,
                    )
                )
        pack: B1EvidencePack = build_evidence_pack(
            cues,
            source_split_fingerprint=args.split_fingerprint,
            subset_digest=args.subset_digest,
        )
        write_evidence_pack(pack, output)
    except B1EvidenceError as exc:
        return _common.fail(f"invalid finalization input: {exc}")
    except OSError as exc:
        print(f"error: failed to write evidence pack: {exc}", file=sys.stderr)
        return 1
    print(f"mesc-b1-evidence finalize-cues: wrote {output}")
    print(f"record_count: {pack.record_count}  pack_sha256: {pack.pack_sha256}")
    return 0


# ---------------------------------------------------------------------------
# validate-pack
# ---------------------------------------------------------------------------


def _cmd_validate_pack(args: argparse.Namespace) -> int:
    pack_path = Path(args.pack)
    source = Path(args.source_record)
    _require_file(pack_path, "pack")
    _require_file(source, "source-record")
    try:
        pack = pack_from_document(_read_json_object(pack_path, "pack"))
        records = load_b1_source_records_from_path(source)
        contexts = {
            (record.example_id, record.source_document_id): record.context for record in records
        }
        validate_evidence_pack(pack, contexts)
    except B1EvidenceError as exc:
        return _common.fail(f"invalid evidence pack: {exc}")
    print(f"mesc-b1-evidence validate-pack: OK ({pack.record_count} cues)")
    return 0


# ---------------------------------------------------------------------------
# parser / entry
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medscale mesc-b1-evidence", description=DESCRIPTION)
    sub = parser.add_subparsers(dest="command", required=True)

    sel = sub.add_parser("select-subset", help="deterministic development-subset selection")
    sel.add_argument(
        "--registry", required=True, help="P01-04 example registry JSONL (explicit path)"
    )
    sel.add_argument("--output", required=True, help="subset manifest output path")
    sel.add_argument("--split-fingerprint", required=True, help="P01-04 split fingerprint")
    sel.add_argument(
        "--require-production-counts",
        action="store_true",
        help="require validation population 150 and selected 100",
    )
    sel.set_defaults(func=_cmd_select_subset)

    view = sub.add_parser("render-annotation-view", help="render label-blind annotation views")
    view.add_argument("--source-record", required=True, help="label-free source-record JSONL")
    view.add_argument("--output", required=True, help="annotation view JSONL output path")
    view.set_defaults(func=_cmd_render_annotation_view)

    val = sub.add_parser("validate-submission", help="validate one annotation submission")
    val.add_argument("--submission", required=True, help="submission JSON path")
    val.add_argument("--source-record", required=True, help="label-free source-record JSONL")
    val.set_defaults(func=_cmd_validate_submission)

    cmp = sub.add_parser("compare-annotations", help="deterministic A/B comparison")
    cmp.add_argument("--submission-a", required=True, help="annotator A submission JSON")
    cmp.add_argument("--submission-b", required=True, help="annotator B submission JSON")
    cmp.add_argument("--output", required=True, help="comparison JSON output path")
    cmp.set_defaults(func=_cmd_compare_annotations)

    fin = sub.add_parser("finalize-cues", help="build final cues from agreement/adjudication")
    fin.add_argument("--comparison", default=None, help="AGREED comparison JSON path")
    fin.add_argument("--adjudication", default=None, help="adjudication submission JSON path")
    fin.add_argument("--source-record", required=True, help="label-free source-record JSONL")
    fin.add_argument("--split-fingerprint", required=True, help="P01-04 split fingerprint")
    fin.add_argument("--subset-digest", required=True, help="development-subset digest")
    fin.add_argument("--output", required=True, help="evidence pack JSON output path")
    fin.set_defaults(func=_cmd_finalize_cues)

    pack = sub.add_parser("validate-pack", help="validate a final evidence pack")
    pack.add_argument("--pack", required=True, help="evidence pack JSON path")
    pack.add_argument("--source-record", required=True, help="label-free source-record JSONL")
    pack.set_defaults(func=_cmd_validate_pack)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except SystemExit as exc:
        return int(exc.code or 0)


if __name__ == "__main__":
    raise SystemExit(main())
