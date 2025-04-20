from fastapi import APIRouter, HTTPException, Depends
from app.db.connection import get_connection
from app.schemas.dijcsomag_schema import  DijcsomagCreate, DijcsomagUpdate, DijcsomagOut
from app.utils.jwt_helper import decode_jwt

router = APIRouter()


@router.get("/api/get_dijcsomagok", response_model=list[DijcsomagOut])
def list_dijcsomagok():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT d_id, neve, ar, max_meret, max_domain FROM dijcsomag")
            rows = cur.fetchall()

    return [
        {
            "d_id": row[0],
            "neve": row[1],
            "ar": row[2],
            "max_meret": row[3],
            "max_domain": row[4]
        } for row in rows
    ]


@router.post("/api/create_dijcsomag", response_model=dict)
def create_dijcsomag(data: DijcsomagCreate, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin hozhat létre díjcsomagot.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO dijcsomag (neve, ar, max_meret, max_domain)
                VALUES (:1, :2, :3, :4)
            """, [data.neve, data.ar, data.max_meret, data.max_domain])
            conn.commit()

            cur.execute("""
                SELECT d_id, neve, ar, max_meret, max_domain
                FROM dijcsomag
                WHERE d_id = (SELECT MAX(d_id) FROM dijcsomag)
            """)
            row = cur.fetchone()

    return {
        "message": "Díjcsomag sikeresen létrehozva.",
        "d_id": row[0],
        "neve": row[1],
        "ar": row[2],
        "max_meret": row[3],
        "max_domain": row[4]
    }


@router.put("/api/update_dijcsomag/{d_id}", response_model=dict)
def update_dijcsomag(d_id: int, data: DijcsomagUpdate, payload: dict = Depends(decode_jwt)):

    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin módosíthat díjcsomagot.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM dijcsomag WHERE d_id = :1", [d_id])
            if cur.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="Nincs ilyen díjcsomag.")

            cur.execute("""
                UPDATE dijcsomag
                SET neve = :1, ar = :2, max_meret = :3, max_domain = :4
                WHERE d_id = :5
            """, [data.neve, data.ar, data.max_meret, data.max_domain, d_id])
            conn.commit()

            cur.execute("""
                SELECT d_id, neve, ar, max_meret, max_domain
                FROM dijcsomag
                WHERE d_id = :1
            """, [d_id])
            row = cur.fetchone()

    return {
        "message": "Díjcsomag frissítve.",
        "d_id": row[0],
        "neve": row[1],
        "ar": row[2],
        "max_meret": row[3],
        "max_domain": row[4]
    }


@router.delete("/api/delete_dijcsomag/{d_id}", response_model=dict)
def delete_dijcsomag(d_id: int, payload: dict = Depends(decode_jwt)):

    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin törölhet díjcsomagot.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM dijcsomag WHERE d_id = :1", [d_id])
            conn.commit()

    return {"message": f"Díjcsomag (id={d_id}) törölve."}