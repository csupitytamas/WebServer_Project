from fastapi import APIRouter, Depends, HTTPException
from app.schemas.szamla_schema import SzamlaCreate, SzamlaUpdate, SzamlaOut, SzamlaOutExtended
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()


@router.get("/api/get_szamlak", response_model=list[SzamlaOut])
def list_szamlak(payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sz_id, osszeg, letrehozas_datuma, u_id, all_id
                FROM szamla
                WHERE u_id = :1
            """, [user_id])
            rows = cur.fetchall()
    return [
        {
            "sz_id": row[0],
            "osszeg": row[1],
            "letrehozas_datuma": row[2],
            "u_id": row[3],
            "all_id": row[4]
        } for row in rows
    ]


@router.post("/api/create_szamla", response_model=SzamlaOut)
def create_szamla(data: SzamlaCreate, payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
                VALUES (:1, SYSTIMESTAMP, :2, :3)
            """, [data.osszeg, user_id, data.all_id])
            conn.commit()
            cur.execute("""
                SELECT s.sz_id, s.osszeg, s.letrehozas_datuma, s.u_id, s.all_id, a.allapot_nev
                FROM szamla s
                JOIN allapot_tabla a ON s.all_id = a.all_id
                WHERE s.sz_id = (SELECT MAX(sz_id) FROM szamla)
            """)
            row = cur.fetchone()

    return {
        "sz_id": row[0],
        "osszeg": row[1],
        "letrehozas_datuma": row[2],
        "u_id": row[3],
        "all_id": row[4]
    }


@router.put("/api/update_szamla/{szamla_id}", response_model=SzamlaOut)
def update_szamla(szamla_id: int, data: SzamlaUpdate, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin frissíthet számlát.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM szamla WHERE sz_id = :1", [szamla_id])
            if cur.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="Számla nem található.")

            cur.execute("""
                UPDATE szamla
                SET osszeg = :1,
                    u_id = :2,
                    all_id = :3
                WHERE sz_id = :4
            """, [data.osszeg, data.u_id, data.all_id, szamla_id])
            conn.commit()

            cur.execute("SELECT sz_id, osszeg, letrehozas_datuma, u_id, all_id FROM szamla WHERE sz_id = :1", [szamla_id])
            row = cur.fetchone()

    return {
        "sz_id": row[0],
        "osszeg": row[1],
        "letrehozas_datuma": row[2],
        "u_id": row[3],
        "all_id": row[4]
    }


@router.delete("/api/delete_szamla/{szamla_id}")
def delete_szamla(szamla_id: int, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin törölhet számlát.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM szamla WHERE sz_id = :1", [szamla_id])
            conn.commit()
    return {"message": f"Számla (id={szamla_id}) törölve."}

@router.get("/api/my_szamlak", response_model=list[SzamlaOutExtended])
def get_my_szamlak(payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sz.sz_id, sz.osszeg, sz.letrehozas_datuma, sz.all_id, a.allapot_nev
                FROM szamla sz
                JOIN allapot_tabla a ON sz.all_id = a.all_id
                WHERE sz.u_id = :1
                ORDER BY sz.letrehozas_datuma DESC
            """, [user_id])
            result = cur.fetchall()

    return [
        SzamlaOutExtended(
            szamla_id=row[0],
            osszeg=row[1],
            letrehozas_datuma=str(row[2]),
            all_id=row[3],
            allapot_nev=row[4]
        ) for row in result
    ]