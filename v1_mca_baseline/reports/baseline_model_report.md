# Baseline model report (V1)

## Dataset
- Source: `v1_mca_baseline/data/staged_sample.csv`
- Rows: **12,000**
- No-show rate: **34.1%**
- Note: dataset is **synthetic** but designed to mimic realistic scheduling and reminder patterns.

## Baseline models tested
1. Logistic Regression (one-hot encoded categoricals)
2. Gradient Boosting (same features)

## Metrics (holdout split, stratified 75/25)
See `outputs/tables/model_metrics_comparison.csv`

- Best ROC-AUC: **0.625**
- Best Average Precision: **0.464**

## Key evaluation artefacts
- ROC curve: `outputs/figures/model_roc_curve_best.png`
- Precision-Recall curve: `outputs/figures/model_pr_curve_best.png`
- Calibration curve: `outputs/figures/model_calibration_curve.png`
- Lift / cumulative gain: `outputs/figures/model_lift_curve.png`

## Threshold policy (outreach list)
Outreach is a policy decision. Below is a practical interpretation of three thresholds:

| Threshold | Outreach rate | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.50 | 9.70% | 0.560 | 0.159 | 0.248 |
| 0.35 | 43.63% | 0.439 | 0.561 | 0.492 |
| 0.25 | 77.33% | 0.373 | 0.847 | 0.518 |

See the full table in `outputs/tables/threshold_policy_table.csv`.

## Interpretability
For Logistic Regression, coefficient importances are exported:
- `outputs/tables/top_feature_coefficients_lr.csv`
- `outputs/figures/model_top_coefficients_lr.png`

Interpretation guidance:
- positive coefficient → higher predicted no-show risk
- negative coefficient → lower predicted no-show risk

## Limitations (V1)
- Random train/test split (not time-aware).
- Fairness checks are *lightweight* (slice metrics only).
- No operational monitoring in V1 (drift/latency/SLA added in V2).

