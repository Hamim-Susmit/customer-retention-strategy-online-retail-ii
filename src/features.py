"""Feature engineering for customer-level metrics."""

from __future__ import annotations

from typing import Optional

import pandas as pd


def build_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction-level data into customer features."""

    if "line_total" not in df.columns:
        raise ValueError("Expected line_total column. Did you run clean_transactions()?")

    snapshot_date = df["invoice_date"].max()

    grouped = df.groupby("customer_id")
    features = grouped.agg(
        first_purchase=("invoice_date", "min"),
        last_purchase=("invoice_date", "max"),
        frequency_orders=("invoice", "nunique"),
        monetary_total=("line_total", "sum"),
        avg_order_value=("line_total", "mean"),
        country_mode=("country", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
    )
    features = features.reset_index()

    features["recency_days"] = (snapshot_date - features["last_purchase"]).dt.days
    features["purchase_span_days"] = (
        features["last_purchase"] - features["first_purchase"]
    ).dt.days
    features["avg_order_value"] = features["monetary_total"] / features["frequency_orders"]

    return features


def add_purchase_span_months(df: pd.DataFrame) -> pd.DataFrame:
    """Add purchase_span_months for downstream simulations."""

    df = df.copy()
    df["purchase_span_months"] = (df["purchase_span_days"] / 30).clip(lower=1)
    return df
