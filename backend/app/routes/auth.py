from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.jwt_helper import create_access_token, verify_password
from app.db.connection import get_connection
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/register")
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

    # 0-szerep alapértelmezett
    token = create_access_token({"sub": str(uj_id), "role": 0})
    return {
        "message": "A regisztráció sikeres",
        "user_id": uj_id,
        "access_token": token
    }


@router.post("/auth/login")
def login(login_data: UserLogin):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, jelszo, szerep FROM felhasznalo WHERE email = :1", [login_data.email])
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

            user_id, hashed_password, szerep = row
            if not verify_password(login_data.jelszo, hashed_password):
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

            cur.execute("BEGIN bejelentkezes_idopont_frissitese(:1); END;", [user_id])
            conn.commit()

    token = create_access_token({"sub": str(user_id), "role": szerep})
    return {
        "message": "Sikeres bejelentkezés",
        "access_token": token
    }
