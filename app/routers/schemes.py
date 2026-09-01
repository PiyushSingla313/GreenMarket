import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/schemes", tags=["Government Schemes"])


def _gen_reference(prefix: str) -> str:
    return f"{prefix}-{random.randint(10000, 99999)}"


@router.get("", response_model=List[schemas.SchemeOut])
def list_schemes(
    category: Optional[str] = None,  # income / insurance / credit / input / infra
    db: Session = Depends(get_db),
):
    query = db.query(models.Scheme)
    if category:
        query = query.filter(models.Scheme.category.ilike(category))
    return query.all()


@router.get("/{scheme_id}", response_model=schemas.SchemeOut)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme


@router.post("/{scheme_id}/apply", response_model=schemas.SchemeApplicationOut, status_code=201)
def apply_scheme(scheme_id: int, payload: schemas.SchemeApplicationCreate, db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    application = models.SchemeApplication(
        scheme_id=scheme_id,
        application_id=_gen_reference("KCC-S"),
        **payload.model_dump(),
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application
