from fastapi import APIRouter, Depends, HTTPException

from app.schemas.vasarlas_schema import VasarlasRequest, VasarlasOut
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()


@router.post("/api/vasarlas", response_model=VasarlasOut)
def vasarlas(data: VasarlasRequest, payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                # 1. Díjcsomag ellenőrzés
                cur.execute("SELECT ar, max_meret, max_domain FROM dijcsomag WHERE d_id = :1", [data.dijcsomag_id])
                dijcsomag = cur.fetchone()
                if not dijcsomag:
                    raise HTTPException(status_code=404, detail="Díjcsomag nem található")

                ar, max_meret, max_domain = dijcsomag

                # 2. ÚJ DOMAINEK LÉTREHOZÁSA (trigger ellenőrzi az egyediségüket)
                domain_ids = []
                for nev in data.domain_nevek:
                    cur.execute("""
                        INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
                        VALUES (1, :1, 0, :2, :3)
                    """, [nev, user_id, data.dijcsomag_id])
                    cur.execute("SELECT MAX(d_id) FROM domain")
                    domain_ids.append(cur.fetchone()[0])

                # 3. Webtárhely kiválasztása meglévőkből (ha kér tárhelyet)
                webtarhely_id = None
                if data.meret:
                    if data.meret > max_meret:
                        raise HTTPException(status_code=400, detail="Túl nagy webtárhelyet igényeltél")

                    cur.execute("""
                        SELECT w_id FROM webtarhely
                        WHERE allapot = 0 AND meret >= :1
                        FETCH FIRST 1 ROWS ONLY
                    """, [data.meret])
                    result = cur.fetchone()
                    if not result:
                        raise HTTPException(status_code=404, detail="Nincs megfelelő szabad webtárhely.")

                    webtarhely_id = result[0]

                    cur.execute("""
                        UPDATE webtarhely
                        SET allapot = 1, u_id = :1, d_id = :2, meret = :3
                        WHERE w_id = :4
                    """, [user_id, data.dijcsomag_id, data.meret, webtarhely_id])

                # 4. Előfizetés létrehozása → trigger automatikusan létrehozza a számlát
                cur.execute("""
                    INSERT INTO elofizet (u_id, d_id, datum)
                    VALUES (:1, :2, SYSTIMESTAMP)
                """, [user_id, data.dijcsomag_id])

                # 5. Visszakeressük a legutóbbi számla ID-t az adott felhasználóhoz
                cur.execute("""
                    SELECT MAX(sz_id)
                    FROM szamla
                    WHERE u_id = :1
                """, [user_id])
                szamla_id = cur.fetchone()[0]

                conn.commit()

                return VasarlasOut(
                    message="A vásárlás sikeresen megtörtént.",
                    szamla_id=szamla_id,
                    domain_ids=domain_ids,
                    webtarhely_id=webtarhely_id
                )

            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Hiba a vásárlás során: {str(e)}")

