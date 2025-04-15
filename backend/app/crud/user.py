from sqlalchemy.orm import Session
from app.models.user import Felhasznalo
from app.schemas.user import FelhasznaloCreate
from app.utils.jwt_helper import hash_password, verify_password  # hash/verify funkciók

"""
A CRUD (Create, Read, Update, Delete) műveletek a felhasználók kezelésére szolgálnak.
A CRUD műveletek segítségével létrehozhatunk új felhasználókat, lekérdezhetjük a felhasználók adatait,
frissíthetjük a meglévő felhasználók adatait, és törölhetjük a felhasználókat.
A CRUD műveletek a FastAPI és SQLAlchemy segítségével valósulnak meg.
A CRUD műveletek a következő funkciókat tartalmazzák:
- get_user_by_email: lekérdezi a felhasználót email alapján
- create_user: új felhasználó létrehozása
- update_user: meglévő felhasználó frissítése
- delete_user: meglévő felhasználó törlése

"""



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
