-- Reporting view for Tableau: one row per card record with the customer
-- attributes attached, plus the buckets the dashboard groups by.
-- Buckets are defined here (not in Tableau) so anything reading the view
-- gets the same age / income / utilization groups.

DROP VIEW IF EXISTS vw_card_customer_weekly;

CREATE VIEW vw_card_customer_weekly AS
SELECT
    c.client_num,
    c.week_start_date,
    CAST(REPLACE(c.week_num, 'Week-', '') AS INTEGER) AS week_no,  -- 'Week-12' sorts wrong as text
    c.qtr,
    c.card_category,
    c.annual_fees,
    c.activation_30_days,
    c.customer_acq_cost,
    c.credit_limit,
    c.total_revolving_bal,
    c.total_trans_amt,
    c.total_trans_ct,
    c.avg_utilization_ratio,
    CASE
        WHEN c.avg_utilization_ratio < 0.2 THEN '0-20%'
        WHEN c.avg_utilization_ratio < 0.4 THEN '20-40%'
        WHEN c.avg_utilization_ratio < 0.6 THEN '40-60%'
        WHEN c.avg_utilization_ratio < 0.8 THEN '60-80%'
        ELSE '80-100%'
    END AS utilization_band,
    c.use_chip AS payment_method,
    c.exp_type AS expense_type,
    c.interest_earned,
    c.delinquent_acc,
    d.customer_age,
    CASE
        WHEN d.customer_age < 30 THEN '20-29'
        WHEN d.customer_age < 40 THEN '30-39'
        WHEN d.customer_age < 50 THEN '40-49'
        WHEN d.customer_age < 60 THEN '50-59'
        ELSE '60+'
    END AS age_group,
    CASE d.gender WHEN 'F' THEN 'Female' WHEN 'M' THEN 'Male' ELSE 'Unknown' END AS gender,
    d.dependent_count,
    d.education_level,
    d.marital_status,
    d.state_cd,
    d.zipcode,
    d.customer_job,
    d.income,
    CASE
        WHEN d.income < 35000 THEN '$0-35K'
        WHEN d.income < 70000 THEN '$35K-70K'
        ELSE '$70K+'
    END AS income_group,
    d.car_owner,
    d.house_owner,
    d.personal_loan,
    d.cust_satisfaction_score
FROM cc_detail c
JOIN cust_detail d ON d.client_num = c.client_num;

-- Export for Tableau Public, which can't connect to Postgres.
-- (In Tableau Desktop you can connect to the view directly instead.)
\copy (SELECT * FROM vw_card_customer_weekly ORDER BY week_start_date, client_num) TO 'data/credit_card_weekly.csv' WITH (FORMAT csv, HEADER true)
