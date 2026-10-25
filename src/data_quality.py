
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"

df = pd.read_excel(DATA_PATH)

print("========== DATA QUALITY REPORT ==========")

# 1. Missing values
print("\n1. Missing values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)

missing_report = pd.DataFrame({
    "missing_count": missing,
    "missing_percentage": missing_pct
})
print(missing_report)

# 2. Duplicate records
print("\n2. Duplicate records:")
print("Duplicate rows:", df.duplicated().sum())

# 3. Negative or zero quantities
print("\n3. Quantity checks:")
print("Negative quantities:", (df["Quantity"] < 0).sum())
print("Zero quantities:", (df["Quantity"] == 0).sum())

# 4. Unit price checks
print("\n4. Unit price checks:")
print("Negative prices:", (df["UnitPrice"] < 0).sum())
print("Zero prices:", (df["UnitPrice"] == 0).sum())

# 5. Cancelled invoices
print("\n5. Invoice checks:")
invoice_text = df["InvoiceNo"].astype(str)
print("Cancelled invoice rows:", invoice_text.str.startswith("C").sum())

# 6. Save report
report_path = PROJECT_ROOT / "data" / "processed" / "data_quality_report.csv"
missing_report.to_csv(report_path)

print("\nQuality report saved to:", report_path)


print("\nMissing CustomerID examples:")
print(
    df[df["CustomerID"].isna()]
    [["InvoiceNo", "StockCode", "Description",
      "Quantity", "UnitPrice", "Country"]]
    .head(10)
    .to_string(index=False)
)

print("\nMissing Description examples:")
print(
    df[df["Description"].isna()]
    [["InvoiceNo", "StockCode", "Quantity",
      "UnitPrice", "Country"]]
    .head(10)
    .to_string(index=False)
)