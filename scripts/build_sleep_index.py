#!/usr/bin/env python3
"""Aggregate validated sleep reports into static API artifacts."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from jsonschema import Draft202012Validator

DEFAULT_INPUT = Path("analysis/reports/diarios_json")
DEFAULT_SCHEMA = Path("schemas/sleep-v1.schema.json")
DEFAULT_OUTPUT = Path("public_api/sleep/v1")
SCHEMA_VERSION = "1.0.0"

NUMERIC_FIELDS: Tuple[str, ...] = (
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
)


def load_validator(schema_path: Path) -> Draft202012Validator:
    with schema_path.open("r", encoding="utf-8") as fp:
        schema = json.load(fp)
    return Draft202012Validator(schema)


def load_entries(input_dir: Path, validator: Draft202012Validator) -> List[Dict[str, Any]]:
    if not input_dir.exists():
        raise SystemExit(f"Diretório de entrada inexistente: {input_dir}")
    entries: List[Dict[str, Any]] = []
    for path in sorted(input_dir.glob("*-dados.json")):
        with path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        validator.validate(data)
        data["_source_path"] = str(path)
        entries.append(data)
    if not entries:
        raise SystemExit(f"Nenhum arquivo encontrado em {input_dir}")
    return entries


def parse_date(entry: Dict[str, Any]) -> datetime:
    try:
        return datetime.strptime(entry["data"], "%Y-%m-%d")
    except KeyError as exc:  # pragma: no cover - garantido pelo schema
        raise SystemExit("Campo 'data' ausente após validação") from exc


def round_value(value: float) -> float:
    return round(float(value), 2)


def compute_stats(entries: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(entries)
    if not rows:
        return {"count": 0, "averages": {}, "totals": {}, "mins": {}, "maxs": {}}
    metrics: Dict[str, Dict[str, float]] = {
        "averages": {},
        "totals": {},
        "mins": {},
        "maxs": {},
    }
    for field in NUMERIC_FIELDS:
        values = [row[field] for row in rows if field in row and isinstance(row[field], (int, float))]
        if not values:
            continue
        metrics["totals"][field] = round_value(sum(values))
        metrics["averages"][field] = round_value(sum(values) / len(values))
        metrics["mins"][field] = round_value(min(values))
        metrics["maxs"][field] = round_value(max(values))
    summary: Dict[str, Any] = {"count": len(rows)}
    summary.update(metrics)
    return summary


def build_days(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ordered = sorted(entries, key=parse_date)
    days: List[Dict[str, Any]] = []
    for item in ordered:
        day = {k: v for k, v in item.items() if not k.startswith("_")}
        day.setdefault("schema_version", SCHEMA_VERSION)
        days.append(day)
    return days


def build_weeks(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    buckets: Dict[Tuple[int, int], List[Dict[str, Any]]] = defaultdict(list)
    for item in entries:
        dt = parse_date(item)
        year, week, _ = dt.isocalendar()
        buckets[(year, week)].append(item)
    weeks: List[Dict[str, Any]] = []
    for (year, week), rows in sorted(buckets.items()):
        dates = sorted(parse_date(row) for row in rows)
        weeks.append(
            {
                "schema_version": SCHEMA_VERSION,
                "week": f"{year}-W{week:02d}",
                "start_date": dates[0].strftime("%Y-%m-%d"),
                "end_date": dates[-1].strftime("%Y-%m-%d"),
                "summary": compute_stats(rows),
            }
        )
    return weeks


def build_months(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    buckets: Dict[Tuple[int, int], List[Dict[str, Any]]] = defaultdict(list)
    for item in entries:
        dt = parse_date(item)
        buckets[(dt.year, dt.month)].append(item)
    months: List[Dict[str, Any]] = []
    for (year, month), rows in sorted(buckets.items()):
        dates = sorted(parse_date(row) for row in rows)
        months.append(
            {
                "schema_version": SCHEMA_VERSION,
                "month": f"{year}-{month:02d}",
                "start_date": dates[0].strftime("%Y-%m-%d"),
                "end_date": dates[-1].strftime("%Y-%m-%d"),
                "summary": compute_stats(rows),
            }
        )
    return months


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2, ensure_ascii=False)
        fp.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Diretório com arquivos *-dados.json")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Schema JSON para validação")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="Diretório de saída da mini-API")
    args = parser.parse_args()

    validator = load_validator(args.schema)
    entries = load_entries(args.input, validator)

    generated_at = datetime.now(timezone.utc).isoformat()
    days = build_days(entries)
    summary = compute_stats(entries)
    summary["range"] = {
        "start": min(parse_date(e) for e in entries).strftime("%Y-%m-%d"),
        "end": max(parse_date(e) for e in entries).strftime("%Y-%m-%d"),
    }

    index_payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "days": days,
        "summary": summary,
    }
    weeks_payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "weeks": build_weeks(entries),
    }
    months_payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "months": build_months(entries),
    }

    write_json(args.out / "index.json", index_payload)
    write_json(args.out / "weekly.json", weeks_payload)
    write_json(args.out / "monthly.json", months_payload)

    print(f"Gerados arquivos em {args.out}")


if __name__ == "__main__":
    main()
