from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.seed import seed_if_empty
from app.routers import auth, marketplace, prices, storage, rentals, schemes

app = FastAPI(
    title="GreenMarket API",
    description="Backend API for GreenMarket — Farmer's Digital Marketplace",
    version="1.0.0",
)

origins = ["*"] if settings.cors_origins == "*" else [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(marketplace.router)
app.include_router(prices.router)
app.include_router(storage.router)
app.include_router(rentals.router)
app.include_router(schemes.router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "greenmarket-api", "version": app.version}


# Serve the frontend (index.html, marketplace.html, style.css, app.js, ...).
# Mounted last / at "/" so it only catches requests that don't match an
# /api/* route above.
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")
