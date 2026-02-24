# Data quality notes (V1)

V1 is intended as an analysis baseline, so the DQ approach is descriptive rather than automated gating.

## Checks performed
- Required schema present (see `tests/test_schema.py`)
- No-show label is binary
- No-show rate in a realistic band (see `tests/test_label_rate.py`)
- Feature table sanity checks (`tests/test_feature_table.py`)

## Known limitations
- We do not run an automated expectation suite in V1.
- V2 adds: expectations, DQ reports (HTML/JSON), and an issue register.

## Data files relevant to DQ discussion
- `data/raw/appointments_raw_sample.csv` contains intentional missingness (gender, deprivation index)
- `data/interim/appointments_interim_cleaned_sample.csv` demonstrates simple cleaning choices
