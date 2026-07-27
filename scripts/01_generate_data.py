"""
01_generate_data.py
--------------------
Simulates the RAW data an Analyst at a consulting firm (like FJ) would receive
from a US retail client considering expansion into new states, plus data
pulled from public sources (Census-style demographics) and a competitor
"scrape" (store counts/ratings).

In a real engagement this data would come from:
 - Client's internal sales systems (CSV/SQL export)
 - Public APIs (Census, BLS) 
 - Web scraping (competitor locations, reviews)

Since this environment has no network access, we generate statistically
realistic synthetic data so the FULL pipeline (extraction -> validation ->
modeling -> client deliverable) is still genuinely runnable end-to-end.
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

STATES = [
    "Texas", "Florida", "Georgia", "North Carolina", "Arizona", "Tennessee",
    "Ohio", "Colorado", "South Carolina", "Nevada", "Utah", "Indiana",
    "Missouri", "Alabama", "Kentucky", "Oklahoma", "Idaho", "Kansas",
    "Arkansas", "New Mexico"
]

n = len(STATES)

# ---- 1. Client's existing store performance (5 states client already operates in) ----
existing_states = STATES[:5]
existing_sales = pd.DataFrame({
    "state": existing_states,
    "store_count": np.random.randint(3, 12, size=5),
    "avg_annual_revenue_per_store": np.random.normal(1_450_000, 180_000, size=5).round(0),
    "avg_operating_margin": np.random.normal(0.14, 0.02, size=5).round(4),
})
existing_sales.to_csv(f"{OUT}/client_existing_stores.csv", index=False)

# ---- 2. Public demographic/economic data (Census/BLS style) for ALL candidate states ----
demographics = pd.DataFrame({
    "state": STATES,
    "population_2025_millions": np.round(np.random.uniform(1.5, 30, size=n), 2),
    "median_household_income": np.random.randint(48000, 92000, size=n),
    "population_growth_5yr_pct": np.round(np.random.uniform(-1, 12, size=n), 2),
    "unemployment_rate_pct": np.round(np.random.uniform(2.8, 6.5, size=n), 2),
    "urbanization_pct": np.round(np.random.uniform(45, 92, size=n), 1),
})
demographics.to_csv(f"{OUT}/public_demographics_raw.csv", index=False)

# ---- 3. "Scraped" competitor landscape data ----
competitor = pd.DataFrame({
    "state": STATES,
    "competitor_store_count": np.random.randint(5, 120, size=n),
    "avg_competitor_rating": np.round(np.random.uniform(3.2, 4.7, size=n), 2),
    "avg_competitor_price_index": np.round(np.random.uniform(0.85, 1.2, size=n), 2),  # 1.0 = market avg
})
# introduce a few messy/missing values on purpose, like real scraped data
competitor.loc[3, "avg_competitor_rating"] = np.nan
competitor.loc[7, "competitor_store_count"] = -1  # bad scrape artifact
competitor.to_csv(f"{OUT}/competitor_scrape_raw.csv", index=False)

# ---- 4. Commercial real estate cost data (client-provided or client-sourced) ----
real_estate = pd.DataFrame({
    "state": STATES,
    "avg_commercial_rent_per_sqft": np.round(np.random.uniform(12, 45, size=n), 2),
    "avg_buildout_cost": np.random.randint(180_000, 420_000, size=n),
})
real_estate.to_csv(f"{OUT}/real_estate_costs_raw.csv", index=False)

print("Raw data files generated in /data:")
for f in os.listdir(OUT):
    print(" -", f)
