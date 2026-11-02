# Tableau Public build guide (native workbook)

The earlier auto-generated Tableau workbook was **not compatible** with Tableau Public. It is not included here. Build a new workbook directly from the source CSV and let Tableau create its own connection and extract.

## 1. Connect to the CSV

1. Open **Tableau Public Desktop** and choose **Connect → Text File** (sometimes labeled **To a File → Text File**).
2. Choose `data/credit_card_portfolio_2025.csv`.
3. On the **Data Source** page, verify `Snapshot_Month` is a **Date**, numeric money fields are **Number (whole)**, and `Delinquent_Flag` is a number (0/1).
4. If the **Live / Extract** choice appears, select **Extract**. When you move to Sheet 1, follow prompts to create/save the extract. Tableau Public supports published **extracts**, not live connections.
5. Rename the data source **Synthetic Credit Card Portfolio | 2025**.

If your Tableau Public Desktop edition offers no manual extract control, still create a *new* workbook using its CSV connector, then use **File → Save to Tableau Public**; Tableau can create the required extract when publishing new file-based workbooks. Do not open the rejected legacy `.twb` / `.twbx`.

## 2. Make two calculated fields

Data pane → right-click → **Create Calculated Field**:

**Delinquency Rate** (format as Percentage, one decimal):

```
AVG([Delinquent_Flag])
```

**Average Monthly Spend per Account** (format as Currency):

```
SUM([Transaction_Volume_USD]) / COUNT([Account_ID])
```

Important: Do **not** multiply `AVG([Delinquent_Flag])` by 100 if you format it as **Percentage**. Otherwise Tableau will show 600% instead of 6%.

## 3. Create 9 worksheets

| Worksheet name | How to build it |
| --- | --- |
| KPI — Transaction Volume | Put `SUM(Transaction_Volume_USD)` on Text; currency format |
| KPI — Interest Income | Put `SUM(Interest_Income_USD)` on Text; currency format |
| KPI — Delinquency Rate | Put `Delinquency Rate` on Text; percentage format |
| KPI — Accounts | Put `Account_ID` on Text; change aggregation to **Count (Distinct)** |
| Monthly Spending | `MONTH(Snapshot_Month)` on Columns (continuous month or exact month), `SUM(Transaction_Volume_USD)` on Rows, Line |
| Monthly Delinquency | `MONTH(Snapshot_Month)` on Columns, `Delinquency Rate` on Rows, Line |
| Spend by Card Tier | `Card_Tier` on Rows, `SUM(Transaction_Volume_USD)` on Columns, Bar, sort descending |
| Delinquency by Risk | `Risk_Segment` on Rows, `Delinquency Rate` on Columns, Bar |
| Interest by Region | `Region` on Rows, `SUM(Interest_Income_USD)` on Columns, Bar |

**Check totals before proceeding:** $46.0M spending, $8.0M interest, 6.0% delinquency, and 3,000 accounts. The figures are deliberately modeled.

## 4. Assemble the dashboard

1. Create **New Dashboard**. Set the size to **Automatic** or approximately **1200 × 850**.
2. Add a text title: **Credit Card Portfolio | Revenue & Risk Analytics**.
3. Arrange the four KPI sheets in a row at the top.
4. Put Monthly Spending and Monthly Delinquency in the middle row.
5. Put Spend by Card Tier, Delinquency by Risk, and Interest by Region below.
6. Click the dashboard dropdown on the Card Tier and Region worksheets and select **Use as Filter** (or Dashboard → Actions → Add Action → Filter).
7. Add a footer: **Synthetic account-month data | 2025 | For portfolio demonstration only**.

`docs/design-preview.png` is a **mockup** for layout inspiration, not proof the dashboard is built.

## 5. Save, publish, and capture proof

1. Save the workbook from Tableau as a packaged `.twbx` if your edition offers that option; make sure the extract is embedded.
2. Publish to Tableau Public. Confirm the dashboard loads in a new browser tab and that filters work.
3. Download/save a verified Tableau workbook (if available) under a new `tableau/` folder in the repository.
4. Replace the static design preview **only after** you have a real Tableau screenshot, and label it as such.
5. Add a **Live Tableau Dashboard** link to `README.md`.

## Why we start from the CSV

The initial programmatically created workbook failed Tableau Public compatibility checks, including a non-extract connection. Connecting through Tableau Public natively and saving/publishing an extract avoids carrying forward the broken workbook structure.
