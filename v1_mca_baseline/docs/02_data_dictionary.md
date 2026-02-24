# Data dictionary (V1)

The primary dataset is `data/staged_sample.csv`.

## Key columns (selection)

| Column | Meaning | Notes |
|---|---|---|
| `appointment_datetime` | time of appointment | used to derive DOW/hour features |
| `booking_datetime` | time of booking | used to derive lead time |
| `lead_time_days` | (appointment - booking) in days | strong signal in EDA |
| `prior_no_show_count` | prior missed appointments | historically strongest signal |
| `sms_reminder_sent` | reminder sent flag | intervention variable |
| `deprivation_index` | neighbourhood index (0–1) | synthetic socioeconomic proxy |
| `daily_capacity` | clinic capacity | used for demand/capacity narrative |
| `no_show_label` | target | 1=no show |

See also `data/data_schema.json`.
