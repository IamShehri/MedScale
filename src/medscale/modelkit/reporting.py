"""Honest metric reporting: mean ± 95% CI over seeds, deterministically.

The reproducibility policy requires comparisons over ≥3 seeds reported as mean ± 95%
confidence interval, with differences inside seed variance reported as *no difference*.
This module is the one implementation of that arithmetic, so every report computes it
identically — pure stdlib, no numerical dependency.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

__all__ = ["MetricSummary", "summarize_metric"]

#: Two-sided 95% Student-t critical values by degrees of freedom (1-30).
_T95: Final[dict[int, float]] = {
    1: 12.706,
    2: 4.303,
    3: 3.182,
    4: 2.776,
    5: 2.571,
    6: 2.447,
    7: 2.365,
    8: 2.306,
    9: 2.262,
    10: 2.228,
    11: 2.201,
    12: 2.179,
    13: 2.160,
    14: 2.145,
    15: 2.131,
    16: 2.120,
    17: 2.110,
    18: 2.101,
    19: 2.093,
    20: 2.086,
    21: 2.080,
    22: 2.074,
    23: 2.069,
    24: 2.064,
    25: 2.060,
    26: 2.056,
    27: 2.052,
    28: 2.048,
    29: 2.045,
    30: 2.042,
}
_T95_LARGE: Final = 1.960


@dataclass(frozen=True)
class MetricSummary:
    """A metric over seeds: the honest, complete report of one number."""

    name: str
    values: tuple[float, ...]
    mean: float
    sample_sd: float | None
    ci95_half_width: float | None

    @property
    def n(self) -> int:
        return len(self.values)


def summarize_metric(name: str, values: tuple[float, ...]) -> MetricSummary:
    """Summarize per-seed metric values as mean ± 95% CI (Student-t).

    With a single value there is no variance estimate: ``sample_sd`` and the CI are
    ``None`` — a single-seed number is reported as exactly that, never dressed up.
    """
    if not name.strip():
        raise ValueError("metric name must be non-empty")
    if not values:
        raise ValueError("at least one value is required")
    n = len(values)
    mean = sum(values) / n
    if n == 1:
        return MetricSummary(name, values, mean, None, None)
    variance = sum((value - mean) ** 2 for value in values) / (n - 1)
    sd = math.sqrt(variance)
    t = _T95.get(n - 1, _T95_LARGE)
    return MetricSummary(name, values, mean, sd, t * sd / math.sqrt(n))
