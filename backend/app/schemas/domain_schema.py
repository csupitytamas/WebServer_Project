from pydantic import BaseModel
from typing import Optional

# Új domain létrehozásához – amit az űrlapból küld a felhasználó
class DomainCreate(BaseModel):
    allapot: int
    domain_nev: str
    megtekintes: int
    dij_id: Optional[int] = None
    u_id: Optional[int] = None

# Frissítéshez (opcionális mezőkkel, ha nem akarja mindet megadni)
class DomainUpdate(BaseModel):
    allapot: Optional[int] = None
    domain_nev: Optional[str] = None
    megtekintes: Optional[int] = None
    dij_id: Optional[int] = None
    u_id: Optional[int] = None

# Kimeneti (response) séma listázáshoz vagy lekéréshez
class DomainOut(BaseModel):
    d_id: int
    allapot: int
    domain_nev: str
    megtekintes: int
    u_id: Optional[int] = None
    dij_id: Optional[int] = None

    class Config:
        from_attributes = True