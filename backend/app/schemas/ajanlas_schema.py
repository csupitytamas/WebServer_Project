from pydantic import BaseModel

class AjanlasOut(BaseModel):
    d_id: int
    nev: str
    ar: float
    max_domain: int
    max_meret: int