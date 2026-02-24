from pathlib import Path
from v1_mca_baseline.src.data_prep import load_staged_sample


def test_no_show_rate_in_reasonable_band():
    path = Path(__file__).resolve().parents[1] / "data" / "staged_sample.csv"
    df = load_staged_sample(path)
    rate = float(df["no_show"].mean())
    # For this synthetic demo, we expect a realistic rate (not extreme)
    assert 0.15 <= rate <= 0.55
