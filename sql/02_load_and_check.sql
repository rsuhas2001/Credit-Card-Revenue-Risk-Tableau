-- Load the raw files and sanity-check them before building anything on top.
-- Run from the repo root:  psql -d ccdb -f sql/02_load_and_check.sql
-- (\copy reads files on the client side, so the relative paths work from there)

-- some exports have dd-mm-yyyy dates; DMY covers that and ISO dates load either way
SET datestyle TO 'ISO, DMY';

-- customers first, cc_detail has a foreign key to it
\copy cust_detail FROM 'data/raw/customer.csv' WITH (FORMAT csv, HEADER true)
\copy cc_detail FROM 'data/raw/credit_card.csv' WITH (FORMAT csv, HEADER true)

-- 1. row counts, should be one card record per customer
SELECT
    (SELECT COUNT(*) FROM cust_detail) AS customers,
    (SELECT COUNT(*) FROM cc_detail)   AS card_records;

-- 2. customers with no card record (the FK already blocks the reverse case)
SELECT COUNT(*) AS customers_without_card
FROM cust_detail d
LEFT JOIN cc_detail c ON c.client_num = d.client_num
WHERE c.client_num IS NULL;

-- 3. nulls / out-of-range values in fields the dashboard uses
SELECT
    COUNT(*) FILTER (WHERE total_trans_amt IS NULL)                    AS null_trans_amt,
    COUNT(*) FILTER (WHERE interest_earned IS NULL)                    AS null_interest,
    COUNT(*) FILTER (WHERE credit_limit IS NULL OR credit_limit <= 0)  AS bad_credit_limit,
    COUNT(*) FILTER (WHERE avg_utilization_ratio NOT BETWEEN 0 AND 1)  AS bad_utilization,
    COUNT(*) FILTER (WHERE delinquent_acc NOT IN (0, 1))               AS bad_delinquent_flag
FROM cc_detail;

-- 4. week coverage
SELECT
    MIN(week_start_date)            AS first_week,
    MAX(week_start_date)            AS last_week,
    COUNT(DISTINCT week_start_date) AS weeks
FROM cc_detail;
