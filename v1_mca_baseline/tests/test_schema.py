from pathlib import Path
import pandas as pd
from v1_mca_baseline.src.data_prep import REQUIRED_COLUMNS, load_staged_sample, basic_schema_check


def test_staged_schema_has_required_columns():
    path = Path(__file__).resolve().parents[1] / "data" / "staged_sample.csv"
    df = load_staged_sample(path)
    basic_schema_check(df)
    for col in REQUIRED_COLUMNS:
        assert col in df.columns


def test_target_is_binary():
    path = Path(__file__).resolve().parents[1] / "data" / "staged_sample.csv"
    df = load_staged_sample(path)
    vals = set(df["no_show"].unique().tolist())
    assert vals.issubset({0, 1})
