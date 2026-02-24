"""Plotting helpers for V1 outputs."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_bar(df: pd.DataFrame, x: str, y: str, title: str, out_path: Path, rotate: int = 45) -> None:
    fig = plt.figure(figsize=(10, 5), dpi=160)
    plt.bar(df[x].astype(str), df[y])
    plt.xticks(rotation=rotate, ha="right")
    plt.ylabel(y)
    plt.title(title)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)


def save_line(df: pd.DataFrame, x: str, y: str, title: str, out_path: Path) -> None:
    fig = plt.figure(figsize=(10, 4.5), dpi=160)
    plt.plot(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.grid(True, axis="y", alpha=0.25)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
