import sys
import unittest
import sqlite3
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from generate_data import generate

class ReportingTests(unittest.TestCase):
    def test_revenue_reconciles(self):
        with tempfile.TemporaryDirectory() as directory:
            db = generate(Path(directory) / "retail.db", customers=90, orders=500)
            with sqlite3.connect(db) as conn:
                query = (ROOT/"sql"/"01_monthly_revenue.sql").read_text()
                total = sum(row[3] for row in conn.execute(query))
                expected = conn.execute(
                    "SELECT SUM(amount_gbp) FROM orders WHERE status='completed'"
                ).fetchone()[0]
                self.assertLess(abs(total-expected), 0.2)
    def test_cohort_retention_within_100_percent(self):
        with tempfile.TemporaryDirectory() as directory:
            db = generate(Path(directory) / "retail.db", customers=90, orders=500)
            with sqlite3.connect(db) as conn:
                query = (ROOT/"sql"/"04_cohort_retention.sql").read_text()
                rows = conn.execute(query).fetchall()
                self.assertTrue(rows)
                self.assertTrue(all(0 <= row[-1] <= 100 for row in rows))

if __name__ == "__main__":
    unittest.main()
