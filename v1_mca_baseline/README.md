# V1 — MCA Baseline: Healthcare Appointment No‑Show Prediction

**Track:** V1 (analysis + baseline ML)  
**Goal:** Understand drivers of no‑shows and build a solid baseline prediction model that can be operationalised (call list / reminders / scheduling).

> Data in this folder is **synthetic** (portfolio-safe). The patterns are designed to be realistic.

---

## What V1 delivers

### 1) Business framing
- Problem statement and decision levers (reminders, scheduling buffers, outreach lists)
- KPI definitions (no-show rate, outreach precision, operational lift)

### 2) Data understanding & EDA
- Cohort breakdowns: age band, lead time bands, booking channel, appointment type
- Operational insights: prior no-show history and deprivation index as risk signals
- Visual outputs: see `outputs/figures/` and `outputs/html/v1_eda_baseline_summary.html`

### 3) Baseline modeling
- Logistic Regression (interpretable baseline)
- Gradient Boosting (stronger non-linear baseline)
- Evaluation artefacts: ROC/PR curves, calibration, lift, confusion matrices
- Thresholding guidance for outreach workflows

### 4) Fairness slice checks (lightweight)
- Slice metrics by **gender** and **region** to ensure outreach policy is not producing obvious skew

---

## Quickstart (V1)

### Option A — Run the orchestrated script
```bash
python -m v1_mca_baseline.src.run_v1_analysis
```

### Option B — Run step scripts
```bash
python v1_mca_baseline/scripts/run_eda.py
python v1_mca_baseline/scripts/train_baselines.py
python v1_mca_baseline/scripts/generate_v1_report.py
```

Outputs will be written to:
- `outputs/figures/`
- `outputs/tables/`
- `outputs/html/`

---

## Key artefacts (start here)

### EDA
- `outputs/html/v1_eda_baseline_summary.html`
- `outputs/figures/eda_no_show_by_booking_channel.png`
- `outputs/figures/eda_no_show_vs_prior_no_show_count.png`
- `outputs/figures/eda_no_show_daily_timeseries.png`

### Modeling
- `outputs/tables/model_metrics_comparison.csv`
- `outputs/figures/model_roc_curve_best.png`
- `outputs/figures/model_calibration_curve.png`
- `outputs/figures/model_lift_curve.png`
- `reports/model_comparison_report.md`

### Governance & logs
- `logs/progress-log_2013-04-01_to_2013-04-20.md`
- `logs/risk-log.md`
- `logs/weekly_hours_v1.csv`

---

## Folder map (V1)

- `data/` — raw/interim/processed samples + schema
- `notebooks/` — analysis notebooks (EDA → features → modeling → error analysis)
- `src/` — reusable python modules
- `scripts/` — one-command scripts for repeatable runs
- `outputs/` — figures/tables/html results
- `reports/` — narrative reports with decisions and recommendations
- `experiments/` — experiment registry (baseline comparisons)
- `tests/` — quick validation tests

---

## Notes on scope

V1 intentionally focuses on:
- interpretability + insight generation
- baseline ML performance and evaluation hygiene

V2 adds:
- DQ gates + data contracts
- monitoring (drift, latency, SLA)
- model registry + API service
- modern BI dashboards
