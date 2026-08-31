import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    farmer = "farmer"
    buyer = "buyer"
    storage_owner = "storage_owner"


# ---------------------------------------------------------------------------
# Users / Auth
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    mobile = Column(String, unique=True, index=True, nullable=False)
    aadhar = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.farmer, nullable=False)
    state = Column(String, nullable=True)
    land_holding_acres = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="farmer")


# ---------------------------------------------------------------------------
# Marketplace
# ---------------------------------------------------------------------------
class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)          # Quintal / Kg / Ton / Bag
    price = Column(Float, nullable=False)
    price_per = Column(String, nullable=False)      # Quintal / Kg / Ton
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    quality_grade = Column(String, nullable=True)   # A Grade / B Grade / Organic Certified
    badge = Column(String, nullable=True)            # Verified / Organic / Premium / Fresh
    category = Column(String, nullable=False)        # grain / veg / fruit / pulse / oil
    image = Column(String, default="🌾")
    description = Column(Text, nullable=True)
    phone = Column(String, nullable=False)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    farmer_name = Column(String, nullable=False)      # denormalized so it works w/o account
    status = Column(String, default="active")          # active / sold
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("User", back_populates="listings")
    enquiries = relationship("ContactEnquiry", back_populates="listing", cascade="all, delete-orphan")


class ContactEnquiry(Base):
    __tablename__ = "contact_enquiries"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    quantity_needed = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing", back_populates="enquiries")


# ---------------------------------------------------------------------------
# Live Mandi Prices
# ---------------------------------------------------------------------------
class MandiPrice(Base):
    __tablename__ = "mandi_prices"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, nullable=False)
    mandi = Column(String, nullable=False)
    state = Column(String, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    change_percent = Column(Float, nullable=False)
    unit = Column(String, nullable=False)             # Quintal / Kg
    category = Column(String, nullable=False)          # grains / vegetables / fruits / pulses / oilseeds
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MSPPrice(Base):
    __tablename__ = "msp_prices"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    season = Column(String, default="Rabi 2024-25")


# ---------------------------------------------------------------------------
# Cold Storage
# ---------------------------------------------------------------------------
class ColdStorage(Base):
    __tablename__ = "cold_storages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    type = Column(String, nullable=False)              # govt / private
    capacity_tons = Column(Float, nullable=False)
    available_tons = Column(Float, nullable=False)
    temp_range = Column(String, nullable=False)
    rate = Column(String, nullable=False)               # display string e.g. "₹8/kg/month"
    crops = Column(JSON, default=list)
    rating = Column(Float, default=4.5)
    image = Column(String, default="❄️")

    bookings = relationship("StorageBooking", back_populates="storage", cascade="all, delete-orphan")


class StorageBooking(Base):
    __tablename__ = "storage_bookings"

    id = Column(Integer, primary_key=True, index=True)
    storage_id = Column(Integer, ForeignKey("cold_storages.id"), nullable=False)
    from_date = Column(String, nullable=False)
    to_date = Column(String, nullable=False)
    crop = Column(String, nullable=False)
    quantity_tons = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    special_requirements = Column(Text, nullable=True)
    reference_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

    storage = relationship("ColdStorage", back_populates="bookings")


# ---------------------------------------------------------------------------
# Rentals (machinery)
# ---------------------------------------------------------------------------
class RentalMachine(Base):
    __tablename__ = "rental_machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price_per_day = Column(Float, nullable=False)
    unit = Column(String, default="day")
    availability = Column(String, nullable=False)        # "Available Now" / "Book in Advance" / ...
    category = Column(String, nullable=False)             # tractor / harvester / irrigation / other
    image = Column(String, default="🚜")
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    color = Column(String, default="#FFF3E0")

    bookings = relationship("RentalBooking", back_populates="machine", cascade="all, delete-orphan")


class RentalBooking(Base):
    __tablename__ = "rental_bookings"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("rental_machines.id"), nullable=False)
    from_date = Column(String, nullable=False)
    to_date = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    location = Column(String, nullable=False)
    acreage = Column(Float, nullable=True)
    reference_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("RentalMachine", back_populates="bookings")


# ---------------------------------------------------------------------------
# Supplies (pesticides / fertilizers / seeds)
# ---------------------------------------------------------------------------
class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    discount_label = Column(String, nullable=True)
    unit = Column(String, nullable=False)
    supply_type = Column(String, nullable=False)   # pesticide / fertilizer / seed
    category = Column(String, nullable=True)        # insecticide / fungicide / herbicide / bio (pesticides only)
    image = Column(String, default="🧪")
    color = Column(String, default="#FFF3E0")

    orders = relationship("SupplyOrder", back_populates="supply", cascade="all, delete-orphan")


class SupplyOrder(Base):
    __tablename__ = "supply_orders"

    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(Integer, ForeignKey("supplies.id"), nullable=False)
    quantity = Column(Integer, default=1)
    delivery_address = Column(Text, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    order_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="placed")
    created_at = Column(DateTime, default=datetime.utcnow)

    supply = relationship("Supply", back_populates="orders")


# ---------------------------------------------------------------------------
# Government Schemes
# ---------------------------------------------------------------------------
class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String, default="🏛️")
    name = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    badge = Column(String, nullable=False)           # "Central Govt" / "State Scheme"
    badge_color = Column(String, default="#1565c0")
    description = Column(Text, nullable=False)
    benefit = Column(String, nullable=False)
    who_can_apply = Column(String, nullable=False)
    deadline = Column(String, default="Ongoing")
    status = Column(String, default="Active")
    tags = Column(JSON, default=list)
    category = Column(String, nullable=False)          # income / insurance / credit / input / infra

    applications = relationship("SchemeApplication", back_populates="scheme", cascade="all, delete-orphan")


class SchemeApplication(Base):
    __tablename__ = "scheme_applications"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    aadhar = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    application_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="submitted")
    created_at = Column(DateTime, default=datetime.utcnow)

    scheme = relationship("Scheme", back_populates="applications")
