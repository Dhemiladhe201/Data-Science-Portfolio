import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation import choose_threshold, classification_cost
from train import make_data

class EvaluationTests(unittest.TestCase):
    def test_costs(self):
        self.assertEqual(classification_cost([1,0], [0.1,0.9], 0.5), 2025.0)
    def test_validation_threshold(self):
        labels, scores = [1,0,1,0,0], [0.45,0.30,0.75,0.12,0.17]
        selected = choose_threshold(labels, scores)
        self.assertLessEqual(
            classification_cost(labels, scores, selected),
            classification_cost(labels, scores, 0.5)
        )
    def test_synthetic_prevalence(self):
        X, y = make_data(1000)
        self.assertEqual(X.shape, (1000,20))
        self.assertGreater(y.mean(), 0)
        self.assertLess(y.mean(), 0.05)

if __name__ == "__main__":
    unittest.main()
