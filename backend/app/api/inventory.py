from app.services.audit_service import create_audit_log
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.inventory import Inventory
from app.models.storage_unit import StorageUnit
from app.models.user import User
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryStatusUpdate,
    InventoryUpdate,
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


def calculate_inventory_status(inventory: Inventory) -> str:
    if inventory.status == "Compromised":
        return "Compromised"

    if inventory.quantity <= 0:
        return "Depleted"

    if inventory.expiration_date <= date.today():
        return "Expired"

    return "Good"


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    inventory_items = db.query(Inventory).all()

    for item in inventory_items:
        item.status = calculate_inventory_status(item)

    return inventory_items


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    inventory.status = calculate_inventory_status(inventory)

    return inventory


@router.post("/", response_model=InventoryResponse)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    storage_unit = db.query(StorageUnit).filter(
        StorageUnit.id == inventory.storage_unit_id
    ).first()

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    new_inventory = Inventory(
        storage_unit_id=inventory.storage_unit_id,
        vaccine_name=inventory.vaccine_name,
        vaccine_code=inventory.vaccine_code,
        lot_number=inventory.lot_number,
        quantity=inventory.quantity,
        expiration_date=inventory.expiration_date,
        status="Good",
    )

    new_inventory.status = calculate_inventory_status(new_inventory)

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="CREATE",
        resource_type="Inventory",
        resource_id=str(new_inventory.id),
        new_values={
            "vaccine_name": new_inventory.vaccine_name,
            "vaccine_code": new_inventory.vaccine_code,
            "lot_number": new_inventory.lot_number,
            "quantity": new_inventory.quantity,
            "status": new_inventory.status,
        },
    )

    return new_inventory


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    storage_unit = db.query(StorageUnit).filter(
        StorageUnit.id == inventory_data.storage_unit_id
    ).first()

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    inventory.storage_unit_id = inventory_data.storage_unit_id
    inventory.vaccine_name = inventory_data.vaccine_name
    inventory.vaccine_code = inventory_data.vaccine_code
    inventory.lot_number = inventory_data.lot_number
    inventory.quantity = inventory_data.quantity
    inventory.expiration_date = inventory_data.expiration_date

    inventory.status = calculate_inventory_status(inventory)

    db.commit()
    db.refresh(inventory)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="UPDATE",
        resource_type="Inventory",
        resource_id=str(inventory.id),
        new_values={
            "storage_unit_id": inventory.storage_unit_id,
            "vaccine_name": inventory.vaccine_name,
            "vaccine_code": inventory.vaccine_code,
            "lot_number": inventory.lot_number,
            "quantity": inventory.quantity,
            "expiration_date": str(inventory.expiration_date),
            "status": inventory.status,
        },
    )

    return inventory


@router.patch("/{inventory_id}/status", response_model=InventoryResponse)
def update_inventory_status(
    inventory_id: int,
    status_data: InventoryStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    if status_data.status != "Compromised":
        raise HTTPException(
            status_code=400,
            detail="Only Compromised status can be manually assigned"
        )

    inventory.status = "Compromised"

    db.commit()
    db.refresh(inventory)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="STATUS_CHANGE",
        resource_type="Inventory",
        resource_id=str(inventory.id),
        new_values={
            "status": inventory.status,
        },
    )

    return inventory


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    db.delete(inventory)
    db.commit()

    return {
        "message": "Inventory item deleted successfully"
    }