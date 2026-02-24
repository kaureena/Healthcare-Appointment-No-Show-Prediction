# Feature engineering (V1)

## Feature families
1. **Patient history**
   - `prior_no_show_count`, `prior_show_count`, `chronic_conditions_count`
2. **Scheduling**
   - `lead_time_days`, `appointment_hour`, `appointment_dow`, `appointment_is_weekend`
3. **Access/Context**
   - `booking_channel`, `appointment_type`, `clinic_type`, `region`, `deprivation_index`
4. **Interventions**
   - `sms_reminder_sent`

## Encoding approach (baseline)
- Categorical: one-hot encoding
- Numerical: passed through (no scaling required for tree models; LR benefits from scaling but is acceptable for baseline)
