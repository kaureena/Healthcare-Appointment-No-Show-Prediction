"""
Minimal Data Quality engine for the V2 pipeline.

The intent is portfolio-grade clarity:
- expectations are small JSON documents
- checks are explicit and reproducible
- output is both machine-readable (JSON) and human-readable (HTML)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import json

import pandas as pd


@dataclass
class CheckResult:
    expectation_id: str
    table: str
    expectation_type: str
    severity: str
    passed: bool
    details: Dict[str, Any]


def _load_expectation(path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_required_columns(df: pd.DataFrame, columns: List[str]) -> Tuple[bool, Dict[str, Any]]:
    missing = [c for c in columns if c not in df.columns]
    return (len(missing) == 0, {"missing_columns": missing})


def check_non_null(df: pd.DataFrame, column: str) -> Tuple[bool, Dict[str, Any]]:
    nulls = int(df[column].isna().sum()) if column in df.columns else None
    return (nulls == 0, {"null_count": nulls})


def check_non_negative(df: pd.DataFrame, column: str) -> Tuple[bool, Dict[str, Any]]:
    if column not in df.columns:
        return False, {"error": "missing_column"}
    bad = int((pd.to_numeric(df[column], errors="coerce") < 0).sum())
    return (bad == 0, {"negative_count": bad})


def check_between(df: pd.DataFrame, column: str, min_value: float, max_value: float) -> Tuple[bool, Dict[str, Any]]:
    if column not in df.columns:
        return False, {"error": "missing_column"}
    s = pd.to_numeric(df[column], errors="coerce")
    bad = int(((s < min_value) | (s > max_value)).sum())
    return (bad == 0, {"out_of_range_count": bad, "min": min_value, "max": max_value})


def check_unique(df: pd.DataFrame, columns: List[str]) -> Tuple[bool, Dict[str, Any]]:
    if any(c not in df.columns for c in columns):
        return False, {"error": "missing_column"}
    dup = int(df.duplicated(subset=columns).sum())
    return (dup == 0, {"duplicate_rows": dup})


def check_in_set(df: pd.DataFrame, column: str, allowed_values: List[Any]) -> Tuple[bool, Dict[str, Any]]:
    if column not in df.columns:
        return False, {"error": "missing_column"}
    bad_mask = ~df[column].isin(allowed_values)
    bad = int(bad_mask.sum())
    sample = df.loc[bad_mask, column].astype(str).head(5).tolist()
    return (bad == 0, {"invalid_count": bad, "sample_invalid_values": sample})


def evaluate_expectation(df: pd.DataFrame, exp: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    et = exp["expectation_type"]
    kw = exp.get("kwargs", {})

    if et == "expect_required_columns":
        return check_required_columns(df, kw["columns"])
    if et == "expect_non_null":
        return check_non_null(df, kw["column"])
    if et == "expect_non_negative":
        return check_non_negative(df, kw["column"])
    if et == "expect_between":
        return check_between(df, kw["column"], kw["min"], kw["max"])
    if et == "expect_unique":
        return check_unique(df, kw["columns"])
    if et == "expect_in_set":
        return check_in_set(df, kw["column"], kw["allowed_values"])

    return False, {"error": f"unknown_expectation_type: {et}"}


def run_checks(datasets: Dict[str, pd.DataFrame], expectations: List[Dict[str, Any]]) -> List[CheckResult]:
    results: List[CheckResult] = []

    for exp in expectations:
        table = exp.get("table", "unknown_table")
        df = datasets.get(table)
        if df is None:
            results.append(CheckResult(
                expectation_id=exp["expectation_id"],
                table=table,
                expectation_type=exp["expectation_type"],
                severity=exp.get("severity","medium"),
                passed=False,
                details={"error": "unknown_table"}
            ))
            continue

        ok, details = evaluate_expectation(df, exp)
        results.append(CheckResult(
            expectation_id=exp["expectation_id"],
            table=table,
            expectation_type=exp["expectation_type"],
            severity=exp.get("severity","medium"),
            passed=bool(ok),
            details=details
        ))

    return results
