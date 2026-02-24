"""
Train the no-show prediction model (V2).

- Reads curated fact_appointments
- Creates a time-aware train/test split
- Trains a model (Logistic Regression with one-hot encoding)
- Writes model artifact + metrics + plots
- Writes predictions back to curated fact table (predicted probability + risk band)
- Updates SQLite warehouse fact_appointments table
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json
import sqlite3

import numpy as np
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    confusion_matrix, precision_recall_fscore_support, roc_curve, precision_recall_curve
)
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


@dataclass
class Config:
    split_date: str = "2026-01-15"
    random_state: int = 20260209


def _base() -> Path:
    return Path(__file__).resolve().parents[1]


def load_fact() -> pd.DataFrame:
    p = _base() / "data" / "curated" / "fact_appointments.csv"
    if not p.exists():
        raise FileNotFoundError(f"Missing curated fact table: {p}. Run ETL first.")
    df = pd.read_csv(p)
    return df


def risk_band(p: float) -> str:
    if p >= 0.75:
        return "Critical"
    if p >= 0.55:
        return "High"
    if p >= 0.35:
        return "Medium"
    return "Low"


def make_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    y = df["no_show_label"].astype(int)

    # Select features that are operationally plausible
    X = df[[
        "lead_time_days", "sms_reminder_sent",
        "prior_no_show_count", "prior_show_count",
        "age", "gender", "age_band",
        "appointment_type", "booking_channel",
        "appointment_hour", "appointment_is_weekend",
        "deprivation_index",
        "clinic_id", "neighbourhood_id", "clinic_type", "clinic_region"
    ]].copy()

    # ensure types
    num_cols = ["lead_time_days","prior_no_show_count","prior_show_count","age","appointment_hour","deprivation_index"]
    for c in num_cols:
        X[c] = pd.to_numeric(X[c], errors="coerce").fillna(0)

    for c in ["sms_reminder_sent","appointment_is_weekend"]:
        X[c] = pd.to_numeric(X[c], errors="coerce").fillna(0).astype(int)

    return X, y


def plot_confusion(cm, path: Path):
    fig = plt.figure(figsize=(6,5), dpi=140)
    ax = fig.add_subplot(111)
    ax.imshow(cm, interpolation="nearest")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    for (i,j), v in np.ndenumerate(cm):
        ax.text(j, i, str(v), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_roc(y_true, y_prob, path: Path):
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    fig = plt.figure(figsize=(6,5), dpi=140)
    ax = fig.add_subplot(111)
    ax.plot(fpr, tpr, label=f"AUC={auc:.3f}")
    ax.plot([0,1],[0,1], linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_pr(y_true, y_prob, path: Path):
    prec, rec, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    fig = plt.figure(figsize=(6,5), dpi=140)
    ax = fig.add_subplot(111)
    ax.plot(rec, prec, label=f"AP={ap:.3f}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_threshold_tuning(y_true, y_prob, path: Path):
    thresholds = np.linspace(0.05, 0.95, 19)
    f1s = []
    recalls = []
    precisions = []
    for t in thresholds:
        y_pred = (y_prob >= t).astype(int)
        p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
        f1s.append(f1); recalls.append(r); precisions.append(p)

    fig = plt.figure(figsize=(8,5), dpi=140)
    ax = fig.add_subplot(111)
    ax.plot(thresholds, f1s, label="F1")
    ax.plot(thresholds, recalls, label="Recall")
    ax.plot(thresholds, precisions, label="Precision")
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Score")
    ax.set_title("Threshold tuning (binary class)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    cfg = Config()
    base = _base()
    reports = base / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    models_dir = base / "models" / "artifacts"
    models_dir.mkdir(parents=True, exist_ok=True)
    registry_dir = base / "models" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)

    df = load_fact()
    df["date_key"] = pd.to_datetime(df["date_key"])

    split_dt = pd.to_datetime(cfg.split_date)
    train_df = df[df["date_key"] < split_dt].copy()
    test_df = df[df["date_key"] >= split_dt].copy()

    X_train, y_train = make_features(train_df)
    X_test, y_test = make_features(test_df)

    num_features = ["lead_time_days","prior_no_show_count","prior_show_count","age","appointment_hour","deprivation_index"]
    cat_features = [c for c in X_train.columns if c not in num_features and c not in ["sms_reminder_sent","appointment_is_weekend"]]
    passthrough_features = ["sms_reminder_sent","appointment_is_weekend"]

    pre = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_features + passthrough_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
        ],
        remainder="drop"
    )

    clf = LogisticRegression(
        max_iter=800,
        solver="saga",
        n_jobs=-1,
        random_state=cfg.random_state
    )

    pipe = Pipeline([("pre", pre), ("clf", clf)])
    pipe.fit(X_train, y_train)

    y_prob = pipe.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    auc = roc_auc_score(y_test, y_prob)
    ap = average_precision_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)

    metrics = {
        "split_date": cfg.split_date,
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
        "roc_auc": float(auc),
        "avg_precision": float(ap),
        "precision_at_0.5": float(p),
        "recall_at_0.5": float(r),
        "f1_at_0.5": float(f1),
        "confusion_matrix": cm.tolist(),
        "model": "LogisticRegression(saga) + OneHotEncoder",
        "generated_at_utc": datetime.utcnow().isoformat() + "Z"
    }

    (reports / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    plot_roc(y_test, y_prob, reports / "roc_curve.png")
    plot_pr(y_test, y_prob, reports / "pr_curve.png")
    plot_confusion(cm, reports / "confusion_matrix.png")
    plot_threshold_tuning(y_test, y_prob, reports / "threshold_tuning_f1.png")

    run_id = f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    model_path = models_dir / "best_model.joblib"
    dump(pipe, model_path)

    # Write registry append
    reg_path = registry_dir / "model_registry.csv"
    row = {
        "run_id": run_id,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "model": "LogisticRegression(saga)+OHE",
        "roc_auc": round(float(auc), 4),
        "avg_precision": round(float(ap), 4),
        "precision_at_0.5": round(float(p), 4),
        "recall_at_0.5": round(float(r), 4),
        "f1_at_0.5": round(float(f1), 4),
        "split_date": cfg.split_date,
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
        "artifact_path": str(model_path.as_posix()),
    }
    if reg_path.exists():
        reg = pd.read_csv(reg_path)
        reg = pd.concat([reg, pd.DataFrame([row])], ignore_index=True)
    else:
        reg = pd.DataFrame([row])
    reg.to_csv(reg_path, index=False)

    # Score full dataset for BI/monitoring
    X_all, _ = make_features(df.assign(no_show_label=df["no_show_label"]))
    all_prob = pipe.predict_proba(X_all)[:, 1]
    df_scored = df.copy()
    df_scored["predicted_no_show_proba"] = all_prob
    df_scored["risk_band"] = df_scored["predicted_no_show_proba"].apply(risk_band)

    # Persist back to curated
    out_fact = base / "data" / "curated" / "fact_appointments.csv"
    df_scored_out = df_scored.copy()
    df_scored_out["date_key"] = df_scored_out["date_key"].dt.date.astype(str)
    df_scored_out.to_csv(out_fact, index=False)

    # Update warehouse fact table
    wh_db = base / "warehouse" / "warehouse.db"
    if wh_db.exists():
        with sqlite3.connect(wh_db) as conn:
            df_scored_out.to_sql("fact_appointments", conn, if_exists="replace", index=False)

    # Write a small feature importance proxy (coefficients)
    # We'll export top coefficients for interpretability.
    ohe = pipe.named_steps["pre"].named_transformers_["cat"]
    cat_feature_names = list(ohe.get_feature_names_out(cat_features))
    feature_names = num_features + passthrough_features + cat_feature_names
    coefs = pipe.named_steps["clf"].coef_[0]
    fi = pd.DataFrame({"feature": feature_names, "coef": coefs})
    fi["abs_coef"] = fi["coef"].abs()
    fi = fi.sort_values("abs_coef", ascending=False).head(40)
    fi.to_csv(reports / "feature_importance_top40.csv", index=False)

    fig = plt.figure(figsize=(10,7), dpi=140)
    ax = fig.add_subplot(111)
    ax.barh(fi["feature"][::-1], fi["abs_coef"][::-1])
    ax.set_title("Top 40 feature effects (|coef|)")
    ax.set_xlabel("|coef|")
    fig.tight_layout()
    fig.savefig(reports / "feature_importance_top40.png")
    plt.close(fig)

    print(f"[OK] Model artifact: {model_path}")
    print(f"[OK] Metrics: {reports/'model_metrics.json'}")
    print(f"[OK] Registry: {reg_path}")
    print(f"[OK] Scored fact updated: {out_fact}")
    print(f"[OK] Updated warehouse: {wh_db}")


if __name__ == "__main__":
    main()
