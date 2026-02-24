"""Generate a small HTML summary for V1.

This is intentionally simple and uses pre-generated artefacts.
"""

from __future__ import annotations

from pathlib import Path
import datetime

from v1_mca_baseline.src.utils import project_root, ensure_dir


def main() -> None:
    root = project_root()
    out_html = root / "outputs" / "html"
    ensure_dir(out_html)

    html = f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>V1 Summary</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 28px; }}
.small {{ color: #666; }}
.card {{ border: 1px solid #ddd; border-radius: 10px; padding: 14px; margin: 12px 0; }}
</style>
</head>
<body>
<h1>V1 Summary</h1>
<div class='small'>Generated: {datetime.datetime.now().isoformat(timespec='seconds')}</div>

<div class='card'>
<h2>Where to look</h2>
<ul>
<li><code>outputs/figures/</code> — charts</li>
<li><code>outputs/tables/</code> — tables</li>
<li><code>reports/</code> — narrative reports</li>
</ul>
</div>

<div class='card'>
<h2>Key plots</h2>
<ul>
<li><code>outputs/figures/model_roc_curve_best.png</code></li>
<li><code>outputs/figures/model_calibration_curve.png</code></li>
<li><code>outputs/figures/model_lift_curve.png</code></li>
</ul>
</div>

</body>
</html>"""

    (out_html / "v1_quick_report.html").write_text(html, encoding="utf-8")
    print("HTML summary written:", out_html / "v1_quick_report.html")


if __name__ == "__main__":
    main()
