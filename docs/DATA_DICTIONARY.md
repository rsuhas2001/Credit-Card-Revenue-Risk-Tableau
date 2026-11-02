# Metrics, grain, and data dictionary

## Grain
One row per **Account_ID + Snapshot_Month** (a monthly portfolio snapshot). The data includes 3,000 accounts and 12 months of 2025, giving 36,000 unique account-month records.

## KPI definitions

| Metric | Tableau expression | Interpretation |
|---|---|---|
| Transaction Volume | `SUM([Transaction_Volume_USD])` | Spending volume during the selected period |
| Interest Income | `SUM([Interest_Income_USD])` | Interest recorded during selected periods |
| Delinquency Rate (%) | `AVG([Delinquent_Flag]) * 100` | Share of account-month observations 30+ DPD |
| Active Accounts | `COUNTD([Account_ID])` | Unique modeled accounts in selected filter context |
| Average Spend per Account-Month | `SUM([Transaction_Volume_USD]) / COUNT([Account_ID])` | Average per observation, not per customer over a year |
| Transaction Count | `SUM([Txn_Count])` | Number of aggregated transactions in sample |

Create this Tableau calculated field when building the workbook: `Delinquency Rate (%) = AVG([Delinquent_Flag]) * 100`.

## Fields

| Field | Type | Description |
|---|---|---|
| Account_ID | String | Synthetic stable account identifier |
| Snapshot_Month | Date | First day of the reporting month |
| Region | String | Four modeled U.S. regions |
| Card_Tier | String | Essential, Rewards, Premium |
| Acquisition_Channel | String | Digital, Branch, Referral, Partner |
| Age_Group | String | Broad synthetic age category |
| Credit_Score_Band | String | Banded synthetic score classification |
| Risk_Segment | String | Low, Moderate, Elevated, High mapped to score band |
| Txn_Count | Integer | Number of transactions aggregated for that account-month |
| Transaction_Volume_USD | Integer | Monthly spending volume in USD |
| Interest_Income_USD | Integer | Monthly accrued interest in USD |
| Ending_Balance_USD | Integer | Modeled balance at month-end; non-additive over time |
| Credit_Limit_USD | Integer | Modeled credit limit; non-additive over time |
| Payment_Amount_USD | Integer | Modeled total payments during month |
| Days_Past_Due | Integer | Snapshot delinquency days |
| Delinquent_Flag | Integer | 1 when Days_Past_Due >= 30; otherwise 0 |

## Quality checks

- The primary key `(Account_ID, Snapshot_Month)` is unique.
- 36,000 account-month rows = 3,000 distinct accounts × 12 months.
- Transaction volume sums to **$46,000,000**.
- Interest income sums to **$8,000,000**.
- Delinquent flags sum to **2,160 / 36,000 = 6%**.
- All flags agree with the 30+ days-past-due definition.
- Financial and count fields are nonnegative.

## Data provenance

This is an original, seeded synthetic dataset created with `src/generate_data.py`. The metrics were intentionally calibrated to a fictional scenario. No data comes from a card issuer, customer account, banking partner, or real consumer.
