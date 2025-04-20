from pydantic import BaseModel
from typing import Optional

class DijcsomagBase(BaseModel):
    neve: str
    ar: int
    max_meret: int
    max_domain: int

class DijcsomagCreate(DijcsomagBase):
    neve: str
    ar: int
    max_meret: int
    max_domain: int

class DijcsomagUpdate(DijcsomagBase):
    neve: str
    ar: int
    max_meret: int
    max_domain: int

class DijcsomagOut(DijcsomagBase):
    d_id: int
    neve: str
    ar: int
    max_meret: int
    max_domain: None | int

    class Config:
        from_attributes = True
