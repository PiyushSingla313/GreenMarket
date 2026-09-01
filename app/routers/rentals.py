import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/rentals", tags=["Rentals & Supplies"])


def _gen_reference(prefix: str) -> str:
    return f"{prefix}-{random.randint(10000, 99999)}"


# ---------------------------------------------------------------------------
# Machinery
# ---------------------------------------------------------------------------
@router.get("/machines", response_model=List[schemas.RentalMachineOut])
def list_machines(
    category: Optional[str] = None,   # tractor / harvester / irrigation / other
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.RentalMachine)
    if category:
        query = query.filter(models.RentalMachine.category.ilike(category))
    if state:
        query = query.filter(models.RentalMachine.state.ilike(state))
    return query.all()


@router.post("/machines/{machine_id}/book", response_model=schemas.RentalBookingOut, status_code=201)
def book_machine(machine_id: int, payload: schemas.RentalBookingCreate, db: Session = Depends(get_db)):
    machine = db.query(models.RentalMachine).filter(models.RentalMachine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    booking = models.RentalBooking(
        machine_id=machine_id,
        reference_id=_gen_reference("KCC-R"),
        **payload.model_dump(),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------------------------------
# Supplies (pesticides / fertilizers / seeds)
# ---------------------------------------------------------------------------
@router.get("/supplies", response_model=List[schemas.SupplyOut])
def list_supplies(
    supply_type: Optional[str] = None,   # pesticide / fertilizer / seed
    category: Optional[str] = None,       # insecticide / fungicide / herbicide / bio (pesticides only)
    db: Session = Depends(get_db),
):
    query = db.query(models.Supply)
    if supply_type:
        query = query.filter(models.Supply.supply_type.ilike(supply_type))
    if category:
        query = query.filter(models.Supply.category.ilike(category))
    return query.all()


@router.post("/supplies/{supply_id}/order", response_model=schemas.SupplyOrderOut, status_code=201)
def order_supply(supply_id: int, payload: schemas.SupplyOrderCreate, db: Session = Depends(get_db)):
    supply = db.query(models.Supply).filter(models.Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Product not found")

    order = models.SupplyOrder(
        supply_id=supply_id,
        order_id=_gen_reference("KCC-O"),
        **payload.model_dump(),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
