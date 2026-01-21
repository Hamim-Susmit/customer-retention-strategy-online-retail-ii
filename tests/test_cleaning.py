import pandas as pd

from src.cleaning import clean_transactions


def test_clean_transactions_removes_invalid_rows():
    df = pd.DataFrame(
        {
            "Invoice": ["A1", "C2"],
            "Quantity": [1, -2],
            "Price": [10.0, 5.0],
            "InvoiceDate": ["2010-01-01", "2010-01-02"],
            "Customer ID": [123, None],
            "Country": ["UK", "UK"],
        }
    )
    cleaned = clean_transactions(df)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["invoice"] == "A1"
    assert cleaned.iloc[0]["line_total"] == 10.0
