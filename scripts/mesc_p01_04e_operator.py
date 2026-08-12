"""Sole controlled operator surface for MESC P01-04E (FD-E-CTX-1).

This is a canonical repository-controlled script, deliberately **not** exported
from ``medscale.mesc``, **not** registered as a ``medscale`` CLI subcommand,
**not** installed as a console script and **not** reachable through an
environment-variable activation switch.

It provides exactly one command:

``audit``
    Verifies every input identity, loads only the required record surfaces,
    delegates to the pure orchestration module, optionally applies a
    classification ledger, and writes the canonical ``leakage-audit.json``
    exactly once to a fresh audit workspace.

Running this script does not authorize P01-04E execution over protected
scientific content.  That remains a separate founder decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(_REPOSITORY_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT / "src"))

from medscale.mesc._leakage_audit_v1 import (  # noqa: E402
    AuditSourceRecord,
    ClassificationLedgerError,
    LeakageAuditContractError,
    SourceRecordIdentity,
    SplitIdentityBundle,
    canonical_audit_bytes,
    run_leakage_audit,
)

COMMANDS: tuple[str, ...] = ("audit",)

_LOWERCASE_HEX = frozenset("0123456789abcdef")
_SHA256_LEN = 64
_COMMIT_LEN = 40

_EXPECTED_CANONICAL_MAIN = "5888cbad58126096013bc4b4680b6b1e5a82bc14"

# ---------------------------------------------------------------------------
# Operator errors
# ---------------------------------------------------------------------------


class OperatorError(Exception):
    """Private operator fail-closed refusal."""


# ---------------------------------------------------------------------------
# Identity verification
# ---------------------------------------------------------------------------


def _require_sha256(value: object, field: str) -> str:
    if type(value) is not str or len(value) != _SHA256_LEN:
        raise OperatorError(f"{field} must be 64 lowercase hex")
    if any(ch not in _LOWERCASE_HEX for ch in value):
        raise OperatorError(f"{field} must be lowercase hex")
    return value


def _require_commit(value: object) -> str:
    if type(value) is not str or len(value) != _COMMIT_LEN:
        raise OperatorError(f"expected commit must be {_COMMIT_LEN} hex chars")
    if any(ch not in _LOWERCASE_HEX for ch in value):
        raise OperatorError("expected commit must be lowercase hex")
    return value


def _require_non_negative_int(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise OperatorError(f"{field} must be a non-negative integer")
    return value


def _verify_identity(
    actual_sha256: str, expected_sha256: str, actual_size: int, expected_size: int, surface: str
) -> None:
    """Fail closed when a consumed input diverges from its canonical identity.

    The audit binds to the canonical P01-04D split and source-record inputs
    supplied at invocation time; any divergence is a refusal, never a
    reclassification or silent tolerance.
    """
    if actual_sha256 != expected_sha256:
        raise OperatorError(f"{surface} sha256 {actual_sha256} != expected {expected_sha256}")
    if actual_size != expected_size:
        raise OperatorError(f"{surface} byte_size {actual_size} != expected {expected_size}")


def _sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_repository_commit(repository_root: Path) -> str:
    """Read the checked-out commit by reading Git ref files, never invoking Git."""
    git_entry = repository_root / ".git"
    if git_entry.is_file():
        pointer = git_entry.read_text(encoding="utf-8").strip()
        if not pointer.startswith("gitdir:"):
            raise OperatorError("repository .git file is not a gitdir pointer")
        git_dir = Path(pointer.split(":", 1)[1].strip())
        if not git_dir.is_absolute():
            git_dir = (repository_root / git_dir).resolve()
    elif git_entry.is_dir():
        git_dir = git_entry
    else:
        raise OperatorError(f"{repository_root} is not a Git repository")

    head_file = git_dir / "HEAD"
    if not head_file.is_file():
        raise OperatorError("repository HEAD is missing")
    head = head_file.read_text(encoding="utf-8").strip()
    if not head.startswith("ref:"):
        return _require_commit(head)

    ref_name = head.split(":", 1)[1].strip()
    common_dir = git_dir
    common_file = git_dir / "commondir"
    if common_file.is_file():
        common = Path(common_file.read_text(encoding="utf-8").strip())
        common_dir = common if common.is_absolute() else (git_dir / common).resolve()
    for base in (git_dir, common_dir):
        candidate = base / Path(ref_name)
        if candidate.is_file():
            return _require_commit(candidate.read_text(encoding="utf-8").strip())
    packed = common_dir / "packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or line.startswith("^") or " " not in line:
                continue
            commit_val, name = line.split(" ", 1)
            if name.strip() == ref_name:
                return _require_commit(commit_val.strip())
    raise OperatorError(f"repository reference {ref_name!r} could not be resolved")


def _verify_repository_identity(repository_root: Path) -> None:
    actual = _resolve_repository_commit(repository_root)
    if actual != _EXPECTED_CANONICAL_MAIN:
        raise OperatorError(
            f"repository is at {actual!r}, not the expected {_EXPECTED_CANONICAL_MAIN!r}"
        )


# ---------------------------------------------------------------------------
# JSONL parsing (minimal, operator-local)
# ---------------------------------------------------------------------------


def _decode_utf8(payload: bytes, surface: str) -> str:
    if not isinstance(payload, bytes):
        raise OperatorError(f"{surface} payload must be bytes")
    if payload.startswith(b"\xef\xbb\xbf"):
        raise OperatorError(f"{surface} must not begin with a BOM")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OperatorError(f"{surface} is not valid UTF-8") from exc


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise OperatorError(f"duplicate JSON object key: {key!r}")
        seen.add(key)
    return dict(pairs)


def _parse_jsonl(text: str, surface: str) -> tuple[Mapping[str, object], ...]:
    if text == "":
        raise OperatorError(f"{surface} must contain at least one record")
    if not text.endswith("\n"):
        raise OperatorError(f"{surface} must end with exactly one line feed")
    if "\r" in text:
        raise OperatorError(f"{surface} must use LF terminators only")
    records: list[Mapping[str, object]] = []
    for index, line in enumerate(text[:-1].split("\n")):
        if line.strip() == "":
            raise OperatorError(f"{surface} record {index} is blank")
        try:
            value = json.loads(line, object_pairs_hook=_no_duplicate_keys)
        except ValueError as exc:
            raise OperatorError(f"{surface} record {index} is not valid JSON") from exc
        if not isinstance(value, dict):
            raise OperatorError(f"{surface} record {index} must be a JSON object")
        records.append(value)
    return tuple(records)


def _parse_json_object(text: str, surface: str) -> Mapping[str, object]:
    try:
        value = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except ValueError as exc:
        raise OperatorError(f"{surface} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise OperatorError(f"{surface} must be a JSON object")
    return value


def _exact_str(record: Mapping[str, object], key: str, surface: str) -> str:
    value = record.get(key)
    if type(value) is not str or value == "" or value.strip() != value:
        raise OperatorError(f"{surface}.{key} must be a non-blank untrimmed string")
    return value


# ---------------------------------------------------------------------------
# Input loading
# ---------------------------------------------------------------------------


def _load_example_registry(
    path: Path,
) -> tuple[Mapping[str, str], Mapping[str, str], int, bytes]:
    """Return ``{source_document_id: assigned_split}`` plus size and raw bytes.

    Also builds ``{source_document_id: example_id}`` for finding identity later.
    """
    raw = path.read_bytes()
    text = _decode_utf8(raw, "example-registry")
    records = _parse_jsonl(text, "example-registry")

    sd_to_partition: dict[str, str] = {}
    sd_to_example_id: dict[str, str] = {}
    for index, record in enumerate(records):
        surface = f"example-registry[{index}]"
        assigned_split = _exact_str(record, "assigned_split", surface)
        source_document_id = _exact_str(record, "source_document_id", surface)
        example_id = _exact_str(record, "example_id", surface)
        if assigned_split not in ("train", "validation", "test"):
            raise OperatorError(f"{surface}.assigned_split unknown: {assigned_split!r}")
        if source_document_id in sd_to_partition:
            raise OperatorError(
                f"duplicate source_document_id in example registry: {source_document_id!r}"
            )
        sd_to_partition[source_document_id] = assigned_split
        sd_to_example_id[source_document_id] = example_id

    return (
        MappingProxyType(sd_to_partition),
        MappingProxyType(sd_to_example_id),
        len(raw),
        raw,
    )


def _load_source_records(path: Path) -> tuple[tuple[AuditSourceRecord, ...], int, bytes]:
    """Load the source-records envelope, returning typed records, size, raw bytes.

    Only the P01-04E audit surfaces are retained: identity fields, question and
    context segments.  All other scientific fields are discarded immediately.
    """
    raw = path.read_bytes()
    text = _decode_utf8(raw, "source-records")
    envelopes = _parse_jsonl(text, "source-records")

    records: list[AuditSourceRecord] = []
    for index, envelope in enumerate(envelopes):
        surface = f"source-records[{index}]"
        record = envelope.get("record")
        if not isinstance(record, dict):
            raise OperatorError(f"{surface}.record must be a JSON object")

        original_example_id = _exact_str(record, "original_example_id", surface)
        source_document_id = _exact_str(record, "source_document_id", surface)
        question = _exact_str(record, "question", surface)
        schema_version = _exact_str(record, "schema_version", surface)
        if schema_version != "mesc-pubmedqa-source/1":
            raise OperatorError(f"{surface}.schema_version must be mesc-pubmedqa-source/1")

        context_segments = record.get("context_segments")
        if not isinstance(context_segments, list) or not context_segments:
            raise OperatorError(f"{surface}.context_segments must be a non-empty list")
        for si, seg in enumerate(context_segments):
            if type(seg) is not str:
                raise OperatorError(f"{surface}.context_segments[{si}] must be a string")

        records.append(
            AuditSourceRecord(
                example_id="",
                original_example_id=original_example_id,
                source_document_id=source_document_id,
                partition="",
                question=question,
                context_segments=tuple(context_segments),
            )
        )

    return tuple(records), len(raw), raw


def _join_and_build_records(
    source_records: tuple[AuditSourceRecord, ...],
    sd_to_partition: Mapping[str, str],
    sd_to_example_id: Mapping[str, str],
) -> tuple[AuditSourceRecord, ...]:
    """Join source records to partition membership and build audit records."""
    records: list[AuditSourceRecord] = []
    for sr in source_records:
        sdid = sr.source_document_id
        if sdid not in sd_to_partition:
            raise OperatorError(
                f"source record source_document_id {sdid!r} not found in example registry"
            )
        partition = sd_to_partition[sdid]
        example_id = sd_to_example_id[sdid]
        records.append(
            AuditSourceRecord(
                example_id=example_id,
                original_example_id=sr.original_example_id,
                source_document_id=sdid,
                partition=partition,
                question=sr.question,
                context_segments=sr.context_segments,
            )
        )
    return tuple(records)


# ---------------------------------------------------------------------------
# Classification ledger loading
# ---------------------------------------------------------------------------


def _load_classification_ledger(path: Path | None) -> tuple[dict[str, object], ...] | None:
    if path is None:
        return None
    raw = path.read_bytes()
    text = _decode_utf8(raw, "classification-ledger")
    try:
        value = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except ValueError as exc:
        raise OperatorError("classification-ledger is not valid JSON") from exc
    if not isinstance(value, list):
        raise OperatorError("classification-ledger must be a JSON array")
    return tuple(value)


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------


def _is_within(candidate: Path, ancestor: Path) -> bool:
    return candidate == ancestor or ancestor.parts == candidate.parts[: len(ancestor.parts)]


def _validate_audit_workspace(
    workspace: Path,
    repository_root: Path,
    example_registry_path: Path,
    source_records_path: Path,
) -> None:
    """Refuse unsafe destination configurations."""
    if _is_within(workspace, repository_root):
        raise OperatorError("audit workspace must be outside the repository root")
    if _is_within(repository_root, workspace):
        raise OperatorError("the repository root must not be inside the workspace")
    if workspace.exists() or workspace.is_symlink():
        raise OperatorError(f"audit workspace already exists: {workspace}")
    parent = workspace.parent
    if not parent.is_dir():
        raise OperatorError(f"workspace parent does not exist: {parent}")
    # The P01-04D workspace is the directory that holds the accepted artifacts;
    # containment is judged against that directory, never against a file path.
    if _is_within(workspace, example_registry_path.parent):
        raise OperatorError("audit workspace must not be inside the P01-04D workspace")
    if _is_within(workspace, source_records_path.parent):
        raise OperatorError("audit workspace must not be inside the source-records directory")


# ---------------------------------------------------------------------------
# Command dispatch
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mesc_p01_04e_operator",
        description=(
            "Controlled MESC P01-04E formal leakage-audit operator. "
            "Running it does not authorize P01-04E execution over protected "
            "scientific content."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="{audit}")

    audit_parser = subparsers.add_parser("audit", help="execute the P01-04E leakage audit")
    audit_parser.add_argument("--repository-root", required=True, type=Path)
    audit_parser.add_argument("--episode-identity", required=True)
    audit_parser.add_argument("--expected-split-fingerprint", required=True)
    audit_parser.add_argument("--expected-generation-manifest-sha256", required=True)
    audit_parser.add_argument("--expected-generation-manifest-byte-size", required=True, type=int)
    audit_parser.add_argument("--expected-example-registry-sha256", required=True)
    audit_parser.add_argument("--expected-example-registry-byte-size", required=True, type=int)
    audit_parser.add_argument("--expected-source-records-sha256", required=True)
    audit_parser.add_argument("--expected-source-records-byte-size", required=True, type=int)
    audit_parser.add_argument("--example-registry", required=True, type=Path)
    audit_parser.add_argument("--generation-manifest", required=True, type=Path)
    audit_parser.add_argument("--source-records", required=True, type=Path)
    audit_parser.add_argument("--audit-workspace", required=True, type=Path)
    audit_parser.add_argument("--classification-ledger", type=Path, default=None)
    return parser


def _run_audit(arguments: argparse.Namespace) -> int:
    repository_root = arguments.repository_root.resolve()
    example_registry_path = arguments.example_registry.resolve()
    source_records_path = arguments.source_records.resolve()
    audit_workspace = arguments.audit_workspace.resolve()
    generation_manifest_path = arguments.generation_manifest.resolve()
    episode_identity = _require_sha256(arguments.episode_identity, "episode-identity")
    expected_fingerprint = _require_sha256(
        arguments.expected_split_fingerprint, "expected-split-fingerprint"
    )
    expected_gm_sha256 = _require_sha256(
        arguments.expected_generation_manifest_sha256, "expected-generation-manifest-sha256"
    )
    expected_gm_size = _require_non_negative_int(
        arguments.expected_generation_manifest_byte_size,
        "expected-generation-manifest-byte-size",
    )
    expected_er_sha256 = _require_sha256(
        arguments.expected_example_registry_sha256, "expected-example-registry-sha256"
    )
    expected_er_size = _require_non_negative_int(
        arguments.expected_example_registry_byte_size, "expected-example-registry-byte-size"
    )
    expected_sr_sha256 = _require_sha256(
        arguments.expected_source_records_sha256, "expected-source-records-sha256"
    )
    expected_sr_size = _require_non_negative_int(
        arguments.expected_source_records_byte_size, "expected-source-records-byte-size"
    )
    ledger_path: Path | None = (
        arguments.classification_ledger.resolve()
        if arguments.classification_ledger is not None
        else None
    )

    if not repository_root.is_dir():
        raise OperatorError(f"repository root is not a directory: {repository_root}")

    _verify_repository_identity(repository_root)

    # --- Load and verify example-registry.jsonl ---
    if not example_registry_path.is_file():
        raise OperatorError(f"example-registry not found: {example_registry_path}")
    sd_to_partition, sd_to_example_id, er_size, er_raw = _load_example_registry(
        example_registry_path
    )
    er_sha256 = hashlib.sha256(er_raw).hexdigest()
    _verify_identity(er_sha256, expected_er_sha256, er_size, expected_er_size, "example-registry")

    # --- Load and verify generation-manifest.json ---
    if not generation_manifest_path.is_file():
        raise OperatorError(f"generation-manifest not found: {generation_manifest_path}")
    gm_raw = generation_manifest_path.read_bytes()
    gm_sha256 = hashlib.sha256(gm_raw).hexdigest()
    gm_size = len(gm_raw)
    _verify_identity(
        gm_sha256, expected_gm_sha256, gm_size, expected_gm_size, "generation-manifest"
    )
    gm_text = _decode_utf8(gm_raw, "generation-manifest")
    gm_doc = _parse_json_object(gm_text, "generation-manifest")
    manifest_fingerprint = gm_doc.get("split_fingerprint")
    if manifest_fingerprint != expected_fingerprint:
        raise OperatorError(
            f"generation-manifest split_fingerprint "
            f"{manifest_fingerprint!r} != expected {expected_fingerprint!r}"
        )

    # --- Load and verify source-records.jsonl ---
    if not source_records_path.is_file():
        raise OperatorError(f"source-records not found: {source_records_path}")
    parsed_records, sr_size, sr_raw = _load_source_records(source_records_path)
    sr_sha256 = hashlib.sha256(sr_raw).hexdigest()
    _verify_identity(sr_sha256, expected_sr_sha256, sr_size, expected_sr_size, "source-records")

    # --- Build identity bundles ---
    split_identity = SplitIdentityBundle(
        episode_identity=episode_identity,
        split_fingerprint=expected_fingerprint,
        generation_manifest_sha256=gm_sha256,
        generation_manifest_byte_size=gm_size,
        example_registry_sha256=er_sha256,
        example_registry_byte_size=er_size,
    )
    source_records_identity = SourceRecordIdentity(
        sha256=sr_sha256,
        byte_size=sr_size,
    )

    # --- Validate workspace safety ---
    _validate_audit_workspace(
        audit_workspace, repository_root, example_registry_path, source_records_path
    )

    # --- Join and build records ---
    records = _join_and_build_records(parsed_records, sd_to_partition, sd_to_example_id)

    # --- Load classification ledger ---
    ledger = _load_classification_ledger(ledger_path)

    # --- Run audit ---
    findings = run_leakage_audit(records, ledger)

    # --- Build canonical audit bytes ---
    audit_bytes = canonical_audit_bytes(findings, split_identity, source_records_identity)

    # --- Write once ---
    audit_workspace.mkdir(parents=False, exist_ok=False)
    output_file = audit_workspace / "leakage-audit.json"
    with output_file.open("xb") as handle:
        handle.write(audit_bytes)

    # --- Verify output ---
    written = output_file.read_bytes()
    if written != audit_bytes:
        raise OperatorError("leakage-audit.json read-back mismatch")
    written_sha256 = hashlib.sha256(written).hexdigest()

    leaked = any(f.classification in ("unresolved", "confirmed_leakage") for f in findings)
    sys.stdout.write(
        f"audit complete: {len(findings)} findings, "
        f"leaked={'true' if leaked else 'false'}, "
        f"output sha256={written_sha256}, "
        f"output size={len(written)}\n"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    if arguments.command == "audit":
        try:
            return _run_audit(arguments)
        except (OperatorError, LeakageAuditContractError, ClassificationLedgerError) as exc:
            sys.stderr.write(f"audit failed: {exc}\n")
            return 1
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
