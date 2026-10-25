
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "retail.db"
SQL_PATH = ROOT / "sql" / "analytics.sql"

sql_text = SQL_PATH.read_text(encoding="utf-8")

# Split and run each query separately
queries = [
    q.strip()
    for q in sql_text.split(";")
    if q.strip()
]

with sqlite3.connect(DB_PATH) as conn:
    for number, query in enumerate(queries, start=1):
        print(f"\n{'=' * 15} QUERY {number} {'=' * 15}")

        cursor = conn.execute(query)
        columns = [col[0] for col in cursor.description]
        print(" | ".join(columns))

        for row in cursor.fetchmany(10):
            print(row)
