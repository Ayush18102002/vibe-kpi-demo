"""
Tests for src/kpi_city.py using pytest.

These tests use a temporary in-memory SQLite database so they
don't depend on the real analytics.db file.
"""

import sqlite3
import os
import pytest

# We need to set up a temp DB before importing city_kpi
from src.kpi_city import city_kpi, ALLOWED_CITIES

# ── Fixtures ─────────────────────────────────────────────────────────

TEMP_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "db", "test_analytics.db",
)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create a small test database before each test, remove it after."""
    os.makedirs(os.path.dirname(TEMP_DB), exist_ok=True)
    conn = sqlite3.connect(TEMP_DB)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers_raw (
            customer_id INTEGER,
            city TEXT,
            monthly_spend REAL,
            churned INTEGER
        )
        """
    )
    conn.execute("DELETE FROM customers_raw")  # clean slate
    conn.executemany(
        "INSERT INTO customers_raw VALUES (?, ?, ?, ?)",
        [
            (1, "Mumbai", 4000.0, 0),
            (2, "Mumbai", 6000.0, 1),
            (3, "Delhi",  3000.0, 0),
        ],
    )
    conn.commit()
    conn.close()

    yield  # run the test

    os.remove(TEMP_DB)


# ── Tests ────────────────────────────────────────────────────────────

def test_city_kpi_happy_path():
    """A valid city should return correct KPIs."""
    result = city_kpi("Mumbai", db_path=TEMP_DB)

    assert result is not None
    assert result["city"] == "Mumbai"
    assert result["total_customers"] == 2
    assert result["avg_spend"] == 5000.0       # (4000 + 6000) / 2
    assert result["churn_rate"] == 0.5          # 1 out of 2


def test_city_kpi_sql_injection():
    """An injection string should be rejected by the allowlist."""
    with pytest.raises(ValueError, match="Unknown city"):
        city_kpi("Mumbai' OR 1=1 --", db_path=TEMP_DB)


def test_city_kpi_unknown_city():
    """A city not in ALLOWED_CITIES should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown city"):
        city_kpi("Tokyo", db_path=TEMP_DB)
