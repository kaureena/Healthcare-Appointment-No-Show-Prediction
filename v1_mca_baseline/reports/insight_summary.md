# Insight summary (V1)

This summary is derived from `data/staged_sample.csv` (**12,000 rows**, synthetic) and is designed to be **operationally actionable**.

---

## 1) Key drivers observed (with evidence)

### A) Lead time
Appointments booked far in advance tend to have higher no-show risk.

Evidence:
- Chart: `outputs/figures/eda_no_show_by_lead_time_band.png`
- In this sample (n≥200 per band):
  - Highest no-show band: **15-30** → **37.46%** (n=2149)
  - Lowest no-show band: **0** → **27.16%** (n=578)

### B) Booking channel
Booking channel behaves like a proxy for “friction” and planning behaviour.

Evidence:
- Chart: `outputs/figures/eda_no_show_by_booking_channel.png`
- Highest channel: **Online** → **36.18%** (n=3038)
- Lowest channel: **Walk-in** → **31.01%** (n=2980)

### C) Patient history
Prior no-shows are a strong behavioural signal.

Evidence:
- Chart: `outputs/figures/eda_no_show_vs_prior_no_show_count.png`
- Table: `outputs/tables/no_show_by_prior_no_show_count.csv`

### D) Deprivation index
Higher deprivation is correlated with higher no-show risk in this synthetic sample.

Evidence:
- Chart: `outputs/figures/eda_no_show_by_deprivation_decile.png`
- Table: `outputs/tables/no_show_by_deprivation_decile.csv`

---

## 2) Baseline model performance (V1)

V1 uses baseline models primarily to:
- produce a risk score for outreach ranking
- quantify lift and calibration

Best model (V1):
- ROC-AUC: **0.625**
- Avg Precision: **0.464**

Evidence:
- `outputs/figures/model_roc_curve_best.png`
- `outputs/figures/model_calibration_curve.png`
- `outputs/figures/model_lift_curve.png`

---

## 3) Operational recommendation (starter policy)

Use a 4-band outreach policy:
- **Low**: no action
- **Medium**: SMS reminder
- **High**: SMS + call attempt
- **Critical**: call + reschedule offer

See:
- Mermaid flow: `docs/mermaid/v1_outreach_policy.mmd`
- Threshold table: `outputs/tables/threshold_policy_table.csv`

---

## 4) Caveats (V1)

- Split is random; time-aware evaluation is handled in V2.
- V1 fairness checks are lightweight (slice metrics only).
- Causal claims are not made in V1; reminder effects should be validated via experiment design.
