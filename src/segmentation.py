"""Risk, value scoring, and segmentation logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RiskValueConfig:
    recency_weight: float = 2.0
    frequency_weight: float = 2.0
    value_weight_monetary: float = 0.7
    value_weight_aov: float = 0.3
    risk_threshold: float = 0.7
    value_threshold: float = 0.7


def _percentile_clip(series: pd.Series, low: float = 0.05, high: float = 0.95) -> pd.Series:
    lower, upper = series.quantile([low, high])
    return series.clip(lower=lower, upper=upper)


def _minmax_scale(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return (series - min_val) / (max_val - min_val)


def _sigmoid(x: pd.Series | np.ndarray) -> pd.Series:
    return 1 / (1 + np.exp(-x))


def score_risk_value(
    df: pd.DataFrame, config: RiskValueConfig | None = None
) -> pd.DataFrame:
    """Compute churn risk and value scores."""

    config = config or RiskValueConfig()
    df = df.copy()

    recency_scaled = _minmax_scale(_percentile_clip(df["recency_days"]))
    frequency_scaled = _minmax_scale(_percentile_clip(df["frequency_orders"]))

    risk_raw = (
        config.recency_weight * recency_scaled
        + config.frequency_weight * (1 - frequency_scaled)
    )
    df["churn_risk_score"] = _sigmoid(risk_raw)

    monetary_scaled = _minmax_scale(_percentile_clip(df["monetary_total"]))
    aov_scaled = _minmax_scale(_percentile_clip(df["avg_order_value"]))
    df["value_score"] = (
        config.value_weight_monetary * monetary_scaled
        + config.value_weight_aov * aov_scaled
    )

    return df


def segment_customers(
    df: pd.DataFrame, config: RiskValueConfig | None = None
) -> pd.DataFrame:
    """Assign 2x2 segments based on risk/value scores."""

    config = config or RiskValueConfig()
    df = df.copy()

    risk_threshold = df["churn_risk_score"].quantile(config.risk_threshold)
    value_threshold = df["value_score"].quantile(config.value_threshold)

    high_risk = df["churn_risk_score"] >= risk_threshold
    high_value = df["value_score"] >= value_threshold

    df["segment"] = np.select(
        [high_risk & high_value, ~high_risk & high_value, high_risk & ~high_value],
        ["Save", "Protect", "Nurture"],
        default="LetGo",
    )

    action_map = {
        "Save": "Discount10",
        "Protect": "LoyaltyPerk",
        "Nurture": "FreeShipping",
        "LetGo": "NoAction",
    }
    df["recommended_action"] = df["segment"].map(action_map)
    return df


def score_and_segment_customers(
    df: pd.DataFrame, config: RiskValueConfig | None = None
) -> pd.DataFrame:
    """Convenience wrapper to score and segment."""

    scored = score_risk_value(df, config=config)
    return segment_customers(scored, config=config)
