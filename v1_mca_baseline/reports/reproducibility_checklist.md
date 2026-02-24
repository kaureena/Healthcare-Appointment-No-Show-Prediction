# Reproducibility checklist (V1)

## Environment
- Python 3.10+
- Key libs: pandas, numpy, matplotlib, scikit-learn

## Steps
1. Inspect the dataset: `data/staged_sample.csv`
2. Run EDA:
   - `python v1_mca_baseline/scripts/run_eda.py`
3. Train baselines:
   - `python v1_mca_baseline/scripts/train_baselines.py`
4. Generate the HTML summary:
   - `python v1_mca_baseline/scripts/generate_v1_report.py`

## Outputs
- Figures: `outputs/figures/`
- Tables: `outputs/tables/`
- HTML summary: `outputs/html/v1_eda_baseline_summary.html`

## Sanity checks
- Ensure no-show rate is within expected band (20–45% in this synthetic sample).
- Ensure `model_metrics_comparison.csv` exists after training.

