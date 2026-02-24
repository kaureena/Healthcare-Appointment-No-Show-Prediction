# Problem statement (V1)

## Prediction target
Binary label: `no_show_label` (1 = appointment missed).

## Prediction time
At booking time (or at reminder time) we want a risk score that supports actions.

## Model output
- Probability of no-show (0–1)
- Recommended outreach bucket (Low / Medium / High / Critical)

## Evaluation goals (V1)
- Performance: ROC-AUC / Average Precision
- Operational: lift & capture of no-shows at top risk percentiles
- Reliability: calibration curve (predicted vs observed)
