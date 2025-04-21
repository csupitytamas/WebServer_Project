from pydantic import BaseModel

class TudastarBase(BaseModel):
    t_id: int
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

class TudastarCreate(TudastarBase):
    t_id: int
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

class TudastarUpdate(TudastarBase):
    t_id: int
    kategoria: int = None
    kerdes_szoveg: str = None
    valasz_szoveg: str = None

class TudastarOut(TudastarBase):
    t_id: int
    kategoria: int
    kerdes_szoveg: str
    valasz_szoveg: str

    class Config:
        from_attributes = True