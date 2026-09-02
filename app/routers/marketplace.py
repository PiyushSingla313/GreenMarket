from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user_optional
from app.database import get_db

router = APIRouter(prefix="/api/listings", tags=["Marketplace"])


@router.get("", response_model=List[schemas.ListingOut])
def list_listings(
    category: Optional[str] = None,     # grain / veg / fruit / pulse / oil
    state: Optional[str] = None,
    search: Optional[str] = None,        # matches crop name or location
    sort: Optional[str] = "newest",      # newest / price_asc / price_desc / qty_desc
    db: Session = Depends(get_db),
):
    query = db.query(models.Listing).filter(models.Listing.status == "active")

    if category:
        query = query.filter(models.Listing.category.ilike(category))
    if state:
        query = query.filter(models.Listing.state.ilike(state))
    if search:
        like = f"%{search}%"
        query = query.filter(
            (models.Listing.crop.ilike(like)) | (models.Listing.district.ilike(like))
        )

    if sort == "price_asc":
        query = query.order_by(models.Listing.price.asc())
    elif sort == "price_desc":
        query = query.order_by(models.Listing.price.desc())
    elif sort == "qty_desc":
        query = query.order_by(models.Listing.quantity.desc())
    else:
        query = query.order_by(models.Listing.created_at.desc())

    return query.all()


@router.get("/{listing_id}", response_model=schemas.ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("", response_model=schemas.ListingOut, status_code=201)
def create_listing(
    payload: schemas.ListingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional),
):
    listing = models.Listing(
        **payload.model_dump(),
        farmer_id=current_user.id if current_user else None,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}", status_code=204)
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_optional),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if current_user and listing.farmer_id and listing.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this listing")
    db.delete(listing)
    db.commit()
    return None


@router.post("/{listing_id}/contact", response_model=schemas.ContactEnquiryOut, status_code=201)
def contact_farmer(listing_id: int, payload: schemas.ContactEnquiryCreate, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    enquiry = models.ContactEnquiry(listing_id=listing_id, **payload.model_dump())
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry
