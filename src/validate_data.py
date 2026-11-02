"""Validate source grain and KPI arithmetic before publishing."""
from pathlib import Path
import pandas as pd

def validate(path: Path) -> dict:
    data=pd.read_csv(path,parse_dates=['Snapshot_Month'])
    assert len(data)==36_000, 'Expected 3,000 accounts x 12 months'
    assert data[['Account_ID','Snapshot_Month']].duplicated().sum()==0, 'Duplicate account-month grain'
    assert data['Account_ID'].nunique()==3000
    assert data['Snapshot_Month'].nunique()==12
    assert data['Transaction_Volume_USD'].sum()==46_000_000
    assert data['Interest_Income_USD'].sum()==8_000_000
    assert int(data['Delinquent_Flag'].sum())==2160
    assert (data['Delinquent_Flag']==(data['Days_Past_Due']>=30).astype(int)).all()
    assert (data[['Transaction_Volume_USD','Interest_Income_USD','Txn_Count','Ending_Balance_USD']]>=0).all().all()
    return {
        'account_months':int(len(data)),'accounts':int(data.Account_ID.nunique()),
        'transaction_volume_usd':int(data.Transaction_Volume_USD.sum()),
        'interest_income_usd':int(data.Interest_Income_USD.sum()),
        'delinquency_rate':float(data.Delinquent_Flag.mean()),
    }

if __name__=='__main__':
    print(validate(Path('data/credit_card_portfolio_2025.csv')))
