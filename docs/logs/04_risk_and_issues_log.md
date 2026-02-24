# 04 — Risk and issues log

| ID   | Type | Description | Impact | Likelihood | Mitigation | Status |
|------|------|-------------|--------|------------|------------|--------|
| R-01 | Data | Synthetic demo data may not fully reflect real healthcare attendance behaviour | Medium | High | Provide configurable ingestion to replace synthetic data with real datasets | Accepted |
| R-02 | Data | Appointment ID not globally unique across all records | High | Medium | Create composite appointment_key using appointment_id and patient_id | Mitigated |
| R-03 | Data Quality | Patient demographic attributes (e.g. gender) inconsistent across visits | High | Low | Apply deterministic selection rule and log inconsistencies in DQ report | Monitoring |
| R-04 | Architecture | SQLite warehouse lacks enterprise scalability and concurrency features | Medium | Low | Use SQLite for portfolio; document migration path to PostgreSQL or SQL Server | Accepted |
| R-05 | Model | Model performance may degrade over time due to behavioural drift | High | Medium | Implement monitoring, drift detection, and retraining pipeline | Open |
| R-06 | Model | Time leakage risk if future appointments included in training | High | Low | Enforce time-based split strategy in training pipeline | Mitigated |
| R-07 | Integration | Power BI connectivity depends on correct ODBC driver configuration | Low | Medium | Provide setup documentation and tested connection workflow | Mitigated |
| R-08 | API | FastAPI scoring endpoint lacks authentication and access control | Medium | Low | Document as demo-only; add authentication layer in production version | Planned |
| R-9 | Governance | Lack of historical version tracking for model and predictions | Medium | Medium | Implement model registry and run_id version tracking | Planned |
| R-10 | Pipeline | ETL pipeline failure may produce incomplete warehouse tables | High | Low | Add validation checks, logging, and DQ gating between layers | Mitigated |
| R-11 | Documentation | Users may misinterpret synthetic data as real healthcare data | Low | Medium | Clearly document synthetic data provenance in repo and reports | Mitigated |