from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.storage_unit import StorageUnit
from app.models.user import User
from app.schemas.storage_unit import (
    StorageUnitCreate,
    StorageUnitResponse,
    StorageUnitUpdate,
)
from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/storage-units",
    tags=["Storage Units"]
)


@router.get("/", response_model=list[StorageUnitResponse])
def get_storage_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    storage_units = db.query(StorageUnit).all()
    return storage_units


@router.get("/{storage_unit_id}", response_model=StorageUnitResponse)
def get_storage_unit_by_id(
    storage_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    storage_unit = db.query(StorageUnit).filter(
        StorageUnit.id == storage_unit_id
    ).first()

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    return storage_unit


@router.post("/", response_model=StorageUnitResponse)
def create_storage_unit(
    storage_unit: StorageUnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    new_storage_unit = StorageUnit(
        name=storage_unit.name,
        facility_id=storage_unit.facility_id,
        unit_type=storage_unit.unit_type,
        min_temp=storage_unit.min_temp,
        max_temp=storage_unit.max_temp,
        status=storage_unit.status,
        last_service_date=storage_unit.last_service_date,
    )

    db.add(new_storage_unit)
    db.commit()
    db.refresh(new_storage_unit)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CREATE_STORAGE_UNIT",
        resource_type="StorageUnit",
        resource_id=str(new_storage_unit.id),
        new_values={
            "name": new_storage_unit.name,
            "facility_id": new_storage_unit.facility_id,
            "unit_type": new_storage_unit.unit_type,
            "min_temp": new_storage_unit.min_temp,
            "max_temp": new_storage_unit.max_temp,
            "status": new_storage_unit.status,
        }
    )

    return new_storage_unit


@router.put("/{storage_unit_id}", response_model=StorageUnitResponse)
def update_storage_unit(
    storage_unit_id: int,
    storage_unit_data: StorageUnitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    storage_unit = db.query(StorageUnit).filter(
        StorageUnit.id == storage_unit_id
    ).first()

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    old_values = {
        "name": storage_unit.name,
        "facility_id": storage_unit.facility_id,
        "unit_type": storage_unit.unit_type,
        "min_temp": storage_unit.min_temp,
        "max_temp": storage_unit.max_temp,
        "status": storage_unit.status,
    }

    storage_unit.name = storage_unit_data.name
    storage_unit.facility_id = storage_unit_data.facility_id
    storage_unit.unit_type = storage_unit_data.unit_type
    storage_unit.min_temp = storage_unit_data.min_temp
    storage_unit.max_temp = storage_unit_data.max_temp
    storage_unit.status = storage_unit_data.status
    storage_unit.last_service_date = storage_unit_data.last_service_date

    db.commit()
    db.refresh(storage_unit)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="UPDATE_STORAGE_UNIT",
        resource_type="StorageUnit",
        resource_id=str(storage_unit.id),
        old_values=old_values,
        new_values={
            "name": storage_unit.name,
            "facility_id": storage_unit.facility_id,
            "unit_type": storage_unit.unit_type,
            "min_temp": storage_unit.min_temp,
            "max_temp": storage_unit.max_temp,
            "status": storage_unit.status,
        }
    )

    return storage_unit


@router.delete("/{storage_unit_id}")
def delete_storage_unit(
    storage_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    storage_unit = db.query(StorageUnit).filter(
        StorageUnit.id == storage_unit_id
    ).first()

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    old_values = {
        "name": storage_unit.name,
        "facility_id": storage_unit.facility_id,
        "unit_type": storage_unit.unit_type,
        "min_temp": storage_unit.min_temp,
        "max_temp": storage_unit.max_temp,
        "status": storage_unit.status,
    }

    resource_id = str(storage_unit.id)

    db.delete(storage_unit)
    db.commit()

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="DELETE_STORAGE_UNIT",
        resource_type="StorageUnit",
        resource_id=resource_id,
        old_values=old_values
    )

    return {
        "message": "Storage unit deleted successfully"
    }