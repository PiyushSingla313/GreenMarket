from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Auth / Users
# ---------------------------------------------------------------------------
class UserRegister(BaseModel):
    full_name: str
    mobile: str
    aadhar: Optional[str] = None
    password: str = Field(min_length=6)
    role: str = "farmer"           # farmer / buyer / storage_owner
    state: Optional[str] = None
    land_holding_acres: Optional[float] = None


class UserLogin(BaseModel):
    mobile: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    mobile: str
    role: str
    state: Optional[str] = None
    land_holding_acres: Optional[float] = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------------------------------------------------------------------------
# Marketplace listings
# ---------------------------------------------------------------------------
class ListingCreate(BaseModel):
    crop: str
    quantity: float
    unit: str = "Quintal"
    price: float
    price_per: str = "Quintal"
    state: str
    district: str
    quality_grade: Optional[str] = None
    badge: Optional[str] = "Fresh"
    category: str                     # grain / veg / fruit / pulse / oil
    image: Optional[str] = "🌾"
    description: Optional[str] = None
    phone: str
    farmer_name: str


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    crop: str
    quantity: float
    unit: str
    price: float
    price_per: str
    state: str
    district: str
    quality_grade: Optional[str] = None
    badge: Optional[str] = None
    category: str
    image: str
    description: Optional[str] = None
    phone: str
    farmer_name: str
    status: str
    created_at: datetime


class ContactEnquiryCreate(BaseModel):
    name: str
    phone: str
    quantity_needed: Optional[str] = None
    message: Optional[str] = None


class ContactEnquiryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    listing_id: int
    name: str
    phone: str
    quantity_needed: Optional[str] = None
    message: Optional[str] = None
    created_at: datetime


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------
class MandiPriceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    crop: str
    mandi: str
    state: str
    min_price: float
    max_price: float
    modal_price: float
    change_percent: float
    unit: str
    category: str
    updated_at: datetime


class MSPPriceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    crop: str
    price: float
    unit: str
    season: str


# ---------------------------------------------------------------------------
# Cold storage
# ---------------------------------------------------------------------------
class ColdStorageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    state: str
    district: str
    type: str
    capacity_tons: float
    available_tons: float
    temp_range: str
    rate: str
    crops: List[str]
    rating: float
    image: str


class StorageBookingCreate(BaseModel):
    from_date: str
    to_date: str
    crop: str
    quantity_tons: float
    name: str
    phone: str
    special_requirements: Optional[str] = None


class StorageBookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    storage_id: int
    from_date: str
    to_date: str
    crop: str
    quantity_tons: float
    name: str
    phone: str
    special_requirements: Optional[str] = None
    reference_id: str
    status: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Rentals
# ---------------------------------------------------------------------------
class RentalMachineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price_per_day: float
    unit: str
    availability: str
    category: str
    image: str
    state: str
    district: str
    color: str


class RentalBookingCreate(BaseModel):
    from_date: str
    to_date: str
    name: str
    phone: str
    location: str
    acreage: Optional[float] = None


class RentalBookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    machine_id: int
    from_date: str
    to_date: str
    name: str
    phone: str
    location: str
    acreage: Optional[float] = None
    reference_id: str
    status: str
    created_at: datetime


class SupplyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    brand: str
    description: str
    price: float
    old_price: Optional[float] = None
    discount_label: Optional[str] = None
    unit: str
    supply_type: str
    category: Optional[str] = None
    image: str
    color: str


class SupplyOrderCreate(BaseModel):
    quantity: int = 1
    delivery_address: str
    name: str
    phone: str


class SupplyOrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    supply_id: int
    quantity: int
    delivery_address: str
    name: str
    phone: str
    order_id: str
    status: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Schemes
# ---------------------------------------------------------------------------
class SchemeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    icon: str
    name: str
    fullname: str
    badge: str
    badge_color: str
    description: str
    benefit: str
    who_can_apply: str
    deadline: str
    status: str
    tags: List[str]
    category: str


class SchemeApplicationCreate(BaseModel):
    aadhar: str
    full_name: str
    mobile: str


class SchemeApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    scheme_id: int
    aadhar: str
    full_name: str
    mobile: str
    application_id: str
    status: str
    created_at: datetime
