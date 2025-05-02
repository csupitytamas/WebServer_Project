from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tudastar_schema import TudastarCreate, TudastarUpdate, TudastarOut
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()

@router.get("/api/tudastar", response_model=list[TudastarOut])
def list_tudastar():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT t_id, kategoria, kerdes_szoveg, valasz_szoveg FROM tudastar")
            rows = cur.fetchall()
    return [
        {
            "t_id": row[0],
            "kategoria": row[1],
            "kerdes_szoveg": row[2],
            "valasz_szoveg": row[3]
        } for row in rows
    ]


@router.post("/api/tudastar", response_model=TudastarOut)
def create_tudastar(data: TudastarCreate, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin adhat hozzá új kérdést.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tudastar (kategoria, kerdes_szoveg, valasz_szoveg)
                VALUES (:1, :2, :3)
            """, [data.kategoria, data.kerdes_szoveg, data.valasz_szoveg])
            conn.commit()

            cur.execute("""
                SELECT t_id, kategoria, kerdes_szoveg, valasz_szoveg
                FROM tudastar
                WHERE t_id = (SELECT MAX(t_id) FROM tudastar)
            """)
            row = cur.fetchone()

    return {
        "t_id": row[0],
        "kategoria": row[1],
        "kerdes_szoveg": row[2],
        "valasz_szoveg": row[3]
    }



@router.put("/api/tudastar/{t_id}", response_model=TudastarOut)
def update_tudastar(t_id: int, data: TudastarUpdate, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin módosíthat.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM tudastar WHERE t_id = :1", [t_id])
            if cur.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="A bejegyzés nem található.")

            cur.execute("""
                UPDATE tudastar
                SET kategoria = :1,
                    kerdes_szoveg = :2,
                    valasz_szoveg = :3
                WHERE t_id = :4
            """, [data.kategoria, data.kerdes_szoveg, data.valasz_szoveg, t_id])
            conn.commit()

            cur.execute("SELECT t_id, kategoria, kerdes_szoveg, valasz_szoveg FROM tudastar WHERE t_id = :1", [t_id])
            row = cur.fetchone()

    return {
        "t_id": row[0],
        "kategoria": row[1],
        "kerdes_szoveg": row[2],
        "valasz_szoveg": row[3]
    }



@router.delete("/api/tudastar/{t_id}")
def delete_tudastar(t_id: int, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin törölhet.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tudastar WHERE t_id = :1", [t_id])
            conn.commit()

    return {"message": f"Tudástár bejegyzés (id={t_id}) törölve."}
