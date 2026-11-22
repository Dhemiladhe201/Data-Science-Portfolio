# Dissertation methodology review

**Notebook reviewed:** `IMPROVING_CREDIT_CARD_FRAUD_DETECTION_THROUGH_COST_SENSITIVE_MACHINE_LEARNING.ipynb`

My original MSc project compared Logistic Regression, Random Forest and Support Vector Machines for credit-card fraud detection with substantial class imbalance. The notebook reports 19,963 rows, including only 27 labelled fraudulent transactions. With so few positive cases, an apparently small change in predictions can move precision, recall and cost estimates dramatically.

The notebook is retained unchanged. This document explains what I want to verify before treating any reported scores as reliable outside the original academic exercise.

## Issues found in the notebook

1. **SMOTE before the split.** One section fits `SMOTE(sampling_strategy=0.5)` to all features and labels before making the resampled train/test partitions. Synthetic neighbours derived from the same original samples can therefore be shared across development and evaluation.
2. **Undersampling before the split.** Another section balances the full dataset before splitting. This tests performance on an artificial class distribution, not the original rare-fraud population. The resulting precision and cost cannot be read as deployment estimates.
3. **Preprocessing before holdout selection.** Missing-value imputation and categorical encoding are performed on the complete table in the consolidated preparation step. Even if no labels are used, fitted imputers and encoders should be learned from training data only.
4. **Cross-validation on already resampled data.** The notebook uses ordinary `KFold` over datasets that were resampled outside the folds. For this problem, stratified folds with resampling inside each training fold are safer. With only 27 fraud observations, some folds can be unstable.
5. **Limited positive test cases.** An 80/20 split of 27 positives typically leaves about five or six fraud examples in the test set. A 100% score in a test with that few positive labels is not strong evidence of generalisation.
6. **Cost assumptions need context.** The notebook illustrates a cost of 1,000 units per false negative and 10 per false positive. These are illustrative assumptions, not measured bank losses. Cost comparisons must use the same unaltered holdout distribution for all models.

These concerns are methodological, not an accusation that the raw dataset or original observations are fabricated.

## Planned re-evaluation

- Verify the public data source, licence, label definition, duplicates, timestamp coverage and any user-level grouping.
- Make an untouched holdout from original observations *before* fitting imputers, encoders or samplers. Consider an out-of-time split if the source supports one.
- Use a single reproducible preprocessing pipeline and `StratifiedKFold`; fit any SMOTE/undersampling **inside the training fold** only.
- Compare simple baseline predictions, class-weighted models and fold-safe resampling at the **original** fraud prevalence.
- Report average precision (PR-AUC), ROC-AUC, precision/recall at selected thresholds, confusion matrices and plausible uncertainty ranges.
- Choose cost assumptions and decision thresholds on validation data, not the final test set.
- Discuss practical consequences of false alerts, limited case counts, dataset shift and any signs of leakage.

## What is already reproducible

The [companion synthetic-data experiment](../projects/fraud-detection-cost-sensitive/) illustrates separate training, validation and testing. It is **not** a re-run of the dissertation dataset and does not validate the dissertation's original scores.

## Limits

The original transactions CSV is not included in this repository. No claim is made here that the dissertation results have been independently reproduced on that data. A properly re-run analysis will be added only after data provenance and permission to share are established.
