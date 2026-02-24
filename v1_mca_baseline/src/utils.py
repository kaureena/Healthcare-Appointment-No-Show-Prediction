"""V1 utility helpers.

This module is intentionally lightweight and dependency-minimal for a baseline track.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Dict


def project_root() -> Path:
    """Return the V1 project root (v1_mca_baseline)."""
    return Path(__file__).resolve().parents[1]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
