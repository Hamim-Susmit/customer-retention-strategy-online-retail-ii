import pandas as pd

from src.simulation import run_simulation_scenarios


def test_run_simulation_scenarios_outputs():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "frequency_orders": [5, 2],
            "purchase_span_months": [2, 1],
            "avg_order_value": [20, 30],
            "recommended_action": ["Discount10", "NoAction"],
            "segment": ["Save", "LetGo"],
        }
    )
    summary, enriched = run_simulation_scenarios(df)
    assert not summary.empty
    assert "expected_incremental_profit" in enriched.columns
