
import math

from sklearn.ensemble import IsolationForest


def detect_temperature_anomalies(
    temperatures: list[float],
) -> list[dict]:
    if len(temperatures) < 10:
        raise ValueError(
            "At least 10 temperature readings are required for AI analysis."
        )

    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in temperatures
    ):
        raise ValueError(
            "All temperature readings must be finite numeric values."
        )

    data = [[float(value)] for value in temperatures]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
    )

    model.fit(data)

    predictions = model.predict(data)
    scores = model.decision_function(data)

    results = []

    for temperature, prediction, score in zip(
        temperatures, predictions, scores
    ):
        results.append(
            {
                "temperature": float(temperature),
                "prediction": (
                    "anomaly" if prediction == -1 else "normal"
                ),
                "anomaly_score": round(float(score), 4),
            }
        )

    return results