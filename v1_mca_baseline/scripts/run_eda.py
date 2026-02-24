"""Run basic EDA exports for V1.

This script generates:
- no-show rate tables by key dimensions
- a small set of charts for quick review

Outputs:
- outputs/tables/*.csv
- outputs/figures/eda_*.png
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from v1_mca_baseline.src.data_prep import load_staged_sample
from v1_mca_baseline.src.utils import project_root, ensure_dir
from v1_mca_baseline.src.viz import save_bar


def rate_table(df: pd.DataFrame, col: str) -> pd.DataFrame:
    g = df.groupby(col)["no_show"].agg(["mean","count"]).reset_index()
    g = g.rename(columns={"mean":"no_show_rate","count":"n"})
    g["no_show_rate"] = (g["no_show_rate"]*100).round(2)
    return g.sort_values("no_show_rate", ascending=False)


def main() -> None:
    root = project_root()
    df = load_staged_sample(root / "data" / "staged_sample.csv")

    out_tables = root / "outputs" / "tables"
    out_fig = root / "outputs" / "figures"
    ensure_dir(out_tables)
    ensure_dir(out_fig)

    dims = [
        ("booking_channel", "No-show rate by booking channel"),
        ("appointment_type", "No-show rate by appointment type"),
        ("lead_time_band", "No-show rate by lead time band"),
        ("region", "No-show rate by region"),
        ("clinic_type", "No-show rate by clinic type"),
    ]

    for col, title in dims:
        t = rate_table(df, col)
        t.to_csv(out_tables / f"no_show_by_{col}.csv", index=False)
        save_bar(t, col, "no_show_rate", title, out_fig / f"eda_no_show_by_{col}.png")

    print("EDA exports complete.")


if __name__ == "__main__":
    main()
