from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_db

router=APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
def create_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email== payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    user = User(name=payload.name,email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "user created"}

@router.post("/login",response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}