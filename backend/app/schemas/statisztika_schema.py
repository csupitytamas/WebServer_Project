from pydantic import BaseModel
from typing import List


class HaviBevetelItem(BaseModel):
    honap: str
    bevetel: float


class LegtobbetFizeto(BaseModel):
    felhasznalo: str
    osszeg: float


class LegnezettebbDomain(BaseModel):
    domain: str
    tulajdonos: str
    megtekintes: int


class LegaktivabbFelhasznalo(BaseModel):
    felhasznalo: str
    domainek: int
    webtarhelyek: int
    szamlak: int