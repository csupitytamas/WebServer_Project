from fastapi import APIRouter, Depends, HTTPException
from app.schemas.webtarhely_schema import WebTarhelyCreate, WebTarhelyUpdate, WebTarhelyOut
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()


@router.get("/api/get_webtarhelyek", response_model=list[WebTarhelyOut])
def list_webtarhelyek():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT w_id, allapot, meret, d_id, u_id FROM webtarhely")
            rows = cur.fetchall()
    return [
        {
            "w_id": row[0],
            "allapot": row[1],
            "meret": row[2],
            "d_id": row[3],
            "u_id": row[4]
        } for row in rows
    ]


@router.post("/api/create_webtarhely", response_model=WebTarhelyOut)
def create_webtarhely(data: WebTarhelyCreate, payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin hozhat létre webtárhelyet.")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO webtarhely (allapot, meret, d_id, u_id)
                VALUES (:1, :2, :3, :4)
            """, [data.allapot, data.meret, data.d_id, user_id])
            conn.commit()
            cur.execute("""
                SELECT w_id, allapot, meret, d_id, u_id
                FROM webtarhely
                WHERE w_id = (SELECT MAX(w_id) FROM webtarhely)
            """)
            row = cur.fetchone()

    return {
        "w_id": row[0],
        "allapot": row[1],
        "meret": row[2],
        "d_id": row[3],
        "u_id": row[4]
    }


@router.put("/api/update_webtarhely/{webtarhely_id}", response_model=WebTarhelyOut)
def update_webtarhely(webtarhely_id: int, data: WebTarhelyUpdate, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin frissíthet webtárhelyet.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM webtarhely WHERE w_id = :1", [webtarhely_id])
            if cur.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="A webtárhely nem található.")

            if data.u_id is not None:
                cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :1", [data.u_id])
                if cur.fetchone()[0] == 0:
                    raise HTTPException(status_code=400, detail="A megadott felhasználó nem létezik.")

            if data.d_id is not None:
                cur.execute("SELECT COUNT(*) FROM dijcsomag WHERE d_id = :1", [data.d_id])
                if cur.fetchone()[0] == 0:
                    raise HTTPException(status_code=400, detail="A megadott díjcsomag nem létezik.")

            cur.execute("""
                UPDATE webtarhely
                SET allapot = :1,
                    meret = :2,
                    d_id = :3,
                    u_id = :4
                WHERE w_id = :5
            """, [
                data.allapot, data.meret,
                data.d_id, data.u_id, webtarhely_id
            ])
            conn.commit()

            cur.execute("SELECT w_id, allapot, meret, d_id, u_id FROM webtarhely WHERE w_id = :1", [webtarhely_id])
            row = cur.fetchone()

    return {
        "w_id": row[0],
        "allapot": row[1],
        "meret": row[2],
        "d_id": row[3],
        "u_id": row[4]
    }


@router.delete("/api/delete_webtarhely/{webtarhely_id}")
def delete_webtarhely(webtarhely_id: int, payload: dict = Depends(decode_jwt)):
    if int(payload["role"]) != 1:
        raise HTTPException(status_code=403, detail="Csak admin törölhet webtárhelyet.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM webtarhely WHERE w_id = :1", [webtarhely_id])
            conn.commit()
    return {"message": f"Webtárhely (id={webtarhely_id}) törölve."}
