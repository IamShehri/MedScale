"""Metric reporting: the one implementation of mean ± 95% CI, verified numerically."""

from __future__ import annotations

import pytest

from medscale.modelkit import summarize_metric


def test_three_seed_summary_known_values() -> None:
    # values (1, 2, 3): mean 2, sample sd 1, t(df=2) = 4.303
    summary = summarize_metric("validity_rate", (1.0, 2.0, 3.0))
    assert summary.mean == pytest.approx(2.0)
    assert summary.sample_sd == pytest.approx(1.0)
    assert summary.ci95_half_width == pytest.approx(4.303 / (3**0.5), rel=1e-6)
    assert summary.n == 3


def test_single_seed_reports_no_ci() -> None:
    summary = summarize_metric("m", (0.5,))
    assert summary.mean == 0.5
    assert summary.sample_sd is None
    assert summary.ci95_half_width is None


def test_zero_variance() -> None:
    summary = summarize_metric("m", (2.0, 2.0, 2.0))
    assert summary.sample_sd == 0.0
    assert summary.ci95_half_width == 0.0


def test_large_n_uses_normal_approximation() -> None:
    values = tuple(float(i % 2) for i in range(40))  # df=39 > table
    summary = summarize_metric("m", values)
    assert summary.ci95_half_width is not None
    sd = summary.sample_sd
    assert sd is not None
    assert summary.ci95_half_width == pytest.approx(1.960 * sd / (40**0.5), rel=1e-6)


def test_validation() -> None:
    with pytest.raises(ValueError, match="name"):
        summarize_metric(" ", (1.0,))
    with pytest.raises(ValueError, match="at least one value"):
        summarize_metric("m", ())
