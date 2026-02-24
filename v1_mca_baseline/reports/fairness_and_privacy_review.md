# Fairness and privacy review (V1)

## Privacy
All data here is synthetic and does not represent real patients.

## Fairness checks in V1
V1 performs a lightweight slice check on:
- gender
- region

Artefacts:
- `outputs/tables/fairness_slice_metrics.csv`
- `outputs/figures/fairness_gender_true_vs_outreach.png`

## How to interpret the slice table
- `true_no_show_rate`: observed rate per slice
- `predicted_outreach_rate`: how often the policy would contact that slice
- Compare rates to detect large imbalances

## Limitations
- This is not a full fairness audit (no counterfactual fairness, no causal analysis).
- V2 expands monitoring and introduces alerting thresholds for drift.

## Recommendation
Before any real deployment:
- involve clinical governance
- define acceptable outreach disparity thresholds
- ensure sensitive features are handled according to policy
