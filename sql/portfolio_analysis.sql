-- Credit Card Revenue & Risk Analysis (SQLite)
-- Data grain: one account in one month. All data is synthetic.
-- Load the database with: python3 src/load_sqlite.py
-- Then run: sqlite3 data/credit_card_portfolio.sqlite < sql/portfolio_analysis.sql

-- 1. Overall portfolio: simulated 2025 totals and account-month delinquency.
SELECT
    COUNT(*) AS account_months,
    COUNT(DISTINCT Account_ID) AS accounts,
    SUM(Transaction_Volume_USD) AS spend_usd,
    SUM(Interest_Income_USD) AS interest_usd,
    ROUND(100.0 * AVG(Delinquent_Flag), 2) AS delinquency_rate_pct
FROM account_months;

-- 2. Month-by-month revenue and risk trends.
SELECT
    substr(Snapshot_Month, 1, 7) AS snapshot_month,
    SUM(Transaction_Volume_USD) AS spend_usd,
    SUM(Interest_Income_USD) AS interest_usd,
    ROUND(100.0 * AVG(Delinquent_Flag), 2) AS delinquency_rate_pct
FROM account_months
GROUP BY substr(Snapshot_Month, 1, 7)
ORDER BY snapshot_month;

-- 3. Spend share by card tier.
WITH tier_totals AS (
    SELECT Card_Tier, SUM(Transaction_Volume_USD) AS spend_usd
    FROM account_months GROUP BY Card_Tier
)
SELECT Card_Tier, spend_usd,
    ROUND(100.0 * spend_usd / SUM(spend_usd) OVER (), 2) AS portfolio_share_pct
FROM tier_totals ORDER BY spend_usd DESC;

-- 4. Risk segments: the modeled delinquency distribution.
SELECT Risk_Segment, COUNT(*) AS account_months,
    SUM(Delinquent_Flag) AS delinquent_account_months,
    ROUND(100.0 * AVG(Delinquent_Flag), 2) AS delinquency_rate_pct
FROM account_months GROUP BY Risk_Segment
ORDER BY delinquency_rate_pct DESC;

-- 5. Regional interest and spending.
SELECT Region, SUM(Interest_Income_USD) AS interest_usd,
    SUM(Transaction_Volume_USD) AS spend_usd,
    ROUND(100.0 * AVG(Delinquent_Flag), 2) AS delinquency_rate_pct
FROM account_months GROUP BY Region ORDER BY interest_usd DESC;

-- 6. Data quality: this should return zero rows.
SELECT Account_ID, Snapshot_Month, COUNT(*) AS duplicate_count
FROM account_months
GROUP BY Account_ID, Snapshot_Month HAVING COUNT(*) > 1;
