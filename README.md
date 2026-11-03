# Credit Card Revenue & Risk Dashboard (Tableau)

Weekly view of a credit card portfolio: what it earns, where the spend goes, and which customers are most likely to fall behind on payments. Built in Tableau on top of a PostgreSQL reporting view.

This is the Tableau version of my [Power BI credit card dashboard](https://github.com/rsuhas2001/Credit_Card_Financial_Dashboard). Same business questions, but the data prep now lives in SQL and the metrics are Tableau calculated fields.

<!-- Tableau Public link goes here -->

## Dashboards

**Revenue Overview** – revenue, transaction amount, interest earned and latest-week revenue vs the week before, a weekly trend, and splits by card category, expense type and payment method.

**Customers & Risk** – customer count, delinquency rate, credit utilization and 30-day activation, delinquency by utilization band and income group, plus revenue by age group, state and job.

A **Metric** selector at the top switches the trend and breakdown charts between revenue, transaction amount and interest earned (the risk charts always show delinquency). Quarter, card category and gender filters apply across both pages.

![Revenue Overview](images/revenue_overview.png)
![Customers & Risk](images/customers_risk.png)

## Headline numbers (2023, all customers)

| Metric | Value |
|---|---|
| Customers | 10,108 |
| Transaction amount | $46.0M |
| Interest earned | $8.0M |
| Revenue (annual fees + interest) | $10.2M |
| Delinquency rate | 6.1% |
| 30-day activation rate | 57.5% |
| Credit utilization | 25.7% |

## What the data shows

- **Utilization is the clearest risk signal.** Delinquency goes from 2.4% for accounts under 20% utilization to 23.6% for accounts above 80%, close to 10x.
- **Interest income and risk sit in the same accounts.** Accounts above 40% utilization are about 30% of customers but earn 63% of interest income, and their delinquency runs 9–24%.
- **Lower income, higher risk.** 10.2% delinquency for incomes under $35K vs 4.5% at $70K+.
- **Premium cards punch above their weight.** Blue is 90.5% of customers but 80.5% of revenue. Silver, Gold and Platinum accounts earn more than twice Blue's interest per account ($1,560–2,310 vs $700, mostly from higher limits) and go delinquent less often (4.7% Silver, 0.9% Gold vs 6.3% Blue).
- **Revenue is concentrated geographically.** Texas, New York and California make up 67% of revenue. Q4 was the strongest quarter, about 12% above Q1.

## How it's built

```
data/raw/*.csv  ->  PostgreSQL tables  ->  vw_card_customer_weekly (view)  ->  data/credit_card_weekly.csv  ->  Tableau
```

The rule I followed: **groupings live in SQL, metrics live in Tableau.**

The view (`sql/03_reporting_view.sql`) joins card and customer records on `client_num`, renames a couple of columns, turns `Week_Num` text like `Week-12` into an integer so weeks sort properly, and adds the age group, income group and utilization band buckets. Because the buckets are defined once in SQL, any tool that reads the view uses the same groups.

Tableau Public can't connect to Postgres, so the workbook reads a CSV export of the view. In Tableau Desktop you can point the data source at the view directly.

`sql/05_kpi_tieout.sql` has the same KPIs written in SQL (including week-over-week with `LAG`) so the dashboard numbers can be checked against the database.

## Calculated fields

| Field | Formula |
|---|---|
| Revenue | `[Annual Fees] + [Interest Earned]` |
| Customers | `COUNTD([Client ID])` |
| Delinquency Rate | `SUM([Delinquent Flag]) / COUNTD([Client ID])` |
| Activation Rate | `SUM([Activated 30 Days]) / COUNTD([Client ID])` |
| Credit Utilization | `SUM([Revolving Balance]) / SUM([Credit Limit])` |
| Latest Week | `{ FIXED : MAX([Week Start]) }` |
| Latest Week Revenue | `SUM(IF [Week Start] = [Latest Week] THEN [Revenue] END)` |
| Prior Week Revenue | `SUM(IF [Week Start] = DATE(DATEADD('week', -1, [Latest Week])) THEN [Revenue] END)` |
| WoW Change | `([Latest Week Revenue] - [Prior Week Revenue]) / [Prior Week Revenue]` |

`Selected Metric` drives the trend and breakdown charts, switched by the `Metric` parameter:

```
CASE [Metric]
WHEN "Revenue" THEN SUM([Revenue])
WHEN "Transaction Amount" THEN SUM([Transaction Amount])
WHEN "Interest Earned" THEN SUM([Interest Earned])
END
```

A few decisions worth explaining:

- **Revenue = annual fees + interest.** Transaction amount is tracked as its own metric. Adding it into revenue (fees + spend + interest) gives $56.1M, but that counts customers' spending as the issuer's income.
- **Credit utilization is a ratio of sums.** Averaging each account's ratio gives 27.3% and treats a $1,500 limit the same as a $30,000 one. Total balance over total limit gives 25.7%.
- **The Quarter filter is a context filter.** FIXED LOD expressions are computed before regular filters, so without context, picking Q2 would still look for the last week of December and the latest-week tile would come up blank. With Quarter in context, `Latest Week` becomes the last week of whatever is selected.

## Data

Synthetic data, no real customers. 10,108 customers with weekly records across 53 weeks of 2023 (weeks start on Sunday).

| File | What's in it |
|---|---|
| `data/raw/credit_card.csv` | Card record per customer: card category, annual fee, credit limit, revolving balance, spend, transaction count, utilization, interest earned, 30-day activation, delinquency flag, week |
| `data/raw/customer.csv` | Customer attributes: age, gender, income, job, education, marital status, state, dependents |
| `data/raw/cc_add.csv`, `cust_add.csv` | Week 53 records, loaded separately to show the weekly refresh |
| `data/credit_card_weekly.csv` | Export of the reporting view (what the workbook reads) |

## Running it

**Just the dashboard:** open `Credit_Card_Revenue_Risk.twbx` in Tableau Desktop or Tableau Public. The data is packaged inside.

**Rebuilding the data** (run from the repo root, the `\copy` paths are relative):

```bash
createdb ccdb
psql -d ccdb -f sql/01_create_tables.sql
psql -d ccdb -f sql/02_load_and_check.sql
psql -d ccdb -f sql/03_reporting_view.sql
psql -d ccdb -f sql/04_weekly_refresh.sql
psql -d ccdb -f sql/05_kpi_tieout.sql
```

`04_weekly_refresh.sql` is the weekly step: append the new week, check it landed, re-export. To pick it up in Tableau, point the data source at the new `data/credit_card_weekly.csv` (Data > Edit Connection) and refresh.

## Repo layout

```
├── Credit_Card_Revenue_Risk.twbx    packaged workbook (data included)
├── data/
│   ├── raw/                         source files + week 53 add-on files
│   └── credit_card_weekly.csv       reporting view export
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_load_and_check.sql        load + data quality checks
│   ├── 03_reporting_view.sql        join, buckets, CSV export
│   ├── 04_weekly_refresh.sql        append new week, re-export
│   └── 05_kpi_tieout.sql            KPIs in SQL to check the dashboard against
└── images/                          dashboard screenshots
```

**Tools:** PostgreSQL, Tableau
