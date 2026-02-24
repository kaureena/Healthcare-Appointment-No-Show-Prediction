# Evaluation strategy (V1)

## Why ROC-AUC is not enough
No-shows can be imbalanced; outreach policies care about the **top-risk** segment.

So we include:
- ROC-AUC
- Average Precision
- Calibration curve
- Lift / cumulative gain curve

## Threshold selection
Outreach threshold is a policy decision balancing:
- contact volume
- expected captured no-shows
- operational cost

See:
- `outputs/tables/confusion_matrix_threshold_0_50.csv`
- `outputs/tables/confusion_matrix_threshold_0_35.csv`
