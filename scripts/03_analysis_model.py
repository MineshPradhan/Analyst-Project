"""
03_analysis_model.py
---------------------
Quantitative analysis (per JD: "Conducting quantitative and qualitative
analyses... developing predictive models").

Two models:
  1. A transparent WEIGHTED OPPORTUNITY SCORE (0-100) ranking every
     candidate state — the kind of clear, defensible model a client
     stakeholder can understand in a meeting.
  2. A linear regression trained on the client's 5 existing stores,
     used to PREDICT expected annual revenue per store in each new state.

Output: ranked_states.csv used to build the Excel model & client deck.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

BASE = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(BASE, "data")

combined = pd.read_csv(f"{DATA}/combined_clean.csv")
existing = pd.read_csv(f"{DATA}/client_existing_stores.csv")
demo_existing = pd.read_csv(f"{DATA}/public_demographics_raw.csv")
re_existing = pd.read_csv(f"{DATA}/real_estate_costs_raw.csv")
comp_existing = pd.read_csv(f"{DATA}/competitor_scrape_raw.csv")

# ---------------- MODEL 1: Weighted Opportunity Score ----------------
df = combined.copy()

def normalize(s, invert=False):
    n = (s - s.min()) / (s.max() - s.min())
    return 1 - n if invert else n

df["score_market_size"]   = normalize(df["population_2025_millions"])
df["score_growth"]        = normalize(df["population_growth_5yr_pct"])
df["score_income"]        = normalize(df["median_household_income"])
df["score_low_competition"] = normalize(df["competitor_store_count"], invert=True)
df["score_low_cost"]      = normalize(df["avg_commercial_rent_per_sqft"] + df["avg_buildout_cost"]/1000, invert=True)
df["score_low_unemployment"] = normalize(df["unemployment_rate_pct"], invert=True)

WEIGHTS = {
    "score_market_size": 0.20,
    "score_growth": 0.20,
    "score_income": 0.15,
    "score_low_competition": 0.20,
    "score_low_cost": 0.15,
    "score_low_unemployment": 0.10,
}
df["opportunity_score"] = sum(df[k] * w for k, w in WEIGHTS.items()) * 100
df["opportunity_score"] = df["opportunity_score"].round(1)

# ---------------- MODEL 2: Revenue Prediction (Linear Regression) ----------------
# Build training set: join existing 5 states' sales with their demo/re/comp features
train = (existing
         .merge(demo_existing, on="state")
         .merge(re_existing, on="state")
         .merge(comp_existing, on="state"))

features = ["population_2025_millions", "median_household_income",
            "population_growth_5yr_pct", "competitor_store_count",
            "avg_commercial_rent_per_sqft"]

X_train = train[features].fillna(train[features].median())
y_train = train["avg_annual_revenue_per_store"]

model = LinearRegression()
model.fit(X_train, y_train)

X_all = df[features].fillna(df[features].median())
df["predicted_revenue_per_store"] = model.predict(X_all).round(0)

# Simple payback estimate: buildout cost / (predicted revenue * assumed 14% margin)
df["est_annual_profit_per_store"] = (df["predicted_revenue_per_store"] * 0.14).round(0)
df["est_payback_years"] = (df["avg_buildout_cost"] / df["est_annual_profit_per_store"]).round(2)

df_sorted = df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)
df_sorted.insert(0, "rank", df_sorted.index + 1)

out_cols = ["rank", "state", "opportunity_score", "predicted_revenue_per_store",
            "est_annual_profit_per_store", "est_payback_years",
            "population_2025_millions", "population_growth_5yr_pct",
            "median_household_income", "competitor_store_count",
            "avg_commercial_rent_per_sqft", "avg_buildout_cost"]

df_sorted[out_cols].to_csv(f"{DATA}/ranked_states.csv", index=False)

print("Model R^2 on training data (5 existing stores):", round(model.score(X_train, y_train), 3))
print("\nTop 5 recommended expansion states:\n")
print(df_sorted[out_cols].head(5).to_string(index=False))
