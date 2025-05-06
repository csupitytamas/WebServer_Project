from fastapi import APIRouter, Depends
from app.db.connection import get_connection
from app.utils.jwt_helper import decode_jwt
from app.schemas.statisztika_schema import (
    HaviBevetelItem,
    LegtobbetFizeto,
    LegnezettebbDomain,
    LegaktivabbFelhasznalo
)
from typing import List

router = APIRouter(prefix="/api/stats", tags=["Statisztikák"])


@router.get("/havi-bevetel", response_model=List[HaviBevetelItem])
def get_havi_bevetel(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT honap, bevetel FROM view_havi_bevetel_stat")
            rows = cur.fetchall()
            return [{"honap": row[0], "bevetel": float(row[1])} for row in rows]


@router.get("/legtobbet-fizetok", response_model=List[LegtobbetFizeto])
def get_legtobbet_fizetok(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT felhasznalo_nev, osszes_fizetes FROM view_legtobbet_fizetok")
            rows = cur.fetchall()
            return [{"felhasznalo": row[0], "osszeg": float(row[1])} for row in rows]


@router.get("/legnezettebb-domain", response_model=List[LegnezettebbDomain])
def get_legnezettebb_domain(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT domain_nev, tulajdonos, megtekintes FROM view_legnezettebb_domain")
            rows = cur.fetchall()
            return [{"domain": row[0], "tulajdonos": row[1], "megtekintes": int(row[2])} for row in rows]


@router.get("/legaktivabb-felhasznalok", response_model=List[LegaktivabbFelhasznalo])
def get_legaktivabb_felhasznalok(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT felhasznalo, domainek_szama, webtarhelyek_szama, szamlak_szama
                FROM view_legaktivabb_felhasznalok
            """)
            rows = cur.fetchall()
            return [
                {
                    "felhasznalo": row[0],
                    "domainek": int(row[1]),
                    "webtarhelyek": int(row[2]),
                    "szamlak": int(row[3])
                }
                for row in rows
            ]