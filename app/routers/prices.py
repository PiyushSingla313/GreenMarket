from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/prices", tags=["Prices"])


@router.get("/mandi", response_model=List[schemas.MandiPriceOut])
def mandi_prices(
    category: Optional[str] = None,   # grains / vegetables / fruits / pulses / oilseeds
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.MandiPrice)
    if category:
        query = query.filter(models.MandiPrice.category.ilike(category))
    if state:
        query = query.filter(models.MandiPrice.state.ilike(state))
    return query.order_by(models.MandiPrice.crop.asc()).all()


@router.get("/msp", response_model=List[schemas.MSPPriceOut])
def msp_prices(db: Session = Depends(get_db)):
    return db.query(models.MSPPrice).all()
