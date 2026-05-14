# 📊 Vibe KPI Demo — Applied Analytics Mini Project

A beginner-friendly project that demonstrates a complete **ETL → KPI → Test** workflow using Python, pandas, SQLite, and pytest.

## 📁 Folder Structure

```
vibe-kpi-demo/
├── data/
│   ├── raw/customers_raw.csv   ← sample customer data
│   └── db/analytics.db         ← SQLite DB (created by ETL)
├── src/
│   ├── etl_load_sqlite.py      ← loads CSV into SQLite
│   └── kpi_city.py             ← city-level KPI calculator
├── tests/
│   └── test_kpi_city.py        ← pytest: happy path + injection test
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the ETL (load CSV → SQLite)

```bash
python src/etl_load_sqlite.py
```

### 4. Run the KPI script

```bash
python src/kpi_city.py
```

### 5. Run tests with pytest

```bash
pytest tests/ -v
```

## 🔐 SQL Injection Safety

The `city_kpi()` function uses **parameterized queries** (`WHERE city = ?`) instead of string formatting. This means an input like `"Mumbai' OR 1=1 --"` is treated as a literal city name — it matches **zero** rows instead of bypassing the filter.

## 📦 Dependencies

| Package | Purpose          |
|---------|------------------|
| pandas  | CSV → DataFrame  |
| pytest  | Unit testing     |

> SQLite is built into Python — no extra install needed!
