
import pytest

from app.services.temperature_anomaly_service import (
    detect_temperature_anomalies,
)


def test_detects_an_extreme_temperature():
    temperatures = [
        5.2, 5.3, 5.4, 5.5, 5.4,
        5.6, 5.3, 5.5, 5.4, 10.5,
    ]

    results = detect_temperature_anomalies(temperatures)

    assert len(results) == 10
    assert results[-1]["prediction"] == "anomaly"


def test_returns_temperature_and_score():
    temperatures = [
        5.2, 5.3, 5.4, 5.5, 5.4,
        5.6, 5.3, 5.5, 5.4, 5.5,
    ]

    results = detect_temperature_anomalies(temperatures)

    assert results[0]["temperature"] == 5.2
    assert isinstance(results[0]["anomaly_score"], float)
    assert results[0]["prediction"] in {"normal", "anomaly"}


def test_rejects_fewer_than_ten_readings():
    with pytest.raises(ValueError):
        detect_temperature_anomalies([5.0] * 9)


@pytest.mark.parametrize(
    "invalid_temperature",
    [float("nan"), float("inf"), True, "5.0"],
)
def test_rejects_invalid_temperature(invalid_temperature):
    temperatures = [5.0] * 9 + [invalid_temperature]

    with pytest.raises(ValueError):
        detect_temperature_anomalies(temperatures)
