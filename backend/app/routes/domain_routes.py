from fastapi import APIRouter, Depends, HTTPException, Path
from app.schemas.domain_schema import DomainCreate, DomainOut, DomainUpdate
from app.db.connection import get_connection
from app.utils.jwt_helper import decode_jwt

router = APIRouter()


@router.get("/api/get_domains", response_model=list[DomainOut])
def list_domains():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT d_id, allapot, domain_nev, megtekintes, u_id, dij_id FROM domain")
            domains = cur.fetchall()
    return [
        {
            "d_id": row[0],
            "allapot": row[1],
            "domain_nev": row[2],
            "megtekintes": row[3],
            "u_id": row[4],
            "dij_id": row[5]
        }
        for row in domains
    ]


@router.post("/api/create_domain", response_model=DomainCreate)
def create_domain(domain: DomainCreate, payload: dict = Depends(decode_jwt)):
    user_id = int(payload["sub"])  # ← Innen jön a user ID (ne frontendről)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO domain (allapot, domain_nev, megtekintes, u_id, dij_id)
                VALUES (:1, :2, :3, :4, :5)
            """, [
                domain.allapot,
                domain.domain_nev,
                domain.megtekintes,
                user_id,
                domain.dij_id
            ])
            conn.commit()

            cur.execute("""
                SELECT d_id, allapot, domain_nev, megtekintes, u_id, dij_id
                FROM domain
                WHERE d_id = (SELECT MAX(d_id) FROM domain)
            """)
            row = cur.fetchone()

    return {
        "d_id": row[0],
        "allapot": row[1],
        "domain_nev": row[2],
        "megtekintes": row[3],
        "u_id": row[4],
        "dij_id": row[5]
    }


@router.put("/api/update_domain/{domain_id}", response_model=DomainOut)
def update_domain(
    domain_id: int,
    updated_domain: DomainUpdate,
    payload: dict = Depends(decode_jwt)
):
    role = int(payload["role"])
    if role != 1:
        raise HTTPException(status_code=403, detail="Csak admin módosíthat domain-t.")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Validáld, hogy a domain létezik
            cur.execute("SELECT COUNT(*) FROM domain WHERE d_id = :1", [domain_id])
            if cur.fetchone()[0] == 0:
                raise HTTPException(status_code=404, detail="A domain nem található.")

            # Validáld, hogy a felhasználó létezik
            if updated_domain.u_id is not None:
                cur.execute("SELECT COUNT(*) FROM felhasznalo WHERE u_id = :1", [updated_domain.u_id])
                if cur.fetchone()[0] == 0:
                    raise HTTPException(status_code=400, detail="A megadott felhasználó (u_id) nem létezik.")

            # Validáld, hogy a díjcsomag létezik
            if updated_domain.dij_id is not None:
                cur.execute("SELECT COUNT(*) FROM dijcsomag WHERE d_id = :1", [updated_domain.dij_id])
                if cur.fetchone()[0] == 0:
                    raise HTTPException(status_code=400, detail="A megadott díjcsomag (dij_id) nem létezik.")

            # Frissítés
            cur.execute("""
                UPDATE domain
                SET allapot = :1,
                    domain_nev = :2,
                    megtekintes = :3,
                    u_id = :4,
                    dij_id = :5
                WHERE d_id = :6
            """, [
                updated_domain.allapot,
                updated_domain.domain_nev,
                updated_domain.megtekintes,
                updated_domain.u_id,
                updated_domain.dij_id,
                domain_id
            ])
            conn.commit()

            # Visszaolvasás
            cur.execute("""
                SELECT d_id, allapot, domain_nev, megtekintes, u_id, dij_id
                FROM domain
                WHERE d_id = :1
            """, [domain_id])
            row = cur.fetchone()

            return {
                "d_id": row[0],
                "allapot": row[1],
                "domain_nev": row[2],
                "megtekintes": row[3],
                "u_id": row[4],
                "dij_id": row[5]
            }

@router.delete("/api/delete_domain/{domain_id}")
def delete_domain(domain_id: int, payload: dict = Depends(decode_jwt)):
    role = int(payload["role"])
    if role != 1:
        raise HTTPException(status_code=403, detail="Csak admin törölhet domain-t.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM domain WHERE d_id = :1", [domain_id])
            conn.commit()
    return {"message": f"Domain (id={domain_id}) törölve."}