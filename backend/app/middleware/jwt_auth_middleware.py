"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import HTTPException, status
from app.utils.jwt_helper import decode_jwt


A middleware egy köztes réteg, amely lehetővé teszi a kérések és válaszok feldolgozását, mielőtt azok elérnék az alkalmazásunk logikáját.
A middleware segítségével ellenőrizhetjük a JWT tokeneket, és biztosíthatjuk, hogy csak a megfelelő jogosultságokkal rendelkező felhasználók férjenek hozzá az API végpontokhoz.
A JWTAuthMiddleware osztály a BaseHTTPMiddleware osztályból származik, és a dispatch metódust felülírja.
A dispatch metódusban ellenőrizzük a kérés fejlécét, és ha a kérés nem tartalmazza a megfelelő Authorization fejlécet, akkor HTTP 401-es hibát dobunk.
A middleware a FastAPI alkalmazásunk inicializálása során kerül beállításra, és minden kérés előtt lefut.



class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        try:
            if request.url.path.startswith("/auth") or request.url.path.startswith(
                    "/docs") or request.url.path.startswith(
                    "/openapi.json"):
                return await call_next(request)
            if request.url.path.startswith("/api"):
                auth_header = request.headers.get("Authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Missing or invalid Authorization header",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                token = auth_header.split(" ")[1]
                decode_jwt(token) 
            response = await call_next(request)
            return response
        
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail},
                headers=http_exc.headers,
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )
"""