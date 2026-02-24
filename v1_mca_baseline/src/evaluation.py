"""Evaluation helpers for V1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
from sklearn.calibration import calibration_curve


@dataclass
class Metrics:
    roc_auc: float
    avg_precision: float


def compute_metrics(y_true, proba) -> Metrics:
    return Metrics(
        roc_auc=float(roc_auc_score(y_true, proba)),
        avg_precision=float(average_precision_score(y_true, proba)),
    )


def threshold_metrics(y_true, proba, threshold: float) -> Dict[str, Any]:
    pred = (np.asarray(proba) >= threshold).astype(int)
    return {
        "threshold": float(threshold),
        "precision": float(precision_score(y_true, pred)),
        "recall": float(recall_score(y_true, pred)),
        "f1": float(f1_score(y_true, pred)),
        "accuracy": float(accuracy_score(y_true, pred)),
        "predicted_outreach_rate": float(pred.mean()),
        "confusion_matrix": confusion_matrix(y_true, pred).tolist(),
    }


def calibration_bins(y_true, proba, bins: int = 10) -> pd.DataFrame:
    prob_true, prob_pred = calibration_curve(y_true, proba, n_bins=bins, strategy="quantile")
    return pd.DataFrame({"bin_pred_mean": prob_pred, "bin_true_rate": prob_true})


def gain_curve(y_true, proba) -> pd.DataFrame:
    order = np.argsort(-np.asarray(proba))
    y_sorted = np.asarray(y_true)[order]
    cum_pos = np.cumsum(y_sorted)
    total_pos = float(cum_pos[-1]) if len(cum_pos) else 1.0
    pct_samples = (np.arange(1, len(y_sorted) + 1) / len(y_sorted)) if len(y_sorted) else np.array([])
    gain = (cum_pos / total_pos) if total_pos > 0 else np.zeros_like(cum_pos, dtype=float)
    return pd.DataFrame({"pct_samples": pct_samples, "cumulative_gain": gain})
