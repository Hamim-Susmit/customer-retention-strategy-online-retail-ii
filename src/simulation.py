"""Simulation utilities for intervention ROI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SimulationConfig:
    baseline_margin_rate: float = 0.30
    discount_rate: float = 0.10
    free_shipping_cost: float = 5.0
    loyalty_perk_cost: float = 3.0
    lift_discount: float = 0.25
    lift_free_shipping: float = 0.12
    lift_loyalty: float = 0.08
    budget: float = 5000.0


def estimate_next_period_revenue(df: pd.DataFrame) -> pd.Series:
    expected_orders = (df["frequency_orders"] / df["purchase_span_months"]).clip(
        lower=0.5, upper=2.0
    )
    return df["avg_order_value"] * expected_orders


def compute_action_costs(
    df: pd.DataFrame, config: SimulationConfig
) -> pd.Series:
    action = df["recommended_action"]
    expected_revenue = df["expected_next_period_revenue"]

    costs = np.where(
        action == "Discount10",
        expected_revenue * config.discount_rate,
        np.where(
            action == "FreeShipping",
            config.free_shipping_cost,
            np.where(action == "LoyaltyPerk", config.loyalty_perk_cost, 0.0),
        ),
    )
    return pd.Series(costs, index=df.index)


def compute_lift_factor(df: pd.DataFrame, config: SimulationConfig) -> pd.Series:
    action = df["recommended_action"]
    lifts = np.where(
        action == "Discount10",
        config.lift_discount,
        np.where(
            action == "FreeShipping",
            config.lift_free_shipping,
            np.where(action == "LoyaltyPerk", config.lift_loyalty, 0.0),
        ),
    )
    return pd.Series(lifts, index=df.index)


def enrich_with_simulation_fields(
    df: pd.DataFrame, config: SimulationConfig | None = None
) -> pd.DataFrame:
    config = config or SimulationConfig()
    df = df.copy()

    df["expected_next_period_revenue"] = estimate_next_period_revenue(df)
    df["action_cost"] = compute_action_costs(df, config)
    df["lift_factor"] = compute_lift_factor(df, config)
    df["expected_profit_saved"] = (
        df["expected_next_period_revenue"]
        * config.baseline_margin_rate
        * df["lift_factor"]
    )
    df["expected_incremental_profit"] = (
        df["expected_profit_saved"] - df["action_cost"]
    )
    df["expected_roi"] = np.where(
        df["action_cost"] > 0,
        df["expected_incremental_profit"] / df["action_cost"],
        0.0,
    )

    return df


def _summarize_scenario(
    name: str, df: pd.DataFrame, budget: float
) -> Dict[str, float | int | str]:
    total_cost = df["action_cost"].sum()
    expected_profit_saved = df["expected_profit_saved"].sum()
    net_profit = expected_profit_saved - total_cost
    roi = net_profit / total_cost if total_cost > 0 else 0.0
    return {
        "scenario_name": name,
        "budget": budget,
        "customers_targeted": int(df["customer_id"].nunique()),
        "total_cost": float(total_cost),
        "expected_profit_saved": float(expected_profit_saved),
        "net_profit": float(net_profit),
        "roi": float(roi),
    }


def _apply_targeting(df: pd.DataFrame, target_mask: pd.Series) -> pd.DataFrame:
    targeted = df[target_mask].copy()
    return targeted


def optimize_under_budget(
    df: pd.DataFrame, budget: float, allow_zero_cost: bool = True
) -> Tuple[pd.DataFrame, pd.Series]:
    candidates = df[df["expected_incremental_profit"] > 0].copy()
    candidates = candidates.sort_values(
        by=["expected_incremental_profit"], ascending=False
    )

    selected_indices: List[int] = []
    total_cost = 0.0
    for idx, row in candidates.iterrows():
        cost = row["action_cost"]
        if cost == 0 and allow_zero_cost:
            selected_indices.append(idx)
            continue
        if total_cost + cost <= budget:
            selected_indices.append(idx)
            total_cost += cost

    selected_mask = df.index.isin(selected_indices)
    return df[selected_mask].copy(), pd.Series(selected_mask, index=df.index)


def run_simulation_scenarios(
    df: pd.DataFrame, config: SimulationConfig | None = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run predefined scenarios and return summary + enriched action list."""

    config = config or SimulationConfig()
    enriched = enrich_with_simulation_fields(df, config)

    scenarios: List[Dict[str, float | int | str]] = []

    base_mask = enriched["recommended_action"] != "NoAction"
    scenarios.append(
        _summarize_scenario("BasePolicy", enriched[base_mask], config.budget)
    )

    save_mask = enriched["segment"] == "Save"
    scenarios.append(_summarize_scenario("SaveOnly", enriched[save_mask], config.budget))

    save_nurture_mask = enriched["segment"].isin(["Save", "Nurture"])
    scenarios.append(
        _summarize_scenario(
            "SaveNurture", enriched[save_nurture_mask], config.budget
        )
    )

    optimized_df, selected_mask = optimize_under_budget(
        enriched, budget=config.budget
    )
    enriched["selected_under_budget"] = selected_mask
    scenarios.append(
        _summarize_scenario("OptimizedBudget", optimized_df, config.budget)
    )

    summary = pd.DataFrame(scenarios)
    return summary, enriched
