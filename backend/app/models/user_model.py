from pydantic import BaseModel

class User(BaseModel):
    nev: str
    email: str
    jelszo: str
    Szerep: int


