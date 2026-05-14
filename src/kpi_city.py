"""
KPI Script: Calculate city-level analytics from the SQLite database.

Uses parameterized SQL (WHERE city = ?) to prevent SQL injection.
"""

import sqlite3
import os

# ── Path ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "data", "db", "analytics.db")

# Allowlist of valid cities -- reject anything not in this set
ALLOWED_CITIES = {"Mumbai", "Delhi", "Bangalore", "Pune"}


def city_kpi(city: str, db_path: str = DB_PATH) -> dict:
    """Return KPIs for a given city.

    Metrics:
        - total_customers : number of customers in the city
        - avg_spend       : average monthly spend
        - churn_rate      : fraction of customers who churned

    Args:
        city: City name to filter on.
        db_path: Path to the SQLite database.

    Returns:
        dict with the KPI values, or None if the city has no data.
    """
    # Reject unknown cities before touching the database
    if city not in ALLOWED_CITIES:
        raise ValueError(f"Unknown city: '{city}'. Allowed: {sorted(ALLOWED_CITIES)}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Parameterized query -- safe from SQL injection
    cursor.execute(
        """
        SELECT
            COUNT(*)            AS total_customers,
            AVG(monthly_spend)  AS avg_spend,
            AVG(churned)        AS churn_rate
        FROM customers_raw
        WHERE city = ?
        """,
        (city,),
    )

    row = cursor.fetchone()
    conn.close()

    total_customers, avg_spend, churn_rate = row

    # If the city doesn't exist, COUNT(*) returns 0
    if total_customers == 0:
        return None

    return {
        "city": city,
        "total_customers": total_customers,
        "avg_spend": round(avg_spend, 2),
        "churn_rate": round(churn_rate, 2),
    }


def print_kpi_table(cities: list, db_path: str = DB_PATH):
    """Print KPIs for multiple cities in a formatted table."""
    header = f"{'City':<15} {'Customers':>10} {'Avg Spend':>12} {'Churn Rate':>12}"
    separator = "-" * len(header)

    print(separator)
    print(header)
    print(separator)

    for city in cities:
        result = city_kpi(city, db_path)
        if result:
            print(
                f"{result['city']:<15} "
                f"{result['total_customers']:>10} "
                f"{result['avg_spend']:>12.2f} "
                f"{result['churn_rate']:>12.2f}"
            )
        else:
            print(f"{city:<15} {'--':>10} {'--':>12} {'--':>12}")

    print(separator)


if __name__ == "__main__":
    # -- City-level KPIs (table format) ------------------------------
    print("\n[City-Level KPI Report]\n")
    print_kpi_table(["Mumbai", "Delhi", "Bangalore", "Pune"])

    # -- Unknown city test (should be rejected by allowlist) ---------
    print("\n[Unknown City Test]\n")
    try:
        city_kpi("Mumbai' OR 1=1 --")
    except ValueError as e:
        print(f"BLOCKED: {e}")
