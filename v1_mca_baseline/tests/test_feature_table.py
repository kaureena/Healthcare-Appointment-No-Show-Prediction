from pathlib import Path
import pandas as pd


def test_features_processed_sample_has_expected_columns():
    path = Path(__file__).resolve().parents[1] / "data" / "processed" / "features_processed_sample.csv"
    df = pd.read_csv(path)
    expected = {"no_show", "age", "lead_time_days", "sms_reminder_sent", "prior_no_show_count", "deprivation_index"}
    assert expected.issubset(set(df.columns))


def test_features_processed_sample_has_no_nan_in_key_fields():
    path = Path(__file__).resolve().parents[1] / "data" / "processed" / "features_processed_sample.csv"
    df = pd.read_csv(path)
    key = ["no_show", "age", "lead_time_days", "sms_reminder_sent"]
    assert df[key].isna().sum().sum() == 0
