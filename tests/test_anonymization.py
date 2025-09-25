"""Tests placeholder for anonymization utilities."""

from src.data import anonymization


def test_remove_identifiers_placeholder():
    records = [{"id": 1}]
    result = list(anonymization.remove_identifiers(records))
    assert result == records  # TODO: update when anonymization implemented
