"""The sole controlled operator surface for MESC P01-04D (FD-DREADY-3 .. FD-DREADY-5).

This is a canonical repository-controlled script, not an improvised one-off.  It
is deliberately **not** exported from ``medscale.mesc``, **not** registered as a
``medscale`` CLI subcommand, **not** installed as a console script and **not**
reachable through an environment-variable activation switch.

It provides exactly two commands and no third:

``generate``
    Executes exactly one generation per process, identified as ``A`` or ``B``.
    One invocation never executes both.  Every input must be supplied
    explicitly: no protected input path is inferred and no default points at
    P01-03G or any real dataset.

``compare``
    Runs only after both generations have terminated.  It reads both completed
    workspaces, compares every candidate artifact byte-for-byte, verifies the
    authoritative fingerprint and reports the disposition.  It never repairs,
    rewrites, copies, suppresses an inequality, promotes, or writes anything into
    either workspace, and it never performs P01-04E leakage execution.

Running this script does not authorize P01-04D entry or P01-04D execution over
protected inputs.  Those remain separate founder decisions.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(_REPOSITORY_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT / "src"))

from medscale.mesc._formal_generation_v1 import (  # noqa: E402 - after the path bootstrap
    build_request,
    compare,
    generate,
)
from medscale.mesc._formal_split_v1 import (  # noqa: E402 - after the path bootstrap
    DECISION_RECORD_SURFACE,
    GENERATION_IDENTITIES,
    ORDERED_EXAMPLE_REGISTRY_SURFACE,
    SOURCE_DOCUMENT_REGISTRY_SURFACE,
    SOURCE_RECORDS_SURFACE,
    TRANSFORMED_DATASET_IDENTITY_SURFACE,
)

#: Exactly two operator commands. No third command exists on this surface.
COMMANDS: tuple[str, ...] = ("generate", "compare")


def build_parser() -> argparse.ArgumentParser:
    """Return the operator parser. Every path argument is required and explicit."""
    parser = argparse.ArgumentParser(
        prog="mesc_p01_04d_operator",
        description=(
            "Controlled MESC P01-04D formal operator. Running it does not authorize "
            "P01-04D entry or execution over protected inputs."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="{generate,compare}")

    generate_parser = subparsers.add_parser(
        "generate", help="execute exactly one generation, identified as A or B"
    )
    generate_parser.add_argument("--expected-canonical-commit", required=True)
    generate_parser.add_argument("--repository-root", required=True, type=Path)
    generate_parser.add_argument("--generation", required=True, choices=list(GENERATION_IDENTITIES))
    generate_parser.add_argument("--workspace", required=True, type=Path)
    generate_parser.add_argument("--external-evidence-root", required=True, type=Path)
    generate_parser.add_argument("--future-evidence-root", required=True, type=Path)
    generate_parser.add_argument("--ordered-example-registry", required=True, type=Path)
    generate_parser.add_argument("--source-document-registry", required=True, type=Path)
    generate_parser.add_argument("--transformed-dataset-identity", required=True, type=Path)
    generate_parser.add_argument("--source-records", required=True, type=Path)
    generate_parser.add_argument("--decision-record", required=True, type=Path)
    generate_parser.add_argument("--python-version", required=True)

    compare_parser = subparsers.add_parser(
        "compare", help="compare two completed generation workspaces byte-for-byte"
    )
    compare_parser.add_argument("--generation-a-workspace", required=True, type=Path)
    compare_parser.add_argument("--generation-b-workspace", required=True, type=Path)
    return parser


def _run_generate(arguments: argparse.Namespace) -> int:
    request = build_request(
        expected_canonical_commit=arguments.expected_canonical_commit,
        repository_root=arguments.repository_root,
        generation_identity=arguments.generation,
        workspace=arguments.workspace,
        external_evidence_root=arguments.external_evidence_root,
        future_evidence_root=arguments.future_evidence_root,
        input_locations={
            ORDERED_EXAMPLE_REGISTRY_SURFACE: arguments.ordered_example_registry,
            SOURCE_DOCUMENT_REGISTRY_SURFACE: arguments.source_document_registry,
            TRANSFORMED_DATASET_IDENTITY_SURFACE: arguments.transformed_dataset_identity,
            SOURCE_RECORDS_SURFACE: arguments.source_records,
            DECISION_RECORD_SURFACE: arguments.decision_record,
        },
        python_version=arguments.python_version,
    )
    result = generate(request)
    sys.stdout.write(
        f"generation {result.generation_identity} complete: "
        f"{len(result.filenames)} artifacts, fingerprint {result.split_fingerprint}\n"
    )
    # The execution-input-manifest identity is recorded on the existing stdout
    # surface and written to no file: no repository evidence record, no eighth
    # workspace artifact, neither seven-file inventory widened (P-C1a §5.8).
    sys.stdout.write(
        f"execution_input_manifest {result.execution_input_manifest_sha256} "
        f"{result.execution_input_manifest_byte_size}\n"
    )
    return 0


def _run_compare(arguments: argparse.Namespace) -> int:
    result = compare(arguments.generation_a_workspace, arguments.generation_b_workspace)
    sys.stdout.write(
        f"comparison equal: {len(result.equal_filenames)} artifacts byte-identical, "
        f"fingerprint {result.split_fingerprint}\n"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and dispatch. Formal domain errors stay typed and propagate.

    A typed formal failure is never downgraded to a warning or to a successful
    return code: it propagates out of this function, so the process cannot exit
    zero after a refusal.
    """
    parser = build_parser()
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    if arguments.command == "generate":
        return _run_generate(arguments)
    if arguments.command == "compare":
        return _run_compare(arguments)
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
