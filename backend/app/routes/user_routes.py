from typing import List
from fastapi import APIRouter, Path
from app.models.user_model import User
from app.db.connection import get_connection
from app.schemas.user_schema import UserOut

router = APIRouter()

@router.get("/users", response_model=List[UserOut])
def list_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, nev, email, szerep FROM felhasznalo")
            eredmeny = cur.fetchall()
    return [
        {"user_id": r[0], "nev": r[1], "email": r[2], "szerep": r[3]} for r in eredmeny
    ]
@router.get("/api/get_user/{user_id}")
def get_user(user_id: int = Path(..., description="A felhasználó azonosítója")):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT nev, email, jelszo, szerep FROM felhasznalo WHERE u_id = :id",
                [user_id]
            )
            row = cur.fetchone()
            if not row:
                return {"message": "Nincs ilyen felhasználó"}
    return {
        "user_id": user_id,
        "nev": row[0],
        "email": row[1],
        "jelszo": row[2],
        "szerep": row[3]
    }

@router.get("/api/get_by_name")
def get_by_name(name: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT u_id, nev, email, jelszo, szerep FROM felhasznalo WHERE nev = :name",
                [name]
            )
            row = cur.fetchone()
            if not row:
                return {"message": "Nincs ilyen nevű felhasználó"}
    return {
        "user_id": row[0],
        "nev": row[1],
        "email": row[2],
        "jelszo": row[3],
        "szerep": row[4]
    }

@router.put("/api/update_user/{user_id}")
def update_user(user_id: int, updated_user: User):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :id", [user_id])
            if cur.fetchone()[0] == 0:
                return {"message": "Nincs ilyen felhasználó"}

            cur.execute("""
                UPDATE felhasznalo
                SET nev = :1, email = :2, jelszo = :3, szerep = :4
                WHERE u_id = :5
            """, [updated_user.nev, updated_user.email, updated_user.jelszo, updated_user.Szerep, user_id])
            conn.commit()
    return {"message": "Felhasználó frissítve"}

@router.delete("/api/delete_user/{user_id}")
def delete_user(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :id", [user_id])
            if cur.fetchone()[0] == 0:
                return {"message": "Nincs ilyen felhasználó"}

            cur.execute("DELETE FROM felhasznalo WHERE u_id = :id", [user_id])
            conn.commit()
    return {"message": "Felhasználó törölve"}