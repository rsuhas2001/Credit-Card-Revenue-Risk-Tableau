-- Numbers to tie the dashboard back to. With no filters applied, the KPI
-- tiles in Tableau should match these.

-- headline KPIs
SELECT
    COUNT(DISTINCT client_num)                                             AS customers,
    SUM(total_trans_amt)                                                   AS transaction_amount,
    SUM(interest_earned)                                                   AS interest_earned,
    SUM(annual_fees + interest_earned)                                     AS revenue,
    ROUND(100.0 * SUM(delinquent_acc) / COUNT(DISTINCT client_num), 2)     AS delinquency_pct,
    ROUND(100.0 * SUM(activation_30_days) / COUNT(DISTINCT client_num), 2) AS activation_pct,
    ROUND(100.0 * SUM(total_revolving_bal) / SUM(credit_limit), 1)         AS utilization_pct
FROM vw_card_customer_weekly;

-- latest week vs prior week revenue (same logic as the Latest Week Revenue tile)
WITH weekly AS (
    SELECT week_start_date,
           SUM(annual_fees + interest_earned) AS revenue
    FROM vw_card_customer_weekly
    GROUP BY week_start_date
)
SELECT
    week_start_date,
    revenue,
    LAG(revenue) OVER (ORDER BY week_start_date) AS prior_week_revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY week_start_date))
          / LAG(revenue) OVER (ORDER BY week_start_date), 1) AS wow_pct
FROM weekly
ORDER BY week_start_date DESC
LIMIT 4;

-- delinquency by utilization band (the main chart on the risk page)
SELECT
    utilization_band,
    COUNT(*)                                         AS accounts,
    SUM(delinquent_acc)                              AS delinquent,
    ROUND(100.0 * SUM(delinquent_acc) / COUNT(*), 1) AS delinquency_pct,
    SUM(interest_earned)                             AS interest_earned
FROM vw_card_customer_weekly
GROUP BY utilization_band
ORDER BY utilization_band;
