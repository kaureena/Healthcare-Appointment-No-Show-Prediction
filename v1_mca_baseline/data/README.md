# Data (V1)

This V1 track uses **synthetic, portfolio-safe data** designed to mimic operational appointment scheduling patterns.

## Datasets in this folder

### `data/raw/appointments_raw_sample.csv`
A *raw-ish* sample with intentional imperfections to demonstrate typical operational issues:
- some missing `gender`
- some missing `deprivation_index`

### `data/interim/appointments_interim_cleaned_sample.csv`
A cleaned intermediate view:
- missing genders mapped to `U` (Unknown)
- `deprivation_index` imputed using median (for baseline only)

### `data/staged_sample.csv`
The main staged dataset used for most V1 EDA and baseline modeling.

### `data/processed/features_processed_sample.csv`
A simplified feature table used by the baseline model scripts/tests.

### `data/external/holiday_calendar_sample.csv`
Synthetic calendar features to show how external data can be used for feature enrichment.

## Privacy note
All data is synthetic. No real patient data is included.

