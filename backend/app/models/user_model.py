from pydantic import BaseModel, EmailStr
from typing import Optional

# ⬇️ Bemenethez regisztrációnál
class UserCreate(BaseModel):
    nev: str
    email: EmailStr
    jelszo: str

# ⬇️ Bejelentkezéshez
class UserLogin(BaseModel):
    email: EmailStr
    jelszo: str

# ⬇️ Kimenethez (jelszó és belső adatok nélkül)
class UserPublic(BaseModel):
    user_id: int
    nev: str
    email: EmailStr
    szerep: Optional[int] = None  # ha benne van az adatbázisban

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nev: str
    email: EmailStr
    jelszo: str
    szerep: int
