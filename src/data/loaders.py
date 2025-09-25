"""Funções de carregamento de dados sintéticos (placeholder)."""

from pathlib import Path
from typing import Any


def load_sample(name: str) -> Any:
    """Carrega amostras sintéticas de `data/samples`. TODO: definir formato."""
    sample_path = Path(__file__).resolve().parents[2] / "data" / "samples" / name
    if not sample_path.exists():
        raise FileNotFoundError(f"Sample not found: {sample_path}")
    # TODO: implementar leitura conforme schema (CSV, JSON, etc.)
    return sample_path
