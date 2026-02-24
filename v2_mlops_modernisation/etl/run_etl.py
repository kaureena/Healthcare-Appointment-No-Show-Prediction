"""
ETL runner (V2): raw -> staged -> curated (star schema) -> SQLite warehouse.

Design goals:
- Reproducible and portfolio-safe (synthetic only)
- Explicit transformations
- Produces datasets used by ML + BI + monitoring
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd


@dataclass
class Paths:
    base: Path
    raw: Path
    staged: Path
    curated: Path
    ref: Path
    wh: Path


def _paths() -> Paths:
    base = Path(__file__).resolve().parents[1]
    data = base / "data"
    wh = base / "warehouse"
    return Paths(
        base=base,
        raw=data / "raw",
        staged=data / "staged",
        curated=data / "curated",
        ref=data / "reference",
        wh=wh,
    )


def _age_band(age: float) -> str:
    if age < 0:
        return "Unknown"
    if age < 18:
        return "0-17"
    if age < 30:
        return "18-29"
    if age < 45:
        return "30-44"
    if age < 60:
        return "45-59"
    if age < 75:
        return "60-74"
    return "75+"


def _lead_band(days: int) -> str:
    if days <= 0:
        return "0"
    if days <= 2:
        return "1-2"
    if days <= 7:
        return "3-7"
    if days <= 14:
        return "8-14"
    if days <= 30:
        return "15-30"
    return "31+"


def extract() -> pd.DataFrame:
    p = _paths()
    raw_path = p.raw / "appointments_raw.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Missing RAW dataset: {raw_path}. Run scripts/make_sample_data.py first.")
    df = pd.read_csv(raw_path)
    return df


def transform_stage(df_raw: pd.DataFrame) -> pd.DataFrame:
    p = _paths()
    df = df_raw.copy()

    # Parse datetimes
    df["appointment_datetime"] = pd.to_datetime(df["appointment_datetime"], errors="coerce")
    df["booking_datetime"] = pd.to_datetime(df["booking_datetime"], errors="coerce")

    # Drop rows with unparseable dates
    df = df.dropna(subset=["appointment_datetime", "booking_datetime"]).copy()

    # Compute lead time
    df["lead_time_days"] = (df["appointment_datetime"].dt.normalize() - df["booking_datetime"].dt.normalize()).dt.days.astype(int)



    # Deduplicate appointment_id (keep earliest booking_datetime)
    #df = df.sort_values(["appointment_id", "booking_datetime"]).drop_duplicates(subset=["appointment_id"], keep="first")

    # Join neighbourhood master
    neigh = pd.read_csv(p.ref / "neighbourhood_master.csv")
    df = df.merge(neigh[["neighbourhood_id", "deprivation_index", "region", "lat", "lon"]],
                  on="neighbourhood_id", how="left")

    # Join clinic master
    clinic = pd.read_csv(p.ref / "clinic_master.csv")
    df = df.merge(clinic[["clinic_id", "clinic_type", "daily_capacity", "region"]].rename(columns={"region":"clinic_region"}),
                  on="clinic_id", how="left")

    # Stage filters (cleanliness)
    # Remove invalid neighbourhoods / clinics
    df = df.dropna(subset=["deprivation_index", "clinic_type"]).copy()

    # Fix invalid age values by clipping into [0, 110]
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df = df.dropna(subset=["age"]).copy()
    df["age"] = df["age"].clip(lower=0, upper=110).astype(int)

    # Remove negative lead time records (booking after appointment)
    df = df[df["lead_time_days"] >= 0].copy()

    # Engineer time fields
    df["appointment_date"] = df["appointment_datetime"].dt.date.astype(str)
    df["appointment_dow"] = df["appointment_datetime"].dt.day_name()
    df["appointment_hour"] = df["appointment_datetime"].dt.hour
    df["appointment_is_weekend"] = (df["appointment_datetime"].dt.weekday >= 5).astype(int)

    df["age_band"] = df["age"].apply(_age_band)
    df["lead_time_band"] = df["lead_time_days"].apply(_lead_band)

    df["no_show_label"] = df["no_show"].astype(int)

    # Ensure types
    for c in ["sms_reminder_sent", "prior_no_show_count", "prior_show_count", "chronic_conditions_count", "disability_flag"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    # Final column ordering
    cols = [
        "appointment_id","patient_id","clinic_id","neighbourhood_id",
        "gender","age","age_band","chronic_conditions_count","disability_flag",
        "appointment_datetime","booking_datetime","appointment_date","appointment_dow","appointment_hour","appointment_is_weekend",
        "lead_time_days","lead_time_band","appointment_type","booking_channel","sms_reminder_sent",
        "prior_no_show_count","prior_show_count",
        "deprivation_index","region","lat","lon","clinic_type","daily_capacity","clinic_region",
        "no_show_label"
    ]
    df = df[cols].copy()

    return df


def build_curated(df_stage: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # Dimensions
    dim_patient = (df_stage.groupby("patient_id")
                   .agg(
                       gender=("gender", lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0]),
                       age=("age","max"),
                       age_band=("age_band", lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0]),
                       chronic_conditions_avg=("chronic_conditions_count","mean"),
                       disability_rate=("disability_flag","mean"),
                       prior_no_show_avg=("prior_no_show_count","mean"),
                   )
                   .reset_index())
    dim_patient["chronic_conditions_avg"] = dim_patient["chronic_conditions_avg"].round(2)
    dim_patient["disability_rate"] = dim_patient["disability_rate"].round(3)
    dim_patient["prior_no_show_avg"] = dim_patient["prior_no_show_avg"].round(2)

    dim_clinic = (df_stage.groupby(["clinic_id","clinic_type","daily_capacity","clinic_region"])
                  .size().reset_index(name="appointments"))
    dim_clinic = dim_clinic.drop(columns=["appointments"])

    dim_neighbourhood = (df_stage.groupby(["neighbourhood_id","region","lat","lon","deprivation_index"])
                         .size().reset_index(name="appointments"))
    dim_neighbourhood = dim_neighbourhood.drop(columns=["appointments"])

    dim_date = (df_stage[["appointment_date","appointment_dow"]]
                .drop_duplicates()
                .assign(date=lambda d: pd.to_datetime(d["appointment_date"]))
                .assign(year=lambda d: d["date"].dt.year,
                        month=lambda d: d["date"].dt.month,
                        month_name=lambda d: d["date"].dt.month_name(),
                        week=lambda d: d["date"].dt.isocalendar().week.astype(int))
                .rename(columns={"appointment_date":"date_key"})
                .sort_values("date_key")
                .reset_index(drop=True))

    # Fact
    fact = df_stage.copy()
    fact = fact.rename(columns={"appointment_date":"date_key"})
    keep_cols = [
        "appointment_id","date_key","patient_id","clinic_id","neighbourhood_id",
        "appointment_datetime","booking_datetime",
        "appointment_type","booking_channel",
        "lead_time_days","lead_time_band","appointment_dow","appointment_hour","appointment_is_weekend",
        "sms_reminder_sent","prior_no_show_count","prior_show_count",
        "age","age_band","gender","chronic_conditions_count","disability_flag",
        "deprivation_index","clinic_type","daily_capacity","region","clinic_region",
        "no_show_label"
    ]
    fact = fact[keep_cols].copy()

    # KPIs
    kpi_daily = (fact.groupby("date_key")
                 .agg(
                     appointments=("appointment_id","count"),
                     no_shows=("no_show_label","sum"),
                     avg_lead_time=("lead_time_days","mean"),
                     sms_rate=("sms_reminder_sent","mean"),
                     avg_prior_no_shows=("prior_no_show_count","mean"),
                 )
                 .reset_index())
    kpi_daily["no_show_rate"] = (kpi_daily["no_shows"] / kpi_daily["appointments"]).round(4)
    kpi_daily["avg_lead_time"] = kpi_daily["avg_lead_time"].round(2)
    kpi_daily["sms_rate"] = kpi_daily["sms_rate"].round(3)
    kpi_daily["avg_prior_no_shows"] = kpi_daily["avg_prior_no_shows"].round(2)

    kpi_clinic = (fact.groupby("clinic_id")
                  .agg(
                      appointments=("appointment_id","count"),
                      no_shows=("no_show_label","sum"),
                      avg_lead_time=("lead_time_days","mean"),
                      sms_rate=("sms_reminder_sent","mean"),
                  )
                  .reset_index())
    kpi_clinic["no_show_rate"] = (kpi_clinic["no_shows"] / kpi_clinic["appointments"]).round(4)
    kpi_clinic["avg_lead_time"] = kpi_clinic["avg_lead_time"].round(2)
    kpi_clinic["sms_rate"] = kpi_clinic["sms_rate"].round(3)

    kpi_neigh = (fact.groupby("neighbourhood_id")
                 .agg(
                     appointments=("appointment_id","count"),
                     no_shows=("no_show_label","sum"),
                     deprivation_index=("deprivation_index","mean"),
                     lat=("deprivation_index", "size"),  # placeholder overwritten below
                 )
                 .reset_index())
    # restore lat/lon by joining from dim_neighbourhood
    kpi_neigh = kpi_neigh.drop(columns=["lat"])
    kpi_neigh["no_show_rate"] = (kpi_neigh["no_shows"] / kpi_neigh["appointments"]).round(4)
    kpi_neigh["deprivation_index"] = kpi_neigh["deprivation_index"].round(3)

    return {
        "dim_patient": dim_patient,
        "dim_clinic": dim_clinic,
        "dim_neighbourhood": dim_neighbourhood,
        "dim_date": dim_date,
        "fact_appointments": fact,
        "kpi_daily": kpi_daily,
        "kpi_clinic_performance": kpi_clinic,
        "kpi_neighbourhood_hotspots": kpi_neigh,
    }


def load_to_warehouse(tables: dict[str, pd.DataFrame]) -> Path:
    p = _paths()
    p.wh.mkdir(parents=True, exist_ok=True)
    db_path = p.wh / "warehouse.db"

    # Create schema SQL file (documented)
    schema_sql = p.wh / "schema.sql"
    if not schema_sql.exists():
        schema_sql.write_text("""
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
""".strip() + "\n", encoding="utf-8")

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql.read_text(encoding="utf-8"))

        # Load tables (replace)
        for name, df in tables.items():
            df.to_sql(name, conn, if_exists="replace", index=False)

    return db_path


def main() -> None:
    p = _paths()
    p.staged.mkdir(parents=True, exist_ok=True)
    p.curated.mkdir(parents=True, exist_ok=True)

    df_raw = extract()
    df_stage = transform_stage(df_raw)

    stage_path = p.staged / "appointments_staged.csv"
    df_stage.to_csv(stage_path, index=False)

    tables = build_curated(df_stage)
    for name, df in tables.items():
        df.to_csv(p.curated / f"{name}.csv", index=False)

    db_path = load_to_warehouse(tables)

    print(f"[OK] Staged rows: {len(df_stage):,} -> {stage_path}")
    print(f"[OK] Curated tables: {len(tables)} -> {p.curated}")
    print(f"[OK] Warehouse loaded: {db_path}")


if __name__ == "__main__":
    main()
