"""Tests placeholder for feature extraction."""

from src.models import features


def test_hrv_features_placeholder():
    result = features.hrv_features([0.8, 0.9, 1.0])
    assert isinstance(result, dict)


def test_gsr_features_placeholder():
    result = features.gsr_features([0.1, 0.2, 0.3])
    assert isinstance(result, dict)
