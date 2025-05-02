from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SzamlaCreate(BaseModel):
    osszeg: float
    u_id: Optional[int]
    all_id: Optional[int]

class SzamlaUpdate(BaseModel):
    osszeg: Optional[float]
    u_id: Optional[int]
    all_id: Optional[int]

class SzamlaOut(BaseModel):
    sz_id: int
    osszeg: float
    letrehozas_datuma: datetime
    u_id: Optional[int]
    all_id: Optional[int]

class SzamlaOutExtended(BaseModel):
    szamla_id: int
    osszeg: float
    letrehozas_datuma: str
    all_id: int
    allapot_nev: str
