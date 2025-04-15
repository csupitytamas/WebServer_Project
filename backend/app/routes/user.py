from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import FelhasznaloCreate, FelhasznaloLogin
from app.crud.user import create_user, get_user_by_email
from app.utils.jwt_helper import verify_password, create_access_token
from app.config.db import get_db

"""
A FastAPI routerek segítségével csoportosítjuk az API végpontokat.
A routerek lehetővé teszik, hogy a kódunk rendezettebb és karbantarthatóbb legyen.
A routerek segítségével külön fájlokba szervezhetjük az API végpontokat, és így könnyebben kezelhetjük a különböző funkciókat.
A routerek segítségével a FastAPI automatikusan generálja a Swagger dokumentációt, amely segít megérteni az API végpontokat és azok működését.
A routerek segítségével könnyen hozzáadhatunk új végpontokat, módosíthatjuk a meglévőket, és eltávolíthatjuk a feleslegeseket.

"""


# Swagger dokumentációhoz TAG beállítás
router = APIRouter(
    prefix="/auth",
    tags=["auth"]  # Ez alapján fog csoportosulni Swaggerben
)

@router.post(
    "/register",
    summary="Felhasználó regisztráció",
    description="Új felhasználó regisztrálása email + jelszó alapján.",
    response_model=dict
)
def register(user: FelhasznaloCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post(
    "/login",
    summary="Bejelentkezés",
    description="Felhasználó bejelentkezése és JWT token generálása.",
    response_model=dict
)
def login(user: FelhasznaloLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.jelszo, db_user.jelszo):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
