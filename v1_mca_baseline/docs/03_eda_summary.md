# EDA summary (V1)

This document explains the main EDA outputs and how to interpret them.

## Figures
- `outputs/figures/eda_no_show_by_booking_channel.png`
- `outputs/figures/eda_no_show_by_appointment_type.png`
- `outputs/figures/eda_no_show_by_lead_time_band.png`
- `outputs/figures/eda_no_show_vs_prior_no_show_count.png`
- `outputs/figures/eda_no_show_by_deprivation_decile.png`
- `outputs/figures/eda_no_show_daily_timeseries.png`

## Typical patterns observed
1. **Long lead times** correlate with higher no-show rate.
2. **Prior no-shows** are a strong behavioural predictor.
3. Reminder channels (SMS) correlate with lower no-show rate (causal inference is *not* claimed in V1).
4. Deprivation index is correlated with higher risk (used as a proxy — ethics note in `reports/fairness_and_privacy_review.md`).

## Caveats
- Correlation ≠ causation.
- Synthetic data is designed for portfolio demonstration; real-world deployment requires clinical governance and approvals.
