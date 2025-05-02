from pydantic import BaseModel
from typing import List


class SzamlaInfo(BaseModel):
    szamla_id: int
    osszeg: float
    datum: str
    allapot_id: int
    allapot_nev: str


class ElofizetesInfo(BaseModel):
    dijcsomag_id: int
    nev: str


class MyAdatokOut(BaseModel):
    domainjeim: List[str]
    ossz_webtarhely_meret: int
    szamlak: List[SzamlaInfo]
    elofizetesek: List[ElofizetesInfo]