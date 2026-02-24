"""Feature definitions for V1.

V1 focuses on a transparent, explainable feature set.
V2 adds feature store + versioning.
"""

from __future__ import annotations

from typing import List, Tuple

CAT_FEATURES: List[str] = [
    "gender",
    "age_band",
    "lead_time_band",
    "appointment_type",
    "booking_channel",
    "appointment_dow",
    "clinic_type",
    "region",
    "clinic_region",
]

NUM_FEATURES: List[str] = [
    "age",
    "chronic_conditions_count",
    "disability_flag",
    "lead_time_days",
    "sms_reminder_sent",
    "prior_no_show_count",
    "prior_show_count",
    "deprivation_index",
    "appointment_is_weekend",
    "appointment_hour",
    "daily_capacity",
]

TARGET_COL = "no_show"


def feature_columns() -> Tuple[List[str], List[str], str]:
    return CAT_FEATURES, NUM_FEATURES, TARGET_COL
