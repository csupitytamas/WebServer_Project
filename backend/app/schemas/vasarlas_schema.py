from pydantic import BaseModel
from typing import Optional, List

class VasarlasRequest(BaseModel):
    dijcsomag_id: int
    domain_nevek: Optional[List[str]] = []
    meret: Optional[int] = None

class VasarlasOut(BaseModel):
    message: str
    szamla_id: int
    domain_ids: Optional[List[int]] = []
    webtarhely_id: Optional[int] = None