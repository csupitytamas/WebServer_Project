from fastapi import APIRouter, HTTPException
from app.models.user_model import UserCreate, UserLogin, UserPublic
from app.utils.jwt_helper import create_access_token, verify_password
from app.db.connection import get_connection
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/register", response_model=UserPublic)
def register(user: UserCreate):
    hashed_password = pwd_context.hash(user.jelszo)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE email = :1", [user.email])
            if cur.fetchone()[0] > 0:
                raise HTTPException(status_code=400, detail="Ez az email már foglalt.")

            cur.execute("""
                INSERT INTO felhasznalo (nev, email, jelszo, szerep, bejelentkezes_idopontja)
                VALUES (:1, :2, :3, 0, SYSDATE)
            """, [user.nev, user.email, hashed_password])
            conn.commit()

            cur.execute("SELECT MAX(u_id) FROM felhasznalo")
            uj_id = cur.fetchone()[0]

    return UserPublic(
        user_id=uj_id,
        nev=user.nev,
        email=user.email,
        szerep=0
    )

@router.post("/auth/login")
def login(login_data: UserLogin):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, jelszo FROM felhasznalo WHERE email = :1", [login_data.email])
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

            user_id, hashed_password = row
            if not verify_password(login_data.jelszo, hashed_password):
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

    token = create_access_token({"sub": str(user_id)})
    return {
        "message": "Sikeres bejelentkezés",
        "access_token": token
    }
