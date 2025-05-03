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

                # 2. Domainek ellenőrzése
                if len(data.domain_nevek) > max_domain:
                    raise HTTPException(status_code=400,
                                        detail="Több domaint választottál, mint amennyit a csomag enged")

                    # Lekérjük a domainek azonosítóit a neveik alapján
                cur.execute(
                    f"""
                                    SELECT d_id, domain_nev, allapot FROM domain
                                    WHERE domain_nev IN ({','.join([':{}'.format(i + 1) for i in range(len(data.domain_nevek))])})
                                    """,
                    data.domain_nevek
                )
                domain_results = cur.fetchall()
                if len(domain_results) != len(data.domain_nevek):
                    raise HTTPException(status_code=404, detail="Egy vagy több megadott domain nem található")

                domain_ids = []
                for row in domain_results:
                    d_id, domain_nev, allapot = row
                    if allapot != 0:
                        raise HTTPException(status_code=400, detail=f"A(z) {domain_nev} domain már foglalt")
                    domain_ids.append(d_id)

                for domain_id in domain_ids:
                    cur.execute("""
                                        UPDATE domain
                                        SET allapot = 1, u_id = :1, dij_id = :2
                                        WHERE d_id = :3
                                    """, [user_id, data.dijcsomag_id, domain_id])

                # 4. Webtárhely kiválasztása meglévőkből (ha kér tárhelyet)
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

                # 5. Számla létrehozása (állapot: 3 = Függőben)
                cur.execute("""
                    INSERT INTO szamla (osszeg, letrehozas_datuma, u_id, all_id)
                    VALUES (:1, SYSTIMESTAMP, :2, 3)
                """, [ar, user_id])
                cur.execute("SELECT MAX(sz_id) FROM szamla")
                szamla_id = cur.fetchone()[0]
                # 6. Előfizetés létrehozása
                cur.execute("""
                                  INSERT INTO elofizet (u_id, d_id, datum)
                                  VALUES (:1, :2, SYSTIMESTAMP)
                              """, [user_id, data.dijcsomag_id])

                conn.commit()

                return VasarlasOut(
                    message="A vásárlás sikeresen megtörtént.",
                    szamla_id=szamla_id,
                    domain_id=data.domain_id,
                    webtarhely_id=webtarhely_id
                )

            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Hiba a vásárlás során: {str(e)}")
