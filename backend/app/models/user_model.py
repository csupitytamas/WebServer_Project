from pydantic import BaseModel

class User(BaseModel):
    nev: str
    email: str
    jelszo: str


class LoginUser(BaseModel):
    email: str
    password: str