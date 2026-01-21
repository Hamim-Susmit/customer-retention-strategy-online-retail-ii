"""Customer retention strategy package."""

from .io import load_raw_transactions
from .cleaning import clean_transactions
from .features import build_customer_features
from .segmentation import score_and_segment_customers
from .simulation import run_simulation_scenarios
from .viz import (
    plot_churn_risk_distribution,
    plot_value_distribution,
    plot_action_matrix,
    plot_roi_by_scenario,
)

__all__ = [
    "load_raw_transactions",
    "clean_transactions",
    "build_customer_features",
    "score_and_segment_customers",
    "run_simulation_scenarios",
    "plot_churn_risk_distribution",
    "plot_value_distribution",
    "plot_action_matrix",
    "plot_roi_by_scenario",
]
