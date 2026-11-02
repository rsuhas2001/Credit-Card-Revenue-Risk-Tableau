"""Self-contained data quality and analysis checks. No Tableau workbook required."""
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from validate_data import validate
from analyze_portfolio import summaries

class TestPortfolio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics = validate(ROOT / 'data' / 'credit_card_portfolio_2025.csv')
        cls.s = summaries()

    def test_observation_grain(self):
        self.assertEqual(self.metrics['account_months'], 36000)
        self.assertEqual(self.metrics['accounts'], 3000)

    def test_kpi_totals(self):
        self.assertEqual(self.metrics['transaction_volume_usd'], 46_000_000)
        self.assertEqual(self.metrics['interest_income_usd'], 8_000_000)
        self.assertAlmostEqual(self.metrics['delinquency_rate'], .06)

    def test_monthly_rollup(self):
        m = self.s['monthly_kpis']
        self.assertEqual(len(m), 12)
        self.assertEqual(m.transaction_volume_usd.sum(), 46_000_000)
        self.assertEqual(m.interest_income_usd.sum(), 8_000_000)
        self.assertEqual(set(m.accounts.unique()), {3000})

    def test_segment_spend_reconciles(self):
        self.assertEqual(self.s['card_tier_performance'].transaction_volume_usd.sum(), 46_000_000)
        self.assertEqual(self.s['region_performance'].interest_income_usd.sum(), 8_000_000)

    def test_risk_rates_and_counts(self):
        risk = self.s['risk_segment_performance']
        self.assertEqual(risk.observations.sum(), 36000)
        self.assertEqual(risk.delinquent_observations.sum(), 2160)
        self.assertTrue(risk.delinquency_rate.between(0, 1).all())

    def test_sqlite_aggregation(self):
        import pandas as pd
        df = pd.read_csv(ROOT / 'data' / 'credit_card_portfolio_2025.csv')
        with sqlite3.connect(':memory:') as con:
            df.to_sql('account_months', con, index=False)
            result = con.execute('SELECT SUM(Transaction_Volume_USD), SUM(Interest_Income_USD), AVG(Delinquent_Flag) FROM account_months').fetchone()
        self.assertEqual(result[0], 46_000_000)
        self.assertEqual(result[1], 8_000_000)
        self.assertAlmostEqual(result[2], 0.06)

if __name__ == '__main__':
    unittest.main()
