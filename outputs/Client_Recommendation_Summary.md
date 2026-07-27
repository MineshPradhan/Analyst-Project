# Client Recommendation Summary
## US Market Expansion — Top Candidate States

**Prepared by:** Analyst Team
**Business question:** Which states offer the strongest opportunity for our client's next 3-5 store openings?

---

### Recommendation

Based on a weighted opportunity model (market size, growth, income,
competitive density, real-estate cost, and unemployment) combined with a
revenue-prediction model trained on the client's existing 5 stores, we
recommend prioritizing:

| Rank | State | Opportunity Score /100 | Predicted Revenue/Store | Est. Payback |
|---|---|---|---|---|
| 1 | Utah | 63.6 | ~$1.10M | 1.4 yrs |
| 2 | South Carolina | 61.5 | ~$1.32M | 1.1 yrs |
| 3 | Colorado | 60.1 | ~$0.91M | 2.3 yrs |
| 4 | Texas | 58.3 | ~$1.28M | 1.6 yrs |
| 5 | Nevada | 54.4 | ~$1.04M | 2.1 yrs |

### Why these states

- **Utah & Texas** combine strong population growth (>11% over 5 years) with
  still-manageable buildout costs — the fastest-growing, lowest-friction
  markets in the candidate set.
- **South Carolina** stands out on payback speed (~13 months) thanks to low
  real-estate costs and low competitive density (34 competitor locations vs.
  60-90 in most other candidates).
- **Colorado** has the largest population of the group but a longer payback
  window due to higher rent and buildout costs — a good second-wave market.

### Methodology (one paragraph, for the appendix)

Twenty candidate states were scored on six weighted factors normalized to a
0-100 scale; weights are adjustable in the accompanying Excel model. A linear
regression trained on the client's five existing stores' actual revenue
provides a directional revenue estimate per candidate state. **Caveat:** the
regression is trained on only 5 data points and should be treated as
illustrative pending review by a senior modeler and, ideally, more
historical data before being finalized for client sign-off.

### Deliverables

- `US_Expansion_Client_Model.xlsx` — full interactive model (Assumptions,
  Raw Data, Ranked Model tabs; live formulas; adjustable weights)
- Underlying Python/SQL pipeline (see project README) for full reproducibility
