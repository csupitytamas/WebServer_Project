from pydantic import BaseModel
from typing import Optional

class WebTarhelyCreate(BaseModel):
    allapot: int
    meret: int
    d_id: Optional[int] = None
    u_id: Optional[int] = None

class WebTarhelyUpdate(BaseModel):
    allapot: Optional[int] = None
    meret: Optional[int] = None
    d_id: Optional[int] = None
    u_id: Optional[int] = None

class WebTarhelyOut(BaseModel):
    w_id: int
    allapot: int
    meret: int
    d_id: Optional[int]
    u_id: Optional[int]

    class Config:
        from_attributes = True