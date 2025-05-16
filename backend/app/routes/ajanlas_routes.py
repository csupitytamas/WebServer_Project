from fastapi import APIRouter, Depends, HTTPException
from app.db.connection import get_connection
from app.utils.jwt_helper import decode_jwt
from app.schemas.ajanlas_schema import AjanlasOut

router = APIRouter()

@router.get("/api/ajanlas")
def ajanlas_dummy():
    return {"ajanlott": []}