"""Cleaning utilities for Online Retail II transactions."""

from __future__ import annotations

from typing import List

import pandas as pd


COLUMN_ALIASES = {
    "invoice": "invoice",
    "invoice_no": "invoice",
    "invoiceno": "invoice",
    "invoice number": "invoice",
    "stockcode": "stock_code",
    "stock_code": "stock_code",
    "description": "description",
    "quantity": "quantity",
    "invoicedate": "invoice_date",
    "invoice_date": "invoice_date",
    "price": "price",
    "unitprice": "price",
    "customer id": "customer_id",
    "customer_id": "customer_id",
    "country": "country",
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case and map known aliases."""

    normalized = (
        df.columns.to_series()
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    df = df.copy()
    df.columns = normalized
    mapped: List[str] = [COLUMN_ALIASES.get(col, col) for col in df.columns]
    df.columns = mapped
    return df


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean transactions according to the project spec."""

    df = normalize_columns(df)
    required_cols = ["invoice", "quantity", "price", "invoice_date", "customer_id"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["customer_id"]).copy()
    df["invoice"] = df["invoice"].astype(str)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    df = df[df["invoice_date"].notna()]

    cancellation_mask = df["invoice"].str.startswith("C", na=False)
    df = df[~cancellation_mask]
    df = df[df["quantity"] > 0]
    df = df[df["price"] > 0]

    df["line_total"] = df["quantity"] * df["price"]
    df = df[df["line_total"] > 0]

    return df
