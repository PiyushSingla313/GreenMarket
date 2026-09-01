import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/storage", tags=["Cold Storage"])


def _gen_reference(prefix: str) -> str:
    return f"{prefix}-{random.randint(10000, 99999)}"


@router.get("", response_model=List[schemas.ColdStorageOut])
def list_storage(
    type: Optional[str] = None,      # govt / private
    state: Optional[str] = None,
    crop: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.ColdStorage)
    if type:
        query = query.filter(models.ColdStorage.type.ilike(type))
    if state:
        query = query.filter(models.ColdStorage.state.ilike(state))
    results = query.all()
    if crop:
        results = [s for s in results if any(crop.lower() in c.lower() for c in s.crops)]
    return results


@router.get("/{storage_id}", response_model=schemas.ColdStorageOut)
def get_storage(storage_id: int, db: Session = Depends(get_db)):
    storage = db.query(models.ColdStorage).filter(models.ColdStorage.id == storage_id).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    return storage


@router.post("/{storage_id}/book", response_model=schemas.StorageBookingOut, status_code=201)
def book_storage(storage_id: int, payload: schemas.StorageBookingCreate, db: Session = Depends(get_db)):
    storage = db.query(models.ColdStorage).filter(models.ColdStorage.id == storage_id).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    if payload.quantity_tons > storage.available_tons:
        raise HTTPException(status_code=400, detail="Requested quantity exceeds available capacity")

    booking = models.StorageBooking(
        storage_id=storage_id,
        reference_id=_gen_reference("KCC"),
        **payload.model_dump(),
    )
    storage.available_tons -= payload.quantity_tons
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
