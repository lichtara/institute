#!/usr/bin/env python3
"""Generate diary index files for BRH sessions and complementary notes."""
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

SESSAO_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-sessao-(?P<num>\d+)(?:-[\w-]+)?\.(?P<ext>md|pdf|png)$",
    re.IGNORECASE,
)
EXTRA_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?!sessao-)(?P<label>[\w-]+)\.(?P<ext>md|pdf|png)$",
    re.IGNORECASE,
)

SESSAO_HEADER = """# Diários BRH

Este índice é gerado automaticamente. Para incluir um novo diário:
1. Crie arquivos em `analysis/reports/diarios/` usando o padrão `YYYY-MM-DD-sessao-NN`.
2. Inclua o registro `.md` e, se disponível, anexos `.pdf` e capturas do Garmin (`-garmin.png`).
3. Execute `make diarios-index` para atualizar este índice.

| Data | Sessão | Diário (.md) | PDF | Print Garmin |
|---|---:|---|---|---|
"""
EXTRA_HEADER = """
## Notas complementares

| Data | Descrição | Arquivos |
|---|---|---|
"""


@dataclass
class SessaoEntry:
    date: str
    num: int
    files: Dict[str, Path]

    def get(self, ext: str) -> Path | None:
        return self.files.get(ext)


@dataclass
class ExtraEntry:
    date: str
    label: str
    files: Dict[str, Path]

    def get(self, ext: str) -> Path | None:
        return self.files.get(ext)


def collect_entries() -> Tuple[Dict[Tuple[str, int], SessaoEntry], Dict[Tuple[str, str], ExtraEntry]]:
    sessoes: Dict[Tuple[str, int], SessaoEntry] = {}
    extras: Dict[Tuple[str, str], ExtraEntry] = {}

    if not DIARIOS_DIR.exists():
        return sessoes, extras

    for candidate in DIARIOS_DIR.iterdir():
        if not candidate.is_file():
            continue

        match_sessao = SESSAO_PATTERN.match(candidate.name)
        match_extra = EXTRA_PATTERN.match(candidate.name)

        if match_sessao:
            date = match_sessao.group("date")
            num = int(match_sessao.group("num"))
            ext = match_sessao.group("ext").lower()
            key = (date, num)
            entry = sessoes.setdefault(key, SessaoEntry(date=date, num=num, files={}))
            entry.files[ext] = candidate
        elif match_extra:
            date = match_extra.group("date")
            label = match_extra.group("label")
            ext = match_extra.group("ext").lower()
            key = (date, label)
            entry = extras.setdefault(key, ExtraEntry(date=date, label=label, files={}))
            entry.files[ext] = candidate

    return sessoes, extras


def relpath(path: Path) -> str:
    try:
        return "/" + path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def format_links(entry_files: Dict[str, Path]) -> str:
    links = []
    for ext, label in (("md", "MD"), ("pdf", "PDF"), ("png", "PNG")):
        path = entry_files.get(ext)
        if path:
            links.append(f"[{label}]({relpath(path)})")
    return ", ".join(links) if links else "—"


def build_index(sessoes: Dict[Tuple[str, int], SessaoEntry], extras: Dict[Tuple[str, str], ExtraEntry]) -> str:
    rows = []
    for key in sorted(sessoes.keys(), reverse=True):
        entry = sessoes[key]
        md = entry.get("md")
        pdf = entry.get("pdf")
        png = entry.get("png")

        md_cell = f"[diário]({relpath(md)})" if md else "—"
        pdf_cell = f"[pdf]({relpath(pdf)})" if pdf else "—"
        png_cell = f"[imagem]({relpath(png)})" if png else "—"

        rows.append(f"| {entry.date} | {entry.num:02d} | {md_cell} | {pdf_cell} | {png_cell} |")

    content = SESSAO_HEADER + "\n".join(rows)
    if rows:
        content += "\n"

    if extras:
        extra_rows = []
        for key in sorted(extras.keys(), reverse=True):
            entry = extras[key]
            label = entry.label
            if '-' in label:
                desc_title = '-'.join(part.capitalize() for part in label.split('-'))
            else:
                desc_title = label.replace('_', ' ').title()
            extra_rows.append(
                f"| {entry.date} | {desc_title} | {format_links(entry.files)} |"
            )
        content += EXTRA_HEADER + "\n".join(extra_rows) + "\n"

    return content


def build_readme(sessoes: Dict[Tuple[str, int], SessaoEntry], extras: Dict[Tuple[str, str], ExtraEntry], existing_extra_block: str | None = None) -> str:
    lines = [
        "# Diário BRH",
        "",
        "Registros de práticas individuais organizados por data no formato `YYYY-MM-DD-sessao-NN`.",
        "",
        "## Convenção",
        "",
        "- **YYYY-MM-DD** — data da prática.",
        "- **sessao-NN** — número sequencial do registro no dia.",
        "- Para cada data mantemos normalmente:",
        "  - um arquivo `.md` com o registro detalhado;",
        "  - anexos relevantes (imagens, PDFs, biofeedback).",
        "",
        "## Último registro",
        "",
    ]

    if sessoes:
        latest_key = max(sessoes.keys())
        latest = sessoes[latest_key]
        md = latest.get("md")
        pdf = latest.get("pdf")
        png = latest.get("png")
        lines.extend([
            f"- **Data:** {latest.date} • **Sessão:** {latest.num:02d}",
            f"- MD: [{md.name}]({relpath(md)})" if md else "- MD: —",
            f"- PDF: [{pdf.name}]({relpath(pdf)})" if pdf else "- PDF: —",
            f"- Print: [{png.name}]({relpath(png)})" if png else "- Print: —",
        ])
    else:
        lines.append("- Nenhum registro disponível no momento.")

    lines.extend([
        "",
        "## Como adicionar novos registros",
        "",
        "1. Criar arquivos seguindo a convenção acima dentro desta pasta.",
        "2. Referenciar anexos na seção **Anexos** do `.md` correspondente.",
        "3. Executar `make diarios-index` para atualizar o índice e este README.",
    ])

    if existing_extra_block:
        lines.extend(["", existing_extra_block.strip()])

    return "\n".join(lines).rstrip() + "\n"


def extract_extra_block() -> str | None:
    if not README_DIARIOS.exists():
        return None
    text = README_DIARIOS.read_text(encoding="utf-8")
    match = re.search(r"(### .*)", text, flags=re.DOTALL)
    return match.group(1) if match else None


def main() -> int:
    sessoes, extras = collect_entries()

    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)
    INDEX_MD.write_text(build_index(sessoes, extras), encoding="utf-8")

    extra_block = extract_extra_block()
    README_DIARIOS.write_text(
        build_readme(sessoes, extras, existing_extra_block=extra_block),
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
