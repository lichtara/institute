"""Ferramentas de anonimização (rascunho)."""

from typing import Iterable, Mapping


def remove_identifiers(records: Iterable[Mapping]) -> Iterable[Mapping]:
    """Remover campos proibidos segundo docs/data-policy.md. TODO: implementar."""
    for record in records:
        yield record  # Placeholder


def apply_noise(record: Mapping, *, epsilon: float = 0.0) -> Mapping:
    """Aplicar ruído diferencial. TODO: especificar mecanismo adequado."""
    return record
