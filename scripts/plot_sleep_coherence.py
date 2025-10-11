#!/usr/bin/env python3
"""Generate weekly sleep coherence chart (04–11 Oct 2025).

Reads structured sleep JSON files (schema v1) and produces a PNG with:
- Total sleep, deep and REM (hours)
- Body Battery change and SpO₂ mínima (%)

Usage:
  python3 scripts/plot_sleep_coherence.py

Requirements: pandas, matplotlib (install via `pip install -r requirements.txt`).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_DIR = Path("analysis/reports/diarios_json")
OUTPUT_PATH = Path("analysis/reports/summaries/sleep_coherence_2025-10-04_2025-10-11.png")
DATE_START = datetime.fromisoformat("2025-10-04")
DATE_END = datetime.fromisoformat("2025-10-11")


def load_entries() -> pd.DataFrame:
    rows = []
    for path in sorted(INPUT_DIR.glob("*-dados.json")):
        with path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        rows.append(data)
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["data"])
    df["total_hours"] = df["total_sleep_h"].astype(float)
    df["deep_hours"] = df["deep_h"].astype(float)
    df["rem_hours"] = df["rem_h"].astype(float)
    return df.sort_values("date").reset_index(drop=True)


def plot(df: pd.DataFrame) -> None:
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, constrained_layout=True)

    ax_top.plot(df["date"], df["total_hours"], marker="o", label="Sono total (h)")
    ax_top.plot(df["date"], df["deep_hours"], marker="o", label="Sono profundo (h)")
    ax_top.plot(df["date"], df["rem_hours"], marker="o", label="Sono REM (h)")
    ax_top.set_ylabel("Horas")
    ax_top.set_title("Ciclo de Sono — 04 a 11/out/2025")
    ax_top.legend(frameon=False)
    ax_top.grid(alpha=0.2)

    ax_bottom.plot(df["date"], df["body_battery_change"], marker="o", color="#6c5ce7", label="Body Battery Δ")
    ax_bottom.set_ylabel("Body Battery Δ")
    ax_bottom.grid(alpha=0.2)

    ax2 = ax_bottom.twinx()
    ax2.plot(df["date"], df["spo2_min_pct"], marker="s", color="#00b894", label="SpO₂ mínima (%)")
    ax2.set_ylabel("SpO₂ mínima (%)")

    lines, labels = ax_bottom.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax_bottom.legend(lines + lines2, labels + labels2, frameon=False, loc="upper left")

    plt.xticks(rotation=45)
    fig.suptitle("Coerência Semanal do Sono", fontsize=14, y=1.02)
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close(fig)


def main() -> None:
    df = load_entries()
    mask = (df["date"] >= DATE_START) & (df["date"] <= DATE_END)
    df_week = df.loc[mask]
    if df_week.empty:
        raise SystemExit("Nenhum dado encontrado para o intervalo 04–11/out/2025")
    plot(df_week)
    print(f"Gráfico salvo em {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
