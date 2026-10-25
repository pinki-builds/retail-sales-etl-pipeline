# Retail Sales ETL & Analytics Pipeline

## Overview

An end-to-end data engineering project that processes retail transaction data using Python, Pandas, SQL, SQLite, and PySpark. The project includes data inspection, quality reporting, transformation, database loading, SQL analytics, and automated tests.

## Dataset

- **Source:** UCI Machine Learning Repository
- **Dataset:** Online Retail
- **Original records:** 541,909
- **Original columns:** 8
- **Period:** December 2010 – December 2011

Dataset: https://archive.ics.uci.edu/dataset/352/online+retail

## Tech Stack

- Python 3.12
- Pandas
- SQL and SQLite
- PySpark
- Pytest
- Git and GitHub

## Pipeline Workflow

The complete pipeline can be executed with a single command:

```bash
python src/pipeline.py
```

The pipeline performs the following steps:

1. Inspects the raw dataset schema and data quality.
2. Generates a data quality report.
3. Removes exact duplicate records and transforms the data using Pandas.
4. Creates transaction quality flags and derives `LineAmount`.
5. Loads the transformed dataset into a SQLite database.
6. Executes SQL analytics queries.
7. Uses PySpark to aggregate sales by country and calculate distinct invoice counts.
8. Saves the country-level sales report as a CSV file.
9. Records pipeline execution details in a log file.

## Project Structure

```text
retail_project/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── inspect_data.py
│   ├── data_quality.py
│   ├── transform.py
│   ├── load_sql.py
│   ├── run_sql.py
│   ├── pyspark_transform.py
│   └── pipeline.py
├── sql/
│   └── analytics.sql
├── tests/
│   └── test_pipeline.py
├── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

## Data Transformation and Validation

- Original records: 541,909
- Exact duplicate records removed: 5,268
- Transformed records: 536,641
- Automated tests: 4 passed

The pipeline reports missing customer IDs, missing descriptions, negative quantities, zero-price rows, and cancelled invoices. These records are flagged or reported rather than automatically assuming that every unusual transaction is invalid.

## Analytics and Results

SQL queries cover:

- Total net transaction value
- Product-level sales
- Country-level sales
- Monthly sales trends
- Daily sales ranking using a window function

### Key Results

| Metric | Result |
|---|---:|
| Transformed records | 536,641 |
| Unique invoices | 25,900 |
| Unique customers | 4,372 |
| Net transaction value | 9,726,006.95 |

The PySpark country-level aggregation identified the United Kingdom as the largest market by net transaction value, at 8,167,128.18.

*Note: Values are in the dataset's transaction currency context; the source contains no explicit currency conversion in this project.*

## Output Files

- `data/processed/data_quality_report.csv` — data quality summary
- `data/processed/retail_cleaned.csv` — transformed transaction data
- `data/retail.db` — SQLite database
- `data/processed/pyspark_output/country_sales.csv` — PySpark country-level aggregation
- `logs/pipeline.log` — pipeline execution log

Generated data and the original dataset are excluded from Git tracking.

## Run Locally

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install a compatible Java version for local PySpark execution. Then run:

```powershell
python src/pipeline.py
python -m pytest tests -v
```

## Future Improvements

- Add incremental data loading and orchestration.
- Strengthen automated data quality and transformation tests.
- Improve business rules for returns, cancellations, and unusual product records.
- Add a cloud-based deployment and scheduled execution.
- Explore data warehouse integration and monitoring.
