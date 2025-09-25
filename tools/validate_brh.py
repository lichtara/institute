#!/usr/bin/env python3
"""Validate BRH sample CSVs against their JSON Schemas."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, Tuple

from jsonschema import Draft202012Validator, ValidationError


SCHEMA_SAMPLE_MAP: Tuple[Tuple[str, str], ...] = (
    ("data/schemas/brh_protocolos.schema.json", "data/samples/brh_protocolos.sample.csv"),
    ("data/schemas/brh_sessoes.schema.json", "data/samples/brh_sessoes.sample.csv"),
    ("data/schemas/brh_metricas.schema.json", "data/samples/brh_metricas.sample.csv"),
)


def load_schema(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def cast_row(row: Dict[str, str], schema: Dict) -> Dict:
    """Cast CSV string values to the types expected by the schema when possible."""
    properties = schema.get("properties", {})
    casted = dict(row)
    for field, definition in properties.items():
        if field not in casted:
            continue
        value = casted[field]
        if value == "":
            continue
        expected_type = definition.get("type")
        if expected_type == "number":
            try:
                casted[field] = float(value)
            except ValueError:
                raise ValidationError(f"Campo '{field}' deveria ser numérico, valor recebido '{value}'")
    return casted


def iter_rows(csv_path: Path) -> Iterable[Dict[str, str]]:
    with csv_path.open("r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield row


def validate_pair(schema_path: Path, sample_path: Path) -> None:
    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema)
    for idx, row in enumerate(iter_rows(sample_path), start=1):
        data = cast_row(row, schema)
        validator.validate(data)
    print(f"✔ {sample_path} válido segundo {schema_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pairs",
        nargs="*",
        default=["::".join(pair) for pair in SCHEMA_SAMPLE_MAP],
        help="Pares schema::sample a validar (default: todos).",
    )
    args = parser.parse_args()

    for pair in args.pairs:
        try:
            schema_str, sample_str = pair.split("::", maxsplit=1)
        except ValueError as exc:
            raise SystemExit(f"Formato inválido para par '{pair}'. Use schema::sample.") from exc
        schema_path = Path(schema_str)
        sample_path = Path(sample_str)
        if not schema_path.exists():
            raise SystemExit(f"Schema não encontrado: {schema_path}")
        if not sample_path.exists():
            raise SystemExit(f"Sample não encontrado: {sample_path}")
        validate_pair(schema_path, sample_path)


if __name__ == "__main__":
    main()
