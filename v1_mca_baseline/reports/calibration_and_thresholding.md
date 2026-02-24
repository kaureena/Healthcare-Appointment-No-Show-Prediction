# Calibration and thresholding (V1)

## Why calibration matters
Outreach policies use *probabilities* to decide who to contact. If probabilities are not calibrated,
the risk bands can mislead operations.

## Artefacts
- Calibration curve: `outputs/figures/model_calibration_curve.png`
- Calibration bins: `outputs/tables/calibration_bins.csv`

## Thresholding
We provide three candidate thresholds for different outreach capacities.

- 0.50 → small, high-confidence list
- 0.35 → medium volume, balanced capture
- 0.25 → high volume, high capture (low precision)

See:
- `outputs/tables/threshold_policy_table.csv`
- `outputs/tables/confusion_matrix_threshold_0_50.csv`
- `outputs/tables/confusion_matrix_threshold_0_35.csv`

## Operational guidance
A common approach:
1. Start with 0.35
2. Measure outreach capacity (calls/SMS/day)
3. Adjust threshold weekly to match capacity while monitoring captured no-shows.

