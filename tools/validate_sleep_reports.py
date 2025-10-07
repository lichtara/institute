#!/usr/bin/env python3
"""Validate daily sleep JSON reports against the BRH sleep-entry schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, ValidationError

DEFAULT_SCHEMA = Path("analysis/reports/diarios/schema/sleep-entry.schema.json")
DEFAULT_GLOB = "analysis/reports/diarios/*-dados.json"


def find_files(pattern: str) -> Iterable[Path]:
    return sorted(Path().glob(pattern))


def load_schema(path: Path) -> Draft202012Validator:
    if not path.exists():
        raise SystemExit(f"Schema não encontrado: {path}")
    with path.open("r", encoding="utf-8") as fp:
        schema = json.load(fp)
    return Draft202012Validator(schema)


def validate_file(validator: Draft202012Validator, path: Path) -> None:
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    validator.validate(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Caminho para o schema JSON (default: %(default)s)",
    )
    parser.add_argument(
        "--glob",
        default=DEFAULT_GLOB,
        help="Padrão glob para localizar os relatórios (default: %(default)s)",
    )
    args = parser.parse_args()

    validator = load_schema(args.schema)
    files = list(find_files(args.glob))
    if not files:
        raise SystemExit(f"Nenhum arquivo encontrado com o padrão '{args.glob}'.")

    ok = 0
    for path in files:
        try:
            validate_file(validator, path)
        except ValidationError as exc:
            raise SystemExit(f"✖ {path} inválido: {exc.message}")
        ok += 1
        print(f"✔ {path} válido")

    print(f"\n{ok} arquivo(s) validados com sucesso contra {args.schema}")


if __name__ == "__main__":
    main()
