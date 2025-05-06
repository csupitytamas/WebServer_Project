from fastapi import APIRouter, Depends, HTTPException
from app.db.connection import get_connection
from app.utils.jwt_helper import decode_jwt
from app.schemas.ajanlas_schema import AjanlasOut

router = APIRouter()

@router.get("/api/ajanlas", response_model=AjanlasOut)
def get_ajanlas(payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT d_id, nev, ar, max_domain, max_meret
                FROM ajanlas
                WHERE u_id = :1
            """, [user_id])
            row = cur.fetchone()
            if row:
                return {
                    "d_id": row[0],
                    "nev": row[1],
                    "ar": float(row[2]),
                    "max_domain": int(row[3]),
                    "max_meret": int(row[4])
                }
            else:
                raise HTTPException(status_code=200, detail="Nincs elérhető ajánlás.")