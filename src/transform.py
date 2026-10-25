
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "retail_cleaned.csv"

# EXTRACT
df = pd.read_excel(RAW_PATH)

initial_rows = len(df)
print("Initial rows:", initial_rows)

# STANDARDIZE
df.columns = df.columns.str.strip()

df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["StockCode"] = df["StockCode"].astype("string").str.strip()
df["Description"] = df["Description"].astype("string").str.strip()
df["Country"] = df["Country"].astype("string").str.strip()

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# CustomerID: preserve missing values, but remove decimal formatting
df["CustomerID"] = df["CustomerID"].astype("Int64")

# DATA QUALITY FLAGS: preserve unusual transactions for investigation
df["IsCancelled"] = df["InvoiceNo"].str.startswith("C", na=False)
df["IsReturnOrNegativeQuantity"] = df["Quantity"] < 0
df["IsZeroPrice"] = df["UnitPrice"] == 0
df["HasMissingCustomerID"] = df["CustomerID"].isna()
df["HasMissingDescription"] = df["Description"].isna()

# Remove exact duplicate rows only; report the count
duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Derived business metric
df["LineAmount"] = df["Quantity"] * df["UnitPrice"]

# LOAD: save the transformed data
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("\nTransformation completed.")
print("Initial rows:", initial_rows)
print("Exact duplicates removed:", duplicates)
print("Rows after deduplication:", len(df))
print("Missing CustomerID:", int(df["CustomerID"].isna().sum()))
print("Cancelled invoice rows:", int(df["IsCancelled"].sum()))
print("Negative quantity rows:", int(df["IsReturnOrNegativeQuantity"].sum()))
print("Zero-price rows:", int(df["IsZeroPrice"].sum()))
print("Output saved to:", OUTPUT_PATH)
