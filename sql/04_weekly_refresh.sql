-- Weekly refresh: append the new week, check it landed, re-export.
-- The view picks the new rows up on its own; Tableau just needs Data > Refresh.

SET datestyle TO 'ISO, DMY';

\copy cust_detail FROM 'data/raw/cust_add.csv' WITH (FORMAT csv, HEADER true)
\copy cc_detail FROM 'data/raw/cc_add.csv' WITH (FORMAT csv, HEADER true)

-- new week should be on top with a normal-looking row count
SELECT week_start_date, COUNT(*) AS card_records
FROM cc_detail
GROUP BY week_start_date
ORDER BY week_start_date DESC
LIMIT 3;

\copy (SELECT * FROM vw_card_customer_weekly ORDER BY week_start_date, client_num) TO 'data/credit_card_weekly.csv' WITH (FORMAT csv, HEADER true)
