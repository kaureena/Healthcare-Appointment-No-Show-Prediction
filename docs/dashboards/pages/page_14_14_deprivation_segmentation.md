# Page 14 — Deprivation Segmentation

![Dashboard Page 14](<../../../v2_mlops_modernisation/bi_powerbi/exports/page_14_14_deprivation_segmentation.png>)

## Why this page exists
Deprivation index segmentation and outreach strategy.

### What you should get from this page
- Segments by deprivation bins and shows risk differences plus channel interactions.
- Supports community outreach strategy and transport/assistance programs.

---

## Visual inventory (minimum widget density enforced)
- **12 KPI tiles** (top band): demand, no-show rate, high-risk share, SMS coverage, lead time, model AUC, drift PSI, freshness, API latency & error.
- **Trend panels**: daily no-show rate and demand volume.
- **Risk donut**: distribution across Low/Medium/High/Critical risk bands.
- **Gauge**: SLA/score indicator (varies by page).
- **Heatmap**: slot/segment heatmap (varies by page).
- **Composition pie**: channel/type/status mix (varies by page).
- **Operational table**: leaderboard/worklist/issue register (varies by page).
- **Monitoring widget**: drift/latency/error/DQ stack/scatter map (varies by page).

---

## Recommended filters / slicers
- Date range (Appointment Date)
- Clinic (Clinic ID / Clinic Type / Region)
- Booking channel
- Appointment type
- Lead-time band
- Risk band (Low/Medium/High/Critical)
- SMS reminder sent (Yes/No)
- Demographics (Age band, Gender)

---

## Metrics and definitions (portfolio audit-friendly)
- `No‑show rate` = No‑shows / Total appointments
- `High+Critical share` = % of appointments in risk bands High or Critical
- `SMS coverage` = % of appointments with sms_reminder_sent = 1
- `Predicted risk` = predicted_no_show_proba (0–1)
- `Freshness lag (days)` = today − latest available curated date
- `PSI drift` = population stability index by feature (reference vs current window)
- `API p95 latency` and `API error rate` from monitoring snapshot/time series

---

## Operational actions (what a team should do next)
- Use **Risk worklist** to prioritize outreach (calls/SMS) when High/Critical volume exceeds capacity.
- Investigate **clinic or neighbourhood spikes** using drill-down pages (07, 08, 09).
- If drift PSI approaches warning thresholds, review **drift console** (18) and initiate retrain playbook (26).
- When DQ failures appear in raw, verify staged/curated pass rates and log the remediation in DQ issue triage (23).

---

## Data sources used
- `v2_mlops_modernisation/data/curated/fact_appointments.csv`
- `v2_mlops_modernisation/data/curated/dim_clinic.csv`
- `v2_mlops_modernisation/data/curated/dim_neighbourhood.csv`
- `v2_mlops_modernisation/reports/model_metrics.json`
- `v2_mlops_modernisation/reports/drift_report.csv`
- `v2_mlops_modernisation/reports/api_latency_daily.csv`
- `v2_mlops_modernisation/reports/monitoring_snapshot.csv`
- `v2_mlops_modernisation/reports/dq_summary.json`

> Note: This repository uses **synthetic data** designed to look and behave like real operational data while avoiding any real patient information.
