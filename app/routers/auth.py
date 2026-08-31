from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, auth as auth_utils
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.mobile == payload.mobile).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this mobile number already exists")

    if payload.role not in [r.value for r in models.UserRole]:
        raise HTTPException(status_code=400, detail="Invalid role. Use farmer, buyer, or storage_owner")

    user = models.User(
        full_name=payload.full_name,
        mobile=payload.mobile,
        aadhar=payload.aadhar,
        password_hash=auth_utils.hash_password(payload.password),
        role=payload.role,
        state=payload.state,
        land_holding_acres=payload.land_holding_acres,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth_utils.create_access_token({"sub": str(user.id)})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.mobile == payload.mobile).first()
    if not user or not auth_utils.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect mobile number or password")

    token = auth_utils.create_access_token({"sub": str(user.id)})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return current_user
