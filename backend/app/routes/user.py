from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import FelhasznaloCreate, FelhasznaloLogin
from app.crud.user import create_user, get_user_by_email
from app.utils.jwt_helper import verify_password, create_access_token
from app.config.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: FelhasznaloCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/login")
def login(user: FelhasznaloLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.jelszo, db_user.jelszo):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
