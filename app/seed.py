"""
Seeds the database with the same demo data that is currently hardcoded
in the frontend's inline <script> blocks, so that swapping the frontend
over to fetch() calls produces an identical first-run experience.
"""
from sqlalchemy.orm import Session

from app import models


def seed_if_empty(db: Session) -> None:
    if db.query(models.Listing).count() == 0:
        _seed_listings(db)
    if db.query(models.MandiPrice).count() == 0:
        _seed_mandi_prices(db)
    if db.query(models.MSPPrice).count() == 0:
        _seed_msp(db)
    if db.query(models.ColdStorage).count() == 0:
        _seed_storage(db)
    if db.query(models.RentalMachine).count() == 0:
        _seed_machines(db)
    if db.query(models.Supply).count() == 0:
        _seed_supplies(db)
    if db.query(models.Scheme).count() == 0:
        _seed_schemes(db)
    db.commit()


def _seed_listings(db):
    rows = [
        dict(crop="Wheat", quantity=50, unit="Quintal", price=2150, price_per="Quintal",
             state="Punjab", district="Ludhiana", badge="Verified", category="grain",
             image="🌾", phone="98XXXXXXXX", farmer_name="Gurpreet Singh"),
        dict(crop="Tomato", quantity=200, unit="Kg", price=38, price_per="Kg",
             state="Maharashtra", district="Nashik", badge="Organic", category="veg",
             image="🍅", phone="97XXXXXXXX", farmer_name="Suresh Patil"),
        dict(crop="Basmati Rice", quantity=30, unit="Quintal", price=6800, price_per="Quintal",
             state="Haryana", district="Karnal", badge="Premium", category="grain",
             image="🌾", phone="96XXXXXXXX", farmer_name="Ramesh Kumar"),
        dict(crop="Onion", quantity=5000, unit="Kg", price=24, price_per="Kg",
             state="Maharashtra", district="Lasalgaon", badge="Fresh", category="veg",
             image="🧅", phone="95XXXXXXXX", farmer_name="Priya Deshmukh"),
        dict(crop="Soybean", quantity=20, unit="Quintal", price=4100, price_per="Quintal",
             state="MP", district="Indore", badge="Verified", category="oil",
             image="🫘", phone="94XXXXXXXX", farmer_name="Mohan Lal"),
        dict(crop="Potato", quantity=100, unit="Bag", price=16, price_per="Kg",
             state="UP", district="Agra", badge="Fresh", category="veg",
             image="🥔", phone="93XXXXXXXX", farmer_name="Rakesh Tiwari"),
        dict(crop="Masoor Dal", quantity=15, unit="Quintal", price=6200, price_per="Quintal",
             state="MP", district="Bhopal", badge="Verified", category="pulse",
             image="🫘", phone="92XXXXXXXX", farmer_name="Arun Sharma"),
        dict(crop="Mustard", quantity=25, unit="Quintal", price=5200, price_per="Quintal",
             state="Rajasthan", district="Alwar", badge="Organic", category="oil",
             image="🌻", phone="91XXXXXXXX", farmer_name="Hari Singh"),
        dict(crop="Mango (Alphonso)", quantity=500, unit="Kg", price=120, price_per="Kg",
             state="Maharashtra", district="Ratnagiri", badge="Premium", category="fruit",
             image="🥭", phone="90XXXXXXXX", farmer_name="Vijay More"),
        dict(crop="Chickpeas (Chana)", quantity=40, unit="Quintal", price=5500, price_per="Quintal",
             state="Gujarat", district="Rajkot", badge="Verified", category="pulse",
             image="🫘", phone="89XXXXXXXX", farmer_name="Bhavesh Patel"),
        dict(crop="Maize", quantity=80, unit="Quintal", price=1890, price_per="Quintal",
             state="AP", district="Chittor", badge="Fresh", category="grain",
             image="🌽", phone="88XXXXXXXX", farmer_name="Ravi Reddy"),
        dict(crop="Banana", quantity=2000, unit="Kg", price=25, price_per="Kg",
             state="Maharashtra", district="Jalgaon", badge="Verified", category="fruit",
             image="🍌", phone="87XXXXXXXX", farmer_name="Sunil Dhumal"),
    ]
    for r in rows:
        db.add(models.Listing(**r))


def _seed_mandi_prices(db):
    rows = [
        # grains
        dict(crop="Wheat", mandi="Khanna Mandi", state="Punjab", min_price=2050, max_price=2300, modal_price=2180, change_percent=4.2, unit="Quintal", category="grains"),
        dict(crop="Basmati Rice", mandi="Karnal APMC", state="Haryana", min_price=6500, max_price=7200, modal_price=6800, change_percent=1.8, unit="Quintal", category="grains"),
        dict(crop="Maize", mandi="Raipur Mandi", state="MP", min_price=1750, max_price=2050, modal_price=1890, change_percent=2.1, unit="Quintal", category="grains"),
        dict(crop="Jowar", mandi="Solapur APMC", state="Maharashtra", min_price=2800, max_price=3100, modal_price=2950, change_percent=-0.5, unit="Quintal", category="grains"),
        dict(crop="Bajra", mandi="Bikaner", state="Rajasthan", min_price=1800, max_price=2100, modal_price=1950, change_percent=1.2, unit="Quintal", category="grains"),
        dict(crop="Barley", mandi="Jaipur", state="Rajasthan", min_price=1600, max_price=1850, modal_price=1720, change_percent=0.8, unit="Quintal", category="grains"),
        # vegetables
        dict(crop="Tomato", mandi="Nashik APMC", state="Maharashtra", min_price=30, max_price=55, modal_price=42, change_percent=-1.5, unit="Kg", category="vegetables"),
        dict(crop="Onion", mandi="Lasalgaon", state="Maharashtra", min_price=20, max_price=35, modal_price=28, change_percent=6.8, unit="Kg", category="vegetables"),
        dict(crop="Potato", mandi="Agra", state="UP", min_price=12, max_price=22, modal_price=16, change_percent=3.4, unit="Kg", category="vegetables"),
        dict(crop="Brinjal", mandi="Guntur", state="AP", min_price=15, max_price=28, modal_price=20, change_percent=-2.1, unit="Kg", category="vegetables"),
        dict(crop="Cabbage", mandi="Shimla", state="HP", min_price=10, max_price=18, modal_price=14, change_percent=5.0, unit="Kg", category="vegetables"),
        dict(crop="Cauliflower", mandi="Varanasi", state="UP", min_price=18, max_price=30, modal_price=24, change_percent=2.5, unit="Kg", category="vegetables"),
        # fruits
        dict(crop="Mango (Alphonso)", mandi="Ratnagiri", state="Maharashtra", min_price=100, max_price=160, modal_price=120, change_percent=8.2, unit="Kg", category="fruits"),
        dict(crop="Banana", mandi="Jalgaon", state="Maharashtra", min_price=18, max_price=32, modal_price=25, change_percent=1.4, unit="Kg", category="fruits"),
        dict(crop="Pomegranate", mandi="Solapur", state="Maharashtra", min_price=80, max_price=140, modal_price=110, change_percent=-3.2, unit="Kg", category="fruits"),
        dict(crop="Grapes", mandi="Sangli", state="Maharashtra", min_price=40, max_price=80, modal_price=58, change_percent=4.5, unit="Kg", category="fruits"),
        dict(crop="Guava", mandi="Allahabad", state="UP", min_price=25, max_price=50, modal_price=35, change_percent=2.0, unit="Kg", category="fruits"),
        # pulses
        dict(crop="Chana Dal", mandi="Indore", state="MP", min_price=5200, max_price=5900, modal_price=5500, change_percent=1.5, unit="Quintal", category="pulses"),
        dict(crop="Masoor Dal", mandi="Kanpur", state="UP", min_price=5800, max_price=6600, modal_price=6200, change_percent=0.9, unit="Quintal", category="pulses"),
        dict(crop="Arhar Dal", mandi="Gulbarga", state="Karnataka", min_price=7000, max_price=8200, modal_price=7600, change_percent=-1.8, unit="Quintal", category="pulses"),
        dict(crop="Moong Dal", mandi="Nagpur", state="Maharashtra", min_price=7500, max_price=8500, modal_price=8000, change_percent=2.2, unit="Quintal", category="pulses"),
        dict(crop="Urad Dal", mandi="Hyderabad", state="Telangana", min_price=6500, max_price=7800, modal_price=7100, change_percent=-0.7, unit="Quintal", category="pulses"),
        # oilseeds
        dict(crop="Soybean", mandi="Indore", state="MP", min_price=3900, max_price=4600, modal_price=4200, change_percent=-0.8, unit="Quintal", category="oilseeds"),
        dict(crop="Mustard", mandi="Alwar", state="Rajasthan", min_price=4900, max_price=5600, modal_price=5200, change_percent=-1.1, unit="Quintal", category="oilseeds"),
        dict(crop="Sunflower", mandi="Bijapur", state="Karnataka", min_price=5400, max_price=6300, modal_price=5800, change_percent=2.9, unit="Quintal", category="oilseeds"),
        dict(crop="Groundnut", mandi="Rajkot", state="Gujarat", min_price=5500, max_price=6400, modal_price=5950, change_percent=1.6, unit="Quintal", category="oilseeds"),
        dict(crop="Sesame", mandi="Ahmedabad", state="Gujarat", min_price=12000, max_price=14000, modal_price=13000, change_percent=3.5, unit="Quintal", category="oilseeds"),
    ]
    for r in rows:
        db.add(models.MandiPrice(**r))


def _seed_msp(db):
    rows = [
        dict(crop="🌾 Wheat", price=2275, unit="/Quintal"),
        dict(crop="🌾 Paddy (Common)", price=2183, unit="/Quintal"),
        dict(crop="🌾 Maize", price=2090, unit="/Quintal"),
        dict(crop="🫘 Gram (Chana)", price=5440, unit="/Quintal"),
        dict(crop="🫘 Masoor Dal", price=6425, unit="/Quintal"),
        dict(crop="🌻 Mustard", price=5650, unit="/Quintal"),
        dict(crop="🌻 Sunflower", price=6760, unit="/Quintal"),
        dict(crop="🌻 Soybean", price=4600, unit="/Quintal"),
    ]
    for r in rows:
        db.add(models.MSPPrice(**r))


def _seed_storage(db):
    rows = [
        dict(name="Punjab State Cold Store", state="Punjab", district="Ludhiana", type="govt",
             capacity_tons=500, available_tons=280, temp_range="-2°C to 10°C", rate="₹8/kg/month",
             crops=["Potato", "Onion", "Wheat"], image="🏛️", rating=4.5),
        dict(name="Kisan Cold Hub", state="Haryana", district="Karnal", type="private",
             capacity_tons=300, available_tons=180, temp_range="0°C to 8°C", rate="₹12/kg/month",
             crops=["Tomato", "Vegetable", "Fruit"], image="❄️", rating=4.8),
        dict(name="Agri Cool Storage Ltd", state="Maharashtra", district="Nashik", type="private",
             capacity_tons=800, available_tons=320, temp_range="-5°C to 15°C", rate="₹10/kg/month",
             crops=["Grapes", "Onion", "Pomegranate"], image="🏢", rating=4.6),
        dict(name="NCCD Cold Warehouse", state="UP", district="Agra", type="govt",
             capacity_tons=1000, available_tons=650, temp_range="2°C to 12°C", rate="₹6/kg/month",
             crops=["Potato", "Apple", "Ginger"], image="🏛️", rating=4.2),
        dict(name="FreshStore Pvt Ltd", state="MP", district="Indore", type="private",
             capacity_tons=400, available_tons=100, temp_range="0°C to 10°C", rate="₹11/kg/month",
             crops=["Soybean", "Wheat", "Maize"], image="❄️", rating=4.7),
        dict(name="Rajasthan Agri Cold", state="Rajasthan", district="Jaipur", type="govt",
             capacity_tons=600, available_tons=400, temp_range="-3°C to 8°C", rate="₹7/kg/month",
             crops=["Onion", "Garlic", "Spices"], image="🏛️", rating=4.0),
        dict(name="GujCold Cooperative", state="Gujarat", district="Rajkot", type="private",
             capacity_tons=350, available_tons=220, temp_range="0°C to 12°C", rate="₹9/kg/month",
             crops=["Groundnut", "Cotton", "Mango"], image="❄️", rating=4.4),
        dict(name="Sahyadri Cold Park", state="Maharashtra", district="Pune", type="private",
             capacity_tons=700, available_tons=490, temp_range="-2°C to 10°C", rate="₹13/kg/month",
             crops=["Strawberry", "Grapes", "Flower"], image="🏢", rating=4.9),
    ]
    for r in rows:
        db.add(models.ColdStorage(**r))


def _seed_machines(db):
    rows = [
        dict(name="Mahindra 575 DI Tractor", description="45 HP tractor with power steering. Suitable for all soil types.",
             price_per_day=1200, availability="Available Now", category="tractor", image="🚜",
             state="Punjab", district="Ludhiana", color="#FFF3E0"),
        dict(name="John Deere 5310 Tractor", description="55 HP, GPS-enabled precision tractor. 4WD with cab.",
             price_per_day=1800, availability="Available in 2 days", category="tractor", image="🚜",
             state="Haryana", district="Karnal", color="#E8F5E9"),
        dict(name="Combine Harvester (Claas 370)", description="High-efficiency wheat & paddy harvester. Capacity 2 acres/hr.",
             price_per_day=3500, availability="Book in Advance", category="harvester", image="🌾",
             state="Punjab", district="Amritsar", color="#E3F2FD"),
        dict(name="Rice Transplanter", description="6-row self-propelled paddy transplanter.",
             price_per_day=2200, availability="Available Now", category="harvester", image="🌱",
             state="Bihar", district="Patna", color="#F3E5F5"),
        dict(name="Drip Irrigation Kit (1 Acre)", description="Complete drip system with pipes, emitters & filter for 1 acre.",
             price_per_day=800, availability="Available Now", category="irrigation", image="💧",
             state="MH", district="Nashik", color="#E3F2FD"),
        dict(name="Sprinkler System (1 Acre)", description="Portable sprinkler set with pump. Covers 1 acre per setup.",
             price_per_day=600, availability="Available Now", category="irrigation", image="🌊",
             state="GJ", district="Rajkot", color="#E3F2FD"),
        dict(name="Rotavator / Cultivator", description="3-point linkage rotavator. Suitable for seedbed preparation.",
             price_per_day=900, availability="Available Now", category="other", image="🔧",
             state="UP", district="Agra", color="#FFF3E0"),
        dict(name="Sprayer (Power)", description="16L power sprayer for pesticide/fertilizer application.",
             price_per_day=300, availability="Available Now", category="other", image="🧴",
             state="MH", district="Nagpur", color="#E8F5E9"),
    ]
    for r in rows:
        db.add(models.RentalMachine(**r))


def _seed_supplies(db):
    pesticides = [
        dict(name="Imidacloprid 17.8% SL", brand="By: Bayer CropScience", description="Systemic insecticide for sucking pests. 100ml treats 1 acre.", price=380, old_price=450, discount_label="16% OFF", unit="100ml bottle", supply_type="pesticide", category="insecticide", image="🐛", color="#FFF3E0"),
        dict(name="Chlorpyrifos 20% EC", brand="By: Rallis India", description="Broad-spectrum insecticide. Effective for soil & foliar pests.", price=220, old_price=280, discount_label="21% OFF", unit="500ml bottle", supply_type="pesticide", category="insecticide", image="🐛", color="#FFF3E0"),
        dict(name="Mancozeb 75% WP", brand="By: Indofil", description="Contact fungicide for blight, rust, and mildew diseases.", price=180, old_price=220, discount_label="18% OFF", unit="500g pack", supply_type="pesticide", category="fungicide", image="🍄", color="#F3E5F5"),
        dict(name="Carbendazim 50% WP", brand="By: BASF India", description="Systemic fungicide for wide range of fungal diseases.", price=280, old_price=340, discount_label="18% OFF", unit="500g pack", supply_type="pesticide", category="fungicide", image="🍄", color="#F3E5F5"),
        dict(name="Glyphosate 41% SL", brand="By: Monsanto", description="Non-selective post-emergent herbicide for weed control.", price=320, old_price=390, discount_label="18% OFF", unit="1 litre", supply_type="pesticide", category="herbicide", image="🌿", color="#E8F5E9"),
        dict(name="Atrazine 50% WP", brand="By: Crystal Crop", description="Pre-emergent herbicide for maize, sugarcane fields.", price=140, old_price=170, discount_label="18% OFF", unit="500g pack", supply_type="pesticide", category="herbicide", image="🌿", color="#E8F5E9"),
        dict(name="Neem Oil (Cold Pressed)", brand="By: Morarka Organic", description="Organic bio-pesticide. Safe for bees. USDA certified.", price=280, old_price=320, discount_label="13% OFF", unit="500ml", supply_type="pesticide", category="bio", image="🌱", color="#E3F2FD"),
        dict(name="Bacillus thuringiensis (Bt)", brand="By: Biostadt India", description="Biological insecticide targeting caterpillars and larvae.", price=350, old_price=420, discount_label="17% OFF", unit="500g", supply_type="pesticide", category="bio", image="🌱", color="#E3F2FD"),
    ]
    fertilizers = [
        dict(name="DAP (Di-Ammonium Phosphate)", brand="IFFCO", description="18-46-0 NPK ratio. Best for all Rabi crops before sowing.", price=1350, old_price=1500, discount_label="10% OFF", unit="50kg bag", supply_type="fertilizer", image="🌿", color="#E8F5E9"),
        dict(name="Urea (46% N)", brand="NFL India", description="Most used nitrogen fertilizer in India. Improves leaf growth.", price=266, old_price=300, discount_label="MRP Fixed", unit="45kg bag", supply_type="fertilizer", image="🧪", color="#FFF3E0"),
        dict(name="MOP (Potash)", brand="IPL India", description="0-0-60 NPK. Improves fruit quality and disease resistance.", price=1200, old_price=1400, discount_label="14% OFF", unit="50kg bag", supply_type="fertilizer", image="🌱", color="#F3E5F5"),
        dict(name="NPK 12:32:16 Complex", brand="Coromandel", description="Balanced complex fertilizer. Ideal for vegetable crops.", price=1450, old_price=1600, discount_label="9% OFF", unit="50kg bag", supply_type="fertilizer", image="⚗️", color="#E3F2FD"),
        dict(name="Vermicompost", brand="Organic India", description="100% organic vermicompost. Improves soil health naturally.", price=350, old_price=400, discount_label="13% OFF", unit="25kg bag", supply_type="fertilizer", image="🪱", color="#E8F5E9"),
        dict(name="Zinc Sulphate (ZnSO4)", brand="Aries Agro", description="Micronutrient fertilizer. Corrects zinc deficiency in soil.", price=180, old_price=210, discount_label="14% OFF", unit="1kg pack", supply_type="fertilizer", image="⚗️", color="#FFF3E0"),
    ]
    seeds = [
        dict(name="HYV Wheat (HD 3086)", brand="ICAR-IARI Certified", description="High yield variety. 55-60 q/ha. Short duration (130 days).", price=80, old_price=95, discount_label="16% OFF", unit="per kg", supply_type="seed", image="🌾", color="#FFF3E0"),
        dict(name="Basmati Rice (Pusa 1121)", brand="NSC Certified", description="Premium basmati. Long grain, high aroma. 130-day variety.", price=120, old_price=150, discount_label="20% OFF", unit="per kg", supply_type="seed", image="🌾", color="#E8F5E9"),
        dict(name="Hybrid Tomato (Syngenta)", brand="Syngenta India", description="Indeterminate hybrid. High yield, disease resistant, 60-day.", price=650, old_price=800, discount_label="19% OFF", unit="10g packet", supply_type="seed", image="🍅", color="#F3E5F5"),
        dict(name="Onion Seed (Bhima Raj)", brand="NHRDF Certified", description="Red onion variety. 110-day crop. Good storage quality.", price=1800, old_price=2100, discount_label="14% OFF", unit="per kg", supply_type="seed", image="🧅", color="#FFF3E0"),
        dict(name="Hybrid Maize (DKC 9141)", brand="Dekalb / Bayer", description="High yield 9 ton/ha. Drought tolerant, 100-day variety.", price=200, old_price=240, discount_label="17% OFF", unit="per kg", supply_type="seed", image="🌽", color="#E3F2FD"),
        dict(name="Soybean Seed (JS 335)", brand="ICAR Certified", description="Popular kharif soybean. 95-day variety, 30+ q/ha yield.", price=75, old_price=90, discount_label="17% OFF", unit="per kg", supply_type="seed", image="🫘", color="#E8F5E9"),
    ]
    for r in pesticides + fertilizers + seeds:
        db.add(models.Supply(**r))


def _seed_schemes(db):
    rows = [
        dict(icon="💰", name="PM-KISAN", fullname="Pradhan Mantri Kisan Samman Nidhi",
             badge="Central Govt", badge_color="#1565c0",
             description="Direct income support of ₹6,000 per year in three equal installments to all landholding farmer families.",
             benefit="₹6,000/year", who_can_apply="All Farmers", deadline="Ongoing", status="Active",
             tags=["Income Support", "Direct Benefit", "All States"], category="income"),
        dict(icon="🛡️", name="PM Fasal Bima Yojana", fullname="Pradhan Mantri Fasal Bima Yojana",
             badge="Central Govt", badge_color="#1565c0",
             description="Crop insurance scheme. Pay just 1.5-2% premium for Rabi crops and 2% for Kharif. Government pays the rest. Covers natural calamities, pest attacks, disease.",
             benefit="Up to full crop value", who_can_apply="All Crop Farmers", deadline="Kharif Season", status="Active",
             tags=["Crop Insurance", "Natural Disaster", "Subsidized Premium"], category="insurance"),
        dict(icon="🏦", name="Kisan Credit Card", fullname="KCC — Short Term Credit for Farmers",
             badge="Central Govt", badge_color="#1565c0",
             description="Credit up to ₹3 lakh at just 4% interest rate (after government subsidy). For seeds, fertilizers, pesticides, and farm equipment.",
             benefit="Up to ₹3 Lakh @ 4%", who_can_apply="Landholding Farmers", deadline="Ongoing", status="Active",
             tags=["Credit", "Low Interest", "Quick Disbursal"], category="credit"),
        dict(icon="🌱", name="Soil Health Card Scheme", fullname="Soil Health Card (SHC) Scheme",
             badge="Central Govt", badge_color="#1565c0",
             description="Free soil testing every 2 years. Get a card with nutrient status of your farm soil and recommendations for appropriate fertilizer dosage.",
             benefit="Free Soil Testing", who_can_apply="All Farmers", deadline="Ongoing", status="Active",
             tags=["Soil Health", "Free Service", "Fertilizer Advisory"], category="input"),
        dict(icon="💧", name="PM Krishi Sinchai Yojana", fullname="Pradhan Mantri Krishi Sinchai Yojana",
             badge="Central Govt", badge_color="#1565c0",
             description="Subsidy on micro-irrigation (drip & sprinkler). Up to 55% subsidy for small farmers, 45% for others. 'Per drop more crop' approach.",
             benefit="55% Subsidy (SF/MF)", who_can_apply="All Farmers", deadline="Ongoing", status="Active",
             tags=["Irrigation", "Drip/Sprinkler", "Water Conservation"], category="infra"),
        dict(icon="🏗️", name="Agriculture Infrastructure Fund", fullname="AIF — Post Harvest Management Scheme",
             badge="Central Govt", badge_color="#1565c0",
             description="Loans up to ₹2 crore at 3% interest subsidy for setting up post-harvest management infrastructure like cold stores, warehouses, sorting grading units.",
             benefit="₹2Cr Loan @ 3% Sub", who_can_apply="FPOs, Farmers, Startups", deadline="Ongoing", status="Active",
             tags=["Cold Storage", "Warehouse", "Post Harvest"], category="infra"),
        dict(icon="📱", name="e-NAM (National Agri Market)", fullname="Electronic National Agriculture Market",
             badge="Central Govt", badge_color="#1565c0",
             description="Online trading platform linking APMC mandis. Sell your produce through transparent online auction. Get the best price from buyers across India.",
             benefit="Better Prices via Auction", who_can_apply="Registered Farmers", deadline="Ongoing", status="Active",
             tags=["Digital Market", "Transparent Pricing", "Online Auction"], category="income"),
        dict(icon="🧑‍🤝‍🧑", name="FPO Promotion Scheme", fullname="Formation & Promotion of 10,000 FPOs",
             badge="Central Govt", badge_color="#1565c0",
             description="Join or form a Farmer Producer Organization. Get ₹18 lakh over 3 years for setup. Collective bargaining power, shared equipment, bulk buying.",
             benefit="₹18 Lakh Grant", who_can_apply="Farmer Groups (11+)", deadline="Ongoing", status="Active",
             tags=["Group Farming", "Collective Benefit", "Marketing"], category="income"),
        dict(icon="🌾", name="Paramparagat Krishi Vikas Yojana", fullname="PKVY — Organic Farming Scheme",
             badge="Central Govt", badge_color="#1565c0",
             description="Financial support for converting to organic farming. Get ₹50,000/ha over 3 years for certification, organic inputs, and training.",
             benefit="₹50,000/ha over 3 years", who_can_apply="Cluster of 50 Farmers", deadline="2024-25", status="Active",
             tags=["Organic Farming", "Certification", "Premium Markets"], category="input"),
        dict(icon="🏦", name="PM SVANidhi (Rural Extension)", fullname="Street Vendor Atmanirbhar Nidhi",
             badge="Central Govt", badge_color="#1565c0",
             description="Working capital loans up to ₹50,000 for small farmer vendors and agri entrepreneurs. Zero collateral required. Digital transactions rewarded.",
             benefit="Up to ₹50,000 Loan", who_can_apply="Small Vendors/Farmers", deadline="Ongoing", status="Active",
             tags=["Micro Credit", "No Collateral", "Digital Payment"], category="credit"),
        dict(icon="🌻", name="Mukhyamantri Krishi Aashirvaad Yojana", fullname="MKAY — Jharkhand State Scheme",
             badge="State Scheme", badge_color="#2e7d32",
             description="₹5,000 per acre per year income support for small and marginal farmers of Jharkhand owning upto 5 acres of agricultural land.",
             benefit="₹5,000/acre/year", who_can_apply="Farmers in Jharkhand", deadline="Ongoing", status="Active",
             tags=["Income Support", "State Scheme", "Jharkhand"], category="income"),
        dict(icon="🌾", name="RKVY (Agriculture Development)", fullname="Rashtriya Krishi Vikas Yojana",
             badge="Central Govt", badge_color="#1565c0",
             description="Comprehensive scheme for agriculture development. Covers allied sectors, horticulture, livestock, and fisheries. Grants for innovative projects.",
             benefit="Project-based Grants", who_can_apply="Farmers, FPOs, Startups", deadline="Annual", status="Active",
             tags=["Agriculture Dev", "Allied Sectors", "Innovation"], category="infra"),
    ]
    for r in rows:
        db.add(models.Scheme(**r))
