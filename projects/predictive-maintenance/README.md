# Predictive maintenance: early warning from sensor readings

This project grew out of my interest in industrial operations and the process-monitoring work I encountered during my chemical engineering training. The question is straightforward: can recent equipment readings identify machines that are more likely to fail in the next seven days?

The data is **simulated**. I have not used internal Nigeria Bottling Company records, and the results are not evidence of performance on real factory machines.

## What the project does

- Simulates daily readings for 40 industrial assets across 2025, including temperature, vibration, pressure and occasional failures.
- Builds seven-day rolling indicators using current and **past** sensor data.
- Predicts whether a failure will occur in the **next seven days**, excluding the current day.
- Splits data chronologically with seven-day gaps to reduce overlap between forecast windows.
- Compares a balanced logistic regression with a random forest.
- Selects the model and warning threshold on validation data only, then evaluates on the held-out test period.
- Reports average precision (PR-AUC), ROC-AUC, recall, precision, F2 and the number of false alerts per 100 asset-days.

## Run from this project folder

```bash
python -m pip install -r requirements.txt
python train.py
python -m unittest discover -s tests -v
```

Outputs are written to `outputs/` and excluded from version control.

## Why the evaluation matters

Predicting an upcoming failure has an operational cost on both sides. Missed failures can cause downtime, but repeated false alarms can waste maintenance time. This example uses F2 to favour recall during threshold selection, then also reports the actual number of false alerts. In a real deployment I'd agree on the trade-off with engineering and maintenance teams rather than assume a universal threshold.

## Limitations and next steps

All records are generated from one simulator, so a good score may reflect the simulator's assumptions. The project does not handle censored maintenance events, equipment replacement, seasonal drift, multiple sites or different asset criticalities. Next steps would include back-testing across several time periods, calibration checks and testing against an appropriately licensed real reliability dataset.

**Tools:** Python, NumPy, pandas, scikit-learn, chronological validation and model evaluation.
