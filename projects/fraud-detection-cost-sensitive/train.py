"""Compare models and hold out the test split until selection is complete."""
from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from evaluation import choose_threshold, score_model

ROOT = Path(__file__).resolve().parent
def make_data(n_samples=12000):
    X, y = make_classification(
        n_samples=n_samples, n_features=20, n_informative=8, n_redundant=3,
        weights=[0.99, 0.01], flip_y=0, random_state=42
    )
    return X, y

def main():
    X, y = make_data()
    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42
    )
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_dev, y_dev, stratify=y_dev, test_size=0.25, random_state=43
    )
    candidates = {
        "logistic_regression": make_pipeline(
            StandardScaler(), LogisticRegression(
                class_weight="balanced", max_iter=1000, random_state=42
            )
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=90, min_samples_leaf=2,
            class_weight="balanced_subsample", random_state=42, n_jobs=-1
        ),
    }
    validation_rows = []
    trained = {}
    for name, estimator in candidates.items():
        estimator.fit(X_train, y_train)
        valid_prob = estimator.predict_proba(X_valid)[:, 1]
        threshold = choose_threshold(y_valid, valid_prob)
        results = score_model(y_valid, valid_prob, threshold)
        validation_rows.append({"model": name, "split": "validation", **results})
        trained[name] = (estimator, threshold, results["cost_units"])

    winner = min(trained, key=lambda name: (trained[name][2], name))
    estimator, threshold, _ = trained[winner]
    test_prob = estimator.predict_proba(X_test)[:, 1]
    test_metrics = score_model(y_test, test_prob, threshold)

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    pd.DataFrame(validation_rows + [
        {"model": winner, "split": "held_out_test", **test_metrics}
    ]).to_csv(out / "metrics.csv", index=False)
    (out / "report.json").write_text(json.dumps({
        "data": "synthetic make_classification; not original MSc dataset",
        "class_distribution": {
            "train_fraud": int(np.sum(y_train)),
            "validation_fraud": int(np.sum(y_valid)),
            "test_fraud": int(np.sum(y_test))
        },
        "assumed_fn_cost_units": 2000,
        "assumed_fp_cost_units": 25,
        "chosen_on": "validation only",
        "model": winner,
        "test": test_metrics,
        "limitations": ["synthetic records", "one split", "illustrative costs"]
    }, indent=2))
    print("Model:", winner)
    print("Held-out test metrics:", test_metrics)

if __name__ == "__main__":
    main()
