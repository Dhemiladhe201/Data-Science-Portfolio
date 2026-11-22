import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_data import generate_sensor_data, add_past_features_and_target, split_by_time

class DataChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = add_past_features_and_target(generate_sensor_data(n_assets=20))

    def test_labels_include_both_classes(self):
        self.assertGreater(self.data["failure_next_7d"].sum(), 0)
        self.assertGreater((self.data["failure_next_7d"] == 0).sum(), 0)

    def test_time_splits_do_not_overlap(self):
        a, b, c = split_by_time(self.data)
        self.assertTrue(a["date"].max() < b["date"].min() < c["date"].min())

    def test_rolling_feature_uses_current_and_previous_rows_only(self):
        sample = self.data[self.data["asset_id"] == 1].head(1).iloc[0]
        self.assertAlmostEqual(sample["temperature_c"], sample["temperature_c_7d_avg"])

    def test_determinism(self):
        one = generate_sensor_data(n_assets=2, seed=42)
        two = generate_sensor_data(n_assets=2, seed=42)
        self.assertTrue(one.equals(two))

if __name__ == "__main__":
    unittest.main()
