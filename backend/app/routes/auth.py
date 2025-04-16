from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.utils.jwt_helper import create_access_token, verify_password
from app.db.connection import get_connection
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/register")
def register(user: User):
    hashed_password = pwd_context.hash(user.jelszo)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO felhasznalo (nev, email, jelszo, szerep, bejelentkezes_idopontja)
                VALUES (:1, :2, :3, :4, SYSDATE)
            """, [user.nev, user.email, hashed_password, user.Szerep])
            conn.commit()

            cur.execute("SELECT MAX(u_id) FROM felhasznalo")
            uj_id = cur.fetchone()[0]

    token = create_access_token({"sub": str(uj_id)})
    return {
        "message": "A regisztráció sikeres",
        "user_id": uj_id,
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/auth/login")
def login(email: str, password: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, jelszo FROM felhasznalo WHERE email = :email", [email])
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

            user_id, hashed_password = row
            if not verify_password(password, hashed_password):
                raise HTTPException(status_code=400, detail="Hibás email vagy jelszó")

    token = create_access_token({"sub": str(user_id)})
    return {
        "message": "Sikeres bejelentkezés",
        "access_token": token,
        "token_type": "bearer"
    }