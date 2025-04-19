from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nev: str
    email: EmailStr
    jelszo: str

class UserLogin(BaseModel):
    email: EmailStr
    jelszo: str

class UserUpdate(BaseModel):
    nev: str = None
    email: EmailStr = None
    jelszo: str = None


class UserOut(BaseModel):
    user_id: int
    nev: str
    email: EmailStr
    szerep: int

    class Config:
        from_attributes = True