"""
Synthetic data generator for Healthcare Appointment No-Show Prediction.

Policy: Synthetic data only (portfolio-safe).

This generator intentionally injects a small amount of data defects into the RAW layer
to demonstrate Data Quality (DQ) gates in V2.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

import numpy as np
import pandas as pd


@dataclass
class Config:
    seed: int = 20260209
    n_rows: int = 55000
    n_patients: int = 12000
    n_clinics: int = 12
    n_neighbourhoods: int = 60
    start_date: str = "2025-10-01"
    end_date: str = "2026-02-08"  # must be <= "today - 1" for realism in this repo context

    # Defect injection (RAW only)
    pct_invalid_neighbourhood: float = 0.007
    pct_negative_age: float = 0.003
    pct_age_over_120: float = 0.002
    pct_negative_lead_time: float = 0.004
    pct_duplicate_appointment_id: float = 0.004


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def _date_range(start: datetime, end: datetime, rng: random.Random) -> datetime:
    # uniform random timestamp in [start, end]
    delta = end - start
    sec = rng.random() * delta.total_seconds()
    return start + timedelta(seconds=sec)


def _make_reference(cfg: Config, base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = _rng(cfg.seed)

    # Neighbourhoods
    neighbourhoods = []
    for i in range(cfg.n_neighbourhoods):
        nid = f"N{i+1:03d}"
        deprivation = round(max(0.0, min(1.0, rng.gauss(0.45, 0.18))), 3)
        lat = 22.3 + rng.random() * 1.2
        lon = 72.4 + rng.random() * 1.8
        region = rng.choice(["North", "South", "East", "West", "Central"])
        neighbourhoods.append({
            "neighbourhood_id": nid,
            "neighbourhood_name": f"Neighbourhood_{i+1:03d}",
            "region": region,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "deprivation_index": deprivation,
        })
    df_neigh = pd.DataFrame(neighbourhoods)

    # Clinics
    clinics = []
    for i in range(cfg.n_clinics):
        cid = f"C{i+1:02d}"
        clinics.append({
            "clinic_id": cid,
            "clinic_name": f"Clinic_{i+1:02d}",
            "clinic_type": rng.choice(["Primary Care", "Specialty Center", "Community Clinic"]),
            "daily_capacity": rng.choice([80, 100, 120, 150, 180]),
            "region": rng.choice(["North", "South", "East", "West", "Central"]),
        })
    df_clinic = pd.DataFrame(clinics)

    ref_dir = base_dir / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)
    df_neigh.to_csv(ref_dir / "neighbourhood_master.csv", index=False)
    df_clinic.to_csv(ref_dir / "clinic_master.csv", index=False)

    return df_neigh, df_clinic


def _no_show_probability(row: dict) -> float:
    # Logistic-like scoring without importing heavy libs for speed
    # Base no-show around 0.23
    x = -1.2

    lead = row["lead_time_days"]
    x += 0.018 * max(0, min(60, lead))          # longer lead increases risk
    x += 0.38 * min(6, row["prior_no_show_count"])
    x += 0.10 * row["chronic_conditions_count"]
    x += 0.35 * row["deprivation_index"]

    if row["sms_reminder_sent"] == 1:
        x -= 0.55

    if row["appointment_type"] in ("Specialist", "Lab"):
        x += 0.18

    if row["booking_channel"] == "Walk-in":
        x -= 0.12

    # time-of-day effect
    hour = row["appointment_hour"]
    if hour < 9:
        x += 0.10
    elif hour >= 17:
        x += 0.08

    # weekend appointments show slightly higher missed rate
    if row["appointment_is_weekend"] == 1:
        x += 0.10

    # convert log-odds to probability
    p = 1 / (1 + np.exp(-x))
    return float(max(0.01, min(0.90, p)))


def make_raw_dataset(cfg: Config, base_dir: Path) -> pd.DataFrame:
    rng = _rng(cfg.seed)
    np.random.seed(cfg.seed)

    df_neigh, df_clinic = _make_reference(cfg, base_dir)

    patient_ids = [f"P{i+1:05d}" for i in range(cfg.n_patients)]
    clinic_ids = df_clinic["clinic_id"].tolist()
    neigh_ids = df_neigh["neighbourhood_id"].tolist()

    start = datetime.fromisoformat(cfg.start_date)
    end = datetime.fromisoformat(cfg.end_date) + timedelta(hours=23, minutes=59, seconds=59)

    rows = []
    for _ in range(cfg.n_rows):
        appointment_dt = _date_range(start, end, rng)
        lead_days = int(max(0, rng.gauss(9, 6)))
        booking_dt = appointment_dt - timedelta(days=lead_days, hours=rng.randint(0, 23))

        age = int(max(0, min(95, rng.gauss(38, 17))))
        gender = rng.choice(["F", "M"])
        chronic = int(max(0, min(5, rng.gauss(1.1, 1.2))))
        disability = 1 if rng.random() < 0.07 else 0

        neigh = rng.choice(neigh_ids)
        dep = float(df_neigh.loc[df_neigh["neighbourhood_id"] == neigh, "deprivation_index"].iloc[0])

        clinic = rng.choice(clinic_ids)

        appointment_type = rng.choice(["General", "Specialist", "Lab", "Follow-up"])
        booking_channel = rng.choice(["Online", "Phone", "Walk-in", "Referral"])

        prior_no_show = int(max(0, min(6, rng.gauss(0.8, 1.3))))
        prior_show = int(max(0, min(20, rng.gauss(4.2, 3.5))))

        sms = 1 if (rng.random() < 0.55) else 0

        hour = appointment_dt.hour
        is_weekend = 1 if appointment_dt.weekday() >= 5 else 0

        # compute probability and label
        row_tmp = {
            "lead_time_days": (appointment_dt.date() - booking_dt.date()).days,
            "prior_no_show_count": prior_no_show,
            "chronic_conditions_count": chronic,
            "deprivation_index": dep,
            "sms_reminder_sent": sms,
            "appointment_type": appointment_type,
            "booking_channel": booking_channel,
            "appointment_hour": hour,
            "appointment_is_weekend": is_weekend,
        }
        p_no_show = _no_show_probability(row_tmp)
        no_show = 1 if rng.random() < p_no_show else 0

        rows.append({
            "appointment_id": str(uuid.uuid4()),
            "patient_id": rng.choice(patient_ids),
            "clinic_id": clinic,
            "neighbourhood_id": neigh,
            "gender": gender,
            "age": age,
            "chronic_conditions_count": chronic,
            "disability_flag": disability,
            "appointment_datetime": appointment_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "booking_datetime": booking_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "appointment_type": appointment_type,
            "booking_channel": booking_channel,
            "sms_reminder_sent": sms,
            "prior_no_show_count": prior_no_show,
            "prior_show_count": prior_show,
            "no_show": no_show,
        })

    df = pd.DataFrame(rows)

    # Inject defects (RAW layer only)
    n = len(df)

    # invalid neighbourhood
    k = int(cfg.pct_invalid_neighbourhood * n)
    if k > 0:
        idx = np.random.choice(n, k, replace=False)
        df.loc[idx, "neighbourhood_id"] = "N999"

    # negative age
    k = int(cfg.pct_negative_age * n)
    if k > 0:
        idx = np.random.choice(n, k, replace=False)
        df.loc[idx, "age"] = -1 * np.random.randint(1, 5, size=k)

    # over 120 age
    k = int(cfg.pct_age_over_120 * n)
    if k > 0:
        idx = np.random.choice(n, k, replace=False)
        df.loc[idx, "age"] = np.random.randint(121, 140, size=k)

    # negative lead time (booking after appointment)
    k = int(cfg.pct_negative_lead_time * n)
    if k > 0:
        idx = np.random.choice(n, k, replace=False)
        # booking_datetime after appointment_datetime
        appts = pd.to_datetime(df.loc[idx, "appointment_datetime"])
        df.loc[idx, "booking_datetime"] = (appts + pd.to_timedelta(np.random.randint(1, 4, size=k), unit="D")).dt.strftime("%Y-%m-%d %H:%M:%S")

    # duplicates appointment_id
    k = int(cfg.pct_duplicate_appointment_id * n)
    if k > 0:
        idx = np.random.choice(n, k, replace=False)
        # set some appointment_ids equal to earlier ones
        df.loc[idx, "appointment_id"] = df.loc[idx // 2, "appointment_id"].values

    raw_dir = base_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_dir / "appointments_raw.csv", index=False)

    return df


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1] / "data"
    cfg = Config()
    df = make_raw_dataset(cfg, base_dir)
    print(f"[OK] Wrote RAW dataset: {len(df):,} rows -> {base_dir/'raw/appointments_raw.csv'}")
    print(f"[OK] Reference masters written to: {base_dir/'reference'}")


if __name__ == "__main__":
    main()
