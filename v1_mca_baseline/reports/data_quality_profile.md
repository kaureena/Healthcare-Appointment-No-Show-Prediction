# Data quality profile (V1)

V1 documents typical data quality risks and how they affect modeling.

## Common issues
1. Missing demographic fields (e.g., gender)
2. Inconsistent neighbourhood identifiers
3. Negative/zero lead time due to booking system errors
4. Duplicates (repeat booking events)

## What we do in V1
- Use `data/interim/appointments_interim_cleaned_sample.csv` to demonstrate basic cleaning.
- Keep a simple schema export: `data/data_schema.json`

## What V2 adds
- DQ expectations suite and automated reporting
- DQ gate: raw can fail; staged/curated must pass
