"""`medscale mesc-b1-eval` — deterministic MESC B1 evidence-cued evaluation.

A narrow research-baseline command. It requires explicit input and evidence-pack
paths with SHA/size attestation, validates every argument before constructing
any runtime, refuses to overwrite an existing output, and performs no model
download, no evidence discovery, and no fallback from missing B1 evidence to
B0. The generator is dependency-injectable so tests exercise validation,
dispatch, and wiring without loading a model.

Exit codes: 2 for usage/configuration errors, 1 for backend/runtime/write
failures, 0 on success.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from medscale.backends.common import BackendError
from medscale.backends.transformers.backend import (
    TransformersTextGenerator,
    build_transformers_runtime,
)
from medscale.backends.transformers.validation import (
    SUPPORTED_DEVICES,
    SUPPORTED_DTYPES,
    TransformersGenerationConfig,
    is_commit_sha,
)
from medscale.cli import _common
from medscale.mesc._b0 import B0Generator
from medscale.mesc._b1 import (
    B1Config,
    B1ConfigError,
    capture_b1_runtime_manifest,
    run_b1,
    validate_b1_config,
    write_b1_report,
)
from medscale.mesc._b1_evidence import (
    B1EvidenceError,
    pack_from_document,
    validate_evidence_pack,
)
from medscale.mesc._pilot_loader import PilotLoaderError, load_b0_inputs_from_path

GeneratorFactory = Callable[[B1Config], B0Generator]

DESCRIPTION = (
    "Run the deterministic MESC B1 manually evidence-cued baseline over an "
    "explicit input file and evidence pack, writing a reproducible report. B1 "
    "is a research baseline only: it performs no training, no retrieval, no "
    "model download, no real split execution, and makes no clinical claim."
)


def _engine_error(message: str) -> int:
    """Print an engine-failure message to stderr and return exit code 1."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def _make_default_factory(device: str, dtype: str) -> GeneratorFactory:
    def factory(config: B1Config) -> B0Generator:
        gen_config = TransformersGenerationConfig(
            model_id=config.model_id,
            model_revision=config.model_revision,
            tokenizer_revision=config.tokenizer_revision,
            max_new_tokens=config.max_new_tokens,
            seed=config.seed,
            device=device,
            dtype=dtype,
        )
        runtime = build_transformers_runtime(gen_config)
        return TransformersTextGenerator(gen_config, runtime=runtime)

    return factory


def _require_hex64(value: str, flag: str) -> int | None:
    if len(value) != 64 or not all(char in "0123456789abcdef" for char in value):
        return _common.fail(f"{flag} must be a full lowercase 64-hex SHA-256")
    return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medscale mesc-b1-eval", description=DESCRIPTION)
    parser.add_argument("--input", dest="input_path", default=None, help="B0 pilot input JSONL")
    parser.add_argument(
        "--input-sha256", dest="input_sha256", default=None, help="exact input SHA-256"
    )
    parser.add_argument(
        "--input-size", dest="input_size", type=int, default=None, help="exact input byte size"
    )
    parser.add_argument(
        "--evidence-pack", dest="pack_path", default=None, help="B1 evidence pack JSON"
    )
    parser.add_argument(
        "--evidence-pack-sha256",
        dest="pack_sha256",
        default=None,
        help="exact evidence pack SHA-256",
    )
    parser.add_argument("--model-id", dest="model_id", default=None, help="approved model id")
    parser.add_argument("--model-revision", dest="model_revision", default=None, help="40-hex SHA")
    parser.add_argument(
        "--tokenizer-revision", dest="tokenizer_revision", default=None, help="40-hex SHA"
    )
    parser.add_argument(
        "--code-commit", dest="code_commit", default=None, help="MedScale 40-hex SHA"
    )
    parser.add_argument("--experiment-version", dest="experiment_version", default="mesc-b1/1")
    parser.add_argument("--max-new-tokens", dest="max_new_tokens", type=int, default=8)
    parser.add_argument("--seed", dest="seed", type=int, default=0)
    parser.add_argument("--device", dest="device", default="cpu")
    parser.add_argument("--dtype", dest="dtype", default="float32")
    parser.add_argument("--output", dest="output_path", default=None, help="report output path")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    generator_factory: GeneratorFactory | None = None,
) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    for value, flag in (
        (args.input_path, "--input"),
        (args.input_sha256, "--input-sha256"),
        (args.input_size, "--input-size"),
        (args.pack_path, "--evidence-pack"),
        (args.pack_sha256, "--evidence-pack-sha256"),
        (args.model_id, "--model-id"),
        (args.model_revision, "--model-revision"),
        (args.tokenizer_revision, "--tokenizer-revision"),
        (args.code_commit, "--code-commit"),
        (args.output_path, "--output"),
    ):
        if value is None:
            return _common.fail(f"{flag} is required")

    if not is_commit_sha(args.code_commit):
        return _common.fail("--code-commit must be a full lowercase 40-hex commit SHA")
    if not is_commit_sha(args.model_revision):
        return _common.fail("--model-revision must be a full lowercase 40-hex commit SHA")
    if not is_commit_sha(args.tokenizer_revision):
        return _common.fail("--tokenizer-revision must be a full lowercase 40-hex commit SHA")
    if args.device not in SUPPORTED_DEVICES:
        return _common.fail(f"--device must be one of {sorted(SUPPORTED_DEVICES)}")
    if args.dtype not in SUPPORTED_DTYPES:
        return _common.fail(f"--dtype must be one of {sorted(SUPPORTED_DTYPES)}")
    for value, flag in (
        (args.input_sha256, "--input-sha256"),
        (args.pack_sha256, "--evidence-pack-sha256"),
    ):
        failure = _require_hex64(value, flag)
        if failure is not None:
            return failure

    input_path = Path(args.input_path)
    pack_path = Path(args.pack_path)
    output_path = Path(args.output_path)
    if not input_path.is_file():
        return _common.fail(f"input file not found: {input_path}")
    if not pack_path.is_file():
        return _common.fail(f"evidence pack file not found: {pack_path}")
    if output_path.exists():
        return _common.fail(
            f"output already exists: {output_path}",
            hint="choose a new --output path; mesc-b1-eval refuses to overwrite results",
        )

    try:
        dataset = load_b0_inputs_from_path(
            input_path, expected_sha256=args.input_sha256, expected_size=args.input_size
        )
        pack = pack_from_document(_load_pack_document(pack_path, args.pack_sha256))
        contexts = {
            (record.example_id, record.source_document_id): record.context
            for record in dataset.records
        }
        validate_evidence_pack(pack, contexts)
    except (PilotLoaderError, B1EvidenceError) as exc:
        return _common.fail(f"invalid input or evidence pack: {exc}")
    except OSError as exc:
        return _common.fail(f"cannot read input or evidence pack: {exc}")

    config = B1Config(
        experiment_version=args.experiment_version,
        model_id=args.model_id,
        model_revision=args.model_revision,
        tokenizer_revision=args.tokenizer_revision,
        max_new_tokens=args.max_new_tokens,
        seed=args.seed,
        evidence_pack_sha256=pack.pack_sha256,
        evidence_pack_size=pack.record_count,
        subset_digest=pack.subset_digest,
    )
    try:
        validate_b1_config(config)
    except B1ConfigError as exc:
        return _common.fail(str(exc))

    manifest = capture_b1_runtime_manifest(
        code_commit=args.code_commit,
        config=config,
        device=args.device,
        dtype=args.dtype,
        quantization="none",
    )

    factory = (
        generator_factory
        if generator_factory is not None
        else _make_default_factory(args.device, args.dtype)
    )
    try:
        generator = factory(config)
        report = run_b1(config, dataset, pack, generator, manifest=manifest)
    except B1ConfigError as exc:
        return _common.fail(str(exc))
    except B1EvidenceError as exc:
        return _common.fail(f"evidence-layer failure: {exc}")
    except BackendError as exc:
        return _engine_error(f"backend error: {exc}")

    try:
        write_b1_report(report, output_path)
    except OSError as exc:
        return _engine_error(f"failed to write report: {exc}")

    print(f"mesc-b1-eval: wrote {output_path}")
    print(f"run_id: {report.run_id}")
    print(
        f"model: {config.model_id}@{config.model_revision}  evidence: {config.evidence_condition}"
    )
    print(
        f"examples: {report.aggregate.total}  parsed: {report.aggregate.parsed_count}  "
        f"correct: {report.aggregate.correct_count}"
    )
    return 0


def _load_pack_document(path: Path, expected_sha256: str) -> dict[str, object]:
    import hashlib
    import json

    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise B1EvidenceError("evidence pack SHA-256 mismatch")
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise B1EvidenceError(f"evidence pack is not valid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise B1EvidenceError("evidence pack must be a JSON object")
    return obj


if __name__ == "__main__":
    raise SystemExit(main())
