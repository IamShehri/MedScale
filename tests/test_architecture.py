"""Architecture enforcement: the accepted layering, verified on every test run.

These tests parse real import statements from ``src/medscale`` and fail the build when
someone adds an edge the architecture forbids (ADR-0012 layers; the stabilization
sprint's transport isolation and storage-abstraction rules). Layering decays silently
without enforcement — the audit found one inversion that lived for weeks; this makes
the next one live for zero commits.
"""

from __future__ import annotations

import re
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src" / "medscale"
_IMPORT = re.compile(r"^from medscale(?P<dotted>\.[\w.]+)? import", re.MULTILINE)

#: Layer number per top-level unit. Imports may only point at strictly usable layers.
_LAYER: dict[str, int] = {
    # spine (importable by everyone)
    "__about__": 0,
    "_layout": 0,
    "_runtime": 0,
    "reproducibility": 0,
    "provenance": 0,
    # knowledge
    "litdb": 1,
    # evidence
    "evidence": 2,
    "evidence_store": 2,
    "evidence_checks": 2,
    "extraction": 2,
    # parallel capability layer (AI infrastructure)
    "modelkit": 2,
    "backends": 2,
    "fhirkit": 2,
    # collaboration
    "collaboration": 2,
    # research intelligence
    "research": 3,
    # dataset artifacts
    "dataset": 3,
    # benchmarks
    "bench": 4,
    # MESC experiment and evaluation orchestration
    "mesc": 4,
    # public facade
    "workspace": 5,
    # transports
    "cli": 6,
}


def _unit_of(module_path: Path) -> str:
    relative = module_path.relative_to(_SRC)
    return relative.parts[0].removesuffix(".py")


def _imports_of(module_path: Path) -> set[str]:
    text = module_path.read_text(encoding="utf-8")
    units: set[str] = set()
    for match in _IMPORT.finditer(text):
        dotted = match.group("dotted")
        if dotted is None:
            units.add("__root__")  # `from medscale import ...`
        else:
            units.add(dotted.lstrip(".").split(".")[0])
    return units


def _all_modules() -> list[Path]:
    return [p for p in _SRC.rglob("*.py") if "__pycache__" not in p.parts]


def test_every_unit_is_classified() -> None:
    unknown = {_unit_of(p) for p in _all_modules()} - set(_LAYER) - {"__init__"}
    assert not unknown, f"new top-level units need a layer assignment: {sorted(unknown)}"


def test_no_module_imports_the_package_root() -> None:
    """`from medscale import X` inside src is an inverted edge (root imports workspace)."""
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) != "__init__" and "__root__" in _imports_of(p)
    ]
    assert not offenders, f"modules importing the package root: {offenders}"


def test_dependencies_only_flow_downward() -> None:
    violations: list[str] = []
    for module in _all_modules():
        unit = _unit_of(module)
        if unit == "__init__":  # the root re-exporter may import anything public
            continue
        own_layer = _LAYER[unit]
        for imported in _imports_of(module) - {"__root__", unit}:
            if imported not in _LAYER:
                continue
            if _LAYER[imported] > own_layer or (
                _LAYER[imported] == own_layer and imported != unit and own_layer not in (0, 2)
            ):
                # same-layer imports allowed only within spine (0) and the evidence
                # cluster (2), which is one conceptual layer split across modules
                violations.append(
                    f"{module.relative_to(_SRC)} (layer {own_layer}) imports "
                    f"{imported} (layer {_LAYER[imported]})"
                )
    assert not violations, "upward/lateral imports:\n  " + "\n  ".join(violations)


def test_transport_isolation() -> None:
    """Nothing outside `cli/` may import the transports."""
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) not in ("cli", "__init__") and "cli" in _imports_of(p)
    ]
    assert not offenders, f"engine modules importing transports: {offenders}"


def test_core_library_is_not_imported_by_the_engine() -> None:
    """Only transports (and the root re-exporter) may consume the facade."""
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) not in ("cli", "workspace", "__init__") and "workspace" in _imports_of(p)
    ]
    assert not offenders, f"engine modules importing the facade: {offenders}"


def test_evidence_layer_does_not_import_application_modules() -> None:
    """Evidence owns the claim model. It must not depend on downstream layers."""
    forbidden = {"litdb", "modelkit", "bench"}
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) == "evidence" and bool(forbidden & _imports_of(p))
    ]
    assert not offenders, "evidence imports cross forbidden boundaries:\n  " + "\n  ".join(
        offenders
    )


def test_storage_layout_lives_in_exactly_one_module() -> None:
    """Path literals for knowledge artifacts may exist only in _layout."""
    layout_literals = (
        "records.jsonl",
        "objects.jsonl",
        "screening_log.jsonl",
        "review_log.jsonl",
        "merge_log.jsonl",
        "uncertain_duplicates.jsonl",
        "uncertain_resolutions.jsonl",
    )
    offenders: list[str] = []
    for module in _all_modules():
        if _unit_of(module) == "_layout":
            continue
        text = module.read_text(encoding="utf-8")
        for literal in layout_literals:
            if f'"{literal}"' in text or f"'{literal}'" in text:
                offenders.append(f"{module.relative_to(_SRC)}: {literal}")
    assert not offenders, "layout literals outside _layout:\n  " + "\n  ".join(offenders)


def test_dataset_does_not_import_research() -> None:
    """The dataset artifact boundary must not depend on research intelligence."""
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) == "dataset" and "research" in _imports_of(p)
    ]
    assert not offenders, "dataset imports research:\n  " + "\n  ".join(offenders)


def test_cli_imports_are_not_imported_by_engine_modules() -> None:
    """CLI is a transport boundary; engine modules must not import it accidentally."""
    forbidden_engine_units = {
        "__about__",
        "_layout",
        "_runtime",
        "reproducibility",
        "provenance",
        "litdb",
        "evidence",
        "evidence_store",
        "evidence_checks",
        "extraction",
        "modelkit",
        "research",
        "dataset",
        "bench",
        "mesc",
        "workspace",
    }
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) in forbidden_engine_units and "cli" in _imports_of(p)
    ]
    assert not offenders, "engine modules importing cli:\n  " + "\n  ".join(offenders)


def test_collaboration_does_not_import_forbidden_modules() -> None:
    forbidden = {"dataset", "research", "backends", "fhirkit"}
    offenders = [
        str(p.relative_to(_SRC))
        for p in _all_modules()
        if _unit_of(p) == "collaboration" and bool(forbidden & _imports_of(p))
    ]
    assert not offenders, "collaboration imports forbidden modules:\n  " + "\n  ".join(offenders)


def test_no_module_package_name_collisions() -> None:
    """A sibling ``name.py`` next to a ``name/`` package is permanently shadowed.

    Python resolves the package, so the module is dead code that still ships in
    the wheel (the audit found ``medscale/evidence.py`` shadowed by
    ``medscale/evidence/`` — and it raised ImportError if ever executed).
    """
    collisions = [
        str(path.relative_to(_SRC))
        for path in sorted(_SRC.rglob("*.py"))
        if path.with_suffix("").is_dir()
    ]
    assert not collisions, "modules shadowed by same-named packages:\n  " + "\n  ".join(collisions)
