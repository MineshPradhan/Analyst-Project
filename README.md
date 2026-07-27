# US Market Expansion Analysis — Analyst Portfolio Project

A fully working, end-to-end project built to mirror exactly what an
Analyst/Sr. Analyst at a US-facing consulting firm does day to day:
turn messy multi-source data into a clean, defensible client recommendation.

**Business question:** *Which US state should our retail client expand into next?*

## Why this project matches the JD

| JD requirement | Where it's demonstrated |
|---|---|
| Python + SQL, data extraction/validation/combination | `scripts/01_generate_data.py`, `02_etl_sql.py` |
| Identifying data sources, database structures | SQLite schema joining demographics, competitor, real-estate tables |
| Quantitative & predictive modeling (under senior guidance) | `03_analysis_model.py` — weighted scoring model + linear regression |
| Complex Excel modeling | `04_build_excel_model.py` → `outputs/US_Expansion_Client_Model.xlsx` (live formulas, editable assumptions, chart) |
| Clear, actionable client recommendations | `outputs/Client_Recommendation_Summary.md` |

## How to run it end to end

```bash
cd scripts
python3 01_generate_data.py        # simulate raw client + public + scraped data
python3 02_etl_sql.py              # clean, validate, load to SQLite, join
python3 03_analysis_model.py       # opportunity score + revenue regression
python3 04_build_excel_model.py    # build client Excel deliverable
```

## Pipeline design

1. **Extraction** — four raw sources are pulled in: client's own store sales
   (5 existing states), public demographic/economic data (Census/BLS-style,
   all 20 candidate states), a competitor "scrape" (intentionally messy —
   one negative value, one missing value, to mirror real scraped data), and
   commercial real-estate cost data.
2. **Validation & combination** — `02_etl_sql.py` fixes the bad scrape
   artifact, imputes missing values with a documented median, runs sanity
   checks, then loads everything into SQLite and joins it into one clean
   analytical table with plain SQL.
3. **Modeling** — two models, deliberately kept transparent for a client
   audience:
   - A **weighted opportunity score** (market size, growth, income,
     competition, cost, unemployment) — fully editable weights.
   - A **linear regression** trained on the client's 5 existing stores,
     predicting expected revenue per store in each candidate state.
   - *Caveat documented in the model:* with only 5 existing stores as
     training data, the regression is illustrative — in a live engagement
     this would be flagged to a senior modeler and refined with more data
     or reviewed for overfitting before being client-facing.
4. **Deliverable** — a client-ready Excel workbook: an Assumptions tab
   (editable, color-coded per standard financial-model convention), a Raw
   Data tab, and a Ranked Model tab with live formulas and a bar chart —
   changing a weight in Assumptions recalculates the entire ranking.

## Files

```
data/        raw + cleaned CSVs, SQLite database
scripts/     01-04, run in order
outputs/     US_Expansion_Client_Model.xlsx, Client_Recommendation_Summary.md
```

## Extending this project for an interview

- Swap the synthetic data generator for a real free API (US Census API,
  BLS API, or a Kaggle retail dataset) once you have network access.
- Add a small Streamlit/Flask app so the client can adjust assumptions
  in a browser instead of Excel.
- Wire in an LLM call (Anthropic API) to auto-draft the executive summary
  paragraph from the ranked_states.csv output — directly demonstrates the
  "using LLMs and generative AI tools" JD line.
