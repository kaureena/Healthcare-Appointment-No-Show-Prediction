from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_repo_has_key_docs():
    for f in ["README.md","ARCHITECTURE.md","DATA_README.md","MODEL_CARD.md","INSTALL_STEPS.md","EVIDENCE_INDEX.md"]:
        assert (ROOT / f).exists(), f"Missing {f}"

def test_v2_reports_exist():
    v2 = ROOT / "v2_mlops_modernisation"
    assert (v2 / "reports" / "dq_summary.json").exists()
    assert (v2 / "reports" / "dq_report.html").exists()
    assert (v2 / "reports" / "model_metrics.json").exists()
    assert (v2 / "reports" / "drift_report.csv").exists()

    metrics = json.loads((v2 / "reports" / "model_metrics.json").read_text())
    assert 0.0 <= metrics["roc_auc"] <= 1.0

def test_mermaid_count():
    mer = ROOT / "docs" / "mermaid"
    assert mer.exists()
    assert len(list(mer.glob("*.mmd"))) >= 10
