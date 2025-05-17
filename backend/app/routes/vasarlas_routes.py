from fastapi import APIRouter, Depends, HTTPException
import traceback
import logging

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
                # Díjcsomag lekérés
                cur.execute("SELECT ar, max_meret, max_domain FROM dijcsomag WHERE d_id = :1", [data.dijcsomag_id])
                dijcsomag = cur.fetchone()
                if not dijcsomag:
                    raise HTTPException(status_code=404, detail="Díjcsomag nem található")
                ar, max_meret, max_domain = dijcsomag

                # Előfizetés meglétének ellenőrzése az INSERT előtt!
                cur.execute("SELECT COUNT(*) FROM elofizet WHERE u_id = :1 AND d_id = :2", [user_id, data.dijcsomag_id])
                if cur.fetchone()[0] > 0:
                    raise HTTPException(status_code=400, detail="Már rendelkezel ezzel a díjcsomaggal.")

                # Domain beszúrás
                domain_ids = []
                for nev in data.domain_nevek:
                    print(f"Domain beszúrás: {nev}")
                    cur.execute("""
                        INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
                        VALUES (1, :1, 0, :2, :3)
                    """, [nev, user_id, data.dijcsomag_id])
                    conn.commit()

                    cur.execute("SELECT d_id FROM domain WHERE domain_nev = :1", [nev])
                    result = cur.fetchone()

                    if result:
                        domain_ids.append(result[0])
                    else:
                        print(f"Hiba: Nem található a beszúrt domain: {nev}")


                # Webtárhely foglalás
                webtarhely_id = None
                if data.meret:
                    if data.meret > max_meret:
                        raise HTTPException(status_code=400, detail="Túl nagy tárhelyet igényeltél")
                    
                    cur.execute("""
                            SELECT w_id
                            FROM webtarhely 
                            WHERE meret >= :1
                            ORDER BY meret
                        """, [data.meret])

                    result = cur.fetchone()
                    if not result:
                        raise HTTPException(status_code=404, detail="Nincs megfelelő szabad tárhely.")
                    webtarhely_id = result[0]
                    cur.execute("""
                        UPDATE webtarhely
                        SET allapot = 1, u_id = :1, d_id = :2, meret = :3
                        WHERE w_id = :4
                    """, [user_id, data.dijcsomag_id, data.meret, webtarhely_id])

                # Előfizetés beszúrása (trigger elvégzi a számla létrehozást)
                cur.execute("""
                    INSERT INTO elofizet (u_id, d_id, datum)
                    VALUES (:1, :2, SYSTIMESTAMP)
                """, [user_id, data.dijcsomag_id])

                # Commit a tranzakció végén!
                conn.commit()

                # Legutóbbi számla lekérdezése
                cur.execute("SELECT MAX(sz_id) FROM szamla WHERE u_id = :1", [user_id])
                szamla_id = cur.fetchone()[0]
                if not szamla_id:
                    raise HTTPException(status_code=500, detail="A számla nem készült el.")

                return VasarlasOut(
                    message="A vásárlás sikeresen megtörtént.",
                    szamla_id=int(szamla_id),
                    domain_ids=[int(d) for d in domain_ids],
                    webtarhely_id=int(webtarhely_id) if webtarhely_id else None
                )
            except Exception as e:
                conn.rollback()
                print("=== Vásárlási kivétel történt ===")
                print(traceback.format_exc())
                raise HTTPException(status_code=500, detail=f"Hiba a vásárlás során: {str(e)}")

