# Architecture

This project is intentionally built as a **portfolio-grade** ML delivery with both analytics engineering and MLOps concerns.

## V1 vs V2
- **V1** focuses on: EDA → model building → evaluation → insights
- **V2** focuses on: data contracts → ETL → DQ gates → warehouse → training pipeline → registry → monitoring → API scaffold → BI exports

## Core principles
1. **Synthetic data only** — safe for public sharing
2. **Reproducible outputs** — everything can be regenerated with `make all`
3. **Quality-first** — DQ checks are explicit and documented
4. **Operational readiness** — drift + SLA + alerts are first-class outputs

## High-level flow (Mermaid)
```mermaid
flowchart LR
  A[Raw Data (synthetic)] --> B[ETL: staged]
  B --> C[ETL: curated + star schema]
  C --> D[(SQLite Warehouse)]
  C --> E[DQ Checks]
  C --> F[Model Training]
  F --> G[Model Registry]
  F --> H[Batch Inference]
  H --> I[Monitoring: Drift + SLA]
  G --> J[API Inference (FastAPI)]
```

## Components
### ETL
Location: `v2_mlops_modernisation/etl/`  
Outputs: `v2_mlops_modernisation/data/staged/`, `.../data/curated/`, `warehouse/warehouse.db`

### Data Quality
Location: `v2_mlops_modernisation/dq_data_quality/`  
Outputs: `v2_mlops_modernisation/reports/dq_report.html`, `dq_summary.json`

### ML pipeline
Location: `v2_mlops_modernisation/ml/`  
Outputs: `v2_mlops_modernisation/models/artifacts/` and `v2_mlops_modernisation/reports/`

### Monitoring
Location: `v2_mlops_modernisation/monitoring/`  
Outputs: monitoring snapshot + drift report + alerts register

---

## Build/Run sequence
1. Generate raw data: `make data`
2. Run ETL: `make etl`
3. Run DQ: `make dq`
4. Train model: `make train`
5. Run monitoring: `make monitor`
