# Credit Card Revenue & Risk Analytics | Tableau + SQL + Python

**Portfolio project by Suhas Ramachandra** · Business intelligence · Financial analytics · Data quality

This project explores revenue and credit risk in a **synthetic** credit-card portfolio. It includes a reproducible dataset, validation checks, SQL analysis, summary reports, and a Tableau dashboard design.

**Status:** Data preparation, metrics, SQL analysis, and design preview are complete. **The interactive Tableau workbook is not published yet.** An earlier generated workbook was incompatible with Tableau Public and is intentionally **not included** in this release. The Tableau build guide documents how to create and publish a native workbook directly from the CSV.

![Static dashboard design preview](docs/design-preview.png)

*This is a design mockup created in Python, **not a screenshot or a working Tableau dashboard**.*

## The business question

How can a portfolio analyst monitor transaction volume and interest income while also spotting rising delinquency risk? This exercise puts financial performance and risk in one monthly review.

## Portfolio overview (modeled, 2025)

| KPI | Result | What it means |
| --- | ---: | --- |
| Transaction volume | **$46.0M** | Sum of monthly card spending |
| Interest income | **$8.0M** | Sum of monthly interest in synthetic data |
| Delinquency rate | **6.0%** | Share of account-months with 30+ days past due |
| Accounts | **3,000** | Distinct synthetic accounts |
| Observations | **36,000** | 3,000 accounts x 12 monthly snapshots |

These headline amounts were **intentionally set by the data generator**. They do not represent actual financial results, prediction accuracy, or observed bank performance.

## Key observations

- The modeled 30+ days-past-due rate increases from **5.33% in January** to **7.03% in December**, so an annual average alone obscures the trend.
- *Rewards* cards have the largest share of simulated annual transaction volume.
- Delinquency differs across risk groups **by design**, because the synthetic data generator models these differences.

**Analysis takeaway:** A useful portfolio review needs both revenue metrics and early risk indicators. See [the case study](docs/CASE_STUDY.md) for what can and cannot be concluded from the sample.

## What's in the repository

```text
Credit-Card-Revenue-Risk-Tableau/
├── data/credit_card_portfolio_2025.csv  # 36k synthetic monthly records
├── reports/                            # reproducible KPI summaries
├── sql/portfolio_analysis.sql          # example SQL analysis
├── src/generate_data.py                # reproducible data generation
├── src/validate_data.py                # data-quality and KPI checks
├── src/analyze_portfolio.py            # report generation
├── src/load_sqlite.py                  # build a local SQLite database
├── scripts/create_preview.py           # static design preview
├── docs/design-preview.png             # design mockup only
├── docs/DATA_DICTIONARY.md
├── docs/CASE_STUDY.md
├── docs/TABLEAU_BUILD_GUIDE.md
├── GITHUB_REPLACEMENT_STEPS.md         # Mac/GitHub publishing steps
└── tests/test_portfolio.py
```

## How to run

Requires Python 3.10+.

```bash
python3 -m pip install -r requirements.txt
python3 src/validate_data.py
python3 src/analyze_portfolio.py
python3 src/load_sqlite.py
python3 -m unittest discover -s tests -v
```

To recreate the original synthetic CSV, run `python3 src/generate_data.py`; it uses a fixed random seed. To regenerate the design image, run `python3 scripts/create_preview.py`.

## Rebuilding the dashboard in Tableau Public

Read [the Tableau build guide](docs/TABLEAU_BUILD_GUIDE.md). Start a **new workbook from the CSV**, choose **Extract** when available, and create the described sheets. The previous programmatically generated `.twb`/`.twbx` is omitted because Tableau Public rejected its connection. A successful native workbook and its Tableau Public link will be added after verification.

## Data integrity and metric notes

- One row = one account in one month (not an individual card purchase).
- Transaction volume and interest income can be added across months. **Do not sum monthly ending balances to claim total annual exposure.**
- Delinquency is `AVG(Delinquent_Flag)` for the selected account-months, **not** the percentage of unique people ever delinquent in the year.
- No confidential account information, production banking integration, or real customer data is included.

**Tech:** Tableau (planned dashboard), Python, Pandas, NumPy, SQL, SQLite, data validation, KPI reporting, financial analytics.
