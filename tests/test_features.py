import pandas as pd

from src.features import build_customer_features


def test_build_customer_features_basic():
    df = pd.DataFrame(
        {
            "customer_id": [1, 1, 2],
            "invoice": ["A", "B", "C"],
            "invoice_date": pd.to_datetime(["2010-01-01", "2010-01-05", "2010-01-03"]),
            "line_total": [10.0, 20.0, 5.0],
            "country": ["UK", "UK", "FR"],
        }
    )
    features = build_customer_features(df)
    assert features.loc[features["customer_id"] == 1, "frequency_orders"].iloc[0] == 2
    assert features.loc[features["customer_id"] == 2, "monetary_total"].iloc[0] == 5.0
