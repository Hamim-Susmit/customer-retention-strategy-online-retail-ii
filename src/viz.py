"""Visualization helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


SEGMENT_COLORS = {
    "Save": "#d1495b",
    "Protect": "#00798c",
    "Nurture": "#edae49",
    "LetGo": "#6c757d",
}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_churn_risk_distribution(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    _ensure_dir(output_path.parent)

    plt.figure(figsize=(6, 4))
    plt.hist(df["churn_risk_score"], bins=30, color="#457b9d", alpha=0.8)
    plt.title("Churn Risk Score Distribution")
    plt.xlabel("Churn Risk Score")
    plt.ylabel("Customers")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_value_distribution(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    _ensure_dir(output_path.parent)

    plt.figure(figsize=(6, 4))
    plt.hist(df["value_score"], bins=30, color="#2a9d8f", alpha=0.8)
    plt.title("Value Score Distribution")
    plt.xlabel("Value Score")
    plt.ylabel("Customers")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_action_matrix(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    _ensure_dir(output_path.parent)

    plt.figure(figsize=(6, 5))
    for segment, color in SEGMENT_COLORS.items():
        subset = df[df["segment"] == segment]
        plt.scatter(
            subset["churn_risk_score"],
            subset["value_score"],
            label=segment,
            alpha=0.7,
            s=30,
            color=color,
        )
    plt.title("Action Matrix: Risk vs Value")
    plt.xlabel("Churn Risk Score")
    plt.ylabel("Value Score")
    plt.legend(title="Segment", fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_roi_by_scenario(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    _ensure_dir(output_path.parent)

    plt.figure(figsize=(7, 4))
    plt.bar(df["scenario_name"], df["roi"], color="#264653")
    plt.title("ROI by Scenario")
    plt.xlabel("Scenario")
    plt.ylabel("ROI")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
