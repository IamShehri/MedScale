"""Dataset license metadata.

Stability: **public**. Produces the metadata/licenses.json artifact from the
dataset corpus and manifest. Reuses existing provenance fields; no new model
is introduced.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

__all__ = ["write_licenses_metadata"]


def _coalesce_license(record: dict[str, object]) -> str | None:
    license_spdx = record.get("license_spdx")
    if isinstance(license_spdx, str) and license_spdx.strip():
        return license_spdx.strip()
    return None


def build_license_summary(records: Sequence[dict[str, object]]) -> dict[str, int]:
    counts: Counter[str | None] = Counter()
    for record in records:
        counts[_coalesce_license(record)] += 1
    summary: dict[str, int] = {}
    for key, value in counts.items():
        if key is None:
            summary["unknown"] = value
        else:
            summary[key] = value
    return summary


def write_licenses_metadata(
    dataset_dir: Path,
    records: Sequence[dict[str, object]],
) -> Path:
    license_dir = dataset_dir / "metadata"
    license_dir.mkdir(parents=True, exist_ok=True)
    summary = build_license_summary(records)
    payload = {
        "dataset_id": dataset_dir.name,
        "license_summary": [
            {"spdx": key, "count": value} for key, value in sorted(summary.items())
        ],
        "unknown_count": summary.get("unknown", 0),
    }
    path = license_dir / "licenses.json"
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    return path
