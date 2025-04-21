from pydantic import BaseModel

class TudastarBase(BaseModel):
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

class TudastarCreate(TudastarBase):
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

class TudastarUpdate(TudastarBase):
    kategoria: int = None
    kerdes_szoveg: str = None
    valasz_szoveg: str = None

class TudastarOut(TudastarBase):
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

    class Config:
        from_attributes = True