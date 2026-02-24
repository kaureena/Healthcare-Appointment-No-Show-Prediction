Project: Healthcare-Appointment-No-Show-Prediction
Author: Kaushal Chauhan
Structure: V1 (Analysis) + V2 (Modernisation)


V1 — Analysis Phase (MCA Portfolio)

-------Week 1
Period: 2013-04-01 → 2013-04-07
Focus: Data acquisition and familiarisation
Completed:
•	Obtained healthcare appointment dataset
•	Reviewed column definitions and business meaning
•	Identified key entities: patient_id, appointment_id, clinic_id
•	Performed initial data inspection
Outcome: Established understanding of appointment workflow and no-show context.

--------Week 2
Period: 2013-04-08 → 2013-04-14
Focus: Data cleaning and preprocessing
Completed:
•	Converted datetime fields
•	Handled missing and invalid values
•	Created lead_time and temporal features
•	Validated cleaned dataset
Outcome: Prepared dataset for analysis and modelling.

--------Week 3
Period: 2013-04-15 → 2013-04-21
Focus: Exploratory data analysis
Completed:
•	Analysed no-show rates by clinic, day, and lead time
•	Identified behavioural and operational patterns
•	Documented insights and trends
Outcome: Identified predictive signals for modelling.

---------Week 4
Period: 2013-04-22 → 2013-04-30
Focus: Initial predictive modelling
Completed:
•	Prepared modelling feature set
•	Trained Logistic Regression model
•	Evaluated performance
•	Interpreted feature importance
Outcome: Delivered baseline no-show prediction model.

V2 — Modernisation Phase
--------Week 1
Period: 2025-12-15 → 2025-12-21
Focus: Pipeline restructuring
Completed:
•	Designed modern repo structure
•	Built extract and transform pipeline
•	Implemented synthetic data generator
Outcome: Reproducible data pipeline established.

----------Week 2
Period: 2025-12-22 → 2025-12-28
Focus: Warehouse modelling
Completed:
•	Created dimension and fact tables
•	Built KPI tables
•	Exported data to SQLite warehouse
Outcome: Analytics-ready warehouse created.

------Week 3
Period: 2025-12-29 → 2026-01-04
Focus: Data quality governance
Completed:
•	Implemented DQ checks
•	Created issue register
•	Validated data integrity
Outcome: Governed and auditable data pipeline.

-------Week 4
Period: 2026-01-05 → 2026-01-15
Focus: ML pipeline and monitoring
Completed:
•	Built ML training pipeline
•	Saved model and metrics
•	Implemented monitoring and alerts
•	Created API scoring endpoint
Outcome: Operational ML and monitoring pipeline established.

