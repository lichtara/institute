#!/usr/bin/env python3
"""Generate analytic artefacts from structured sleep reports.

Reads JSON entries produced in ``analysis/reports/diarios_json`` (schema v1) and
produces:

* CSV detalhado por noite com métricas derivadas.
* CSV semanal (ISO week) com agregados básicos.
* Gráficos PNG (horas totais, fases, SpO₂ mínima, correlação Body Battery).
* Sumário textual com insights rápidos em formato Markdown.

Artefactos são salvos em ``analysis/reports/summaries/sleep_2025-09-25_2025-10-07``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List

import pandas as pd


@dataclass
class SleepEntry:
    date: datetime
    start_time: str
    end_time: str
    total_sleep_h: float
    deep_h: float
    light_h: float
    rem_h: float
    awake_min: int
    hr_rest_bpm: int
    body_battery_change: int
    spo2_avg_pct: float
    spo2_min_pct: float
    resp_rate_avg_brpm: float
    resp_rate_min_brpm: float


INPUT_DIR = Path("analysis/reports/diarios_json")
OUTPUT_DIR = Path("analysis/reports/summaries/sleep_2025-09-25_2025-10-07")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_entries() -> List[dict]:
    rows = []
    for path in sorted(INPUT_DIR.glob("*-dados.json")):
        data = json.loads(path.read_text())
        rows.append(data)
    return rows


def build_dataframe(rows: Iterable[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["data"])
    df = df.sort_values("date").reset_index(drop=True)

    # Durations in minutes
    for col in ("total", "deep", "light", "rem"):
        df[f"{col}_min"] = df[f"{col}_h"] = df[f"{col}_h"] if f"{col}_h" in df.columns else None

    df["total_min"] = (df["total_sleep_h"] * 60).round(2)
    df["deep_min"] = (df["deep_h"] * 60).round(2)
    df["light_min"] = (df["light_h"] * 60).round(2)
    df["rem_min"] = (df["rem_h"] * 60).round(2)

    df["total_hours"] = df["total_sleep_h"].round(2)

    df["deep_pct"] = (df["deep_min"] / df["total_min"] * 100).round(1)
    df["light_pct"] = (df["light_min"] / df["total_min"] * 100).round(1)
    df["rem_pct"] = (df["rem_min"] / df["total_min"] * 100).round(1)

    df["meets_7h"] = df["total_min"] >= 7 * 60
    df["spo2_flag_low"] = df["spo2_min_pct"] < 88
    df["rem_low_flag"] = df["rem_min"] < 60
    df["deep_target_flag"] = df["deep_min"] >= 90

    df["start_dt"] = df.apply(lambda r: _compose_datetime(r["date"], r.get("start_time")), axis=1)
    df["end_dt"] = df.apply(lambda r: _compose_datetime(r["date"], r.get("end_time")), axis=1)
    mask = (df["end_dt"].notna()) & (df["start_dt"].notna()) & (df["end_dt"] < df["start_dt"])
    df.loc[mask, "end_dt"] += pd.Timedelta(days=1)

    return df


def _compose_datetime(base_date: pd.Timestamp, time_str: str | None) -> pd.Timestamp | pd.NaT:
    if not time_str:
        return pd.NaT
    try:
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return pd.NaT
    return pd.Timestamp(datetime.combine(base_date.date(), time_obj))


def compute_weekly(df: pd.DataFrame) -> pd.DataFrame:
    iso = df["date"].dt.isocalendar()
    df = df.assign(iso_year=iso.year, iso_week=iso.week)
    weekly = (
        df.groupby(["iso_year", "iso_week"])
        .agg(
            nights=("date", "count"),
            avg_total_h=("total_hours", "mean"),
            avg_deep_min=("deep_min", "mean"),
            avg_rem_min=("rem_min", "mean"),
            avg_rhr=("hr_rest_bpm", "mean"),
            avg_spo2_avg=("spo2_avg_pct", "mean"),
            avg_spo2_min=("spo2_min_pct", "mean"),
            avg_resp=("resp_rate_avg_brpm", "mean"),
            avg_body_batt=("body_battery_change", "mean"),
        )
        .round(2)
        .reset_index()
    )
    weekly["iso_year_week"] = weekly.apply(lambda r: f"{int(r.iso_year)}-W{int(r.iso_week):02d}", axis=1)
    return weekly[
        [
            "iso_year_week",
            "nights",
            "avg_total_h",
            "avg_deep_min",
            "avg_rem_min",
            "avg_rhr",
            "avg_spo2_avg",
            "avg_spo2_min",
            "avg_resp",
            "avg_body_batt",
        ]
    ]


def save_artifacts(df: pd.DataFrame, weekly: pd.DataFrame) -> None:
    detail_cols = [
        "data",
        "start_time",
        "end_time",
        "total_sleep_h",
        "deep_h",
        "light_h",
        "rem_h",
        "awake_min",
        "hr_rest_bpm",
        "body_battery_change",
        "spo2_avg_pct",
        "spo2_min_pct",
        "resp_rate_avg_brpm",
        "resp_rate_min_brpm",
        "total_min",
        "deep_min",
        "light_min",
        "rem_min",
        "deep_pct",
        "light_pct",
        "rem_pct",
        "meets_7h",
        "spo2_flag_low",
        "rem_low_flag",
        "deep_target_flag",
    ]
    df[detail_cols].to_csv(OUTPUT_DIR / "sleep_detail_2025-09-25_2025-10-07.csv", index=False)
    weekly.to_csv(OUTPUT_DIR / "sleep_weekly_summary.csv", index=False)


def plot_artifacts(df: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["total_hours"], marker="o")
    plt.title("Total de sono por noite")
    plt.xlabel("Data")
    plt.ylabel("Horas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart_total_sleep_hours.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["deep_min"], marker="o", label="Profundo (min)")
    plt.plot(df["date"], df["rem_min"], marker="o", label="REM (min)")
    plt.title("Fases de sono por noite")
    plt.xlabel("Data")
    plt.ylabel("Minutos")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart_sleep_stages.png", dpi=200)
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.scatter(df["total_hours"], df["body_battery_change"], alpha=0.8)
    for _, row in df.iterrows():
        plt.annotate(row["data"], (row["total_hours"], row["body_battery_change"]), fontsize=7)
    plt.title("Sono total vs Body Battery Δ")
    plt.xlabel("Sono total (h)")
    plt.ylabel("Body Battery (Δ)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart_total_vs_bodybattery.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["spo2_min_pct"], marker="o")
    plt.axhline(88, linestyle="--", color="red", linewidth=1)
    plt.title("SpO₂ mínima por noite")
    plt.xlabel("Data")
    plt.ylabel("SpO₂ mínima (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chart_spo2_min.png", dpi=200)
    plt.close()


def write_summary(df: pd.DataFrame) -> None:
    corr = df[[
        "total_min",
        "deep_min",
        "rem_min",
        "hr_rest_bpm",
        "spo2_avg_pct",
        "spo2_min_pct",
        "resp_rate_avg_brpm",
        "body_battery_change",
    ]].corr()

    avg_total = df["total_hours"].mean().round(2)
    med_total = df["total_hours"].median().round(2)
    pct_7h = (df["meets_7h"].mean() * 100).round(1)
    avg_deep = df["deep_min"].mean().round(1)
    pct_deep_target = (df["deep_target_flag"].mean() * 100).round(1)
    avg_rem = df["rem_min"].mean().round(1)
    pct_rem_low = (df["rem_low_flag"].mean() * 100).round(1)
    avg_spo2_min = df["spo2_min_pct"].mean().round(1)
    nights_spo2_low = int(df["spo2_flag_low"].sum())
    corr_total_bb = corr.loc["total_min", "body_battery_change"].round(2)
    best = df.loc[df["total_min"].idxmax()]
    shortest = df.loc[df["total_min"].idxmin()]

    md_path = OUTPUT_DIR / "sleep_insights.md"
    md_path.write_text(
        """# Resumo de Sono — 25/09 a 07/10/2025

* Noites analisadas: {nights}
* Sono total médio: {avg_total} h (mediana {med_total} h)
* Noites ≥7h: {pct_7h}%
* Sono profundo médio: {avg_deep} min — {pct_deep_target}% das noites ≥90 min
* Sono REM médio: {avg_rem} min — {pct_rem_low}% das noites <60 min
* SpO₂ mínima média: {avg_spo2_min}% — {nights_spo2_low} noites abaixo de 88%
* Correlação sono total ↔ Body Battery Δ: {corr_total_bb}
* Noite mais longa: {best_date} ({best_hours} h)
* Noite mais curta: {shortest_date} ({shortest_hours} h)

Artefactos gerados em `{output}`.
""".format(
            nights=len(df),
            avg_total=avg_total,
            med_total=med_total,
            pct_7h=pct_7h,
            avg_deep=avg_deep,
            pct_deep_target=pct_deep_target,
            avg_rem=avg_rem,
            pct_rem_low=pct_rem_low,
            avg_spo2_min=avg_spo2_min,
            nights_spo2_low=nights_spo2_low,
            corr_total_bb=corr_total_bb,
            best_date=best["data"],
            best_hours=(best["total_min"] / 60).round(2),
            shortest_date=shortest["data"],
            shortest_hours=(shortest["total_min"] / 60).round(2),
            output=OUTPUT_DIR,
        )
    )


def main() -> None:
    rows = load_entries()
    df = build_dataframe(rows)
    weekly = compute_weekly(df)
    save_artifacts(df, weekly)
    plot_artifacts(df)
    write_summary(df)
    print(f"Gerados artefactos em {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

