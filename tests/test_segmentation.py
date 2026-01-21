import pandas as pd

from src.segmentation import score_and_segment_customers


def test_score_and_segment_customers():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "recency_days": [10, 100, 5, 200],
            "frequency_orders": [5, 1, 10, 2],
            "monetary_total": [100, 50, 200, 30],
            "avg_order_value": [20, 50, 20, 15],
        }
    )
    scored = score_and_segment_customers(df)
    assert "segment" in scored.columns
    assert "recommended_action" in scored.columns
