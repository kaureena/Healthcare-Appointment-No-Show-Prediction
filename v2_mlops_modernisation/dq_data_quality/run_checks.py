"""
DQ runner: loads datasets, runs expectations, writes JSON + HTML reports and a CSV issue register.
"""

from __future__ import annotations

from pathlib import Path
import json
import csv
from datetime import datetime

import pandas as pd

from .check_engine import run_checks, _load_expectation


def _base() -> Path:
    return Path(__file__).resolve().parents[1]


def load_datasets() -> dict[str, pd.DataFrame]:
    base = _base()
    data = base / "data"

    datasets = {}

    # RAW
    raw_path = data / "raw" / "appointments_raw.csv"
    if raw_path.exists():
        datasets["raw_appointments"] = pd.read_csv(raw_path)

    # STAGED
    staged_path = data / "staged" / "appointments_staged.csv"
    if staged_path.exists():
        datasets["staged_appointments"] = pd.read_csv(staged_path)

    # CURATED (key tables)
    curated_dir = data / "curated"
    for name in ["fact_appointments", "dim_patient", "dim_clinic", "dim_neighbourhood", "dim_date"]:
        p = curated_dir / f"{name}.csv"
        if p.exists():
            datasets[name] = pd.read_csv(p)

    return datasets


def load_expectations() -> list[dict]:
    base = _base()
    exp_dir = base / "dq_data_quality" / "expectations"
    exps = []
    for p in sorted(exp_dir.glob("EXP_*.json")):
        exps.append(_load_expectation(p))
    return exps


def write_reports(results, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON summary
    by_table = {}
    for r in results:
        by_table.setdefault(r.table, {"passed": 0, "failed": 0, "results": []})
        by_table[r.table]["passed" if r.passed else "failed"] += 1
        by_table[r.table]["results"].append({
            "expectation_id": r.expectation_id,
            "expectation_type": r.expectation_type,
            "severity": r.severity,
            "passed": r.passed,
            "details": r.details,
        })

    summary = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "tables": by_table,
        "overall": {
            "passed": sum(v["passed"] for v in by_table.values()),
            "failed": sum(v["failed"] for v in by_table.values())
        }
    }
    json_path = out_dir / "dq_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # HTML report
    rows = []
    for r in results:
        rows.append({
            "table": r.table,
            "expectation_id": r.expectation_id,
            "type": r.expectation_type,
            "severity": r.severity,
            "passed": "PASS" if r.passed else "FAIL",
            "details": json.dumps(r.details),
        })
    df = pd.DataFrame(rows).sort_values(["table","severity","passed"])
    html = df.to_html(index=False, escape=True)
    html_path = out_dir / "dq_report.html"
    html_path.write_text(
        "<html><head><meta charset='utf-8'><title>DQ Report</title></head>"
        "<body style='font-family: Arial, sans-serif; background:#0b1220; color:#e6edf7;'>"
        "<h1>Data Quality Report</h1>"
        f"<p>Generated: {summary['generated_at']}</p>"
        "<div style='background:#111a2e;padding:12px;border-radius:10px;border:1px solid #22304a;'>"
        + html +
        "</div></body></html>",
        encoding="utf-8"
    )
    return json_path, html_path


def write_issue_register(results, logs_dir: Path) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    issue_path = logs_dir / "V2_DQ_ISSUE_REGISTER.csv"
    fieldnames = ["issue_id","date","table","expectation_id","severity","description","status","notes"]
    rows = []
    i = 1
    for r in results:
        if r.passed:
            continue
        rows.append({
            "issue_id": f"DQ-{i:04d}",
            "date": datetime.utcnow().date().isoformat(),
            "table": r.table,
            "expectation_id": r.expectation_id,
            "severity": r.severity,
            "description": f"Expectation failed: {r.expectation_type} ({r.details})",
            "status": "Open",
            "notes": "Fix upstream in ETL or adjust expectation if justified."
        })
        i += 1

    with open(issue_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return issue_path


def main() -> None:
    base = _base()
    datasets = load_datasets()
    if not datasets:
        raise RuntimeError("No datasets found. Run make_sample_data.py then etl/run_etl.py first.")

    exps = load_expectations()
    results = run_checks(datasets, exps)

    reports_dir = base / "reports"
    json_path, html_path = write_reports(results, reports_dir)

    logs_dir = base / "logs"
    issue_path = write_issue_register(results, logs_dir)

    print(f"[OK] DQ summary: {json_path}")
    print(f"[OK] DQ HTML report: {html_path}")
    print(f"[OK] DQ issue register: {issue_path}")


if __name__ == "__main__":
    main()
