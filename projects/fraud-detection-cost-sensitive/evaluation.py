"""Metrics for a cost-sensitive binary classification example."""
import numpy as np
from sklearn.metrics import (
    average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
)

def classification_cost(y_true, probabilities, threshold, fn_cost=2000, fp_cost=25):
    actual = np.asarray(y_true, dtype=int)
    predicted = (np.asarray(probabilities) >= threshold).astype(int)
    false_negatives = np.sum((actual == 1) & (predicted == 0))
    false_positives = np.sum((actual == 0) & (predicted == 1))
    return float(false_negatives * fn_cost + false_positives * fp_cost)

def choose_threshold(y_true, probabilities):
    """Use ONLY the validation split for this step."""
    candidates = np.linspace(0.01, 0.99, 99)
    return min(candidates, key=lambda t: (classification_cost(y_true, probabilities, t), t))

def score_model(y_true, probabilities, threshold):
    y_pred = (np.asarray(probabilities) >= threshold).astype(int)
    return {
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "average_precision": float(average_precision_score(y_true, probabilities)),
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "cost_units": classification_cost(y_true, probabilities, threshold),
        "threshold": float(threshold),
    }
