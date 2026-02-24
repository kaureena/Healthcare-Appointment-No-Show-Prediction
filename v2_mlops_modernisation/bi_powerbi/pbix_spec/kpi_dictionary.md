# KPI Dictionary

## Core KPIs
- **Total Appointments:** count of scheduled appointments
- **Total No-Shows:** count where `no_show_label = 1`
- **No-Show Rate:** no-shows / total appointments
- **Avg Lead Time:** average days between booking and appointment
- **SMS Coverage:** share of appointments where SMS reminder was sent
- **Avg Predicted Risk:** average predicted probability across appointments

## Risk KPIs
- **High Risk Appointments:** count where `risk_band` in {High, Critical}
- **High Risk Rate:** high risk appointments / total appointments

## Monitoring KPIs (from monitoring outputs)
- **Drift Warn / Alert Count:** derived from `reports/drift_report.csv`
- **Freshness Lag (days):** derived from `reports/monitoring_snapshot.csv`
- **API p95 latency (ms) / error rate:** derived from `reports/api_latency_daily.csv`
