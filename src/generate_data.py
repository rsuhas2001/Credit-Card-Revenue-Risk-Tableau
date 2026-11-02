"""Create a deterministic, synthetic monthly credit-card account portfolio.

This is not bank data. Metric totals are targets for a portfolio demonstration.
Each row represents one account in one snapshot month, not one transaction.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20261102
N_ACCOUNTS = 3000
MONTHS = pd.date_range('2025-01-01', periods=12, freq='MS')
TARGET_SPEND = 46_000_000
TARGET_INTEREST = 8_000_000
MONTHLY_DELINQUENT_COUNTS = [160, 162, 167, 172, 175, 178, 182, 184, 187, 189, 193, 211]  # total: 2160 / 36k = 6%


def allocate_exact(raw: np.ndarray, target: int) -> np.ndarray:
    """Apportion nonnegative raw weights into integer currency units with exact sum."""
    scaled = np.maximum(raw, 0.0000001) / np.maximum(raw.sum(), 1e-9) * target
    base = np.floor(scaled).astype(np.int64)
    residue = target - int(base.sum())
    if residue:
        # stable deterministic tie break
        order = np.argsort(-(scaled - base), kind='stable')
        base[order[:residue]] += 1
    return base


def generate(output: Path) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    accounts = pd.DataFrame({
        'Account_ID': [f'ACC-{i:05d}' for i in range(1, N_ACCOUNTS + 1)],
        'Region': rng.choice(['Northeast', 'Midwest', 'South', 'West'], N_ACCOUNTS, p=[.26,.22,.30,.22]),
        'Card_Tier': rng.choice(['Essential', 'Rewards', 'Premium'], N_ACCOUNTS, p=[.45,.37,.18]),
        'Acquisition_Channel': rng.choice(['Digital', 'Branch', 'Referral', 'Partner'], N_ACCOUNTS, p=[.43,.26,.18,.13]),
        'Age_Group': rng.choice(['18-29','30-44','45-59','60+'], N_ACCOUNTS, p=[.19,.36,.29,.16]),
        'Credit_Score_Band': rng.choice(['Below 620','620-679','680-739','740+'], N_ACCOUNTS, p=[.11,.24,.37,.28]),
    })
    accounts['Risk_Segment'] = accounts['Credit_Score_Band'].map({'Below 620':'High','620-679':'Elevated','680-739':'Moderate','740+':'Low'})
    tier_mult = accounts['Card_Tier'].map({'Essential':.72,'Rewards':1.11,'Premium':1.67}).to_numpy()
    score_mult = accounts['Credit_Score_Band'].map({'Below 620':.85,'620-679':.98,'680-739':1.08,'740+':1.14}).to_numpy()
    credit_limit = accounts['Card_Tier'].map({'Essential':8000,'Rewards':16000,'Premium':28000}).to_numpy() * rng.uniform(.85,1.25,N_ACCOUNTS)
    risk_priority = accounts['Risk_Segment'].map({'Low':.1,'Moderate':.7,'Elevated':1.7,'High':2.9}).to_numpy()
    rows = []
    for month_idx, dt in enumerate(MONTHS):
        seasonality = [0.88,0.85,0.94,0.97,1.01,1.02,1.05,1.04,1.03,1.11,1.16,1.29][month_idx]
        spending_weight = rng.gamma(2.9, 1., N_ACCOUNTS) * tier_mult * score_mult * seasonality
        # A little month-to-month persistence without storing a sensitive profile
        revolving = rng.uniform(.38,.87,N_ACCOUNTS)
        balance = np.rint(credit_limit * revolving).astype(int)
        interest_weight = balance * rng.uniform(.014,.022,N_ACCOUNTS) * (1 + .08*month_idx/11)
        payments = np.rint(np.maximum(0, balance*rng.uniform(.08,.24,N_ACCOUNTS))).astype(int)
        txn_count = np.maximum(1, rng.poisson(11 * tier_mult * seasonality)).astype(int)
        # More elevated-risk accounts tend to be delinquent, plus incidental noise.
        delinq_score = risk_priority + rng.normal(0,1.2,N_ACCOUNTS) + .10*month_idx/11
        k = MONTHLY_DELINQUENT_COUNTS[month_idx]
        delinquent = np.zeros(N_ACCOUNTS,dtype=int)
        delinquent[np.argsort(delinq_score,kind='stable')[-k:]] = 1
        past_due = np.where(delinquent == 1, rng.integers(31,96,N_ACCOUNTS), rng.choice([0,0,0,0,0,8,17,25],N_ACCOUNTS))
        base = accounts.copy()
        base['Snapshot_Month'] = dt.strftime('%Y-%m-%d')
        base['Txn_Count'] = txn_count
        base['spend_weight'] = spending_weight
        base['interest_weight'] = interest_weight
        base['Ending_Balance_USD'] = balance
        base['Credit_Limit_USD'] = np.rint(credit_limit).astype(int)
        base['Payment_Amount_USD'] = payments
        base['Days_Past_Due'] = past_due
        base['Delinquent_Flag'] = delinquent
        rows.append(base)
    df = pd.concat(rows,ignore_index=True)
    df['Transaction_Volume_USD'] = allocate_exact(df.pop('spend_weight').to_numpy(),TARGET_SPEND)
    df['Interest_Income_USD'] = allocate_exact(df.pop('interest_weight').to_numpy(),TARGET_INTEREST)
    df = df[['Account_ID','Snapshot_Month','Region','Card_Tier','Acquisition_Channel','Age_Group',
             'Credit_Score_Band','Risk_Segment','Txn_Count','Transaction_Volume_USD','Interest_Income_USD',
             'Ending_Balance_USD','Credit_Limit_USD','Payment_Amount_USD','Days_Past_Due','Delinquent_Flag']]
    output.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(output,index=False)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('data/credit_card_portfolio_2025.csv'))
    args=parser.parse_args()
    df=generate(args.output)
    print(f'Saved {len(df):,} account-month rows, {df.Account_ID.nunique():,} accounts')
    print(f'Spend ${df.Transaction_Volume_USD.sum():,}; interest ${df.Interest_Income_USD.sum():,}; delinquency {df.Delinquent_Flag.mean():.1%}')
