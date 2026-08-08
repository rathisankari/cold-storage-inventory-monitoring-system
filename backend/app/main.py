from fastapi import FastAPI

from app.api.inventory import router as inventory_router
from app.api.storage_unit import router as storage_unit_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import Inventory

app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(inventory_router)
app.include_router(storage_unit_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}