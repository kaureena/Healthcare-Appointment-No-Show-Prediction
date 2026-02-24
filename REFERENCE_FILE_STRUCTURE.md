# Reference File Structure

This repo follows the same style used for the earlier portfolio repositories (Library and Gujarat), with a stronger MLOps focus.

## Top-level
- `docs/` — portfolio documentation, mermaid diagrams, evidence index
- `v1_mca_baseline/` — baseline analysis + modelling + insight reports
- `v2_mlops_modernisation/` — modern data + MLOps pipeline, DQ, monitoring, API, warehouse

## docs/
- `docs/mermaid/` — editable diagrams (>=10)
- `docs/screenshots/` — run evidence images
- `docs/dashboards/` — dashboard documentation (page-level)

## v2_mlops_modernisation/
- `scripts/` — data generation
- `etl/` — raw → staged → curated + warehouse load
- `dq_data_quality/` — DQ expectations + rules + engine
- `ml/` — training + evaluation + inference
- `monitoring/` — drift + SLA + alerts
- `api/` — FastAPI inference scaffold
- `warehouse/` — schema + SQLite db + dictionary
- `bi_powerbi/` — pbix specification + exports folder
- `reports/` — generated artefacts (metrics, plots, DQ html, monitoring snapshots)
