
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_raw_dataset_exists():
    assert (ROOT / "data/raw/Online Retail.xlsx").exists()

def test_cleaned_csv_exists():
    path = ROOT / "data/processed/retail_cleaned.csv"
    assert path.exists()

def test_cleaned_data_has_required_columns():
    df = pd.read_csv(
        ROOT / "data/processed/retail_cleaned.csv",
        nrows=5
    )
    required = {
        "InvoiceNo", "StockCode", "Quantity",
        "InvoiceDate", "UnitPrice", "Country", "LineAmount"
    }
    assert required.issubset(df.columns)

def test_database_row_count():
    db = ROOT / "data/retail.db"
    assert db.exists()

    with sqlite3.connect(db) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM retail_transactions"
        ).fetchone()[0]

    assert count == 536641
