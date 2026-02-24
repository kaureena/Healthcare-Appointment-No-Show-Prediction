# Error analysis (V1)

This report focuses on understanding:
- false positives: contacted patients who would have shown up
- false negatives: missed no-shows

## Practical use
Error analysis informs:
- whether to tighten threshold for a clinic with limited staff
- whether to add features (e.g., transport proxy, appointment complexity)

## Artefacts available
- Confusion matrices:
  - `outputs/tables/confusion_matrix_threshold_0_50.csv`
  - `outputs/tables/confusion_matrix_threshold_0_35.csv`
- Lift curve:
  - `outputs/figures/model_lift_curve.png`

## Suggested next step (V1)
Run a structured review with clinicians and operations:
- Validate whether the top-risk cohort looks clinically plausible
- Ensure the outreach policy is ethically acceptable

V2 adds monitoring of drift and fairness over time.
