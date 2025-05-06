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

router = APIRouter()


@router.get("/api/havi-bevetel", response_model=List[HaviBevetelItem])
def get_havi_bevetel(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT honap, bevetel FROM havi_bevetel_stat")
            rows = cur.fetchall()
            return [{"honap": row[0], "bevetel": float(row[1])} for row in rows]


@router.get("/api/legtobbet-fizetok", response_model=List[LegtobbetFizeto])
def get_legtobbet_fizetok(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT felhasznalo_nev, osszes_fizetes FROM legtobbet_fizetok")
            rows = cur.fetchall()
            return [{"felhasznalo": row[0], "osszeg": float(row[1])} for row in rows]


@router.get("/api/legnezettebb-domain", response_model=List[LegnezettebbDomain])
def get_legnezettebb_domain(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT domain_nev, tulajdonos, megtekintes FROM legnezettebb_domain")
            rows = cur.fetchall()
            return [{"domain": row[0], "tulajdonos": row[1], "megtekintes": int(row[2])} for row in rows]


@router.get("/api/legaktivabb-felhasznalok", response_model=List[str])
def get_legaktivabb_felhasznalok(payload: dict = Depends(decode_jwt)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT felhasznalo FROM legaktivabb_felhasznalok
            """)
            rows = cur.fetchall()
            return [row[0] for row in rows]