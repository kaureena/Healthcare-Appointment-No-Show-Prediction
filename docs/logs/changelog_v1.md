# V1 Changelog

This changelog tracks notable changes during the notebook-led analysis phase.

### 2013-04-01 — Project initiation
Added:
•	Initial project structure for analysis
•	Imported healthcare appointment dataset
•	Identified core fields: appointment_id, patient_id, clinic_id, appointment_datetime, no_show_flag
Outcome:
•	Established foundation for exploratory analysis

#### 2013-04-04 — Data exploration and profiling
Added:
•	Basic dataset profiling
•	Missing value inspection
•	Distribution analysis for key variables
Outcome:
•	Identified key data quality concerns and feature candidates

#### 2013-04-08 — Data cleaning and preprocessing
Added:
•	Datetime parsing for appointment and booking timestamps
•	Handling of missing and invalid values
•	Removal of corrupted records
•  Exported cleaned dataset to data/interim/appointments_cleaned.csv
Outcome:
•	Created cleaned dataset suitable for analysis

#### 2013-04-12 — Feature engineering
Added:
•	Added lead_time_days feature
•	Added appointment_day_of_week feature
•	Added appointment_hour feature
•	Added weekend indicator feature
Outcome:
•	Enhanced dataset with predictive features

#### 2013-04-16 — Exploratory data analysis
Added:
•	Analysed no-show rate by clinic
•	Analysed no-show rate by day of week
•	Analysed no-show rate by appointment time
•	Generated visualisations and charts
Outcome:
•	Identified patterns influencing attendance behaviour

#### 2013-04-21 — Feature evaluation
Added:
•	Performed correlation analysis
•	Evaluated feature impact on no-show prediction
Outcome:
•	Selected relevant features for predictive modelling

#### 2013-04-25 — Model development
Added:
•	Implemented Logistic Regression baseline model
•	Created training and validation workflow
Outcome:
•	Established baseline predictive performance

### 2013-04-28 — Model evaluation and documentation
Added:
•	Evaluated model performance
•	Interpreted model results
•	Documented modelling notebook
Outcome:
•	Finalised V1 modelling results

### 2013-04-30 — V1 completion
Added:
•	Saved final dataset and analysis outputs
•	Completed project documentation and evidence preparation
Outcome:
•	Completed V1 MCA portfolio analysis phase
