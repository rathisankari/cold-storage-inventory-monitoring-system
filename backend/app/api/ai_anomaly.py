
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.storage_unit import StorageUnit
from app.models.temperature_log import TemperatureLog
from app.models.user import User
from app.services.temperature_anomaly_service import (
    detect_temperature_anomalies,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Anomaly Detection"],
)


@router.get("/anomalies/{storage_unit_id}")
def get_temperature_anomalies(
    storage_unit_id: int,
    limit: int = Query(default=100, ge=10, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    ),
):
    storage_unit = (
        db.query(StorageUnit)
        .filter(StorageUnit.id == storage_unit_id)
        .first()
    )

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found",
        )

    logs = (
        db.query(TemperatureLog)
        .filter(
            TemperatureLog.storage_unit_id == storage_unit_id
        )
        .order_by(TemperatureLog.recorded_at.desc())
        .limit(limit)
        .all()
    )

    if len(logs) < 10:
        raise HTTPException(
            status_code=400,
            detail="At least 10 historical readings are required.",
        )

    logs.reverse()
    temperatures = [float(log.temperature) for log in logs]

    try:
        predictions = detect_temperature_anomalies(temperatures)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    results = []

    for log, prediction in zip(logs, predictions):
        temperature = prediction["temperature"]
        threshold_breach = (
            temperature < storage_unit.min_temp
            or temperature > storage_unit.max_temp
        )

        results.append(
            {
                "reading_id": log.id,
                "storage_unit_id": log.storage_unit_id,
                "recorded_at": log.recorded_at,
                "temperature": temperature,
                "ai_prediction": prediction["prediction"],
                "anomaly_score": prediction["anomaly_score"],
                "temperature_status": (
                    "outside_safe_range"
                    if threshold_breach
                    else "within_safe_range"
                ),
                "threshold_breach": threshold_breach,
                "source": log.source,
            }
        )

    anomaly_count = sum(
        result["ai_prediction"] == "anomaly"
        for result in results
    )

    threshold_breach_count = sum(
        result["threshold_breach"]
        for result in results
    )

    return {
        "storage_unit_id": storage_unit.id,
        "storage_unit_name": storage_unit.name,
        "configured_min_temp": storage_unit.min_temp,
        "configured_max_temp": storage_unit.max_temp,
        "readings_analyzed": len(results),
        "anomaly_count": anomaly_count,
        "threshold_breach_count": threshold_breach_count,
        "method": "Isolation Forest",
        "results": results,
    }
