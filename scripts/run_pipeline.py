"""Run end-to-end customer retention pipeline."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cleaning import clean_transactions
from src.features import build_customer_features, add_purchase_span_months
from src.io import load_raw_transactions
from src.segmentation import score_and_segment_customers
from src.simulation import run_simulation_scenarios
from src.viz import (
    plot_action_matrix,
    plot_churn_risk_distribution,
    plot_roi_by_scenario,
    plot_value_distribution,
)


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Customer retention pipeline")
    parser.add_argument(
        "--input",
        default="data/raw/online_retail_II.xlsx",
        help="Path to Online Retail II Excel file",
    )
    parser.add_argument(
        "--outdir",
        default="reports",
        help="Output directory for reports",
    )
    return parser.parse_args()


def main() -> None:
    _setup_logging()
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        logging.error("Input file not found: %s", input_path)
        logging.info("Place the Online Retail II dataset at data/raw/online_retail_II.xlsx")
        return

    outdir = Path(args.outdir)
    figures_dir = outdir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Loading raw transactions...")
    raw_df = load_raw_transactions(input_path)

    logging.info("Cleaning transactions...")
    cleaned = clean_transactions(raw_df)

    logging.info("Building customer features...")
    features = build_customer_features(cleaned)
    features = add_purchase_span_months(features)

    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    features_path = processed_dir / "customer_features.parquet"
    features.to_parquet(features_path, index=False)
    logging.info("Saved features to %s", features_path)

    logging.info("Scoring risk/value and segmenting...")
    segmented = score_and_segment_customers(features)

    logging.info("Running ROI simulation scenarios...")
    summary, action_list = run_simulation_scenarios(segmented)

    action_list_path = outdir / "customer_action_list.csv"
    summary_path = outdir / "simulation_summary.csv"
    action_list.to_csv(action_list_path, index=False)
    summary.to_csv(summary_path, index=False)
    logging.info("Saved action list to %s", action_list_path)
    logging.info("Saved simulation summary to %s", summary_path)

    logging.info("Saving figures...")
    plot_churn_risk_distribution(action_list, figures_dir / "churn_risk_distribution.png")
    plot_value_distribution(action_list, figures_dir / "value_distribution.png")
    plot_action_matrix(action_list, figures_dir / "action_matrix.png")
    plot_roi_by_scenario(summary, figures_dir / "roi_by_scenario.png")
    logging.info("Pipeline complete")


if __name__ == "__main__":
    main()
