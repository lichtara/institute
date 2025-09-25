"""Funções estatísticas auxiliares (placeholder)."""

from typing import Sequence


def mean(values: Sequence[float]) -> float:
    """Retorna média simples. TODO: substituir por implementação robusta."""
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
