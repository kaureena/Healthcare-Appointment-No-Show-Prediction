# V2 Changelog

## [2026-02-10] — Modernisation milestone
- Implemented synthetic data generator with controlled defects (RAW layer)
- Built ETL pipeline: raw → staged → curated + SQLite warehouse
- Added DQ engine with 90 expectations + 36 rule docs; generated HTML/JSON reports
- Added ML training pipeline; exported model artifact, registry, metrics, and plots
- Added monitoring: drift PSI, freshness SLA, latency simulation, and alert register
- Added FastAPI inference scaffold and PBIX specification pack
