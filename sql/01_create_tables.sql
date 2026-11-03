-- Raw tables for the credit card dashboard.
-- Columns are in the same order as the CSVs so \copy can load them by position.
-- Both tables are keyed on client_num.

DROP VIEW IF EXISTS vw_card_customer_weekly;
DROP TABLE IF EXISTS cc_detail;
DROP TABLE IF EXISTS cust_detail;

CREATE TABLE cust_detail (
    client_num              INTEGER PRIMARY KEY,
    customer_age            SMALLINT,
    gender                  VARCHAR(5),
    dependent_count         SMALLINT,
    education_level         VARCHAR(50),
    marital_status          VARCHAR(20),
    state_cd                VARCHAR(2),
    zipcode                 VARCHAR(10),   -- text on purpose, NJ/MA zips start with 0
    car_owner               VARCHAR(5),
    house_owner             VARCHAR(5),
    personal_loan           VARCHAR(5),
    contact                 VARCHAR(50),
    customer_job            VARCHAR(50),
    income                  INTEGER,
    cust_satisfaction_score SMALLINT
);

CREATE TABLE cc_detail (
    client_num            INTEGER NOT NULL REFERENCES cust_detail (client_num),
    card_category         VARCHAR(20),
    annual_fees           INTEGER,
    activation_30_days    SMALLINT,
    customer_acq_cost     INTEGER,
    week_start_date       DATE NOT NULL,
    week_num              VARCHAR(20),
    qtr                   VARCHAR(10),
    current_year          SMALLINT,
    credit_limit          NUMERIC(10,2),
    total_revolving_bal   INTEGER,
    total_trans_amt       INTEGER,
    total_trans_ct        INTEGER,
    avg_utilization_ratio NUMERIC(10,3),
    use_chip              VARCHAR(10),
    exp_type              VARCHAR(50),
    interest_earned       NUMERIC(10,2),
    delinquent_acc        SMALLINT,
    PRIMARY KEY (client_num, week_start_date)
);
