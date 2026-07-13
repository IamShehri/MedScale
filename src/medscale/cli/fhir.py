import json
from pathlib import Path

import click

from medscale.fhirkit.report import load_report_from_json, report_to_json
from medscale.fhirkit.storage import store_report
from medscale.fhirkit.validate import validate_fhir


@click.group("fhir")
def fhir_group() -> None:
    """Read-only FHIR boundary commands."""


@fhir_group.command("validate")
@click.argument("input_file", type=click.Path(path_type=Path, exists=True))
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False),
    default="data/fhirkit",
    show_default=True,
)
@click.option("--with-validator", "validator_command", default=None)
@click.option("--created-at", default=None)
@click.option("--summary-only", is_flag=True, default=False)
@click.pass_context
def validate_fhir_command(
    context: click.Context,
    input_file: Path,
    output_dir: str,
    validator_command: str | None,
    created_at: str | None,
    summary_only: bool,
) -> None:
    """Validate a local FHIR JSON object and store the deterministic report."""
    try:
        payload = json.loads(input_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        click.echo(f"input read error: {exc}", err=True)
        context.exit(1)

    if summary_only:
        click.echo(json.dumps(payload, sort_keys=True, ensure_ascii=False))
        return

    command = (
        validator_command.split()
        if isinstance(validator_command, str)
        and validator_command.strip()
        else None
    )
    report = validate_fhir(payload, created_at=created_at)
    if command:
        try:
            from medscale.fhirkit.validate import validate_fhir_with_validator

            report = validate_fhir_with_validator(
                payload, command=command, created_at=created_at
            )
        except Exception as exc:
            click.echo(f"validator error: {exc}", err=True)
            context.exit(1)

    path = store_report(report, root=Path(output_dir))
    click.echo(report_to_json(load_report_from_json(report_to_json(report))))
    click.echo(f"report stored at: {path}", err=True)
