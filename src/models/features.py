"""Extração de features para BRH (placeholder)."""

from typing import Sequence


def hrv_features(rr_intervals: Sequence[float]) -> dict:
    """Calcular métricas HRV básicas. TODO: implementar rmssd, sdnn etc."""
    return {}


def gsr_features(signal: Sequence[float]) -> dict:
    """Calcular métricas GSR. TODO: separar componentes tônico/fásico."""
    return {}
