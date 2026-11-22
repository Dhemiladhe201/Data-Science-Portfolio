"""Time-ordered predictive-maintenance example using simulated sensor records."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, fbeta_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from generate_data import SENSOR_COLUMNS, add_past_features_and_target, generate_sensor_data, split_by_time

BASE = Path(__file__).resolve().parent
FEATURES = SENSOR_COLUMNS + [c + "_7d_avg" for c in SENSOR_COLUMNS]
TARGET = "failure_next_7d"

def results(y, probabilities, threshold):
    predictions = (np.asarray(probabilities) >= threshold).astype(int)
    false_alarms = int(((np.asarray(y) == 0) & (predictions == 1)).sum())
    return {
        "threshold": round(float(threshold), 3),
        "precision": round(float(precision_score(y, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y, predictions, zero_division=0)), 4),
        "f2": round(float(fbeta_score(y, predictions, beta=2, zero_division=0)), 4),
        "average_precision": round(float(average_precision_score(y, probabilities)), 4),
        "roc_auc": round(float(roc_auc_score(y, probabilities)), 4),
        "false_alarms_per_100_asset_days": round(100.0 * false_alarms / len(y), 3),
        "positive_days": int(np.sum(y)),
        "evaluated_days": int(len(y)),
    }

def choose_threshold(y, probabilities):
    choices = np.linspace(0.10, 0.90, 17)
    return float(max(choices, key=lambda t: (
        fbeta_score(y, np.asarray(probabilities) >= t, beta=2, zero_division=0),
        -t
    )))

def main():
    data = add_past_features_and_target(generate_sensor_data())
    train, validation, test = split_by_time(data)
    models = {
        "logistic_regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=120, min_samples_leaf=5,
            class_weight="balanced_subsample", random_state=42, n_jobs=-1
        )
    }
    comparison = []
    fitted = {}
    for name, model in models.items():
        model.fit(train[FEATURES], train[TARGET])
        probabilities = model.predict_proba(validation[FEATURES])[:, 1]
        threshold = choose_threshold(validation[TARGET], probabilities)
        scores = results(validation[TARGET], probabilities, threshold)
        comparison.append({"model": name, "period": "validation", **scores})
        fitted[name] = (model, threshold, scores["f2"])
    winner = max(fitted, key=lambda k: (fitted[k][2], k))
    winner_model, threshold, _ = fitted[winner]
    test_probabilities = winner_model.predict_proba(test[FEATURES])[:, 1]
    test_scores = results(test[TARGET], test_probabilities, threshold)
    comparison.append({"model": winner, "period": "test", **test_scores})
    output = BASE / "outputs"
    output.mkdir(exist_ok=True)
    pd.DataFrame(comparison).to_csv(output / "model_comparison.csv", index=False)
    report = {
        "source": "simulated asset histories; not real manufacturing data",
        "split": "chronological with seven-day embargo",
        "selected_model": winner,
        "threshold_selected_on": "validation period only",
        "test_metrics": test_scores,
        "limitations": "Simulator-only performance; not validated on industrial assets"
    }
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
