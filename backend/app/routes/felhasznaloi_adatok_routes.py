from fastapi import APIRouter, Depends, HTTPException

from app.schemas.felhasznaloi_adatok_schema import MyAdatokOut
from app.utils.jwt_helper import decode_jwt
from app.db.connection import get_connection

router = APIRouter()

@router.get("/api/felhasznaloi_adatok", response_model=MyAdatokOut)
def get_my_adatok(payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Domainek
            cur.execute("SELECT domain_nev FROM domain WHERE u_id = :1", [user_id])
            domain_list = [row[0] for row in cur.fetchall()]

            # Webtárhely méret összege
            cur.execute("SELECT SUM(meret) FROM webtarhely WHERE u_id = :1", [user_id])
            meret_sum = cur.fetchone()[0] or 0

            # Számlák részletes listája
            cur.execute("""
                SELECT sz.sz_id, sz.osszeg, sz.letrehozas_datuma, sz.all_id, a.allapot_nev
                FROM szamla sz
                JOIN allapot_tabla a ON sz.all_id = a.all_id
                WHERE sz.u_id = :1
                ORDER BY sz.letrehozas_datuma DESC
            """, [user_id])
            szamlak = [
                {
                    "szamla_id": row[0],
                    "osszeg": row[1],
                    "datum": str(row[2]),
                    "allapot_id": row[3],
                    "allapot_nev": str(row[4])
                }
                for row in cur.fetchall()
            ]


            cur.execute("""
                SELECT d.d_id, d.neve
                FROM elofizet e
                JOIN dijcsomag d ON e.d_id = d.d_id
                WHERE e.u_id = :1
                      """, [user_id])
            elofizetesek = [ {"dijcsomag_id": row[0], "nev": row[1]}
                 for row in cur.fetchall()
]

    return MyAdatokOut(
        domainjeim=domain_list,
        ossz_webtarhely_meret=meret_sum,
        szamlak=szamlak,
        elofizetesek=elofizetesek
    )

