
from pathlib import Path
import shutil
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "processed" / "retail_cleaned.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "pyspark_output"

spark = (
    SparkSession.builder
    .appName("RetailSalesETL")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

try:
    # Read transformed CSV
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(CSV_PATH))
    )

    print("========== PYSPARK ETL ==========")
    print("Total rows:", df.count())

    # Create typed columns and derived metrics
    df = (
        df.withColumn("Quantity", F.col("Quantity").cast("integer"))
          .withColumn("UnitPrice", F.col("UnitPrice").cast("double"))
          .withColumn("LineAmount", F.col("Quantity") * F.col("UnitPrice"))
          .withColumn("InvoiceDate", F.to_timestamp("InvoiceDate"))
    )

    # Aggregate sales by country
    country_sales = (
        df.groupBy("Country")
          .agg(
              F.round(F.sum("LineAmount"), 2).alias("net_sales"),
              F.countDistinct("InvoiceNo").alias("invoice_count")
          )
          .orderBy(F.desc("net_sales"))
    )

    print("\nTop 10 countries:")
    country_sales.show(10, truncate=False)

    # Data quality summary
    print("\nData quality checks:")
    df.select(
        F.sum(F.col("CustomerID").isNull().cast("int"))
          .alias("missing_customer_ids"),
        F.sum((F.col("Quantity") < 0).cast("int"))
          .alias("negative_quantity_rows"),
        F.sum((F.col("UnitPrice") == 0).cast("int"))
          .alias("zero_price_rows")
    ).show()

    # Convert only the small aggregated result to Pandas.
    # Pandas writes the CSV without requiring Windows winutils.exe.
    output_df = country_sales.toPandas()

    if OUTPUT_PATH.exists():
        shutil.rmtree(OUTPUT_PATH)

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_PATH / "country_sales.csv"
    output_df.to_csv(output_file, index=False)

    print("PySpark output saved to:", output_file)

finally:
    spark.stop()
