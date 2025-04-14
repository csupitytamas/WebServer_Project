from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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
        orm_mode = True