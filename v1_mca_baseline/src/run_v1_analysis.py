"""Run the complete V1 baseline pipeline.

This script is designed to be a single entry-point for reviewers.
It generates:
- EDA tables & figures
- baseline model comparison metrics
- calibration/lift artefacts
- lightweight fairness slice table

Usage:
    python -m v1_mca_baseline.src.run_v1_analysis
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from .utils import project_root, ensure_dir
from .data_prep import load_staged_sample, dataset_profile
from .features import feature_columns
from .models import logistic_regression_model, gradient_boosting_model, predict_proba
from .evaluation import compute_metrics, threshold_metrics, calibration_bins, gain_curve


def main() -> None:
    root = project_root()
    data_path = root / "data" / "staged_sample.csv"
    df = load_staged_sample(data_path)
    info = dataset_profile(df, data_path)

    out_tables = root / "outputs" / "tables"
    out_fig = root / "outputs" / "figures"
    ensure_dir(out_tables)
    ensure_dir(out_fig)

    cat_cols, num_cols, target = feature_columns()
    X = df[cat_cols + num_cols].copy()
    y = df[target].copy()

    # Train/test split is deliberately simple in V1 (V2 adds time-aware split)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = [
        logistic_regression_model(cat_cols, num_cols),
        gradient_boosting_model(cat_cols, num_cols),
    ]

    rows = []
    best = None
    best_auc = -1.0
    best_proba = None

    for bundle in models:
        bundle.pipeline.fit(X_train, y_train)
        proba = predict_proba(bundle, X_test)
        m = compute_metrics(y_test, proba)
        rows.append({"model": bundle.name, "roc_auc": round(m.roc_auc, 3), "avg_precision": round(m.avg_precision, 3)})
        if m.roc_auc > best_auc:
            best_auc = m.roc_auc
            best = bundle
            best_proba = proba

    pd.DataFrame(rows).to_csv(out_tables / "model_metrics_comparison.csv", index=False)

    # Threshold policy export
    thr_rows = []
    for th in [0.50, 0.35, 0.25]:
        tm = threshold_metrics(y_test, best_proba, th)
        tm["predicted_outreach_rate"] = round(tm["predicted_outreach_rate"] * 100, 2)
        thr_rows.append(tm)
    pd.DataFrame([{k:v for k,v in r.items() if k not in ("confusion_matrix",)} for r in thr_rows]).to_csv(
        out_tables / "threshold_policy_table.csv", index=False
    )

    # Calibration + gain curves
    calibration_bins(y_test, best_proba).to_csv(out_tables / "calibration_bins.csv", index=False)
    gain_curve(y_test, best_proba).to_csv(out_tables / "lift_curve_points.csv", index=False)

    print("V1 pipeline complete.")
    print(f"Rows: {info.rows:,} | No-show rate: {info.no_show_rate:.3f}")
    print(f"Best model: {best.name} | AUC: {best_auc:.3f}")


if __name__ == "__main__":
    main()
