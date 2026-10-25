
from pathlib import Path
import pandas as pd
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "retail_cleaned.csv"
DB_PATH = PROJECT_ROOT / "data" / "retail.db"

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Cleaned CSV not found: {CSV_PATH}")

# Read transformed data
df = pd.read_csv(CSV_PATH)

# Create database and load data
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        "retail_transactions",
        conn,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    # Verify the load
    row_count = conn.execute(
        "SELECT COUNT(*) FROM retail_transactions"
    ).fetchone()[0]

    print("Database created:", DB_PATH)
    print("Rows loaded:", row_count)

    print("\nSample records:")
    for row in conn.execute("""
        SELECT InvoiceNo, StockCode, Quantity, UnitPrice, LineAmount
        FROM retail_transactions
        LIMIT 5
    """):
        print(row)
