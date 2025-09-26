#!/usr/bin/env python3
"""Generate diary index files for BRH sessions."""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
DIARIOS_DIR = ROOT / "analysis" / "reports" / "diarios"
DOCS_DIR = ROOT / "docs"
README_DIARIOS = DIARIOS_DIR / "README.md"
INDEX_MD = DOCS_DIR / "_diarios.md"

PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-sessao-(?P<num>\d+)(?:-[\w-]+)?\.(?P<ext>md|pdf|png)$",
    re.IGNORECASE,
)

HEADER = """# Diários BRH

Este índice é gerado automaticamente. Para incluir um novo diário:
1. Crie arquivos em `analysis/reports/diarios/` usando o padrão `YYYY-MM-DD-sessao-NN`.
2. Inclua o registro `.md` e, se disponível, anexos `.pdf` e capturas do Garmin (`-garmin.png`).
3. Execute `make diarios-index` para atualizar este índice.

| Data | Sessão | Diário (.md) | PDF | Print Garmin |
|---|---:|---|---|---|
"""

ROW_TEMPLATE = "| {date} | {sess:02d} | {md_cell} | {pdf_cell} | {png_cell} |"


@dataclass
class Entry:
    date: str
    num: int
    files: Dict[str, Path]

    def get(self, ext: str) -> Path | None:
        return self.files.get(ext)


def collect_entries() -> Dict[Tuple[str, int], Entry]:
    entries: Dict[Tuple[str, int], Entry] = {}

    if not DIARIOS_DIR.exists():
        return entries

    for candidate in DIARIOS_DIR.iterdir():
        match = PATTERN.match(candidate.name)
        if not match or not candidate.is_file():
            continue

        date = match.group("date")
        num = int(match.group("num"))
        ext = match.group("ext").lower()

        key = (date, num)
        entry = entries.setdefault(key, Entry(date=date, num=num, files={}))
        entry.files[ext] = candidate

    return entries


def relpath(path: Path) -> str:
    try:
        return "/" + path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_index(entries: Dict[Tuple[str, int], Entry]) -> str:
    rows = []
    for key in sorted(entries.keys(), reverse=True):
        entry = entries[key]
        md = entry.get("md")
        pdf = entry.get("pdf")
        png = entry.get("png")

        md_cell = f"[diário]({relpath(md)})" if md else "—"
        pdf_cell = f"[pdf]({relpath(pdf)})" if pdf else "—"
        png_cell = f"[imagem]({relpath(png)})" if png else "—"

        rows.append(
            ROW_TEMPLATE.format(
                date=entry.date,
                sess=entry.num,
                md_cell=md_cell,
                pdf_cell=pdf_cell,
                png_cell=png_cell,
            )
        )

    content = HEADER + "\n".join(rows)
    if rows:
        content += "\n"
    return content


def ensure_readme_base() -> str:
    if README_DIARIOS.exists():
        return README_DIARIOS.read_text(encoding="utf-8")

    README_DIARIOS.parent.mkdir(parents=True, exist_ok=True)
    base = (
        "# Diário BRH\n\n"
        "Registros de práticas individuais organizados por data no formato ``YYYY-MM-DD-sessao-NN``.\n\n"
        "## Convenção\n\n"
        "- **YYYY-MM-DD** — data da prática.\n"
        "- **sessao-NN** — número sequencial do registro no dia.\n"
        "- Normalmente mantemos arquivos `.md`, anexos `.pdf` e imagens associadas.\n\n"
        "## Último registro\n\n"
        "- Nenhum registro disponível no momento.\n\n"
        "## Como adicionar novos registros\n\n"
        "1. Criar arquivos seguindo a convenção acima dentro desta pasta.\n"
        "2. Referenciar anexos na seção **Anexos** do `.md` correspondente.\n"
        "3. Executar `make diarios-index` para atualizar o índice e este README.\n"
    )
    README_DIARIOS.write_text(base, encoding="utf-8")
    return base


def update_readme(entries: Dict[Tuple[str, int], Entry]) -> None:
    readme_text = ensure_readme_base()

    if entries:
        latest_key = max(entries.keys())
        latest = entries[latest_key]
        md = latest.get("md")
        pdf = latest.get("pdf")
        png = latest.get("png")
        block_lines = [
            "## Último registro\n",
            f"- **Data:** {latest.date} • **Sessão:** {latest.num:02d}",
            f"- MD: [{md.name}]({relpath(md)})" if md else "- MD: —",
            f"- PDF: [{pdf.name}]({relpath(pdf)})" if pdf else "- PDF: —",
            f"- Print: [{png.name}]({relpath(png)})" if png else "- Print: —",
            "",
        ]
    else:
        block_lines = ["## Último registro\n", "- Nenhum registro disponível no momento.\n"]

    block = "\n".join(block_lines)

    if "## Último registro" in readme_text:
        readme_text = re.sub(
            r"(?s)## Último registro.*?(?=^## |\Z)",
            block,
            readme_text,
            flags=re.MULTILINE,
        )
    else:
        readme_text = readme_text.rstrip() + "\n\n" + block

    README_DIARIOS.write_text(readme_text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    entries = collect_entries()

    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)
    INDEX_MD.write_text(build_index(entries), encoding="utf-8")
    update_readme(entries)

    return 0


if __name__ == "__main__":
    sys.exit(main())
