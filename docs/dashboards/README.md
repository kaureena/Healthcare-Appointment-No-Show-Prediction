# Dashboard Documentation (V2)

This directory documents the 30 planned dashboard pages for the V2 modernisation track.

## Page list
- **Page 01 — executive_overview**: Executive overview of demand, no-show rate, risk bands, and SLA status.
- **Page 02 — demand_capacity**: Demand vs capacity by clinic and time-of-day.
- **Page 03 — no_show_drivers**: Feature driver view: lead time, prior history, deprivation, channel.
- **Page 04 — sms_impact**: Reminder coverage and measured impact on no-show rates.
- **Page 05 — lead_time_heatmap**: Heatmap of no-show rate by lead-time band and DOW.
- **Page 06 — dow_hour_heatmap**: No-show heatmap by weekday x hour.
- **Page 07 — clinic_performance_leaderboard**: Clinic leaderboard with KPIs and risk mix.
- **Page 08 — neighbourhood_hotspots**: Map-like scatter hotspots using lat/lon with risk intensity.
- **Page 09 — risk_worklist_top200**: Operational worklist for high/critical risk appointments.
- **Page 10 — appointment_type_mix**: Pie/donut composition by appointment type and channel.
- **Page 11 — booking_channel_trends**: Channel share trend and no-show rate trend.
- **Page 12 — age_and_equity_slices**: Age bands and fairness/equity slices (illustrative).
- **Page 13 — prior_history_segmentation**: Segments by prior no-show count and effect on risk.
- **Page 14 — deprivation_segmentation**: Deprivation index segmentation and outreach strategy.
- **Page 15 — threshold_tuning**: Model threshold tuning panel for ops trade-offs.
- **Page 16 — model_performance**: ROC/PR/Confusion summary panels.
- **Page 17 — monitoring_overview**: Monitoring overview: drift, freshness, latency, alerts.
- **Page 18 — drift_console**: PSI drift table, trend lines, drill-down by feature.
- **Page 19 — freshness_sla**: Freshness gauges and pipeline refresh audit.
- **Page 20 — api_latency_and_errors**: Latency percentiles and error rates with incident markers.
- **Page 21 — alert_register**: Alert register with severity and status.
- **Page 22 — dq_quality_overview**: DQ pass/fail summary and top failing rules.
- **Page 23 — dq_issue_triage**: Issue register and triage workflow.
- **Page 24 — pipeline_health**: Pipeline run register and SLA compliance.
- **Page 25 — model_registry**: Registry overview of model runs and metrics.
- **Page 26 — retrain_playbook**: Retrain triggers and runbook summary.
- **Page 27 — what_if_simulator**: What-if scenario cards for SMS and lead-time policies.
- **Page 28 — cohort_retention**: Cohort style follow-up adherence (illustrative).
- **Page 29 — ops_actions_tracker**: Ops action tracker and impact measurement plan.
- **Page 30 — pipeline_health_and_model_monitoring**: Combined NOC page: drift + SLA + latency + risk mix.

PNG exports will be generated under: `v2_mlops_modernisation/bi_powerbi/exports/`.
