# Case study: balancing portfolio revenue and delinquency risk

## Situation

A portfolio manager wants a concise monthly view of card spend and interest income, with risk signals that can be discussed alongside revenue. Separate finance and risk reports can make it difficult to decide where to investigate.

## Goal

Plan a simple Tableau decision interface that answers three questions: *How is the portfolio performing? Which segments contribute to revenue? Where is delinquency changing?*

## Data and model

The source is a reproducible synthetic monthly panel (3,000 accounts x 12 months). Because every row is an account-month, the dashboard can sum transaction volume and interest income while calculating the fraction of observations at least 30 days past due.

The planned dashboard will contain:

1. Four primary KPI sheets: spend, interest, delinquency rate, distinct accounts.
2. Monthly transaction volume trend.
3. Monthly delinquency trend.
4. Spend by card tier.
5. Delinquency by credit-risk segment.
6. Interest by region.

The fields and formula definitions are detailed in `DATA_DICTIONARY.md`.

## Observations from the synthetic scenario

- Spend totals **$46M** and interest income totals **$8M** across the modeled year.
- The overall account-month delinquency rate is **6.0%**.
- Delinquency increases from **5.33%** to **7.03%** from January to December, so the annual average masks a worsening modeled trend.
- The Rewards card tier contributes about **$18.5M** in annual spending.
- In the model, high-risk accounts are deliberately more likely to be past due; segment comparisons should be treated as a data generator behavior rather than real market evidence.

## Decision memo

**Recommendation 1 — Monitor trend rather than only annual average.** Review the 30+ DPD rate each month and investigate increases before they are obscured by the annual portfolio-level average.

**Recommendation 2 — Evaluate revenue with risk context.** When looking at card-tier spending or regional interest income, add 30+ DPD rate as a companion measure before reallocating promotional budgets.

**Recommendation 3 — Improve data maturity.** A real implementation would need account-level status transition analysis, charge-off data, recovery metrics, and cohort controls to support meaningful risk conclusions.

## Design decisions and limitations

- A single source table avoids join duplication for a small demonstration. A real issuer's production model would use separate account, transaction, billing and risk fact tables.
- Average of a 0/1 flag provides the correct account-month delinquency fraction, but it is not a unique borrower ever-delinquent rate.
- $46M / $8M are synthetic totals. The dataset is not an assessment of a real card issuer's performance.
- A business dashboard is descriptive. It does not support loan underwriting, credit-limit decisions, or causal claims about behavior.

## Extension plan

1. Add a second synthetic year for genuine YoY comparisons.
2. Add migration matrices between risk stages and 30/60/90+ DPD buckets.
3. Connect a permitted PostgreSQL source with scheduled extracts.
4. Run a controlled data-quality monitoring process before dashboard refreshes.
