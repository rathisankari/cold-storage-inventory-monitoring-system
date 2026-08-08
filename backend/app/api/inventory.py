from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    inventory = db.query(Inventory).all()
    return inventory


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    return inventory


@router.post("/", response_model=InventoryResponse)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    new_inventory = Inventory(
        storage_unit_id=inventory.storage_unit_id,
        vaccine_name=inventory.vaccine_name,
        vaccine_code=inventory.vaccine_code,
        lot_number=inventory.lot_number,
        quantity=inventory.quantity,
        expiration_date=inventory.expiration_date,
        status=inventory.status,
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory item not found"
        )

    inventory.storage_unit_id = inventory_data.storage_unit_id
    inventory.vaccine_name = inventory_data.vaccine_name
    inventory.vaccine_code = inventory_data.vaccine_code
    inventory.lot_number = inventory_data.lot_number
    inventory.quantity = inventory_data.quantity
    inventory.expiration_date = inventory_data.expiration_date
    inventory.status = inventory_data.status

    db.commit()
    db.refresh(inventory)

    return inventory