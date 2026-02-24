"""Data preparation utilities for the V1 baseline.

V1 keeps data prep intentionally simple:
- load staged sample
- basic type casting
- sanity checks used by tests
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "appointment_id","patient_id","clinic_id","neighbourhood_id",
    "gender","age","appointment_datetime","booking_datetime",
    "appointment_type","booking_channel","sms_reminder_sent",
    "prior_no_show_count","prior_show_count","deprivation_index",
    "clinic_type","daily_capacity","region","clinic_region",
    "no_show_label",
]


@dataclass(frozen=True)
class DatasetInfo:
    path: Path
    rows: int
    no_show_rate: float


def load_staged_sample(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        parse_dates=["appointment_datetime","booking_datetime","appointment_date"],
    )
    # Standardise target
    df["no_show"] = df["no_show_label"].astype(int)
    return df


def basic_schema_check(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df["no_show_label"].isna().any():
        raise ValueError("Target contains null values")


def dataset_profile(df: pd.DataFrame, path: Path) -> DatasetInfo:
    basic_schema_check(df)
    rows = int(df.shape[0])
    no_show_rate = float(df["no_show"].mean())
    return DatasetInfo(path=path, rows=rows, no_show_rate=no_show_rate)
