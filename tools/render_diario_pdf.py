#!/usr/bin/env python3
"""Generate a multi-page PDF for a BRH diary entry.

Usage:
    python tools/render_diario_pdf.py \
        --summary analysis/reports/diarios/2025-09-27-relatorio.md \
        --output analysis/reports/diarios/2025-09-27-diario.pdf \
        --title "Diário BRH — 27/09/2025" \
        --image "analysis/reports/diarios/2025-09-27-fc.png::Frequência cardíaca" \
        --image "analysis/reports/diarios/2025-09-27-body-battery.png::Body Battery" \
        ...

The summary Markdown is rendered as plain text on the first page. Each
``--image`` argument accepts ``PATH::CAPTION``. When images are missing,
a placeholder page is added informing which file was not found.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import wrap
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages


def load_summary_text(summary_path: Path) -> list[str]:
    text = summary_path.read_text(encoding="utf-8")
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped.startswith("#"):
            stripped = stripped.lstrip("# ")
            lines.append(stripped.upper())
            continue
        indent = "  " if stripped.startswith("-") else ""
        stripped = stripped.lstrip("- ")
        wrapped = wrap(stripped, width=90)
        if not wrapped:
            lines.append(indent + stripped)
        else:
            lines.extend(indent + w for w in wrapped)
    return lines


def add_text_page(pdf: PdfPages, title: str, lines: list[str]) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    plt.axis("off")
    y = 0.95
    plt.text(0.5, y, title, ha="center", va="top", fontsize=18, weight="bold")
    y -= 0.05
    for line in lines:
        if not line:
            y -= 0.02
            continue
        plt.text(0.08, y, line, ha="left", va="top", fontsize=11)
        y -= 0.03
        if y < 0.1:
            break
    timestamp = datetime.now().strftime("Gerado em %Y-%m-%d %H:%M")
    plt.text(0.08, 0.06, timestamp, fontsize=9, alpha=0.6)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_image_page(pdf: PdfPages, image_path: Path, caption: str) -> None:
    if not image_path.exists():
        fig = plt.figure(figsize=(8.27, 11.69))
        plt.axis("off")
        message = f"Arquivo não encontrado:\n{image_path}"
        plt.text(0.5, 0.5, message, ha="center", va="center", fontsize=12)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
        return

    img = mpimg.imread(image_path)
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")
    plt.text(0.5, 0.96, caption, ha="center", va="top", fontsize=14, weight="bold")
    ax = fig.add_axes([0.08, 0.12, 0.84, 0.8])
    ax.imshow(img)
    ax.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def parse_image_args(values: list[str]) -> list[tuple[Path, str]]:
    result: list[tuple[Path, str]] = []
    for value in values:
        if "::" in value:
            path_str, caption = value.split("::", 1)
        else:
            path_str, caption = value, Path(value).stem
        result.append((Path(path_str), caption.strip()))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate BRH diary PDF")
    parser.add_argument("--summary", required=True, type=Path, help="Markdown file with summary text")
    parser.add_argument("--output", required=True, type=Path, help="Output PDF path")
    parser.add_argument("--title", required=True, help="Title for the summary page")
    parser.add_argument("--image", action="append", default=[], help="Image specification: PATH::CAPTION")
    args = parser.parse_args()

    summary_lines = load_summary_text(args.summary)
    image_specs = parse_image_args(args.image)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(args.output) as pdf:
        add_text_page(pdf, args.title, summary_lines)
        for path, caption in image_specs:
            add_image_page(pdf, path, caption)

    print(f"PDF gerado em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
