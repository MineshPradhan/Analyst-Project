"""
02_etl_sql.py
-------------
Data extraction, VALIDATION, and combination step (per JD: "Identifying
information sources... developing the optimal approach for data extraction,
validation, and combination" + "Employing Python and SQL").

Loads the 4 raw CSVs, cleans them, loads into SQLite, and uses SQL joins to
build one clean analytical table.
"""
import pandas as pd
import numpy as np
import sqlite3
import os

BASE = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(BASE, "data")
DB_PATH = os.path.join(DATA, "expansion_analysis.db")

# ---------- Load ----------
existing = pd.read_csv(f"{DATA}/client_existing_stores.csv")
demo = pd.read_csv(f"{DATA}/public_demographics_raw.csv")
comp = pd.read_csv(f"{DATA}/competitor_scrape_raw.csv")
re_ = pd.read_csv(f"{DATA}/real_estate_costs_raw.csv")

# ---------- VALIDATE & CLEAN ----------
issues = []

# fix bad scrape artifact (negative store count is impossible)
bad_count = comp["competitor_store_count"] < 0
if bad_count.any():
    issues.append(f"Fixed {bad_count.sum()} negative competitor_store_count value(s)")
    comp.loc[bad_count, "competitor_store_count"] = np.nan

# impute missing values with column median (documented assumption)
for col in ["avg_competitor_rating", "competitor_store_count"]:
    n_missing = comp[col].isna().sum()
    if n_missing:
        med = comp[col].median()
        issues.append(f"Imputed {n_missing} missing '{col}' with median ({med:.2f})")
        comp[col] = comp[col].fillna(med)

# sanity range checks
assert demo["unemployment_rate_pct"].between(0, 30).all(), "Unemployment rate out of range"
assert demo["population_2025_millions"].gt(0).all(), "Non-positive population found"

print("Validation log:")
for i in issues:
    print(" -", i)

# ---------- LOAD into SQLite ----------
conn = sqlite3.connect(DB_PATH)
existing.to_sql("client_existing_stores", conn, if_exists="replace", index=False)
demo.to_sql("demographics", conn, if_exists="replace", index=False)
comp.to_sql("competitor", conn, if_exists="replace", index=False)
re_.to_sql("real_estate", conn, if_exists="replace", index=False)

# ---------- COMBINE via SQL join ----------
query = """
SELECT
    d.state,
    d.population_2025_millions,
    d.median_household_income,
    d.population_growth_5yr_pct,
    d.unemployment_rate_pct,
    d.urbanization_pct,
    c.competitor_store_count,
    c.avg_competitor_rating,
    c.avg_competitor_price_index,
    r.avg_commercial_rent_per_sqft,
    r.avg_buildout_cost
FROM demographics d
JOIN competitor c ON d.state = c.state
JOIN real_estate r ON d.state = r.state
ORDER BY d.state;
"""
combined = pd.read_sql_query(query, conn)
conn.close()

combined.to_csv(f"{DATA}/combined_clean.csv", index=False)
print(f"\nCombined analytical table -> {DATA}/combined_clean.csv  ({len(combined)} states)")
print(combined.head())
