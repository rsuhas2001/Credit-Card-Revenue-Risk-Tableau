"""Load the synthetic account-month CSV into a local SQLite database for SQL demos."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_database(csv_path=None, db_path=None):
    csv_path = Path(csv_path or (ROOT / 'data' / 'credit_card_portfolio_2025.csv'))
    db_path = Path(db_path or (ROOT / 'data' / 'credit_card_portfolio.sqlite'))
    df = pd.read_csv(csv_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        df.to_sql('account_months', con, if_exists='replace', index=False)
        con.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_account_month ON account_months(Account_ID, Snapshot_Month)')
        con.execute('CREATE INDEX IF NOT EXISTS ix_month ON account_months(Snapshot_Month)')
    return db_path

if __name__ == '__main__':
    out = load_database()
    print(f'Created SQLite database at {out} (excluded from GitHub by .gitignore)')
