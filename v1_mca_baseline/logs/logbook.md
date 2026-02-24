# V1 Logbook

This logbook captures V1 decisions, work notes, and scope boundaries.

## Decisions
- Use a staged sample to keep V1 lightweight and reproducible.
- Use Logistic Regression baseline to keep interpretability and fast iteration.
- Focus on operationally relevant drivers: SMS reminders, lead time, prior no-shows.

## Outputs
- EDA charts: `outputs/figures/eda_*.png`
- Baseline report: `reports/baseline_model_report.md`
- Baseline metrics: `reports/baseline_model_metrics.json`

## Notes
V1 is intentionally simpler; V2 adds quality gates, warehouse, monitoring and API scaffolding.
