-- SQLite warehouse schema (simplified)
-- Generated/maintained by ETL script.

-- Dimensions
CREATE TABLE IF NOT EXISTS dim_patient (
  patient_id TEXT PRIMARY KEY,
  gender TEXT,
  age INTEGER,
  age_band TEXT,
  chronic_conditions_avg REAL,
  disability_rate REAL,
  prior_no_show_avg REAL
);

CREATE TABLE IF NOT EXISTS dim_clinic (
  clinic_id TEXT PRIMARY KEY,
  clinic_type TEXT,
  daily_capacity INTEGER,
  clinic_region TEXT
);

CREATE TABLE IF NOT EXISTS dim_neighbourhood (
  neighbourhood_id TEXT PRIMARY KEY,
  region TEXT,
  lat REAL,
  lon REAL,
  deprivation_index REAL
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_key TEXT PRIMARY KEY,
  appointment_dow TEXT,
  date TEXT,
  year INTEGER,
  month INTEGER,
  month_name TEXT,
  week INTEGER
);

-- Fact
CREATE TABLE IF NOT EXISTS fact_appointments (
  appointment_id TEXT PRIMARY KEY,
  date_key TEXT,
  patient_id TEXT,
  clinic_id TEXT,
  neighbourhood_id TEXT,
  appointment_datetime TEXT,
  booking_datetime TEXT,
  appointment_type TEXT,
  booking_channel TEXT,
  lead_time_days INTEGER,
  lead_time_band TEXT,
  appointment_dow TEXT,
  appointment_hour INTEGER,
  appointment_is_weekend INTEGER,
  sms_reminder_sent INTEGER,
  prior_no_show_count INTEGER,
  prior_show_count INTEGER,
  age INTEGER,
  age_band TEXT,
  gender TEXT,
  chronic_conditions_count INTEGER,
  disability_flag INTEGER,
  deprivation_index REAL,
  clinic_type TEXT,
  daily_capacity INTEGER,
  region TEXT,
  clinic_region TEXT,
  no_show_label INTEGER
);
