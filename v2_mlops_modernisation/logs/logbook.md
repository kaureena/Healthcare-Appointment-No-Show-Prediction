# V2 Logbook

This logbook captures V2 implementation notes and operational assumptions.

## Decisions
- Use controlled RAW defects to demonstrate DQ gates (without hiding upstream realities).
- Promote a star-schema curated layer for BI and ML reuse.
- Use explicit expectation JSONs + rule docs to keep DQ auditable.
- Use PSI drift for lightweight drift checks and alerting.

## Outputs
- Warehouse: `warehouse/warehouse.db`
- DQ reports: `reports/dq_report.html`, `reports/dq_summary.json`
- ML: `models/artifacts/best_model.joblib`, `reports/model_metrics.json`
- Monitoring: `reports/drift_report.csv`, `reports/alerts_register.csv`

## Notes
Dashboard PNG exports are generated in a later full release pack to keep this milestone zip lean.
