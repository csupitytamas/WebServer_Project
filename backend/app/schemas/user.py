from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

"""
A Schemakban a bemeneti és kimeneti adatokat definiáljuk.
A Pydantic könyvtár segítségével definiáljuk a bemeneti és kimeneti adatokat.
A bemeneti adatok a felhasználó által megadott adatok, amelyeket a FastAPI automatikusan validál.
A kimeneti adatok a válasz, amelyet az API visszaad a felhasználónak.
A FelhasznaloCreate a felhasználó regisztrációjához szükséges adatokat tartalmazza.
A FelhasznaloLogin a felhasználó bejelentkezéséhez szükséges adatokat tartalmazza.
A FelhasznaloOut a felhasználó adatait tartalmazza, amelyeket az API visszaad a felhasználónak.

"""


class FelhasznaloCreate(BaseModel):
    nev: str
    email: EmailStr
    jelszo: str

class FelhasznaloLogin(BaseModel):
    email: EmailStr
    jelszo: str

class FelhasznaloOut(BaseModel):
    u_id: int
    nev: str
    email: EmailStr
    szerep: int
    bejelentkezes_idopontja: Optional[datetime]

    class Config:
        from_attributes = True