from fastapi import APIRouter, Depends, HTTPException
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()

@router.put("/api/fizetes/{szamla_id}")
def fizetes(szamla_id: int, payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Ellenőrizzük, hogy a számla a felhasználóhoz tartozik-e és nincs-e már kifizetve vagy megfelelő az állapot.
            cur.execute("""
                SELECT all_id FROM szamla
                WHERE sz_id = :1 AND u_id = :2
            """, [szamla_id, user_id])
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Nincs ilyen számlád.")

            if row[0] != 3:
                raise HTTPException(status_code=400, detail="Csak függőben lévő számlát lehet kifizetni.")

            if row[0] == 4:
                raise HTTPException(status_code=400, detail="Ez a számla már ki van fizetve.")


            cur.execute("""
                UPDATE szamla
                SET all_id = 4
                WHERE sz_id = :1
            """, [szamla_id])
            conn.commit()

    return {"message": "A számla sikeresen kifizetve (lezárva)."}
