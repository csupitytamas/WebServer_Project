from fastapi import FastAPI, Path
from pydantic import BaseModel
import oracledb
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

class User(BaseModel):
    nev: str
    email: str
    jelszo: str
    Szerep: int


def get_connection():
    wallet_path = os.getenv("WALLET_PATH")
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn="webtarhely_high",
        config_dir=wallet_path,
        wallet_location=wallet_path,
        wallet_password=os.getenv("WALLET_PASSWORD")
    )


@app.get("/")
def root():
    return {"message": "API elérhető"}


@app.get("/test_oracle")
def test_oracle():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 'Kapcsolat sikeres!' FROM dual")
            eredmeny = cur.fetchone()[0]
    return {"uzenet": eredmeny}


@app.get("/felhasznalok")
def list_felhasznalok():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, nev, email, szerep FROM felhasznalo")
            eredmeny = cur.fetchall()
    return {"felhasznalok": [
        {"id": r[0], "nev": r[1], "email": r[2], "szerep": r[3]} for r in eredmeny
    ]}


@app.get("/get_user/{user_id}")
def get_user(user_id: int = Path(..., description="A felhasználó azonosítója")):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nev, email, jelszo, szerep FROM felhasznalo WHERE u_id = :id", [user_id])
            row = cur.fetchone()
            if not row:
                return {"message": "Nincs ilyen felhasználó"}
    return {"user_id": user_id, "nev": row[0], "email": row[1], "jelszo": row[2], "szerep": row[3]}


@app.get("/get_by_name")
def get_by_name(name: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT u_id, nev, email, jelszo, szerep FROM felhasznalo WHERE nev = :name", [name])
            row = cur.fetchone()
            if not row:
                return {"message": "Nincs ilyen nevű felhasználó"}
    return {"user_id": row[0], "nev": row[1], "email": row[2], "jelszo": row[3], "szerep": row[4]}


@app.post("/add_user")
def add_user(user: User):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO felhasznalo (nev, email, jelszo, szerep, bejelentkezes_idopontja)
                VALUES (:1, :2, :3, :4, SYSDATE)
            """, [user.nev, user.email, user.jelszo, user.Szerep])
            conn.commit()

            cur.execute("SELECT MAX(u_id) FROM felhasznalo")
            uj_id = cur.fetchone()[0]

    return {"message": "Felhasználó hozzáadva", "user_id": uj_id}

@app.put("/update_user/{user_id}")
def update_user(user_id: int, updated_user: User):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :id", [user_id])
            if cur.fetchone()[0] == 0:
                return {"message": "Nincs ilyen felhasználó"}

            cur.execute("""
                UPDATE felhasznalo SET
                    nev = :1,
                    email = :2,
                    jelszo = :3,
                    szerep = :4
                WHERE u_id = :5
            """, [updated_user.nev, updated_user.email, updated_user.jelszo, updated_user.Szerep, user_id])
            conn.commit()
    return {"message": "Felhasználó frissítve"}


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :id", [user_id])
            if cur.fetchone()[0] == 0:
                return {"message": "Nincs ilyen felhasználó"}

            cur.execute("DELETE FROM felhasznalo WHERE u_id = :id", [user_id])
            conn.commit()
    return {"message": "Felhasználó törölve"}