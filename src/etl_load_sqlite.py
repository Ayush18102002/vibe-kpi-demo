"""
ETL Script: Load customers_raw.csv into a SQLite database.

Steps:
  1. Read the CSV file using pandas.
  2. Create (or replace) the 'customers_raw' table in analytics.db.
  3. Print a confirmation with the row count.
"""

import pandas as pd
import sqlite3
import os

# ── Paths ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "customers_raw.csv")
DB_PATH  = os.path.join(BASE_DIR, "data", "db", "analytics.db")


def load_csv_to_sqlite(csv_path: str = CSV_PATH, db_path: str = DB_PATH) -> int:
    """Read the CSV and write it into the SQLite table 'customers_raw'.

    Returns:
        int: Number of rows loaded.
    """
    # 1. Extract — read the CSV
    df = pd.read_csv(csv_path)
    print(f"[OK] Read {len(df)} rows from {os.path.basename(csv_path)}")

    # 2. Load — write to SQLite (replace if table already exists)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("customers_raw", conn, if_exists="replace", index=False)
    conn.close()

    print(f"[OK] Loaded {len(df)} rows into analytics.db -> customers_raw")
    return len(df)


if __name__ == "__main__":
    load_csv_to_sqlite()
