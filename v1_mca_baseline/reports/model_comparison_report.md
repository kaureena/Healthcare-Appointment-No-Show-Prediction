# Model comparison report (V1)

This report compares baseline models in a consistent feature setup.

## Why compare more than one model?
- Logistic Regression is interpretable and stable.
- Gradient Boosting can capture non-linear effects (interactions).

## Results
See `outputs/tables/model_metrics_comparison.csv`

### Observations
- Logistic Regression slightly outperformed Gradient Boosting on this sample.
- Both are adequate for a baseline deliverable; V2 focuses on operationalisation rather than squeezing marginal AUC.

## Recommendation (V1)
- Use Logistic Regression as the **baseline** for transparency and governance.
- Use Gradient Boosting as a challenger model for later.

## Supporting artefacts
- `outputs/figures/model_comparison_roc_auc.png`
- `outputs/figures/model_roc_curve_best.png`
- `outputs/figures/model_pr_curve_best.png`
