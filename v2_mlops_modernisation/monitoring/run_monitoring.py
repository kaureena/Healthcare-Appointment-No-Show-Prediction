"""
Monitoring runner: drift + freshness SLA + API latency simulation.

Outputs (under v2_mlops_modernisation/reports/):
- drift_report.csv / drift_report.json
- api_latency_daily.csv
- monitoring_snapshot.csv
- alerts_register.csv
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta, date
import json
import random

import numpy as np
import pandas as pd


@dataclass
class Config:
    split_date: str = "2026-01-15"
    reference_start: str = "2025-12-01"
    reference_end: str = "2025-12-31"
    current_start: str = "2026-02-01"
    current_end: str = "2026-02-08"
    psi_bins: int = 10
    warn_threshold: float = 0.1
    alert_threshold: float = 0.25

    # Freshness
    expected_latest_date: str = "2026-02-08"
    freshness_sla_days: int = 2

    # Latency simulation
    latency_days: int = 30
    rng_seed: int = 20260209


def _base() -> Path:
    return Path(__file__).resolve().parents[1]


def _psi_numeric(ref: pd.Series, cur: pd.Series, bins: int) -> float:
    ref = pd.to_numeric(ref, errors="coerce").dropna()
    cur = pd.to_numeric(cur, errors="coerce").dropna()
    if len(ref) < 100 or len(cur) < 100:
        return float("nan")

    # quantile bins from reference
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.unique(np.quantile(ref, quantiles))
    if len(edges) < 3:
        return 0.0

    ref_counts, _ = np.histogram(ref, bins=edges)
    cur_counts, _ = np.histogram(cur, bins=edges)

    ref_dist = ref_counts / max(1, ref_counts.sum())
    cur_dist = cur_counts / max(1, cur_counts.sum())

    # replace zeros
    eps = 1e-6
    ref_dist = np.where(ref_dist == 0, eps, ref_dist)
    cur_dist = np.where(cur_dist == 0, eps, cur_dist)

    psi = np.sum((cur_dist - ref_dist) * np.log(cur_dist / ref_dist))
    return float(psi)


def _psi_categorical(ref: pd.Series, cur: pd.Series) -> float:
    ref = ref.astype(str).fillna("NA")
    cur = cur.astype(str).fillna("NA")
    ref_counts = ref.value_counts(normalize=True)
    cur_counts = cur.value_counts(normalize=True)

    cats = sorted(set(ref_counts.index).union(set(cur_counts.index)))
    eps = 1e-6
    psi = 0.0
    for c in cats:
        r = float(ref_counts.get(c, eps))
        u = float(cur_counts.get(c, eps))
        r = r if r > 0 else eps
        u = u if u > 0 else eps
        psi += (u - r) * np.log(u / r)
    return float(psi)


def _status(psi: float, warn: float, alert: float) -> str:
    if np.isnan(psi):
        return "NA"
    if psi >= alert:
        return "ALERT"
    if psi >= warn:
        return "WARN"
    return "OK"


def load_fact() -> pd.DataFrame:
    p = _base() / "data" / "curated" / "fact_appointments.csv"
    if not p.exists():
        raise FileNotFoundError(f"Missing fact_appointments.csv: {p}. Run ETL + train first.")
    df = pd.read_csv(p)
    df["date_key"] = pd.to_datetime(df["date_key"])
    return df


def freshness_snapshot(df: pd.DataFrame, cfg: Config) -> dict:
    latest = df["date_key"].max().date()
    expected = date.fromisoformat(cfg.expected_latest_date)
    lag_days = (expected - latest).days
    status = "OK" if lag_days <= cfg.freshness_sla_days else "ALERT"
    return {
        "expected_latest_date": expected.isoformat(),
        "observed_latest_date": latest.isoformat(),
        "lag_days": int(lag_days),
        "sla_days": cfg.freshness_sla_days,
        "freshness_status": status
    }


def build_drift_report(df: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    ref = df[(df["date_key"] >= pd.to_datetime(cfg.reference_start)) & (df["date_key"] <= pd.to_datetime(cfg.reference_end))]
    cur = df[(df["date_key"] >= pd.to_datetime(cfg.current_start)) & (df["date_key"] <= pd.to_datetime(cfg.current_end))]

    numeric = ["lead_time_days","age","deprivation_index","predicted_no_show_proba","prior_no_show_count"]
    categorical = ["clinic_id","booking_channel","appointment_type","risk_band","clinic_region","age_band"]

    rows = []
    for col in numeric:
        psi = _psi_numeric(ref[col], cur[col], cfg.psi_bins)
        rows.append({"feature": col, "feature_type": "numeric", "psi": psi, "status": _status(psi, cfg.warn_threshold, cfg.alert_threshold)})

    for col in categorical:
        psi = _psi_categorical(ref[col], cur[col])
        rows.append({"feature": col, "feature_type": "categorical", "psi": psi, "status": _status(psi, cfg.warn_threshold, cfg.alert_threshold)})

    out = pd.DataFrame(rows)
    out["psi"] = out["psi"].round(6)
    out = out.sort_values(["status","psi"], ascending=[False, False]).reset_index(drop=True)
    out["reference_window"] = f"{cfg.reference_start}..{cfg.reference_end}"
    out["current_window"] = f"{cfg.current_start}..{cfg.current_end}"
    return out


def simulate_latency(cfg: Config) -> pd.DataFrame:
    rng = random.Random(cfg.rng_seed)
    end = date.fromisoformat(cfg.current_end)
    start = end - timedelta(days=cfg.latency_days-1)

    days = [start + timedelta(days=i) for i in range(cfg.latency_days)]

    rows = []
    base_p50 = 120
    for d in days:
        # mild weekday variation + occasional incident spikes
        weekday = d.weekday()
        spike = 1.0
        if rng.random() < 0.08:
            spike = rng.uniform(1.5, 3.2)

        p50 = base_p50 * (1.0 + 0.08*(weekday in (0,1))) * spike
        p95 = p50 * rng.uniform(2.1, 2.7)
        p99 = p95 * rng.uniform(1.15, 1.35)
        err = rng.uniform(0.002, 0.018) * spike

        rows.append({
            "date": d.isoformat(),
            "p50_ms": round(p50, 1),
            "p95_ms": round(p95, 1),
            "p99_ms": round(p99, 1),
            "error_rate": round(err, 4),
        })
    return pd.DataFrame(rows)


def alerts_from_monitoring(drift: pd.DataFrame, fresh: dict, latency: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    alerts = []
    now = datetime.utcnow().isoformat() + "Z"

    # Drift alerts
    for _, r in drift.iterrows():
        if r["status"] == "ALERT":
            alerts.append({
                "alert_id": f"AL-{len(alerts)+1:04d}",
                "timestamp_utc": now,
                "alert_type": "DRIFT",
                "severity": "high",
                "entity": r["feature"],
                "message": f"PSI drift ALERT for {r['feature']} (psi={r['psi']})",
                "status": "Open"
            })
        elif r["status"] == "WARN":
            alerts.append({
                "alert_id": f"AL-{len(alerts)+1:04d}",
                "timestamp_utc": now,
                "alert_type": "DRIFT",
                "severity": "medium",
                "entity": r["feature"],
                "message": f"PSI drift WARN for {r['feature']} (psi={r['psi']})",
                "status": "Open"
            })

    # Freshness alert
    if fresh["freshness_status"] == "ALERT":
        alerts.append({
            "alert_id": f"AL-{len(alerts)+1:04d}",
            "timestamp_utc": now,
            "alert_type": "FRESHNESS",
            "severity": "high",
            "entity": "fact_appointments",
            "message": f"Freshness SLA breach. Lag days={fresh['lag_days']}, SLA={fresh['sla_days']}",
            "status": "Open"
        })

    # Latency alert
    last = latency.tail(1).iloc[0]
    if last["p95_ms"] > 600 or last["error_rate"] > 0.03:
        alerts.append({
            "alert_id": f"AL-{len(alerts)+1:04d}",
            "timestamp_utc": now,
            "alert_type": "API_PERF",
            "severity": "high",
            "entity": "predict_api",
            "message": f"API performance alert. p95_ms={last['p95_ms']} error_rate={last['error_rate']}",
            "status": "Open"
        })

    return pd.DataFrame(alerts)


def monitoring_snapshot(drift: pd.DataFrame, fresh: dict, latency: pd.DataFrame) -> pd.DataFrame:
    # summarise
    n_alert = int((drift["status"] == "ALERT").sum())
    n_warn = int((drift["status"] == "WARN").sum())
    last = latency.tail(1).iloc[0]

    row = {
        "snapshot_time_utc": datetime.utcnow().isoformat() + "Z",
        "drift_alert_count": n_alert,
        "drift_warn_count": n_warn,
        "freshness_status": fresh["freshness_status"],
        "freshness_lag_days": fresh["lag_days"],
        "api_p95_ms": float(last["p95_ms"]),
        "api_error_rate": float(last["error_rate"]),
    }
    return pd.DataFrame([row])


def main() -> None:
    cfg = Config()
    base = _base()
    reports = base / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    df = load_fact()

    drift = build_drift_report(df, cfg)
    drift.to_csv(reports / "drift_report.csv", index=False)
    (reports / "drift_report.json").write_text(drift.to_json(orient="records", indent=2), encoding="utf-8")

    fresh = freshness_snapshot(df, cfg)

    latency = simulate_latency(cfg)
    latency.to_csv(reports / "api_latency_daily.csv", index=False)

    snapshot = monitoring_snapshot(drift, fresh, latency)
    snapshot.to_csv(reports / "monitoring_snapshot.csv", index=False)

    alerts = alerts_from_monitoring(drift, fresh, latency, cfg)
    alerts.to_csv(reports / "alerts_register.csv", index=False)

    print(f"[OK] Drift report: {reports/'drift_report.csv'}")
    print(f"[OK] Monitoring snapshot: {reports/'monitoring_snapshot.csv'}")
    print(f"[OK] Alerts register: {reports/'alerts_register.csv'}")
    print(f"[OK] API latency: {reports/'api_latency_daily.csv'}")


if __name__ == "__main__":
    main()
