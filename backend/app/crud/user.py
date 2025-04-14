from sqlalchemy.orm import Session
from app.models.user import Felhasznalo
from app.schemas.user import FelhasznaloCreate
from app.utils.jwt_helper import hash_password, verify_password  # hash/verify funkciók

def get_user_by_email(db: Session, email: str):
    return db.query(Felhasznalo).filter(Felhasznalo.email == email).first()

def create_user(db: Session, user: FelhasznaloCreate):
    hashed_pw = hash_password(user.jelszo)
    db_user = Felhasznalo(
        nev=user.nev,
        email=user.email,
        jelszo=hashed_pw,
        szerep=0  # alapértelmezett szerep
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
