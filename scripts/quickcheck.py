"""Quick sanity checks for pipeline inputs/outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quick checks for pipeline outputs")
    parser.add_argument(
        "--outdir",
        default="reports",
        help="Output directory for reports",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)

    action_list_path = outdir / "customer_action_list.csv"
    summary_path = outdir / "simulation_summary.csv"

    if not action_list_path.exists():
        raise FileNotFoundError(f"Missing {action_list_path}")
    if not summary_path.exists():
        raise FileNotFoundError(f"Missing {summary_path}")

    action_list = pd.read_csv(action_list_path)
    summary = pd.read_csv(summary_path)

    required_cols = {
        "customer_id",
        "recency_days",
        "frequency_orders",
        "monetary_total",
        "avg_order_value",
        "churn_risk_score",
        "value_score",
        "segment",
        "recommended_action",
        "expected_incremental_profit",
        "action_cost",
        "expected_roi",
    }

    missing_cols = required_cols - set(action_list.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in action list: {missing_cols}")

    if summary.empty:
        raise ValueError("Simulation summary is empty")

    print("Quickcheck passed:")
    print(f"- {len(action_list)} customers in action list")
    print(f"- {len(summary)} simulation scenarios")


if __name__ == "__main__":
    main()
