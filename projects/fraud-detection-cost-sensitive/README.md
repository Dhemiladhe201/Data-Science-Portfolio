# Fraud detection: evaluating thresholds and error costs

This is a small, reproducible experiment separate from my MSc dissertation. The transactions are **synthetic**, created with scikit-learn. The goal is to understand why a fraud model's decision threshold should be judged against the cost of false alerts and missed fraud.

## Question
Given different costs for missing fraud and flagging a legitimate transaction, which classifier and probability threshold offer the lowest *illustrative* validation cost?

## Approach
- Generate 12,000 synthetic examples, approximately 1% fraud.
- Reserve stratified training, validation and test partitions (60/20/20).
- Fit a class-weighted logistic regression and random forest.
- Select the model and threshold **only from validation data**.
- Evaluate the selected combination once on the untouched test set.
- Report precision, recall, F1, ROC-AUC, average precision and assumed cost.

No scores here are bank performance estimates. Costs use **2,000 units per missed fraud** and **25 units per false alert**, not GBP values or empirically established losses.

## Run
```bash
python -m pip install -r projects/fraud-detection-cost-sensitive/requirements.txt
python projects/fraud-detection-cost-sensitive/train.py
python -m unittest discover -s projects/fraud-detection-cost-sensitive/tests -v
```

Outputs are written to `projects/fraud-detection-cost-sensitive/outputs/`. The experiment uses fixed random seeds. The outputs are generated locally, not committed as independent evidence.

## Limitations
Only synthetic data, one holdout split, arbitrary costs, no drift monitoring and no decisioning policy. The original dissertation has its own validation questions in [the methodology review](../../research-notes/dissertation-methodology-review.md).

**Next:** inspect threshold stability across repeated splits, use confidence intervals, and compare with the re-audited dissertation data when available.
