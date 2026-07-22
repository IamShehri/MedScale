"""`medscale mesc-eval` — deterministic MESC B0 zero-shot evaluation.

A narrow research-baseline command. It validates every argument before
constructing any runtime, refuses to overwrite an existing output, uses
local-files-only deterministic generation, and makes no training, retrieval,
clinical-deployment, or real-split claim. The generator is dependency-injectable
so tests exercise validation, dispatch, and wiring without loading a model.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from medscale.backends.common import BackendError
from medscale.backends.transformers.backend import (
    TransformersTextGenerator,
    build_transformers_runtime,
)
from medscale.backends.transformers.validation import TransformersGenerationConfig
from medscale.cli import _common
from medscale.mesc._b0 import (
    B0Config,
    B0ConfigError,
    B0Generator,
    run_b0,
    validate_b0_config,
    write_b0_report,
)
from medscale.mesc._pilot_loader import PilotLoaderError, load_b0_inputs_from_path

GeneratorFactory = Callable[[B0Config], B0Generator]

DESCRIPTION = (
    "Run the deterministic MESC B0 zero-shot baseline over an explicit input file "
    "and write a reproducible report. B0 is a research baseline only: it performs no "
    "training, no retrieval, no real split execution, and makes no clinical claim."
)


def _default_generator_factory(config: B0Config) -> B0Generator:
    gen_config = TransformersGenerationConfig(
        model_id=config.model_id,
        revision=config.model_revision,
        max_new_tokens=config.max_new_tokens,
        seed=config.seed,
    )
    runtime = build_transformers_runtime(gen_config)
    return TransformersTextGenerator(gen_config, runtime=runtime)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medscale mesc-eval", description=DESCRIPTION)
    parser.add_argument("--input", dest="input_path", default=None, help="B0 input JSONL file")
    parser.add_argument("--output", dest="output_path", default=None, help="report output path")
    parser.add_argument("--model-id", dest="model_id", default=None, help="approved model id")
    parser.add_argument("--model-revision", dest="model_revision", default=None)
    parser.add_argument("--tokenizer-revision", dest="tokenizer_revision", default=None)
    parser.add_argument("--experiment-version", dest="experiment_version", default="mesc-b0/1")
    parser.add_argument("--max-new-tokens", dest="max_new_tokens", type=int, default=8)
    parser.add_argument("--seed", dest="seed", type=int, default=0)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    generator_factory: GeneratorFactory | None = None,
) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    for value, flag in (
        (args.input_path, "--input"),
        (args.output_path, "--output"),
        (args.model_id, "--model-id"),
        (args.model_revision, "--model-revision"),
        (args.tokenizer_revision, "--tokenizer-revision"),
    ):
        if value is None:
            return _common.fail(f"{flag} is required")

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    if not input_path.is_file():
        return _common.fail(f"input file not found: {input_path}")
    if output_path.exists():
        return _common.fail(
            f"output already exists: {output_path}",
            hint="choose a new --output path; mesc-eval refuses to overwrite results",
        )

    config = B0Config(
        experiment_version=args.experiment_version,
        model_id=args.model_id,
        model_revision=args.model_revision,
        tokenizer_revision=args.tokenizer_revision,
        max_new_tokens=args.max_new_tokens,
        seed=args.seed,
    )
    try:
        validate_b0_config(config)
    except B0ConfigError as exc:
        return _common.fail(str(exc))

    try:
        dataset = load_b0_inputs_from_path(input_path)
    except PilotLoaderError as exc:
        return _common.fail(f"invalid B0 input: {exc}")

    factory = generator_factory if generator_factory is not None else _default_generator_factory
    try:
        generator = factory(config)
        report = run_b0(config, dataset, generator)
    except BackendError as exc:
        return _common.fail(f"backend error: {exc}")

    write_b0_report(report, output_path)
    print(f"mesc-eval: wrote {output_path}")
    print(f"run_id: {report.run_id}")
    print(
        f"model: {config.model_id}@{config.model_revision}  evidence: {config.evidence_condition}"
    )
    print(
        f"examples: {report.aggregate.total}  parsed: {report.aggregate.parsed_count}  "
        f"correct: {report.aggregate.correct_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
