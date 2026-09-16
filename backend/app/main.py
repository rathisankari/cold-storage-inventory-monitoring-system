from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.inventory import router as inventory_router
from app.api.storage_unit import router as storage_unit_router
from app.api.temperature_log import router as temperature_log_router
from app.api.alert import router as alert_router
from app.api.monitoring import router as monitoring_router
from app.api.audit import router as audit_router

from app.core.config import settings
from app.core.database import Base, engine

from app.models import (
    Inventory,
    TemperatureLog,
    StorageUnit,
    Alert,
)


app = FastAPI(title=settings.PROJECT_NAME)


# Allow the React frontend to communicate with the FastAPI backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables if they do not already exist
Base.metadata.create_all(bind=engine)


# API routes
app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(storage_unit_router)
app.include_router(temperature_log_router)
app.include_router(monitoring_router)
app.include_router(alert_router)
app.include_router(audit_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}