"""Generate clear, reproducible summary CSV reports from the synthetic portfolio."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "credit_card_portfolio_2025.csv"
REPORTS = ROOT / "reports"


def summaries(path=DATA):
    df = pd.read_csv(path, parse_dates=["Snapshot_Month"])
    monthly = (df.groupby("Snapshot_Month", as_index=False)
        .agg(transaction_volume_usd=("Transaction_Volume_USD", "sum"),
             interest_income_usd=("Interest_Income_USD", "sum"),
             delinquency_rate=("Delinquent_Flag", "mean"),
             accounts=("Account_ID", "nunique")))
    tier = (df.groupby("Card_Tier", as_index=False)
        .agg(transaction_volume_usd=("Transaction_Volume_USD", "sum"),
             interest_income_usd=("Interest_Income_USD", "sum"),
             delinquency_rate=("Delinquent_Flag", "mean")))
    risk = (df.groupby("Risk_Segment", as_index=False)
        .agg(observations=("Account_ID", "size"),
             delinquent_observations=("Delinquent_Flag", "sum"),
             delinquency_rate=("Delinquent_Flag", "mean")))
    region = (df.groupby("Region", as_index=False)
        .agg(transaction_volume_usd=("Transaction_Volume_USD", "sum"),
             interest_income_usd=("Interest_Income_USD", "sum"),
             delinquency_rate=("Delinquent_Flag", "mean")))
    return {"monthly_kpis": monthly, "card_tier_performance": tier,
            "risk_segment_performance": risk, "region_performance": region}


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    for name, frame in summaries().items():
        path = REPORTS / (name + ".csv")
        frame.to_csv(path, index=False, date_format="%Y-%m-%d")
        print(f"Wrote {len(frame)} rows to {path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
