# Data README

## Source
This project uses a **synthetic appointment dataset** generated locally (no real patient data).

Generator:
- `v2_mlops_modernisation/scripts/make_sample_data.py`

## Main tables
### Raw
- `v2_mlops_modernisation/data/raw/appointments_raw.csv`

Raw contains controlled data defects to demonstrate realistic DQ gates (e.g., invalid neighbourhood codes, duplicates, out-of-range ages, negative lead times).

### Staged
- `v2_mlops_modernisation/data/staged/appointments_staged.csv`

Staged is the cleaned version used for modelling and warehouse loading.

### Curated (Star schema)
- `v2_mlops_modernisation/data/curated/fact_appointments.csv`
- `v2_mlops_modernisation/data/curated/dim_patient.csv`
- `v2_mlops_modernisation/data/curated/dim_clinic.csv`
- `v2_mlops_modernisation/data/curated/dim_neighbourhood.csv`
- `v2_mlops_modernisation/data/curated/dim_date.csv`

Curated includes engineered features:
- lead time bands
- appointment weekday/hour
- prior no-show count
- sms reminder flag
- neighbourhood deprivation index
- predicted risk probability and risk band (after training)

## Warehouse
SQLite warehouse:
- `v2_mlops_modernisation/warehouse/warehouse.db`

Schema is documented in:
- `v2_mlops_modernisation/warehouse/schema.sql`
- `v2_mlops_modernisation/warehouse/data_dictionary.md`

## Privacy & ethics
Even though data is synthetic, we treat it as healthcare-adjacent:
- No direct identifiers
- No attempt to re-identify
- Model monitoring includes fairness slices
